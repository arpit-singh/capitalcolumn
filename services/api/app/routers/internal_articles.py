"""Internal publishing API — used by the Python AI pipeline.

All endpoints require API key authentication via X-API-Key header.
"""

import math
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_api_key
from app.db.session import get_db
from app.models.api_key import APIKey
from app.models.audit import ActorType
from app.schemas.article import (
    ArticleCreatePayload,
    ArticleCreateResponse,
    ArticleResponse,
    ArticleSchedulePayload,
    ArticleUpdatePayload,
)
from app.services import article_service, audit_service

router = APIRouter(prefix="/internal", tags=["Internal Publishing"])


# ---------------------------------------------------------------------------
# API Key Authentication Dependency
# ---------------------------------------------------------------------------

async def verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
) -> APIKey:
    """Verify the API key from the X-API-Key header."""
    key_hash = hash_api_key(x_api_key)
    result = await db.execute(
        select(APIKey).where(APIKey.key_hash == key_hash, APIKey.is_active == True)
    )
    api_key = result.scalar_one_or_none()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")

    # Update last used timestamp
    api_key.last_used_at = datetime.now(timezone.utc)
    return api_key


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/articles", response_model=ArticleCreateResponse, status_code=201)
async def create_article(
    payload: ArticleCreatePayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """Create or update an article (idempotent on external_id).

    If external_id already exists, updates the existing article instead of
    creating a duplicate. Returns created=true for new, created=false for update.
    """
    article, created = await article_service.create_or_update_article(
        db, payload, str(api_key.id)
    )

    # Audit log
    await audit_service.log_action(
        db,
        actor_type=ActorType.api_key,
        actor_id=str(api_key.id),
        action="create" if created else "update",
        entity_type="article",
        entity_id=article.id,
        after_json={"title": article.title, "slug": article.slug, "status": article.status.value},
        ip_address=request.client.host if request.client else None,
    )

    public_url = None
    if article.status.value == "published":
        public_url = f"{settings.PUBLIC_SITE_URL}/news/{article.slug}"

    return ArticleCreateResponse(
        id=article.id,
        slug=article.slug,
        status=article.status.value,
        preview_url=f"{settings.PUBLIC_SITE_URL}/news/{article.slug}",
        public_url=public_url,
        created=created,
    )


@router.patch("/articles/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: UUID,
    payload: ArticleUpdatePayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """Partially update an existing article."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Apply updates
    update_data = payload.model_dump(exclude_unset=True)

    if "title" in update_data and update_data["title"]:
        article.title = update_data["title"]
        article.slug = await article_service.generate_unique_slug(
            update_data["title"], db, existing_id=article.id
        )

    if "dek" in update_data:
        article.dek = update_data["dek"]
    if "summary" in update_data:
        article.summary = update_data["summary"]
    if "body_markdown" in update_data and update_data["body_markdown"]:
        article.body_markdown = update_data["body_markdown"]
        article.reading_time_minutes = article_service._estimate_reading_time(update_data["body_markdown"])
    if "key_takeaways" in update_data:
        article.key_takeaways = update_data["key_takeaways"]
    if "correction_note" in update_data:
        article.correction_note = update_data["correction_note"]
        article.last_corrected_at = datetime.now(timezone.utc)

    # SEO
    if "seo" in update_data and update_data["seo"]:
        seo = payload.seo
        if seo.seo_title is not None:
            article.seo_title = seo.seo_title
        if seo.seo_description is not None:
            article.seo_description = seo.seo_description
        if seo.canonical_url is not None:
            article.canonical_url = seo.canonical_url
        if seo.noindex is not None:
            article.noindex = seo.noindex

    # AI metadata
    if "ai_metadata" in update_data and update_data["ai_metadata"]:
        ai = payload.ai_metadata
        if ai.is_ai_generated is not None:
            article.is_ai_generated = ai.is_ai_generated
        if ai.is_editor_reviewed is not None:
            article.is_editor_reviewed = ai.is_editor_reviewed

    await db.flush()

    # Audit
    await audit_service.log_action(
        db,
        actor_type=ActorType.api_key,
        actor_id=str(api_key.id),
        action="update",
        entity_type="article",
        entity_id=article.id,
        after_json={"updated_fields": list(update_data.keys())},
        ip_address=request.client.host if request.client else None,
    )

    # Reload with relationships
    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)


@router.post("/articles/{article_id}/publish", response_model=ArticleResponse)
async def publish_article(
    article_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """Publish an article — validates SEO fields and sets status to published."""
    try:
        article = await article_service.publish_article(db, article_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    await audit_service.log_action(
        db,
        actor_type=ActorType.api_key,
        actor_id=str(api_key.id),
        action="publish",
        entity_type="article",
        entity_id=article.id,
        ip_address=request.client.host if request.client else None,
    )

    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)


@router.post("/articles/{article_id}/schedule", response_model=ArticleResponse)
async def schedule_article(
    article_id: UUID,
    payload: ArticleSchedulePayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """Schedule an article for future publication."""
    try:
        article = await article_service.schedule_article(db, article_id, payload.scheduled_at)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    await audit_service.log_action(
        db,
        actor_type=ActorType.api_key,
        actor_id=str(api_key.id),
        action="schedule",
        entity_type="article",
        entity_id=article.id,
        after_json={"scheduled_at": payload.scheduled_at.isoformat()},
        ip_address=request.client.host if request.client else None,
    )

    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)

"""Admin API — article management endpoints for the editorial dashboard.

All endpoints require JWT authentication via Bearer token.
"""

import math
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.article import Article, ArticleStatus
from app.models.audit import ActorType
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.article import (
    ArticleListItem,
    ArticleResponse,
    ArticleUpdatePayload,
)
from app.schemas.common import PaginatedResponse
from app.services import article_service, audit_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/articles", response_model=PaginatedResponse[ArticleListItem])
async def list_admin_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    search: Optional[str] = Query(None, description="Search in title/summary"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all articles (all statuses) for admin review."""
    articles, total = await article_service.list_articles(
        db,
        page=page,
        limit=limit,
        status=status,
        category_slug=category,
        search=search,
        published_only=False,
    )

    return PaginatedResponse(
        items=[ArticleListItem.model_validate(a) for a in articles],
        total=total,
        page=page,
        limit=limit,
        total_pages=max(1, math.ceil(total / limit)),
    )


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_admin_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get full article detail for editing/review."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse.model_validate(article)


@router.patch("/articles/{article_id}", response_model=ArticleResponse)
async def update_admin_article(
    article_id: UUID,
    payload: ArticleUpdatePayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Manually edit an article from the admin console."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "title" in update_data and update_data["title"]:
        article.title = update_data["title"]
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
    if "status" in update_data:
        article.status = ArticleStatus(update_data["status"])

    # SEO
    if "seo" in update_data and update_data["seo"]:
        seo = payload.seo
        if seo.seo_title is not None:
            article.seo_title = seo.seo_title
        if seo.seo_description is not None:
            article.seo_description = seo.seo_description

    await db.flush()

    await audit_service.log_action(
        db,
        actor_type=ActorType.user,
        actor_id=str(current_user.id),
        action="admin_update",
        entity_type="article",
        entity_id=article.id,
        after_json={"updated_fields": list(update_data.keys())},
        ip_address=request.client.host if request.client else None,
    )

    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)


@router.post("/articles/{article_id}/approve", response_model=ArticleResponse)
async def approve_article(
    article_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark an article as editor-reviewed."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.is_editor_reviewed = True
    article.fact_check_status = "human_checked"
    await db.flush()

    await audit_service.log_action(
        db,
        actor_type=ActorType.user,
        actor_id=str(current_user.id),
        action="approve",
        entity_type="article",
        entity_id=article.id,
        ip_address=request.client.host if request.client else None,
    )

    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)


@router.post("/articles/{article_id}/reject")
async def reject_article(
    article_id: UUID,
    request: Request,
    reason: str = Query(..., description="Rejection reason"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reject an article with a reason."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.status = ArticleStatus.rejected
    article.correction_note = f"Rejected: {reason}"
    await db.flush()

    await audit_service.log_action(
        db,
        actor_type=ActorType.user,
        actor_id=str(current_user.id),
        action="reject",
        entity_type="article",
        entity_id=article.id,
        after_json={"reason": reason},
        ip_address=request.client.host if request.client else None,
    )

    return {"status": "rejected", "article_id": str(article_id), "reason": reason}


@router.post("/articles/{article_id}/correction", response_model=ArticleResponse)
async def add_correction(
    article_id: UUID,
    request: Request,
    correction_note: str = Query(..., description="Correction description"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a correction note to an article."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.correction_note = correction_note
    article.last_corrected_at = datetime.now(timezone.utc)
    await db.flush()

    await audit_service.log_action(
        db,
        actor_type=ActorType.user,
        actor_id=str(current_user.id),
        action="correction",
        entity_type="article",
        entity_id=article.id,
        after_json={"correction_note": correction_note},
        ip_address=request.client.host if request.client else None,
    )

    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)


@router.post("/articles/{article_id}/publish", response_model=ArticleResponse)
async def publish_article(
    article_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Publish an article from the admin dashboard — validates SEO fields and sets status to published."""
    try:
        article = await article_service.publish_article(db, article_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    await audit_service.log_action(
        db,
        actor_type=ActorType.user,
        actor_id=str(current_user.id),
        action="publish",
        entity_type="article",
        entity_id=article.id,
        ip_address=request.client.host if request.client else None,
    )

    article = await article_service.get_article_by_id(db, article.id)
    return ArticleResponse.model_validate(article)

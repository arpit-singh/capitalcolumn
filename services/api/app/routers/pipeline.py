"""Pipeline API — admin endpoints for the AI article pipeline.

All endpoints require JWT authentication (admin role).
"""

import hashlib
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.models.user import User
from app.routers.auth import get_current_user
from app.services import pipeline_service

router = APIRouter(prefix="/admin/pipeline", tags=["Pipeline"])


# ---------------------------------------------------------------------------
# Request / Response Schemas
# ---------------------------------------------------------------------------

class TopicCreate(BaseModel):
    title: str
    category: str = "markets"
    url: str = ""


class TopicStatusUpdate(BaseModel):
    topic_ids: List[str]
    status: str = "approved"


class TopicDelete(BaseModel):
    topic_ids: List[str]


class GenerateRequest(BaseModel):
    topic_ids: List[str]
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    image_model: str = "prunaai/z-image-turbo"
    word_count: int = 1200
    skip_image: bool = False


class SourceCreate(BaseModel):
    name: str
    url: str
    category: str = "markets"
    source_type: str = "rss"  # "rss" or "sitemap"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/config")
async def get_config(
    current_user: User = Depends(get_current_user),
):
    """Get pipeline configuration — available models, sources, status."""
    return pipeline_service.get_pipeline_config()


@router.get("/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
):
    """Get topic queue statistics."""
    return pipeline_service.get_topic_stats()


@router.post("/scan")
async def scan_sources(
    current_user: User = Depends(get_current_user),
):
    """Scan all configured RSS feeds for new topics (free, no cost)."""
    new_topics = pipeline_service.scan_rss_feeds()
    return {
        "new_topics": len(new_topics),
        "topics": new_topics,
        "stats": pipeline_service.get_topic_stats(),
    }


@router.get("/topics")
async def list_topics(
    status: Optional[str] = Query(None, description="Filter: pending, approved, rejected, completed, error"),
    current_user: User = Depends(get_current_user),
):
    """List topics in the queue, optionally filtered by status."""
    topics = pipeline_service.get_topics(status=status)
    return {"topics": topics, "total": len(topics)}


@router.post("/topics")
async def add_topic(
    payload: TopicCreate,
    current_user: User = Depends(get_current_user),
):
    """Manually add a topic to the queue (with free SEO research)."""
    topic = pipeline_service.add_manual_topic(
        title=payload.title,
        category=payload.category,
        url=payload.url,
    )
    return {"topic": topic, "stats": pipeline_service.get_topic_stats()}


@router.patch("/topics/status")
async def update_status(
    payload: TopicStatusUpdate,
    current_user: User = Depends(get_current_user),
):
    """Approve or reject topics by ID."""
    if payload.status not in ("pending", "approved", "rejected"):
        raise HTTPException(400, "Status must be 'pending', 'approved', or 'rejected'")

    count = pipeline_service.update_topic_status(payload.topic_ids, payload.status)
    return {"updated": count, "stats": pipeline_service.get_topic_stats()}


@router.delete("/topics")
async def delete_topics(
    payload: TopicDelete,
    current_user: User = Depends(get_current_user),
):
    """Delete topics from the queue."""
    count = pipeline_service.delete_topics(payload.topic_ids)
    return {"deleted": count, "stats": pipeline_service.get_topic_stats()}


@router.post("/topics/clear")
async def clear_topics(
    status: Optional[str] = Query(None, description="Clear only this status, or all if empty"),
    current_user: User = Depends(get_current_user),
):
    """Clear the topic queue (optionally by status)."""
    count = pipeline_service.clear_topics(status=status)
    return {"cleared": count, "stats": pipeline_service.get_topic_stats()}


@router.post("/generate")
async def generate_articles(
    payload: GenerateRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate articles for selected approved topics (uses paid APIs).

    This runs in the background via asyncio.create_task.
    Check /admin/pipeline/topics?status=completed to see results.
    """
    import asyncio

    # Validate topics
    all_topics = pipeline_service.get_topics()
    selected = [t for t in all_topics if t.get("id") in set(payload.topic_ids)]

    if not selected:
        raise HTTPException(400, "No matching topics found")

    non_approved = [t for t in selected if t.get("status") != "approved"]
    if non_approved:
        raise HTTPException(
            400,
            f"{len(non_approved)} topic(s) are not approved. Approve them first.",
        )

    # Mark as processing
    pipeline_service.update_topic_status(payload.topic_ids, "processing")

    # Fire-and-forget async task on the event loop
    asyncio.create_task(_run_generation(
        topics=selected,
        llm_provider=payload.llm_provider,
        llm_model=payload.llm_model,
        image_model=payload.image_model,
        word_count=payload.word_count,
        skip_image=payload.skip_image,
    ))

    return {
        "message": f"Generating {len(selected)} article(s) in the background",
        "processing": len(selected),
        "estimated_cost": f"~${len(selected) * 0.05:.2f}",
    }


async def _run_generation(
    topics: list[dict],
    llm_provider: str,
    llm_model: str,
    image_model: str,
    word_count: int,
    skip_image: bool,
):
    """Background task: generate articles for approved topics.

    Runs on the event loop via asyncio.create_task().
    Sync LLM/image calls are offloaded to threads via asyncio.to_thread().
    Articles are inserted directly into the DB (no HTTP self-call).
    """
    import asyncio
    import logging

    logger = logging.getLogger("pipeline.generate")

    for topic_data in topics:
        topic_id = topic_data.get("id")
        title = topic_data.get("title", "Untitled")

        try:
            logger.info(f"[Pipeline] Starting: {title[:60]}")
            seo = topic_data.get("seo", {})
            primary = seo.get("primary_keywords", [title])
            secondary = seo.get("secondary_keywords", [])
            category = topic_data.get("category", "markets")

            # Step 1: Image generation (paid) — run sync code in thread
            media_asset_id = None
            if not skip_image:
                try:
                    logger.info(f"[Pipeline] Generating image with {image_model}...")
                    image_bytes, img_meta = await asyncio.to_thread(
                        pipeline_service.generate_article_image,
                        topic=title,
                        category=category,
                        model_id=image_model,
                    )
                    logger.info(f"[Pipeline] Image generated ({img_meta.get('compressed_kb', '?')} KB)")

                    # Upload image directly to R2 + DB (no HTTP self-call)
                    slug_for_img = title.lower().replace(" ", "-")[:60]
                    filename = f"{slug_for_img}-hero.webp"
                    media_asset_id = await _save_image_to_db(
                        image_bytes=image_bytes,
                        filename=filename,
                        alt_text=title,
                        credit="AI Generated / CapitalColumn",
                    )
                    logger.info(f"[Pipeline] Image saved to DB (asset_id: {media_asset_id})")
                except Exception as img_err:
                    logger.error(f"[Pipeline] Image error (continuing without image): {img_err}")

            # Step 2: Compose article (paid) — run sync LLM call in thread
            logger.info(f"[Pipeline] Composing article with {llm_provider}/{llm_model}...")
            article = await asyncio.to_thread(
                pipeline_service.compose_article,
                topic=title,
                summary=topic_data.get("summary", ""),
                primary_keywords=primary,
                secondary_keywords=secondary,
                source_url=topic_data.get("url", ""),
                word_count=word_count,
                provider=llm_provider,
                model=llm_model,
            )
            logger.info(f"[Pipeline] Article composed: {article.get('word_count', 0)} words")

            # Step 3: Insert directly into DB (no HTTP self-call)
            logger.info("[Pipeline] Saving article to database...")
            hash_input = f"{title}:{topic_data.get('url', '')}".encode()
            external_id = f"pipeline-{hashlib.sha256(hash_input).hexdigest()[:12]}"

            source_info = None
            if topic_data.get("url") and not topic_data["url"].startswith("manual://"):
                source_info = {
                    "source_name": topic_data.get("source_name", "News Source"),
                    "source_url": topic_data["url"],
                    "source_type": "news_article",
                }

            result = await _save_article_to_db(
                external_id=external_id,
                title=article["title"],
                body_markdown=article["body_markdown"],
                category_slug=category,
                dek=article.get("dek", ""),
                summary=article.get("summary", ""),
                key_takeaways=article.get("key_takeaways", []),
                tags=secondary[:5],
                seo_title=article.get("seo_title", ""),
                seo_description=article.get("seo_description", ""),
                meta_keywords=article.get("meta_keywords", []),
                ai_model_name=article.get("model_used", llm_model),
                source_info=source_info,
                featured_image_id=media_asset_id,
            )

            logger.info(f"[Pipeline] ✓ Saved: {result['slug']} (id: {result['id']})")
            pipeline_service.update_topic_status([topic_id], "completed")
            pending = pipeline_service._load_pending()
            for t in pending:
                if t.get("id") == topic_id:
                    t["article_id"] = str(result["id"])
                    t["article_slug"] = result["slug"]
                    t["completed_at"] = datetime.now(timezone.utc).isoformat()
            pipeline_service._save_pending(pending)

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:200]}"
            logger.error(f"[Pipeline] ✗ Failed '{title[:40]}': {error_msg}", exc_info=True)
            pipeline_service.update_topic_status([topic_id], "error")
            pending = pipeline_service._load_pending()
            for t in pending:
                if t.get("id") == topic_id:
                    t["error"] = error_msg
            pipeline_service._save_pending(pending)


async def _save_image_to_db(
    *,
    image_bytes: bytes,
    filename: str,
    alt_text: str,
    credit: str,
):
    """Upload image to R2 and create a MediaAsset record directly.

    Returns the media_asset UUID (for linking to articles).
    """
    import logging

    from app.db.session import async_session_factory
    from app.models.media import MediaAsset
    from app.services import r2_service

    logger = logging.getLogger("pipeline.generate")

    # Upload to R2
    r2_key = r2_service.generate_r2_key(filename)
    public_url = await r2_service.upload_bytes(image_bytes, r2_key, "image/webp")

    # Create DB record
    async with async_session_factory() as session:
        try:
            asset = MediaAsset(
                r2_key=r2_key,
                public_url=public_url,
                filename=filename,
                mime_type="image/webp",
                size_bytes=len(image_bytes),
                alt_text=alt_text,
                credit=credit,
            )
            session.add(asset)
            await session.commit()
            logger.info(f"[Pipeline] Image stored in R2: {r2_key} ({len(image_bytes)} bytes)")
            return asset.id
        except Exception as e:
            await session.rollback()
            raise



async def _save_article_to_db(
    *,
    external_id: str,
    title: str,
    body_markdown: str,
    category_slug: str,
    dek: str,
    summary: str,
    key_takeaways: list,
    tags: list,
    seo_title: str,
    seo_description: str,
    meta_keywords: list,
    ai_model_name: str,
    source_info: dict | None,
    featured_image_id=None,
) -> dict:
    """Insert an article directly into the database, bypassing HTTP.

    Uses its own async session to avoid greenlet conflicts.
    Returns dict with 'id' and 'slug'.
    """
    import math
    import re
    import logging

    from slugify import slugify as make_slug
    from sqlalchemy import select, or_

    from app.db.session import async_session_factory
    from app.models.article import (
        Article, ArticleSource, ArticleStatus, ArticleType,
        SourceType,
    )
    from app.models.taxonomy import Category, Tag
    from app.models.author import Author

    logger = logging.getLogger("pipeline.generate")

    # Estimate reading time
    text = re.sub(r"[#*_\[\]()\>\`~\-|]", "", body_markdown)
    reading_time = max(1, math.ceil(len(text.split()) / 200))

    async with async_session_factory() as session:
        try:
            # Check idempotency on external_id
            result = await session.execute(
                select(Article).where(Article.external_id == external_id)
            )
            existing = result.scalar_one_or_none()
            if existing:
                logger.info(f"[Pipeline] Article with external_id={external_id} already exists, updating")
                existing.title = title
                existing.body_markdown = body_markdown
                existing.dek = dek
                existing.summary = summary
                existing.key_takeaways = key_takeaways
                existing.seo_title = seo_title or title
                existing.seo_description = seo_description or summary
                existing.meta_keywords = meta_keywords
                existing.reading_time_minutes = reading_time
                await session.commit()
                return {"id": existing.id, "slug": existing.slug}

            # Generate unique slug
            base_slug = make_slug(title, max_length=200, lowercase=True) or "article"
            slug = base_slug
            counter = 1
            while True:
                check = await session.execute(
                    select(Article.id).where(Article.slug == slug)
                )
                if check.scalar_one_or_none() is None:
                    break
                counter += 1
                slug = f"{base_slug}-{counter}"

            # Resolve category
            category_id = None
            if category_slug:
                cat_result = await session.execute(
                    select(Category).where(
                        or_(Category.name == category_slug, Category.slug == category_slug)
                    )
                )
                cat = cat_result.scalar_one_or_none()
                if cat:
                    category_id = cat.id

            # Resolve author
            author_id = None
            author_result = await session.execute(
                select(Author).where(Author.slug == "editorial-desk")
            )
            author = author_result.scalar_one_or_none()
            if author:
                author_id = author.id

            # Create article
            article = Article(
                external_id=external_id,
                slug=slug,
                title=title,
                dek=dek,
                summary=summary,
                body_markdown=body_markdown,
                article_type=ArticleType.news,
                status=ArticleStatus.draft,
                reading_time_minutes=reading_time,
                key_takeaways=key_takeaways,
                category_id=category_id,
                author_id=author_id,
                featured_image_id=featured_image_id,
                seo_title=seo_title or title,
                seo_description=seo_description or summary,
                meta_keywords=meta_keywords,
                is_ai_generated=True,
                ai_pipeline_name="capitalcolumn-pipeline",
                ai_model_name=ai_model_name,
                ai_pipeline_version="1.0.0",
            )
            session.add(article)
            await session.flush()

            # Resolve/create tags
            for tag_name in (tags or []):
                if not tag_name or not tag_name.strip():
                    continue
                tag_result = await session.execute(
                    select(Tag).where(
                        or_(Tag.name == tag_name, Tag.slug == make_slug(tag_name, lowercase=True))
                    )
                )
                tag = tag_result.scalar_one_or_none()
                if not tag:
                    tag = Tag(name=tag_name, slug=make_slug(tag_name, lowercase=True))
                    session.add(tag)
                    await session.flush()
                article.tags.append(tag)

            # Add source
            if source_info:
                source = ArticleSource(
                    article_id=article.id,
                    source_name=source_info["source_name"],
                    source_url=source_info["source_url"],
                    source_type=SourceType(source_info.get("source_type", "news_article")),
                    is_primary_source=True,
                    accessed_at=datetime.now(timezone.utc),
                )
                session.add(source)

            await session.commit()
            logger.info(f"[Pipeline] DB commit successful: {slug}")
            return {"id": article.id, "slug": slug}

        except Exception as e:
            await session.rollback()
            raise


# ---------------------------------------------------------------------------
# Source Management
# ---------------------------------------------------------------------------

@router.get("/sources")
async def list_sources(
    current_user: User = Depends(get_current_user),
):
    """List configured news sources."""
    sources = pipeline_service._load_sources()
    return sources


@router.post("/sources")
async def add_source(
    payload: SourceCreate,
    current_user: User = Depends(get_current_user),
):
    """Add a new RSS feed or sitemap source."""
    sources = pipeline_service._load_sources()
    entry = {"name": payload.name, "url": payload.url, "category": payload.category}

    if payload.source_type == "sitemap":
        sources.setdefault("sitemaps", []).append(entry)
    else:
        sources.setdefault("rss_feeds", []).append(entry)

    pipeline_service.save_sources(sources)
    return {"message": "Source added", "sources": sources}


@router.delete("/sources/{index}")
async def remove_source(
    index: int,
    source_type: str = Query("rss", description="'rss' or 'sitemap'"),
    current_user: User = Depends(get_current_user),
):
    """Remove a source by index."""
    sources = pipeline_service._load_sources()
    key = "sitemaps" if source_type == "sitemap" else "rss_feeds"
    items = sources.get(key, [])

    if 0 <= index < len(items):
        removed = items.pop(index)
        pipeline_service.save_sources(sources)
        return {"message": f"Removed: {removed.get('name')}", "sources": sources}

    raise HTTPException(404, "Source not found")

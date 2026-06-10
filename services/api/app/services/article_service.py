"""Article service — core business logic for creating, updating, and publishing articles."""

import math
import re
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.article import Article, ArticleSource, ArticleStatus, ArticleType, FactCheckStatus, SourceType
from app.models.taxonomy import Category, Tag
from app.models.company import CompanyTicker
from app.models.author import Author
from app.schemas.article import (
    ArticleCreatePayload,
    ArticleUpdatePayload,
    SourceInput,
    TickerInput,
)
from app.services.slug_service import generate_unique_slug


def _estimate_reading_time(markdown: str) -> int:
    """Estimate reading time from markdown text (200 words per minute)."""
    text = re.sub(r"[#*_\[\]()>`~\-|]", "", markdown)
    word_count = len(text.split())
    minutes = max(1, math.ceil(word_count / 200))
    return minutes


async def _resolve_category(db: AsyncSession, category_input: Optional[str]) -> Optional[Category]:
    """Resolve a category by name or slug."""
    if not category_input:
        return None
    result = await db.execute(
        select(Category).where(
            or_(Category.name == category_input, Category.slug == category_input)
        )
    )
    return result.scalar_one_or_none()


async def _resolve_tags(db: AsyncSession, tag_inputs: Optional[List[str]]) -> List[Tag]:
    """Resolve tags by name or slug — create missing ones."""
    if not tag_inputs:
        return []

    tags = []
    for tag_input in tag_inputs:
        result = await db.execute(
            select(Tag).where(or_(Tag.name == tag_input, Tag.slug == tag_input))
        )
        tag = result.scalar_one_or_none()
        if not tag:
            from slugify import slugify
            tag = Tag(name=tag_input, slug=slugify(tag_input, lowercase=True))
            db.add(tag)
            await db.flush()
        tags.append(tag)
    return tags


async def _resolve_tickers(
    db: AsyncSession, ticker_inputs: Optional[List[TickerInput]]
) -> List[CompanyTicker]:
    """Resolve tickers — create missing ones."""
    if not ticker_inputs:
        return []

    tickers = []
    for ti in ticker_inputs:
        result = await db.execute(
            select(CompanyTicker).where(CompanyTicker.ticker == ti.ticker)
        )
        ticker = result.scalar_one_or_none()
        if not ticker:
            from slugify import slugify
            ticker = CompanyTicker(
                name=ti.company_name,
                ticker=ti.ticker,
                exchange=ti.exchange,
                country=ti.country,
                sector=ti.sector,
                industry=ti.industry,
                company_page_slug=slugify(ti.company_name, lowercase=True),
            )
            db.add(ticker)
            await db.flush()
        tickers.append(ticker)
    return tickers


def _build_sources(
    article_id: uuid.UUID, source_inputs: Optional[List[SourceInput]]
) -> List[ArticleSource]:
    """Build ArticleSource objects from input."""
    if not source_inputs:
        return []

    sources = []
    for si in source_inputs:
        sources.append(
            ArticleSource(
                article_id=article_id,
                source_name=si.source_name,
                source_url=si.source_url,
                source_type=SourceType(si.source_type) if si.source_type else SourceType.other,
                publisher=si.publisher,
                published_at=si.published_at,
                accessed_at=datetime.now(timezone.utc),
                relevance_note=si.relevance_note,
                quote_used=si.quote_used,
                is_primary_source=si.is_primary_source,
            )
        )
    return sources


async def _get_default_author(db: AsyncSession) -> Optional[Author]:
    """Get the default editorial desk author."""
    result = await db.execute(select(Author).where(Author.slug == "editorial-desk"))
    return result.scalar_one_or_none()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def create_or_update_article(
    db: AsyncSession,
    payload: ArticleCreatePayload,
    api_key_id: str,
) -> Tuple[Article, bool]:
    """Create a new article, or update if external_id already exists.

    Returns (article, created) where created=True if new.
    """
    created = True
    article: Optional[Article] = None

    # Idempotency: check external_id
    if payload.external_id:
        result = await db.execute(
            select(Article).where(Article.external_id == payload.external_id)
        )
        article = result.scalar_one_or_none()

    if article:
        # Update existing
        created = False
        article.title = payload.title
        article.dek = payload.dek
        article.summary = payload.summary
        article.body_markdown = payload.body_markdown
        article.language = payload.language
        article.article_type = ArticleType(payload.article_type)
        article.reading_time_minutes = _estimate_reading_time(payload.body_markdown)
        article.key_takeaways = payload.key_takeaways
        article.disclaimer_variant = payload.disclaimer_variant

        # Re-generate slug if title changed
        if article.title != payload.title:
            article.slug = await generate_unique_slug(payload.title, db, existing_id=article.id)
    else:
        # Create new
        slug = await generate_unique_slug(payload.title, db)
        article = Article(
            external_id=payload.external_id,
            slug=slug,
            title=payload.title,
            dek=payload.dek,
            summary=payload.summary,
            body_markdown=payload.body_markdown,
            language=payload.language,
            article_type=ArticleType(payload.article_type),
            status=ArticleStatus(payload.status) if payload.status else ArticleStatus.draft,
            reading_time_minutes=_estimate_reading_time(payload.body_markdown),
            key_takeaways=payload.key_takeaways,
            disclaimer_variant=payload.disclaimer_variant,
        )
        db.add(article)
        await db.flush()  # Get the article.id

    # Resolve category
    category = await _resolve_category(db, payload.category)
    article.category_id = category.id if category else None
    article.category = category

    # Resolve author
    author = await _get_default_author(db)
    article.author_id = author.id if author else None

    # Resolve tags
    article.tags = await _resolve_tags(db, payload.tags)

    # Resolve tickers
    article.tickers = await _resolve_tickers(db, payload.tickers)

    # SEO
    if payload.seo:
        article.seo_title = payload.seo.seo_title or payload.title
        article.seo_description = payload.seo.seo_description or payload.summary
        article.canonical_url = payload.seo.canonical_url
        article.noindex = payload.seo.noindex
        article.meta_keywords = payload.seo.meta_keywords
    else:
        article.seo_title = article.seo_title or payload.title
        article.seo_description = article.seo_description or payload.summary

    # AI metadata
    if payload.ai_metadata:
        article.is_ai_generated = payload.ai_metadata.is_ai_generated
        article.is_editor_reviewed = payload.ai_metadata.is_editor_reviewed
        article.ai_pipeline_name = payload.ai_metadata.ai_pipeline_name
        article.ai_model_name = payload.ai_metadata.ai_model_name
        article.ai_pipeline_version = payload.ai_metadata.ai_pipeline_version
        article.confidence_score = payload.ai_metadata.confidence_score

    # Sources — replace all
    if payload.sources is not None:
        # Remove old sources
        for old_source in list(article.sources):
            await db.delete(old_source)
        await db.flush()
        article.sources = _build_sources(article.id, payload.sources)

    await db.flush()
    return article, created


async def publish_article(db: AsyncSession, article_id: uuid.UUID) -> Article:
    """Publish an article — validate and set status."""
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if not article:
        raise ValueError(f"Article {article_id} not found")

    # Validation
    errors = []
    if not article.title:
        errors.append("Title is required")
    if not article.body_markdown:
        errors.append("Body is required")
    if not article.seo_title:
        errors.append("SEO title is required")
    if not article.seo_description:
        errors.append("SEO description is required")

    if errors:
        raise ValueError(f"Cannot publish: {'; '.join(errors)}")

    article.status = ArticleStatus.published
    if not article.published_at:
        article.published_at = datetime.now(timezone.utc)

    await db.flush()
    return article


async def schedule_article(
    db: AsyncSession, article_id: uuid.UUID, scheduled_at: datetime
) -> Article:
    """Schedule an article for future publication."""
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if not article:
        raise ValueError(f"Article {article_id} not found")

    article.status = ArticleStatus.scheduled
    article.scheduled_at = scheduled_at
    await db.flush()
    return article


async def get_article_by_id(db: AsyncSession, article_id: uuid.UUID) -> Optional[Article]:
    """Get a single article by ID with all relationships loaded."""
    result = await db.execute(
        select(Article)
        .options(
            selectinload(Article.category),
            selectinload(Article.author),
            selectinload(Article.featured_image),
            selectinload(Article.tags),
            selectinload(Article.tickers),
            selectinload(Article.sources),
        )
        .where(Article.id == article_id)
    )
    return result.scalar_one_or_none()


async def get_article_by_slug(
    db: AsyncSession, slug: str, published_only: bool = False
) -> Optional[Article]:
    """Get a single article by slug."""
    query = (
        select(Article)
        .options(
            selectinload(Article.category),
            selectinload(Article.author),
            selectinload(Article.featured_image),
            selectinload(Article.tags),
            selectinload(Article.tickers),
            selectinload(Article.sources),
        )
        .where(Article.slug == slug)
    )
    if published_only:
        query = query.where(Article.status == ArticleStatus.published)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_articles(
    db: AsyncSession,
    *,
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    category_slug: Optional[str] = None,
    tag_slug: Optional[str] = None,
    ticker: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = False,
) -> Tuple[List[Article], int]:
    """List articles with filtering and pagination.

    Returns (articles, total_count).
    """
    query = (
        select(Article)
        .options(
            selectinload(Article.category),
            selectinload(Article.author),
            selectinload(Article.featured_image),
            selectinload(Article.tags),
            selectinload(Article.tickers),
        )
    )
    count_query = select(func.count(Article.id))

    # Filters
    if published_only:
        query = query.where(Article.status == ArticleStatus.published)
        count_query = count_query.where(Article.status == ArticleStatus.published)
    elif status:
        query = query.where(Article.status == ArticleStatus(status))
        count_query = count_query.where(Article.status == ArticleStatus(status))

    if category_slug:
        query = query.join(Article.category).where(Category.slug == category_slug)
        count_query = count_query.join(Article.category).where(Category.slug == category_slug)

    if tag_slug:
        query = query.join(Article.tags).where(Tag.slug == tag_slug)
        count_query = count_query.join(Article.tags).where(Tag.slug == tag_slug)

    if ticker:
        query = query.join(Article.tickers).where(CompanyTicker.ticker == ticker)
        count_query = count_query.join(Article.tickers).where(CompanyTicker.ticker == ticker)

    if search:
        search_filter = or_(
            Article.title.ilike(f"%{search}%"),
            Article.summary.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    # Ordering
    query = query.order_by(Article.published_at.desc().nullslast(), Article.created_at.desc())

    # Pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    articles = list(result.scalars().unique().all())

    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    return articles, total

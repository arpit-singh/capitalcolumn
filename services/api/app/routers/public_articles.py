"""Public read API — serves published content to the Astro frontend and any client.

No authentication required. Only returns published articles.
"""

import math
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.article import Article, ArticleStatus
from app.models.taxonomy import Category, Tag
from app.models.company import CompanyTicker
from app.schemas.article import (
    ArticleListItem,
    ArticleResponse,
    CategoryResponse,
    CompanyTickerResponse,
    TagResponse,
)
from app.schemas.common import PaginatedResponse
from app.services import article_service

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/articles", response_model=PaginatedResponse[ArticleListItem])
async def list_published_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    tag: Optional[str] = Query(None, description="Filter by tag slug"),
    ticker: Optional[str] = Query(None, description="Filter by ticker symbol"),
    search: Optional[str] = Query(None, description="Search in title and summary"),
    db: AsyncSession = Depends(get_db),
):
    """List published articles with pagination and filtering."""
    articles, total = await article_service.list_articles(
        db,
        page=page,
        limit=limit,
        category_slug=category,
        tag_slug=tag,
        ticker=ticker,
        search=search,
        published_only=True,
    )

    return PaginatedResponse(
        items=[ArticleListItem.model_validate(a) for a in articles],
        total=total,
        page=page,
        limit=limit,
        total_pages=max(1, math.ceil(total / limit)),
    )


@router.get("/articles/{slug}", response_model=ArticleResponse)
async def get_published_article(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a single published article by slug."""
    article = await article_service.get_article_by_slug(db, slug, published_only=True)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse.model_validate(article)


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    """List all active categories."""
    result = await db.execute(
        select(Category)
        .where(Category.is_active == True)
        .order_by(Category.sort_order)
    )
    categories = result.scalars().all()
    return [CategoryResponse.model_validate(c) for c in categories]


@router.get("/categories/{slug}", response_model=CategoryResponse)
async def get_category(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a single category by slug."""
    result = await db.execute(
        select(Category).where(Category.slug == slug, Category.is_active == True)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryResponse.model_validate(category)


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(
    db: AsyncSession = Depends(get_db),
):
    """List all tags."""
    result = await db.execute(select(Tag).order_by(Tag.name))
    tags = result.scalars().all()
    return [TagResponse.model_validate(t) for t in tags]


@router.get("/tickers/{ticker_symbol}")
async def get_ticker_page(
    ticker_symbol: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Get company/ticker page data with related articles."""
    result = await db.execute(
        select(CompanyTicker).where(CompanyTicker.ticker == ticker_symbol.upper())
    )
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found")

    articles, total = await article_service.list_articles(
        db,
        page=page,
        limit=limit,
        ticker=ticker_symbol.upper(),
        published_only=True,
    )

    return {
        "company": CompanyTickerResponse.model_validate(company),
        "articles": PaginatedResponse(
            items=[ArticleListItem.model_validate(a) for a in articles],
            total=total,
            page=page,
            limit=limit,
            total_pages=max(1, math.ceil(total / limit)),
        ),
    }

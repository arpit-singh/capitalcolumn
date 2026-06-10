"""Article request/response schemas — matches Claude.md section 7.2 and frontend types.ts."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Nested Input Schemas (used in ArticleCreatePayload)
# ---------------------------------------------------------------------------

class SourceInput(BaseModel):
    source_name: str
    source_url: str
    source_type: str = "other"
    publisher: Optional[str] = None
    published_at: Optional[datetime] = None
    relevance_note: Optional[str] = None
    quote_used: Optional[str] = None
    is_primary_source: bool = False


class TickerInput(BaseModel):
    ticker: str
    exchange: str = "NSE"
    company_name: str
    country: str = "India"
    sector: Optional[str] = None
    industry: Optional[str] = None


class FeaturedImageInput(BaseModel):
    source_url: Optional[str] = None
    alt_text: str = ""
    caption: Optional[str] = None
    credit: Optional[str] = None


class SEOInput(BaseModel):
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    canonical_url: Optional[str] = None
    noindex: bool = False
    meta_keywords: Optional[List[str]] = None


class AIMetadataInput(BaseModel):
    is_ai_generated: bool = True
    is_editor_reviewed: bool = False
    ai_pipeline_name: Optional[str] = None
    ai_model_name: Optional[str] = None
    ai_pipeline_version: Optional[str] = None
    confidence_score: Optional[float] = None


# ---------------------------------------------------------------------------
# Create / Update Payloads
# ---------------------------------------------------------------------------

class ArticleCreatePayload(BaseModel):
    """Matches the POST /internal/articles request body from Claude.md."""
    external_id: Optional[str] = None
    title: str
    dek: Optional[str] = None
    summary: Optional[str] = None
    body_markdown: str
    language: str = "en"
    article_type: str = "news"
    status: str = "draft"
    category: Optional[str] = None  # Category name or slug
    tags: Optional[List[str]] = None  # Tag names or slugs
    tickers: Optional[List[TickerInput]] = None
    sources: Optional[List[SourceInput]] = None
    featured_image: Optional[FeaturedImageInput] = None
    seo: Optional[SEOInput] = None
    ai_metadata: Optional[AIMetadataInput] = None
    key_takeaways: Optional[List[str]] = None
    disclaimer_variant: Optional[str] = None


class ArticleUpdatePayload(BaseModel):
    """Partial update — all fields optional."""
    title: Optional[str] = None
    dek: Optional[str] = None
    summary: Optional[str] = None
    body_markdown: Optional[str] = None
    language: Optional[str] = None
    article_type: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    tickers: Optional[List[TickerInput]] = None
    sources: Optional[List[SourceInput]] = None
    seo: Optional[SEOInput] = None
    ai_metadata: Optional[AIMetadataInput] = None
    key_takeaways: Optional[List[str]] = None
    correction_note: Optional[str] = None
    disclaimer_variant: Optional[str] = None


class ArticleSchedulePayload(BaseModel):
    scheduled_at: datetime


# ---------------------------------------------------------------------------
# Response Schemas — match frontend types.ts
# ---------------------------------------------------------------------------

class SourceResponse(BaseModel):
    id: UUID
    source_name: str
    source_url: str
    source_type: str
    publisher: Optional[str] = None
    published_at: Optional[datetime] = None
    accessed_at: Optional[datetime] = None
    relevance_note: Optional[str] = None
    quote_used: Optional[str] = None
    is_primary_source: bool

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    sort_order: int
    is_active: bool

    model_config = {"from_attributes": True}


class TagResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = {"from_attributes": True}


class CompanyTickerResponse(BaseModel):
    id: UUID
    name: str
    ticker: str
    exchange: str
    country: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    logo_url: Optional[str] = None
    company_page_slug: str

    model_config = {"from_attributes": True}


class AuthorResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    author_type: str

    model_config = {"from_attributes": True}


class MediaAssetResponse(BaseModel):
    id: UUID
    public_url: str
    alt_text: str
    caption: Optional[str] = None
    credit: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    model_config = {"from_attributes": True}


class ArticleResponse(BaseModel):
    """Full article response matching the frontend Article interface."""
    id: UUID
    external_id: Optional[str] = None
    slug: str
    title: str
    dek: Optional[str] = None
    summary: Optional[str] = None
    body_markdown: str
    body_html: Optional[str] = None
    status: str
    language: str
    article_type: str
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    tickers: List[CompanyTickerResponse] = []
    sources: List[SourceResponse] = []
    author: Optional[AuthorResponse] = None
    published_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    reading_time_minutes: int
    featured_image: Optional[MediaAssetResponse] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    canonical_url: Optional[str] = None
    noindex: bool
    is_ai_generated: bool
    is_editor_reviewed: bool
    ai_pipeline_name: Optional[str] = None
    ai_model_name: Optional[str] = None
    confidence_score: Optional[float] = None
    fact_check_status: str
    correction_note: Optional[str] = None
    last_corrected_at: Optional[datetime] = None
    key_takeaways: Optional[List[str]] = None

    model_config = {"from_attributes": True}


class ArticleListItem(BaseModel):
    """Compact article for list views — excludes body."""
    id: UUID
    slug: str
    title: str
    dek: Optional[str] = None
    summary: Optional[str] = None
    status: str
    article_type: str
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    author: Optional[AuthorResponse] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    reading_time_minutes: int
    featured_image: Optional[MediaAssetResponse] = None
    is_ai_generated: bool
    is_editor_reviewed: bool
    fact_check_status: str

    model_config = {"from_attributes": True}


class ArticleCreateResponse(BaseModel):
    """Response after creating/updating an article."""
    id: UUID
    slug: str
    status: str
    preview_url: Optional[str] = None
    public_url: Optional[str] = None
    created: bool

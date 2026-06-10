"""Article model — the core content entity."""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    Column,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

import enum


class ArticleStatus(str, enum.Enum):
    draft = "draft"
    in_review = "in_review"
    scheduled = "scheduled"
    published = "published"
    archived = "archived"
    rejected = "rejected"


class ArticleType(str, enum.Enum):
    news = "news"
    analysis = "analysis"
    explainer = "explainer"
    earnings = "earnings"
    market_update = "market_update"
    alert = "alert"
    opinion = "opinion"


class FactCheckStatus(str, enum.Enum):
    unchecked = "unchecked"
    ai_checked = "ai_checked"
    human_checked = "human_checked"
    source_verified = "source_verified"


class SourceType(str, enum.Enum):
    company_filing = "company_filing"
    exchange_disclosure = "exchange_disclosure"
    press_release = "press_release"
    news_article = "news_article"
    official_statement = "official_statement"
    market_data = "market_data"
    social_media = "social_media"
    other = "other"


# ---------------------------------------------------------------------------
# Association Tables
# ---------------------------------------------------------------------------

article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

article_tickers = Table(
    "article_tickers",
    Base.metadata,
    Column("article_id", UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("ticker_id", UUID(as_uuid=True), ForeignKey("company_tickers.id", ondelete="CASCADE"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Article Model
# ---------------------------------------------------------------------------

class Article(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "articles"

    # Identity
    external_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)
    slug: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, index=True)

    # Content
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    dek: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    key_takeaways: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Classification
    status: Mapped[ArticleStatus] = mapped_column(
        SAEnum(ArticleStatus, name="article_status", create_constraint=True),
        default=ArticleStatus.draft,
        nullable=False,
        index=True,
    )
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    article_type: Mapped[ArticleType] = mapped_column(
        SAEnum(ArticleType, name="article_type", create_constraint=True),
        default=ArticleType.news,
        nullable=False,
    )

    # Relationships — foreign keys
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    author_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("authors.id"), nullable=True
    )
    featured_image_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media_assets.id"), nullable=True
    )

    # Timestamps
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Reading
    reading_time_minutes: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # SEO
    seo_title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    seo_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    canonical_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    meta_keywords: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    noindex: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # AI Provenance
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_editor_reviewed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ai_pipeline_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ai_model_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ai_pipeline_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Numeric(4, 2), nullable=True)
    fact_check_status: Mapped[FactCheckStatus] = mapped_column(
        SAEnum(FactCheckStatus, name="fact_check_status", create_constraint=True),
        default=FactCheckStatus.unchecked,
        nullable=False,
    )
    disclaimer_variant: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Corrections
    correction_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_corrected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    category = relationship("Category", back_populates="articles", lazy="selectin")
    author = relationship("Author", back_populates="articles", lazy="selectin")
    featured_image = relationship("MediaAsset", lazy="selectin")
    tags = relationship("Tag", secondary=article_tags, back_populates="articles", lazy="selectin")
    tickers = relationship("CompanyTicker", secondary=article_tickers, back_populates="articles", lazy="selectin")
    sources = relationship("ArticleSource", back_populates="article", cascade="all, delete-orphan", lazy="selectin")


# ---------------------------------------------------------------------------
# Article Source Model
# ---------------------------------------------------------------------------

class ArticleSource(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "article_sources"

    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_name: Mapped[str] = mapped_column(String(500), nullable=False)
    source_url: Mapped[str] = mapped_column(String(2000), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(
        SAEnum(SourceType, name="source_type", create_constraint=True),
        default=SourceType.other,
        nullable=False,
    )
    publisher: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    accessed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    relevance_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quote_used: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_primary_source: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    article = relationship("Article", back_populates="sources")

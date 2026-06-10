"""Company / Ticker model."""

from typing import Optional

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.article import article_tickers


class CompanyTicker(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "company_tickers"

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    ticker: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    exchange: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="India", nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    logo_media_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    company_page_slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)

    # Relationships
    articles = relationship("Article", secondary=article_tickers, back_populates="tickers", lazy="noload")

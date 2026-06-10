"""Category and Tag models."""

from typing import List, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.article import article_tags


class Category(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="category", lazy="noload")
    parent = relationship("Category", remote_side="Category.id", lazy="selectin")


class Tag(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)

    # Relationships
    articles = relationship("Article", secondary=article_tags, back_populates="tags", lazy="noload")

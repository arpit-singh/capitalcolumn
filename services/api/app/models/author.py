"""Author model."""

import enum
from typing import Optional

from sqlalchemy import Boolean, Enum as SAEnum, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AuthorType(str, enum.Enum):
    human = "human"
    ai_assisted = "ai_assisted"
    editorial_team = "editorial_team"


class Author(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    slug: Mapped[str] = mapped_column(String(300), nullable=False, unique=True, index=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_media_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    author_type: Mapped[AuthorType] = mapped_column(
        SAEnum(AuthorType, name="author_type", create_constraint=True),
        default=AuthorType.editorial_team,
        nullable=False,
    )
    social_links: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="author", lazy="noload")

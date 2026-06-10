"""Media asset model for images stored in R2."""

from typing import Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class MediaAsset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "media_assets"

    r2_key: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    public_url: Mapped[str] = mapped_column(String(2000), nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    alt_text: Mapped[str] = mapped_column(String(1000), default="", nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    credit: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    uploaded_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

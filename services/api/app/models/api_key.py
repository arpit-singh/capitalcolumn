"""API Key model for internal pipeline authentication."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class APIKey(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "api_keys"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    key_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

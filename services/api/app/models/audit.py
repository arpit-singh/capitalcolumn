"""Audit log model for tracking all content changes."""

import enum
import uuid
from typing import Optional

from sqlalchemy import DateTime, Enum as SAEnum, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDPrimaryKeyMixin


class ActorType(str, enum.Enum):
    user = "user"
    api_key = "api_key"
    system = "system"
    ai_agent = "ai_agent"


class AuditLog(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "audit_logs"

    actor_type: Mapped[ActorType] = mapped_column(
        SAEnum(ActorType, name="actor_type", create_constraint=True),
        nullable=False,
    )
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    before_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    after_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

"""Audit log service."""

import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import ActorType, AuditLog


async def log_action(
    db: AsyncSession,
    *,
    actor_type: ActorType,
    actor_id: str,
    action: str,
    entity_type: str,
    entity_id: uuid.UUID,
    before_json: Optional[dict] = None,
    after_json: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Create an audit log entry."""
    entry = AuditLog(
        actor_type=actor_type,
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        before_json=before_json,
        after_json=after_json,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(entry)
    return entry

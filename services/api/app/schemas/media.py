"""Media upload request/response schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class MediaUploadByURL(BaseModel):
    """Upload media by fetching from a remote URL."""
    source_url: str
    alt_text: str = ""
    caption: Optional[str] = None
    credit: Optional[str] = None


class MediaResponse(BaseModel):
    """Media asset response."""
    id: UUID
    r2_key: str
    public_url: str
    filename: str
    mime_type: str
    size_bytes: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    alt_text: str
    caption: Optional[str] = None
    credit: Optional[str] = None
    source_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MediaListResponse(BaseModel):
    items: list[MediaResponse]
    total: int

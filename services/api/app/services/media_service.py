"""Media service — handles image uploads and URL fetching."""

import io
import logging
import mimetypes
import os
from typing import Optional
from urllib.parse import urlparse

import httpx
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import MediaAsset
from app.services import r2_service

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/svg+xml",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def fetch_and_store(
    db: AsyncSession,
    *,
    source_url: str,
    alt_text: str = "",
    caption: Optional[str] = None,
    credit: Optional[str] = None,
) -> MediaAsset:
    """Download an image from a URL and store it in R2.

    Returns a MediaAsset record.
    """
    # Check if this source_url was already fetched
    result = await db.execute(
        select(MediaAsset).where(MediaAsset.source_url == source_url)
    )
    existing = result.scalar_one_or_none()
    if existing:
        # Update metadata if changed
        if alt_text:
            existing.alt_text = alt_text
        if caption is not None:
            existing.caption = caption
        if credit is not None:
            existing.credit = credit
        return existing

    # Fetch the image
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(source_url)
        response.raise_for_status()

    data = response.content
    content_type = response.headers.get("content-type", "").split(";")[0].strip()

    # Validate
    if content_type not in ALLOWED_MIME_TYPES:
        # Try to guess from URL
        guessed, _ = mimetypes.guess_type(source_url)
        if guessed and guessed in ALLOWED_MIME_TYPES:
            content_type = guessed
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    if len(data) > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {len(data)} bytes (max {MAX_FILE_SIZE})")

    # Determine filename and extension
    parsed_url = urlparse(source_url)
    filename = os.path.basename(parsed_url.path) or "image"
    if "." not in filename:
        ext = mimetypes.guess_extension(content_type) or ".jpg"
        filename = f"{filename}{ext}"

    # Upload to R2
    r2_key = r2_service.generate_r2_key(filename)
    public_url = await r2_service.upload_bytes(data, r2_key, content_type)

    # Create media asset record
    asset = MediaAsset(
        r2_key=r2_key,
        public_url=public_url,
        filename=filename,
        mime_type=content_type,
        size_bytes=len(data),
        alt_text=alt_text,
        caption=caption,
        credit=credit,
        source_url=source_url,
    )
    db.add(asset)
    await db.flush()

    logger.info("Stored media: %s → %s (%d bytes)", source_url, r2_key, len(data))
    return asset


async def upload_file(
    db: AsyncSession,
    *,
    data: bytes,
    filename: str,
    content_type: str,
    alt_text: str = "",
    caption: Optional[str] = None,
    credit: Optional[str] = None,
) -> MediaAsset:
    """Upload a file directly to R2.

    Returns a MediaAsset record.
    """
    if content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Unsupported content type: {content_type}")

    if len(data) > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {len(data)} bytes (max {MAX_FILE_SIZE})")

    r2_key = r2_service.generate_r2_key(filename)
    public_url = await r2_service.upload_bytes(data, r2_key, content_type)

    asset = MediaAsset(
        r2_key=r2_key,
        public_url=public_url,
        filename=filename,
        mime_type=content_type,
        size_bytes=len(data),
        alt_text=alt_text,
        caption=caption,
        credit=credit,
    )
    db.add(asset)
    await db.flush()

    return asset


async def list_media(
    db: AsyncSession, *, page: int = 1, limit: int = 50
) -> tuple[list[MediaAsset], int]:
    """List media assets with pagination."""
    offset = (page - 1) * limit
    result = await db.execute(
        select(MediaAsset)
        .order_by(MediaAsset.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    assets = list(result.scalars().all())

    count_result = await db.execute(select(func.count(MediaAsset.id)))
    total = count_result.scalar_one()

    return assets, total

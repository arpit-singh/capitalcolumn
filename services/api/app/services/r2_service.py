"""Cloudflare R2 (S3-compatible) storage service."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


def _get_r2_client():
    """Create a boto3 S3 client configured for Cloudflare R2."""
    if not settings.r2_endpoint or not settings.R2_ACCESS_KEY_ID:
        return None

    return boto3.client(
        "s3",
        endpoint_url=settings.r2_endpoint,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        config=Config(
            signature_version="s3v4",
            retries={"max_attempts": 3, "mode": "standard"},
        ),
        region_name="auto",
    )


def generate_r2_key(filename: str, prefix: str = "articles") -> str:
    """Generate a unique R2 object key: articles/2026/06/uuid-filename."""
    now = datetime.now(timezone.utc)
    unique = uuid.uuid4().hex[:8]
    safe_name = filename.replace(" ", "-").lower()
    return f"{prefix}/{now.year}/{now.month:02d}/{unique}-{safe_name}"


async def upload_bytes(
    data: bytes,
    r2_key: str,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload bytes to R2 and return the public URL.

    Falls back to logging a warning if R2 is not configured.
    """
    client = _get_r2_client()
    if not client:
        logger.warning("R2 not configured — skipping upload for key: %s", r2_key)
        return f"{settings.R2_PUBLIC_BASE_URL}/{r2_key}"

    try:
        client.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=r2_key,
            Body=data,
            ContentType=content_type,
        )
        logger.info("Uploaded to R2: %s (%d bytes)", r2_key, len(data))
    except ClientError as e:
        logger.error("R2 upload failed for %s: %s", r2_key, e)
        raise

    return f"{settings.R2_PUBLIC_BASE_URL}/{r2_key}"


async def delete_object(r2_key: str) -> bool:
    """Delete an object from R2."""
    client = _get_r2_client()
    if not client:
        logger.warning("R2 not configured — skipping delete for key: %s", r2_key)
        return False

    try:
        client.delete_object(Bucket=settings.R2_BUCKET_NAME, Key=r2_key)
        logger.info("Deleted from R2: %s", r2_key)
        return True
    except ClientError as e:
        logger.error("R2 delete failed for %s: %s", r2_key, e)
        return False


def get_public_url(r2_key: str) -> str:
    """Get the public URL for an R2 key."""
    return f"{settings.R2_PUBLIC_BASE_URL}/{r2_key}"

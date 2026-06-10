"""Cache revalidation endpoint — stub for future Cloudflare cache purge integration."""

import logging
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.db.session import get_db
from app.models.api_key import APIKey
from app.routers.internal_articles import verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/internal", tags=["Cache"])


class RevalidateRequest(BaseModel):
    paths: List[str]


class RevalidateResponse(BaseModel):
    status: str
    paths_requested: int
    message: str


@router.post("/revalidate", response_model=RevalidateResponse)
async def revalidate_cache(
    payload: RevalidateRequest,
    api_key: APIKey = Depends(verify_api_key),
):
    """Request cache invalidation for specific paths.

    Currently a stub that logs the request. In production, connect this to:
    - Cloudflare cache purge API
    - Or a deployment hook to trigger Astro rebuild
    """
    logger.info(
        "Cache revalidation requested for %d paths by API key %s: %s",
        len(payload.paths),
        api_key.name,
        payload.paths,
    )

    # TODO: Implement Cloudflare cache purge
    # cf_client.purge_cache(files=[f"{PUBLIC_SITE_URL}{p}" for p in payload.paths])

    return RevalidateResponse(
        status="accepted",
        paths_requested=len(payload.paths),
        message="Revalidation request logged. Cloudflare cache purge integration pending.",
    )

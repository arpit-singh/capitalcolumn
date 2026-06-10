"""Media upload endpoints — used by the pipeline to upload/fetch images.

Supports both direct file upload and remote URL fetch.
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.routers.internal_articles import verify_api_key
from app.models.api_key import APIKey
from app.schemas.media import MediaListResponse, MediaResponse, MediaUploadByURL
from app.services import media_service

router = APIRouter(prefix="/internal", tags=["Media"])


@router.post("/media/upload", response_model=MediaResponse, status_code=201)
async def upload_media_file(
    file: UploadFile = File(...),
    alt_text: str = Form(""),
    caption: str = Form(None),
    credit: str = Form(None),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """Upload a media file directly."""
    data = await file.read()
    content_type = file.content_type or "application/octet-stream"

    try:
        asset = await media_service.upload_file(
            db,
            data=data,
            filename=file.filename or "upload",
            content_type=content_type,
            alt_text=alt_text,
            caption=caption,
            credit=credit,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return MediaResponse.model_validate(asset)


@router.post("/media/fetch", response_model=MediaResponse, status_code=201)
async def fetch_media_from_url(
    payload: MediaUploadByURL,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """Fetch an image from a remote URL and store it in R2."""
    try:
        asset = await media_service.fetch_and_store(
            db,
            source_url=payload.source_url,
            alt_text=payload.alt_text,
            caption=payload.caption,
            credit=payload.credit,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch image: {str(e)}")

    return MediaResponse.model_validate(asset)


@router.get("/media", response_model=MediaListResponse)
async def list_media(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(verify_api_key),
):
    """List uploaded media assets."""
    assets, total = await media_service.list_media(db, page=page, limit=limit)
    return MediaListResponse(
        items=[MediaResponse.model_validate(a) for a in assets],
        total=total,
    )

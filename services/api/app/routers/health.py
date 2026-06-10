"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {"status": "ok", "app": "capitalcolumn-api"}


@router.get("/health/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    """Check database connectivity."""
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

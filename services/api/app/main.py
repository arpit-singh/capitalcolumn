"""CapitalColumn API — FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import RateLimitMiddleware, RequestLoggingMiddleware
from app.routers import (
    admin,
    auth,
    feeds,
    health,
    internal_articles,
    media,
    pipeline,
    public_articles,
    revalidation,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    logging.getLogger("capitalcolumn.api").info("Starting CapitalColumn API")
    yield
    # Shutdown: dispose engine
    from app.db.session import engine
    await engine.dispose()
    logging.getLogger("capitalcolumn.api").info("CapitalColumn API shut down")


app = FastAPI(
    title="CapitalColumn API",
    description="Publishing and content management API for CapitalColumn financial news.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middleware (order matters: last added = first executed) ---

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting for public endpoints (60 req/min per IP)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Request logging
app.add_middleware(RequestLoggingMiddleware)

# --- Routers ---

# Health
app.include_router(health.router)

# Internal (API key auth)
app.include_router(internal_articles.router)
app.include_router(media.router)
app.include_router(revalidation.router)

# Public (no auth)
app.include_router(public_articles.router)
app.include_router(feeds.router)

# Admin (JWT auth)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(pipeline.router)

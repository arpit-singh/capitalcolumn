"""Request logging and rate limiting middleware."""

import logging
import time
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("capitalcolumn.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with method, path, status, and duration."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s → %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["X-Response-Time"] = f"{duration_ms:.1f}ms"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter for public endpoints.

    Limits requests per IP per window. Only applies to /public/ and /feeds/ paths.
    Not suitable for multi-process deployments — use Cloudflare rate limiting in production.
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.window = 60  # seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        # Only rate-limit public endpoints
        if not (path.startswith("/public/") or path.startswith("/feeds/")):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Prune old hits
        self._hits[client_ip] = [
            t for t in self._hits[client_ip] if now - t < self.window
        ]

        if len(self._hits[client_ip]) >= self.rpm:
            return Response(
                content='{"detail":"Rate limit exceeded. Try again later."}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(self.window)},
            )

        self._hits[client_ip].append(now)
        return await call_next(request)

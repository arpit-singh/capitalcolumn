"""Security utilities: API key hashing, JWT token handling."""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings


# ---------------------------------------------------------------------------
# API Key Utilities
# ---------------------------------------------------------------------------

def generate_api_key() -> str:
    """Generate a random API key prefixed with 'cc_'."""
    return f"cc_{secrets.token_urlsafe(32)}"


def hash_api_key(key: str) -> str:
    """SHA-256 hash an API key for storage."""
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    """Verify a plain API key against its hash."""
    return hash_api_key(plain_key) == hashed_key


# ---------------------------------------------------------------------------
# JWT Utilities
# ---------------------------------------------------------------------------

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT and return the subject, or None if invalid."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload.get("sub")
    except JWTError:
        return None

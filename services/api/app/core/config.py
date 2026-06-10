"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    # App
    APP_ENV: str = "production"
    APP_NAME: str = "capitalcolumn-api"
    DEBUG: bool = False

    # URLs
    API_BASE_URL: str = "https://api.capitalcolumn.in"
    PUBLIC_SITE_URL: str = "https://capitalcolumn.in"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://capitalcolumn_user:CapColUser*1234@postgres:5432/capitalcolumn"

    # Sync database URL (for Alembic migrations)
    @property
    def DATABASE_URL_SYNC(self) -> str:
        return self.DATABASE_URL.replace("+asyncpg", "+psycopg")

    # R2 / S3 Storage
    R2_PUBLIC_BASE_URL: str = "https://media.capitalcolumn.in"
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "capitalcolumn-media"
    R2_ENDPOINT_URL: str = ""

    @property
    def r2_endpoint(self) -> str:
        if self.R2_ENDPOINT_URL:
            return self.R2_ENDPOINT_URL
        if self.R2_ACCOUNT_ID:
            return f"https://{self.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
        return ""

    # CORS
    CORS_ALLOWED_ORIGINS: str = "https://capitalcolumn.in,https://www.capitalcolumn.in"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]

    # Auth
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()

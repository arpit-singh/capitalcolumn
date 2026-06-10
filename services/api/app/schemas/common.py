"""Common schemas used across routers."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response matching the frontend PaginatedResponse<T> type."""
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int


class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None


class MessageResponse(BaseModel):
    message: str

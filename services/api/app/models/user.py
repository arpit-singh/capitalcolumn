"""User model for admin authentication."""

import enum
from typing import Optional

from sqlalchemy import Boolean, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(300), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role", create_constraint=True),
        default=UserRole.editor,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

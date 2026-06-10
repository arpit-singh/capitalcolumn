"""Add users table and seed admin user.

Revision ID: 003_users
Revises: 002_seed_data
Create Date: 2026-06-07
"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "003_users"
down_revision: Union[str, None] = "002_seed_data"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(128), nullable=False),
        sa.Column("full_name", sa.String(300), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin", "editor", "viewer", name="user_role", create_constraint=True),
            nullable=False,
            server_default="editor",
        ),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # Seed a default admin user
    # Password: CapCol@dmin2026
    # Use bcrypt directly instead of passlib to avoid version incompatibilities
    import bcrypt
    hashed = bcrypt.hashpw(b"CapCol@dmin2026", bcrypt.gensalt()).decode("utf-8")
    uid = str(uuid.uuid4())

    op.execute(sa.text(
        f"INSERT INTO users (id, email, hashed_password, full_name, role, is_active) "
        f"VALUES ('{uid}', 'admin@capitalcolumn.in', '{hashed}', 'Admin', 'admin', true)"
    ))


def downgrade() -> None:
    op.drop_table("users")
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)

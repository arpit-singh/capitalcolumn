"""Initial schema — all tables.

Revision ID: 001_initial
Revises: None
Create Date: 2026-06-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Categories ---
    op.create_table(
        "categories",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False, unique=True),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("parent_id", UUID(as_uuid=True), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("sort_order", sa.Integer, default=0, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"])

    # --- Tags ---
    op.create_table(
        "tags",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False, unique=True),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_tags_slug", "tags", ["slug"])

    # --- Authors ---
    op.create_table(
        "authors",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("slug", sa.String(300), nullable=False, unique=True),
        sa.Column("bio", sa.Text, nullable=True),
        sa.Column("avatar_media_id", UUID(as_uuid=True), nullable=True),
        sa.Column(
            "author_type",
            sa.Enum("human", "ai_assisted", "editorial_team", name="author_type", create_constraint=True),
            nullable=False,
            server_default="editorial_team",
        ),
        sa.Column("social_links", JSONB, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_authors_slug", "authors", ["slug"])

    # --- Media Assets ---
    op.create_table(
        "media_assets",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("r2_key", sa.String(1000), nullable=False, unique=True),
        sa.Column("public_url", sa.String(2000), nullable=False),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.Integer, nullable=True),
        sa.Column("width", sa.Integer, nullable=True),
        sa.Column("height", sa.Integer, nullable=True),
        sa.Column("alt_text", sa.String(1000), server_default="", nullable=False),
        sa.Column("caption", sa.Text, nullable=True),
        sa.Column("credit", sa.String(500), nullable=True),
        sa.Column("source_url", sa.String(2000), nullable=True),
        sa.Column("uploaded_by", UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # --- Company Tickers ---
    op.create_table(
        "company_tickers",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("ticker", sa.String(50), nullable=False, unique=True),
        sa.Column("exchange", sa.String(50), nullable=False),
        sa.Column("country", sa.String(100), server_default="India", nullable=False),
        sa.Column("sector", sa.String(200), nullable=True),
        sa.Column("industry", sa.String(200), nullable=True),
        sa.Column("logo_media_id", UUID(as_uuid=True), nullable=True),
        sa.Column("company_page_slug", sa.String(200), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_company_tickers_ticker", "company_tickers", ["ticker"])
    op.create_index("ix_company_tickers_slug", "company_tickers", ["company_page_slug"])

    # --- Articles ---
    op.create_table(
        "articles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("external_id", sa.String(255), nullable=True, unique=True),
        sa.Column("slug", sa.String(512), nullable=False, unique=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("dek", sa.Text, nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("body_markdown", sa.Text, nullable=False),
        sa.Column("body_html", sa.Text, nullable=True),
        sa.Column("key_takeaways", JSONB, nullable=True),
        sa.Column(
            "status",
            sa.Enum("draft", "in_review", "scheduled", "published", "archived", "rejected",
                     name="article_status", create_constraint=True),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("language", sa.String(10), server_default="en", nullable=False),
        sa.Column(
            "article_type",
            sa.Enum("news", "analysis", "explainer", "earnings", "market_update", "alert", "opinion",
                     name="article_type", create_constraint=True),
            nullable=False,
            server_default="news",
        ),
        sa.Column("category_id", UUID(as_uuid=True), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("author_id", UUID(as_uuid=True), sa.ForeignKey("authors.id"), nullable=True),
        sa.Column("featured_image_id", UUID(as_uuid=True), sa.ForeignKey("media_assets.id"), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reading_time_minutes", sa.Integer, server_default="1", nullable=False),
        sa.Column("seo_title", sa.String(500), nullable=True),
        sa.Column("seo_description", sa.Text, nullable=True),
        sa.Column("canonical_url", sa.String(1000), nullable=True),
        sa.Column("meta_keywords", JSONB, nullable=True),
        sa.Column("noindex", sa.Boolean, server_default=sa.text("false"), nullable=False),
        sa.Column("is_ai_generated", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("is_editor_reviewed", sa.Boolean, server_default=sa.text("false"), nullable=False),
        sa.Column("ai_pipeline_name", sa.String(255), nullable=True),
        sa.Column("ai_model_name", sa.String(255), nullable=True),
        sa.Column("ai_pipeline_version", sa.String(50), nullable=True),
        sa.Column("confidence_score", sa.Numeric(4, 2), nullable=True),
        sa.Column(
            "fact_check_status",
            sa.Enum("unchecked", "ai_checked", "human_checked", "source_verified",
                     name="fact_check_status", create_constraint=True),
            nullable=False,
            server_default="unchecked",
        ),
        sa.Column("disclaimer_variant", sa.String(100), nullable=True),
        sa.Column("correction_note", sa.Text, nullable=True),
        sa.Column("last_corrected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_articles_slug", "articles", ["slug"])
    op.create_index("ix_articles_external_id", "articles", ["external_id"])
    op.create_index("ix_articles_status", "articles", ["status"])

    # --- Article Sources ---
    op.create_table(
        "article_sources",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("article_id", UUID(as_uuid=True), sa.ForeignKey("articles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_name", sa.String(500), nullable=False),
        sa.Column("source_url", sa.String(2000), nullable=False),
        sa.Column(
            "source_type",
            sa.Enum("company_filing", "exchange_disclosure", "press_release", "news_article",
                     "official_statement", "market_data", "social_media", "other",
                     name="source_type", create_constraint=True),
            nullable=False,
            server_default="other",
        ),
        sa.Column("publisher", sa.String(500), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("accessed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("relevance_note", sa.Text, nullable=True),
        sa.Column("quote_used", sa.Text, nullable=True),
        sa.Column("is_primary_source", sa.Boolean, server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_article_sources_article_id", "article_sources", ["article_id"])

    # --- Article ↔ Tag junction ---
    op.create_table(
        "article_tags",
        sa.Column("article_id", UUID(as_uuid=True), sa.ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", UUID(as_uuid=True), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )

    # --- Article ↔ Ticker junction ---
    op.create_table(
        "article_tickers",
        sa.Column("article_id", UUID(as_uuid=True), sa.ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("ticker_id", UUID(as_uuid=True), sa.ForeignKey("company_tickers.id", ondelete="CASCADE"), primary_key=True),
    )

    # --- API Keys ---
    op.create_table(
        "api_keys",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("key_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_api_keys_hash", "api_keys", ["key_hash"])

    # --- Audit Logs ---
    op.create_table(
        "audit_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "actor_type",
            sa.Enum("user", "api_key", "system", "ai_agent", name="actor_type", create_constraint=True),
            nullable=False,
        ),
        sa.Column("actor_id", sa.String(255), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", UUID(as_uuid=True), nullable=False),
        sa.Column("before_json", JSONB, nullable=True),
        sa.Column("after_json", JSONB, nullable=True),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity_type", "entity_id"])
    op.create_index("ix_audit_logs_created", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("api_keys")
    op.drop_table("article_tickers")
    op.drop_table("article_tags")
    op.drop_table("article_sources")
    op.drop_table("articles")
    op.drop_table("company_tickers")
    op.drop_table("media_assets")
    op.drop_table("authors")
    op.drop_table("tags")
    op.drop_table("categories")
    # Drop enum types
    sa.Enum(name="article_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="article_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="fact_check_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="source_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="author_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="actor_type").drop(op.get_bind(), checkfirst=True)

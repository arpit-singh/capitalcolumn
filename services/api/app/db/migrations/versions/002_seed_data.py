"""Seed default categories, tags, and author.

Revision ID: 002_seed_data
Revises: 001_initial
Create Date: 2026-06-07
"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

revision: str = "002_seed_data"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _uuid() -> str:
    return str(uuid.uuid4())


def _q(s: str) -> str:
    """Escape a string for safe SQL insertion (single-quote escaping)."""
    return s.replace("'", "''")


def upgrade() -> None:
    # --- Default Author ---
    author_id = _uuid()
    op.execute(sa.text(
        f"INSERT INTO authors (id, name, slug, bio, author_type, is_active) "
        f"VALUES ('{author_id}', 'CapitalColumn Editorial Desk', 'editorial-desk', "
        f"'{_q('AI-assisted editorial desk covering Indian and global financial markets with source-linked, transparent reporting.')}', "
        f"'editorial_team', true)"
    ))

    # --- Categories ---
    categories = [
        ("Markets", "markets", "Market indices, trading activity, and broad market movements.", 1),
        ("Earnings", "earnings", "Quarterly results, revenue, and profit analysis.", 2),
        ("Companies", "companies", "Corporate news, management changes, and business strategy.", 3),
        ("Technology", "technology", "Tech sector news, AI, cloud computing, and digital platforms.", 4),
        ("Banking", "banking", "Banking sector, RBI policy, credit growth, and fintech.", 5),
        ("Energy", "energy", "Oil, gas, renewables, and power sector coverage.", 6),
        ("Consumer", "consumer", "FMCG, retail, auto, and consumer sentiment.", 7),
        ("Industrials", "industrials", "Infrastructure, manufacturing, and industrial output.", 8),
        ("Healthcare", "healthcare", "Pharma, biotech, hospitals, and health policy.", 9),
        ("Global Markets", "global-markets", "International markets, Fed policy, and global macro.", 10),
        ("IPOs", "ipos", "IPO filings, listings, subscriptions, and debut performance.", 11),
        ("Policy & Regulation", "policy-regulation", "Government policy, SEBI regulations, and economic reforms.", 12),
    ]
    for name, slug, desc, order in categories:
        cid = _uuid()
        op.execute(sa.text(
            f"INSERT INTO categories (id, name, slug, description, sort_order, is_active) "
            f"VALUES ('{cid}', '{_q(name)}', '{slug}', '{_q(desc)}', {order}, true)"
        ))

    # --- Tags ---
    tags = [
        ("AI & Machine Learning", "ai-ml"),
        ("Electric Vehicles", "electric-vehicles"),
        ("Semiconductors", "semiconductors"),
        ("Interest Rates", "interest-rates"),
        ("Inflation", "inflation"),
        ("Mergers & Acquisitions", "mergers-acquisitions"),
        ("Quarterly Results", "quarterly-results"),
        ("Management Change", "management-change"),
        ("Analyst Rating", "analyst-rating"),
        ("Valuation", "valuation"),
        ("Debt", "debt"),
        ("Margin Pressure", "margin-pressure"),
        ("5G & Telecom", "5g-telecom"),
        ("Cloud Computing", "cloud-computing"),
        ("Digital Payments", "digital-payments"),
        ("Real Estate", "real-estate"),
        ("ESG", "esg"),
        ("Startup & Venture", "startup-venture"),
    ]
    for name, slug in tags:
        tid = _uuid()
        op.execute(sa.text(
            f"INSERT INTO tags (id, name, slug) "
            f"VALUES ('{tid}', '{_q(name)}', '{slug}')"
        ))

    # --- Seed API Key (for testing) ---
    import hashlib
    seed_key = "cc_SEED_KEY_change_me_in_production"
    key_hash = hashlib.sha256(seed_key.encode()).hexdigest()
    kid = _uuid()
    op.execute(sa.text(
        f"INSERT INTO api_keys (id, name, key_hash, is_active, description) "
        f"VALUES ('{kid}', 'Development Seed Key', '{key_hash}', true, "
        f"'Seed API key for initial development. Replace in production.')"
    ))


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM api_keys WHERE name = 'Development Seed Key'"))
    op.execute(sa.text("DELETE FROM tags"))
    op.execute(sa.text("DELETE FROM categories"))
    op.execute(sa.text("DELETE FROM authors WHERE slug = 'editorial-desk'"))

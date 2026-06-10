"""Slug generation service."""

import re
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article


async def generate_unique_slug(title: str, db: AsyncSession, existing_id=None) -> str:
    """Generate a URL-safe slug from a title, ensuring uniqueness.

    If the slug already exists (for a different article), append -2, -3, etc.
    """
    base_slug = slugify(title, max_length=200, lowercase=True)

    if not base_slug:
        base_slug = "article"

    slug = base_slug
    counter = 1

    while True:
        query = select(Article.id).where(Article.slug == slug)
        if existing_id:
            query = query.where(Article.id != existing_id)
        result = await db.execute(query)
        if result.scalar_one_or_none() is None:
            return slug
        counter += 1
        slug = f"{base_slug}-{counter}"

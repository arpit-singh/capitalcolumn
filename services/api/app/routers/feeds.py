"""RSS, Atom, Sitemap, and News Sitemap feeds."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.db.session import get_db
from app.models.article import Article, ArticleStatus
from app.models.taxonomy import Category

router = APIRouter(tags=["Feeds"])


def _build_rss_xml(articles: list[Article]) -> str:
    """Build an RSS 2.0 XML feed."""
    items = []
    for a in articles:
        pub_date = ""
        if a.published_at:
            pub_date = a.published_at.strftime("%a, %d %b %Y %H:%M:%S +0000")

        category_name = a.category.name if a.category else ""
        description = a.seo_description or a.summary or a.dek or ""

        items.append(f"""    <item>
      <title><![CDATA[{a.title}]]></title>
      <link>{settings.PUBLIC_SITE_URL}/news/{a.slug}</link>
      <guid isPermaLink="true">{settings.PUBLIC_SITE_URL}/news/{a.slug}</guid>
      <description><![CDATA[{description}]]></description>
      <category><![CDATA[{category_name}]]></category>
      <pubDate>{pub_date}</pubDate>
    </item>""")

    items_xml = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>CapitalColumn</title>
    <link>{settings.PUBLIC_SITE_URL}</link>
    <description>AI-powered financial intelligence, grounded in primary sources and editorial integrity.</description>
    <language>en</language>
    <atom:link href="{settings.API_BASE_URL}/feeds/rss.xml" rel="self" type="application/rss+xml"/>
    <lastBuildDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
{items_xml}
  </channel>
</rss>"""


def _build_atom_xml(articles: list[Article]) -> str:
    """Build an Atom feed."""
    entries = []
    for a in articles:
        updated = (a.updated_at or a.published_at or a.created_at).strftime("%Y-%m-%dT%H:%M:%SZ")
        summary = a.seo_description or a.summary or a.dek or ""

        entries.append(f"""  <entry>
    <title><![CDATA[{a.title}]]></title>
    <link href="{settings.PUBLIC_SITE_URL}/news/{a.slug}"/>
    <id>{settings.PUBLIC_SITE_URL}/news/{a.slug}</id>
    <updated>{updated}</updated>
    <summary><![CDATA[{summary}]]></summary>
  </entry>""")

    entries_xml = "\n".join(entries)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>CapitalColumn</title>
  <link href="{settings.PUBLIC_SITE_URL}"/>
  <link href="{settings.API_BASE_URL}/feeds/atom.xml" rel="self"/>
  <updated>{now}</updated>
  <id>{settings.PUBLIC_SITE_URL}/</id>
  <subtitle>AI-powered financial intelligence, grounded in primary sources and editorial integrity.</subtitle>
{entries_xml}
</feed>"""


def _build_sitemap_xml(articles: list[Article], categories: list[Category]) -> str:
    """Build an XML sitemap."""
    urls = []

    # Static pages
    for path in ["/", "/about", "/contact", "/editorial-policy", "/privacy", "/terms", "/disclaimer", "/search"]:
        urls.append(f"""  <url>
    <loc>{settings.PUBLIC_SITE_URL}{path}</loc>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if path == "/" else "0.5"}</priority>
  </url>""")

    # Category pages
    for cat in categories:
        urls.append(f"""  <url>
    <loc>{settings.PUBLIC_SITE_URL}/category/{cat.slug}</loc>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""")

    # Article pages
    for a in articles:
        lastmod = (a.updated_at or a.published_at or a.created_at).strftime("%Y-%m-%d")
        urls.append(f"""  <url>
    <loc>{settings.PUBLIC_SITE_URL}/news/{a.slug}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    urls_xml = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.w3.org/2000/sitemaps/schemas/sitemap/0.9">
{urls_xml}
</urlset>"""


def _build_news_sitemap_xml(articles: list[Article]) -> str:
    """Build a Google News sitemap (recent articles only)."""
    urls = []
    for a in articles:
        pub_date = (a.published_at or a.created_at).strftime("%Y-%m-%dT%H:%M:%SZ")
        urls.append(f"""  <url>
    <loc>{settings.PUBLIC_SITE_URL}/news/{a.slug}</loc>
    <news:news>
      <news:publication>
        <news:name>CapitalColumn</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>{pub_date}</news:publication_date>
      <news:title><![CDATA[{a.title}]]></news:title>
    </news:news>
  </url>""")

    urls_xml = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.w3.org/2000/sitemaps/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
{urls_xml}
</urlset>"""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/feeds/rss.xml")
async def rss_feed(db: AsyncSession = Depends(get_db)):
    """RSS 2.0 feed of the latest 50 published articles."""
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.category))
        .where(Article.status == ArticleStatus.published)
        .order_by(Article.published_at.desc())
        .limit(50)
    )
    articles = list(result.scalars().all())
    xml = _build_rss_xml(articles)
    return Response(content=xml, media_type="application/rss+xml; charset=utf-8")


@router.get("/feeds/atom.xml")
async def atom_feed(db: AsyncSession = Depends(get_db)):
    """Atom feed of the latest 50 published articles."""
    result = await db.execute(
        select(Article)
        .where(Article.status == ArticleStatus.published)
        .order_by(Article.published_at.desc())
        .limit(50)
    )
    articles = list(result.scalars().all())
    xml = _build_atom_xml(articles)
    return Response(content=xml, media_type="application/atom+xml; charset=utf-8")


@router.get("/sitemap.xml")
async def sitemap(db: AsyncSession = Depends(get_db)):
    """Full sitemap including static pages, categories, and all published articles."""
    articles_result = await db.execute(
        select(Article)
        .where(Article.status == ArticleStatus.published)
        .order_by(Article.published_at.desc())
    )
    articles = list(articles_result.scalars().all())

    categories_result = await db.execute(
        select(Category).where(Category.is_active == True).order_by(Category.sort_order)
    )
    categories = list(categories_result.scalars().all())

    xml = _build_sitemap_xml(articles, categories)
    return Response(content=xml, media_type="application/xml; charset=utf-8")


@router.get("/news-sitemap.xml")
async def news_sitemap(db: AsyncSession = Depends(get_db)):
    """Google News sitemap — last 200 published articles (per Google's guidelines)."""
    result = await db.execute(
        select(Article)
        .where(Article.status == ArticleStatus.published)
        .order_by(Article.published_at.desc())
        .limit(200)
    )
    articles = list(result.scalars().all())
    xml = _build_news_sitemap_xml(articles)
    return Response(content=xml, media_type="application/xml; charset=utf-8")

"""Sitemap monitor — discovers new articles on sites without RSS feeds."""

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional
from xml.etree import ElementTree

import httpx
from bs4 import BeautifulSoup
from rich.console import Console

from config import SEEN_URLS_FILE, DATA_DIR
from monitor.rss_monitor import NewsTopic, _load_seen_urls, _save_seen_urls

console = Console()

SITEMAP_NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
LAST_CHECK_FILE = DATA_DIR / "sitemap_last_check.json"


def _load_last_check() -> dict:
    """Load timestamps of last sitemap check per source."""
    if LAST_CHECK_FILE.exists():
        try:
            return json.loads(LAST_CHECK_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _save_last_check(data: dict) -> None:
    LAST_CHECK_FILE.write_text(json.dumps(data), encoding="utf-8")


def _fetch_sitemap_urls(sitemap_url: str) -> list[dict]:
    """Parse a sitemap.xml and return list of {loc, lastmod}."""
    try:
        resp = httpx.get(sitemap_url, timeout=15, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        console.print(f"  [red]Error fetching sitemap {sitemap_url}:[/red] {e}")
        return []

    urls = []
    try:
        root = ElementTree.fromstring(resp.text)
        # Handle sitemap index (recursive)
        sitemapindex = root.findall("ns:sitemap", SITEMAP_NS)
        if sitemapindex:
            for sm in sitemapindex:
                loc = sm.find("ns:loc", SITEMAP_NS)
                if loc is not None and loc.text:
                    urls.extend(_fetch_sitemap_urls(loc.text.strip()))
            return urls

        # Regular sitemap
        for url_elem in root.findall("ns:url", SITEMAP_NS):
            loc = url_elem.find("ns:loc", SITEMAP_NS)
            lastmod = url_elem.find("ns:lastmod", SITEMAP_NS)
            if loc is not None and loc.text:
                urls.append({
                    "loc": loc.text.strip(),
                    "lastmod": lastmod.text.strip() if lastmod is not None and lastmod.text else None,
                })
    except ElementTree.ParseError as e:
        console.print(f"  [red]Error parsing sitemap XML:[/red] {e}")

    return urls


def _fetch_page_meta(url: str) -> tuple[str, str]:
    """Fetch a page and extract title + meta description."""
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (compatible; CapitalColumnBot/1.0)"
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        description = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            description = meta["content"].strip()

        return title, description
    except Exception:
        return "", ""


def poll_sitemaps(sources_config: dict) -> list[NewsTopic]:
    """Poll configured sitemaps and return new (unseen) topics.

    Args:
        sources_config: The full sources.json config dict.

    Returns:
        List of NewsTopic objects for pages not seen before.
    """
    seen = _load_seen_urls()
    last_check = _load_last_check()
    new_topics: list[NewsTopic] = []

    for sm_cfg in sources_config.get("sitemaps", []):
        name = sm_cfg.get("name", "Unknown")
        sitemap_url = sm_cfg.get("url", "")
        category = sm_cfg.get("category", "markets")

        if not sitemap_url:
            continue

        console.print(f"  [dim]Checking sitemap:[/dim] {name}")
        urls = _fetch_sitemap_urls(sitemap_url)

        for url_info in urls:
            loc = url_info["loc"]
            url_hash = hashlib.sha256(loc.encode()).hexdigest()[:16]

            if url_hash in seen:
                continue

            # Fetch page metadata
            title, summary = _fetch_page_meta(loc)
            if not title:
                seen.add(url_hash)
                continue

            topic = NewsTopic(
                title=title,
                url=loc,
                summary=summary[:500],
                source_name=name,
                category=category,
                published_at=url_info.get("lastmod"),
            )
            new_topics.append(topic)
            seen.add(url_hash)

    _save_seen_urls(seen)
    _save_last_check(last_check)
    return new_topics

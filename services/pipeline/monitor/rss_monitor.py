"""RSS feed monitor — polls configured feeds and discovers new stories."""

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import feedparser
from rich.console import Console

from config import SEEN_URLS_FILE, BASE_DIR

console = Console()


@dataclass
class NewsTopic:
    """A discovered news story ready for pipeline processing."""
    title: str
    url: str
    summary: str
    source_name: str
    category: str
    published_at: Optional[str] = None
    discovered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    url_hash: str = ""

    def __post_init__(self):
        if not self.url_hash:
            self.url_hash = hashlib.sha256(self.url.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "NewsTopic":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


def _load_seen_urls() -> set:
    """Load the set of already-processed URL hashes."""
    if SEEN_URLS_FILE.exists():
        try:
            data = json.loads(SEEN_URLS_FILE.read_text(encoding="utf-8"))
            return set(data.get("hashes", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def _save_seen_urls(hashes: set) -> None:
    """Persist seen URL hashes to disk."""
    SEEN_URLS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_URLS_FILE.write_text(
        json.dumps({"hashes": list(hashes), "updated_at": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )


def _load_sources() -> dict:
    """Load the source configuration."""
    sources_file = BASE_DIR / "monitor" / "sources.json"
    if not sources_file.exists():
        console.print("[red]sources.json not found![/red]")
        return {"rss_feeds": [], "sitemaps": []}
    return json.loads(sources_file.read_text(encoding="utf-8"))


def _parse_published_date(entry) -> Optional[str]:
    """Extract and normalize the published date from a feed entry."""
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                dt = datetime(*parsed[:6], tzinfo=timezone.utc)
                return dt.isoformat()
            except Exception:
                pass
    # Fallback to string
    for attr in ("published", "updated"):
        val = getattr(entry, attr, None)
        if val:
            return val
    return None


def poll_rss_feeds(max_per_feed: int = 10) -> list[NewsTopic]:
    """Poll all configured RSS feeds and return new (unseen) topics.

    Args:
        max_per_feed: Maximum entries to process per feed (most recent first).

    Returns:
        List of NewsTopic objects for stories not seen before.
    """
    sources = _load_sources()
    seen = _load_seen_urls()
    new_topics: list[NewsTopic] = []

    for feed_cfg in sources.get("rss_feeds", []):
        name = feed_cfg["name"]
        url = feed_cfg["url"]
        category = feed_cfg.get("category", "markets")

        console.print(f"  [dim]Polling:[/dim] {name}")
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            console.print(f"  [red]Error parsing {name}:[/red] {e}")
            continue

        if feed.bozo and not feed.entries:
            console.print(f"  [yellow]Warning: {name} returned no entries[/yellow]")
            continue

        entries = feed.entries[:max_per_feed]
        for entry in entries:
            link = getattr(entry, "link", "") or ""
            if not link:
                continue

            url_hash = hashlib.sha256(link.encode()).hexdigest()[:16]
            if url_hash in seen:
                continue

            title = getattr(entry, "title", "").strip()
            summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
            # Strip HTML tags from summary
            if "<" in summary:
                from html.parser import HTMLParser
                class _Strip(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self._parts = []
                    def handle_data(self, d):
                        self._parts.append(d)
                    def get_text(self):
                        return " ".join(self._parts)
                s = _Strip()
                s.feed(summary)
                summary = s.get_text()

            summary = summary[:500].strip()

            if not title:
                continue

            topic = NewsTopic(
                title=title,
                url=link,
                summary=summary,
                source_name=name,
                category=category,
                published_at=_parse_published_date(entry),
            )
            new_topics.append(topic)
            seen.add(url_hash)

    _save_seen_urls(seen)
    return new_topics


def mark_url_seen(url: str) -> None:
    """Manually mark a URL as seen (for dedup)."""
    seen = _load_seen_urls()
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    seen.add(url_hash)
    _save_seen_urls(seen)


def reset_seen_urls() -> None:
    """Clear all seen URLs — useful for testing."""
    _save_seen_urls(set())

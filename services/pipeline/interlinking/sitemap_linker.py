"""Sitemap-based internal linker — finds related articles and injects links.

Workflow:
1. Fetches the site's sitemap.xml and article list from the API
2. Builds a TF-IDF search index on article titles
3. Finds related articles for a new article using cosine similarity
4. Injects natural inline links and a "Related Articles" section
"""

import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from xml.etree import ElementTree

import httpx
from rich.console import Console
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config

console = Console()


@dataclass
class SitemapArticle:
    """An article from the sitemap index."""
    slug: str
    title: str
    url: str
    category: str = ""
    published_at: str = ""

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "url": self.url,
            "category": self.category,
            "published_at": self.published_at,
        }


class SitemapIndex:
    """Cached index of all published articles for interlinking."""

    def __init__(self):
        self.articles: list[SitemapArticle] = []
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._tfidf_matrix = None
        self._last_refresh: float = 0

    def is_stale(self) -> bool:
        """Check if the cache needs refreshing."""
        ttl = config.SITEMAP_CACHE_TTL_HOURS * 3600
        return (time.time() - self._last_refresh) > ttl

    def refresh(self) -> None:
        """Refresh the article index from the API."""
        console.print("  [dim]Refreshing sitemap index...[/dim]")

        articles = []

        # Try fetching from the public articles API first (more structured)
        try:
            resp = httpx.get(
                f"{config.API_BASE_URL}/public/articles",
                params={"limit": 500, "status": "published"},
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                items = data if isinstance(data, list) else data.get("items", [])
                for item in items:
                    slug = item.get("slug", "")
                    title = item.get("title", "")
                    cat = item.get("category", {})
                    cat_slug = cat.get("slug", "") if isinstance(cat, dict) else ""
                    pub_at = item.get("published_at", "")

                    if slug and title:
                        articles.append(SitemapArticle(
                            slug=slug,
                            title=title,
                            url=f"{config.PUBLIC_SITE_URL}/news/{slug}",
                            category=cat_slug,
                            published_at=pub_at,
                        ))
        except Exception as e:
            console.print(f"  [yellow]API fetch failed, trying sitemap:[/yellow] {e}")

        # Fallback: parse sitemap.xml
        if not articles:
            try:
                resp = httpx.get(f"{config.API_BASE_URL}/sitemap.xml", timeout=15)
                if resp.status_code == 200:
                    root = ElementTree.fromstring(resp.text)
                    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                    for url_elem in root.findall("ns:url", ns):
                        loc = url_elem.find("ns:loc", ns)
                        if loc is not None and loc.text and "/news/" in loc.text:
                            url = loc.text.strip()
                            slug = url.rsplit("/news/", 1)[-1].rstrip("/")
                            # Title from slug (rough, but usable for matching)
                            title = slug.replace("-", " ").title()
                            articles.append(SitemapArticle(
                                slug=slug,
                                title=title,
                                url=url,
                            ))
            except Exception as e:
                console.print(f"  [red]Sitemap fetch failed:[/red] {e}")

        self.articles = articles
        self._build_index()
        self._last_refresh = time.time()
        self._save_cache()

        console.print(f"  [green]✓[/green] Indexed {len(self.articles)} articles")

    def _build_index(self) -> None:
        """Build TF-IDF index from article titles."""
        if not self.articles:
            self._vectorizer = None
            self._tfidf_matrix = None
            return

        titles = [a.title for a in self.articles]
        self._vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
        )
        self._tfidf_matrix = self._vectorizer.fit_transform(titles)

    def _save_cache(self) -> None:
        """Save the index to disk."""
        cache = {
            "articles": [a.to_dict() for a in self.articles],
            "refreshed_at": datetime.now(timezone.utc).isoformat(),
        }
        config.SITEMAP_CACHE_FILE.write_text(
            json.dumps(cache, indent=2), encoding="utf-8"
        )

    def load_cache(self) -> bool:
        """Load index from disk cache. Returns True if loaded successfully."""
        if not config.SITEMAP_CACHE_FILE.exists():
            return False

        try:
            data = json.loads(config.SITEMAP_CACHE_FILE.read_text(encoding="utf-8"))
            self.articles = [SitemapArticle(**a) for a in data.get("articles", [])]
            self._build_index()

            refreshed = data.get("refreshed_at", "")
            if refreshed:
                dt = datetime.fromisoformat(refreshed)
                self._last_refresh = dt.timestamp()
            return len(self.articles) > 0
        except Exception:
            return False

    def find_related(
        self,
        title: str,
        body: str = "",
        max_results: int = None,
        exclude_slug: str = "",
    ) -> list[SitemapArticle]:
        """Find articles related to a given title/body.

        Args:
            title: The new article's title.
            body: The new article's body (optional, for better matching).
            max_results: Max related articles to return.
            exclude_slug: Slug to exclude (the article itself).

        Returns:
            List of related SitemapArticle objects, sorted by relevance.
        """
        max_results = max_results or config.MAX_INTERNAL_LINKS

        if not self.articles or self._vectorizer is None:
            return []

        # Combine title and first 200 words of body for matching
        query_text = title
        if body:
            body_words = body.split()[:200]
            query_text += " " + " ".join(body_words)

        query_vec = self._vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self._tfidf_matrix).flatten()

        # Rank and filter
        ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in ranked:
            if score < 0.05:  # Minimum relevance threshold
                break
            article = self.articles[idx]
            if article.slug == exclude_slug:
                continue
            results.append(article)
            if len(results) >= max_results:
                break

        return results


# Module-level singleton
_index = SitemapIndex()


def get_index() -> SitemapIndex:
    """Get the sitemap index, refreshing if stale."""
    if not _index.articles:
        _index.load_cache()
    if _index.is_stale():
        _index.refresh()
    return _index


def inject_internal_links(
    body_markdown: str,
    title: str,
    slug: str = "",
) -> str:
    """Inject relevant internal links into an article's markdown body.

    Strategy:
    - Find related articles via TF-IDF similarity
    - Insert inline links where topic overlap is natural
    - Add a "Related Articles" section at the end if ≥2 matches
    - Never force links — only add when genuinely relevant

    Args:
        body_markdown: The article body in markdown.
        title: The article title (for similarity matching).
        slug: The article's own slug (to avoid self-linking).

    Returns:
        Modified markdown with internal links injected.
    """
    index = get_index()
    related = index.find_related(title, body_markdown, exclude_slug=slug)

    if not related:
        return body_markdown

    modified = body_markdown
    linked_slugs = set()

    # Strategy 1: Inline links — find mentions of related article topics in the body
    for article in related[:3]:
        # Extract 2-3 word key phrases from the related article title
        title_words = [
            w for w in article.title.lower().split()
            if w not in {"the", "a", "an", "is", "are", "of", "in", "to", "for", "and", "on", "at", "by", "with"}
            and len(w) > 2
        ]

        # Look for natural mentions of these key words in the body
        for phrase_len in [3, 2]:
            if article.slug in linked_slugs:
                break
            for i in range(len(title_words) - phrase_len + 1):
                phrase = " ".join(title_words[i:i + phrase_len])
                if len(phrase) < 5:
                    continue

                # Case-insensitive search in the body
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                match = pattern.search(modified)
                if match:
                    original_text = match.group(0)
                    # Only link the first occurrence, and not inside existing links
                    before = modified[:match.start()]
                    if "[" not in before[-50:] or "]" not in before[-50:]:
                        link = f"[{original_text}]({article.url})"
                        modified = modified[:match.start()] + link + modified[match.end():]
                        linked_slugs.add(article.slug)
                        break

    # Strategy 2: "Related Articles" section at the bottom
    unlinked = [a for a in related if a.slug not in linked_slugs]
    all_related = [a for a in related if a.slug in linked_slugs] + unlinked

    if len(all_related) >= 2:
        related_section = "\n\n---\n\n### Related Articles\n\n"
        for article in all_related[:4]:
            related_section += f"- [{article.title}]({article.url})\n"
        modified += related_section

    return modified

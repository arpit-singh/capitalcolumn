"""SEO keyword research — free approach using Google Autocomplete + People Also Ask."""

import json
import re
from dataclasses import dataclass, field
from typing import Optional

import httpx
from rich.console import Console

console = Console()

AUTOCOMPLETE_URL = "https://suggestqueries.google.com/complete/search"
GOOGLE_SEARCH_URL = "https://www.google.com/search"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class SEOData:
    """Keyword research results for an article topic."""
    topic: str
    primary_keywords: list[str] = field(default_factory=list)
    secondary_keywords: list[str] = field(default_factory=list)
    people_also_ask: list[str] = field(default_factory=list)
    meta_description_suggestion: str = ""

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "primary_keywords": self.primary_keywords,
            "secondary_keywords": self.secondary_keywords,
            "people_also_ask": self.people_also_ask,
            "meta_description_suggestion": self.meta_description_suggestion,
        }


def _fetch_autocomplete(query: str, lang: str = "en", country: str = "in") -> list[str]:
    """Fetch Google Autocomplete suggestions for a query."""
    params = {
        "client": "firefox",
        "q": query,
        "hl": lang,
        "gl": country,
    }
    try:
        resp = httpx.get(
            AUTOCOMPLETE_URL,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and len(data) >= 2:
            return [s for s in data[1] if isinstance(s, str)]
    except Exception as e:
        console.print(f"  [yellow]Autocomplete error:[/yellow] {e}")
    return []


def _fetch_people_also_ask(query: str) -> list[str]:
    """Scrape 'People Also Ask' questions from Google search results."""
    try:
        resp = httpx.get(
            GOOGLE_SEARCH_URL,
            params={"q": query, "hl": "en", "gl": "in"},
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        resp.raise_for_status()
        html = resp.text

        # PAA questions are typically in data-q attributes or specific div patterns
        paa_questions = []

        # Pattern 1: data-q attribute
        matches = re.findall(r'data-q="([^"]+)"', html)
        paa_questions.extend(matches)

        # Pattern 2: aria-label on expandable sections
        matches = re.findall(r'aria-label="([^"]*\?)"', html)
        paa_questions.extend(matches)

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for q in paa_questions:
            q_lower = q.lower().strip()
            if q_lower not in seen and len(q) > 10:
                seen.add(q_lower)
                unique.append(q.strip())

        return unique[:6]
    except Exception as e:
        console.print(f"  [yellow]PAA scrape error:[/yellow] {e}")
    return []


def _extract_key_terms(text: str) -> list[str]:
    """Extract key noun phrases from a text string."""
    # Remove common stop words and extract meaningful terms
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "out", "off", "over",
        "under", "again", "further", "then", "once", "and", "but", "or",
        "nor", "not", "no", "so", "if", "than", "too", "very", "just",
        "about", "up", "its", "it", "this", "that", "these", "those",
        "what", "which", "who", "whom", "how", "when", "where", "why",
        "all", "each", "every", "both", "few", "more", "most", "other",
        "some", "such", "only", "own", "same", "new", "also", "says",
        "said", "according", "report", "reports", "news", "latest",
    }

    words = re.findall(r'[A-Za-z]+(?:\s+[A-Za-z]+)?', text.lower())
    terms = []
    for w in text.split():
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', w).strip().lower()
        if cleaned and cleaned not in stop_words and len(cleaned) > 2:
            terms.append(cleaned)
    return terms


def research_keywords(topic: str, summary: str = "") -> SEOData:
    """Run lightweight SEO research for a given topic.

    Workflow:
    1. Get Google Autocomplete suggestions for the topic
    2. Get variations with prefixes (what, how, why, best)
    3. Scrape People Also Ask questions
    4. Classify into primary (1-2) and secondary (3-5) keywords

    Args:
        topic: The news article topic/title.
        summary: Optional summary for additional context.

    Returns:
        SEOData with categorized keywords.
    """
    console.print(f"  [dim]Researching keywords for:[/dim] {topic[:60]}...")
    seo = SEOData(topic=topic)

    # 1. Base autocomplete
    base_suggestions = _fetch_autocomplete(topic)

    # 2. Prefix variations
    key_terms = _extract_key_terms(topic)
    core_phrase = " ".join(key_terms[:3]) if key_terms else topic

    prefix_suggestions = []
    for prefix in ["what is", "why", "how", f"{core_phrase} impact"]:
        results = _fetch_autocomplete(f"{prefix} {core_phrase}")
        prefix_suggestions.extend(results[:3])

    # 3. People Also Ask
    paa = _fetch_people_also_ask(topic)
    seo.people_also_ask = paa

    # 4. Classify keywords
    all_suggestions = base_suggestions + prefix_suggestions

    # Primary: the topic itself (cleaned) + most relevant suggestion
    primary = [topic.strip()]
    if base_suggestions:
        # Pick the suggestion closest to the original topic
        primary.append(base_suggestions[0])

    seo.primary_keywords = primary[:2]

    # Secondary: remaining autocomplete suggestions + PAA-derived terms
    secondary = []
    seen_lower = {p.lower() for p in primary}
    for s in all_suggestions:
        s_clean = s.strip()
        if s_clean.lower() not in seen_lower and len(s_clean) > 5:
            secondary.append(s_clean)
            seen_lower.add(s_clean.lower())
        if len(secondary) >= 5:
            break

    seo.secondary_keywords = secondary

    # 5. Generate meta description suggestion
    seo.meta_description_suggestion = (
        f"{topic}. "
        f"{''.join(summary[:120]) + '...' if summary else 'Read the latest analysis and insights.'}"
    )

    console.print(f"  [green]✓[/green] Found {len(seo.primary_keywords)} primary, "
                  f"{len(seo.secondary_keywords)} secondary keywords")
    return seo

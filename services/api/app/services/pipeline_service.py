"""Pipeline service — news monitoring, SEO research, image generation, article composition.

This is the server-side implementation of the pipeline, called from API endpoints.
Topics are stored in a JSON file for simplicity.
"""

import hashlib
import io
import json
import os
import re
import time
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

import feedparser
import httpx
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Configuration (from env vars)
# ---------------------------------------------------------------------------

DATA_DIR = Path(os.getenv("PIPELINE_DATA_DIR", "/app/pipeline_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

PENDING_FILE = DATA_DIR / "pending_topics.json"
SEEN_FILE = DATA_DIR / "seen_urls.json"
SOURCES_FILE = Path(os.getenv("PIPELINE_SOURCES_FILE", "/app/pipeline_data/sources.json"))
SITEMAP_CACHE_FILE = DATA_DIR / "sitemap_cache.json"

# API keys from env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

# Defaults
DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_IMAGE_MODEL = os.getenv("IMAGE_MODEL", "prunaai/z-image-turbo")
DEFAULT_WORD_COUNT = int(os.getenv("WORD_COUNT", "1200"))
TARGET_LOCATION = os.getenv("TARGET_LOCATION", "India")
PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL", "https://capitalcolumn.in")

# Available models
LLM_MODELS = {
    "openai": [
        {"id": "gpt-5.5", "name": "GPT-5.5"},
        {"id": "gpt-5.1", "name": "GPT-5.1"},
        {"id": "gpt-4o", "name": "GPT-4o"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini"},
        {"id": "o3", "name": "o3"},
        {"id": "gpt-4.1", "name": "GPT-4.1"},
        {"id": "gpt-4.1-mini", "name": "GPT-4.1 Mini"},
        {"id": "gpt-4.1-nano", "name": "GPT-4.1 Nano"},
    ],
    "gemini": [
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash"},
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro"},
        {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash"},
    ],
}

IMAGE_MODELS = [
    {"id": "prunaai/z-image-turbo", "name": "Z-Image Turbo (Fast)", "default": True},
    {"id": "bytedance/seedream-3", "name": "SeedReam 3 (ByteDance)"},
    {"id": "google/nano-banana-pro", "name": "Nano Banana Pro (Google)"},
]


# ---------------------------------------------------------------------------
# Topic Queue (JSON-based)
# ---------------------------------------------------------------------------

def _load_pending() -> list[dict]:
    if PENDING_FILE.exists():
        try:
            return json.loads(PENDING_FILE.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_pending(topics: list[dict]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps(topics, indent=2, default=str), "utf-8")


def _load_seen() -> set:
    if SEEN_FILE.exists():
        try:
            data = json.loads(SEEN_FILE.read_text("utf-8"))
            return set(data.get("hashes", []))
        except (json.JSONDecodeError, OSError):
            return set()
    return set()


def _save_seen(hashes: set):
    SEEN_FILE.write_text(json.dumps({
        "hashes": list(hashes),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }), "utf-8")


def _load_sources() -> dict:
    if SOURCES_FILE.exists():
        try:
            return json.loads(SOURCES_FILE.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"rss_feeds": [], "sitemaps": []}


def save_sources(sources: dict):
    SOURCES_FILE.parent.mkdir(parents=True, exist_ok=True)
    SOURCES_FILE.write_text(json.dumps(sources, indent=2), "utf-8")


# ---------------------------------------------------------------------------
# RSS Monitoring
# ---------------------------------------------------------------------------

class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
    def handle_data(self, d):
        self._parts.append(d)
    def get_text(self):
        return " ".join(self._parts)


def scan_rss_feeds(max_per_feed: int = 10) -> list[dict]:
    """Poll all RSS feeds and return new topics (with free SEO)."""
    sources = _load_sources()
    seen = _load_seen()
    new_topics = []

    for feed_cfg in sources.get("rss_feeds", []):
        name = feed_cfg.get("name", "Unknown")
        url = feed_cfg.get("url", "")
        category = feed_cfg.get("category", "markets")
        if not url:
            continue

        try:
            feed = feedparser.parse(url)
        except Exception:
            continue

        for entry in feed.entries[:max_per_feed]:
            link = getattr(entry, "link", "") or ""
            if not link:
                continue

            url_hash = hashlib.sha256(link.encode()).hexdigest()[:16]
            if url_hash in seen:
                continue

            title = getattr(entry, "title", "").strip()
            summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
            if "<" in summary:
                s = _HTMLStripper()
                s.feed(summary)
                summary = s.get_text()
            summary = summary[:500].strip()

            if not title:
                continue

            # Parse published date
            published_at = None
            for attr in ("published", "updated"):
                val = getattr(entry, attr, None)
                if val:
                    published_at = val
                    break

            # Free SEO research
            seo = _research_keywords(title, summary)

            topic = {
                "id": str(uuid.uuid4())[:8],
                "title": title,
                "url": link,
                "url_hash": url_hash,
                "summary": summary,
                "source_name": name,
                "category": category,
                "published_at": published_at,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "status": "pending",
                "seo": seo,
            }
            new_topics.append(topic)
            seen.add(url_hash)

    _save_seen(seen)

    # Add to pending queue
    if new_topics:
        pending = _load_pending()
        existing_hashes = {p.get("url_hash") for p in pending}
        for t in new_topics:
            if t["url_hash"] not in existing_hashes:
                pending.append(t)
        _save_pending(pending)

    return new_topics


def add_manual_topic(title: str, category: str = "markets", url: str = "") -> dict:
    """Manually add a topic to the queue with free SEO research."""
    url = url or f"manual://{title.lower().replace(' ', '-')[:50]}"
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]

    seo = _research_keywords(title)

    topic = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "url": url,
        "url_hash": url_hash,
        "summary": "Manually added topic.",
        "source_name": "Manual",
        "category": category,
        "published_at": None,
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
        "seo": seo,
    }

    pending = _load_pending()
    pending.append(topic)
    _save_pending(pending)
    return topic


# ---------------------------------------------------------------------------
# SEO Research (free)
# ---------------------------------------------------------------------------

AUTOCOMPLETE_URL = "https://suggestqueries.google.com/complete/search"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"


def _research_keywords(topic: str, summary: str = "") -> dict:
    """Free SEO research via Google Autocomplete."""
    try:
        resp = httpx.get(AUTOCOMPLETE_URL, params={
            "client": "firefox", "q": topic, "hl": "en", "gl": "in"
        }, headers={"User-Agent": UA}, timeout=8)
        data = resp.json()
        suggestions = data[1] if isinstance(data, list) and len(data) >= 2 else []
    except Exception:
        suggestions = []

    primary = [topic.strip()]
    if suggestions:
        primary.append(suggestions[0])

    secondary = []
    seen = {p.lower() for p in primary}
    for s in suggestions[1:]:
        if s.strip().lower() not in seen and len(s.strip()) > 5:
            secondary.append(s.strip())
            seen.add(s.strip().lower())
        if len(secondary) >= 5:
            break

    return {
        "primary_keywords": primary[:2],
        "secondary_keywords": secondary,
        "meta_description": f"{topic}. {summary[:120]}..." if summary else topic,
    }


# ---------------------------------------------------------------------------
# Topic Queue Operations
# ---------------------------------------------------------------------------

def get_topics(status: str = None) -> list[dict]:
    """Get topics, optionally filtered by status."""
    topics = _load_pending()
    if status:
        topics = [t for t in topics if t.get("status") == status]
    return topics


def get_topic_stats() -> dict:
    """Get counts by status."""
    topics = _load_pending()
    stats = {}
    for t in topics:
        s = t.get("status", "unknown")
        stats[s] = stats.get(s, 0) + 1
    stats["total"] = len(topics)
    return stats


def update_topic_status(topic_ids: list[str], new_status: str) -> int:
    """Update status of topics by ID. Returns count updated."""
    pending = _load_pending()
    count = 0
    id_set = set(topic_ids)
    for t in pending:
        if t.get("id") in id_set:
            t["status"] = new_status
            t["updated_at"] = datetime.now(timezone.utc).isoformat()
            count += 1
    _save_pending(pending)
    return count


def delete_topics(topic_ids: list[str]) -> int:
    """Delete topics by ID. Returns count deleted."""
    pending = _load_pending()
    id_set = set(topic_ids)
    remaining = [t for t in pending if t.get("id") not in id_set]
    deleted = len(pending) - len(remaining)
    _save_pending(remaining)
    return deleted


def clear_topics(status: str = None) -> int:
    """Clear topics, optionally only a specific status."""
    if status:
        pending = _load_pending()
        remaining = [t for t in pending if t.get("status") != status]
        cleared = len(pending) - len(remaining)
        _save_pending(remaining)
        return cleared
    else:
        pending = _load_pending()
        _save_pending([])
        return len(pending)


# ---------------------------------------------------------------------------
# Image Generation
# ---------------------------------------------------------------------------

CATEGORY_PROMPTS = {
    "markets": "Professional editorial photo of Indian stock market activity, digital screens, corporate atmosphere.",
    "earnings": "Professional editorial photo of corporate earnings reports, financial documents, modern office.",
    "technology": "Professional editorial photo of modern technology, futuristic workspace, AI visualization.",
    "banking": "Professional editorial photo of Indian banking, digital banking interface, modern finance.",
    "ipos": "Professional editorial photo of IPO listing, stock exchange, financial district.",
    "energy": "Professional editorial photo of energy sector, solar panels, wind turbines, power grid.",
    "healthcare": "Professional editorial photo of healthcare, laboratory, pharmaceutical research.",
}


def generate_article_image(
    topic: str,
    category: str = "markets",
    model_id: str = None,
) -> tuple[bytes, dict]:
    """Generate and compress an article image via Replicate.

    Returns (compressed_image_bytes, metadata_dict).
    """
    import replicate

    if not REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN not set")

    model = model_id or DEFAULT_IMAGE_MODEL
    base_prompt = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS.get("markets"))
    prompt = (
        f"{base_prompt} Visually related to: {topic[:100]}. "
        "Style: clean, modern, editorial, photojournalistic. High resolution. "
        "VERY IMPORTANT:No text overlays, no watermarks, no logos."
    )

    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    model_input = {"prompt": prompt, "width": 1200, "height": 800}
    if model == "prunaai/z-image-turbo":
        model_input["num_inference_steps"] = 4

    output = client.run(model, input=model_input)

    # Handle various Replicate output formats:
    # - FileOutput object (has .read() and .url)
    # - List of FileOutput/URLs
    # - Plain URL string
    # - Iterator/generator
    raw_bytes = None

    def _extract_bytes(item):
        """Get image bytes from a Replicate output item."""
        # FileOutput — read bytes directly
        if hasattr(item, 'read'):
            return item.read()
        # Has a URL attribute
        url = getattr(item, 'url', None) or str(item)
        if url.startswith('http'):
            r = httpx.get(url, timeout=30, follow_redirects=True)
            r.raise_for_status()
            return r.content
        return None

    if isinstance(output, bytes):
        raw_bytes = output
    elif isinstance(output, str) and output.startswith('http'):
        r = httpx.get(output, timeout=30, follow_redirects=True)
        r.raise_for_status()
        raw_bytes = r.content
    elif isinstance(output, list) and output:
        raw_bytes = _extract_bytes(output[0])
    elif hasattr(output, 'read'):
        raw_bytes = output.read()
    elif hasattr(output, '__iter__'):
        for item in output:
            raw_bytes = _extract_bytes(item)
            if raw_bytes:
                break

    if not raw_bytes:
        raise RuntimeError("Could not extract image from Replicate output")

    # Compress
    compressed, metadata = _compress_image(raw_bytes)

    # Add text overlay
    overlayed = _add_overlay(compressed, topic, category)

    return overlayed, metadata


def _compress_image(image_bytes: bytes) -> tuple[bytes, dict]:
    """Compress and resize image to WebP."""
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize
    ratio = min(1200 / img.size[0], 800 / img.size[1])
    if ratio < 1:
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=82, method=4)
    compressed = buf.getvalue()

    return compressed, {
        "original_kb": round(len(image_bytes) / 1024, 1),
        "compressed_kb": round(len(compressed) / 1024, 1),
        "width": img.size[0],
        "height": img.size[1],
    }


def _add_overlay(image_bytes: bytes, headline: str, category: str = "") -> bytes:
    """Add headline text overlay and CapitalColumn branding to the image."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    w, h = img.size

    # Gradient overlay at bottom
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for y in range(int(h * 0.55), h):
        progress = (y - int(h * 0.55)) / (h - int(h * 0.55))
        draw_ov.line([(0, y), (w, y)], fill=(0, 0, 0, int(180 * progress)))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # --- Load fonts ---
    font_large = font_small = font_logo = None

    # Try Source Serif 4 Bold (bundled) first
    SERIF_PATHS = [
        "/app/fonts/SourceSerif4-Bold.ttf",
        "fonts/SourceSerif4-Bold.ttf",
    ]
    SANS_PATHS = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]

    serif_font_path = None
    for fp in SERIF_PATHS:
        try:
            ImageFont.truetype(fp, 14)
            serif_font_path = fp
            break
        except (OSError, IOError):
            continue

    sans_font_path = None
    for fp in SANS_PATHS:
        try:
            ImageFont.truetype(fp, 14)
            sans_font_path = fp
            break
        except (OSError, IOError):
            continue

    # Headline + category use sans, logo uses serif
    active_sans = sans_font_path or serif_font_path
    active_serif = serif_font_path or sans_font_path

    if active_sans:
        font_large = ImageFont.truetype(active_sans, 32)
        font_small = ImageFont.truetype(active_sans, 16)
    else:
        font_large = font_small = ImageFont.load_default()

    if active_serif:
        font_logo = ImageFont.truetype(active_serif, 20)
    else:
        font_logo = ImageFont.load_default()

    # Category badge
    if category:
        cat_text = category.upper()
        cat_bbox = draw.textbbox((0, 0), cat_text, font=font_small)
        draw.rounded_rectangle(
            [24, int(h * 0.68), 36 + cat_bbox[2] - cat_bbox[0], int(h * 0.68) + cat_bbox[3] - cat_bbox[1] + 8],
            radius=3, fill=(99, 102, 241, 220))
        draw.text((30, int(h * 0.68) + 2), cat_text, fill=(255, 255, 255), font=font_small)

    # Headline
    words = headline.split()
    lines, current = [], []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font_large)
        if bbox[2] - bbox[0] <= w - 60:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    for i, line in enumerate(lines[:3]):
        y = int(h * 0.76) + i * 38
        draw.text((31, y + 1), line, fill=(0, 0, 0, 150), font=font_large)
        draw.text((30, y), line, fill=(255, 255, 255), font=font_large)

    # --- CapitalColumn branding (bottom-right) ---
    BRAND_WHITE = (255, 255, 255)
    BRAND_GREEN = (46, 184, 138)  # #2EB88A — accent green from dark theme

    capital_bbox = draw.textbbox((0, 0), "Capital", font=font_logo)
    column_bbox = draw.textbbox((0, 0), "Column", font=font_logo)
    capital_w = capital_bbox[2] - capital_bbox[0]
    column_w = column_bbox[2] - column_bbox[0]
    logo_total_w = capital_w + column_w + 2  # 2px kerning
    logo_h = max(capital_bbox[3] - capital_bbox[1], column_bbox[3] - column_bbox[1])

    # Semi-transparent dark pill behind logo
    pill_pad_x, pill_pad_y = 12, 6
    pill_x1 = w - logo_total_w - pill_pad_x * 2 - 16
    pill_y1 = h - logo_h - pill_pad_y * 2 - 14
    pill_x2 = w - 16
    pill_y2 = h - 14

    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill)
    pill_draw.rounded_rectangle(
        [pill_x1, pill_y1, pill_x2, pill_y2],
        radius=6, fill=(20, 20, 20, 160))
    img = Image.alpha_composite(img, pill)
    draw = ImageDraw.Draw(img)

    # Draw "Capital" in white, "Column" in green
    text_x = pill_x1 + pill_pad_x
    text_y = pill_y1 + pill_pad_y
    draw.text((text_x, text_y), "Capital", fill=BRAND_WHITE, font=font_logo)
    draw.text((text_x + capital_w + 2, text_y), "Column", fill=BRAND_GREEN, font=font_logo)

    final = img.convert("RGB")
    buf = io.BytesIO()
    final.save(buf, format="WEBP", quality=82)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Article Composition
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a senior human news blogger and journalist with years of experience at financial news agencies. You write with authority, nuance, and a distinctly human voice. You never sound like a generic AI blog."""


def compose_article(
    topic: str,
    summary: str = "",
    primary_keywords: list = None,
    secondary_keywords: list = None,
    source_url: str = "",
    word_count: int = None,
    provider: str = None,
    model: str = None,
) -> dict:
    """Generate article + metadata via LLM. Returns dict with all fields."""
    word_count = word_count or DEFAULT_WORD_COUNT
    primary_keywords = primary_keywords or [topic]
    secondary_keywords = secondary_keywords or []
    provider = provider or DEFAULT_LLM_PROVIDER
    model = model or (DEFAULT_OPENAI_MODEL if provider == "openai" else DEFAULT_GEMINI_MODEL)

    prompt = _build_article_prompt(topic, summary, primary_keywords, secondary_keywords, word_count, source_url)
    body = _call_llm(SYSTEM_PROMPT, prompt, provider, model)

    # Clean preamble
    lines = body.split("\n")
    clean = []
    started = False
    for line in lines:
        if not started and line.strip():
            if line.strip().startswith("#") or not any(
                p in line.lower() for p in ["here's", "sure!", "certainly", "of course", "i'll write", "below is"]
            ):
                started = True
        if started:
            clean.append(line)
    body = "\n".join(clean).strip()

    # Extract metadata
    meta_prompt = (
        f'Given this article about "{topic}", extract as JSON:\n'
        '"dek": subtitle (max 150 chars), "summary": 2-3 sentence preview (max 300 chars), '
        '"seo_title": SEO title (50-60 chars), "seo_description": meta description (120-155 chars), '
        f'"key_takeaways": array of 3-5 key points.\n\nArticle:\n{body[:3000]}\n\nReturn ONLY valid JSON.'
    )
    meta_raw = _call_llm("Return only valid JSON.", meta_prompt, provider, model)
    meta = _extract_json(meta_raw)

    return {
        "title": topic,
        "body_markdown": body,
        "dek": meta.get("dek", ""),
        "summary": meta.get("summary", ""),
        "seo_title": meta.get("seo_title", topic[:60]),
        "seo_description": meta.get("seo_description", ""),
        "meta_keywords": primary_keywords + secondary_keywords,
        "key_takeaways": meta.get("key_takeaways", []),
        "word_count": len(body.split()),
        "model_used": f"{provider}/{model}",
    }


def _build_article_prompt(topic, summary, primary, secondary, word_count, source_url):
    primary_str = ", ".join(primary) if primary else topic
    secondary_str = ", ".join(secondary) if secondary else ""
    return f"""Write a comprehensive, engaging news article of approximately {word_count} words about the topic provided.

**Topic:** {topic}
**Source context:** {summary}
{f"**Reference URL:** {source_url}" if source_url else ""}

Target location: {TARGET_LOCATION}

SEO requirements: 
- Use the primary keyword exactly as written, naturally, around 4–6 times total. Primary keywords are : {primary_str}
- Use the secondary keyword exactly as written, naturally, around 8–12 times total. Secondary keywords are : {secondary_str}
- Use the primary keyword in at least one heading or subheading.
- Use the secondary keyword in at least one heading or subheading.
- Do not force the keywords into every section.
- Avoid keyword stuffing. The article should still read like a real person wrote it for humans first.

Writing style requirements: Write like an experienced human journalist who has actually worked with news agencies. The tone should feel informed, conversational, and slightly opinionated, not like a neutral encyclopedia or generic SEO blog.
Very important:
- Do NOT write in a perfect “AI article” structure.
- Do NOT use phrases like: “in today’s digital landscape” “game-changer” “delve into” “unlock” “leverage” “seamless” “testament to” “in conclusion” “moreover” “furthermore” “the bottom line” “one thing is clear” “the best part?” “brands are realizing” “it’s no secret” "Let's be honest"
- Avoid neat claim-style sentences like: “Markets always rebound after a downturn.” “Investors trust gold more than equities.” “Rate cuts invariably boost stock prices.” Instead, make these ideas grounded and quoted from other authoritative financial news sources and cite them.
Human writing instructions:
- Use varied sentence lengths. Some sentences can be short. Some can be longer and slightly imperfect.
- Include a few small, natural imperfections, like a casual aside, a sentence fragment, or a slightly conversational phrase.
- Use specific examples from Indian and global finance market and other sectors.
- Add small observations that sound like they came from experience.
- Avoid broad statements unless they are followed by a concrete example.
- Do not make every paragraph the same length.
- Do not over-explain obvious ideas.
- Do not use rhetorical questions too often.
- Do not use too many polished transitions.
- Avoid symmetrical structures like “X, Y, and Z” repeatedly.
- Avoid motivational or dramatic language.
- Keep the news article useful, practical, and easy to read.

Structure: Markdown with H2/H3 headings. Editorial headings, not generic. Start with a specific observation, not a formulaic intro. No excessive bullet points.

Final quality check before writing:
- Remove any sentence that sounds like a LinkedIn marketing cliché.
- Replace generic claims with examples.
- Make sure no section sounds like it was copied from a generic agency blog.
- Make sure the article has a few uneven, human-feeling rhythms.
After you create the article, revise it to make it sound less polished and less template-like.
Focus on:
- Replacing broad claims with concrete examples.
- Removing slogan-like sentences.
- Making paragraph lengths more uneven.
- Reducing “SEO blog” tone.
- Adding 3–5 small, realistic observations from actual work.
- Keeping the keywords intact where possible, but do not make them feel forced.
- Do not make the writing messy for no reason. It should still sound professional, just more human.

Data tables and visual elements:
- If the article involves numerical data, comparisons, timelines, or financial metrics, include 1-2 markdown tables using GFM pipe syntax (| Header | Header |). Tables should be grounded in real data from the source context and must mention the source.
- Use blockquotes (> ) for important expert quotes or key analyst observations.
- Where appropriate, use a "key stat" callout by starting a line with "> **Key Stat:**" to highlight a standout data point.
- Tables should NOT be used for every article — only when they genuinely add value (e.g., earnings comparison, sector performance, timeline of events, before/after metrics).
- Keep tables concise (3-6 rows). Do not create tables with redundant data already covered in the prose.

Output ONLY the article in Markdown. No preamble."""


def _call_llm(system: str, user: str, provider: str, model: str) -> str:
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Newer models (gpt-5.1, o3, etc.) require max_completion_tokens
        # instead of the deprecated max_tokens parameter
        NEWER_MODELS = {'gpt-5.5', 'gpt-5.1', 'o3', 'o3-mini', 'o1', 'o1-mini', 'o1-preview'}
        use_new_param = any(model.startswith(m) for m in NEWER_MODELS)

        params = dict(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.8,
        )
        if use_new_param:
            params["max_completion_tokens"] = 4000
        else:
            params["max_tokens"] = 4000

        resp = client.chat.completions.create(**params)
        return resp.choices[0].message.content.strip()
    elif provider == "gemini":
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        resp = client.models.generate_content(model=model, contents=f"{system}\n\n{user}")
        return resp.text.strip()
    raise ValueError(f"Unknown provider: {provider}")


def _extract_json(text: str) -> dict:
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```\s*$', '', text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return {}


# ---------------------------------------------------------------------------
# Get available config for the UI
# ---------------------------------------------------------------------------

def get_pipeline_config() -> dict:
    """Return available models and configuration for the UI."""
    return {
        "llm_providers": [
            {"id": "openai", "name": "OpenAI", "models": LLM_MODELS["openai"],
             "configured": bool(OPENAI_API_KEY)},
            {"id": "gemini", "name": "Google Gemini", "models": LLM_MODELS["gemini"],
             "configured": bool(GEMINI_API_KEY)},
        ],
        "image_models": IMAGE_MODELS,
        "defaults": {
            "llm_provider": DEFAULT_LLM_PROVIDER,
            "llm_model": DEFAULT_OPENAI_MODEL if DEFAULT_LLM_PROVIDER == "openai" else DEFAULT_GEMINI_MODEL,
            "image_model": DEFAULT_IMAGE_MODEL,
            "word_count": DEFAULT_WORD_COUNT,
        },
        "sources": _load_sources(),
        "image_generation_configured": bool(REPLICATE_API_TOKEN),
    }

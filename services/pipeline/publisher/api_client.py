"""API client — publishes articles and images to the CapitalColumn API."""

import hashlib
import io
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

import httpx
from rich.console import Console

import config

console = Console()


@dataclass
class PublishResult:
    """Result of publishing an article."""
    article_id: str
    slug: str
    status: str
    preview_url: str = ""
    public_url: str = ""
    created: bool = True
    media_id: str = ""


def _headers() -> dict:
    """Build auth headers for the API."""
    return {"X-API-Key": config.API_KEY}


def upload_image(
    image_bytes: bytes,
    filename: str,
    alt_text: str = "",
    caption: str = "",
    credit: str = "AI Generated / CapitalColumn",
    content_type: str = "image/webp",
) -> dict:
    """Upload an image to the CapitalColumn media API.

    Args:
        image_bytes: The compressed image bytes.
        filename: SEO-friendly filename.
        alt_text: Image alt text for accessibility/SEO.
        caption: Image caption.
        credit: Image credit line.
        content_type: MIME type.

    Returns:
        Media asset response dict with id, public_url, etc.

    Raises:
        RuntimeError: If upload fails.
    """
    console.print(f"  [dim]Uploading image:[/dim] {filename} ({len(image_bytes) / 1024:.0f} KB)")

    files = {
        "file": (filename, io.BytesIO(image_bytes), content_type),
    }
    data = {
        "alt_text": alt_text,
        "caption": caption or "",
        "credit": credit,
    }

    try:
        resp = httpx.post(
            f"{config.API_BASE_URL}/internal/media/upload",
            headers=_headers(),
            files=files,
            data=data,
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()
        console.print(f"  [green]✓[/green] Image uploaded: {result.get('public_url', 'N/A')}")
        return result
    except httpx.HTTPStatusError as e:
        error_detail = e.response.json() if e.response.content else {}
        raise RuntimeError(f"Image upload failed ({e.response.status_code}): {error_detail}")
    except httpx.HTTPError as e:
        raise RuntimeError(f"Image upload failed: {e}")


def create_article(
    title: str,
    body_markdown: str,
    category: str,
    dek: str = "",
    summary: str = "",
    tags: list[str] = None,
    seo_title: str = "",
    seo_description: str = "",
    meta_keywords: list[str] = None,
    key_takeaways: list[str] = None,
    source_name: str = "",
    source_url: str = "",
    media_public_url: str = "",
    media_alt_text: str = "",
    media_caption: str = "",
    model_used: str = "",
    external_id: str = "",
    status: str = None,
) -> PublishResult:
    """Create an article via the CapitalColumn internal API.

    Builds the full ArticleCreatePayload matching the API schema.

    Args:
        title: Article title.
        body_markdown: Full article body in markdown.
        category: Category slug (e.g., "markets").
        ... (all fields map to ArticleCreatePayload)

    Returns:
        PublishResult with article ID, slug, status.
    """
    status = status or config.DEFAULT_STATUS

    # Build external_id for idempotency
    if not external_id:
        hash_input = f"{title}:{source_url}".encode()
        external_id = f"pipeline-{hashlib.sha256(hash_input).hexdigest()[:12]}"

    payload = {
        "external_id": external_id,
        "title": title,
        "body_markdown": body_markdown,
        "article_type": "news",
        "status": status,
        "category": category,
    }

    # Optional fields
    if dek:
        payload["dek"] = dek
    if summary:
        payload["summary"] = summary
    if tags:
        payload["tags"] = tags
    if key_takeaways:
        payload["key_takeaways"] = key_takeaways

    # Sources
    if source_url:
        payload["sources"] = [{
            "source_name": source_name or "News Source",
            "source_url": source_url,
            "source_type": "news_article",
            "is_primary_source": True,
        }]

    # Featured image (reference by URL if already uploaded)
    if media_public_url:
        payload["featured_image"] = {
            "source_url": media_public_url,
            "alt_text": media_alt_text or title,
            "caption": media_caption or "",
            "credit": "AI Generated / CapitalColumn",
        }

    # SEO
    seo = {}
    if seo_title:
        seo["seo_title"] = seo_title
    if seo_description:
        seo["seo_description"] = seo_description
    if meta_keywords:
        seo["meta_keywords"] = meta_keywords
    if seo:
        payload["seo"] = seo

    # AI metadata
    payload["ai_metadata"] = {
        "is_ai_generated": True,
        "is_editor_reviewed": False,
        "ai_pipeline_name": "capitalcolumn-pipeline",
        "ai_model_name": model_used or config.OPENAI_MODEL,
        "ai_pipeline_version": "1.0.0",
    }

    console.print(f"  [dim]Creating article:[/dim] {title[:60]}...")

    try:
        resp = httpx.post(
            f"{config.API_BASE_URL}/internal/articles",
            headers={**_headers(), "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()

        publish_result = PublishResult(
            article_id=result.get("id", ""),
            slug=result.get("slug", ""),
            status=result.get("status", status),
            preview_url=result.get("preview_url", ""),
            public_url=result.get("public_url", ""),
            created=result.get("created", True),
        )

        action = "Created" if publish_result.created else "Updated"
        console.print(f"  [green]✓[/green] {action}: {publish_result.slug} (status: {publish_result.status})")
        return publish_result

    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text[:500]
        raise RuntimeError(f"Article creation failed ({e.response.status_code}): {error_detail}")
    except httpx.HTTPError as e:
        raise RuntimeError(f"Article creation failed: {e}")


def publish_article(article_id: str) -> dict:
    """Publish a draft article (set status to published).

    Args:
        article_id: UUID of the article.

    Returns:
        Updated article response.
    """
    console.print(f"  [dim]Publishing article:[/dim] {article_id}")

    try:
        resp = httpx.post(
            f"{config.API_BASE_URL}/internal/articles/{article_id}/publish",
            headers=_headers(),
            timeout=15,
        )
        resp.raise_for_status()
        result = resp.json()
        console.print(f"  [green]✓[/green] Published: {result.get('slug', '')}")
        return result
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text[:500]
        raise RuntimeError(f"Publish failed ({e.response.status_code}): {error_detail}")


def test_connection() -> bool:
    """Test connectivity to the CapitalColumn API."""
    try:
        resp = httpx.get(f"{config.API_BASE_URL}/health", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            console.print(f"  [green]✓[/green] API connected: {data.get('app', 'OK')}")
            return True
    except Exception as e:
        console.print(f"  [red]✗[/red] API unreachable: {e}")
    return False

"""CapitalColumn AI Article Pipeline — CLI entry point.

Usage:
    python main.py scan           # Scan sources, collect topics (free, no cost)
    python main.py review         # Review pending topics, approve/reject (interactive)
    python main.py generate       # Generate articles for approved topics (costs $)
    python main.py topic "Title"  # Manually add a topic to the queue
    python main.py watch          # Continuous: scan every N minutes
    python main.py status         # Show pipeline status
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

# Ensure the pipeline directory is in the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from monitor.rss_monitor import NewsTopic, poll_rss_feeds
from monitor.sitemap_monitor import poll_sitemaps
from seo.keyword_research import research_keywords

console = Console()


# ---------------------------------------------------------------------------
# Pending Topics Queue (persisted to JSON)
# ---------------------------------------------------------------------------

def _load_pending() -> list[dict]:
    """Load the pending topics queue."""
    if config.PENDING_TOPICS_FILE.exists():
        try:
            return json.loads(config.PENDING_TOPICS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def _save_pending(topics: list[dict]) -> None:
    """Save the pending topics queue."""
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.PENDING_TOPICS_FILE.write_text(
        json.dumps(topics, indent=2, default=str), encoding="utf-8"
    )


def _add_to_pending(topic: NewsTopic, seo_data: dict = None) -> None:
    """Add a discovered topic to the pending queue."""
    pending = _load_pending()

    # Check for duplicates
    for p in pending:
        if p.get("url_hash") == topic.url_hash:
            return  # Already in queue

    entry = topic.to_dict()
    entry["status"] = "pending"  # pending | approved | rejected | completed
    entry["seo"] = seo_data or {}
    entry["added_at"] = datetime.now(timezone.utc).isoformat()

    pending.append(entry)
    _save_pending(pending)


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------

@click.group()
def cli():
    """CapitalColumn AI Article Pipeline"""
    console.print(Panel.fit(
        "[bold]CapitalColumn[/bold] AI Article Pipeline",
        border_style="blue",
    ))


@cli.command()
@click.option("--max-per-feed", default=10, help="Max entries to check per feed.")
def scan(max_per_feed: int):
    """Scan news sources and collect topics (free, no API costs)."""
    console.print("\n[bold blue]📡 Scanning news sources...[/bold blue]\n")

    # 1. Poll RSS feeds
    new_topics = poll_rss_feeds(max_per_feed=max_per_feed)

    # 2. Poll sitemaps
    sources_file = config.BASE_DIR / "monitor" / "sources.json"
    if sources_file.exists():
        sources = json.loads(sources_file.read_text(encoding="utf-8"))
        sitemap_topics = poll_sitemaps(sources)
        new_topics.extend(sitemap_topics)

    if not new_topics:
        console.print("[yellow]No new topics found.[/yellow]")
        return

    console.print(f"\n[green]Found {len(new_topics)} new topics:[/green]\n")

    # 3. Run free SEO research on each
    for topic in new_topics:
        console.print(f"  📰 [bold]{topic.title}[/bold]")
        console.print(f"     [dim]{topic.source_name} | {topic.category}[/dim]")

        # Free SEO research
        seo = research_keywords(topic.title, topic.summary)
        _add_to_pending(topic, seo.to_dict())

    pending = _load_pending()
    pending_count = sum(1 for p in pending if p.get("status") == "pending")
    console.print(f"\n[blue]📋 {pending_count} topics pending review.[/blue]")
    console.print("[dim]Run 'python main.py review' to approve topics for generation.[/dim]")


@cli.command()
def review():
    """Review pending topics — approve or reject (interactive)."""
    pending = _load_pending()
    pending_topics = [p for p in pending if p.get("status") == "pending"]

    if not pending_topics:
        console.print("[yellow]No pending topics to review.[/yellow]")
        return

    console.print(f"\n[bold blue]📋 {len(pending_topics)} topics pending review[/bold blue]\n")

    # Display all topics in a table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", width=4)
    table.add_column("Title", min_width=40)
    table.add_column("Source", width=20)
    table.add_column("Category", width=12)
    table.add_column("Keywords", width=30)

    for i, t in enumerate(pending_topics, 1):
        seo = t.get("seo", {})
        keywords = ", ".join(seo.get("primary_keywords", [])[:2])
        table.add_row(
            str(i),
            t.get("title", "")[:50],
            t.get("source_name", ""),
            t.get("category", ""),
            keywords[:30],
        )

    console.print(table)

    # Ask for selection
    console.print("\n[bold]Options:[/bold]")
    console.print("  • Enter numbers to approve (e.g., '1,3,5' or '1-5' or 'all')")
    console.print("  • Type 'reject N' to reject a topic")
    console.print("  • Type 'skip' to exit without changes\n")

    selection = Prompt.ask("Select topics to approve")

    if selection.lower() == "skip":
        return

    # Parse selection
    approved_indices = set()

    if selection.lower() == "all":
        approved_indices = set(range(len(pending_topics)))
    elif selection.lower().startswith("reject"):
        # Handle rejection
        try:
            reject_nums = selection.replace("reject", "").strip().split(",")
            for num in reject_nums:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(pending_topics):
                    pending_topics[idx]["status"] = "rejected"
                    console.print(f"  [red]✗[/red] Rejected: {pending_topics[idx]['title'][:50]}")
        except ValueError:
            console.print("[red]Invalid input.[/red]")
            return
    else:
        # Parse comma-separated and ranges
        parts = selection.replace(" ", "").split(",")
        for part in parts:
            if "-" in part:
                try:
                    start, end = part.split("-")
                    for i in range(int(start) - 1, int(end)):
                        approved_indices.add(i)
                except ValueError:
                    pass
            else:
                try:
                    approved_indices.add(int(part) - 1)
                except ValueError:
                    pass

    # Apply approvals
    for idx in approved_indices:
        if 0 <= idx < len(pending_topics):
            pending_topics[idx]["status"] = "approved"
            console.print(f"  [green]✓[/green] Approved: {pending_topics[idx]['title'][:50]}")

    # Update the full pending list
    pending_map = {p.get("url_hash"): p for p in pending_topics}
    for p in pending:
        url_hash = p.get("url_hash")
        if url_hash in pending_map:
            p["status"] = pending_map[url_hash]["status"]

    _save_pending(pending)

    approved_count = sum(1 for p in pending if p.get("status") == "approved")
    console.print(f"\n[blue]✓ {approved_count} topics approved for generation.[/blue]")
    console.print("[dim]Run 'python main.py generate' to create articles (will use paid APIs).[/dim]")


@cli.command()
@click.option("--provider", type=click.Choice(["openai", "gemini"]), default=None, help="LLM provider.")
@click.option("--model", default=None, help="LLM model name.")
@click.option("--image-model", default=None, help="Replicate image model.")
@click.option("--dry-run", is_flag=True, help="Generate but don't publish to API.")
@click.option("--no-image", is_flag=True, help="Skip image generation.")
def generate(provider: str, model: str, image_model: str, dry_run: bool, no_image: bool):
    """Generate articles for approved topics (uses paid APIs)."""
    from images.generator import generate_image
    from images.optimizer import compress_and_resize, generate_seo_filename, add_text_overlay
    from composer.article_writer import compose_article
    from interlinking.sitemap_linker import inject_internal_links
    from publisher.api_client import create_article, upload_image, publish_article, test_connection

    pending = _load_pending()
    approved = [p for p in pending if p.get("status") == "approved"]

    if not approved:
        console.print("[yellow]No approved topics. Run 'python main.py review' first.[/yellow]")
        return

    # Limit per run
    batch = approved[:config.MAX_ARTICLES_PER_RUN]
    console.print(f"\n[bold blue]🚀 Generating {len(batch)} articles[/bold blue]")

    if not dry_run:
        console.print("\n[dim]Testing API connection...[/dim]")
        if not test_connection():
            console.print("[red]Cannot reach CapitalColumn API. Aborting.[/red]")
            return

    # Cost estimate
    estimated_cost = len(batch) * 0.05  # ~$0.05 per article (LLM + image)
    console.print(f"[yellow]Estimated cost: ~${estimated_cost:.2f}[/yellow]")
    if not Confirm.ask("Proceed?"):
        return

    results = []
    for i, topic_data in enumerate(batch, 1):
        title = topic_data.get("title", "Untitled")
        console.print(f"\n{'='*60}")
        console.print(f"[bold]Article {i}/{len(batch)}: {title[:60]}[/bold]")
        console.print(f"{'='*60}")

        try:
            seo = topic_data.get("seo", {})
            primary = seo.get("primary_keywords", [title])
            secondary = seo.get("secondary_keywords", [])
            category = topic_data.get("category", "markets")

            # Step 1: Generate image (paid)
            media_url = ""
            if not no_image:
                console.print("\n[bold]Step 1: Image Generation[/bold]")
                raw_image = generate_image(title, category, model_id=image_model)
                compressed, img_meta = compress_and_resize(raw_image)

                # Add text overlay
                overlayed = add_text_overlay(compressed, title, category)

                if not dry_run:
                    slug_guess = title.lower().replace(" ", "-")[:60]
                    filename = generate_seo_filename(slug_guess, img_meta.get("extension", ".webp"))
                    media_result = upload_image(
                        overlayed,
                        filename=filename,
                        alt_text=title,
                        caption=seo.get("meta_description_suggestion", ""),
                    )
                    media_url = media_result.get("public_url", "")
            else:
                console.print("\n[dim]Skipping image generation.[/dim]")

            # Step 2: Compose article (paid)
            console.print("\n[bold]Step 2: Article Composition[/bold]")
            article = compose_article(
                topic=title,
                summary=topic_data.get("summary", ""),
                primary_keywords=primary,
                secondary_keywords=secondary,
                source_url=topic_data.get("url", ""),
                provider=provider,
                model=model,
            )

            # Step 3: Internal linking (free)
            console.print("\n[bold]Step 3: Internal Linking[/bold]")
            linked_body = inject_internal_links(
                article.body_markdown,
                title=title,
            )
            article.body_markdown = linked_body

            # Step 4: Publish (free)
            if not dry_run:
                console.print("\n[bold]Step 4: Publishing[/bold]")
                result = create_article(
                    title=article.title,
                    body_markdown=article.body_markdown,
                    category=category,
                    dek=article.dek,
                    summary=article.summary,
                    tags=secondary[:5],  # Use secondary keywords as tags
                    seo_title=article.seo_title,
                    seo_description=article.seo_description,
                    meta_keywords=article.meta_keywords,
                    key_takeaways=article.key_takeaways,
                    source_name=topic_data.get("source_name", ""),
                    source_url=topic_data.get("url", ""),
                    media_public_url=media_url,
                    media_alt_text=title,
                    model_used=article.model_used,
                )
                results.append(result)

                # Auto-publish if configured
                if config.AUTO_PUBLISH and result.article_id:
                    publish_article(result.article_id)
            else:
                console.print(f"\n[yellow]DRY RUN — article not published[/yellow]")
                console.print(f"  Title: {article.title}")
                console.print(f"  Words: {article.word_count}")
                console.print(f"  SEO Title: {article.seo_title}")

            # Mark as completed
            topic_data["status"] = "completed"
            topic_data["completed_at"] = datetime.now(timezone.utc).isoformat()

        except Exception as e:
            console.print(f"\n[red]Error processing '{title[:40]}':[/red] {e}")
            topic_data["status"] = "error"
            topic_data["error"] = str(e)

    _save_pending(pending)

    # Summary
    console.print(f"\n{'='*60}")
    console.print(f"[bold green]✓ Generation complete![/bold green]")
    console.print(f"  Processed: {len(batch)}")
    console.print(f"  Published: {len(results)}")
    if results:
        console.print(f"\n  [dim]Articles created:[/dim]")
        for r in results:
            console.print(f"    • {r.slug} ({r.status})")


@cli.command()
@click.argument("title")
@click.option("--category", default="markets", help="Article category slug.")
@click.option("--url", default="", help="Source URL for reference.")
def topic(title: str, category: str, url: str):
    """Manually add a topic to the pending queue."""
    console.print(f"\n[bold]Adding topic:[/bold] {title}")

    topic_obj = NewsTopic(
        title=title,
        url=url or f"manual://{title.lower().replace(' ', '-')}",
        summary="Manually added topic.",
        source_name="Manual",
        category=category,
    )

    # Run free SEO research
    seo = research_keywords(title)
    _add_to_pending(topic_obj, seo.to_dict())

    console.print(f"[green]✓[/green] Topic added to queue.")
    console.print(f"  Primary keywords: {', '.join(seo.primary_keywords)}")
    console.print(f"  Secondary keywords: {', '.join(seo.secondary_keywords)}")
    console.print(f"\n[dim]Run 'python main.py review' to approve, then 'python main.py generate'.[/dim]")


@cli.command()
@click.option("--interval", default=None, type=int, help="Check interval in minutes.")
def watch(interval: int):
    """Continuous monitoring — scan sources every N minutes."""
    interval = interval or config.CHECK_INTERVAL_MINUTES

    console.print(f"\n[bold blue]👁  Watch mode — scanning every {interval} minutes[/bold blue]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]\n")

    try:
        while True:
            console.print(f"[dim]--- Scan at {datetime.now().strftime('%H:%M:%S')} ---[/dim]")

            new_topics = poll_rss_feeds()
            if new_topics:
                for t in new_topics:
                    seo = research_keywords(t.title, t.summary)
                    _add_to_pending(t, seo.to_dict())
                console.print(f"[green]Found {len(new_topics)} new topics.[/green]")
            else:
                console.print("[dim]No new topics.[/dim]")

            pending = _load_pending()
            pending_count = sum(1 for p in pending if p.get("status") == "pending")
            if pending_count:
                console.print(f"[yellow]{pending_count} topics awaiting review.[/yellow]")

            console.print(f"[dim]Next scan in {interval} minutes...[/dim]\n")
            time.sleep(interval * 60)
    except KeyboardInterrupt:
        console.print("\n[yellow]Watch mode stopped.[/yellow]")


@cli.command()
def status():
    """Show pipeline status — pending, approved, completed topics."""
    pending = _load_pending()

    status_counts = {}
    for p in pending:
        s = p.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    console.print("\n[bold blue]📊 Pipeline Status[/bold blue]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Status", width=15)
    table.add_column("Count", width=10, justify="right")

    colors = {"pending": "yellow", "approved": "blue", "completed": "green",
              "rejected": "red", "error": "red"}
    for s, count in sorted(status_counts.items()):
        color = colors.get(s, "white")
        table.add_row(f"[{color}]{s}[/{color}]", str(count))

    table.add_row("[bold]Total[/bold]", f"[bold]{len(pending)}[/bold]")
    console.print(table)

    # Show recent errors
    errors = [p for p in pending if p.get("status") == "error"]
    if errors:
        console.print(f"\n[red]Recent errors:[/red]")
        for e in errors[-3:]:
            console.print(f"  • {e.get('title', '')[:50]}: {e.get('error', 'Unknown')}")

    # Config info
    console.print(f"\n[dim]LLM: {config.LLM_PROVIDER}/{config.OPENAI_MODEL if config.LLM_PROVIDER == 'openai' else config.GEMINI_MODEL}[/dim]")
    console.print(f"[dim]Image: {config.IMAGE_MODEL}[/dim]")
    console.print(f"[dim]Default status: {config.DEFAULT_STATUS}[/dim]")


@cli.command()
def clear():
    """Clear all pending topics (reset the queue)."""
    if Confirm.ask("Clear ALL pending topics? This cannot be undone"):
        _save_pending([])
        console.print("[green]✓ Queue cleared.[/green]")


if __name__ == "__main__":
    cli()

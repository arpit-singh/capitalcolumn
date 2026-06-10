"""Article writer — generates articles using OpenAI or Gemini with your editorial prompt."""

import json
import re
from dataclasses import dataclass, field
from typing import Optional

from rich.console import Console

import config

console = Console()


@dataclass
class ComposedArticle:
    """A fully composed article ready for publishing."""
    title: str
    body_markdown: str
    dek: str = ""
    summary: str = ""
    seo_title: str = ""
    seo_description: str = ""
    meta_keywords: list[str] = field(default_factory=list)
    key_takeaways: list[str] = field(default_factory=list)
    word_count: int = 0
    model_used: str = ""


# ---------------------------------------------------------------------------
# The editorial prompt template — exactly as specified by the user
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a senior human news blogger and journalist with years of experience at financial news agencies. You write with authority, nuance, and a distinctly human voice. You never sound like a generic AI blog."""


def _build_article_prompt(
    topic: str,
    summary: str,
    primary_keywords: list[str],
    secondary_keywords: list[str],
    word_count: int,
    source_url: str = "",
) -> str:
    """Build the full article generation prompt from user's template."""

    primary_str = ", ".join(primary_keywords) if primary_keywords else topic
    secondary_str = ", ".join(secondary_keywords) if secondary_keywords else ""

    return f"""Write a comprehensive, engaging article of approximately {word_count} words about the following topic:

**Topic:** {topic}
**Source context:** {summary}
{f"**Reference URL:** {source_url}" if source_url else ""}

If applicable to the content, make sure to consider the target location: {config.TARGET_LOCATION}

SEO requirements:
- Use the primary keyword exactly as written, naturally, around 4–6 times total. Primary keywords are: {primary_str}
- Use the secondary keyword exactly as written, naturally, around 8–12 times total. Secondary keywords are: {secondary_str}
- Use the primary keyword in at least one heading or subheading.
- Use the secondary keyword in at least one heading or subheading.
- Do not force the keywords into every section.
- Avoid keyword stuffing. The article should still read like a real person wrote it for humans first.

Writing style requirements: Write like an experienced human journalist who has actually worked with news agencies. The tone should feel informed, conversational, and slightly opinionated, not like a neutral encyclopedia or generic SEO blog.

Very important:
- Do NOT write in a perfect "AI article" structure.
- Do NOT use phrases like: "in today's digital landscape" "game-changer" "delve into" "unlock" "leverage" "seamless" "testament to" "in conclusion" "moreover" "furthermore" "the bottom line" "one thing is clear" "the best part?" "brands are realizing" "it's no secret"
- Avoid neat claim-style sentences like: "TikTok has changed how people discover products." "People trust people more than brands." "Paid TikTok ads work better when organic comes first." Instead, make these ideas sound more grounded, specific, and less slogan-like.

Human writing instructions:
- Use varied sentence lengths. Some sentences can be short. Some can be longer and slightly imperfect.
- Include a few small, natural imperfections, like a casual aside, a sentence fragment, or a slightly conversational phrase.
- Use specific examples from Indian market contexts: large-caps, mid-caps, IPOs, banking, IT sector, pharma, FMCG, auto, energy, infrastructure, etc.
- Add small observations that sound like they came from experience, such as: a company's management commentary that didn't match the numbers, a sector rotation nobody saw coming, retail investors piling in after the run-up was already done, a quarterly result that looked good on paper but had margin compression underneath.
- Avoid broad statements unless they are followed by a concrete example.
- Do not make every paragraph the same length.
- Do not over-explain obvious ideas.
- Do not use rhetorical questions too often.
- Do not use too many polished transitions.
- Avoid symmetrical structures like "X, Y, and Z" repeatedly.
- Avoid motivational or dramatic language.
- Keep the article useful, practical, and easy to read.

Structure:
- Use Markdown.
- Use H2 and H3 headings, but make the headings sound editorial, not generic.
- Do not use too many bullet points.
- Avoid a formulaic intro. Start with a specific scene, observation, or tension.
- The article should feel like a column written by someone who watches markets daily, not like a corporate guide.

Final quality check before writing:
- Remove any sentence that sounds like a LinkedIn marketing cliché.
- Replace generic claims with examples.
- Make sure no section sounds like it was copied from a generic agency blog.
- Make sure the article has a few uneven, human-feeling rhythms.

After you create the article, revise it to make it sound less polished and less template-like.
Focus on:
- Replacing broad marketing claims with concrete examples.
- Removing slogan-like sentences.
- Making paragraph lengths more uneven.
- Reducing "SEO blog" tone.
- Adding 3–5 small, realistic observations from actual work.
- Keeping the keywords intact where possible, but do not make them feel forced.
- Do not make the writing messy for no reason. It should still sound professional, just more human.

Output ONLY the article in Markdown format. Do not include any preamble like "Here's the article" or "Sure!". Start directly with the first heading or paragraph."""


def _build_metadata_prompt(article_body: str, topic: str) -> str:
    """Build a prompt to extract SEO metadata from the article."""
    return f"""Given this article about "{topic}", extract the following as a JSON object:

1. "dek": A compelling 1-sentence subtitle/deck (max 150 chars)
2. "summary": A 2-3 sentence summary for previews (max 300 chars)
3. "seo_title": An SEO-optimized title (50-60 chars, include primary keyword)
4. "seo_description": A meta description for search engines (120-155 chars)
5. "key_takeaways": An array of 3-5 key bullet points from the article (each max 100 chars)

Article:
{article_body[:3000]}

Return ONLY valid JSON, no markdown formatting."""


def _call_openai(system: str, user: str, model: str = None) -> str:
    """Call OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    model = model or config.OPENAI_MODEL

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.8,
        max_tokens=4000,
    )
    return response.choices[0].message.content.strip()


def _call_gemini(system: str, user: str, model: str = None) -> str:
    """Call Google Gemini API."""
    from google import genai

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    model = model or config.GEMINI_MODEL

    response = client.models.generate_content(
        model=model,
        contents=f"{system}\n\n{user}",
    )
    return response.text.strip()


def _call_llm(system: str, user: str, provider: str = None, model: str = None) -> str:
    """Route to the configured LLM provider."""
    provider = provider or config.LLM_PROVIDER

    if provider == "openai":
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")
        return _call_openai(system, user, model)
    elif provider == "gemini":
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")
        return _call_gemini(system, user, model)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM output, handling markdown code blocks."""
    # Strip markdown code blocks
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```\s*$', '', text, flags=re.MULTILINE)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON in the response
        match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return {}


def compose_article(
    topic: str,
    summary: str = "",
    primary_keywords: list[str] = None,
    secondary_keywords: list[str] = None,
    source_url: str = "",
    word_count: int = None,
    provider: str = None,
    model: str = None,
) -> ComposedArticle:
    """Generate a complete article with metadata.

    Args:
        topic: The news topic/title.
        summary: Source article summary for context.
        primary_keywords: SEO primary keywords.
        secondary_keywords: SEO secondary keywords.
        source_url: Original source URL for reference.
        word_count: Target word count.
        provider: LLM provider override ("openai" or "gemini").
        model: Model name override.

    Returns:
        ComposedArticle with body, SEO fields, and metadata.
    """
    word_count = word_count or config.DEFAULT_WORD_COUNT
    primary_keywords = primary_keywords or [topic]
    secondary_keywords = secondary_keywords or []
    provider = provider or config.LLM_PROVIDER
    model_name = model or (config.OPENAI_MODEL if provider == "openai" else config.GEMINI_MODEL)

    console.print(f"  [dim]Writing article with:[/dim] {provider}/{model_name}")

    # Step 1: Generate the article body
    article_prompt = _build_article_prompt(
        topic=topic,
        summary=summary,
        primary_keywords=primary_keywords,
        secondary_keywords=secondary_keywords,
        word_count=word_count,
        source_url=source_url,
    )

    body = _call_llm(SYSTEM_PROMPT, article_prompt, provider, model)

    # Clean up any AI preamble
    lines = body.split("\n")
    clean_lines = []
    started = False
    for line in lines:
        if not started:
            # Skip preamble lines
            if line.strip().startswith("#") or line.strip().startswith("**") or (line.strip() and not any(
                phrase in line.lower() for phrase in [
                    "here's", "sure!", "certainly", "of course", "i'll write", "below is",
                ]
            )):
                started = True
        if started:
            clean_lines.append(line)

    body = "\n".join(clean_lines).strip()
    actual_word_count = len(body.split())

    console.print(f"  [green]✓[/green] Article generated ({actual_word_count} words)")

    # Step 2: Extract metadata
    console.print(f"  [dim]Extracting SEO metadata...[/dim]")
    meta_prompt = _build_metadata_prompt(body, topic)
    meta_raw = _call_llm(
        "You are an SEO specialist. Return only valid JSON.",
        meta_prompt,
        provider,
        model,
    )
    meta = _extract_json(meta_raw)

    result = ComposedArticle(
        title=topic,
        body_markdown=body,
        dek=meta.get("dek", ""),
        summary=meta.get("summary", ""),
        seo_title=meta.get("seo_title", topic[:60]),
        seo_description=meta.get("seo_description", ""),
        meta_keywords=primary_keywords + secondary_keywords,
        key_takeaways=meta.get("key_takeaways", []),
        word_count=actual_word_count,
        model_used=f"{provider}/{model_name}",
    )

    console.print(f"  [green]✓[/green] Metadata extracted")
    return result

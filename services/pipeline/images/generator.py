"""Image generator — creates article hero images via Replicate API.

Generates clean editorial images WITHOUT baked-in text.
Text overlays (headline, logo) should be added separately via Pillow or CSS.
"""

import io
from typing import Optional

import httpx
import replicate
from rich.console import Console

import config

console = Console()


# Image prompt templates for different article categories
CATEGORY_PROMPTS = {
    "markets": (
        "Professional editorial photograph of Indian stock market activity. "
        "Modern trading floor, digital screens showing stock charts, "
        "clean corporate atmosphere. No text, no logos, no watermarks."
    ),
    "earnings": (
        "Professional editorial photograph of corporate earnings report concept. "
        "Clean desk with financial documents, laptop showing charts, "
        "modern office setting. No text, no logos, no watermarks."
    ),
    "technology": (
        "Professional editorial photograph of modern technology concept. "
        "Clean, futuristic tech workspace, circuit boards, server racks, or AI visualization. "
        "No text, no logos, no watermarks."
    ),
    "banking": (
        "Professional editorial photograph of Indian banking and finance. "
        "Modern bank building, digital banking interface, RBI headquarters concept. "
        "No text, no logos, no watermarks."
    ),
    "ipos": (
        "Professional editorial photograph of IPO listing concept. "
        "Stock exchange bell ceremony, new company listing celebration, "
        "modern financial district. No text, no logos, no watermarks."
    ),
    "energy": (
        "Professional editorial photograph of energy sector. "
        "Solar panels, wind turbines, oil refinery, or power grid infrastructure. "
        "Clean industrial photography. No text, no logos, no watermarks."
    ),
    "healthcare": (
        "Professional editorial photograph of healthcare and pharma industry. "
        "Modern laboratory, medical research, pharmaceutical manufacturing. "
        "No text, no logos, no watermarks."
    ),
    "default": (
        "Professional editorial photograph for a financial news article. "
        "Clean, modern, corporate atmosphere. Photojournalistic style. "
        "No text, no logos, no watermarks."
    ),
}


def _build_prompt(topic: str, category: str = "default") -> str:
    """Build the image generation prompt from topic and category."""
    base = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["default"])
    return (
        f"{base} "
        f"The image should visually relate to: {topic[:100]}. "
        f"Style: clean, modern, editorial, photojournalistic. "
        f"High resolution, sharp focus, professional lighting. "
        f"Absolutely no text overlays, no watermarks, no logos."
    )


def _get_model_input(model_id: str, prompt: str) -> dict:
    """Build the model-specific input parameters."""
    if model_id == "prunaai/z-image-turbo":
        return {
            "prompt": prompt,
            "width": 1200,
            "height": 800,
            "num_inference_steps": 4,
        }
    elif model_id == "bytedance/seedream-3":
        return {
            "prompt": prompt,
            "width": 1200,
            "height": 800,
            "num_outputs": 1,
        }
    elif model_id == "google/nano-banana-pro":
        return {
            "prompt": prompt,
            "width": 1200,
            "height": 800,
        }
    else:
        # Generic fallback
        return {
            "prompt": prompt,
            "width": 1200,
            "height": 800,
        }


def generate_image(
    topic: str,
    category: str = "default",
    model_id: Optional[str] = None,
) -> bytes:
    """Generate an article hero image using Replicate.

    Args:
        topic: The article topic/title for prompt context.
        category: Article category for prompt template selection.
        model_id: Replicate model ID. Defaults to config.IMAGE_MODEL.

    Returns:
        Raw image bytes (PNG/JPEG from the model).

    Raises:
        ValueError: If Replicate token is not configured.
        RuntimeError: If image generation fails.
    """
    if not config.REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN is not set. Add it to your .env file.")

    model = model_id or config.IMAGE_MODEL
    model_info = config.IMAGE_MODELS.get(model, {"name": model})
    prompt = _build_prompt(topic, category)

    console.print(f"  [dim]Generating image with:[/dim] {model_info.get('name', model)}")
    console.print(f"  [dim]Prompt:[/dim] {prompt[:80]}...")

    try:
        client = replicate.Client(api_token=config.REPLICATE_API_TOKEN)
        model_input = _get_model_input(model, prompt)

        output = client.run(model, input=model_input)

        # Output can be a URL string, a list of URLs, or a FileOutput
        image_url = None
        if isinstance(output, list):
            image_url = str(output[0]) if output else None
        elif isinstance(output, str):
            image_url = output
        elif hasattr(output, "url"):
            image_url = output.url
        elif hasattr(output, "__iter__"):
            for item in output:
                image_url = str(item)
                break

        if not image_url:
            raise RuntimeError(f"No image URL returned from {model}")

        # Download the generated image
        console.print(f"  [dim]Downloading generated image...[/dim]")
        resp = httpx.get(image_url, timeout=30, follow_redirects=True)
        resp.raise_for_status()

        image_bytes = resp.content
        console.print(f"  [green]✓[/green] Image generated ({len(image_bytes) / 1024:.0f} KB)")
        return image_bytes

    except replicate.exceptions.ReplicateError as e:
        raise RuntimeError(f"Replicate API error: {e}")
    except httpx.HTTPError as e:
        raise RuntimeError(f"Failed to download generated image: {e}")


def list_available_models() -> dict:
    """Return the available image generation models."""
    return config.IMAGE_MODELS

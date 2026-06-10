"""Image optimizer — compress, resize, and add metadata to generated images."""

import io
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

import config

console = Console()


def compress_and_resize(
    image_bytes: bytes,
    max_width: int = None,
    max_height: int = None,
    quality: int = None,
    output_format: str = "WEBP",
) -> tuple[bytes, dict]:
    """Compress and resize an image while preserving aspect ratio.

    Args:
        image_bytes: Raw image bytes.
        max_width: Maximum width (default from config).
        max_height: Maximum height (default from config).
        quality: Compression quality 0-100 (default from config).
        output_format: Output format — WEBP, JPEG, or PNG.

    Returns:
        Tuple of (compressed bytes, metadata dict).
    """
    max_width = max_width or config.IMAGE_MAX_WIDTH
    max_height = max_height or config.IMAGE_MAX_HEIGHT
    quality = quality or config.IMAGE_QUALITY

    original_size = len(image_bytes)
    img = Image.open(io.BytesIO(image_bytes))

    # Convert to RGB if needed (RGBA/P modes don't work with JPEG/WEBP)
    if img.mode in ("RGBA", "P", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize maintaining aspect ratio
    orig_w, orig_h = img.size
    ratio = min(max_width / orig_w, max_height / orig_h)
    if ratio < 1:
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # Compress
    buffer = io.BytesIO()
    if output_format.upper() == "WEBP":
        img.save(buffer, format="WEBP", quality=quality, method=4)
        mime_type = "image/webp"
        ext = ".webp"
    elif output_format.upper() == "JPEG":
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        mime_type = "image/jpeg"
        ext = ".jpg"
    else:
        img.save(buffer, format="PNG", optimize=True)
        mime_type = "image/png"
        ext = ".png"

    compressed = buffer.getvalue()
    compressed_size = len(compressed)
    savings = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0

    metadata = {
        "original_size_kb": round(original_size / 1024, 1),
        "compressed_size_kb": round(compressed_size / 1024, 1),
        "savings_percent": round(savings, 1),
        "width": img.size[0],
        "height": img.size[1],
        "format": output_format.lower(),
        "mime_type": mime_type,
        "extension": ext,
    }

    console.print(
        f"  [green]✓[/green] Compressed: {metadata['original_size_kb']}KB → "
        f"{metadata['compressed_size_kb']}KB ({metadata['savings_percent']}% saved)"
    )
    return compressed, metadata


def generate_seo_filename(slug: str, ext: str = ".webp") -> str:
    """Generate an SEO-friendly filename from article slug.

    Args:
        slug: Article slug (e.g., 'sensex-rallies-500-points').
        ext: File extension.

    Returns:
        Filename like 'sensex-rallies-500-points-hero.webp'
    """
    # Clean the slug
    clean = slug.strip().lower().replace(" ", "-")
    # Truncate if too long
    if len(clean) > 60:
        clean = clean[:60].rsplit("-", 1)[0]
    return f"{clean}-hero{ext}"


def add_text_overlay(
    image_bytes: bytes,
    headline: str,
    category_label: Optional[str] = None,
    logo_text: str = "CapitalColumn",
) -> bytes:
    """Add headline text and category label overlay to an image using Pillow.

    This creates a professional news-style overlay at the bottom of the image
    with a semi-transparent gradient background.

    Args:
        image_bytes: Compressed image bytes.
        headline: Article headline to overlay.
        category_label: Optional category tag (e.g., "MARKETS").
        logo_text: Site name for corner branding.

    Returns:
        Image bytes with text overlay applied.
    """
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Create gradient overlay at bottom (semi-transparent black)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Draw gradient from transparent to semi-opaque black (bottom 40%)
    gradient_start = int(h * 0.55)
    for y in range(gradient_start, h):
        progress = (y - gradient_start) / (h - gradient_start)
        alpha = int(180 * progress)
        overlay_draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Try to load a good font, fall back to default
    font_large = None
    font_small = None
    font_logo = None

    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]

    for fp in font_paths:
        try:
            font_large = ImageFont.truetype(fp, size=32)
            font_small = ImageFont.truetype(fp, size=16)
            font_logo = ImageFont.truetype(fp, size=14)
            break
        except (OSError, IOError):
            continue

    if font_large is None:
        font_large = ImageFont.load_default()
        font_small = font_large
        font_logo = font_large

    # Category label (top-left of overlay area)
    if category_label:
        cat_y = int(h * 0.68)
        cat_text = category_label.upper()
        # Draw category badge
        cat_bbox = draw.textbbox((0, 0), cat_text, font=font_small)
        cat_w = cat_bbox[2] - cat_bbox[0]
        cat_h = cat_bbox[3] - cat_bbox[1]
        badge_x = 30
        badge_y = cat_y
        draw.rounded_rectangle(
            [badge_x - 6, badge_y - 4, badge_x + cat_w + 6, badge_y + cat_h + 4],
            radius=3,
            fill=(99, 102, 241, 220),  # Indigo
        )
        draw.text((badge_x, badge_y), cat_text, fill=(255, 255, 255), font=font_small)

    # Headline text (bottom area, with word wrap)
    headline_y = int(h * 0.76)
    max_text_width = w - 60  # 30px padding each side

    # Simple word wrap
    words = headline.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_large)
        if bbox[2] - bbox[0] <= max_text_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    # Limit to 3 lines
    lines = lines[:3]
    if len(lines) == 3 and len(headline.split()) > len(" ".join(lines).split()):
        lines[2] = lines[2][:50].rsplit(" ", 1)[0] + "..."

    for i, line in enumerate(lines):
        y = headline_y + i * 38
        # Text shadow
        draw.text((31, y + 1), line, fill=(0, 0, 0, 150), font=font_large)
        # Main text
        draw.text((30, y), line, fill=(255, 255, 255), font=font_large)

    # Logo text (bottom-right corner)
    logo_bbox = draw.textbbox((0, 0), logo_text, font=font_logo)
    logo_w = logo_bbox[2] - logo_bbox[0]
    draw.text((w - logo_w - 20, h - 30), logo_text, fill=(255, 255, 255, 180), font=font_logo)

    # Convert back to RGB for output
    final = img.convert("RGB")
    buffer = io.BytesIO()
    final.save(buffer, format="WEBP", quality=config.IMAGE_QUALITY)
    return buffer.getvalue()

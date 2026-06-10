"""Pipeline configuration — loaded from environment variables with sensible defaults."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SEEN_URLS_FILE = DATA_DIR / "seen_urls.json"
PENDING_TOPICS_FILE = DATA_DIR / "pending_topics.json"
SITEMAP_CACHE_FILE = DATA_DIR / "sitemap_cache.json"

# ---------------------------------------------------------------------------
# CapitalColumn API
# ---------------------------------------------------------------------------
API_BASE_URL = os.getenv("CC_API_BASE_URL", "http://31.97.186.143:8000")
API_KEY = os.getenv("CC_API_KEY", "cc_SEED_KEY_change_me_in_production")
PUBLIC_SITE_URL = os.getenv("CC_PUBLIC_SITE_URL", "https://capitalcolumn.in")

# ---------------------------------------------------------------------------
# LLM Configuration
# ---------------------------------------------------------------------------
# Provider: "openai" or "gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Available OpenAI models for selection
OPENAI_MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"]

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Available Gemini models for selection
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]

# ---------------------------------------------------------------------------
# Replicate (Image Generation)
# ---------------------------------------------------------------------------
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

# Default image model
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "prunaai/z-image-turbo")

# Available image models for selection
IMAGE_MODELS = {
    "prunaai/z-image-turbo": {
        "name": "Z-Image Turbo (Fast)",
        "description": "Fast, cost-effective image generation",
    },
    "bytedance/seedream-3": {
        "name": "SeedReam 3 (ByteDance)",
        "description": "High quality, photorealistic images",
    },
    "google/nano-banana-pro": {
        "name": "Nano Banana Pro (Google)",
        "description": "Google's efficient image generator",
    },
}

# ---------------------------------------------------------------------------
# Article Defaults
# ---------------------------------------------------------------------------
DEFAULT_WORD_COUNT = int(os.getenv("WORD_COUNT", "1200"))
DEFAULT_STATUS = os.getenv("DEFAULT_STATUS", "draft")  # draft | in_review | published
AUTO_PUBLISH = os.getenv("AUTO_PUBLISH", "false").lower() == "true"
TARGET_LOCATION = os.getenv("TARGET_LOCATION", "India")

# ---------------------------------------------------------------------------
# Pipeline Settings
# ---------------------------------------------------------------------------
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
MAX_ARTICLES_PER_RUN = int(os.getenv("MAX_ARTICLES_PER_RUN", "5"))
MAX_INTERNAL_LINKS = int(os.getenv("MAX_INTERNAL_LINKS", "5"))
SITEMAP_CACHE_TTL_HOURS = int(os.getenv("SITEMAP_CACHE_TTL_HOURS", "6"))

# Image settings
IMAGE_MAX_WIDTH = 1200
IMAGE_MAX_HEIGHT = 800
IMAGE_QUALITY = 82  # WebP quality (0-100)

import os

from dotenv import load_dotenv

load_dotenv()

# Supabase HTTP API keys (not used by scrapers/DB today; for a future web UI)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

# How far back to scrape and which digests go into the daily email (24 = last day).
SCRAPE_HOURS = int(os.getenv("SCRAPE_HOURS", "24"))
EMAIL_DIGEST_HOURS = int(os.getenv("EMAIL_DIGEST_HOURS", os.getenv("SCRAPE_HOURS", "24")))

# When OpenAI has no quota: build digests from RSS text and send email without AI ranking.
USE_FALLBACK_DIGESTS = os.getenv("USE_FALLBACK_DIGESTS", "").lower() in ("1", "true", "yes")

YOUTUBE_CHANNELS = [
    "UCn8ujwUInbJkBhffxqAPBVQ",  # Dave Ebbelaar
    "UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
    "UCNJ1EctdEE88VnBeKmKYLA",  # AI Explained
    "UCdWHKDijI-m9081yQ6lEhw",  # Wes Roth
]

# Extra AI news via RSS (source id, feed URL). Add more in docs/SOURCES.md
RSS_FEEDS = [
    ("google_ai", "https://blog.google/technology/ai/rss/"),
    ("microsoft_ai", "https://blogs.microsoft.com/ai/feed/"),
    ("huggingface", "https://huggingface.co/blog/feed.xml"),
    ("nvidia_ai", "https://blogs.nvidia.com/feed/"),
    ("mit_ai", "https://www.technologyreview.com/topic/artificial-intelligence/feed/"),
    ("verge_ai", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("techcrunch_ai", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("langchain", "https://blog.langchain.dev/rss/"),
    ("arxiv_cs_ai", "http://export.arxiv.org/rss/cs.AI"),
    (
        "google_news_ai",
        "https://news.google.com/rss/search?q=artificial+intelligence+OR+LLM+OR+GenAI+OR+agentic+AI&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        "google_news_agents",
        "https://news.google.com/rss/search?q=AI+agents+OR+autonomous+agents&hl=en-US&gl=US&ceid=US:en",
    ),
]


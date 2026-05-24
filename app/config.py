import os

from dotenv import load_dotenv

load_dotenv()

# Supabase HTTP API keys (not used by scrapers/DB today; for a future web UI)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

# How far back to collect new items (RSS only returns ~15 recent entries per channel).
# 24 often yields 0 if creators did not post today; 168 = last 7 days is a practical default.
SCRAPE_HOURS = int(os.getenv("SCRAPE_HOURS", "168"))

# When OpenAI has no quota: build digests from RSS text and send email without AI ranking.
USE_FALLBACK_DIGESTS = os.getenv("USE_FALLBACK_DIGESTS", "").lower() in ("1", "true", "yes")

YOUTUBE_CHANNELS = [
    "UCn8ujwUInbJkBhffxqAPBVQ",  # Dave Ebbelaar
    "UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
]


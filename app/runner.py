from typing import List, Optional
from .config import YOUTUBE_CHANNELS, SCRAPE_HOURS, RSS_FEEDS
from .scrapers.youtube import YouTubeScraper, ChannelVideo
from .scrapers.openai import OpenAIScraper, OpenAIArticle
from .scrapers.anthropic import AnthropicScraper, AnthropicArticle
from .scrapers.rss_feed import RssFeedScraper
from .database.repository import Repository


def run_scrapers(hours: Optional[int] = None) -> dict:
    if hours is None:
        hours = SCRAPE_HOURS
    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()
    repo = Repository()
    
    youtube_videos = []
    video_dicts = []
    for channel_id in YOUTUBE_CHANNELS:
        videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)
        youtube_videos.extend(videos)
        video_dicts.extend([
            {
                "video_id": v.video_id,
                "title": v.title,
                "url": v.url,
                "channel_id": channel_id,
                "published_at": v.published_at,
                "description": v.description,
                "transcript": v.transcript
            }
            for v in videos
        ])
    
    openai_articles = openai_scraper.get_articles(hours=hours)
    anthropic_articles = anthropic_scraper.get_articles(hours=hours)
    rss_scraper = RssFeedScraper()
    feed_articles = rss_scraper.get_articles(RSS_FEEDS, hours=hours)
    
    if video_dicts:
        repo.bulk_create_youtube_videos(video_dicts)
    
    if openai_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in openai_articles
        ]
        repo.bulk_create_openai_articles(article_dicts)
    
    if anthropic_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in anthropic_articles
        ]
        repo.bulk_create_anthropic_articles(article_dicts)

    if feed_articles:
        feed_dicts = [
            {
                "guid": a.guid,
                "source": a.source,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category,
            }
            for a in feed_articles
        ]
        repo.bulk_create_feed_articles(feed_dicts)
    
    return {
        "youtube": youtube_videos,
        "openai": openai_articles,
        "anthropic": anthropic_articles,
        "feeds": feed_articles,
    }


if __name__ == "__main__":
    import sys

    hours = SCRAPE_HOURS
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])

    results = run_scrapers(hours=hours)
    print(f"Scrape window: last {hours} hours")
    print(f"YouTube videos: {len(results['youtube'])}")
    print(f"OpenAI articles: {len(results['openai'])}")
    print(f"Anthropic articles: {len(results['anthropic'])}")
    print(f"RSS feed articles: {len(results['feeds'])}")


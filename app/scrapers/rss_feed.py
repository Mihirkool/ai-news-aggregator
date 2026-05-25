from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

import feedparser
from pydantic import BaseModel


class FeedArticle(BaseModel):
    source: str
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class RssFeedScraper:
    def get_articles(
        self,
        feeds: List[Tuple[str, str]],
        hours: int = 24,
    ) -> List[FeedArticle]:
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        articles: List[FeedArticle] = []
        seen_guids: set[str] = set()

        for source, rss_url in feeds:
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                continue

            for entry in feed.entries:
                published_parsed = getattr(entry, "published_parsed", None) or getattr(
                    entry, "updated_parsed", None
                )
                if not published_parsed:
                    continue

                published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
                if published_time < cutoff_time:
                    continue

                raw_guid = entry.get("id", entry.get("link", ""))
                guid = f"{source}:{raw_guid}"
                if guid in seen_guids:
                    continue
                seen_guids.add(guid)

                articles.append(
                    FeedArticle(
                        source=source,
                        title=entry.get("title", "").strip(),
                        description=entry.get("summary", entry.get("description", "")),
                        url=entry.get("link", ""),
                        guid=guid,
                        published_at=published_time,
                        category=entry.get("tags", [{}])[0].get("term")
                        if entry.get("tags")
                        else source,
                    )
                )

        return articles

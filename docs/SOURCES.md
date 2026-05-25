# Adding news sources

## Already built in

| Type | Where to configure | Examples |
|------|-------------------|----------|
| YouTube | `app/config.py` → `YOUTUBE_CHANNELS` | Creator channel IDs |
| OpenAI blog | `app/scrapers/openai.py` | Fixed RSS |
| Anthropic | `app/scrapers/anthropic.py` | Community RSS mirrors |
| Many RSS feeds | `app/config.py` → `RSS_FEEDS` | Google AI, Microsoft, Hugging Face, arXiv, Google News, etc. |

Stored in Supabase:

- `youtube_videos`, `openai_articles`, `anthropic_articles`, **`feed_articles`** (all extra RSS sources)

After changing config, create the new table if needed:

```bash
uv run python -m app.database.create_tables
```

Add a feed by appending to `RSS_FEEDS`:

```python
("my_source", "https://example.com/blog/rss.xml"),
```

Find RSS links on most blogs via “RSS” in the page footer or `/feed`, `/rss.xml`.

---

## Twitter / X

**Not included by default** — X requires a paid [developer API](https://developer.x.com/). Scraping the website breaks their terms and breaks often.

**Steps if you want it later:**

1. Create an X Developer project and get a **Bearer token**.
2. Use the API v2 endpoint `GET /2/tweets/search/recent` with query e.g. `(AI OR LLM OR GenAI) lang:en -is:retweet`.
3. Add a small scraper module (e.g. `app/scrapers/twitter.py`) that maps tweets into `feed_articles` with `source="twitter"`.
4. Store `TWITTER_BEARER_TOKEN` in `.env` (never commit it).

**Lighter alternative:** follow AI accounts on X and add their **Nitter/RSS bridges** only if you run your own bridge (public Nitter instances are unreliable).

---

## Instagram

**Not included** — Meta’s Graph API only allows Instagram content for **business/creator accounts you own**, not arbitrary AI news pages.

**Options:**

- Manually follow accounts; no stable legal scrape for “all AI Instagram.”
- Use **RSS bridges** only for specific public profiles you care about (fragile).
- Prefer YouTube / blogs / Google News RSS (already in this project) for the same creators.

---

## Wikipedia

Wikipedia is an **encyclopedia**, not a daily news wire. “New AI being built” updates appear on article talk pages slowly.

**Reasonable approaches:**

1. **Google News RSS** (already in `RSS_FEEDS` as `google_news_ai`) — picks up press coverage of new models and companies.
2. **arXiv cs.AI RSS** (already included) — research preprints.
3. **Wikimedia API** (custom): monitor category [Artificial intelligence](https://en.wikipedia.org/wiki/Category:Artificial_intelligence) recent changes — noisy; only add if you want a dedicated scraper.

Example API (exploration only):

```
https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Artificial_intelligence&cmtype=page&cmlimit=20&format=json
```

Map results into `feed_articles` with `source="wikipedia"` if you build `app/scrapers/wikipedia.py`.

---

## Reddit, LinkedIn, newsletters

| Platform | Practical approach |
|----------|-------------------|
| Reddit | Subreddit RSS: `https://www.reddit.com/r/MachineLearning/.rss` — add tuple to `RSS_FEEDS` |
| LinkedIn | No open RSS; official API is restricted |
| Newsletters | If the author publishes RSS (Substack often has `/feed`) add URL to `RSS_FEEDS` |

---

## Suggested RSS to add yourself

```python
("reddit_ml", "https://www.reddit.com/r/MachineLearning/.rss"),
("reddit_localgpt", "https://www.reddit.com/r/LocalLLaMA/.rss"),
("semi_analysis", "https://www.semianalysis.com/feed"),
("import_ai", "https://importai.substack.com/feed"),
```

Test a feed URL in the browser or with:

```bash
uv run python -c "import feedparser; print(len(feedparser.parse('URL').entries))"
```

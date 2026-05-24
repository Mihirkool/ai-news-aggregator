import logging
from dotenv import load_dotenv

load_dotenv()

from datetime import datetime

from app.agent.email_agent import EmailAgent, EmailIntroduction, RankedArticleDetail, EmailDigestResponse
from app.agent.curator_agent import CuratorAgent
from app.config import USE_FALLBACK_DIGESTS
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository
from app.services.email import send_email, digest_to_html

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def generate_email_digest_simple(hours: int = 24, top_n: int = 10) -> EmailDigestResponse:
    repo = Repository()
    digests = repo.get_recent_digests(hours=hours)
    if not digests:
        raise ValueError("No digests available")

    selected = digests[:top_n]
    today = datetime.now().strftime("%B %d, %Y")
    introduction = EmailIntroduction(
        greeting=f"Hey {USER_PROFILE['name']}, here is your daily digest of AI news for {today}.",
        introduction=(
            f"Here are {len(selected)} recent items from your sources "
            "(summaries from feed text; enable OpenAI billing for AI-written digests)."
        ),
    )
    articles = [
        RankedArticleDetail(
            digest_id=d["id"],
            rank=i + 1,
            relevance_score=5.0,
            reasoning="Listed by date (fallback mode)",
            title=d["title"],
            summary=d["summary"],
            url=d["url"],
            article_type=d["article_type"],
        )
        for i, d in enumerate(selected)
    ]
    return EmailDigestResponse(
        introduction=introduction,
        articles=articles,
        total_ranked=len(digests),
        top_n=len(articles),
    )


def generate_email_digest(hours: int = 24, top_n: int = 10) -> EmailDigestResponse:
    if USE_FALLBACK_DIGESTS:
        return generate_email_digest_simple(hours=hours, top_n=top_n)
    curator = CuratorAgent(USER_PROFILE)
    email_agent = EmailAgent(USER_PROFILE)
    repo = Repository()
    
    digests = repo.get_recent_digests(hours=hours)
    total = len(digests)
    
    if total == 0:
        logger.warning(f"No digests found from the last {hours} hours")
        raise ValueError("No digests available")
    
    logger.info(f"Ranking {total} digests for email generation")
    ranked_articles = curator.rank_digests(digests)
    
    if not ranked_articles:
        logger.error("Failed to rank digests")
        raise ValueError("Failed to rank articles")
    
    logger.info(f"Generating email digest with top {top_n} articles")
    
    article_details = [
        RankedArticleDetail(
            digest_id=a.digest_id,
            rank=a.rank,
            relevance_score=a.relevance_score,
            reasoning=a.reasoning,
            title=next((d["title"] for d in digests if d["id"] == a.digest_id), ""),
            summary=next((d["summary"] for d in digests if d["id"] == a.digest_id), ""),
            url=next((d["url"] for d in digests if d["id"] == a.digest_id), ""),
            article_type=next((d["article_type"] for d in digests if d["id"] == a.digest_id), "")
        )
        for a in ranked_articles
    ]
    
    email_digest = email_agent.create_email_digest_response(
        ranked_articles=article_details,
        total_ranked=len(ranked_articles),
        limit=top_n
    )
    
    logger.info("Email digest generated successfully")
    logger.info(f"\n=== Email Introduction ===")
    logger.info(email_digest.introduction.greeting)
    logger.info(f"\n{email_digest.introduction.introduction}")
    
    return email_digest


def send_digest_email(hours: int = 24, top_n: int = 10) -> dict:
    try:
        result = generate_email_digest(hours=hours, top_n=top_n)
        markdown_content = result.to_markdown()
        html_content = digest_to_html(result)
        
        subject = f"Daily AI News Digest - {result.introduction.greeting.split('for ')[-1] if 'for ' in result.introduction.greeting else 'Today'}"
        
        send_email(
            subject=subject,
            body_text=markdown_content,
            body_html=html_content
        )
        
        logger.info("Email sent successfully!")
        return {
            "success": True,
            "subject": subject,
            "articles_count": len(result.articles)
        }
    except ValueError as e:
        logger.error(f"Error sending email: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    result = send_digest_email(hours=24, top_n=10)
    if result["success"]:
        print("\n=== Email Digest Sent ===")
        print(f"Subject: {result['subject']}")
        print(f"Articles: {result['articles_count']}")
    else:
        print(f"Error: {result['error']}")


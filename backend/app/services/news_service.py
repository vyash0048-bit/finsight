import logging
from typing import List
from datetime import datetime, timezone
import yfinance as yf
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.schemas.news import NewsArticle

logger = logging.getLogger(__name__)

# Lazily initialized to not block module load if mongo is missing during simple testing
_client = None
_db = None

def get_db():
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URL)
        _db = _client[settings.MONGO_DB]
    return _db

async def get_recent_news(ticker: str, days: int = 7) -> List[NewsArticle]:
    """
    Fetch recent news for a ticker and deduplicate them in MongoDB.
    """
    db = get_db()
    news_collection = db["news"]
    
    # 1. Fetch raw news from yfinance
    stock = yf.Ticker(ticker)
    raw_news = stock.news
    
    articles = []
    
    for item in raw_news:
        try:
            # yfinance returns Unix timestamp in seconds for 'providerPublishTime'
            published_at = datetime.fromtimestamp(item.get("providerPublishTime", 0), tz=timezone.utc)
            
            # Simple deduplication: Check if we already have an article with the exact same URL or same Title
            existing = await news_collection.find_one({
                "$or": [
                    {"url": item.get("link")},
                    {"title": item.get("title")}
                ]
            })
            
            if existing:
                logger.info(f"Skipping duplicate news: {item.get('title')}")
                continue
                
            article = NewsArticle(
                ticker=ticker,
                title=item.get("title", "No Title"),
                url=item.get("link", ""),
                source=item.get("publisher", "Unknown"),
                published_at=published_at,
                summary=str(item.get("relatedTickers", "")) # Summary isn't reliably available in yfinance
            )
            
            # Save to mongo
            await news_collection.insert_one(article.model_dump())
            articles.append(article)
            
        except Exception as e:
            logger.error(f"Error parsing news item for {ticker}: {str(e)}")
            continue
            
    return articles

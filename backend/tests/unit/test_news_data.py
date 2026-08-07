import pytest
from datetime import datetime, timezone

from app.schemas.news import NewsArticle
from app.services.news_service import get_recent_news

@pytest.fixture
def anyio_backend():
    return 'asyncio'

# We will use pytest.mark.asyncio for async tests. 
# We need to install pytest-asyncio if we haven't already. (Wait, anyio is installed by fastapi, but pytest-asyncio is usually needed. We can just use anyio)

@pytest.fixture
def mock_yfinance_news(mocker):
    # Two articles, one is a duplicate by title!
    mock_news = [
        {
            "title": "Stock hits all time high",
            "link": "https://news.com/1",
            "publisher": "NewsCorp",
            "providerPublishTime": 1700000000,
        },
        {
            "title": "Stock hits all time high", # Duplicate title
            "link": "https://news.com/2",
            "publisher": "AnotherCorp",
            "providerPublishTime": 1700000050,
        }
    ]
    
    mock_ticker = mocker.MagicMock()
    mock_ticker.news = mock_news
    
    return mocker.patch("app.services.news_service.yf.Ticker", return_value=mock_ticker)

@pytest.fixture
def mock_mongo(mocker):
    # Mock motor's collection find_one and insert_one to simulate deduplication
    class MockCollection:
        def __init__(self):
            self.stored = []
            
        async def find_one(self, query):
            # Very simple mock: just check if title matches any stored title
            or_conditions = query.get("$or", [])
            for cond in or_conditions:
                if "title" in cond:
                    for doc in self.stored:
                        if doc["title"] == cond["title"]:
                            return doc
            return None
            
        async def insert_one(self, doc):
            self.stored.append(doc)
            
    mock_db = {"news": MockCollection()}
    return mocker.patch("app.services.news_service.get_db", return_value=mock_db)

@pytest.mark.anyio
async def test_get_recent_news_deduplication(mock_yfinance_news, mock_mongo):
    # We call the service. It should return 1 article because the second is a duplicate.
    articles = await get_recent_news("AAPL")
    
    assert len(articles) == 1
    assert articles[0].title == "Stock hits all time high"
    assert articles[0].url == "https://news.com/1"

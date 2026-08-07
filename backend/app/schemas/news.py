from datetime import datetime

from pydantic import BaseModel


class NewsArticle(BaseModel):
    ticker: str
    title: str
    url: str
    source: str
    published_at: datetime
    summary: str

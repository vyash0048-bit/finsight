from datetime import datetime

from pydantic import BaseModel


class PriceBar(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    ticker: str

class PriceHistory(BaseModel):
    ticker: str
    period: str
    bars: list[PriceBar]

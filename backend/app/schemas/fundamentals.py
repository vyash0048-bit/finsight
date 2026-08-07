from pydantic import BaseModel
from typing import Optional

class FundamentalData(BaseModel):
    ticker: str
    market_cap: Optional[int] = None
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    eps_trailing: Optional[float] = None
    eps_forward: Optional[float] = None
    dividend_yield: Optional[float] = None
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    recommendation_key: Optional[str] = None

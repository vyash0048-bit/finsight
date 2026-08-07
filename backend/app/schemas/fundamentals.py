
from pydantic import BaseModel


class FundamentalData(BaseModel):
    ticker: str
    market_cap: int | None = None
    trailing_pe: float | None = None
    forward_pe: float | None = None
    eps_trailing: float | None = None
    eps_forward: float | None = None
    dividend_yield: float | None = None
    profit_margin: float | None = None
    operating_margin: float | None = None
    recommendation_key: str | None = None

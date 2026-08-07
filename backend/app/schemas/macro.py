
from pydantic import BaseModel


class MacroContext(BaseModel):
    sp500_trend: str  # e.g., "BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN"
    sp500_current_price: float | None = None
    treasury_10y_yield: float | None = None
    market_volatility_vix: float | None = None

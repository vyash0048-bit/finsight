from pydantic import BaseModel
from typing import Optional

class MacroContext(BaseModel):
    sp500_trend: str  # e.g., "BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN"
    sp500_current_price: Optional[float] = None
    treasury_10y_yield: Optional[float] = None
    market_volatility_vix: Optional[float] = None

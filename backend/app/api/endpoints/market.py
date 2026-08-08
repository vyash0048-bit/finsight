import logging
from typing import Any

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.market_data import PriceHistory
from app.services.market_data_service import MarketDataError, get_price_history
from app.services.technical_service import get_technical_features

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class TechnicalIndicators(BaseModel):
    ticker: str
    latest_close: float
    SMA_20: float = Field(..., description="20-day Simple Moving Average")
    EMA_20: float = Field(..., description="20-day Exponential Moving Average")
    RSI_14: float = Field(..., description="14-day Relative Strength Index")
    MACD: float = Field(..., description="MACD line value")
    MACD_signal: float = Field(..., description="MACD signal line value")
    BB_upper: float = Field(..., description="Bollinger Band upper")
    BB_lower: float = Field(..., description="Bollinger Band lower")
    trading_signal: str = Field(..., description="Rule-based signal (e.g. 'BULLISH (Momentum)')")


def _validate_ticker(ticker: str) -> str:
    ticker = ticker.strip().upper()
    if not ticker.isalpha() or not (1 <= len(ticker) <= 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticker must be 1-5 alphabetic characters",
        )
    return ticker


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/price/{ticker}", response_model=PriceHistory)
def get_price(
    ticker: str,
    period: str = Query("1mo", description="Period for price history (e.g. '1mo', '3mo', '1y')"),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve historical OHLCV price bars for a ticker.
    """
    ticker = _validate_ticker(ticker)

    try:
        history = get_price_history(ticker, period=period, use_cache=True)
    except MarketDataError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Market data unavailable: {e!s}",
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching prices for {ticker}: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error fetching market data",
        )

    return history


@router.get("/technicals/{ticker}", response_model=TechnicalIndicators)
def get_technicals(
    ticker: str,
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve pre-computed technical indicators (RSI, MACD, Bollinger Bands, etc.)
    for a ticker using 3 months of price data.
    """
    ticker = _validate_ticker(ticker)

    try:
        history = get_price_history(ticker, period="3mo", use_cache=True)
    except MarketDataError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Market data unavailable: {e!s}",
        )

    if not history.bars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No price data available for {ticker}",
        )

    # Convert to DataFrame for the technical service
    df = pd.DataFrame([{
        "open": b.open, "high": b.high, "low": b.low,
        "close": b.close, "volume": b.volume
    } for b in history.bars])

    features = get_technical_features(df)

    if "error" in features:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=features["error"],
        )

    return TechnicalIndicators(ticker=ticker, **features)

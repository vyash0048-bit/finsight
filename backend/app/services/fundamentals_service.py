import logging

import yfinance as yf

from app.schemas.fundamentals import FundamentalData

logger = logging.getLogger(__name__)

def get_fundamentals(ticker: str) -> FundamentalData:
    """
    Fetch fundamental data for a ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info:
            logger.warning(f"No fundamental info found for {ticker}")
            return FundamentalData(ticker=ticker)
            
        return FundamentalData(
            ticker=ticker,
            market_cap=info.get("marketCap"),
            trailing_pe=info.get("trailingPE"),
            forward_pe=info.get("forwardPE"),
            eps_trailing=info.get("trailingEps"),
            eps_forward=info.get("forwardEps"),
            dividend_yield=info.get("dividendYield"),
            profit_margin=info.get("profitMargins"),
            operating_margin=info.get("operatingMargins"),
            recommendation_key=info.get("recommendationKey")
        )
    except Exception as e:
        logger.error(f"Error fetching fundamentals for {ticker}: {e!s}")
        return FundamentalData(ticker=ticker)

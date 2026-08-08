import json
import logging
from datetime import datetime
from pathlib import Path


from tenacity import retry, stop_after_attempt, wait_exponential

from app.schemas.market_data import PriceBar, PriceHistory

logger = logging.getLogger(__name__)

# Very simple local file cache for development to avoid getting rate-limited by Yahoo Finance
CACHE_DIR = Path(".cache/market_data")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

class MarketDataError(Exception):
    pass

@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def _fetch_from_yfinance(ticker: str, period: str):
    """
    Fetch data from Yahoo Finance. This function is wrapped with tenacity
    to automatically retry on network failures.
    """
    import pandas as pd
    import yfinance as yf
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        raise MarketDataError(f"No price data found for ticker {ticker} with period {period}")
        
    return df

def get_price_history(ticker: str, period: str = "1mo", use_cache: bool = True) -> PriceHistory:
    import pandas as pd
    """
    Retrieve historical price data for a given ticker.
    Supports basic file-based caching during development.
    """
    ticker = ticker.upper()
    cache_file = CACHE_DIR / f"{ticker}_{period}_{datetime.now().strftime('%Y%m%d')}.json"
    
    # 1. Try Cache
    if use_cache and cache_file.exists():
        logger.info(f"Cache hit for {ticker} ({period})")
        with open(cache_file, "r") as f:
            data = json.load(f)
            return PriceHistory.model_validate(data)
            
    logger.info(f"Fetching fresh data for {ticker} ({period}) from Yahoo Finance")
    
    # 2. Fetch from External API (with retries)
    try:
        df = _fetch_from_yfinance(ticker, period)
    except Exception as e:
        logger.error(f"Failed to fetch market data for {ticker}: {e!s}")
        raise MarketDataError(f"Market data service unavailable: {e!s}")
        
    # 3. Clean and Transform
    df.reset_index(inplace=True)
    
    bars = []
    for _, row in df.iterrows():
        # yfinance returns timezone-aware datetimes in the index (now a column named 'Date' or 'Datetime')
        date_col = 'Date' if 'Date' in df.columns else 'Datetime'
        
        bars.append(PriceBar(
            timestamp=row[date_col].to_pydatetime(),
            open=float(row['Open']),
            high=float(row['High']),
            low=float(row['Low']),
            close=float(row['Close']),
            volume=int(row['Volume']),
            ticker=ticker
        ))
        
    history = PriceHistory(ticker=ticker, period=period, bars=bars)
    
    # 4. Save to Cache
    if use_cache:
        with open(cache_file, "w") as f:
            f.write(history.model_dump_json())
            
    return history

import pandas as pd
from typing import List, Dict
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from app.services.market_data_service import get_price_history

def optimize_portfolio(tickers: List[str]) -> Dict[str, float]:
    """
    Optimizes a portfolio using mean-variance optimization (Max Sharpe Ratio).
    Returns the optimal weights for the given tickers.
    """
    if not tickers or len(tickers) < 2:
        return {ticker: 1.0 for ticker in tickers} if tickers else {}
        
    prices_dict = {}
    
    # Fetch historical prices for the past year
    for ticker in tickers:
        history = get_price_history(ticker, period="1y", use_cache=True)
        if history and history.bars:
            prices_dict[ticker] = {bar.timestamp: bar.close for bar in history.bars}
            
    if not prices_dict:
        return {}
        
    # Construct a DataFrame of closing prices
    df = pd.DataFrame(prices_dict)
    df.index = pd.to_datetime(df.index, utc=True).tz_localize(None)
    df = df.sort_index().dropna()
    
    if len(df) < 50:
        # Not enough data for meaningful optimization, return equal weights
        return {ticker: 1.0 / len(tickers) for ticker in tickers}
        
    try:
        # Calculate expected returns and sample covariance
        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)
        
        # Optimize for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        
        return dict(cleaned_weights)
    except Exception as e:
        # Fallback to equal weighting if optimization fails
        return {ticker: 1.0 / len(tickers) for ticker in tickers}

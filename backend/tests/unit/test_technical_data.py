import numpy as np
import pandas as pd
from app.services.technical_service import get_technical_features


def test_get_technical_features():
    # Generate 50 days of fake price data
    np.random.seed(42)
    base_price = 150
    prices = [base_price]
    for _ in range(49):
        # random walk
        prices.append(prices[-1] + np.random.normal(0, 2))
        
    df = pd.DataFrame({
        "open": prices,
        "high": [p + 1 for p in prices],
        "low": [p - 1 for p in prices],
        "close": prices,
        "volume": [1000] * 50
    })
    
    # Force the last price to be very high to simulate overbought
    df.loc[49, "close"] = 250
    df.loc[48, "close"] = 240
    df.loc[47, "close"] = 230
    
    result = get_technical_features(df)
    
    assert "error" not in result
    assert "SMA_20" in result
    assert "RSI_14" in result
    assert "MACD" in result
    assert "trading_signal" in result
    
    # RSI should be high because we spiked the price at the end
    assert result["RSI_14"] > 70
    assert "BEARISH" in result["trading_signal"] or "BULLISH" in result["trading_signal"]

def test_get_technical_features_not_enough_data():
    # Only 10 rows, should return error
    df = pd.DataFrame({
        "open": [100]*10,
        "high": [100]*10,
        "low": [100]*10,
        "close": [100]*10,
        "volume": [1000]*10
    })
    
    result = get_technical_features(df)
    assert "error" in result

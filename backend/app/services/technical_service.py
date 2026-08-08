from typing import Any




def get_technical_features(df: 'pd.DataFrame') -> dict[str, Any]:
    import pandas as pd
    import ta
    """
    Calculate SMA, EMA, RSI, MACD, and Bollinger Bands from a price DataFrame using the 'ta' library.
    Returns the latest indicator values and a simple rule-based signal.
    """
    if df is None or df.empty or len(df) < 30:
        return {"error": "Not enough data to calculate technicals"}
        
    df = df.copy()
    
    # Ensure column names are correct case if they differ
    close = df['close'] if 'close' in df else df['Close']
    
    # Calculate Indicators using ta
    df['SMA_20'] = ta.trend.sma_indicator(close, window=20)
    df['EMA_20'] = ta.trend.ema_indicator(close, window=20)
    df['RSI_14'] = ta.momentum.rsi(close, window=14)
    
    macd = ta.trend.MACD(close, window_slow=26, window_fast=12, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    
    bollinger = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    df['BB_upper'] = bollinger.bollinger_hband()
    df['BB_lower'] = bollinger.bollinger_lband()
    
    # Extract the most recent values
    latest = df.iloc[-1]
    
    rsi_val = latest.get('RSI_14', 50)
    if pd.isna(rsi_val): rsi_val = 50
    
    macd_val = latest.get('MACD', 0)
    macd_signal = latest.get('MACD_signal', 0)
    
    close_price = latest.get('close', 0)
    bb_upper = latest.get('BB_upper', close_price * 1.1)
    bb_lower = latest.get('BB_lower', close_price * 0.9)
    
    # Generate simple rule-based signal
    signal = "NEUTRAL"
    if rsi_val > 70 and close_price > bb_upper:
        signal = "BEARISH (Overbought)"
    elif rsi_val < 30 and close_price < bb_lower:
        signal = "BULLISH (Oversold)"
    elif macd_val > macd_signal and rsi_val < 60:
        signal = "BULLISH (Momentum)"
    elif macd_val < macd_signal and rsi_val > 40:
        signal = "BEARISH (Momentum)"
        
    return {
        "latest_close": float(close_price),
        "SMA_20": float(latest.get('SMA_20', 0)),
        "EMA_20": float(latest.get('EMA_20', 0)),
        "RSI_14": float(rsi_val),
        "MACD": float(macd_val),
        "MACD_signal": float(macd_signal),
        "BB_upper": float(bb_upper),
        "BB_lower": float(bb_lower),
        "trading_signal": signal
    }

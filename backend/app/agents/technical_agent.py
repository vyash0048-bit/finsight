from app.agents.base import AgentState
from app.services.market_data_service import get_price_history
from app.services.technical_service import get_technical_features
import pandas as pd

def technical_node(state: AgentState) -> dict:
    ticker = state["ticker"]
    # Fetch 1 month of daily data
    history = get_price_history(ticker, period="3mo", use_cache=True)
    
    if not history.bars:
        return {"technical_analysis": "No price data available.", "messages": ["Tech agent failed"]}
        
    df = pd.DataFrame([{
        "open": b.open, "high": b.high, "low": b.low, 
        "close": b.close, "volume": b.volume
    } for b in history.bars])
    
    features = get_technical_features(df)
    
    if "error" in features:
        analysis = f"Technical error: {features['error']}"
    else:
        analysis = f"Technicals for {ticker}: RSI={features.get('RSI_14', 0):.2f}. Signal: {features.get('trading_signal', 'NEUTRAL')}."
        
    return {"technical_analysis": analysis, "messages": [f"Technical agent completed for {ticker}"]}

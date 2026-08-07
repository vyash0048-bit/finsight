from app.agents.base import AgentState
from app.services.fundamentals_service import get_fundamentals

def fundamental_node(state: AgentState) -> dict:
    ticker = state["ticker"]
    fundamentals = get_fundamentals(ticker)
    
    analysis = f"Fundamentals for {ticker}: PE={fundamentals.trailing_pe}, Market Cap={fundamentals.market_cap}. "
    if fundamentals.trailing_pe and fundamentals.trailing_pe < 25:
        analysis += "Valuation looks reasonable."
    else:
        analysis += "Valuation appears high."
        
    return {"fundamental_analysis": analysis, "messages": [f"Fundamental agent completed for {ticker}"]}

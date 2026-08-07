from typing import TypedDict, List
from app.services.portfolio_service import optimize_portfolio

class PortfolioState(TypedDict):
    tickers: List[str]
    portfolio_analysis: str
    messages: List[str]

def portfolio_node(state: PortfolioState) -> dict:
    tickers = state["tickers"]
    
    if not tickers:
        return {"portfolio_analysis": "No tickers provided.", "messages": ["Portfolio agent failed"]}
        
    weights = optimize_portfolio(tickers)
    
    if not weights:
        analysis = "Failed to compute portfolio weights."
    else:
        analysis = "Optimal Portfolio Allocation (Max Sharpe):\n"
        for ticker, weight in weights.items():
            analysis += f"- {ticker}: {weight:.1%}\n"
            
    return {"portfolio_analysis": analysis, "messages": ["Portfolio agent completed"]}

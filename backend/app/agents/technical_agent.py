
from pydantic import BaseModel, Field

from app.agents.base import AgentState, BaseAgent


class TechnicalOutputSchema(BaseModel):
    trend: str = Field(..., description="Current trend: 'BULLISH', 'BEARISH', or 'NEUTRAL'")
    support_levels: list[float] = Field(..., description="Key price support levels")
    resistance_levels: list[float] = Field(..., description="Key price resistance levels")
    momentum_signal: str = Field(..., description="Momentum indicator signal, e.g. 'OVERSOLD', 'OVERBOUGHT'")
    summary: str = Field(..., description="Concise technical summary and price action observation")

class TechnicalAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a specialized Technical Analyst Agent. You analyze price history, volume, and momentum indicators "
            "(RSI, MACD, moving averages) to determine short to medium-term market trends. "
            "Output a structured technical perspective based purely on the provided data context."
        )
        
    @property
    def output_schema(self):
        return TechnicalOutputSchema
        
    def get_tools(self) -> list:
        return ["get_price_history", "get_technical_features"]
        
    def execute(self, ticker: str):
        try:
            from app.services.market_data_service import get_price_history
            from app.services.technical_service import get_technical_features
            
            history = get_price_history(ticker, period="3mo", use_cache=True)
            context = {"ticker": ticker, "price_data_summary": "No data"}
            
            if history.bars:
                df = pd.DataFrame([{
                    "open": b.open, "high": b.high, "low": b.low, 
                    "close": b.close, "volume": b.volume
                } for b in history.bars])
                features = get_technical_features(df)
                context["price_data_summary"] = {
                    "latest_close": df["close"].iloc[-1] if not df.empty else None,
                    "features": features
                }
            return self.run(context)
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))
        
# For LangGraph integration
def technical_node(state: AgentState) -> dict:
    import pandas as pd

    from app.services.market_data_service import get_price_history
    from app.services.technical_service import get_technical_features
    
    ticker = state["ticker"]
    history = get_price_history(ticker, period="3mo", use_cache=True)
    
    context = {"ticker": ticker, "price_data_summary": "No data"}
    
    if history.bars:
        df = pd.DataFrame([{
            "open": b.open, "high": b.high, "low": b.low, 
            "close": b.close, "volume": b.volume
        } for b in history.bars])
        features = get_technical_features(df)
        context["price_data_summary"] = {
            "latest_close": df["close"].iloc[-1] if not df.empty else None,
            "features": features
        }
        
    agent = TechnicalAgent()
    out = agent.run(context)
    
    if out.status == "success":
        analysis_str = f"Technical Summary: {out.data['summary']} (Trend: {out.data['trend']})"
    else:
        analysis_str = "Technical agent failed to generate analysis."
        
    return {"technical_analysis": analysis_str, "messages": [f"Technical agent completed for {ticker}"]}

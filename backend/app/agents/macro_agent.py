
from app.agents.base import BaseAgent
from pydantic import BaseModel, Field


class MacroOutputSchema(BaseModel):
    market_regime: str = Field(..., description="'BULL_MARKET', 'BEAR_MARKET', or 'VOLATILE'")
    interest_rate_impact: str = Field(..., description="Expected impact of current interest rates on the asset")
    key_macro_events: list[str] = Field(..., description="List of major macroeconomic factors (e.g. inflation, Fed meetings) impacting the asset")
    summary: str = Field(..., description="Concise macro environment summary")

class MacroAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a highly skilled Macroeconomic Analyst Agent. Your job is to analyze broader economic conditions, "
            "interest rates, inflation data, and market regimes, and determine how they specifically impact a given asset. "
            "Output a structured macroeconomic assessment."
        )
        
    @property
    def output_schema(self):
        return MacroOutputSchema
        
    def get_tools(self) -> list:
        return ["get_macro_indicators"]
        
    def execute(self, ticker: str):
        try:
            from app.services.macro_service import get_macro_context
            indicators = get_macro_context()
            return self.run({"ticker": ticker, "macro_indicators": indicators.model_dump() if hasattr(indicators, 'model_dump') else {}})
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))
        
# For LangGraph integration
def macro_node(state: dict) -> dict:
    from app.services.macro_service import get_macro_indicators
    
    ticker = state.get("ticker", "SPY")
    indicators = get_macro_indicators()
    
    context = {"ticker": ticker, "macro_indicators": indicators}
        
    agent = MacroAgent()
    out = agent.run(context)
    
    if out.status == "success":
        analysis_str = f"Macro Summary: {out.data['summary']} (Regime: {out.data['market_regime']})"
    else:
        analysis_str = "Macro agent failed to generate analysis."
        
    return {"macro_analysis": analysis_str, "messages": [f"Macro agent completed for {ticker}"]}

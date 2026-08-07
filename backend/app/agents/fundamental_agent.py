from app.agents.base import BaseAgent, AgentState
from pydantic import BaseModel, Field
from typing import Optional

class FundamentalOutputSchema(BaseModel):
    valuation_signal: str = Field(..., description="'UNDERVALUED', 'OVERVALUED', or 'FAIRLY_VALUED'")
    pe_ratio_analysis: str = Field(..., description="Brief analysis of the P/E ratio context")
    growth_prospects: str = Field(..., description="Analysis of revenue/earnings growth prospects")
    financial_health: str = Field(..., description="Assessment of balance sheet and debt levels")
    summary: str = Field(..., description="Overall fundamental health summary")

class FundamentalAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a specialized Fundamental Analyst Agent. You evaluate company financials, valuation multiples, "
            "and growth metrics. Use the provided financial data (e.g., P/E, EPS, Debt/Equity) to output a structured "
            "fundamental analysis. Do not hallucinate metrics not present in the context."
        )
        
    @property
    def output_schema(self):
        return FundamentalOutputSchema
        
    def get_tools(self) -> list:
        return ["get_company_info", "get_financials"]
        
    def execute(self, ticker: str):
        try:
            from app.services.fundamentals_service import get_fundamentals
            info = get_fundamentals(ticker)
            return self.run({"ticker": ticker, "company_info": info.model_dump() if hasattr(info, 'model_dump') else {}})
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))
        
# For LangGraph integration
def fundamental_node(state: AgentState) -> dict:
    from app.services.fundamentals_service import get_company_info
    
    ticker = state["ticker"]
    info = get_company_info(ticker)
    
    context = {"ticker": ticker, "company_info": info}
        
    agent = FundamentalAgent()
    out = agent.run(context)
    
    if out.status == "success":
        analysis_str = f"Fundamentals Summary: {out.data['summary']} (Valuation: {out.data['valuation_signal']})"
    else:
        analysis_str = "Fundamental agent failed to generate analysis."
        
    return {"fundamental_analysis": analysis_str, "messages": [f"Fundamental agent completed for {ticker}"]}

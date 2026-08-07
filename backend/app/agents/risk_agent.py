
from app.agents.base import BaseAgent
from pydantic import BaseModel, Field


class RiskOutputSchema(BaseModel):
    risk_score: int = Field(..., description="Overall risk score from 1 (lowest) to 10 (highest)")
    volatility_assessment: str = Field(..., description="Assessment of recent price volatility and historical VaR")
    downside_risks: list[str] = Field(..., description="List of primary downside risks or red flags")
    summary: str = Field(..., description="Concise risk profile summary")

class RiskAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a strict Risk Management Agent. Your responsibility is to analyze all incoming data "
            "(fundamentals, technicals, news, and macro) for a given asset to identify red flags, assess downside risk, "
            "and assign an overall risk score. Always prioritize capital preservation in your assessment."
        )
        
    @property
    def output_schema(self):
        return RiskOutputSchema
        
    def get_tools(self) -> list:
        return []
        
    def execute(self, ticker: str, findings: dict):
        try:
            import pandas as pd
            from app.services.market_data_service import get_price_history
            from app.services.risk_service import compute_risk_metrics
            
            history = get_price_history(ticker, period="1y", use_cache=True)
            metrics_dict = {}
            if history and history.bars:
                df = pd.DataFrame([b.close for b in history.bars], columns=['close'])
                returns = df['close'].pct_change().dropna()
                metrics = compute_risk_metrics(returns)
                metrics_dict = metrics.model_dump()
                
            context = {
                "ticker": ticker,
                "agent_findings": findings,
                "quantitative_risk_metrics": metrics_dict
            }
            return self.run(context)
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))
        
# For LangGraph integration
def risk_node(state: dict) -> dict:
    context = {
        "ticker": state.get("ticker"),
        "fundamental_analysis": state.get("fundamental_analysis"),
        "technical_analysis": state.get("technical_analysis"),
        "news_analysis": state.get("news_analysis"),
        "macro_analysis": state.get("macro_analysis")
    }
        
    agent = RiskAgent()
    out = agent.run(context)
    
    if out.status == "success":
        analysis_str = f"Risk Summary: {out.data['summary']} (Risk Score: {out.data['risk_score']}/10)"
    else:
        analysis_str = "Risk agent failed to generate analysis."
        
    return {"risk_analysis": analysis_str, "messages": [f"Risk agent completed for {state.get('ticker')}"]}

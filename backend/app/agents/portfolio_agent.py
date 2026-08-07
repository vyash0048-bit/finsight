
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class PortfolioOutputSchema(BaseModel):
    explanation: str = Field(..., description="Plain-English explanation of the allocated weights. Must explicitly state that this is a model-dependent estimate and explicitly list the assumptions made (e.g., historical lookback window, mean-variance max-sharpe optimization).")
    warning: str = Field(..., description="A standard disclosure emphasizing that this is not a guarantee of future performance.")

class PortfolioAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a Portfolio Optimization Analyst. Your job is to take the mathematical outputs of a portfolio optimizer "
            "(ticker weights) and explain them to a client in plain English. You must explicitly disclose the assumptions used "
            "by the model (e.g., 1-year historical lookback window, mean-variance Max Sharpe Ratio objective). You must "
            "clearly state that these weights are model-dependent estimates and not a guarantee of future performance."
        )
        
    @property
    def output_schema(self):
        return PortfolioOutputSchema
        
    def get_tools(self) -> list:
        return ["optimize_portfolio"]
        
    def execute(self, tickers: list[str]):
        try:
            from app.services.portfolio_service import optimize_portfolio
            weights = optimize_portfolio(tickers)
            
            context = {
                "tickers": tickers,
                "assumptions_applied": {
                    "lookback": "1y",
                    "method": "Mean-Variance Optimization (Max Sharpe Ratio)",
                    "risk_free_rate": "Default pypfopt risk-free rate (approx 2%)",
                    "historical_returns": "Expected returns based on mean historical return"
                },
                "computed_weights": weights
            }
            return self.run(context)
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))

# LangGraph node compatibility
def portfolio_node(state: dict) -> dict:
    tickers = state.get("tickers", [])
    if not tickers:
        return {"portfolio_analysis": "No tickers provided.", "messages": ["Portfolio agent failed"]}
    
    agent = PortfolioAgent()
    out = agent.execute(tickers)
    
    if out.status == "success":
        analysis = f"Optimal Portfolio Allocation (Max Sharpe):\n{out.data['explanation']}\n\nWarning: {out.data['warning']}"
    else:
        analysis = "Failed to compute portfolio weights."
        
    return {"portfolio_analysis": analysis, "messages": ["Portfolio agent completed"]}


from app.agents.base import BaseAgent
from pydantic import BaseModel, Field


class ReportOutputSchema(BaseModel):
    executive_summary: str = Field(..., description="High level summary of the asset.")
    final_recommendation: str = Field(..., description="STRONG BUY, BUY, HOLD, SELL, STRONG SELL")
    key_drivers: list[str] = Field(..., description="The main factors driving this recommendation.")

class ReportAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are the Lead Portfolio Manager (Supervisor). Synthesize the findings from all specialized agents "
            "and the Debate Agent's conflict resolution into a final comprehensive report and recommendation. "
            "Make a clear final decision."
        )
        
    @property
    def output_schema(self):
        return ReportOutputSchema
        
    def get_tools(self): 
        return []
        
    def execute(self, ticker: str, findings: dict, debate_out: dict):
        try:
            context = {
                "ticker": ticker,
                "agent_findings": findings,
                "debate_resolution": debate_out
            }
            return self.run(context)
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))

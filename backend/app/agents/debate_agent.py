from app.agents.base import BaseAgent
from pydantic import BaseModel, Field


class DebateOutputSchema(BaseModel):
    conflict_detected: bool = Field(..., description="True if there is a major conflict between agents (e.g. Technical says strong buy, Risk says extremely high risk).")
    resolution: str = Field(..., description="Resolution or synthesis of the conflict, or 'No major conflict' if false.")

class DebateAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are the Debate Agent. Analyze the outputs from various analyst agents. If they fundamentally "
            "conflict (e.g., Bullish Technicals vs Terrible Fundamentals/Risk), synthesize a balanced resolution. "
            "Focus only on serious contradictions."
        )
        
    @property
    def output_schema(self):
        return DebateOutputSchema
        
    def get_tools(self): 
        return []
        
    def execute(self, ticker: str, findings: dict):
        try:
            context = {"ticker": ticker, "agent_findings": findings}
            return self.run(context)
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))


from pydantic import BaseModel, Field

from app.agents.base import AgentState, BaseAgent


class NewsOutputSchema(BaseModel):
    sentiment_score: float = Field(..., description="Overall sentiment score between -1.0 (very bearish) to 1.0 (very bullish)")
    key_themes: list[str] = Field(..., description="List of 2-3 main themes found in the news")
    bullish_points: list[str] = Field(..., description="Key bullish factors extracted from news")
    bearish_points: list[str] = Field(..., description="Key bearish factors extracted from news")
    summary: str = Field(..., description="A concise 2-sentence summary of the news sentiment")

class NewsAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a highly specialized Financial News Analyst Agent. Your objective is to ingest recent news "
            "headlines and text chunks for a given ticker and output a structured sentiment and thematic analysis. "
            "Focus only on facts and explicit opinions in the provided text. Never invent news."
        )
        
    @property
    def output_schema(self):
        return NewsOutputSchema
        
    def get_tools(self) -> list:
        return ["retrieve_and_rerank"]
        
    def execute(self, ticker: str):
        try:
            from app.services.rag_service import retrieve_and_rerank
            results = retrieve_and_rerank(f"Latest important news and sentiment about {ticker}", ticker=ticker, k=5)
            
            context = {"ticker": ticker, "news_documents": []}
            if results and results.get("documents") and results["documents"][0]:
                context["news_documents"] = results["documents"][0]
                
            return self.run(context)
        except Exception as e:
            from app.agents.base import AgentOutput
            return AgentOutput(agent_name=self.name, status="error", data={}, summary=str(e))
            
# For LangGraph integration
def news_node(state: AgentState) -> dict:
    from app.services.rag_service import retrieve_and_rerank
    ticker = state["ticker"]
    query = f"Latest important news and sentiment about {ticker}"
    
    results = retrieve_and_rerank(query, ticker=ticker, k=5)
    
    context = {"ticker": ticker, "news_documents": []}
    if results and results.get("documents") and results["documents"][0]:
        context["news_documents"] = results["documents"][0]
        
    agent = NewsAgent()
    out = agent.run(context)
    
    if out.status == "success":
        analysis_str = f"News Summary: {out.data['summary']} (Sentiment: {out.data['sentiment_score']})"
    else:
        analysis_str = "News agent failed to generate analysis."
        
    return {"news_analysis": analysis_str, "messages": [f"News agent completed for {ticker}"]}

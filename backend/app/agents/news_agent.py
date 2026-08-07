from app.agents.base import AgentState
from app.services.rag_service import search_similar_text

def news_node(state: AgentState) -> dict:
    ticker = state["ticker"]
    query = f"Latest important news and sentiment about {ticker}"
    
    results = search_similar_text(query, n_results=3)
    
    if not results or not results["documents"] or not results["documents"][0]:
        analysis = "No recent news found in vector database."
    else:
        analysis = "Recent News Highlights:\n"
        for doc in results["documents"][0]:
            # Take just the first 150 chars of each chunk to avoid huge texts
            analysis += f"- {doc[:150]}...\n"
            
    return {"news_analysis": analysis, "messages": [f"News agent completed for {ticker}"]}

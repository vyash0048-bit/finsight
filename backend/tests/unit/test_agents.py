import pytest
from app.agents.supervisor import build_graph

def test_agent_graph():
    graph = build_graph()
    initial_state = {
        "ticker": "AAPL",
        "fundamental_analysis": "",
        "technical_analysis": "",
        "news_analysis": "",
        "final_decision": "",
        "messages": []
    }
    
    result = graph.invoke(initial_state)
    
    assert "final_decision" in result
    assert "AAPL" in result["final_decision"]
    assert "RECOMMENDATION" in result["final_decision"]
    assert len(result["messages"]) == 4

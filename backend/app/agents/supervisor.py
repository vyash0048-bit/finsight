from app.agents.base import AgentState
from app.agents.fundamental_agent import fundamental_node
from app.agents.news_agent import news_node
from app.agents.technical_agent import technical_node
from langgraph.graph import END, StateGraph


def supervisor_node(state: AgentState) -> dict:
    f_analysis = state.get("fundamental_analysis", "")
    t_analysis = state.get("technical_analysis", "")
    n_analysis = state.get("news_analysis", "")
    
    # In a real app, an LLM (like GPT-4) would read these and make a dynamic decision.
    # For now, we simulate the supervisor's synthesis logic.
    decision = "HOLD"
    if "BULLISH" in t_analysis and "reasonable" in f_analysis:
        decision = "STRONG BUY"
    elif "BEARISH" in t_analysis:
        decision = "SELL"
        
    final_output = (
        f"--- SUPERVISOR DECISION ---\n"
        f"TICKER: {state['ticker']}\n\n"
        f"FUNDAMENTALS:\n{f_analysis}\n\n"
        f"TECHNICALS:\n{t_analysis}\n\n"
        f"NEWS:\n{n_analysis}\n\n"
        f"RECOMMENDATION: {decision}\n"
    )
    
    return {"final_decision": final_output, "messages": ["Supervisor made a decision"]}

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("fundamental", fundamental_node)
    workflow.add_node("technical", technical_node)
    workflow.add_node("news", news_node)
    workflow.add_node("supervisor", supervisor_node)
    
    # Sequential execution graph for simplicity
    workflow.set_entry_point("fundamental")
    
    workflow.add_edge("fundamental", "technical")
    workflow.add_edge("technical", "news")
    workflow.add_edge("news", "supervisor")
    workflow.add_edge("supervisor", END)
    
    return workflow.compile()

from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    ticker: str
    fundamental_analysis: str
    technical_analysis: str
    news_analysis: str
    final_decision: str
    messages: Annotated[List[str], operator.add]

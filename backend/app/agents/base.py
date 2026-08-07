from typing import TypedDict, Annotated, List, Any, Dict, Optional, Type
import operator
from abc import ABC, abstractmethod
from pydantic import BaseModel
import json

class AgentState(TypedDict):
    ticker: str
    fundamental_analysis: str
    technical_analysis: str
    news_analysis: str
    final_decision: str
    messages: Annotated[List[str], operator.add]

class AgentOutput(BaseModel):
    agent_name: str
    status: str
    data: Dict[str, Any]
    summary: str

class BaseAgent(ABC):
    def __init__(self, llm_client=None):
        self.name = self.__class__.__name__
        from app.services.llm_client import LLMClient
        self.llm_client = llm_client or LLMClient()
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The tightly scoped role/system prompt for this agent."""
        pass
        
    @property
    @abstractmethod
    def output_schema(self) -> Type[BaseModel]:
        """The Pydantic schema expected as output from the LLM."""
        pass
        
    @abstractmethod
    def get_tools(self) -> list:
        """Return a list of tools/functions this agent has access to."""
        pass

    def run(self, context: Dict[str, Any]) -> AgentOutput:
        """
        Executes the agent's logic given the context.
        """
        prompt = self.build_prompt(context)
        llm_response = self.llm_client.call_llm(
            prompt=prompt, 
            schema=self.output_schema,
            system_prompt=self.system_prompt
        )
        
        if not llm_response:
            return AgentOutput(
                agent_name=self.name,
                status="error",
                data={},
                summary="LLM failed to produce valid output."
            )
            
        return AgentOutput(
            agent_name=self.name,
            status="success",
            data=json.loads(llm_response.model_dump_json()),
            summary=f"{self.name} completed analysis successfully."
        )
        
    def build_prompt(self, context: Dict[str, Any]) -> str:
        """
        Combine system prompt, context, and instruction.
        """
        context_str = json.dumps(context, indent=2)
        return f"Please analyze the following context based on your role:\n\n{context_str}"

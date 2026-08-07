from unittest.mock import MagicMock

import pytest
from app.agents.fundamental_agent import FundamentalAgent, FundamentalOutputSchema
from app.agents.macro_agent import MacroAgent, MacroOutputSchema
from app.agents.news_agent import NewsAgent, NewsOutputSchema
from app.agents.risk_agent import RiskAgent, RiskOutputSchema
from app.agents.technical_agent import TechnicalAgent, TechnicalOutputSchema
from app.services.llm_client import LLMClient
from pydantic import BaseModel


class MockLLMResponse:
    def __init__(self, data: BaseModel):
        self._data = data
        
    def model_dump(self):
        return self._data.model_dump()
        
    def model_dump_json(self):
        return self._data.model_dump_json()

@pytest.fixture
def mock_llm_client():
    client = MagicMock(spec=LLMClient)
    return client

def test_news_agent(mock_llm_client):
    mock_llm_client.call_llm.return_value = MockLLMResponse(
        NewsOutputSchema(
            sentiment_score=0.8,
            key_themes=["Earnings Beat", "Product Launch"],
            bullish_points=["Strong sales", "High margins"],
            bearish_points=["Supply chain issues"],
            summary="Very positive news overall."
        )
    )
    
    agent = NewsAgent(llm_client=mock_llm_client)
    out = agent.run({"ticker": "AAPL", "news_documents": ["fake news text"]})
    
    assert out.status == "success"
    assert out.agent_name == "NewsAgent"
    assert out.data["sentiment_score"] == 0.8
    assert "Financial News Analyst Agent" in agent.system_prompt
    mock_llm_client.call_llm.assert_called_once()

def test_technical_agent(mock_llm_client):
    mock_llm_client.call_llm.return_value = MockLLMResponse(
        TechnicalOutputSchema(
            trend="BULLISH",
            support_levels=[140.5, 135.0],
            resistance_levels=[150.0, 155.0],
            momentum_signal="OVERBOUGHT",
            summary="Stock is trending up."
        )
    )
    
    agent = TechnicalAgent(llm_client=mock_llm_client)
    out = agent.run({"ticker": "AAPL", "price_data_summary": {}})
    
    assert out.status == "success"
    assert out.data["trend"] == "BULLISH"
    
def test_fundamental_agent(mock_llm_client):
    mock_llm_client.call_llm.return_value = MockLLMResponse(
        FundamentalOutputSchema(
            valuation_signal="UNDERVALUED",
            pe_ratio_analysis="P/E is low",
            growth_prospects="High growth",
            financial_health="Strong balance sheet",
            summary="Solid fundamentals."
        )
    )
    
    agent = FundamentalAgent(llm_client=mock_llm_client)
    out = agent.run({"ticker": "AAPL"})
    
    assert out.status == "success"
    assert out.data["valuation_signal"] == "UNDERVALUED"

def test_macro_agent(mock_llm_client):
    mock_llm_client.call_llm.return_value = MockLLMResponse(
        MacroOutputSchema(
            market_regime="BULL_MARKET",
            interest_rate_impact="Positive",
            key_macro_events=["Fed meeting"],
            summary="Good macro."
        )
    )
    
    agent = MacroAgent(llm_client=mock_llm_client)
    out = agent.run({"ticker": "AAPL"})
    
    assert out.status == "success"
    assert out.data["market_regime"] == "BULL_MARKET"

def test_risk_agent(mock_llm_client):
    mock_llm_client.call_llm.return_value = MockLLMResponse(
        RiskOutputSchema(
            risk_score=3,
            volatility_assessment="Low volatility",
            downside_risks=["Market correction"],
            summary="Low risk."
        )
    )
    
    agent = RiskAgent(llm_client=mock_llm_client)
    out = agent.run({"ticker": "AAPL"})
    
    assert out.status == "success"
    assert out.data["risk_score"] == 3

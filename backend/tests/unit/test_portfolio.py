import pytest
import pandas as pd
from app.services.portfolio_service import optimize_portfolio
from app.agents.portfolio_agent import portfolio_node, PortfolioAgent
from app.agents.base import AgentOutput
from unittest.mock import patch

def test_optimize_portfolio(mocker):
    # Mock price history
    def mock_get_price_history(ticker, period, use_cache):
        class MockBar:
            def __init__(self, timestamp, close):
                self.timestamp = timestamp
                self.close = close
                self.open = close
                self.high = close
                self.low = close
                self.volume = 1000
                self.ticker = ticker
        
        class MockHistory:
            def __init__(self):
                # Generate simple upward trends
                if ticker == "AAPL":
                    self.bars = [MockBar(f"2023-01-{i:02d}", 100 + i) for i in range(1, 30)] * 4
                else:
                    self.bars = [MockBar(f"2023-01-{i:02d}", 100 + i*0.5) for i in range(1, 30)] * 4
                    
        return MockHistory()
        
    mocker.patch("app.services.portfolio_service.get_price_history", side_effect=mock_get_price_history)
    
    weights = optimize_portfolio(["AAPL", "MSFT"])
    
    assert weights is not None
    assert "AAPL" in weights
    assert "MSFT" in weights
    # The sum of weights should be close to 1
    assert abs(sum(weights.values()) - 1.0) < 0.01

def test_portfolio_agent_architecture(mocker):
    # Mock the underlying execute method to avoid LLM call
    mock_execute = mocker.patch.object(PortfolioAgent, 'execute')
    mock_execute.return_value = AgentOutput(
        agent_name="PortfolioAgent",
        status="success",
        data={
            "explanation": "Given AAPL: 60.0% and MSFT: 40.0%, this is an estimate based on mean-variance optimization over 1y.",
            "warning": "Not a guarantee of future performance."
        },
        summary="Success"
    )
    
    state = {"tickers": ["AAPL", "MSFT"]}
    result = portfolio_node(state)
    
    assert "portfolio_analysis" in result
    assert "AAPL: 60.0%" in result["portfolio_analysis"]
    assert "Not a guarantee" in result["portfolio_analysis"]
    assert "Optimal Portfolio Allocation" in result["portfolio_analysis"]

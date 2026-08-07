import pytest
import pandas as pd
from app.services.portfolio_service import optimize_portfolio
from app.agents.portfolio_agent import portfolio_node

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
                # Generate an upward trend for AAPL and flat for MSFT to see if it favors AAPL
                if ticker == "AAPL":
                    self.bars = [MockBar(f"2023-01-{i:02d}", 100 + i) for i in range(1, 30)] * 4
                else:
                    self.bars = [MockBar(f"2023-01-{i:02d}", 100) for i in range(1, 30)] * 4
                    
        return MockHistory()
        
    mocker.patch("app.services.portfolio_service.get_price_history", side_effect=mock_get_price_history)
    
    weights = optimize_portfolio(["AAPL", "MSFT"])
    
    assert weights is not None
    assert "AAPL" in weights
    assert "MSFT" in weights
    # The sum of weights should be close to 1
    assert abs(sum(weights.values()) - 1.0) < 0.01

def test_portfolio_agent(mocker):
    mocker.patch("app.agents.portfolio_agent.optimize_portfolio", return_value={"AAPL": 0.6, "MSFT": 0.4})
    
    state = {"tickers": ["AAPL", "MSFT"], "portfolio_analysis": "", "messages": []}
    result = portfolio_node(state)
    
    assert "portfolio_analysis" in result
    assert "AAPL: 60.0%" in result["portfolio_analysis"]
    assert "MSFT: 40.0%" in result["portfolio_analysis"]

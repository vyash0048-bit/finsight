import pytest
import pandas as pd
from datetime import datetime, timezone

from app.services.market_data_service import get_price_history, MarketDataError

@pytest.fixture
def mock_yfinance(mocker):
    # Create a mock dataframe that yfinance would return
    dates = pd.date_range(start="2024-01-01", periods=3, tz=timezone.utc)
    mock_df = pd.DataFrame({
        'Open': [100.0, 101.0, 102.0],
        'High': [105.0, 106.0, 107.0],
        'Low': [95.0, 96.0, 97.0],
        'Close': [103.0, 104.0, 105.0],
        'Volume': [1000, 2000, 3000]
    }, index=dates)
    mock_df.index.name = 'Date'
    
    # Mock the internal fetch function so it never hits the internet
    return mocker.patch('app.services.market_data_service._fetch_from_yfinance', return_value=mock_df)

@pytest.fixture
def mock_yfinance_empty(mocker):
    # Mock the fetch function to raise an Exception, simulating a failure or empty data
    return mocker.patch('app.services.market_data_service._fetch_from_yfinance', side_effect=Exception("Simulated failure"))

def test_get_price_history_success(mock_yfinance):
    # We turn off cache for tests to ensure it calls our mock
    result = get_price_history(ticker="AAPL", period="1mo", use_cache=False)
    
    assert result.ticker == "AAPL"
    assert result.period == "1mo"
    assert len(result.bars) == 3
    
    # Check the first bar
    first_bar = result.bars[0]
    assert first_bar.open == 100.0
    assert first_bar.close == 103.0
    assert first_bar.volume == 1000

    # Ensure our mock was called exactly once
    mock_yfinance.assert_called_once_with("AAPL", "1mo")

def test_get_price_history_empty_data(mock_yfinance_empty):
    # We expect our service to raise a custom MarketDataError when it gets empty data or fails
    with pytest.raises(MarketDataError):
        get_price_history(ticker="UNKNOWN_TICKER", period="1mo", use_cache=False)

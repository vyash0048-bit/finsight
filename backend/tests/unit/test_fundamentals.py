import pytest
from app.services.fundamentals_service import get_fundamentals
from app.schemas.fundamentals import FundamentalData

def test_get_fundamentals_success(mocker):
    mock_info = {
        "marketCap": 2000000000000,
        "trailingPE": 25.5,
        "forwardPE": 22.1,
        "trailingEps": 5.2,
        "forwardEps": 6.1,
        "dividendYield": 0.015,
        "profitMargins": 0.25,
        "operatingMargins": 0.30,
        "recommendationKey": "buy"
    }
    
    mock_ticker = mocker.MagicMock()
    mock_ticker.info = mock_info
    
    mocker.patch("app.services.fundamentals_service.yf.Ticker", return_value=mock_ticker)
    
    data = get_fundamentals("AAPL")
    
    assert isinstance(data, FundamentalData)
    assert data.ticker == "AAPL"
    assert data.market_cap == 2000000000000
    assert data.trailing_pe == 25.5
    assert data.recommendation_key == "buy"

def test_get_fundamentals_missing_data(mocker):
    # Simulate a ticker with missing/empty info
    mock_ticker = mocker.MagicMock()
    mock_ticker.info = {}
    
    mocker.patch("app.services.fundamentals_service.yf.Ticker", return_value=mock_ticker)
    
    data = get_fundamentals("UNKNOWN")
    
    assert data.ticker == "UNKNOWN"
    assert data.market_cap is None

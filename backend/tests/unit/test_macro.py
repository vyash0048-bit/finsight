import pytest
import pandas as pd
from app.services.macro_service import get_macro_context
from app.schemas.macro import MacroContext

def test_get_macro_context_success(mocker):
    # Mock yfinance history to return a fake dataframe
    def mock_history(period):
        if period == "6mo":
            # Simulate bullish S&P 500 where price > 50 SMA
            return pd.DataFrame({
                "Close": [100.0] * 50 + [120.0] # SMA will be ~100.4, price is 120
            })
        else:
            return pd.DataFrame({"Close": [4.2]})
            
    mock_ticker = mocker.MagicMock()
    mock_ticker.history.side_effect = mock_history
    
    mocker.patch("app.services.macro_service.yf.Ticker", return_value=mock_ticker)
    
    context = get_macro_context()
    
    assert isinstance(context, MacroContext)
    assert context.sp500_trend == "BULLISH"
    assert context.sp500_current_price == 120.0
    assert context.treasury_10y_yield == 4.2
    assert context.market_volatility_vix == 4.2

def test_get_macro_context_error(mocker):
    mocker.patch("app.services.macro_service.yf.Ticker", side_effect=Exception("API Error"))
    
    context = get_macro_context()
    assert context.sp500_trend == "UNKNOWN"

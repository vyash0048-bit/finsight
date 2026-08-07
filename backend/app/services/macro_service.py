import logging

import yfinance as yf

from app.schemas.macro import MacroContext

logger = logging.getLogger(__name__)

def get_macro_context() -> MacroContext:
    """
    Fetch macroeconomic indicators using yfinance.
    Gets S&P 500 (^GSPC), 10-Year Treasury (^TNX), and VIX (^VIX).
    """
    try:
        # Fetch S&P 500 for trend
        sp500 = yf.Ticker("^GSPC")
        sp500_hist = sp500.history(period="6mo")
        
        trend = "NEUTRAL"
        sp500_price = None
        
        if not sp500_hist.empty and len(sp500_hist) > 50:
            sp500_price = float(sp500_hist['Close'].iloc[-1])
            sma_50 = sp500_hist['Close'].rolling(window=50).mean().iloc[-1]
            if sp500_price > sma_50:
                trend = "BULLISH"
            else:
                trend = "BEARISH"
                
        # Fetch 10-Year Treasury Yield
        tnx = yf.Ticker("^TNX")
        tnx_hist = tnx.history(period="5d")
        tnx_yield = float(tnx_hist['Close'].iloc[-1]) if not tnx_hist.empty else None
        
        # Fetch VIX
        vix = yf.Ticker("^VIX")
        vix_hist = vix.history(period="5d")
        vix_price = float(vix_hist['Close'].iloc[-1]) if not vix_hist.empty else None
        
        return MacroContext(
            sp500_trend=trend,
            sp500_current_price=sp500_price,
            treasury_10y_yield=tnx_yield,
            market_volatility_vix=vix_price
        )
    except Exception as e:
        logger.error(f"Error fetching macro context: {e!s}")
        return MacroContext(sp500_trend="UNKNOWN")

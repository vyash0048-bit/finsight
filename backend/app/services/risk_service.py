import logging

import numpy as np
import pandas as pd
from app.schemas.risk import RiskSnapshot

logger = logging.getLogger(__name__)

def compute_risk_metrics(returns: pd.Series, risk_free_rate: float = 0.02) -> RiskSnapshot:
    """
    Computes key risk metrics from a series of daily returns.
    Includes Volatility, Max Drawdown, Sharpe Ratio, and Historical VaR.
    """
    if returns.empty or len(returns) < 30:
        logger.warning("Insufficient data points for robust risk metrics. Returning zeros.")
        return RiskSnapshot(
            annualized_volatility=0.0,
            max_drawdown=0.0,
            sharpe_ratio=0.0,
            historical_var_95=0.0,
            lookback_days=len(returns)
        )
        
    # Annualized Volatility
    volatility = returns.std() * np.sqrt(252)
    
    # Annualized Return
    annual_return = returns.mean() * 252
    
    # Sharpe Ratio
    sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0.0
    
    # Max Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    
    # Historical Value at Risk (VaR) at 95% confidence level
    # 5th percentile of daily returns
    var_95 = np.percentile(returns.dropna(), 5)
    
    return RiskSnapshot(
        annualized_volatility=float(volatility),
        max_drawdown=float(max_drawdown),
        sharpe_ratio=float(sharpe_ratio),
        historical_var_95=float(var_95),
        lookback_days=len(returns)
    )

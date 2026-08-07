import pytest
import numpy as np
import pandas as pd
from app.services.risk_service import compute_risk_metrics

def test_compute_risk_metrics_math():
    # Construct a synthetic returns series with known properties
    # Let's do 252 days (1 year)
    np.random.seed(42)
    # Mean daily return = 0.001, Daily vol = 0.01
    daily_mean = 0.001
    daily_vol = 0.01
    returns = pd.Series(np.random.normal(daily_mean, daily_vol, 252))
    
    # Hand-computed theoretical expectations
    # Annualized Volatility expected ~ 0.01 * sqrt(252) = ~ 0.1587
    # Annualized Return expected ~ 0.001 * 252 = 0.252
    # Risk-free rate = 0.02
    # Sharpe expected ~ (0.252 - 0.02) / 0.1587 = ~ 1.46
    
    metrics = compute_risk_metrics(returns, risk_free_rate=0.02)
    
    # We assert that the computed metrics are mathematically sound
    assert metrics.lookback_days == 252
    
    # Volatility should be close to theoretical 15.8%
    assert 0.13 < metrics.annualized_volatility < 0.18
    
    # Sharpe ratio should be positive and around 1.4
    assert 1.0 < metrics.sharpe_ratio < 2.0
    
    # Max drawdown should be negative and less than 0
    assert metrics.max_drawdown < 0
    assert metrics.max_drawdown > -1.0
    
    # Historical VaR at 95% should be negative (a loss)
    # Z-score for 95% is ~1.645 -> expected VaR ~ 0.001 - 1.645*0.01 = -0.015
    assert metrics.historical_var_95 < 0
    assert -0.025 < metrics.historical_var_95 < -0.005

def test_compute_risk_metrics_empty():
    returns = pd.Series([], dtype=float)
    metrics = compute_risk_metrics(returns)
    assert metrics.annualized_volatility == 0.0
    assert metrics.lookback_days == 0

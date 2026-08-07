from pydantic import BaseModel, Field


class RiskSnapshot(BaseModel):
    annualized_volatility: float = Field(..., description="Annualized volatility of returns")
    max_drawdown: float = Field(..., description="Maximum drawdown observed in the period")
    sharpe_ratio: float = Field(..., description="Annualized Sharpe ratio")
    historical_var_95: float = Field(..., description="Historical Value at Risk (95% confidence level)")
    lookback_days: int = Field(..., description="Number of trading days used in the calculation")

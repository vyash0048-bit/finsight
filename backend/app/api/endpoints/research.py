import hashlib
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from app.api.deps import get_current_user
from app.models.user import User
from app.orchestration.orchestrator import Orchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ResearchRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g. 'AAPL')")

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        v = v.strip().upper()
        if not v.isalpha() or not (1 <= len(v) <= 5):
            raise ValueError("Ticker must be 1-5 alphabetic characters")
        return v


class ResearchReport(BaseModel):
    ticker: str
    findings: dict[str, Any]
    debate: dict[str, Any]
    report: dict[str, Any]


# In-memory report cache — keyed by ticker
_report_cache: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/report", response_model=ResearchReport, status_code=status.HTTP_200_OK)
async def create_research_report(
    body: ResearchRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Trigger a full multi-agent research report for a given ticker.
    This orchestrates the debate among specialized agents and can take
    several seconds to complete.
    """
    ticker = body.ticker
    logger.info(f"User {current_user.id} requested research report for {ticker}")

    try:
        orchestrator = Orchestrator(timeout=60)
        result = await orchestrator.run_research(ticker)
    except Exception as e:
        logger.error(f"Orchestration failed for {ticker}: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research orchestration failed: {e!s}",
        )

    # Cache the result for later retrieval
    _report_cache[ticker] = result

    return ResearchReport(**result)


@router.get("/report/{ticker}", response_model=ResearchReport)
def get_research_report(
    ticker: str,
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a cached/historical research report for a ticker.
    """
    ticker = ticker.strip().upper()
    report = _report_cache.get(ticker)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No cached report found for ticker '{ticker}'. "
                   f"Use POST /research/report to generate one.",
        )
    return ResearchReport(**report)

from unittest.mock import patch

import pytest
from app.agents.base import AgentOutput
from app.orchestration.orchestrator import Orchestrator


@pytest.mark.asyncio
async def test_orchestrator_error_isolation():
    orchestrator = Orchestrator(timeout=2)
    
    # Mock the execute methods of agents directly to avoid external calls
    with patch("app.agents.news_agent.NewsAgent.execute") as mock_news, \
         patch("app.agents.technical_agent.TechnicalAgent.execute") as mock_tech, \
         patch("app.agents.fundamental_agent.FundamentalAgent.execute") as mock_fund, \
         patch("app.agents.macro_agent.MacroAgent.execute") as mock_macro, \
         patch("app.agents.risk_agent.RiskAgent.execute") as mock_risk, \
         patch("app.agents.debate_agent.DebateAgent.execute") as mock_debate, \
         patch("app.agents.report_agent.ReportAgent.execute") as mock_report:
             
        # Mock successful responses for most
        mock_news.return_value = AgentOutput(agent_name="NewsAgent", status="success", data={"sentiment_score": 0.8}, summary="Good news")
        mock_fund.return_value = AgentOutput(agent_name="FundamentalAgent", status="success", data={"valuation_signal": "UNDERVALUED"}, summary="Good fund")
        mock_macro.return_value = AgentOutput(agent_name="MacroAgent", status="success", data={"market_regime": "BULL_MARKET"}, summary="Good macro")
        mock_risk.return_value = AgentOutput(agent_name="RiskAgent", status="success", data={"risk_score": 2}, summary="Low risk")
        mock_debate.return_value = AgentOutput(agent_name="DebateAgent", status="success", data={"conflict_detected": False}, summary="No conflict")
        mock_report.return_value = AgentOutput(agent_name="ReportAgent", status="success", data={"final_recommendation": "BUY"}, summary="Buy it")
        
        # Simulate TechnicalAgent timing out or raising exception
        def failing_tech(*args):
            raise Exception("API failure simulated")
            
        mock_tech.side_effect = failing_tech
        
        result = await orchestrator.run_research("AAPL")
        
        # Verify orchestration order (tech, fund, macro, news in parallel -> risk -> debate -> report)
        mock_news.assert_called_once()
        mock_tech.assert_called_once()
        mock_fund.assert_called_once()
        mock_macro.assert_called_once()
        mock_risk.assert_called_once()
        mock_debate.assert_called_once()
        mock_report.assert_called_once()
        
        # Verify error isolation
        assert result["findings"]["technical"]["status"] == "error"
        assert "failed" in result["findings"]["technical"]["summary"]
        
        # Rest of the pipeline should still succeed
        assert result["findings"]["news"]["status"] == "success"
        assert result["report"]["status"] == "success"
        assert result["report"]["data"]["final_recommendation"] == "BUY"

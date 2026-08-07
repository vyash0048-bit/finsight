import asyncio
from typing import Dict, Any

from app.agents.news_agent import NewsAgent
from app.agents.technical_agent import TechnicalAgent
from app.agents.fundamental_agent import FundamentalAgent
from app.agents.macro_agent import MacroAgent
from app.agents.risk_agent import RiskAgent
from app.agents.debate_agent import DebateAgent
from app.agents.report_agent import ReportAgent

class Orchestrator:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        
    async def run_agent_safe(self, agent, func, *args) -> dict:
        import time
        from app.core.metrics import agent_run_total, agent_run_duration_seconds
        
        start_time = time.time()
        try:
            # Run the synchronous agent execution in a thread to not block the asyncio event loop
            out = await asyncio.wait_for(
                asyncio.to_thread(func, *args),
                timeout=self.timeout
            )
            duration = time.time() - start_time
            agent_run_duration_seconds.labels(agent_name=agent.name).observe(duration)
            agent_run_total.labels(agent_name=agent.name, status=out.status).inc()
            return {"status": out.status, "data": out.data, "summary": out.summary}
        except asyncio.TimeoutError:
            duration = time.time() - start_time
            agent_run_duration_seconds.labels(agent_name=agent.name).observe(duration)
            agent_run_total.labels(agent_name=agent.name, status="error").inc()
            return {"status": "error", "summary": f"{agent.name} timed out."}
        except Exception as e:
            duration = time.time() - start_time
            agent_run_duration_seconds.labels(agent_name=agent.name).observe(duration)
            agent_run_total.labels(agent_name=agent.name, status="error").inc()
            return {"status": "error", "summary": f"{agent.name} failed: {str(e)}"}

    async def run_research(self, ticker: str) -> dict:
        # Phase 1: Parallel dispatch of base worker agents
        news = NewsAgent()
        tech = TechnicalAgent()
        fund = FundamentalAgent()
        macro = MacroAgent()
        
        # Parallel execution via gather
        results = await asyncio.gather(
            self.run_agent_safe(news, news.execute, ticker),
            self.run_agent_safe(tech, tech.execute, ticker),
            self.run_agent_safe(fund, fund.execute, ticker),
            self.run_agent_safe(macro, macro.execute, ticker)
        )
        
        findings = {
            "news": results[0],
            "technical": results[1],
            "fundamental": results[2],
            "macro": results[3]
        }
        
        # Phase 2: Risk Agent (depends on all base findings)
        risk = RiskAgent()
        risk_out = await self.run_agent_safe(risk, risk.execute, ticker, findings)
        findings["risk"] = risk_out
        
        # Phase 3: Conflict Detection / Debate Agent
        debate_agent = DebateAgent()
        debate_out = await self.run_agent_safe(debate_agent, debate_agent.execute, ticker, findings)
        
        # Phase 4: Final Synthesis (Supervisor)
        report_agent = ReportAgent()
        report_out = await self.run_agent_safe(report_agent, report_agent.execute, ticker, findings, debate_out)
        
        return {
            "ticker": ticker,
            "findings": findings,
            "debate": debate_out,
            "report": report_out
        }

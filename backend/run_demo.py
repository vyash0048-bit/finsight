import asyncio
import json
import os
import sys

# Load env file manually
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key.strip().upper()] = val.strip().strip('"').strip("'")

from app.orchestration.orchestrator import Orchestrator

async def run_for_ticker(ticker: str):
    print(f"\n{'='*50}\nStarting Research for {ticker}...\n{'='*50}")
    orchestrator = Orchestrator(timeout=45) # generous timeout for real APIs + LLM
    result = await orchestrator.run_research(ticker)
    
    print(f"\n[FINAL REPORT FOR {ticker}]")
    if result["report"]["status"] == "success":
        report_data = result["report"]["data"]
        print(f"RECOMMENDATION: {report_data.get('final_recommendation')}")
        print(f"EXECUTIVE SUMMARY:\n{report_data.get('executive_summary')}")
        print("KEY DRIVERS:")
        for driver in report_data.get("key_drivers", []):
            print(f" - {driver}")
    else:
        print(f"Report failed: {result['report']['summary']}")
        
    print(f"\n[AGENT STATUS FOR {ticker}]")
    for agent, findings in result["findings"].items():
        print(f" - {agent.capitalize()}: {findings['status']}")
    print(f" - Risk: {result['findings'].get('risk', {}).get('status', 'unknown')}")
    print(f" - Debate: {result['debate']['status']}")

async def main():
    tickers = ["AAPL", "MSFT", "TSLA"]
    for t in tickers:
        await run_for_ticker(t)
        
if __name__ == "__main__":
    asyncio.run(main())

# FinSight

![CI Pipeline](https://github.com/vyash0048-bit/finsight/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An AI-driven multi-agent research swarm and optimization platform.

## What it does
FinSight is an investment research platform driven by multiple specialized LLM agents. Instead of replacing human judgment with automated trading, FinSight empowers researchers by gathering real-time market data, technical indicators, fundamental filings, news sentiment, and macro context. A Supervisor Agent orchestrates a debate among these specialized lenses, culminating in a citation-backed, synthesized investment memo.

## Explicit Non-Goals
- **Not** a real trading bot; it never executes trades or connects to a brokerage.
- **Not** investment advice; every report is for research and demonstration purposes only.
- **Not** attempting to beat the market or backtest alpha generation — the value is in explainable synthesis, not in claimed returns.

## Architecture
See the detailed [Architecture Document](docs/architecture.md) for flow diagrams and component breakdowns.

## Quick Start
Get up and running in under 5 minutes:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vyash0048-bit/finsight.git
   cd finsight
   ```
2. **Environment Setup:**
   ```bash
   cp .env.example .env
   # Add your external API keys (OpenAI/Anthropic, Finnhub, etc.) to .env
   ```
3. **Launch with Docker Compose:**
   ```bash
   docker-compose -f infra/docker-compose.yml up --build
   ```
4. **Access the application:**
   - Frontend: `http://localhost:8501`
   - API Docs: `http://localhost:8000/docs`

## Tech Stack
| Domain | Technologies |
|---|---|
| **Backend** | Python 3.12, FastAPI, Pydantic |
| **Frontend** | Streamlit |
| **AI / Agents** | LangGraph, OpenAI/Anthropic SDKs, SentenceTransformers |
| **Data & Storage** | PostgreSQL, MongoDB, ChromaDB, Redis |
| **Infra & CI/CD** | Docker, Docker Compose, GitHub Actions |

## Key Design Decisions
- **Postgres + MongoDB Split:** Structured data (users, price bars) lives in Postgres for integrity and relational querying, while unstructured data (agent outputs, news, filings) lives in MongoDB for schema flexibility.
- **Hand-rolled Orchestration:** Provides exact control over the agent debate flow and failure isolation.
- **Read-Only / No Trading:** Sidesteps regulatory and liability concerns while showcasing complex multi-agent reasoning.
*Read more in the [Design Decisions](docs/design_decisions.md) document.*

## Running Tests
To run the test suite locally:
```bash
cd backend
pip install -r requirements.txt
pytest --cov=app tests/
```

## Roadmap
- Enhance macro agent with more FRED indicators.
- Support multi-ticker portfolio correlation analysis.
- Implement streaming debate visualization in Streamlit.
- Add user-defined evaluation rubrics for reports.
- Support open-weight local models (Ollama/vLLM).

## Credits
Inspired by the academic prototype **StockAgent** (Zhang, Liu, Jin et al., 2024, arXiv:2407.18957).

## License & Disclaimer
Licensed under the MIT License. **This software is for educational purposes only and does not constitute financial advice.**

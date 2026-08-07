# System Architecture

FinSight uses a layered architecture to orchestrate multiple LLM agents, ingest diverse financial data, and serve results via a modern web stack.

## High-Level Component Diagram

```mermaid
flowchart TB
    subgraph Client
        UI[Streamlit / React Frontend]
    end

    subgraph API["FastAPI Backend"]
        GW[API Gateway / Routers]
        AUTH[Auth Service - JWT]
        ORCH[Agent Orchestrator]
    end

    subgraph Agents["Agent Layer"]
        SUP[Supervisor Agent]
        NEWS[News Agent]
        TECH[Technical Analysis Agent]
        FUND[Fundamental Analysis Agent]
        MACRO[Macro Agent]
        RISK[Risk Agent]
        PORT[Portfolio Agent]
        MEM[Memory Agent]
        DEBATE[Debate Agent]
        REPORT[Report Agent]
    end

    subgraph Data["Data Layer"]
        MONGO[(MongoDB - documents, news, reports)]
        PG[(PostgreSQL - users, portfolios, structured price data)]
        REDIS[(Redis - cache, rate limit, session)]
        VDB[(ChromaDB/FAISS - embeddings)]
    end

    subgraph External["External APIs"]
        YF[Yahoo Finance]
        AV[Alpha Vantage]
        FH[Finnhub]
        NA[NewsAPI]
        SEC[SEC EDGAR]
        FRED[FRED - macro data]
    end

    subgraph Infra["Infra / Ops"]
        MLF[MLflow - experiment + prompt tracking]
        PROM[Prometheus/Grafana]
        CI[GitHub Actions CI/CD]
    end

    UI --> GW
    GW --> AUTH
    GW --> ORCH
    ORCH --> SUP
    SUP --> NEWS
    SUP --> TECH
    SUP --> FUND
    SUP --> MACRO
    SUP --> RISK
    SUP --> PORT
    SUP --> DEBATE
    DEBATE --> REPORT
    NEWS --> MEM
    TECH --> MEM
    FUND --> MEM
    MACRO --> MEM
    RISK --> MEM

    NEWS --> NA
    NEWS --> VDB
    TECH --> YF
    TECH --> AV
    FUND --> SEC
    FUND --> FH
    MACRO --> FRED
    RISK --> PG

    MEM --> MONGO
    MEM --> VDB
    ORCH --> REDIS
    AUTH --> PG

    ORCH --> MLF
```

## Layers Overview

1. **Client Layer:** A Streamlit frontend allows researchers to input a ticker, monitor the agent debate stream, and read the synthesized report.
2. **API Layer:** A FastAPI backend acts as the gateway. It handles JWT authentication, background task dispatching, and acts as the orchestrator to kick off the multi-agent debate.
3. **Agent Layer:** The core of FinSight. Specialized agents gather information using tools (e.g. News, Technicals, Macro). A Supervisor Agent dictates the debate flow and a Report Agent synthesizes the findings.
4. **Data Layer:** Uses Polyglot persistence. PostgreSQL for highly structured, tabular data (users, timeseries), MongoDB for unstructured logs and raw documents, ChromaDB for vector retrieval (RAG), and Redis for ephemeral caching.
5. **External APIs:** Integration with Yahoo Finance, SEC EDGAR, FRED, and NewsAPI provides real-world context for the agents.

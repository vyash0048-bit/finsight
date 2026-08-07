# Architectural Design Decisions & Trade-offs

This document outlines the core technical decisions made while designing FinSight. It is intended to explain the *why* rather than the *what*.

## 1. Polyglot Persistence: PostgreSQL + MongoDB
**Decision**: Use PostgreSQL for structured relational data and MongoDB for unstructured document storage.
**Why**: 
Financial applications require strict ACID compliance and schema enforcement for user management, portfolio tracking, and timeseries data (OHLCV price bars). PostgreSQL is the best tool for this. However, LLM agent outputs, raw SEC filings, and news articles are highly unstructured and heterogeneous. Storing them in Postgres would require excessive use of JSONB columns, making indexing and schema migrations cumbersome. MongoDB handles this unstructured document layer naturally. 
**Trade-off**: Increases operational complexity (managing two database engines locally and in CI/CD) in exchange for optimal data modeling.

## 2. Vector Store: Local ChromaDB vs. Hosted Pinecone/Qdrant
**Decision**: Use ChromaDB running locally (or FAISS) rather than a managed cloud vector database.
**Why**:
For a portfolio project and initial MVP, limiting external cloud dependencies significantly lowers the barrier to entry (no credit card required to run the stack, zero network latency for local embeddings). ChromaDB in persistent mode operates seamlessly alongside the FastAPI backend.
**Trade-off**: Local vector stores are harder to scale horizontally. In a true enterprise deployment, migrating to Pinecone or a managed Qdrant cluster would be necessary to handle billions of embeddings.

## 3. Scope: Research/Decision-Support vs. Autonomous Trading
**Decision**: The multi-agent swarm operates strictly in a read-only, research-oriented capacity. It does not place real trades.
**Why**:
Autonomous trading bots introduce severe liability, regulatory compliance issues, and require complex sandboxing. By constraining the agents to *research and synthesis*, the platform demonstrates 100% of the complex LLM orchestration, RAG pipelines, and data engineering required for a trading system, without the catastrophic risk of a hallucinating agent draining a brokerage account.
**Trade-off**: We cannot backtest the AI's direct alpha generation. The success metric is shifted from "ROI" to "Explainability and Synthesis Quality".

## 4. Multi-Agent Orchestration: Hand-Rolled / LangGraph vs. Simple Prompts
**Decision**: Use a structured Supervisor-Worker agent pattern over a simple linear chain of prompts.
**Why**:
A single mega-prompt attempting to analyze technicals, fundamentals, and news simultaneously suffers from severe context degradation and hallucination. By separating concerns (e.g., a Technical Agent that only sees price tools, a News Agent that only sees a vector DB of articles), each agent can reason deeply about its domain. The Supervisor Agent then forces them to debate, exposing contradicting signals (e.g., strong technicals but a bearish macro environment).
**Trade-off**: Significantly higher latency per report and higher API token costs. A single report might trigger 10-15 LLM calls instead of 1.

## 5. Ingestion Pipeline: Explicit TTL Caching vs. Real-Time Streaming
**Decision**: External API responses (news, fundamentals) are cached with explicit Time-To-Live (TTL) expiries in Redis.
**Why**:
Financial APIs strictly rate-limit free tiers. If three users request a report on `AAPL` within 10 minutes, querying Finnhub or NewsAPI three times would burn rate limits unnecessarily. 
**Trade-off**: The agents may occasionally reason over slightly stale news (e.g., 15 minutes old). For high-frequency trading, this is unacceptable. For swing-trading research, it is perfectly fine.

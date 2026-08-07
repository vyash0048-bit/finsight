# API Documentation Overview

FinSight's backend is powered by FastAPI, which automatically generates a complete OpenAPI (Swagger) specification. 

## Accessing the Interactive Docs
When the backend is running locally, you can view and test the complete API specification at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Core API Domains

The API is structured into several core domains using FastAPI routers.

### 1. Authentication (`/api/v1/auth`)
Handles user registration, login, and JWT token issuance.
- `POST /api/v1/auth/signup` - Register a new researcher account.
- `POST /api/v1/auth/login` - Authenticate and receive a JWT access token.
- `GET /api/v1/auth/me` - Retrieve the current authenticated user's profile.

### 2. Research & Agents (`/api/v1/research`)
The primary interface for interacting with the multi-agent swarm.
- `POST /api/v1/research/report` - Trigger a new research report for a given ticker (e.g., `{"ticker": "AAPL"}`). This kicks off the orchestrated debate and can take several minutes.
- `GET /api/v1/research/report/{ticker}` - Retrieve a cached or historical report for a ticker.
- `GET /api/v1/research/stream/{job_id}` - (Optional) Server-Sent Events (SSE) endpoint to stream agent thoughts and debate progress to the UI in real-time.

### 3. Market Data (`/api/v1/market`)
Provides access to normalized data from external providers (Yahoo Finance, Alpha Vantage).
- `GET /api/v1/market/price/{ticker}` - Retrieve latest OHLCV price bars.
- `GET /api/v1/market/technicals/{ticker}` - Retrieve pre-computed technical indicators (RSI, MACD) for the UI.

### 4. RAG / Documents (`/api/v1/documents`)
Interface for the Retrieval-Augmented Generation system.
- `POST /api/v1/documents/ingest` - Manually trigger ingestion and embedding of latest news and SEC filings for a given ticker.
- `GET /api/v1/documents/search` - Directly query the ChromaDB vector store (useful for debugging agent retrieval logic).

## Authentication Flow
Most endpoints (except login/signup) require an `Authorization: Bearer <token>` header. If a token is missing or expired, the API will return a `401 Unauthorized` response.

## Error Handling
The API follows standard HTTP status codes:
- `200 OK` - Success.
- `400 Bad Request` - Invalid input (e.g., unsupported ticker).
- `401 Unauthorized` - Missing or invalid JWT.
- `429 Too Many Requests` - Rate limit exceeded (protects external API quotas).
- `500 Internal Server Error` - Unexpected orchestration or database failure.

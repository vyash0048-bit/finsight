import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

import app.core.metrics as metrics  # noqa: F401 — registers Prometheus collectors
from app.api.endpoints import auth, documents, market, research

app = FastAPI(title="FinSight API", version="0.1.0")

# ---------------------------------------------------------------------------
# CORS — allow Streamlit frontend and local development origins
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# HTTP Metrics Middleware — records request count & duration for Prometheus
# ---------------------------------------------------------------------------
@app.middleware("http")
async def http_metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    endpoint = request.url.path
    method = request.method
    status = str(response.status_code)

    metrics.http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
    metrics.http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

    return response

# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to FinSight API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ---------------------------------------------------------------------------
# API Routers
# ---------------------------------------------------------------------------
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(research.router, prefix="/research", tags=["research"])
app.include_router(market.router, prefix="/market", tags=["market"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])

# ---------------------------------------------------------------------------
# Prometheus metrics ASGI sub-application
# ---------------------------------------------------------------------------
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

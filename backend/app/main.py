from fastapi import FastAPI

app = FastAPI(title="FinSight API", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to FinSight API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.api.endpoints import auth

app.include_router(auth.router, prefix="/auth", tags=["auth"])

from prometheus_client import make_asgi_app

import app.core.metrics as _metrics  # noqa: F401 — registers Prometheus collectors

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

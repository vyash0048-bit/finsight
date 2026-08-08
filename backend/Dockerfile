# Stage 1: Build & Dependencies
FROM python:3.12-slim as builder

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Use uv for extremely fast deterministic builds
RUN pip install uv && uv pip install --system --no-cache -r requirements.txt

# Stage 2: Production Runtime
FROM python:3.12-slim

WORKDIR /app

# Copy python dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source code
COPY . .

# Set env vars to not buffer logs and explicitly set PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Create a non-root user for security
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m finsight

USER finsight

EXPOSE 8000

# Health check is managed by Render via render.yaml healthCheckPath

CMD alembic upgrade head 2>&1 || echo "Migration skipped"; exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

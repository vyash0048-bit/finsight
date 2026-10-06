# Stage 1: Build & Dependencies
FROM python:3.12-slim as builder

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.docker.txt .

RUN pip install --no-cache-dir -r requirements.docker.txt

# Stage 2: Production Runtime
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user for security
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m finsight

# Copy python dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source code with proper ownership
COPY --chown=finsight:finsight . .

# Install any local wheel patches (avoids needing network in stage 2)
RUN pip install --no-cache-dir --no-deps .packages/*.whl 2>/dev/null || true

# Set env vars to not buffer logs and explicitly set PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

USER finsight

EXPOSE 8000

# Health check configured via docker-compose

CMD alembic upgrade head 2>&1 || echo "Migration skipped"; exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

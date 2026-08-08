#!/bin/sh
# Run Alembic migrations, then start the server
alembic upgrade head 2>&1 || echo "Migration skipped (DB may not be ready yet)"
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

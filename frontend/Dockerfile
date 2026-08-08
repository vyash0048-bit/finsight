FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8080

# Health check (relies on our /health endpoint)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Command to run the application using gunicorn
CMD gunicorn app:app -b 0.0.0.0:${PORT:-8080} -w 2 --access-logfile - --error-logfile -

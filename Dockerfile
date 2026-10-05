FROM python:3.12-slim

# Install system dependencies (e.g. for curl_cffi and building pandas)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the backend requirements first for caching
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Jinja2 explicitly for serving templates
RUN pip install --no-cache-dir jinja2

# Copy the entire project (backend and frontend)
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Set environment variables for Hugging Face Spaces
ENV PORT=7860
ENV ENV=production
ENV PYTHONPATH=/app/backend

# Note: In Hugging Face Spaces, you must configure secrets for GEMINI_API_KEY, DATABASE_URL, and MONGO_URL in the Spaces Settings UI.

EXPOSE 7860

# Run the FastAPI app via Uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]

#!/bin/bash
set -e

echo "Starting FinSight Backend locally (bypassing Docker networking issues)..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv || python -m venv .venv
fi

# Activate virtual environment (Git Bash / Windows)
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Set environment variables for local execution
export DATABASE_URL="postgresql://finsight_user:finsight_pass@localhost:5432/finsight_db"
export MONGO_URL="mongodb://localhost:27017"
export ENV="development"

# Load API key from root .env
if [ -f "../.env" ]; then
    echo "Loading .env file..."
    while IFS= read -r line || [ -n "$line" ]; do
        # Ignore comments and empty lines
        if [[ $line == \#* ]] || [[ -z "$line" ]]; then
            continue
        fi
        # Remove spaces around equals and quotes
        CLEANED=$(echo "$line" | sed -e 's/ *= */=/' -e 's/"//g' -e "s/'//g")
        export "$CLEANED"
    done < ../.env
fi

# Start the server
echo "Starting Uvicorn server on http://127.0.0.1:8000"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

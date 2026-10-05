$ErrorActionPreference = 'Stop'

Write-Host "Starting FinSight Backend locally (bypassing Docker networking issues)..."
cd backend

# Create virtual environment if it doesn't exist
if (!(Test-Path .venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing requirements..."
pip install -r requirements.txt

# Set environment variables for local execution
$env:DATABASE_URL="postgresql://finsight_user:finsight_pass@localhost:5432/finsight_db"
$env:MONGO_URL="mongodb://localhost:27017"
$env:ENV="development"

# Load API key from root .env
if (Test-Path ../.env) {
    Write-Host "Loading .env file..."
    Get-Content ../.env | ForEach-Object {
        if ($_ -match '^(.*?)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim(' ', '"', "'")
            Set-Item -Path env:\$name -Value $value
        }
    }
}

# Start the server
Write-Host "Starting Uvicorn server on http://127.0.0.1:8000"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

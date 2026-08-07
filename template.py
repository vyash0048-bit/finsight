import os
from pathlib import Path

# Base directory for the project. Set to '.' to create in the current directory.
BASE_DIR = "."

# List of all files to be created
files = [
    "backend/app/main.py",
    "backend/app/core/config.py",
    "backend/app/core/security.py",
    "backend/app/core/logging.py",
    "backend/app/core/exceptions.py",
    "backend/app/api/deps.py",
    "backend/app/api/v1/routers/auth.py",
    "backend/app/api/v1/routers/reports.py",
    "backend/app/api/v1/routers/portfolios.py",
    "backend/app/api/v1/routers/watchlist.py",
    "backend/app/api/v1/routers/health.py",
    "backend/app/api/v1/__init__.py",
    "backend/app/agents/base.py",
    "backend/app/agents/supervisor.py",
    "backend/app/agents/news_agent.py",
    "backend/app/agents/technical_agent.py",
    "backend/app/agents/fundamental_agent.py",
    "backend/app/agents/macro_agent.py",
    "backend/app/agents/risk_agent.py",
    "backend/app/agents/portfolio_agent.py",
    "backend/app/agents/memory_agent.py",
    "backend/app/agents/debate_agent.py",
    "backend/app/agents/report_agent.py",
    "backend/app/services/market_data_service.py",
    "backend/app/services/news_service.py",
    "backend/app/services/fundamentals_service.py",
    "backend/app/services/macro_service.py",
    "backend/app/services/rag_service.py",
    "backend/app/services/report_service.py",
    "backend/app/services/llm_client.py",
    "backend/app/repositories/mongo_repo.py",
    "backend/app/repositories/postgres_repo.py",
    "backend/app/repositories/vector_repo.py",
    "backend/app/schemas/report.py",
    "backend/app/schemas/user.py",
    "backend/app/schemas/portfolio.py",
    "backend/app/schemas/agent_io.py",
    "backend/app/models/user.py",
    "backend/app/models/portfolio.py",
    "backend/app/models/price_bar.py",
    "backend/app/orchestration/orchestrator.py",
    "backend/app/orchestration/graph.py",
    "backend/app/tasks/ingestion_jobs.py",
    "backend/app/tasks/worker.py",
    "backend/pyproject.toml",
    "backend/requirements.txt",
    "backend/Dockerfile",
    "frontend/streamlit_app/Home.py",
    "frontend/streamlit_app/pages/1_Dashboard.py",
    "frontend/streamlit_app/pages/2_Portfolio.py",
    "frontend/streamlit_app/pages/3_Watchlist.py",
    "frontend/streamlit_app/pages/4_Reports.py",
    "frontend/streamlit_app/pages/5_Settings.py",
    "frontend/requirements.txt",
    "frontend/Dockerfile",
    "infra/docker-compose.yml",
    "infra/docker-compose.prod.yml",
    "mlops/eval/prompt_regression_tests.py",
    "scripts/seed_db.py",
    "scripts/run_ingestion.py",
    "docs/architecture.md",
    "docs/api.md",
    ".github/workflows/ci.yml",
    ".github/workflows/deploy.yml",
    ".env.example",
    "README.md",
    "PROJECT_GUIDE.md"
]

# List of empty directories to be created
directories = [
    "backend/app/agents/prompts",
    "backend/tests/unit",
    "backend/tests/integration",
    "backend/tests/agents",
    "backend/alembic",
    "frontend/streamlit_app/components",
    "infra/k8s",
    "mlops/mlflow",
    "mlops/eval/golden_datasets",
    "docs/diagrams"
]

def create_structure():
    print(f"Creating project structure in: {os.path.abspath(BASE_DIR)}")
    
    # Create standalone directories
    for dir_path in directories:
        full_dir_path = os.path.join(BASE_DIR, dir_path)
        os.makedirs(full_dir_path, exist_ok=True)
        print(f"Created directory: {full_dir_path}")
        
    # Create directories for files and the files themselves
    for file_path in files:
        full_file_path = os.path.join(BASE_DIR, file_path)
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        Path(full_file_path).touch()
        print(f"Created file: {full_file_path}")

if __name__ == '__main__':
    create_structure()
    print("Project structure created successfully!")

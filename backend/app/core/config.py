import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinSight"
    VERSION: str = "0.1.0"
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "finsight_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "finsight_pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "finsight_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

settings = Settings()

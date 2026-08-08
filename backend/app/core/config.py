from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "FinSight"
    VERSION: str = "0.1.0"

    SECRET_KEY: str = "super-secret-key-for-local-dev-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: str = "finsight_user"
    POSTGRES_PASSWORD: str = "finsight_pass"
    POSTGRES_DB: str = "finsight_db"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"

    DATABASE_URL: str = ""

    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB: str = "finsight_mongo"

    REDIS_URL: str = "redis://localhost:6379/0"

    GEMINI_API_KEY: str = ""

    @model_validator(mode="after")
    def assemble_database_url(self) -> "Settings":
        """Build DATABASE_URL from individual Postgres fields if not explicitly set."""
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        return self


settings = Settings()

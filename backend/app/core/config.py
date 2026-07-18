import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Volti Backend API"
    API_V1_STR: str = "/api"
    
    # Database Settings
    DB_HOST: str = os.getenv("VOLTI_DB_HOST", "localhost")
    DB_PORT: str = os.getenv("VOLTI_DB_PORT", "5432")
    DB_NAME: str = os.getenv("VOLTI_DB_NAME", "volti_db")
    DB_USER: str = os.getenv("VOLTI_DB_USER", "postgres")
    DB_PASS: str = os.getenv("VOLTI_DB_PASS", "password")
    
    @property
    def DATABASE_URL(self) -> str:
        # Support direct environment variable override (e.g. Heroku/Docker)
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
            
        # Build PostgreSQL URL if custom credentials or host are set
        # Otherwise, fall back to SQLite to make it run out-of-the-box locally.
        if os.getenv("VOLTI_DB_HOST") or os.getenv("VOLTI_DB_PASS"):
            return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        # SQLite local fallback
        return "sqlite:///volti.db"

settings = Settings()

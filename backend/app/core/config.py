import os

# Load environment variables from .env file if it exists in the backend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Volti Backend API"
    API_V1_STR: str = "/api/v1"
    
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
            
        # Default to PostgreSQL database connection URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

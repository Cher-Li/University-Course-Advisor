# env vars 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Academic Advisor"
    DATABASE_URL: str = "postgresql://postgres:devpass@localhost:5432/advisor"

    class Config:
        env_file = ".env"

settings = Settings()
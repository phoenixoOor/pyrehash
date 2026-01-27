import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "pyrehash"
    DATABASE_URL: str = "sqlite:///./data/pyrehash.db"
    DICTIONARY_DIR: str = "data/dictionaries"
    RESULTS_DIR: str = "data/results"
    MAX_WORKERS: int = os.cpu_count() or 4
    
    # HIBP Integration
    HIBP_API_KEY: str = os.getenv("HIBP_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@db:5432/urlshortener")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()
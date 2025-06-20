from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_V1_STR: str
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[str]
    DEFAULT_PAGE_SIZE: int
    MAX_PAGE_SIZE: int
    CACHE_EXPIRE_SECONDS: int

settings = Settings()

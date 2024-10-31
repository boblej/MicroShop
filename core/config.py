from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_name: str
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: str = "5432"

    class Config:
        env_file = ".env"

settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
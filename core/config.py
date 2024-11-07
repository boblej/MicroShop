from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class DbSettings(BaseSettings):
    user: str
    name: str
    password: str
    host: str = "localhost"
    port: str = "5432"

    class Config:
        env_prefix = "DB_"

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()

    class Config:
        env_file = ".env"

settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"

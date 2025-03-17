from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

class AppConfig(BaseSettings):
    APP_NAME: str = "DefaultAppName"
    DEBUG: bool = True

    JWT_SECRET: str = "default_jwt_secret"

    DATABASE_URL: str 
    MESSAGE_BROKER_URL: str

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

config = AppConfig()


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.DATABASE_URL,
        isolation_level="REPEATABLE READ"
    )
)
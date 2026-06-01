from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DBBaseModel = declarative_base()

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = (
        f"postgresql+asyncpg://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'password')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'bd_backend')}"
    )
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'fallback-inseguro')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))

    class Config:
        case_sensitive = True

settings = Settings()

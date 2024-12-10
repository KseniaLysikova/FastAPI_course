from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseSettings):
    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_ADDR: str = "db"
    DB_PORT: int = 5432

    JWT_SECRET: str = os.getenv('JWT_SECRET')
    JWT_ACCESS_EXPIRE: int = os.getenv('JWT_ACCESS_EXPIRE')
    JWT_REFRESH_EXPIRE: int = os.getenv('JWT_REFRESH_EXPIRE')


settings = Settings()

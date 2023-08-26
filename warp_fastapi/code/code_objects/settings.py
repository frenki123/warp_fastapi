from ..config import NameConfig
from .base import SimpleModuleCode


class SettingsModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig):
        self.folder = ''
        self.filename = config.settings_file

    def __str__(self) -> str:
        return """
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    API_V1_STRING:str = "/api/v1"
    SECRET_KEY:str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URL:str = "sqlite:///./database.db"
    PROJECT_NAME:str = "Book REST API"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []



settings = Settings()

"""

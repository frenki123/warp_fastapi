from ..config import NameConfig
from .base import SimpleModuleCode


class SettingsModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig, project_name: str):
        self.folder = config.get_settings_folder()
        self.filename = config.get_settings_filename()
        self.project_name = project_name

    def __str__(self) -> str:
        return f"""
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    API_V1_STRING:str = "/api/v1"
    SECRET_KEY:str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URL:str = ""
    PROJECT_NAME:str = '{self.project_name}'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []



settings = Settings()

"""

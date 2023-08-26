from warp_fastapi.code.code_objects.settings import SettingsModuleCode
from warp_fastapi.code.config import NameConfig

from .conftest import assert_code_lines


def test_settings_module():
    config = NameConfig()
    m = SettingsModuleCode(config)
    r = """
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
    assert_code_lines(m, r)

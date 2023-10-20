from warp_fastapi.code.code_objects.settings import SettingsModuleCode
from warp_fastapi.config import NameConfig

from .conftest import assert_code_lines


def test_settings_module():
    config = NameConfig()
    m = SettingsModuleCode(config, 'NEW_PROJECT_NAME')
    r = """
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, SecretStr
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    API_V1_STRING:str = "/api/v1"
    SECRET_KEY:SecretStr = SecretStr(secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URL:str = ""
    PROJECT_NAME:str = 'NEW_PROJECT_NAME'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALGORITHM:str = "HS256"
settings = Settings()
"""
    assert_code_lines(m, r)

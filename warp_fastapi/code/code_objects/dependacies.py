from ...main import AuthObject
from ..config import NameConfig
from .base import SimpleModuleCode


class DependanciesModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig, auth_obj: AuthObject | None = None):
        self.folder = config.get_dependency_folder()
        self.filename = config.get_dependency_filename()
        self.db_module = config.get_module_for_dependency(config.get_database_path())
        self.auth_code = self._get_auth_code(auth_obj)
        self.security_import_string = self._get_sec_import_string(auth_obj, config)

    def __str__(self) -> str:
        return f"""
from typing import Any
from {self.db_module} import SessionLocal
{self.security_import_string}


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

{self.auth_code}
"""

    @staticmethod
    def _get_auth_code(auth_obj: AuthObject | None) -> str:
        if not auth_obj:
            return ''
        serv_func = f'get_{auth_obj.name}_service'
        return f"""
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def get_token_data(token: str = Depends(oauth2)):
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data

def get_current_user(
    token: TokenPayload = Depends(get_token_data),
    db: Session = Depends(get_db),
):
    {auth_obj.name}_service = {serv_func}(db)
    {auth_obj.name} = {auth_obj.name}_service.get_{auth_obj.name}(id=token.{auth_obj.name}_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""

    @staticmethod
    def _get_sec_import_string(auth_obj: AuthObject | None, config: NameConfig) -> str:
        if not auth_obj:
            return ''
        settings_module = config.get_module_for_dependency(config.get_settings_path())
        model_module = config.get_module_for_dependency(config.get_model_path(auth_obj))
        auth_class = auth_obj.class_name
        service_module = config.get_module_for_dependency(config.get_service_path(auth_obj))
        schema_module = config.get_module_for_dependency(config.get_common_schema_path())
        service_func = f'get_{auth_obj.name}_service'
        return f"""
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from {settings_module} import settings
from {schema_module} import TokenPayload

from {model_module} import {auth_class}
from {service_module} import {service_func}
"""

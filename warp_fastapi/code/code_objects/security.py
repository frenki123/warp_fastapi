from ... import AuthObject
from ...config import StructureConfig
from .base import SimpleModuleCode


class SecurityModuleCode(SimpleModuleCode):
    def __init__(self, auth_obj: AuthObject, config: StructureConfig):
        self.folder = config.get_security_folder()
        self.filename = config.get_security_filename()
        self.settings_module = config.get_module_for_security(config.get_settings_path())
        self.model_module = config.get_module_for_security(config.get_model_path(auth_obj))
        self.auth_class = auth_obj.class_name
        self.service_module = config.get_module_for_security(config.get_service_path(auth_obj))
        self.service_func = f'get_{auth_obj.name}_service'
        self.auth_name = auth_obj.name

    def __str__(self) -> str:
        return f"""
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import EmailStr
from {self.settings_module} import settings
from {self.model_module} import {self.auth_class}
from {self.service_module} import {self.service_func}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token({self.auth_name}: {self.auth_class}) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
       {{"exp": expire, "{self.auth_name}_id": str({self.auth_name}.id)}},
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate(
    db: Session, username: str, password: str) -> {self.auth_class} | None:
    {self.auth_name}_service = {self.service_func}(db)
    {self.auth_name} = {self.auth_name}_service.search_{self.auth_name}(attribute='username',
    value=username, sort=None, skip=0, limit=1)
    if {self.auth_name}:
        if is_valid_password(password, {self.auth_name}[0].password):
            return {self.auth_name}[0]
    return None
"""

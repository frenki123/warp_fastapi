from ...main import AppObject
from ..config import NameConfig
from .base import SimpleModuleCode


class DatabaseModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig):
        self.folder = ''
        self.filename = config.database_file
        self.settings_filename = config.settings_file

    def __str__(self) -> str:
        return f"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from .{self.settings_filename} import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={{"check_same_thread": False}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
"""


class BaseModuleCode(SimpleModuleCode):
    def __init__(self, objects: list[AppObject], config: NameConfig):
        self.folder = ''
        self.filename = config.base_file
        self.database = config.database_file
        code_lines: list[str] = []
        for obj in objects:
            code_line = f'from .{config.model_folder}.{obj.name}{config.model_extension} import {obj.class_name} # noqa'
            code_lines.append(code_line)
        self.models_code = '\n'.join(code_lines)

    def __str__(self) -> str:
        return f"""from .{self.database} import Base # noqa
{self.models_code}
"""

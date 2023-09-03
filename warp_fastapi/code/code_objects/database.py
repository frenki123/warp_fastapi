from ...main import AppObject
from ..config import NameConfig
from .base import SimpleModuleCode


class DatabaseModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig):
        self.folder = config.get_database_folder()
        self.filename = config.get_database_filename()
        self.settings_module = config.get_module_for_database(config.get_settings_path())

    def __str__(self) -> str:
        return f"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from {self.settings_module} import settings

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
        self.folder = config.get_base_folder()
        self.filename = config.get_base_filename()
        self.database_module = config.get_module_for_base(config.get_database_path())
        code_lines: list[str] = []
        for obj in objects:
            code_line = (
                f'from {config.get_module_for_base(config.get_model_path(obj))} import {obj.class_name} # noqa'
            )
            code_lines.append(code_line)
        self.models_code = '\n'.join(code_lines)

    def __str__(self) -> str:
        return f"""from {self.database_module} import Base # noqa
{self.models_code}
"""

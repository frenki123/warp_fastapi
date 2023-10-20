from warp_fastapi import AppObject
from warp_fastapi.code.code_objects.database import BaseModuleCode, DatabaseModuleCode
from warp_fastapi.config import NameConfig

from .conftest import assert_code_lines


def test_db_module():
    config = NameConfig()
    config.settings_file = 'test_settings'
    m = DatabaseModuleCode(config)
    r = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from .test_settings import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
"""
    assert_code_lines(m, r)


def test_base_db_module(app_objs: list[AppObject]):
    config = NameConfig()
    m = BaseModuleCode(app_objs, config)
    r = """from .database import Base # noqa
from .models.obj1_model import Obj1 # noqa
from .models.obj2_model import Obj2 # noqa"""
    assert_code_lines(m, r)

from warp_fastapi.code.code_objects.dependacies import DependanciesModuleCode
from warp_fastapi.config import NameConfig

from .conftest import assert_code_lines


def test_dep_module():
    config = NameConfig()
    m = DependanciesModuleCode(config)
    r = """
from typing import Any
from .database import SessionLocal
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
"""
    assert_code_lines(m, r)

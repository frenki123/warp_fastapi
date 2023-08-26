from ..config import NameConfig
from .base import SimpleModuleCode


class DependanciesModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig):
        self.folder = ''
        self.filename = config.dependency_file
        self.db_file = config.database_file

    def __str__(self) -> str:
        return f"""
from .{self.db_file} import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

"""

from ..config import NameConfig
from .base import SimpleModuleCode


class DependanciesModuleCode(SimpleModuleCode):
    def __init__(self, config: NameConfig):
        self.folder = config.get_dependency_folder()
        self.filename = config.get_dependency_filename()
        self.db_module = config.get_module_for_dependency(config.get_database_path())

    def __str__(self) -> str:
        return f"""
from {self.db_module} import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

"""

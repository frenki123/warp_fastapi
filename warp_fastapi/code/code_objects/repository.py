from ... import AppObject
from ...config import StructureConfig
from .base import (
    AbstractModuleCode,
    SimpleClassCode,
    SimpleFunctionCode,
    SimpleModuleCode,
    SimpleVariable,
)


class RepoModuleCode(AbstractModuleCode):
    def __init__(self, app_obj: AppObject, config: StructureConfig):
        self.type_checking_imports = {}
        self.classes = []
        self.functions = []
        self.variables = []
        self.config = config
        self.folder = config.get_repository_folder(app_obj)
        self.filename = config.get_repository_filename(app_obj)
        main_repo_module = config.get_module_for_repository(app_obj, config.get_repository_main_path())
        model_module = config.get_module_for_repository(app_obj, config.get_model_path(app_obj))
        self.imports = {
            'sqlalchemy.orm': {'Session'},
            main_repo_module: {config.repository_main_class_name},
            model_module: {app_obj.class_name},
        }
        class_name = config.get_repo_classname(app_obj)
        init_function = SimpleFunctionCode(
            '__init__',
            f'super().__init__(db, {app_obj.class_name})',
            parametars=[SimpleVariable('self'), SimpleVariable('db', 'Session')],
        )
        self.classes.append(SimpleClassCode(class_name, config.repository_main_class_name, methods=[init_function]))

    def __str__(self) -> str:
        return f"""
{self.imports_code}
{self.classes_code}
""".strip(
            '\n'
        )


class RepoBaseModule(SimpleModuleCode):
    def __init__(self, config: StructureConfig):
        self.folder = config.get_repository_main_folder()
        self.filename = config.get_repository_main_filename()
        self.database_module = config.get_module_for_repository_main(config.get_database_path())

    def __str__(self) -> str:
        return f"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from {self.database_module} import Base
from typing import Type, Dict, Any, Optional, TypeVar
from fastapi import HTTPException

class Repository:
    def __init__(self, db: Session, model_type: type[Base]):
        self.db = db
        self.model_type = model_type

    def get_by_id(self, id: int):
        db_obj = self.db.get(self.model_type, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{{self.model_type.__name__}} with ID {{id}} not found!")
        return db_obj

    def get_all(self, skip: int, limit: int):
        return self.db.scalars(select(self.model_type).offset(skip).limit(limit)).all()

    def get_by_ids(self, ids:list[int]):
        results = self.db.query(self.model_type).filter(self.model_type.id.in_(ids)).all()
        if len(results) != len(ids):
            raise HTTPException(status_code=400,
            detail=(f'{{len(ids)-len(results)}} ids not '
                    f'found for {{self.model_type.__name__}}!'))
        return results

    def create(self, data: dict[str, Any]):
        instance = self.model_type(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, data: dict[str, Any]):
        instance = self.get_by_id(id)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{{self.model_type.__name__}} with ID {{id}} not found!")
        for key, value in data.items():
            setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def edit(self, id: int, data: dict[str, Any]):
        instance = self.get_by_id(id)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{{self.model_type.__name__}} with ID {{id}} not found!")

        for key, value in data.items():
            if value:
                if isinstance(getattr(instance, key), list) and isinstance(value, list):
                    for val in value:
                        getattr(instance, key).append(val)
                else:
                    setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int):
        instance = self.get_by_id(id)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{{self.model_type.__name__}} with ID {{id}} not found!")

        self.db.delete(instance)
        self.db.commit()
        return True

    def search(self, attribute: str | None, value: str | None, sort: str | None, skip: int, limit: int):
        columns = self.model_type.__table__.columns.keys()
        statement = select(self.model_type)
        if attribute and value:
            if attribute not in columns:
                raise HTTPException(status_code=406,
                detail=(f"Attribute {{attribute}} in "
                    f"{{self.model_type.__name__}} not found!"))
            statement = statement.filter_by(**{{attribute: value}})
        if sort in columns:
            statement = statement.order_by(sort)
        return self.db.scalars(statement.offset(skip).limit(limit)).all()
"""

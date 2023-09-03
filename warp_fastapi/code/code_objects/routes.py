from ...main import AppObject
from ..config import NameConfig
from .base import (
    SimpleModuleCode,
)


class RoutesModuleCode(SimpleModuleCode):
    def __init__(self, app_obj: AppObject, config: NameConfig = NameConfig()):
        self.folder = config.get_route_folder(app_obj)
        self.filename = config.get_route_filename(app_obj)
        self.name = app_obj.name
        self.class_name = app_obj.class_name
        self.response_schema = config.get_read_cls_schema(app_obj)
        self.create_schema = config.get_create_cls_schema(app_obj)
        self.edit_schema = config.get_edit_cls_schema(app_obj)
        self.service = config.get_service_classname(app_obj)
        self.route_name = app_obj.route_name
        self.dependency_module = config.get_module_for_route(app_obj, config.get_dependency_path())
        self.schema_modul = config.get_module_for_route(app_obj, config.get_schema_path(app_obj))
        self.repo_modul = config.get_module_for_route(app_obj, config.get_repository_path(app_obj))
        self.repo_class = config.get_repo_classname(app_obj)
        self.service_modul = config.get_module_for_route(app_obj, config.get_service_path(app_obj))
        self.common_schema_module = config.get_module_for_route(app_obj, config.get_common_schema_path())

    def __str__(self) -> str:
        return f"""from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from {self.dependency_module} import authorize, get_db
from {self.schema_modul} import {self.response_schema}, {self.create_schema}, {self.edit_schema}
from {self.repo_modul} import {self.repo_class}
from {self.service_modul} import {self.service}, get_{self.name}_service
from {self.common_schema_module} import QuerySchema

router = APIRouter(prefix="/{self.route_name}", tags=['{self.name}'])

@router.post("/", response_model={self.response_schema}, status_code=201)
def create_{self.name}({self.name}: {self.create_schema},
                  db: Annotated[Session, Depends(get_db)]):
    service = get_{self.name}_service(db)
    return service.create_{self.name}({self.name})

@router.get("/{{id}}", response_model={self.response_schema}, status_code=200)
def read_{self.name}(id: int,
                db: Annotated[Session, Depends(get_db)]):
    service = get_{self.name}_service(db)
    return service.get_{self.name}(id)

@router.get("/", response_model=list[{self.response_schema}], status_code=200)
def get_all_{self.name}(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0, limit: int = 100,):
    service = get_{self.name}_service(db)
    return service.search_{self.name}(None, None, None, skip, limit)

@router.get("/search", response_model=list[{self.response_schema}], status_code=200)
def search_{self.name}(
    q: Annotated[QuerySchema, Depends(QuerySchema)],
    db: Annotated[Session, Depends(get_db)]):
    service = get_{self.name}_service(db)
    return service.search_{self.name}(**q.model_dump())

@router.put("/{{id}}", response_model={self.response_schema}, status_code=200)
def update_{self.name}(
    id: int, {self.name}: {self.create_schema},
    db: Annotated[Session, Depends(get_db)]):
    service = get_{self.name}_service(db)
    return service.update_{self.name}(id, {self.name})

@router.patch("/{{id}}", response_model={self.response_schema}, status_code=200)
def edit_{self.name}(
    id: int, {self.name}: {self.edit_schema},
    db: Annotated[Session, Depends(get_db)]):
    service = get_{self.name}_service(db)
    return service.edit_{self.name}(id, {self.name})

@router.delete("/{{id}}", status_code=200)
def delete_{self.name}(
    id: int,
    db: Annotated[Session, Depends(get_db)]):
    service = get_{self.name}_service(db)
    service.delete_{self.name}(id)
    return JSONResponse(content={{"message":"Resource successfully deleted."}})
"""


class MainRouterCode(SimpleModuleCode):
    def __init__(self, app_objects: list[AppObject], config: NameConfig = NameConfig()):
        self.folder = config.get_main_route_folder()
        self.filename = config.get_main_route_filename()
        self.routes: list[str] = []
        self.fill_routes(app_objects, config)

    def fill_routes(self, app_objects: list[AppObject], config: NameConfig) -> None:
        for obj in app_objects:
            self.routes.append(config.get_route_filename(obj))

    @property
    def all_routes_code(self) -> str:
        code_lines: list[str] = []
        for route in self.routes:
            code = f'router.include_router({route}.router)'
            code_lines.append(code)
        return '\n'.join(code_lines)

    def __str__(self) -> str:
        return f"""from fastapi import APIRouter
from . import {', '.join(self.routes)}

router = APIRouter()

{self.all_routes_code}
"""

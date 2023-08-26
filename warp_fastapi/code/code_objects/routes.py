from ...main import AppObject
from ..config import NameConfig
from .base import (
    SimpleModuleCode,
)


class RoutesModuleCode(SimpleModuleCode):
    def __init__(self, app_obj: AppObject, config: NameConfig = NameConfig()):
        self.folder = config.route_folder
        self.filename = app_obj.name + config.route_extension
        self.name = app_obj.name
        self.class_name = app_obj.class_name
        self.response_schema = config.read_schema(app_obj)
        self.create_schema = config.create_schema(app_obj)
        self.edit_schema = config.edit_schema(app_obj)
        self.service = config.service_class(app_obj)
        self.route_name = app_obj.route_name
        self.dependency_file = config.dependency_file
        self.schema_modul = config.schema_module(app_obj)
        self.repo_modul = config.repo_module(app_obj)
        self.repo_class = config.repo_class(app_obj)
        self.service_modul = config.service_module(app_obj)
        self.common_schema = config.common_schema_module()

    def __str__(self) -> str:
        return f"""from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from ..{self.dependency_file} import authorize, get_db
from ..{self.schema_modul} import {self.response_schema}, {self.create_schema}, {self.edit_schema}
from ..{self.repo_modul} import {self.repo_class}
from ..{self.service_modul} import {self.service}, get_{self.name}_service
from ..{self.common_schema} import QuerySchema

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
        self.folder = config.route_folder
        self.filename = config.main_route_filename
        self.routes: list[str] = []
        self.fill_routes(app_objects, config)

    def fill_routes(self, app_objects: list[AppObject], config: NameConfig) -> None:
        for obj in app_objects:
            self.routes.append(f'{obj.name}{config.route_extension}')

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

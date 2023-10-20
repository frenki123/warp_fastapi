from warp_fastapi import AppObject
from warp_fastapi.code.code_objects.routes import MainRouterCode, RoutesModuleCode
from warp_fastapi.config import NameConfig

from .conftest import assert_code_lines


def test_routes_code(app_obj: AppObject):
    config = NameConfig()
    m = RoutesModuleCode(app_obj, config)
    print(m)
    r = (
        """
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from ..dependancies import get_db, get_current_user
from ..schemas.app_schema import AppResponse, AppCreate, AppEdit
from ..repository.app_repository import AppRepository
from ..services.app_service import AppService, get_app_service
from ..schemas.common_schema import QuerySchema

router = APIRouter(prefix="/apps", tags=['app'])
@router.post("/", response_model=AppResponse, status_code=201)
def create_app(app: AppCreate,
                  db: Annotated[Session, Depends(get_db)]):
    service = get_app_service(db)
"""
        + '    \n'
        + """    return service.create_app(app)
@router.get("/{id}", response_model=AppResponse, status_code=200)
def read_app(id: int,
                db: Annotated[Session, Depends(get_db)]):
    service = get_app_service(db)
    return service.get_app(id)

@router.get("/", response_model=list[AppResponse], status_code=200)
def get_all_app(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0, limit: int = 100,):
    service = get_app_service(db)
    return service.search_app(None, None, None, skip, limit)

@router.get("/search/", response_model=list[AppResponse], status_code=200)
def search_app(
    q: Annotated[QuerySchema, Depends(QuerySchema)],
    db: Annotated[Session, Depends(get_db)]):
    service = get_app_service(db)
    return service.search_app(**q.model_dump())

@router.put("/{id}", response_model=AppResponse, status_code=200)
def update_app(
    id: int, app: AppCreate,
    db: Annotated[Session, Depends(get_db)]):
    service = get_app_service(db)
    return service.update_app(id, app)

@router.patch("/{id}", response_model=AppResponse, status_code=200)
def edit_app(
    id: int, app: AppEdit,
    db: Annotated[Session, Depends(get_db)]):
    service = get_app_service(db)
    return service.edit_app(id, app)

@router.delete("/{id}", status_code=200)
def delete_app(
    id: int,
    db: Annotated[Session, Depends(get_db)]):
    service = get_app_service(db)
    service.delete_app(id)
    return JSONResponse(content={"message":"Resource successfully deleted."})
"""
    )
    assert_code_lines(m, r)


def test_main_router(app_objs: list[AppObject]):
    config = NameConfig()
    m = MainRouterCode(app_objs, config)
    print(m)
    r = """
from fastapi import APIRouter
from . import obj1_route, obj2_route

router = APIRouter()

router.include_router(obj1_route.router)
router.include_router(obj2_route.router)
"""
    assert_code_lines(m, r)

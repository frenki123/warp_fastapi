from warp_fastapi import AppObject
from warp_fastapi.code.code_objects.service import ServiceModuleCode
from warp_fastapi.code.config import NameConfig

from .conftest import assert_code_lines


def test_simple_service(app_obj: AppObject):
    m = ServiceModuleCode(app_obj, NameConfig())
    r = """
from ..schemas.app_schema import AppCreate, AppDatabase, AppEdit, AppResponse
from ..repository.app_repository import AppRepository
from sqlalchemy.orm import Session
class AppService:
    def __init__(self, repository: AppRepository):
        self.repository = repository
    def get_app(self, id: int):
        return self.repository.get_by_id(id)
    def create_app(self, app: AppCreate):
        app_data = app.model_dump()
        db_app = self.repository.create(app_data)
        return db_app
    def update_app(self, id: int, app: AppCreate):
        app_data = app.model_dump()
        db_app = self.repository.update(id, app_data)
        return db_app
    def edit_app(self, id: int, app: AppEdit):
        app_data = app.model_dump()
        db_app = self.repository.edit(id, app_data)
        return db_app
    def delete_app(self, id: int):
        return self.repository.delete(id)
    def search_app(self, attribute: str|None, value: str|None, sort: str|None, skip: int, limit: int):
        db_results = self.repository.search(attribute, value, sort, skip, limit)
        return db_results
def get_app_service(db: Session):
    return AppService(AppRepository(db))
"""
    assert_code_lines(m, r)


# noqa: E501
def test_complex_service(app_objs_with_rel: tuple[AppObject, AppObject]):
    obj = app_objs_with_rel[0]
    m = ServiceModuleCode(obj, NameConfig())
    return_service_line = (
        'return Object1Service(Object1Repository(db), '
        'object2_repository=Object2Repository(db), '
        'object3_repository=Object3Repository(db), '
        'object4_repository=Object4Repository(db))'
    )
    r = (
        f"""
from ..schemas.object1_schema import Object1Create, Object1Database, Object1Edit, Object1Response
from ..repository.object1_repository import Object1Repository
from sqlalchemy.orm import Session
from ..repository.object2_repository import Object2Repository
from ..schemas.object2_schema import Object2Response
from ..repository.object3_repository import Object3Repository
from ..schemas.object3_schema import Object3Response
from ..repository.object4_repository import Object4Repository
from ..schemas.object4_schema import Object4Response
class Object1Service:
    def __init__(self, repository: Object1Repository, object2_repository: Object2Repository, """
        f"""object3_repository: Object3Repository, object4_repository: Object4Repository):
        self.repository = repository
        self.object2_repository = object2_repository
        self.object3_repository = object3_repository
        self.object4_repository = object4_repository
    def _get_id_data(self, object1: Object1Create|Object1Edit):
        rel1: list[Object2Response] = []
        rel2: Object3Response|None = None
        rel3: list[Object4Response] = []
        if object1.rel1_id:
            rel1 = self.object2_repository.get_by_ids(object1.rel1_id)
        if object1.rel2_id:
            rel2 = self.object3_repository.get_by_id(object1.rel2_id)
        if object1.rel3_id:
            rel3 = self.object4_repository.get_by_ids(object1.rel3_id)
        return rel1, rel2, rel3
    def _prepare_db_data(self, object1: Object1Create|Object1Edit):
        rel1, rel2, rel3 = self._get_id_data(object1)
        id_data = {{'rel1':rel1, 'rel2':rel2, 'rel3':rel3}}
        data = object1.model_dump(exclude_unset=True,exclude={{"rel1_id", "rel2_id", "rel3_id"}})
        data.update(id_data)
        return data
    def get_object1(self, id: int):
        return self.repository.get_by_id(id)
    def create_object1(self, object1: Object1Create):
        object1_data = self._prepare_db_data(object1)
        db_object1 = self.repository.create(object1_data)
        return db_object1
    def update_object1(self, id: int, object1: Object1Create):
        object1_data = self._prepare_db_data(object1)
        db_object1 = self.repository.update(id, object1_data)
        return db_object1
    def edit_object1(self, id: int, object1: Object1Edit):
        object1_data = self._prepare_db_data(object1)
        db_object1 = self.repository.edit(id, object1_data)
        return db_object1
    def delete_object1(self, id: int):
        return self.repository.delete(id)
    def search_object1(self, attribute: str|None, value: str|None, sort: str|None, skip: int, limit: int):
        db_results = self.repository.search(attribute, value, sort, skip, limit)
        return db_results
def get_object1_service(db: Session):
    {return_service_line}
"""
    )
    print(m)
    assert_code_lines(m, r)

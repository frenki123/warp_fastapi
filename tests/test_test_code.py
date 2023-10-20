from warp_fastapi import AppObject, Attribute
from warp_fastapi.code.code_objects.tests import ConfTestModuleCode, TestModuleCode as TModuleCode
from warp_fastapi.config import StructureConfig

from .conftest import assert_code_lines


def test_conftest_code(app_objs_with_rel: tuple[AppObject, AppObject]):
    m = ConfTestModuleCode(list(app_objs_with_rel), StructureConfig())
    r = """
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.base import Base
from app.dependancies import get_current_user, get_db
from app.main import app
@pytest.fixture
def base_client():
    TEST_DB = "sqlite://"
    engine = create_engine(
        TEST_DB,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return app
@pytest.fixture
def client(base_client: FastAPI):
    with TestClient(base_client) as c:
        yield c
@pytest.fixture
def get_object1() -> dict[str,str|int]:
    return {"name": "name", "desc": "desc", "date": "2020-11-20", "time": "07:44", "rel2_id": "1"}
@pytest.fixture
def get_object4() -> dict[str,str|int]:
    return {"name": "name", "desc": "desc"}
"""
    assert_code_lines(m, r)


def test_tmodule_code(app_objs_with_rel: tuple[AppObject, AppObject], complex_int_att: Attribute):
    obj1 = app_objs_with_rel[0]
    obj1.add_attributes(complex_int_att)
    obj2 = app_objs_with_rel[1]
    m = TModuleCode([obj1, obj2], StructureConfig())
    r = (
        """
import pytest
from fastapi.testclient import TestClient
from app.security import is_valid_password
def test_object1(client: TestClient, get_object1: dict[str,str|int], """
        """get_object3: dict[str,str|int], get_object4: dict[str,str|int]):
    client.post('/api/v1/object3s',json=get_object3)
    client.post('/api/v1/object4s',json=get_object4)
    response = client.post('/api/v1/object1s',json=get_object1)
    assert response.status_code == 201, response.text
    data = response.json()
    assert "id" in data
    id = data["id"]
    assert data['name'] == 'name'
    assert data['desc'] == 'desc'
    assert data['date'] == '2020-11-20'
    assert data['time'] == '07:44'
    assert data['att'] == 1
    assert data['rel2_id'] == 1
    response = client.get(f"/api/v1/object1s/{id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == id
    assert data['name'] == 'name'
    assert data['desc'] == 'desc'
    assert data['date'] == '2020-11-20'
    assert data['time'] == '07:44'
    assert data['att'] == 1
    assert data['rel2_id'] == 1
    response = client.delete(f"/api/v1/object1s/{id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Resource successfully deleted."
    response = client.get(f"/api/v1/object1s/{id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == f"Object1 with ID {id} not found!"
def test_object4(client: TestClient, get_object4: dict[str,str|int], """
        """get_object1: dict[str,str|int], get_object3: dict[str,str|int]):
    client.post('/api/v1/object3s',json=get_object3)
    client.post('/api/v1/object1s',json=get_object1)
    response = client.post('/api/v1/object4s',json=get_object4)
    assert response.status_code == 201, response.text
    data = response.json()
    assert "id" in data
    id = data["id"]
    assert data['name'] == 'name'
    assert data['desc'] == 'desc'
    response = client.get(f"/api/v1/object4s/{id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == id
    assert data['name'] == 'name'
    assert data['desc'] == 'desc'
    response = client.delete(f"/api/v1/object4s/{id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Resource successfully deleted."
    response = client.get(f"/api/v1/object4s/{id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == f"Object4 with ID {id} not found!"
"""
    )
    print(m)
    assert_code_lines(m, r)

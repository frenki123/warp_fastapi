from warp_fastapi import AppObject, Attribute
from warp_fastapi.code.code_objects.schema import AttributeCode, CommonSchemaModule, RelationshipCode, SchemaModuleCode
from warp_fastapi.config import NameConfig
from warp_fastapi.data_types import email_type

from .conftest import assert_code_lines


def test_common_schema():
    config = NameConfig()
    m = CommonSchemaModule(config)
    r = """
from pydantic import AnyUrl, BaseModel, Field
from typing import Annotated, Literal
from fastapi import Query

class Pagination(BaseModel):
    total: int
    current_page: int
    next_page: AnyUrl | None = None
    prev_page: AnyUrl | None = None
    limit: int | None = None
    offset: int | None = None

class QuerySchema(BaseModel):
    attribute: Annotated[str | None, Query()] = Field(max_length=100)
    value: Annotated[str | None, Query()] = Field(max_length=1000)
    sort: Annotated[str | None, Query()] = Field(max_length=100, default=None)
    skip: int = Field(ge=0, default=0)
    limit: int = Field(le=1000, default=100)
"""
    assert_code_lines(m, r)


def test_attributes(complex_int_att: Attribute):
    att1 = Attribute('email', email_type)
    a1 = AttributeCode(att1)
    assert str(a1) == 'email: EmailStr'
    a1.add_optional()
    assert str(a1) == 'email: EmailStr | None = None'
    att2 = Attribute('email', email_type, 'some@email.com')
    a2 = AttributeCode(att2)
    assert str(a2) == 'email: EmailStr = some@email.com'
    a2.add_optional()
    assert str(a2) == 'email: EmailStr | None = some@email.com'
    a3 = AttributeCode(complex_int_att)
    assert str(a3) == 'att: int | None = 1'


def test_relationship_code(app_objs_with_rel: tuple[AppObject, AppObject]):
    obj1 = app_objs_with_rel[0]
    rel1 = obj1.relationships[0]
    r1 = RelationshipCode(rel1, obj1)
    assert str(r1) == 'rel1_id: list[int] | None = None'
    rel2 = obj1.relationships[1]
    r2 = RelationshipCode(rel2, obj1)
    assert str(r2) == 'rel2_id: int'


def test_module_code(app_objs_with_rel: tuple[AppObject, AppObject]):
    obj1 = app_objs_with_rel[0]
    m1 = SchemaModuleCode(obj1, config=NameConfig())
    print(m1)
    r1 = """
from __future__ import annotations
from .common_schema import Pagination
from pydantic import BaseModel, ConfigDict
from datetime import date, time
class Object1Base(BaseModel):
    name: str
    desc: str
    date: date
    time: time
    rel1_id: list[int] | None = None
    rel2_id: int
    rel3_id: list[int] | None = None
class Object1sResponse(Pagination):
    data: list[Object1Response]
class Object1Response(Object1Base):
    id: int
    model_config = ConfigDict(from_attributes=True)
class Object1Create(Object1Base):
    pass
class Object1Edit(BaseModel):
    name: str | None = None
    desc: str | None = None
    date: date | None = None
    time: time | None = None
    rel1_id: list[int] | None = None
    rel2_id: int | None = None
    rel3_id: list[int] | None = None
"""
    assert_code_lines(m1, r1)

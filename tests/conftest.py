import pytest

from warp_fastapi import AppObject, AppProject, Attribute, AuthObject
from warp_fastapi.code.code_objects.base import (
    AbstractClassCode,
    AbstractModuleCode,
    SimpleDecoratorCode,
    SimpleFunctionCode,
    SimpleVariable,
)
from warp_fastapi.data_types import date_only_type, int_type, string_type, time_type
from warp_fastapi.relationships import Relationship, many_to_many, many_to_one, one_to_many


@pytest.fixture
def atts():
    return [Attribute('name', string_type), Attribute('desc', string_type)]


@pytest.fixture
def complex_int_att():
    return Attribute('att', int_type, 1, True, True)


@pytest.fixture
def complex_att():
    return Attribute('att', string_type, 'def', True, True)


@pytest.fixture
def app_obj(atts: list[Attribute]):
    return AppObject('app', *atts)


@pytest.fixture
def auth_obj(atts: list[Attribute]):
    return AuthObject('auth_obj', *atts)


@pytest.fixture
def rel(app_obj: AppObject):
    return Relationship('rel', app_obj, one_to_many)


@pytest.fixture
def app_objs(atts: list[Attribute]):
    return [AppObject('obj1', *atts), AppObject('obj2', *atts)]


@pytest.fixture
def app_objs_with_rel(atts: list[Attribute]):
    data_att = Attribute('date', date_only_type)
    time_att = Attribute('time', time_type)
    obj1 = AppObject('object1', *atts)
    obj2 = AppObject('object2', *atts)
    obj3 = AppObject('object3', *atts)
    obj4 = AppObject('object4', *atts)
    obj1.add_attributes(data_att, time_att)
    obj1.add_relationship(obj2, one_to_many, 'rel1', 'back_rel1')
    obj1.add_relationship(obj3, many_to_one, 'rel2', 'back_rel2')
    obj1.add_relationship(obj4, many_to_many, 'rel3', 'back_rel3')
    return obj1, obj4


@pytest.fixture
def app_proj(app_objs: list[AppObject]):
    return AppProject('test_project', *app_objs)


@pytest.fixture
def variables():
    return [SimpleVariable('num', 'int', '1'), SimpleVariable('text', 'str', 'text')]


@pytest.fixture
def decorators():
    return [SimpleDecoratorCode('dec1', is_function=True), SimpleDecoratorCode('dec2')]


@pytest.fixture
def functions():
    return [SimpleFunctionCode('get_num', 'return 1'), SimpleFunctionCode('get_a', 'return a')]


def code_to_list(s: str | AbstractModuleCode | AbstractClassCode):
    return list(filter(lambda line: line != '', str(s).split('\n')))


def assert_code_lines(m: AbstractModuleCode | AbstractClassCode | str, r: str):
    l1 = code_to_list(m)
    l2 = code_to_list(r)
    assert len(l1) == len(l2), f'Not same line numbers: {len(l1)} == {len(l2)}'
    for i in range(len(l1)):
        assert l1[i] == l2[i], f'Fail at line {i}:{l1[i]}=={l2[i]}'

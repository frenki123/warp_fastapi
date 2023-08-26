from datetime import date

import pytest
from pydantic import EmailStr
from sqlalchemy import Date

from warp_fastapi.exceptions import RelationshipException
from warp_fastapi.main import (
    AppConfig,
    AppObject,
    AppProject,
    Attribute,
    BackpopulatesRelationship,
    TemplateModel,
    create_relationship,
)
from warp_fastapi.relationships import many_to_many, one_to_many
from warp_fastapi.sqlalch_types import string_type
from warp_fastapi.types import DataType


def test_datatype():
    data_type = DataType(python_type=date, db_type=Date)
    assert data_type.python_type == 'date'
    assert data_type.python_module == 'datetime'
    assert data_type.db_type == 'Date'
    assert data_type.db_module == 'sqlalchemy.sql.sqltypes'
    assert data_type.pydantic_type is None

    data_type.add_pydantic_type(EmailStr)
    assert data_type.pydantic_type == 'EmailStr'
    data_type = DataType(python_type=date, db_type=Date, pydantic_type=EmailStr)
    assert data_type.pydantic_type == 'EmailStr'


def test_template_model_str():
    model = TemplateModel(name='test')
    assert str(model) == "TemplateModel(name='test')"
    with pytest.raises(ValueError) as e:
        TemplateModel(name='wrong name')
    assert 'Name most follow snake_case rule' in str(e.value)


def test_attribute_creation():
    attribute = Attribute(name='attr', type=string_type, default='default', unique=True)
    assert attribute.name == 'attr'
    assert attribute.type == string_type
    assert attribute.default == 'default'
    assert attribute.unique is True


def test_relationship_creation_error(app_obj: AppObject):
    r = create_relationship('rel', app_obj, one_to_many)
    assert r.name == 'rel'
    with pytest.raises(RelationshipException) as e:
        create_relationship('rel', app_obj, many_to_many)
    assert str(e.value) == 'Relationship of type many_to_many must have backpopulates object!'


def test_app_object(app_objs: list[AppObject], atts: list[Attribute]):
    obj = AppObject('some_name', *atts)
    assert obj.name == 'some_name'
    assert obj.plural_class_name == 'SomeNames'
    assert obj.class_name == 'SomeName'
    assert obj.table_name == 'some_names'
    assert obj.route_name == 'some-names'
    assert obj.attributes == atts
    new_att1 = Attribute('new_att', string_type)
    new_att2 = Attribute('other_att', string_type)
    obj.add_attributes(new_att1, new_att2)
    assert obj.attributes == atts + [new_att1, new_att2]
    rel_obj1 = app_objs[0]
    rel_obj2 = app_objs[1]
    obj.add_relationship(rel_obj1, one_to_many, 'rel1_name')
    assert len(obj.all_relationships) == 1
    rel1 = obj.relationships[0]
    assert obj.get_rel_name(rel1) == 'rel1_name'
    assert obj.get_rel_obj(rel1).name == 'obj1'
    assert obj.is_relationship_multiple(rel1) is False
    assert obj.is_relationship_many(rel1) is True
    obj.add_relationship(rel_obj2, one_to_many, 'rel2_name', 'backpopulates_rel_name')
    rel2 = obj.relationships[1]
    assert obj.get_rel_name(rel2) == 'rel2_name'
    assert obj.get_rel_obj(rel2) == rel_obj2
    assert isinstance(rel2, BackpopulatesRelationship)
    assert obj.get_backpopulates_name(rel2) == 'backpopulates_rel_name'
    back_rel = rel_obj2.all_relationships[0]
    assert rel_obj2.get_rel_name(back_rel) == 'backpopulates_rel_name'
    assert rel_obj2.get_rel_obj(back_rel) == obj
    assert isinstance(back_rel, BackpopulatesRelationship)
    assert rel_obj2.get_backpopulates_name(back_rel) == 'rel2_name'
    assert rel_obj2.is_relationship_many(back_rel) is False
    assert obj.is_relationship_self(rel2) is False
    assert obj.is_relationship_multiple(rel2) is False
    obj.add_relationship(rel_obj2, one_to_many, 'rel2_name2', 'backpopulates_rel2_name')
    assert obj.is_relationship_multiple(rel2) is True
    obj.add_relationship(obj, one_to_many, 'same_obj', 'other_obj')
    back_rel = obj.back_populates_relationships[0]
    assert obj.is_relationship_multiple(back_rel) is False  # check if this is OK??
    # checking probably needs to be only on "MANY" side with foreign key
    rel3 = obj.relationships[3]
    assert obj.is_relationship_self(rel3) is True
    with pytest.raises(AttributeError) as e:
        rel_obj1.is_relationship_many(rel3)
    assert 'Relationship not associated with object!' in str(e.value)


def test_app_config(atts: list[Attribute]):
    config = AppConfig(class_name='custom_class', plural='custom_plural')
    obj = AppObject('some_name', *atts, config=config)
    assert obj.route_name == 'custom-plural'
    assert obj.table_name == 'custom_plural'
    assert obj.class_name == 'custom_class'
    assert obj.plural_class_name == 'CustomPlural'
    config.plural_class_name = 'custom_class_plural'
    config.route_name = 'custom-route'
    config.table_name = 'custom_table'
    obj = AppObject('some_name', *atts, config=config)
    assert obj.plural_class_name == 'custom_class_plural'
    assert obj.route_name == 'custom-route'
    assert obj.table_name == 'custom_table'


def test_plural_generation(atts: list[Attribute]):
    obj1 = AppObject('nice_city', *atts)
    assert obj1.route_name == 'nice-cities'
    obj2 = AppObject('big_class', *atts)
    assert obj2.table_name == 'big_classes'


def test_project_creation(app_objs: list[AppObject]):
    project = AppProject('my_project', *app_objs)
    assert project.name == 'my_project'
    assert project.app_objects == app_objs

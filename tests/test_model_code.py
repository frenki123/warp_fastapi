from warp_fastapi import AppObject, Attribute
from warp_fastapi.code.code_objects.model import (
    AssociationTableCode,
    AttributeCode,
    ForeignKeyCode,
    HybridPropertyFunc,
    ModelClassCode,
    ModelModuleCode,
    RelationshipCode,
)
from warp_fastapi.code.config import NameConfig
from warp_fastapi.main import BackpopulatesRelationship
from warp_fastapi.relationships import many_to_many, many_to_one, one_to_many, one_to_one

from .conftest import assert_code_lines


def test_attribute_code(complex_att: Attribute, atts: list[Attribute], complex_int_att: Attribute):
    a = AttributeCode(complex_att)
    assert str(a) == "att: Mapped[str] = mapped_column(String, default='def', unique=True, nullable=True)"
    att = atts[0]
    a = AttributeCode(att)
    assert str(a) == 'name: Mapped[str] = mapped_column(String)'
    a = AttributeCode(complex_int_att)
    assert str(a) == 'att: Mapped[int] = mapped_column(Integer, default=1, unique=True, nullable=True)'


def test_simple_relationship_code(atts: list[Attribute]):
    obj1 = AppObject('object1', *atts)
    obj2 = AppObject('object2', *atts)
    obj1.add_relationship(obj2, one_to_many, 'test_rel')
    rel = obj1.relationships[0]
    r = RelationshipCode(rel, obj1)
    assert str(r) == 'test_rel: Mapped[list[Object2]] = relationship()'
    obj1.add_relationship(obj2, one_to_one, 'rel')
    rel = obj1.relationships[1]
    r = RelationshipCode(rel, obj1)
    assert str(r) == 'rel: Mapped[Object2] = relationship(foreign_keys=[rel_id])'


def test_backref_relationship_code(atts: list[Attribute]):
    obj1 = AppObject('object1', *atts)
    obj2 = AppObject('object2', *atts)
    obj1.add_relationship(obj2, many_to_one, 'obj1_rel', 'obj2_rel')
    obj1_rel = obj1.relationships[0]
    obj2_rel = obj2.all_relationships[0]
    r1 = RelationshipCode(obj1_rel, obj1)
    r2 = RelationshipCode(obj2_rel, obj2)
    assert str(r1) == "obj1_rel: Mapped[Object2] = relationship(back_populates='obj2_rel')"
    assert (
        str(r2)
        == "obj2_rel: Mapped[list[Object1]] = relationship(back_populates='obj1_rel', cascade='all, delete-orphan')"
    )
    obj1.add_relationship(obj2, many_to_many, 'rel1', 'back_rel1')
    obj1_rel = obj1.relationships[1]
    obj2_rel = obj2.all_relationships[1]
    r1 = RelationshipCode(obj1_rel, obj1)
    r2 = RelationshipCode(obj2_rel, obj2)
    assert str(r1) == (
        "rel1: Mapped[list[Object2]] = relationship(secondary=object2_object1_association,"
        " back_populates='back_rel1', cascade='all, delete', foreign_keys=[rel1_id])"
    )
    assert str(r2) == (
        "back_rel1: Mapped[list[Object1]] = relationship(secondary="
        "object2_object1_association, back_populates='rel1')"
    )
    # TODO: check if this is missing: , foreign_keys=[back_rel1_id])
    obj1.add_relationship(obj1, one_to_many, 'self_rel', optional=True)
    obj1_rel = obj1.relationships[2]
    r1 = RelationshipCode(obj1_rel, obj1)
    assert str(r1) == 'self_rel: Mapped[list[Object1]] = relationship(remote_side=[id])'


def test_foreign_key(atts: list[Attribute]):
    obj1 = AppObject('object1', *atts)
    obj2 = AppObject('object2', *atts)
    obj1.add_relationship(obj2, one_to_one, 'obj1_rel', 'obj2_rel', True)
    obj1_rel = obj1.relationships[0]
    fk = ForeignKeyCode(obj1_rel, obj1)
    assert str(fk) == (
        "obj1_rel_id: Mapped[int] = mapped_column(ForeignKey('object2s.id')," " nullable = True, unique=True)"
    )
    obj1.add_relationship(obj2, one_to_many, 'rel')
    obj1_rel = obj1.relationships[1]
    fk = ForeignKeyCode(obj1_rel, obj1)
    assert str(fk) == "rel_id: Mapped[int] = mapped_column(ForeignKey('object2s.id'))"


def test_association_table(atts: list[Attribute]):
    obj1 = AppObject('object1', *atts)
    obj2 = AppObject('object2', *atts)
    obj1.add_relationship(obj2, many_to_many, 'obj1_rel', 'obj2_rel', True)
    rel = obj1.relationships[0]
    assert isinstance(rel, BackpopulatesRelationship)
    c = AssociationTableCode(rel)
    assert str(c) == (
        "object2_object1_association = Table"
        "('object2_object1',Base.metadata,Column('object2_id', Integer, "
        "ForeignKey('object2s.id')),Column('object1_id', Integer, "
        "ForeignKey('object1s.id')))"
    )
    r = RelationshipCode(rel, obj1)
    assert str(r) == (
        "obj1_rel: Mapped[list[Object2]] = relationship"
        "(secondary=object2_object1_association, back_populates='obj2_rel')"
    )


def test_hybrid_property():
    h = HybridPropertyFunc('test')
    print(h)
    r = """@hybrid_property
def test_id(self):
    return [test.id for test in self.test]"""
    assert str(h) == r


def test_model_class(app_objs_with_rel: tuple[AppObject, AppObject]):
    c = ModelClassCode(app_objs_with_rel[0])
    print(c)
    r = (
        """class Object1(Base):
    __tablename__ = 'object1s'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    date: Mapped[date] = mapped_column(Date)
    time: Mapped[time] = mapped_column(Time)
    rel1: Mapped[list[Object2]] = relationship(back_populates='back_rel1', cascade='all, delete-orphan')
    rel2_id: Mapped[int] = mapped_column(ForeignKey('object3s.id'))
    rel2: Mapped[Object3] = relationship(back_populates='back_rel2')
    rel3: Mapped[list[Object4]] = relationship(secondary=object4_object1_association,"""
        """ back_populates='back_rel3', cascade='all, delete')
    @hybrid_property
    def rel1_id(self):
        return [rel1.id for rel1 in self.rel1]
    @hybrid_property
    def rel3_id(self):
        return [rel3.id for rel3 in self.rel3]
"""
    )
    assert_code_lines(c, r)


def test_model_module(app_objs_with_rel: tuple[AppObject, AppObject]):
    obj1 = app_objs_with_rel[0]
    obj2 = app_objs_with_rel[1]
    config = NameConfig()
    m1 = ModelModuleCode(obj1, config)
    assoc_table_line = (
        "object4_object1_association = Table('object4_object1',Base.metadata,Column"
        "('object4_id', Integer, ForeignKey('object4s.id')),Column('object1_id', "
        "Integer, ForeignKey('object1s.id')))"
    )
    r1 = (
        f"""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..database import Base
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Time
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date, time
if TYPE_CHECKING:
    from .object2_model import Object2
    from .object3_model import Object3
    from .object4_model import Object4
{assoc_table_line}
class Object1(Base):
    __tablename__ = 'object1s'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    date: Mapped[date] = mapped_column(Date)
    time: Mapped[time] = mapped_column(Time)
    rel1: Mapped[list[Object2]] = relationship(back_populates='back_rel1', cascade='all, delete-orphan')
    rel2_id: Mapped[int] = mapped_column(ForeignKey('object3s.id'))
    rel2: Mapped[Object3] = relationship(back_populates='back_rel2')
    rel3: Mapped[list[Object4]] = relationship(secondary=object4_object1_association,"""
        f""" back_populates='back_rel3', cascade='all, delete')
    @hybrid_property
    def rel1_id(self):
        return [rel1.id for rel1 in self.rel1]
    @hybrid_property
    def rel3_id(self):
        return [rel3.id for rel3 in self.rel3]
"""
    )
    assert_code_lines(m1, r1)
    m2 = ModelModuleCode(obj2, config)
    print(m2)
    r2 = """
from __future__ import annotations
from typing import TYPE_CHECKING
from ..database import Base
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.hybrid import hybrid_property
from .object1_model import object4_object1_association
if TYPE_CHECKING:
    from .object1_model import Object1
class Object4(Base):
    __tablename__ = 'object4s'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    back_rel3: Mapped[list[Object1]] = relationship(secondary=object4_object1_association, back_populates='rel3')
    @hybrid_property
    def back_rel3_id(self):
        return [back_rel3.id for back_rel3 in self.back_rel3]
"""
    assert_code_lines(m2, r2)

from ordered_set import OrderedSet

from ... import AppObject, Attribute
from ...config import StructureConfig
from ...relationships import BackpopulatesRelationship, Relationship
from .base import (
    AbstractModuleCode,
    AbstractVariableCode,
    SimpleClassCode,
    SimpleModuleCode,
    SimpleVariable,
)


class AttributeCode(AbstractVariableCode):
    def __init__(self, att: Attribute, all_optional: bool = False):
        self.name = att.name
        self.type = f'{att.type.python_type}'
        if att.default:
            self.value = att.default
        if att.type.pydantic_type:
            self.type = f'{att.type.pydantic_type}'
        if att.optional or all_optional:
            self.add_optional()

    def add_optional(self) -> None:
        super().add_optional()
        if not self.value:
            self.value = 'None'


class RelationshipCode(AbstractVariableCode):
    def __init__(
        self,
        rel: Relationship | BackpopulatesRelationship,
        app_obj: AppObject,
        is_int: bool = True,
        all_optional: bool = False,
    ):
        self.name = app_obj.get_rel_name(rel) + '_id'
        self.type = 'int'
        if app_obj.is_relationship_many(rel):
            self.type = 'list[int]'
        if not is_int:  # pragma: no cover -> needs to be checked
            self.name = app_obj.get_rel_name(rel)
            rel_obj = app_obj.get_rel_obj(rel)
            self.type = rel_obj.class_name
            if app_obj.is_relationship_many(rel):
                self.type = f'list[{rel_obj.class_name}]'
        if rel.optional or all_optional or app_obj.is_relationship_many(rel):
            self.add_optional()
            self.value = 'None'


class SchemaModuleCode(AbstractModuleCode):
    def __init__(self, app_obj: AppObject, config: StructureConfig = StructureConfig()):
        self.type_checking_imports = {}
        self.classes = []
        self.functions = []
        self.variables = []
        self.config = config
        self.folder = config.get_schema_folder(app_obj)
        self.filename = config.get_schema_filename(app_obj)
        common_schema_module = config.get_module_for_schema(app_obj, config.get_common_schema_path())
        self.imports = {
            '__future__': {'annotations'},
            common_schema_module: {'Pagination'},
            'pydantic': {'BaseModel', 'ConfigDict'},
        }
        self.fill_imports(app_obj)
        self.get_schema_classes(app_obj, config)

    def __str__(self) -> str:
        return f"""
{self.imports_code}
{self.classes_code}
""".strip(
            '\n'
        )

    def fill_imports(self, app_obj: AppObject) -> None:
        for att in app_obj.attributes:
            if att.type.python_module != 'builtins':
                if self.imports.get(att.type.python_module):
                    self.imports[att.type.python_module].add(att.type.python_type)
                else:
                    self.imports[att.type.python_module] = {att.type.python_type}

    def get_schema_classes(self, app_obj: AppObject, config: StructureConfig = StructureConfig()) -> None:
        id = SimpleVariable('id', 'int')
        orm_config = SimpleVariable('model_config', value='ConfigDict(from_attributes=True)')
        # data_att: set[AbstractVariableCode] = {id, orm_config}
        # att_order:list[AbstractVariableCode] = [orm_config, id]
        read_att: OrderedSet[AbstractVariableCode] = OrderedSet([id, orm_config])
        create_att: OrderedSet[AbstractVariableCode] = OrderedSet([])
        edit_att: OrderedSet[AbstractVariableCode] = OrderedSet([])
        for att in app_obj.attributes:
            # data_att.add(AttributeCode(att))
            read_att.add(AttributeCode(att))
            create_att.add(AttributeCode(att))
            # att_order.append(AttributeCode(att))
            edit_att.add(AttributeCode(att, all_optional=True))
            # att_order.append(AttributeCode(att,all_optional=True))
        for rel in app_obj.all_relationships:
            # data_att.add(RelationshipCode(rel, app_obj, False))
            read_att.add(RelationshipCode(rel, app_obj))
            create_att.add(RelationshipCode(rel, app_obj))
            # att_order.append(RelationshipCode(rel, app_obj))
            edit_att.add(RelationshipCode(rel, app_obj, all_optional=True))
            # att_order.append(RelationshipCode(rel, app_obj,all_optional=True))
        base_att: OrderedSet[AbstractVariableCode] = find_base_att(read_att, create_att, edit_att)
        base_class_name = config.get_base_cls_schema(app_obj)
        self.classes.append(SimpleClassCode(base_class_name, 'BaseModel', list(base_att)))
        self.classes.append(
            SimpleClassCode(
                config.get_pagination_cls_schema(app_obj),
                'Pagination',
                [SimpleVariable('data', f'list[{config.get_read_cls_schema(app_obj)}]')],
            )
        )
        schemas: dict[str, OrderedSet[AbstractVariableCode]] = {
            config.get_read_cls_schema(app_obj): read_att,
            config.get_create_cls_schema(app_obj): create_att,
            config.get_edit_cls_schema(app_obj): edit_att,
        }
        for schema_cls_name, att_list in schemas.items():
            super_class = 'BaseModel'
            passed_att = att_list
            x1 = list(att_list - base_att) + list(base_att)
            x2 = list(att_list)
            if x1 == x2:
                super_class = base_class_name
                passed_att = OrderedSet(att_list - base_att)
            self.classes.append(SimpleClassCode(schema_cls_name, super_class, list(passed_att)))


def find_base_att(*sets: OrderedSet[AbstractVariableCode]) -> OrderedSet[AbstractVariableCode]:
    union_sets = sets[0]
    for i in range(len(sets) - 1):
        union_sets = union_sets.union(sets[i + 1])
    unknow_set: OrderedSet[AbstractVariableCode] = OrderedSet([])
    current_len = sum([len(s) for s in sets])
    for x in union_sets:
        unknow_set.add(x)
        new_sets: list[OrderedSet[AbstractVariableCode]] = []
        for s in sets:
            new_set = OrderedSet(s - unknow_set)
            if not list(new_set) + list(unknow_set) == list(s):
                new_set = s
            new_sets.append(new_set)
        new_len = sum([len(s) for s in new_sets]) + len(unknow_set)
        if new_len < current_len:
            current_len = new_len
        else:
            unknow_set.remove(x)
    return unknow_set


class CommonSchemaModule(SimpleModuleCode):
    def __init__(self, config: StructureConfig, secure: bool = False):
        self.filename = config.get_common_schema_filename()
        self.folder = config.get_common_schema_folder()
        self.token = ''
        if secure:
            self.token = self._get_token_code()

    def __str__(self) -> str:
        return f"""
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

{self.token}
"""

    @staticmethod
    def _get_token_code() -> str:
        return """
class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]

class TokenPayload(BaseModel):
    user_id: int|None
"""

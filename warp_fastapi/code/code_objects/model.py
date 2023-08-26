from ...main import AppObject, Attribute, BackpopulatesRelationship, Relationship
from ...relationships import many_to_many, one_to_one
from ..config import NameConfig
from .base import (
    AbstractClassCode,
    AbstractFunctionCode,
    AbstractModuleCode,
    AbstractVariableCode,
    SimpleDecoratorCode,
    SimpleVariable,
)


class AttributeCode(AbstractVariableCode):
    def __init__(self, att: Attribute):
        self.name = att.name
        self.type = f'Mapped[{att.type.python_type}]'
        def_val = att.default
        if isinstance(att.default, str):
            def_val = f"'{def_val}'"
        self.value = (
            f"mapped_column({att.type.db_type}"
            f"{', default=' + str(def_val) if def_val is not None else ''}"
            f"{', unique=True' if att.unique else ''}"
            f"{', nullable=True' if att.optional else ''})"
        )


class RelationshipCode(AbstractVariableCode):
    def __init__(self, rel: Relationship | BackpopulatesRelationship, app_obj: AppObject) -> None:
        self.name = app_obj.get_rel_name(rel)
        self.rel_obj = app_obj.get_rel_obj(rel)

        self.type = f'Mapped[{self.rel_obj.class_name}]'
        if app_obj.is_relationship_many(rel):
            self.type = f'Mapped[list[{self.rel_obj.class_name}]]'
        self.value = f'relationship({self.get_params(rel, app_obj)})'

    def get_params(self, rel: Relationship | BackpopulatesRelationship, app_obj: AppObject) -> str:
        params: list[str] = []
        if rel.relationship_type == many_to_many and isinstance(rel, BackpopulatesRelationship):
            params.append(f'secondary={get_association_table_name(rel)}')
        if isinstance(rel, BackpopulatesRelationship):
            params.append(f"back_populates='{app_obj.get_backpopulates_name(rel)}'")
        if self.needs_cascade(rel, app_obj):
            if rel.relationship_type == many_to_many:
                if not app_obj.is_rel_backref(rel):
                    params.append("cascade='all, delete'")
            else:
                params.append("cascade='all, delete-orphan'")
        if app_obj.is_relationship_multiple(rel):
            params.append(f'foreign_keys=[{self.name}_id]')
        if app_obj.is_relationship_self(rel) and not app_obj.is_rel_backref(rel):
            params.append('remote_side=[id]')
        return ', '.join(params)

    @staticmethod
    def needs_cascade(rel: Relationship | BackpopulatesRelationship, app_obj: AppObject) -> bool:
        if isinstance(rel, Relationship):
            return False
        if not app_obj.is_relationship_many(rel):
            return False
        if rel.optional:
            return False
        return True


class ForeignKeyCode(AbstractVariableCode):
    def __init__(self, rel: Relationship | BackpopulatesRelationship, app_obj: AppObject) -> None:
        self.name = app_obj.get_rel_name(rel) + '_id'
        self.rel_obj = app_obj.get_rel_obj(rel)
        optional = rel.optional
        self.type = 'Mapped[int]'
        params = [f"ForeignKey('{self.rel_obj.table_name}.id')"]
        if optional:
            params.append('nullable = True')
        if rel.relationship_type == one_to_one:
            params.append('unique=True')
        self.value = f"mapped_column({', '.join(params)})"


class AssociationTableCode(AbstractVariableCode):
    def __init__(self, rel: BackpopulatesRelationship) -> None:
        self.name = get_association_table_name(rel)
        self.value = (
            f"Table('{rel.related_object.name}_{rel.back_populates_object.name}',"
            f"Base.metadata,"
            f"Column('{rel.related_object.name}_id', Integer, ForeignKey('{rel.related_object.table_name}.id')),"
            f"Column('{rel.back_populates_object.name}_id', Integer, "
            f"ForeignKey('{rel.back_populates_object.table_name}.id'))"
            f")"
        )


class HybridPropertyFunc(AbstractFunctionCode):
    def __init__(self, name: str):
        self.name = name + '_id'
        self.decorators = [SimpleDecoratorCode('hybrid_property')]
        self.parametars = [SimpleVariable('self')]
        self.content = f'return [{name}.id for {name} in self.{name}]'


class ModelClassCode(AbstractClassCode):
    def __init__(self, app_obj: AppObject):
        self.class_name = app_obj.class_name
        self.attributes = []
        self.methods = []
        self.super_class_name = 'Base'
        self.attributes.append(SimpleVariable('__tablename__', '', f"'{app_obj.table_name}'"))
        self.attributes.append(SimpleVariable('id', 'Mapped[int]', 'mapped_column(primary_key=True)'))
        for att in app_obj.attributes:
            self.attributes.append(AttributeCode(att))
        for rel in app_obj.all_relationships:
            if app_obj.is_relationship_many(rel):
                self.attributes.append(RelationshipCode(rel, app_obj))
                self.methods.append(HybridPropertyFunc(app_obj.get_rel_name(rel)))
            else:
                self.attributes.append(ForeignKeyCode(rel, app_obj))
                self.attributes.append(RelationshipCode(rel, app_obj))


class ModelModuleCode(AbstractModuleCode):
    def __init__(self, app_obj: AppObject, config: NameConfig = NameConfig()):
        self.config = config
        self.folder = config.model_folder
        self.filename = app_obj.name + config.model_extension
        self.imports = {
            '__future__': {'annotations'},
            'typing': {'TYPE_CHECKING'},
            f'..{config.database_file}': {'Base'},
            'sqlalchemy.orm': {'mapped_column', 'relationship', 'Session', 'Mapped'},
            'sqlalchemy': {'ForeignKey', 'Table', 'Column', 'Integer'},
            'sqlalchemy.ext.hybrid': {'hybrid_property'},
        }
        self.type_checking_imports = {}
        self.fill_imports(app_obj)
        self.classes = [ModelClassCode(app_obj)]
        self.variables = []
        for rel in app_obj.relationships:
            if isinstance(rel, BackpopulatesRelationship) and rel.relationship_type == many_to_many:
                self.variables.append(AssociationTableCode(rel))

    def fill_imports(self, app_obj: AppObject) -> None:
        for att in app_obj.attributes:
            self.imports['sqlalchemy'].add(att.type.db_type)
            if att.type.python_module != 'builtins':
                if self.imports.get(att.type.python_module):
                    self.imports[att.type.python_module].add(att.type.python_type)
                else:
                    self.imports[att.type.python_module] = {att.type.python_type}
        for rel in app_obj.all_relationships:
            obj = app_obj.get_rel_obj(rel)
            module = f'.{self.config.model_name(obj)}'
            class_name = obj.class_name
            if self.type_checking_imports.get(module):
                self.type_checking_imports[module].add(class_name)  # pragma: no cover -> probably will never happen
            else:
                self.type_checking_imports[module] = {class_name}
            if (
                rel.relationship_type == many_to_many
                and app_obj.is_rel_backref(rel)
                and isinstance(rel, BackpopulatesRelationship)
            ):
                table_name = get_association_table_name(rel)
                if self.imports.get(module):
                    self.imports[module].add(table_name)  # pragma: no cover -> probably will never happen
                else:
                    self.imports[module] = {table_name}

    def __str__(self) -> str:
        return f"""
{self.imports_code}
{self.type_checking_imports_code}
{self.variables_code}
{self.classes_code}
""".strip(
            '\n'
        )


def get_association_table_name(rel: BackpopulatesRelationship) -> str:
    return f'{rel.related_object.name}_{rel.back_populates_object.name}_association'

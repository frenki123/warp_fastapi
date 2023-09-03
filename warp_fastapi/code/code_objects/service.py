from typing import Literal

from ...main import AppObject
from ..config import NameConfig
from .base import (
    AbstractClassCode,
    AbstractFunctionCode,
    AbstractModuleCode,
    AbstractVariableCode,
    SimpleFunctionCode,
    SimpleVariable,
)


class ServiceInitFunction(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject, config: NameConfig):
        self.name = '__init__'
        self.parametars = [
            SimpleVariable('self'),
            SimpleVariable('repository', config.get_repo_classname(app_obj)),
        ]
        self.content = ''
        self.get_data(app_obj, config)

    def get_data(self, app_obj: AppObject, config: NameConfig) -> None:
        content: list[AbstractVariableCode] = [SimpleVariable('self.repository', value='repository')]
        for rel in app_obj.all_relationships:
            obj = app_obj.get_rel_obj(rel)
            self.parametars.append(
                SimpleVariable(f'{config.get_repository_filename(obj)}', f'{config.get_repo_classname(obj)}')
            )
            content.append(
                SimpleVariable(
                    f'self.{config.get_repository_filename(obj)}', value=f'{config.get_repository_filename(obj)}'
                )
            )
        self.content = '\n'.join([str(c) for c in content])


class ServiceIdSearchFunc(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject, config: NameConfig):
        self.name = '_get_id_data'
        self.parametars = [
            SimpleVariable('self'),
            SimpleVariable(
                app_obj.name, f'{config.get_create_cls_schema(app_obj)}|{config.get_edit_cls_schema(app_obj)}'
            ),
        ]
        self.content = self.get_content(app_obj, config)

    def get_content(self, app_obj: AppObject, config: NameConfig) -> str:
        init_vars: list[str] = []
        search_vars: list[str] = []
        return_vars: list[str] = []
        for rel in app_obj.all_relationships:
            name = app_obj.get_rel_name(rel)
            obj = app_obj.get_rel_obj(rel)
            v1 = str(SimpleVariable(name, f'{config.get_read_cls_schema(obj)}|None', 'None'))
            search_fun = 'get_by_id'
            return_vars.append(name)
            if app_obj.is_relationship_many(rel):
                v1 = str(SimpleVariable(name, f'list[{config.get_read_cls_schema(obj)}]', '[]'))
                search_fun = 'get_by_ids'
            search_vars.append(
                f'if {app_obj.name}.{name}_id:\n'
                f'    {name} = self.{config.get_repository_filename(obj)}.{search_fun}({app_obj.name}.{name}_id)'
            )
            init_vars.append(v1)
        r1 = '\n'.join(init_vars)
        r2 = '\n'.join(search_vars)
        r3 = 'return ' + ', '.join(return_vars)
        return f"""{r1}
{r2}
{r3}
"""


class ServicePrapareDBFucn(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject, config: NameConfig):
        self.name = '_prepare_db_data'
        self.parametars = [
            SimpleVariable('self'),
            SimpleVariable(
                app_obj.name, f'{config.get_create_cls_schema(app_obj)}|{config.get_edit_cls_schema(app_obj)}'
            ),
        ]
        self.content = self.get_content(app_obj, config)

    def get_content(self, app_obj: AppObject, config: NameConfig) -> str:
        var_params: list[str] = []
        dict_params: list[str] = []
        id_params: list[str] = []
        for rel in app_obj.all_relationships:
            name = app_obj.get_rel_name(rel)
            var_params.append(name)
            dict_params.append(f"'{name}':{name}")
            id_params.append(f'"{name}_id"')
        return f"""
{', '.join(var_params)} = self._get_id_data({app_obj.name})
id_data = {{{', '.join(dict_params)}}}
data = {app_obj.name}.model_dump(exclude_unset=True,exclude={{{', '.join(id_params)}}})
data.update(id_data)
return data
"""


class ServiceGetCode(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject):
        self.name = f'get_{app_obj.name}'
        self.parametars = [SimpleVariable('self'), SimpleVariable('id', 'int')]
        self.content = 'return self.repository.get_by_id(id)'


class ServiceActionCode(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject, action: Literal['create', 'edit', 'update'], config: NameConfig):
        self.name = f'{action}_{app_obj.name}'
        obj_type = config.get_edit_cls_schema(app_obj)
        if action != 'edit':
            obj_type = config.get_create_cls_schema(app_obj)
        self.parametars = [
            SimpleVariable('self'),
        ]
        action_params = [f'{app_obj.name}_data']
        if action != 'create':
            action_params = ['id', f'{app_obj.name}_data']
            self.parametars.append(SimpleVariable('id', 'int'))
        self.parametars.append(SimpleVariable(app_obj.name, obj_type))
        prepare_data = f'{app_obj.name}_data = {app_obj.name}.model_dump()'
        if app_obj.all_relationships:
            prepare_data = f'{app_obj.name}_data = self._prepare_db_data({app_obj.name})'
        self.content = f"""
{prepare_data}
db_{app_obj.name} = self.repository.{action}({', '.join(action_params)})
return db_{app_obj.name}
"""


class ServiceDeleteCode(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject):
        self.name = f'delete_{app_obj.name}'
        self.parametars = [SimpleVariable('self'), SimpleVariable('id', 'int')]
        self.content = 'return self.repository.delete(id)'


class ServiceSearchCode(AbstractFunctionCode):
    def __init__(self, app_obj: AppObject):
        self.name = f'search_{app_obj.name}'
        self.parametars = [
            SimpleVariable('self'),
            SimpleVariable('attribute', 'str|None'),
            SimpleVariable('value', 'str|None'),
            SimpleVariable('sort', 'str|None'),
            SimpleVariable('skip', 'int'),
            SimpleVariable('limit', 'int'),
        ]
        self.content = """
db_results = self.repository.search(attribute, value, sort, skip, limit)
return db_results
"""


class ServiceClassCode(AbstractClassCode):
    def __init__(self, app_obj: AppObject, config: NameConfig):
        self.class_name = config.get_service_classname(app_obj)
        self.attributes = []
        self.methods = [ServiceInitFunction(app_obj, config)]
        if app_obj.all_relationships:
            self.methods += [
                ServiceIdSearchFunc(app_obj, config),
                ServicePrapareDBFucn(app_obj, config),
            ]
        self.methods += [
            ServiceGetCode(app_obj),
            ServiceActionCode(app_obj, action='create', config=config),
            ServiceActionCode(app_obj, action='update', config=config),
            ServiceActionCode(app_obj, action='edit', config=config),
            ServiceDeleteCode(app_obj),
            ServiceSearchCode(app_obj),
        ]


class GetServiceFunc(SimpleFunctionCode):
    def __init__(self, app_obj: AppObject, config: NameConfig):
        self.name = f'get_{app_obj.name}_service'
        self.parametars = [SimpleVariable('db', 'Session')]
        return_params = [f'{config.get_repo_classname(app_obj)}(db)']
        for rel in app_obj.all_relationships:
            obj = app_obj.get_rel_obj(rel)
            return_params.append(f'{config.get_repository_filename(obj)}={config.get_repo_classname(obj)}(db)')
        self.content = f"return {config.get_service_classname(app_obj)}({', '.join(return_params)})"


class ServiceModuleCode(AbstractModuleCode):
    def __init__(self, app_obj: AppObject, config: NameConfig):
        self.type_checking_imports = {}
        self.classes = []
        self.functions = [GetServiceFunc(app_obj, config)]
        self.variables = []
        self.config = config
        self.folder = config.get_service_folder(app_obj)
        self.filename = config.get_service_filename(app_obj)
        schema_module = config.get_module_for_service(app_obj, config.get_schema_path(app_obj))
        create_schema = config.get_create_cls_schema(app_obj)
        edit_schema = config.get_edit_cls_schema(app_obj)
        response_schema = config.get_read_cls_schema(app_obj)
        db_schema = config.get_db_cls_schema(app_obj)
        repo_modul = config.get_module_for_service(app_obj, config.get_repository_path(app_obj))
        repo_name = config.get_repo_classname(app_obj)
        self.imports = {
            f'{schema_module}': {create_schema, edit_schema, response_schema, db_schema},
            f'{repo_modul}': {repo_name},
            'sqlalchemy.orm': {'Session'},
        }
        self.fill_imports(app_obj, config)
        self.classes = [ServiceClassCode(app_obj, config)]

    def __str__(self) -> str:
        return f"""
{self.imports_code}
{self.classes_code}
{self.functions_code}
"""

    def fill_imports(self, app_obj: AppObject, config: NameConfig) -> None:
        for rel in app_obj.all_relationships:
            obj = app_obj.get_rel_obj(rel)
            class_name = config.get_repo_classname(obj)
            module_name = config.get_module_for_service(app_obj, config.get_repository_path(obj))
            schema_module = config.get_module_for_service(app_obj, config.get_schema_path(obj))
            response_class = config.get_read_cls_schema(obj)
            if self.imports.get(module_name):
                self.imports[module_name].add(
                    class_name
                )  # pragma: no cover -> response schema should be in specific file
            else:
                self.imports[module_name] = {class_name}
            if self.imports.get(schema_module):
                self.imports[schema_module].add(
                    response_class
                )  # pragma: no cover -> response schema should be in specific file
            else:
                self.imports[schema_module] = {response_class}

from pathlib import Path
from typing import NotRequired, TypedDict, Unpack

from ..main import AppObject
from .utils import get_module_str


class TypedNameConfig(TypedDict):
    database_file: NotRequired[str]
    base_file: NotRequired[str]
    dependency_file: NotRequired[str]
    settings_file: NotRequired[str]
    model_file: NotRequired[str]
    route_file: NotRequired[str]
    main_route_file: NotRequired[str]
    schema_file: NotRequired[str]
    base_schema_tmpl: NotRequired[str]
    create_schema_tmpl: NotRequired[str]
    read_schema_tmpl: NotRequired[str]
    read_full_schema_tmpl: NotRequired[str]
    edit_schema_tmpl: NotRequired[str]
    db_schema_tmpl: NotRequired[str]
    pagination_schema_tmpl: NotRequired[str]
    common_schema_file: NotRequired[str]
    repository_file: NotRequired[str]
    repository_main_class_name: NotRequired[str]
    repository_main_file: NotRequired[str]
    repository_class_tmpl: NotRequired[str]
    service_file: NotRequired[str]
    service_class_tmpl: NotRequired[str]
    alembic_folder: NotRequired[str]
    app_foldername: NotRequired[str]


class NameConfig:
    database_file: str = 'database'
    base_file: str = 'base'
    dependency_file: str = 'dependancies'
    settings_file: str = 'settings'
    model_file: str = 'models/{name}_model'
    route_file: str = 'routes/{name}_route'
    main_route_file: str = 'routes/main_routes'
    schema_file: str = 'schemas/{name}_schema'
    base_schema_tmpl: str = '{class_name}Base'
    create_schema_tmpl: str = '{class_name}Create'
    read_schema_tmpl: str = '{class_name}Response'
    read_full_schema_tmpl: str = '{class_name}Info'
    edit_schema_tmpl: str = '{class_name}Edit'
    db_schema_tmpl: str = '{class_name}Database'
    pagination_schema_tmpl: str = '{plural_class_name}Response'
    common_schema_file: str = 'schemas/common_schema'
    repository_file: str = 'repository/{name}_repository'
    repository_main_class_name: str = 'Repository'
    repository_main_file: str = 'repository/base'
    repository_class_tmpl: str = '{class_name}Repository'
    service_file: str = 'services/{name}_service'
    service_class_tmpl: str = '{class_name}Service'
    alembic_folder: str = 'alembic'
    app_foldername: str = 'app'

    def __init__(self, **kwargs: Unpack[TypedNameConfig]) -> None:
        self._custom_init(**kwargs)

    def update_config(self, **kwargs: Unpack[TypedNameConfig]) -> None:
        self._custom_init(**kwargs)

    def _custom_init(self, **kwargs: Unpack[TypedNameConfig]) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'NameConfig' object has no attribute '{key}'")

    def get_database_filename(self) -> str:
        return Path(self.database_file).name

    def get_database_folder(self) -> str:
        return str(Path(self.database_file).parent)

    def get_database_path(self) -> str:
        return str(Path(self.database_file))

    def get_module_for_database(self, other_path: str | Path) -> str:
        return get_module_str(self.database_file, str(other_path))

    def get_base_filename(self) -> str:
        return Path(self.base_file).name

    def get_base_folder(self) -> str:
        return str(Path(self.base_file).parent)

    def get_base_path(self) -> str:
        return str(Path(self.base_file))

    def get_module_for_base(self, other_path: str | Path) -> str:
        return get_module_str(self.base_file, str(other_path))

    def get_dependency_filename(self) -> str:
        return Path(self.dependency_file).name

    def get_dependency_folder(self) -> str:
        return str(Path(self.dependency_file).parent)

    def get_dependency_path(self) -> str:
        return str(Path(self.dependency_file))

    def get_module_for_dependency(self, other_path: str | Path) -> str:
        return get_module_str(self.dependency_file, str(other_path))

    def get_settings_filename(self) -> str:
        return Path(self.settings_file).name

    def get_settings_folder(self) -> str:
        return str(Path(self.settings_file).parent)

    def get_settings_path(self) -> str:
        return str(Path(self.settings_file))

    def get_module_for_settings(self, other_path: str | Path) -> str:
        return get_module_str(self.database_file, str(other_path))

    def get_model_filename(self, obj: AppObject) -> str:
        return self.get_modul_path(self.model_file, obj).name

    def get_model_folder(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.model_file, obj).parent)

    def get_model_path(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.model_file, obj))

    def get_module_for_model(self, obj: AppObject, other_path: str | Path) -> str:
        return get_module_str(self.get_model_path(obj), str(other_path))

    def get_route_filename(self, obj: AppObject) -> str:
        return self.get_modul_path(self.route_file, obj).name

    def get_route_folder(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.route_file, obj).parent)

    def get_route_path(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.route_file, obj))

    def get_module_for_route(self, obj: AppObject, other_path: str | Path) -> str:
        return get_module_str(self.get_route_path(obj), str(other_path))

    def get_main_route_filename(self) -> str:
        return Path(self.main_route_file).name

    def get_main_route_folder(self) -> str:
        return str(Path(self.main_route_file).parent)

    def get_main_route_path(self) -> str:
        return str(Path(self.main_route_file))

    def get_module_for_main_route(self, other_path: str | Path) -> str:
        return get_module_str(self.main_route_file, str(other_path))

    def get_schema_filename(self, obj: AppObject) -> str:
        return self.get_modul_path(self.schema_file, obj).name

    def get_schema_folder(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.schema_file, obj).parent)

    def get_schema_path(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.schema_file, obj))

    def get_module_for_schema(self, obj: AppObject, other_path: str | Path) -> str:
        return get_module_str(self.get_schema_path(obj), str(other_path))

    def get_base_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.base_schema_tmpl, obj)

    def get_create_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.create_schema_tmpl, obj)

    def get_read_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.read_schema_tmpl, obj)

    def get_read_full_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.read_full_schema_tmpl, obj)

    def get_edit_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.edit_schema_tmpl, obj)

    def get_db_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.db_schema_tmpl, obj)

    def get_common_schema_filename(self) -> str:
        return Path(self.common_schema_file).name

    def get_common_schema_folder(self) -> str:
        return str(Path(self.common_schema_file).parent)

    def get_common_schema_path(self) -> str:
        return str(Path(self.common_schema_file))

    def get_module_for_common_schema(self, other_path: str | Path) -> str:
        return get_module_str(self.common_schema_file, str(other_path))

    def get_pagination_cls_schema(self, obj: AppObject) -> str:
        return self._format(self.pagination_schema_tmpl, obj)

    def get_repository_filename(self, obj: AppObject) -> str:
        return self.get_modul_path(self.repository_file, obj).name

    def get_repository_folder(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.repository_file, obj).parent)

    def get_repository_path(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.repository_file, obj))

    def get_module_for_repository(self, obj: AppObject, other_path: str | Path) -> str:
        return get_module_str(self.get_repository_path(obj), str(other_path))

    def get_repo_classname(self, obj: AppObject) -> str:
        return self._format(self.repository_class_tmpl, obj)

    def get_repository_main_filename(self) -> str:
        return Path(self.repository_main_file).name

    def get_repository_main_folder(self) -> str:
        return str(Path(self.repository_main_file).parent)

    def get_repository_main_path(self) -> str:
        return str(Path(self.repository_main_file))

    def get_module_for_repository_main(self, other_path: str | Path) -> str:
        return get_module_str(self.repository_main_file, str(other_path))

    def get_service_filename(self, obj: AppObject) -> str:
        return self.get_modul_path(self.service_file, obj).name

    def get_service_folder(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.service_file, obj).parent)

    def get_service_path(self, obj: AppObject) -> str:
        return str(self.get_modul_path(self.service_file, obj))

    def get_module_for_service(self, obj: AppObject, other_path: str | Path) -> str:
        return get_module_str(self.get_service_path(obj), str(other_path))

    def get_service_classname(self, obj: AppObject) -> str:
        return self._format(self.service_class_tmpl, obj)

    def get_module_for_main(self, other_path: str | Path) -> str:
        return get_module_str('.', str(other_path))

    def get_module_for_tests(self, other_path: str | Path) -> str:
        return self.app_foldername + get_module_str('.', str(other_path))

    def get_module_for_alembic(self, other_path: str | Path) -> str:
        return self.app_foldername + get_module_str('.', str(other_path))

    @staticmethod
    def _format(s: str, app_obj: AppObject) -> str:
        return s.format(
            name=app_obj.name,
            class_name=app_obj.class_name,
            table_name=app_obj.table_name,
            route_name=app_obj.route_name,
            plural_class_name=app_obj.plural_class_name,
        )

    def get_modul_path(self, string_path: str, app_obj: AppObject) -> Path:
        path = Path(self._format(string_path, app_obj))
        return path


config_kludex = NameConfig(
    database_file='core/database',
    base_file='models/base',
    dependency_file='api/deps',
    settings_file='core/config',
    model_file='models/{name}_model',
    route_file='api/v1/{name}_route',
    main_route_file='api/v1/routes',
    schema_file='schemas/{name}_schema',
    common_schema_file='schemas/common',
    repository_file='repo/{name}_repo',
    repository_main_file='repo/base_repo',
    service_file='services/{name}_service',
    alembic_folder='app/database/migrations',
)

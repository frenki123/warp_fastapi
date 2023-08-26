from ..main import AppObject


class NameConfig:
    database_file: str = 'database'
    base_file: str = 'base'
    dependency_file: str = 'dependancies'
    settings_file: str = 'settings'
    model_folder: str = 'models'
    model_extension: str = '_model'
    route_folder: str = 'routes'
    route_extension: str = '_route'
    main_route_filename: str = 'main_routes'
    base_schema_ext: str = 'Base'
    create_schema_ext: str = 'Create'
    read_schema_ext: str = 'Response'
    read_full_schema_ext: str = 'Info'
    edit_schema_ext: str = 'Edit'
    db_schema_ext: str = 'Database'
    pagination_schema_ext: str = 'Response'
    schema_folder: str = 'schemas'
    schema_extension: str = '_schema'
    common_schema_filename: str = 'common_schema'
    repository_folder: str = 'repository'
    repository_extension: str = '_repository'
    repository_main_class_name: str = 'Repository'
    repository_main_class_filename: str = 'base'
    repository_class_ext: str = 'Repository'
    service_folder: str = 'services'
    service_extension: str = '_service'
    service_class_ext: str = 'Service'
    app_foldername: str = 'app'

    def model_module(self, obj: AppObject) -> str:
        return f'{self.model_folder}.{obj.name}{self.model_extension}'

    def model_name(self, obj: AppObject) -> str:
        return f'{obj.name}{self.model_extension}'

    def model_class(self, obj: AppObject) -> str:
        return obj.class_name

    def route_module(self, obj: AppObject) -> str:
        return f'{self.route_folder}.{obj.name}{self.route_extension}'

    def main_route_module(self) -> str:
        return f'{self.route_folder}.{self.main_route_filename}'

    def route_name(self, obj: AppObject) -> str:
        return f'{obj.name}{self.route_extension}'

    def schema_module(self, obj: AppObject) -> str:
        return f'{self.schema_folder}.{obj.name}{self.schema_extension}'

    def common_schema_module(self) -> str:
        return f'{self.schema_folder}.{self.common_schema_filename}'

    def schema_name(self, obj: AppObject) -> str:
        return f'{obj.name}{self.schema_extension}'

    def read_schema(self, obj: AppObject) -> str:
        return f'{obj.class_name}{self.read_schema_ext}'

    def base_schema(self, obj: AppObject) -> str:
        return f'{obj.class_name}{self.base_schema_ext}'

    def create_schema(self, obj: AppObject) -> str:
        return f'{obj.class_name}{self.create_schema_ext}'

    def edit_schema(self, obj: AppObject) -> str:
        return f'{obj.class_name}{self.edit_schema_ext}'

    def pagination_schema(self, obj: AppObject) -> str:
        return f'{obj.plural_class_name}{self.pagination_schema_ext}'

    def repo_module(self, obj: AppObject) -> str:
        return f'{self.repository_folder}.{obj.name}{self.repository_extension}'

    def repo_name(self, obj: AppObject) -> str:
        return f'{obj.name}{self.repository_extension}'

    def repo_class(self, obj: AppObject) -> str:
        return f'{obj.class_name}{self.repository_class_ext}'

    def service_module(self, obj: AppObject) -> str:
        return f'{self.service_folder}.{obj.name}{self.service_extension}'

    def service_name(self, obj: AppObject) -> str:
        return f'{obj.name}{self.service_extension}'

    def service_class(self, obj: AppObject) -> str:
        return f'{obj.class_name}{self.service_class_ext}'

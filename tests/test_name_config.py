from warp_fastapi import AppObject
from warp_fastapi.code.config import NameConfig


def test_config(app_obj: AppObject):
    config = NameConfig()
    config.main_route_filename = 'test_route'
    assert config.model_module(app_obj) == 'models.app_model'
    assert config.model_name(app_obj) == 'app_model'
    assert config.model_class(app_obj) == 'App'
    assert config.route_module(app_obj) == 'routes.app_route'
    assert config.main_route_module() == 'routes.test_route'
    assert config.route_name(app_obj) == 'app_route'
    assert config.schema_module(app_obj) == 'schemas.app_schema'
    assert config.common_schema_module() == 'schemas.common_schema'
    assert config.schema_name(app_obj) == 'app_schema'
    assert config.read_schema(app_obj) == 'AppResponse'
    assert config.base_schema(app_obj) == 'AppBase'
    assert config.create_schema(app_obj) == 'AppCreate'
    assert config.edit_schema(app_obj) == 'AppEdit'
    assert config.pagination_schema(app_obj) == 'AppsResponse'
    assert config.repo_module(app_obj) == 'repository.app_repository'
    assert config.repo_name(app_obj) == 'app_repository'
    assert config.repo_class(app_obj) == 'AppRepository'
    assert config.service_module(app_obj) == 'services.app_service'
    assert config.service_name(app_obj) == 'app_service'
    assert config.service_class(app_obj) == 'AppService'

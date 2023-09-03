from warp_fastapi import AppObject
from warp_fastapi.code.config import NameConfig
from pathlib import Path
import pytest


def test_main_config(app_obj: AppObject):
    config = NameConfig()
    assert config.get_database_filename() == 'database'
    assert config.get_database_folder() == '.'
    assert config.get_database_path() == 'database'
    assert config.get_module_for_database(
        "folder1/folder2/file") == '.folder1.folder2.file'
    assert config.get_base_filename() == 'base'
    assert config.get_base_folder() == '.'
    assert config.get_base_path() == str(Path('base'))
    assert config.get_module_for_base("file") == '.file'
    assert config.get_dependency_filename() == 'dependancies'
    assert config.get_dependency_folder() == '.'
    assert config.get_dependency_path() == str(Path('dependancies'))
    assert config.get_module_for_dependency("mod1/mod2") == '.mod1.mod2'
    assert config.get_settings_filename() == 'settings'
    assert config.get_settings_folder() == '.'
    assert config.get_settings_path() == str(Path('settings'))
    assert config.get_module_for_settings("x") == '.x'
    assert config.get_model_filename(app_obj) == 'app_model'
    assert config.get_model_folder(app_obj) == 'models'
    assert config.get_model_path(app_obj) == str(Path('models/app_model'))
    assert config.get_module_for_model(app_obj, "models/add/other") == '.add.other'
    assert config.get_module_for_model(app_obj, "base/other") == '..base.other'
    assert config.get_route_filename(app_obj) == 'app_route'
    assert config.get_route_folder(app_obj) == 'routes'
    assert config.get_route_path(app_obj) == str(Path('routes/app_route'))
    assert config.get_module_for_route(app_obj, "base") == '..base'
    assert config.get_main_route_filename() == 'main_routes'
    assert config.get_main_route_folder() == 'routes'
    assert config.get_main_route_path() == str(Path('routes/main_routes'))
    assert config.get_module_for_main_route('routes/other') == '.other'
    assert config.get_schema_filename(app_obj) == 'app_schema'
    assert config.get_schema_folder(app_obj) == 'schemas'
    assert config.get_schema_path(app_obj) == str(Path('schemas/app_schema'))
    assert config.get_module_for_schema(app_obj, "m") == '..m'
    assert config.get_base_cls_schema(app_obj) == 'AppBase'
    assert config.get_create_cls_schema(app_obj) == 'AppCreate'
    assert config.get_read_cls_schema(app_obj) == 'AppResponse'
    assert config.get_read_full_cls_schema(app_obj) == 'AppInfo'
    assert config.get_edit_cls_schema(app_obj) == 'AppEdit'
    assert config.get_db_cls_schema(app_obj) == 'AppDatabase'
    assert config.get_common_schema_filename() == 'common_schema'
    assert config.get_common_schema_folder() == 'schemas'
    assert config.get_common_schema_path() == str(Path('schemas/common_schema'))
    assert config.get_module_for_common_schema('schemas/a') == '.a'
    assert config.get_pagination_cls_schema(app_obj) == 'AppsResponse'
    assert config.get_repository_filename(app_obj) == 'app_repository'
    assert config.get_repository_folder(app_obj) == 'repository'
    assert config.get_repository_path(app_obj) == str(Path('repository/app_repository'))
    assert config.get_module_for_repository(app_obj, 'a/b/c') == '..a.b.c'
    assert config.get_repo_classname(app_obj) == 'AppRepository'
    assert config.get_repository_main_filename() == 'base'
    assert config.get_repository_main_folder() == 'repository'
    assert config.get_repository_main_path() == str(Path('repository/base'))
    assert config.get_module_for_repository_main("a") == '..a'
    assert config.get_service_filename(app_obj) == 'app_service'
    assert config.get_service_folder(app_obj) == 'services'
    assert config.get_service_path(app_obj) == str(Path('services/app_service'))
    assert config.get_module_for_service(app_obj, 'services/a') == '.a'
    assert config.get_service_classname(app_obj) == 'AppService'
    assert config.get_module_for_main('a/b/c/d') == '.a.b.c.d'
    assert config.get_module_for_main('r') == '.r'


def test_wird_config(app_obj: AppObject):
    config = NameConfig(database_file='database/folder2/main',
                        model_file='{name}/model_{name}')
    #assert standard which will be chagned later with update
    assert config.get_schema_filename(app_obj) == 'app_schema'
    assert config.get_schema_folder(app_obj) == 'schemas'
    assert config.get_schema_path(app_obj) == str(Path('schemas/app_schema'))
    assert config.get_module_for_schema(app_obj, "m") == '..m'
    assert config.get_base_cls_schema(app_obj) == 'AppBase'
    #assert changes
    assert config.get_database_filename() == 'main'
    assert config.get_database_folder() == str(Path('database/folder2'))
    assert config.get_database_path() == str(Path('database/folder2/main'))
    assert config.get_module_for_database(
        "folder1/folder2/file") == '...folder1.folder2.file'
    assert config.get_module_for_database(
        "database/folder2/a") == '.a'
    assert config.get_module_for_database(
        "database/b/a") == '..b.a'
    
    assert config.get_model_filename(app_obj) == 'model_app'
    assert config.get_model_folder(app_obj) == 'app'
    assert config.get_model_path(app_obj) == str(Path('app/model_app'))
    assert config.get_module_for_model(app_obj, "models/add/other") == '..models.add.other'
    assert config.get_module_for_model(app_obj, "app/other") == '.other'

    config.update_config(schema_file='{class_name}/{name}/schema',
                         base_schema_tmpl='{name}SomethingElse')

    assert config.get_schema_filename(app_obj) == 'schema'
    assert config.get_schema_folder(app_obj) == str(Path('App/app'))
    assert config.get_schema_path(app_obj) == str(Path('App/app/schema'))
    assert config.get_module_for_schema(app_obj, "m") == '...m'
    assert config.get_base_cls_schema(app_obj) == 'appSomethingElse'

    with pytest.raises(AttributeError) as e:
        NameConfig(wrong_key="something") # type: ignore [call-arg]
    assert "'NameConfig' object has no attribute 'wrong_key'" in str(e) 







































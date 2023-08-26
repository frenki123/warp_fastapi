from pathlib import Path

from warp_fastapi import AppProject
from warp_fastapi.create_project import ProjectCreator


def file_contains(filepath: Path, text: str):
    c = filepath.read_text()
    return text in c


def file_is_empty(filepath: Path):
    c = filepath.read_text()
    return c == ''


def test_poject_creator_init(app_proj: AppProject, tmp_path: Path):
    creator = ProjectCreator(app_proj, str(tmp_path))
    creator.create_project()
    proj_dir = tmp_path / creator.project.name
    assert proj_dir.is_dir()
    app_dir = proj_dir / 'app'
    assert app_dir.is_dir()
    test_dir = proj_dir / 'tests'
    assert test_dir.is_dir()
    req_file = proj_dir / 'requirements.txt'
    assert req_file.is_file()
    assert file_contains(req_file, 'fastapi[all]')
    startup_f = proj_dir / 'startup.sh'
    assert startup_f.is_file()
    assert file_contains(startup_f, '.venv')
    test_init = test_dir / '__init__.py'
    assert file_is_empty(test_init)
    models_dir = app_dir / 'models'
    assert models_dir.is_dir()
    service_f = app_dir / 'services/obj1_service.py'
    assert file_contains(service_f, 'update_obj1')
    service_f.write_text('SOME TEST FOR TESTING')
    creator.requirements = ['req1', 'test_req']
    creator.update_project()
    assert not file_contains(service_f, 'SOME TEST FOR TESTING')
    assert not file_contains(req_file, 'fastapi[all]')
    assert file_contains(req_file, 'req1')

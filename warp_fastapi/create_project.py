from pathlib import Path

from .code.alembic.alembic import (
    get_alembic_env_code,
    get_alembic_ini_code,
    get_alembic_readme,
    get_script_py_mako,
)
from .code.code_objects.base import AbstractModuleCode
from .code.code_objects.database import BaseModuleCode, DatabaseModuleCode
from .code.code_objects.dependacies import DependanciesModuleCode
from .code.code_objects.main import MainModuleCode
from .code.code_objects.model import ModelModuleCode
from .code.code_objects.repository import RepoBaseModule, RepoModuleCode
from .code.code_objects.routes import MainRouterCode, RoutesModuleCode
from .code.code_objects.schema import CommonSchemaModule, SchemaModuleCode
from .code.code_objects.service import ServiceModuleCode
from .code.code_objects.settings import SettingsModuleCode
from .code.code_objects.tests import ConfTestModuleCode, TestModuleCode
from .code.config import NameConfig
from .main import AppObject, AppProject


# TODO:create app in temp dir first, run black and ruff then copy to main folder
class ProjectCreator:
    def __init__(
        self,
        project: AppProject,
        project_dir: str = '.',
        config: NameConfig = NameConfig(),
        env_file: str = '.env',
        requirements: list[str] = [],
    ):
        self.project = project
        self.config = config
        self.project_dir = Path(project_dir, project.name)
        self.app_dir = self.project_dir / config.app_foldername
        self.test_dir = self.project_dir / 'tests'
        self.requirements = ['fastapi[all]', 'sqlalchemy', 'alembic', 'black', 'ruff', 'pytest', 'pytest-cov', 'mypy']
        if requirements:
            self.requirements = requirements  # pragma: no cover
        self.env_file = env_file

    def create_project(self) -> None:
        self._generate(False)

    def update_project(self) -> None:
        self._generate(True)

    def _generate(self, update: bool) -> None:
        self.app_dir.mkdir(parents=True, exist_ok=update)
        self.test_dir.mkdir(parents=True, exist_ok=update)
        init_file = self.app_dir / '__init__.py'
        init_file.write_text('')
        test_init_file = self.test_dir / '__init__.py'
        test_init_file.write_text('')
        for obj in self.project.app_objects:
            self._generate_obj_code(obj, update)
        self._generate_const_file(update)
        self._generate_alembic(update)
        self._copy_env_file()
        self._generate_requirements_txt()
        self._generate_startup_script()

    def _generate_const_file(self, update: bool) -> None:
        const_modules: list[AbstractModuleCode] = [
            MainModuleCode(self.project, self.config),
            DatabaseModuleCode(self.config),
            DependanciesModuleCode(self.config),
            SettingsModuleCode(self.config, self.project.name),
            CommonSchemaModule(self.config),
            BaseModuleCode(self.project.app_objects, self.config),
            RepoBaseModule(self.config),
            MainRouterCode(self.project.app_objects, self.config),
        ]

        for module in const_modules:
            self._write_module(module, update, self.app_dir)

        test_modules: list[AbstractModuleCode] = [
            TestModuleCode(self.project.app_objects, self.config),
            ConfTestModuleCode(self.project.app_objects, self.config),
        ]
        for module in test_modules:
            self._write_module(module, update, self.test_dir)

    def _generate_obj_code(self, obj: AppObject, update: bool) -> None:
        modules = self._generate_modules(obj)
        for module in modules:
            self._write_module(module, update, self.app_dir)

    def _write_module(self, module: AbstractModuleCode, update: bool, main_dir: Path) -> None:
        dir = main_dir / module.folder
        if not dir.exists():
            dir.mkdir(parents=True, exist_ok=update)
            init_file = dir / '__init__.py'
            init_file.write_text('')
        module_file = dir / (module.filename + '.py')
        module_file.write_text(str(module))

    def _generate_modules(self, obj: AppObject) -> list[AbstractModuleCode]:
        return [
            ModelModuleCode(obj, self.config),
            RepoModuleCode(obj, self.config),
            RoutesModuleCode(obj, self.config),
            SchemaModuleCode(obj, self.config),
            ServiceModuleCode(obj, self.config),
        ]

    def _generate_alembic(self, update: bool) -> None:
        alembic_dir = self.project_dir / self.config.alembic_folder
        alembic_dir.mkdir(parents=True, exist_ok=update)
        alembic_ini = self.project_dir / 'alembic.ini'
        alembic_ini.write_text(get_alembic_ini_code(self.config))
        versions_dir = alembic_dir / 'versions'
        versions_dir.mkdir(parents=True, exist_ok=update)
        env_file = alembic_dir / 'env.py'
        env_file.write_text(get_alembic_env_code(self.config))
        readme_file = alembic_dir / 'README'
        readme_file.write_text(get_alembic_readme())
        mako_file = alembic_dir / 'script.py.mako'
        mako_file.write_text(get_script_py_mako())

    def _copy_env_file(self) -> None:
        dest = self.project_dir / '.env'
        src = Path(self.env_file)
        if src.is_file():
            dest.write_text(src.read_text())
            return None
        env_template = """
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
"""
        dest.write_text(env_template)

    def _generate_requirements_txt(self) -> None:
        file = self.project_dir / 'requirements.txt'
        txt = '\n'.join(self.requirements)
        file.write_text(txt)

    def _generate_startup_script(self) -> None:
        script_file = self.project_dir / 'startup.sh'
        script = """#!/bin/bash
echo "Creating virtual enviroment .venv"
python -m venv .venv
source ./.venv/Scripts/activate
echo "Instaling requirements"
pip install -r requirements.txt
echo "Lint and formating check"
black app
ruff app --fix
black app
echo "Database initial migration"
alembic revision -m "Tables creation" --autogenerate
alembic upgrade head
echo "mypy check"
mypy .
echo "tests"
pytest --cov
echo "starting app"
uvicorn app.main:app --reload"""

        script_file.write_text(script)

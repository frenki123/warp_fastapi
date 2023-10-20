from ... import AppProject
from ...config import StructureConfig
from .base import (
    SimpleModuleCode,
)


class MainModuleCode(SimpleModuleCode):
    def __init__(self, project: AppProject, config: StructureConfig = StructureConfig()):
        self.folder = ''
        self.filename = 'main'
        self.settings_module = config.get_module_for_main(config.get_settings_path())
        self.main_route_module = config.get_module_for_main(config.get_main_route_path())

    def __str__(self) -> str:
        return f"""from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from {self.main_route_module} import router
from {self.settings_module} import settings

app = FastAPI(title=settings.PROJECT_NAME)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix=settings.API_V1_STRING)
"""

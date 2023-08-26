from warp_fastapi import AppProject
from warp_fastapi.code.code_objects.main import MainModuleCode
from warp_fastapi.code.config import NameConfig

from .conftest import assert_code_lines


def test_main_module(app_proj: AppProject):
    config = NameConfig()
    m = MainModuleCode(app_proj, config)
    r = """
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routes.main_routes import router
from .settings import settings

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
    assert_code_lines(m, r)

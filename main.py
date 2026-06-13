from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.core.logger import configure_logging
from app.routers import analysis_router, api_router, page_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize application resources during startup."""
    if settings.auto_create_tables:
        init_db()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()
    app = FastAPI(
        title=settings.app_name,
        description="二手房数据采集、清洗、分析与可视化展示系统",
        version="0.1.0",
        debug=settings.app_debug,
        lifespan=lifespan,
    )
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(page_router.router)
    app.include_router(api_router.router)
    app.include_router(analysis_router.router)

    return app


app = create_app()

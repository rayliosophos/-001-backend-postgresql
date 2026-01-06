from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from fastapi.staticfiles import StaticFiles
from app.middleware import setup_middlewares
from app.api.v1.router import router as v1_router


def create_app() -> FastAPI:
    
    setup_logging(level=settings.LOG_LEVEL)

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url=None if settings.PRODUCTION else "/docs",
        redoc_url=None if settings.PRODUCTION else "/redoc",
        openapi_url=None if settings.PRODUCTION else "/openapi.json",
        lifespan=lifespan,
    )
    
    # Middleware
    setup_middlewares(app)
    
    # 
    app.mount("/static", StaticFiles(directory="static"), name="static" )

    # Routers
    app.include_router(v1_router, prefix="/api/v1")

    return app

app = create_app()

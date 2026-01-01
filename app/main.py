from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.core.config import settings

setup_logging(level=settings.LOG_LEVEL)

app = FastAPI(
    title="Admin API",
    lifespan=lifespan,
)

app.include_router(v1_router, prefix="/api/v1")

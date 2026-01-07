import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.postgres import init_pg_pool, close_pg_pool

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # STARTUP
    await init_pg_pool()
    logger.info("PostgreSQL asyncpg pool initialized")

    yield

    # SHUTDOWN
    await close_pg_pool()
    logger.info("PostgreSQL asyncpg pool closed")

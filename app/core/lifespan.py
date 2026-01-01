import logging
from fastapi import FastAPI
# from app.db.oracle import oracle_pool
from contextlib import asynccontextmanager
from app.db.postgres import init_pg_pool, close_pg_pool

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # STARTUP
    await init_pg_pool()
    logger.info("PostgreSQL asyncpg pool initialized")

    # Oracle pool is created at import time (acceptable for oracledb)
    # print("Oracle pool ready")

    yield

    # SHUTDOWN
    await close_pg_pool()
    logger.info("PostgreSQL asyncpg pool closed")

    # if oracle_pool:
    #     oracle_pool.close()
    #     print("Oracle pool closed")
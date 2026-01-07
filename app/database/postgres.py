import asyncpg
from typing import Optional
from app.core.config import settings

_pg_pool: Optional[asyncpg.Pool] = None

async def init_pg_pool() -> None:
    global _pg_pool
    if _pg_pool is None:
        _pg_pool = await asyncpg.create_pool(
            dsn=settings.POSTGRES_DSN,
            min_size=5,
            max_size=20,
            command_timeout=30,
        )

async def close_pg_pool() -> None:
    global _pg_pool
    if _pg_pool:
        await _pg_pool.close()
        _pg_pool = None

def get_pg_pool() -> asyncpg.Pool:
    if _pg_pool is None:
        raise RuntimeError("PostgreSQL pool is not initialized")
    return _pg_pool

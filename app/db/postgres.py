import asyncpg
from app.core.config import settings

_pg_pool: asyncpg.Pool | None = None

async def init_pg_pool() -> None:
    global _pg_pool
    _pg_pool = await asyncpg.create_pool(
        dsn=settings.POSTGRES_DSN,
        min_size=10,
        max_size=50,
        command_timeout=30,
    )

async def close_pg_pool() -> None:
    if _pg_pool:
        await _pg_pool.close()

def get_pg_pool() -> asyncpg.Pool:
    if not _pg_pool:
        raise RuntimeError("PostgreSQL pool not initialized")
    return _pg_pool
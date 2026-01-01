import asyncpg
from typing import AsyncGenerator
from app.db.postgres import get_pg_pool

async def get_pg_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    pool = get_pg_pool()
    conn: asyncpg.Connection = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)
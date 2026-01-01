from datetime import datetime
from app.db.postgres import get_pg_pool
class LoginRepository:

    async def is_user_exist(self, username: str) -> dict | None:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow( "select * from f_is_user_exist($1)", username)
        if not row:
            return None
        return dict(row) if row else None
        
    async def register_token(self, guid: str, access_token: str, refresh_token : str, expiration: datetime) -> bool:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            result = await conn.fetchval( "select f_register_token($1, $2, $3, $4)", guid, access_token, refresh_token, expiration)
        return result == "SUCCESS"

    async def is_authorized(self, guid: str, access_token: str, code: str) -> bool:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            result = await conn.fetchval( "select f_is_authorized($1, $2, $3)", guid, access_token, code)
        return result == "SUCCESS"
    
    async def revoke_token(self, access_token: str) -> bool:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            result = await conn.fetchval( "select f_revoke_token($1)", access_token)
        return result == "SUCCESS"
    
    async def refresh_token(self, refresh_token: str) -> str | None:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            result = await conn.fetchval( "select f_refresh_token($1)", refresh_token)
        return result
    
    
import logging
from datetime import datetime
from app.db.postgres import get_pg_pool

logger = logging.getLogger(__name__)

class LoginRepository:

    async def is_user_exist(self, username: str) -> dict | None:
        try:
            pool = get_pg_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow("select * from f_is_user_exist($1)", username)
            if not row:
                return None
            return dict(row) if row else None
        except Exception as e:
            logger.error("Error checking user existence: %s", e)
            return None
        
    async def register_token(self, guid: str, access_token: str, refresh_token : str, expiration: datetime) -> bool:
        try:
            pool = get_pg_pool()
            async with pool.acquire() as conn:
                result = await conn.fetchval("select f_register_token($1, $2, $3, $4)", guid, access_token, refresh_token, expiration)
            return result == "SUCCESS"
        except Exception as e:
            logger.error("Error registering token: %s", e)
            return False
        
    async def is_authorized(self, guid: str, access_token: str, code: str) -> bool:
        try:
            pool = get_pg_pool()
            async with pool.acquire() as conn:
                result = await conn.fetchval("select f_is_authorized($1, $2, $3)", guid, access_token, code)
            return result == "SUCCESS"
        except Exception as e:
            logger.error("Error checking authorization: %s", e)
            return False
    
    async def revoke_token(self, access_token: str) -> bool:
        try:
            pool = get_pg_pool()
            async with pool.acquire() as conn:
                result = await conn.fetchval("select f_revoke_token($1)", access_token)
            return result == "SUCCESS"
        except Exception as e:
            logger.error("Error revoking token: %s", e)
            return False
        
    async def refresh_token(self, guid: str, refresh_token: str) -> str | None:
        try:
            pool = get_pg_pool()
            async with pool.acquire() as conn:
                result = await conn.fetchval("select f_refresh_token($1, $2)", guid, refresh_token)
            return result
        except Exception as e:
            logger.error("Error refreshing token: %s", e)
            return None
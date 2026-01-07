import uuid
import logging
import asyncpg
from app.core.config import settings
from fastapi.responses import JSONResponse
from app.core.security import create_access_token
from datetime import datetime, timezone, timedelta
from app.utils.response_handler import ResponseHandler
from app.repositories.postgres.login_repository import LoginRepository

logger = logging.getLogger(__name__)

class LoginService:
    def __init__(self):
        self.pg_login_repo = LoginRepository()
        
    async def generate_access_token(self, *, conn: asyncpg.Connection, username: str) -> JSONResponse:
        is_user_exist  = await self.pg_login_repo.is_user_exist(conn=conn, username=username)
        if not is_user_exist:
            logger.warning("User not found: %s", username)
            return ResponseHandler.generate_response_unsuccessful(404, "Error generating token for user.")
        refresh_token = str(uuid.uuid4())
        token = create_access_token(subject=is_user_exist["guid"], jti= refresh_token)
        registered = await self.pg_login_repo.register_token(
            conn=conn,
            guid=is_user_exist["guid"],
            access_token=token,
            refresh_token=refresh_token,
            expiration= datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        )
        if not registered:
            logger.error("Failed to register token for user.")
            return ResponseHandler.generate_response_unsuccessful(500, "Error generating token for user.")
        return ResponseHandler.generate_response_successful(
            "Access token generated successfully.", 
            {
                "last_login": is_user_exist["last_login"],
                "access_token": token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
            }
        )
    
    async def revoke_token(self, *, conn: asyncpg.Connection, access_token: str) -> JSONResponse:
        revoked = await self.pg_login_repo.revoke_token(conn=conn, access_token=access_token)
        if not revoked:
            logger.error("Failed to revoke token.")
            return ResponseHandler.generate_response_unsuccessful(500, "Error revoking token.")
        return ResponseHandler.generate_response_successful("Token revoked successfully.", None)

    async def refresh_token(self, *, conn: asyncpg.Connection, guid: str, refresh_token: str) -> JSONResponse:
        username  = await self.pg_login_repo.refresh_token(conn=conn, guid=guid, refresh_token=refresh_token)
        if not username:
            logger.warning("Invalid refresh token.")
            return ResponseHandler.generate_response_unsuccessful(400, "Invalid refresh token.")
        return await self.generate_access_token(conn=conn,username=username)
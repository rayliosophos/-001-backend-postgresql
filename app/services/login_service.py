import uuid
import logging
from app.core.config import settings
from fastapi.responses import JSONResponse
from app.core.security import create_access_token
from datetime import datetime, timezone, timedelta
from app.utils.response_handler import ResponseHandler
from app.repositories.postgres.login_repo import LoginRepository

logger = logging.getLogger(__name__)

class LoginService:
    def __init__(self):
        self.pg_repo = LoginRepository()
        
    async def generate_access_token(self, username: str) -> JSONResponse:
        logger.info("Generating access token for user.")
        is_user_exist  = await self.pg_repo.is_user_exist(username)
        if not is_user_exist:
            logger.warning("User not found: %s", username)
            return ResponseHandler.generate_response_unsuccessful(404, "Error generating token for user.")
        refresh_token = str(uuid.uuid4())
        token = create_access_token(subject=is_user_exist["guid"], jti= refresh_token)
        registered = await self.pg_repo.register_token(
            guid=is_user_exist["guid"],
            access_token=token,
            refresh_token=refresh_token,
            expiration= datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        )
        if not registered:
            logger.error("Failed to register token for user.")
            return ResponseHandler.generate_response_unsuccessful(500, "Error generating token for user.")
        logger.info("Access token generated for user.")
        json_response = ResponseHandler.generate_response_successful(
            "Access token generated successfully.", 
            {
                "last_login": is_user_exist["last_login"],
                "access_token": token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
            }
        )
        # Set HTTP-only secure cookie
        json_response.set_cookie(
            key="to_hNPdrSwfeLK",
            value=token,
            httponly=True,
            secure=True,
            samesite ="strict",
            max_age = settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
            path="/"
        )
        
        return json_response
    
    async def revoke_token(self, access_token: str) -> JSONResponse:
        logger.info("Revoking token.")
        revoked = await self.pg_repo.revoke_token(access_token)
        if not revoked:
            logger.error("Failed to revoke token.")
            return ResponseHandler.generate_response_unsuccessful(500, "Error revoking token.")
        logger.info("Token revoked successfully.")
        json_response = ResponseHandler.generate_response_successful("Token revoked successfully.", None)
        json_response.delete_cookie(
            key="to_hNPdrSwfeLK",
            path="/",
            httponly=True,
            secure=True,
            samesite="strict"
        )
        return json_response
    
    async def refresh_token(self, refresh_token: str) -> JSONResponse:
        logger.info("Refreshing token for user.")
        username  = await self.pg_repo.refresh_token(refresh_token)
        if not username:
            logger.warning("Invalid refresh token.")
            return ResponseHandler.generate_response_unsuccessful(400, "Invalid refresh token.")
        return await self.generate_access_token(username)
    
    
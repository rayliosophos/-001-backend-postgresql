import logging
from typing import List
from app.core.security import decode_token
from fastapi import Depends, HTTPException, status
from app.repositories.postgres.login_repo import LoginRepository
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
logger = logging.getLogger(__name__)

def require_permissions(required: List[str]):
    async def checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            logger.info("Verifying permissions for token.")
            payload = decode_token(credentials.credentials)
            login_repo = LoginRepository()
            is_authorized = await login_repo.is_authorized(payload.get("sub"), credentials.credentials, required[0])
            if not is_authorized:
                logger.warning("Invalid or insufficient permissions.")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or insufficient permissions.",
                )
        except HTTPException:
            raise
        except Exception:
            logger.warning("Invalid or expired token.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
    return checker

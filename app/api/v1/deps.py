
import logging
import asyncpg
from app.core.security import decode_token
from app.database.postgres import get_pg_pool
from app.services.ldap_service import LDAPService
from typing import List, Callable, AsyncGenerator
from fastapi import Depends, HTTPException, status
from app.services.users_service import UserService
from app.services.login_service import LoginService
from app.services.audit_service import AuditService
from app.services.permissions_service import PermissionService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.repositories.postgres.login_repository import LoginRepository

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)

async def get_db_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    pool = get_pg_pool()
    async with pool.acquire() as conn:
        yield conn

def get_user_service() -> UserService:
    return UserService()

def get_audit_service() -> AuditService:
    return AuditService()
  
def get_ldap_service() -> LDAPService:
    return LDAPService()
  
def get_login_service() -> LoginService:
    return LoginService()
  
def get_permission_service() -> PermissionService:
    return PermissionService()

def get_login_repository() -> LoginRepository:
    return LoginRepository()

def require_permissions(required_permissions: List[str]) -> Callable:
    async def checker(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        login_repo: LoginRepository = Depends(get_login_repository),
        conn: asyncpg.Connection = Depends(get_db_conn),
    ) -> str:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization credentials missing")
        try:
            payload = decode_token(credentials.credentials)
            guid: str | None = payload.get("sub")
            if not guid:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            for permission in required_permissions:
                authorized = await login_repo.is_authorized(conn=conn, guid=guid, access_token=credentials.credentials, code=permission)
                if not authorized:
                    logger.warning("Permission denied | user=%s | permission=%s", guid, permission)
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
            return guid
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Token validation failed")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc
    return checker

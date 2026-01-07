import logging
import asyncpg
from fastapi import APIRouter, Depends
from app.services.ldap_service import LDAPService
from app.services.login_service import LoginService
from app.utils.response_handler import ResponseHandler
from app.schemas.request.login_request import LoginRequest
from app.schemas.request.token_request import RevokeRequest, RefreshTokenRequest
from app.api.v1.deps import get_db_conn, get_ldap_service, get_login_service, require_permissions

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
async def login(
    payload: LoginRequest, 
    ldap_service: LDAPService = Depends(get_ldap_service),
    login_service: LoginService = Depends(get_login_service),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    if not ldap_service.authenticate(username=payload.username, password=payload.password):
        logger.warning("Authentication failed for user; Reason: Invalid credentials")
        return ResponseHandler.generate_response_unsuccessful(401, "Invalid username or password")
    return await login_service.generate_access_token(conn=conn, username=payload.username)

@router.post("/revoke", dependencies=[Depends(require_permissions(["token:revoke"]))])
async def revoke(
    payload: RevokeRequest, 
    login_service: LoginService = Depends(get_login_service),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    return await login_service.revoke_token(conn=conn, access_token=payload.token)

@router.post("/refresh_token")
async def refresh_token(
    payload: RefreshTokenRequest, 
    guid: str = Depends(require_permissions(["token:refresh"])), 
    login_service: LoginService = Depends(get_login_service),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    return await login_service.refresh_token(conn=conn, guid=guid, refresh_token=payload.refresh_token)

@router.get("/validate", dependencies=[Depends(require_permissions(["token-validation:read"]))])
async def validate_token():
    return ResponseHandler.generate_response_successful("Token validated successfully.", None)


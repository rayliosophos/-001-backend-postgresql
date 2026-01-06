import logging
from fastapi import APIRouter, Depends
from app.services.ldap_service import LDAPService
from app.services.login_service import LoginService
from app.utils.response_handler import ResponseHandler
from app.dependencies.ldap_dep import get_ldap_service
from app.dependencies.login_dep import get_login_service
from app.dependencies.security_dep import get_current_sub
from app.schemas.request.login_request import LoginRequest
from app.dependencies.require_permission_dep import require_permissions
from app.schemas.request.token_request import RevokeRequest, RefreshTokenRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
async def login(
    payload: LoginRequest, 
    ldap_service: LDAPService = Depends(get_ldap_service),
    login_service: LoginService = Depends(get_login_service),
):
    if not ldap_service.authenticate(payload.username, payload.password):
        logger.warning("Authentication failed for user; Reason: Invalid credentials")
        return ResponseHandler.generate_response_unsuccessful(401, "Invalid username or password")
    return await login_service.generate_access_token(payload.username)

@router.post("/revoke", dependencies=[Depends(require_permissions(["token:revoke"]))])
async def revoke(
    payload: RevokeRequest, 
    login_service: LoginService = Depends(get_login_service)
):
    return await login_service.revoke_token(payload.token)

@router.post("/refresh_token", dependencies=[Depends(require_permissions(["token:refresh"]))])
async def refresh_token(payload: RefreshTokenRequest, guid: str = Depends(get_current_sub), login_service: LoginService = Depends(get_login_service)):
    return await login_service.refresh_token(guid, payload.refresh_token)

@router.get("/validate", dependencies=[Depends(require_permissions(["token-validation:read"]))])
async def validate_token():
    return ResponseHandler.generate_response_successful("Token validated successfully.", None)


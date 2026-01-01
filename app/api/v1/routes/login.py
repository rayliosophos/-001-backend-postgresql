import logging
from fastapi import APIRouter, Depends
from app.utils.mask_handler import MaskHandler
from app.services.ldap_service import LDAPService
from app.services.login_service import LoginService
from app.utils.response_handler import ResponseHandler
from app.schemas.request.login_request import LoginRequest
from app.dependencies.permissions import require_permissions
from app.dependencies.login_service import get_login_service
from app.schemas.request.token_request import RevokeRequest, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

@router.post("/token")
async def login(request: LoginRequest, login_service: LoginService = Depends(get_login_service)):
    logger.info("Processing authentication request for user %s.", MaskHandler.mask_username(request.username))
    ldap_service = LDAPService()
    if not ldap_service.authenticate(request.username, request.password):
        logger.warning("Authentication failed for user; Reason: Invalid credentials")
        return ResponseHandler.generate_response_unsuccessful(401, "Invalid username or password")
    return await login_service.generate_access_token(request.username)

@router.post("/revoke", dependencies=[Depends(require_permissions(["token:revoke"]))])
async def revoke(request: RevokeRequest, login_service: LoginService = Depends(get_login_service)):
    logger.info("Processing token revocation request.")
    return await login_service.revoke_token(request.token)

@router.post("/refresh_token", dependencies=[Depends(require_permissions(["token:refresh"]))])
async def refresh_token(request: RefreshTokenRequest, login_service: LoginService = Depends(get_login_service)):
    logger.info("Processing token refresh request.")
    return await login_service.refresh_token(request.refresh_token)

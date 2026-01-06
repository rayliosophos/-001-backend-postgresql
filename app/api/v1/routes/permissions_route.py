import logging
from app.services.audit_service import AuditService
from app.utils.response_handler import ResponseHandler
from app.dependencies.audit_dep import get_audit_service
from app.dependencies.security_dep import get_current_sub
from app.services.permissions_service import PermissionService
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from app.dependencies.permissions_dep import get_permission_service
from app.dependencies.require_permission_dep import require_permissions
from app.schemas.request.permissions_role_request import PermissionsRoleRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/permission", tags=["Permission"])

@router.get("/get-roles", dependencies=[Depends(require_permissions(["permission:read"]))])
async def get_roles(
    permission_service: PermissionService = Depends(get_permission_service),
):
    return ResponseHandler.generate_response_successful("Roles list retrieved successfully.", await permission_service.get_list_roles())

@router.get("/get-permissions-detail", dependencies=[Depends(require_permissions(["permission:read"]))])
async def get_permissions_detail(
    role_id: int,
    permission_service: PermissionService = Depends(get_permission_service),
):
    return ResponseHandler.generate_response_successful("Permissions detail retrieved successfully.", await permission_service.get_permissions_detail(role_id))

@router.put("/assign-permissions-to-role", dependencies=[Depends(require_permissions(["permission:write"]))])
async def assign_permissions_to_role(
    request: Request,
    payload: PermissionsRoleRequest,
    background_tasks: BackgroundTasks,
    permission_service: PermissionService = Depends(get_permission_service),
    audit_service: AuditService = Depends(get_audit_service),
    guid: str = Depends(get_current_sub),
):
    result = await permission_service.assign_permissions_to_role(payload.role_id, payload.permissions)
    if result != "SUCCESS":
        return ResponseHandler.generate_response_unsuccessful(400, result)
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="EXPORT_CSV_USERS",
        resource="/user/export/csv",
        request_body=payload.model_dump(),
    )
    return ResponseHandler.generate_response_successful("Permissions assigned to role successfully.", None)
import logging
from fastapi.params import Query
from fastapi import APIRouter, Depends
from app.services.audit_service import AuditService
from app.utils.response_handler import ResponseHandler
from app.dependencies.audit_dep import get_audit_service
from app.dependencies.require_permission_dep import require_permissions

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/get-list-audit", dependencies=[Depends(require_permissions(["audit-log:read"]))])
async def get_list_audit(
    page_number: int = 1,
    page_size: int = Query(default=50, le=200),
    search: str = None,
    start_date: str = None,
    end_date: str = None,
    order_by: str = 'created_desc',
    audit_service: AuditService = Depends(get_audit_service),
):
    result = await audit_service.get_list_audit_logs(
        page_number=page_number,
        page_size=page_size,
        search=search,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by
    )
    if result["error"] != "SUCCESS":
        logger.error("Failed to retrieve audit list.")
        return ResponseHandler.generate_response_unsuccessful(400, result["error"])
    return ResponseHandler.generate_response_successful("Audit list retrieved successfully.", result)
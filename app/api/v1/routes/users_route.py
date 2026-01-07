import io
import csv
import asyncpg
import logging
from fastapi.params import Query
from fastapi.responses import StreamingResponse
from app.utils.files_handler import FilesHandler
from app.services.users_service import UserService
from app.services.audit_service import AuditService
from app.utils.response_handler import ResponseHandler
from app.schemas.request.user_request import UserRequest
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from app.api.v1.deps import get_audit_service, get_db_conn, get_user_service, require_permissions


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/get-menu")
async def get_user_menu(
    request: Request,
    background_tasks: BackgroundTasks,
    guid: str = Depends(require_permissions(["frontend-menu:read"])), 
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="GET_USER_MENU",
        resource="/user/get-user-menu",
        request_body={},
    )
    return ResponseHandler.generate_response_successful("User menu retrieved successfully.", await user_service.get_user_menu(conn=conn,guid=guid))

@router.post("/create")
async def create_user(
    request: Request,
    background_tasks: BackgroundTasks,
    payload: UserRequest,
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service),
    guid: str = Depends(require_permissions(["user:write"])),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    if payload.photo and not FilesHandler.move_to_profile_image(payload.photo):
        return ResponseHandler.generate_response_unsuccessful(400, "Moved file error.")      
    result = await user_service.create_user(conn=conn, data=payload, created_by=guid)
    if result != "SUCCESS":
        logger.error("User creation failed for payload: %s", payload)
        return ResponseHandler.generate_response_unsuccessful(400, result)
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="CREATE_USER",
        resource="/user/create",
        request_body=payload.model_dump(),
    )
    return ResponseHandler.generate_response_successful("User created successfully.", None)

@router.put("/update")
async def update_user(
    request: Request,
    background_tasks: BackgroundTasks,
    payload: UserRequest,
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service),
    guid: str = Depends(require_permissions(["user:update"])),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    payload.modify_by = guid
    result = await user_service.update_user(conn=conn, data=payload)
    if result != "SUCCESS":
        logger.error("User updating failed for payload: %s", payload)
        return ResponseHandler.generate_response_unsuccessful(400, result)
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="UPDATE_USER",
        resource="/user/update",
        request_body=payload.model_dump(),
    )
    return ResponseHandler.generate_response_successful("User updated successfully.", None)

@router.delete("/delete")
async def delete_user(
    request: Request,
    background_tasks: BackgroundTasks,
    guid_to_delete: str,
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service),
    guid: str = Depends(require_permissions(["user:delete"])),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    result = await user_service.delete_user(conn=conn, guid=guid_to_delete, deleted_by=guid)
    if result != "SUCCESS":
        logger.error("User deletion failed.",)
        return ResponseHandler.generate_response_unsuccessful(400, result)
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="DELETE_USER",
        resource="/user/delete",
        request_body={"guid_to_delete": guid_to_delete},
    )
    return ResponseHandler.generate_response_successful("User deleted successfully.", None)

@router.get("/get-list-users")
async def get_list_users(
    request: Request,
    background_tasks: BackgroundTasks,
    page_number: int = 1,
    page_size: int = Query(default=50, le=200),
    search: str = None,
    start_date: str = None,
    end_date: str = None,
    order_by: str = 'created_desc',
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service),
    guid: str = Depends(require_permissions(["user:read"])),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    result = await user_service.get_list_users(
        conn=conn,
        page_number=page_number,
        page_size=page_size,
        search=search,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by
    )
    if result["error"] != "SUCCESS":
        logger.error("Failed to retrieve user list.")
        return ResponseHandler.generate_response_unsuccessful(400, result["error"])
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="GET_LIST_USERS",
        resource="/user/get-list-users",
        request_body={
            "page_number": page_number,
            "page_size": page_size,
            "search": search,
            "start_date": start_date,
            "end_date": end_date,
            "order_by": order_by
        },
    )
    return ResponseHandler.generate_response_successful("User list retrieved successfully.", result)

@router.get("/export/csv", )
async def export_csv(
    request: Request,
    background_tasks: BackgroundTasks,
    search: str = None,
    start_date: str = None,
    end_date: str = None,
    order_by: str = 'created_desc',
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service),
    guid: str = Depends(require_permissions(["user:read"])),
    conn: asyncpg.Connection = Depends(get_db_conn)
):
    result = await user_service.get_list_users(
        conn=conn,
        page_number=1,
        page_size=1000000,
        search=search,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by
    )
    if result["error"] != "SUCCESS":
        logger.error("Failed to exported user list.")
        return ResponseHandler.generate_response_unsuccessful(400, result["error"])
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=result["data"][0].keys())
    writer.writeheader()
    writer.writerows(result["data"])
    output.seek(0)
    background_tasks.add_task(
        audit_service.log_action,
        guid=guid,
        request=request,
        action="EXPORT_CSV_USERS",
        resource="/user/export/csv",
        request_body={
            "page_number": 1,
            "page_size": 1000000,
            "search": search,
            "start_date": start_date,
            "end_date": end_date,
            "order_by": order_by
        },
    )
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=users.csv"
        }
    )
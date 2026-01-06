import logging
from h11 import Request
from typing import Dict, Any
from app.repositories.postgres.audit_repository import AuditRepository

logger = logging.getLogger(__name__)

class AuditService:
    def __init__(self):
        self.audit_repo = AuditRepository()

    async def log_action(
        self,
        guid: str,
        request: Request,
        action: str,
        resource: str,
        request_body: Dict[str, Any],
    ) -> None:
        x_forwarded_for = request.headers.get("x-forwarded-for")
        ip_address = None
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0].strip()
        elif request.client:
            ip_address = request.client.host
        user_agent = request.headers.get("user-agent")
        log_data = {
            "trace_id": request.state.trace_id,
            "action": action,
            "resource": resource,
            "method": request.method,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "request_body": request_body,
            "guid": guid,
        }
        await self.audit_repo.write_log(log_data)

    async def get_list_audit_logs(self, page_number: int, page_size: int, search: str, start_date: str, end_date: str, order_by: str) -> dict | None:
        return await self.audit_repo.get_list_audit_logs(
            page_number=page_number,
            page_size=page_size,
            search=search,
            start_date=start_date,
            end_date=end_date,
            order_by=order_by
        )
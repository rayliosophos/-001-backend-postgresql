import logging
import asyncpg
from fastapi import Request
from typing import Dict, Any
from app.database.postgres import get_pg_pool
from app.repositories.postgres.audit_repository import AuditRepository

logger = logging.getLogger(__name__)

class AuditService:
    def __init__(self):
        self.audit_repo = AuditRepository()

    async def log_action(
        self,
        *,
        guid: str,
        request: Request,
        action: str,
        resource: str,
        request_body: Dict[str, Any],
    ) -> None:
        pool = await get_pg_pool()
        async with pool.acquire() as conn:
            x_forwarded_for = request.headers.get("x-forwarded-for")
            ip_address = None
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(",")[0].strip()
            elif request.client:
                ip_address = request.client.host
            user_agent = request.headers.get("user-agent")
            log_data = {
                "trace_id": getattr(request.state, "trace_id", None),
                "action": action,
                "resource": resource,
                "method": request.method,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "request_body": request_body,
                "guid": guid,
            }
            await self.audit_repo.write_log(conn = conn, data = log_data)

    async def get_list_audit_logs(self, *, conn: asyncpg.Connection, page_number: int, page_size: int, search: str, start_date: str, end_date: str, order_by: str) -> dict | None:
        return await self.audit_repo.get_list_audit_logs(
            conn = conn,
            page_number=page_number,
            page_size=page_size,
            search=search,
            start_date=start_date,
            end_date=end_date,
            order_by=order_by
        )
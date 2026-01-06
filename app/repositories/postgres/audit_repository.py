import json
import logging
from typing import Any, Dict
from datetime import datetime
from app.db.postgres import get_pg_pool

logger = logging.getLogger(__name__)

class AuditRepository:
  
  @staticmethod
  async def write_log(data: dict):
      try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                call p_audit_logs( $1, $2, $3, $4, $5, $6, $7, $8 )
                """,
                data["trace_id"],
                data["action"],
                data["resource"],
                data["method"],
                data["ip_address"],
                data["user_agent"],
                json.dumps(data["request_body"]),
                data["guid"]
            )
      except Exception as e:
        logger.error("Error writing audit log: %s", e)
        
  async def get_list_audit_logs(self, page_number: int, page_size: int, search: str, start_date: str, end_date: str, order_by: str) -> Dict[str, Any]:
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            result = await conn.fetchrow(
                "select * from f_get_list_audit_logs($1, $2, $3, $4, $5, $6)",
                page_number,
                page_size,
                search,
                datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None,
                datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None,
                order_by
            )
            if result['out_error'] != "SUCCESS":
                logger.error("Error from f_get_list_audit_logs: %s", result['out_error'])
                return {
                    "total_pages": 0,
                    "data": [],
                    "error": result['out_error']
                }
        return {
            "total_pages": result["out_total_pages"],
            "data": json.loads(result["out_data"]) if result["out_data"] else [],
            "error": "SUCCESS"
        }
    except Exception as e:
        logger.error("Error getting list of audit: %s", e)
        return None
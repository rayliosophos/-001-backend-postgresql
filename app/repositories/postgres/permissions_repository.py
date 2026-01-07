import json
import logging
import asyncpg

logger = logging.getLogger(__name__)

class PermissionRepository:

    async def get_list_roles(self, *, conn: asyncpg.Connection):
        result = await conn.fetch(
        """
        select id, name from tbl_roles order by name
        """
        )
        return [dict(row) for row in result]

    async def get_permissions_detail(self, *, conn: asyncpg.Connection, role_id: int) -> json:
        try:
            result = await conn.fetchval("select f_get_permissions_detail($1)", role_id)
            return json.loads(result)
        except Exception as e:
            logger.error("Error getting permissions detail: %s", e)
            return None
            
    async def assign_permissions_to_role(self, *, conn: asyncpg.Connection, role_id: int, permissions: str) -> str:
        try:
            result = await conn.fetchval("select f_assign_permissions_to_role($1, $2)", role_id, permissions)
            return result
        except Exception as e:
            logger.error("Error assigning permissions to role: %s", e)
            return f"Error: {str(e)}"
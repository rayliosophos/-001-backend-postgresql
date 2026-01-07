import json
import logging
import asyncpg
from app.repositories.postgres.permissions_repository import PermissionRepository

logger = logging.getLogger(__name__)

class PermissionService:
    def __init__(self):
        self.pg_permission_repo = PermissionRepository()
        
    async def get_list_roles(self, *, conn: asyncpg.Connection):
        return await self.pg_permission_repo.get_list_roles(conn=conn)
    
    async def get_permissions_detail(self, *, conn: asyncpg.Connection, role_id: int) -> json:
        return await self.pg_permission_repo.get_permissions_detail(conn=conn, role_id=role_id)
    
    async def assign_permissions_to_role(self, *, conn: asyncpg.Connection,role_id: int, permissions: str) -> str:
        return await self.pg_permission_repo.assign_permissions_to_role(conn=conn,role_id= role_id, permissions=permissions)
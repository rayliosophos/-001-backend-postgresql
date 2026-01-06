import json
import logging
from app.repositories.postgres.permissions_repository import PermissionRepository

logger = logging.getLogger(__name__)

class PermissionService:
    def __init__(self):
        self.pg_permission_repo = PermissionRepository()
        
    async def get_list_roles(self):
        return await self.pg_permission_repo.get_list_roles()
    
    async def get_permissions_detail(self, role_id: int) -> json:
        return await self.pg_permission_repo.get_permissions_detail(role_id)
    
    async def assign_permissions_to_role(self, role_id: int, permissions: str) -> str:
        return await self.pg_permission_repo.assign_permissions_to_role(role_id, permissions)
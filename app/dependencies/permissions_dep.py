from app.services.permissions_service import PermissionService

def get_permission_service() -> PermissionService:
    return PermissionService()
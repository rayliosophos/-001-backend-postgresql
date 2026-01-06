from pydantic import BaseModel

class PermissionsRoleRequest (BaseModel):
    role_id: int
    permissions: str
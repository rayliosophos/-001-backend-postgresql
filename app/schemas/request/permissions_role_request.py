from typing import Optional
from pydantic import BaseModel, EmailStr

class PermissionsRoleRequest (BaseModel):
    role_id: int
    permissions: str
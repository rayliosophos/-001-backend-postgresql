from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRequest (BaseModel):
    guid: Optional[str] = None
    role_id: int
    photo: Optional[str] = None
    first_name: str
    last_name: str
    gender: str
    username: str
    password: Optional[str] = None
    email: EmailStr
    phone: str
    about: Optional[str] = None
    created_by: Optional[str] = None
    modify_by: Optional[str] = None
    is_enabled: Optional[bool] = None
    is_deleted: Optional[bool] = None
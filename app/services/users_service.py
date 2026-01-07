import json
import logging
import asyncpg
from app.schemas.request.user_request import UserRequest
from app.repositories.postgres.user_repository import UserRepository

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.pg_user_repo = UserRepository()
        
    async def get_user_menu(self, *, conn: asyncpg.Connection, guid: str) -> json:
        menu_json = await self.pg_user_repo.get_user_menu(conn=conn, guid=guid)
        if not menu_json:
            logger.warning("No menu found for user.")
            return json.loads("[]")
        return menu_json

    async def create_user(self, *, conn: asyncpg.Connection, data: UserRequest, created_by: str) -> str | None:
        return await self.pg_user_repo.create_user(
            conn=conn,
            role_id=data.role_id,
            first_name=data.first_name,
            last_name=data.last_name,
            gender=data.gender,
            photo=data.photo,
            username=data.username,
            password=data.password,
            email=data.email,
            phone=data.phone,
            about=data.about,
            created_by=created_by
        )
        
    async def update_user(self, *, conn: asyncpg.Connection, data: UserRequest) -> str | None:
        return await self.pg_user_repo.update_user(conn=conn, data=data)
        
    async def delete_user(self, *, conn: asyncpg.Connection, guid: str, deleted_by: str) -> str | None:
        return await self.pg_user_repo.delete_user(conn=conn, guid=guid, deleted_by=deleted_by)
        
    async def get_list_users(self, *, conn: asyncpg.Connection, page_number: int, page_size: int, search: str, start_date: str, end_date: str, order_by: str) -> dict | None:
        return await self.pg_user_repo.get_list_users(
            conn=conn,
            page_number=page_number,
            page_size=page_size,
            search=search,
            start_date=start_date,
            end_date=end_date,
            order_by=order_by
        )
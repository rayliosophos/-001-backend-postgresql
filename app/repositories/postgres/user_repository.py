import json
import logging
import asyncpg
from typing import Any, Dict
from pydantic import EmailStr
from datetime import datetime
from app.schemas.request.user_request import UserRequest

logger = logging.getLogger(__name__)

class UserRepository:
    
    async def get_user_menu(self, *, conn: asyncpg.Connection, guid: str) -> json:
        try:
            result = await conn.fetchval( "select f_get_user_menu($1)", guid)
            return json.loads(result)
        except Exception as e:
            logger.error("Error getting user menu: %s", e)
            return None
        
    async def create_user(
        self,
        *, 
        conn: asyncpg.Connection,
        role_id: int,
        first_name: str,
        last_name: str,
        gender: str,
        photo: str,
        username: str,
        password: str,
        email: EmailStr,
        phone: str,
        about: str,
        created_by: str
    ) -> str | None:
        try:
            result = await conn.fetchval(
                "select f_create_user($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)",
                role_id, first_name, last_name, gender, photo, username, password, email, phone, about, created_by
            )
            return result
        except Exception as e:
            logger.error("Error creating user: %s", e)
            return None
        
    async def update_user(self, *, conn: asyncpg.Connection, data: UserRequest) -> str | None:
        try:
            result = await conn.fetchval(
                "select f_update_user($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)",
                data.guid, data.role_id, data.first_name, data.last_name, data.gender, data.photo, data.username, data.password, data.email, data.phone, data.about, data.modify_by, data.is_enabled
            )
            return result
        except Exception as e:
            logger.error("Error updating user: %s", e)
            return None
        
    async def delete_user(self, *, conn: asyncpg.Connection, guid: str, deleted_by: str) -> str | None:
        try:
            result = await conn.fetchval(
                "select f_delete_user($1, $2)",
                guid, deleted_by
            )
            return result
        except Exception as e:
            logger.error("Error deleting user: %s", e)
            return None

    async def get_list_users(self, *, conn: asyncpg.Connection, page_number: int, page_size: int, search: str, start_date: str, end_date: str, order_by: str) -> Dict[str, Any]:
        try:
            result = await conn.fetchrow(
                "select * from f_get_list_users($1, $2, $3, $4, $5, $6)",
                page_number, 
                page_size, 
                search, 
                datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None, 
                datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None, 
                order_by
            )
            if result['out_error'] != "SUCCESS":
                logger.error("Error from f_get_list_users: %s", result['out_error'])
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
            logger.error("Error getting list of users: %s", e)
            return None
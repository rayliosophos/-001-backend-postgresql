from fastapi import APIRouter
from app.api.v1.routes import login

router = APIRouter()

router.include_router(login.router)

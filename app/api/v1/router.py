from fastapi import APIRouter
from app.api.v1.routes import audit_route, health_route, login_route, permissions_route, users_route, utilities_route

router = APIRouter()

router.include_router(login_route.router)
router.include_router(users_route.router)
router.include_router(health_route.router)
router.include_router(permissions_route.router)
router.include_router(audit_route.router)
router.include_router(utilities_route.router)

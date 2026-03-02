"""API 路由聚合"""

from fastapi import APIRouter

from .status import router as status_router
from .settings import router as settings_router
from .providers import router as providers_router
from .personas import router as personas_router
from .napcat import router as napcat_router

api_router = APIRouter()
api_router.include_router(status_router, prefix="/status", tags=["状态"])
api_router.include_router(settings_router, prefix="/settings", tags=["设置"])
api_router.include_router(providers_router, prefix="/providers", tags=["提供商"])
api_router.include_router(personas_router, prefix="/personas", tags=["角色"])
api_router.include_router(napcat_router, prefix="/napcat", tags=["NapCat"])

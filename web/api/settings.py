"""设置 CRUD API"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from config import config

router = APIRouter()


class SettingsUpdate(BaseModel):
    max_interactions: int | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    timeout: int | None = None
    cooldown_seconds: int | None = None
    max_context_messages: int | None = None
    active_provider_id: str | None = None
    active_persona_id: str | None = None


@router.get("")
async def get_settings():
    """获取当前设置"""
    return config.settings.model_dump()


@router.put("")
async def update_settings(body: SettingsUpdate):
    """更新设置"""
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    updated = config.update_settings(**updates)
    return updated.model_dump()

"""AI 提供商 CRUD API"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import config

router = APIRouter()


def _mask_key(key: str) -> str:
    """掩码 API Key — 任何非空 key 都只显示前 4 + 后 4 位"""
    if not key:
        return ""
    if len(key) <= 8:
        return "****"
    return key[:4] + "****" + key[-4:]


def _safe_provider(p: dict) -> dict:
    """返回掩码后的 provider 字典"""
    safe = dict(p)
    safe["api_key"] = _mask_key(safe.get("api_key", ""))
    return safe


class ProviderCreate(BaseModel):
    id: str
    name: str
    type: str = "openai_compat"
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    enabled: bool = True


@router.get("")
async def list_providers():
    """列出所有提供商（掩码 API Key）"""
    return [_safe_provider(p) for p in config.providers]


@router.post("")
async def create_provider(body: ProviderCreate):
    """创建或更新提供商"""
    config.add_provider(body.model_dump())
    return {"ok": True}


@router.get("/{provider_id}")
async def get_provider(provider_id: str):
    """获取单个提供商（掩码 API Key）"""
    p = config.get_provider(provider_id)
    if not p:
        raise HTTPException(404, "提供商不存在")
    return _safe_provider(p)


@router.put("/{provider_id}")
async def update_provider(provider_id: str, body: ProviderCreate):
    """更新提供商"""
    data = body.model_dump()
    data["id"] = provider_id
    # 如果传入的 api_key 是掩码格式，保留原值
    if "****" in data.get("api_key", ""):
        existing = config.get_provider(provider_id)
        if existing:
            data["api_key"] = existing["api_key"]
    config.add_provider(data)
    return {"ok": True}


@router.delete("/{provider_id}")
async def delete_provider(provider_id: str):
    """删除提供商"""
    if config.delete_provider(provider_id):
        return {"ok": True}
    raise HTTPException(404, "提供商不存在")

"""AI 提供商 CRUD API"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import config

router = APIRouter()


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
    """列出所有提供商（隐藏完整 API Key）"""
    result = []
    for p in config.providers:
        safe = dict(p)
        key = safe.get("api_key", "")
        if key and len(key) > 8:
            safe["api_key"] = key[:4] + "****" + key[-4:]
        result.append(safe)
    return result


@router.post("")
async def create_provider(body: ProviderCreate):
    """创建或更新提供商"""
    config.add_provider(body.model_dump())
    return {"ok": True}


@router.get("/{provider_id}")
async def get_provider(provider_id: str):
    """获取单个提供商"""
    p = config.get_provider(provider_id)
    if not p:
        raise HTTPException(404, "提供商不存在")
    return p


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

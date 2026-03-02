"""模型 CRUD API"""

from __future__ import annotations

import re
from uuid import uuid4

import httpx
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
    name: str
    type: str = "openai_compat"
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    enabled: bool = True
    id: str | None = None


class ProviderUpdate(BaseModel):
    name: str
    type: str = "openai_compat"
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    enabled: bool = True


class ProviderModelKeyUpdate(BaseModel):
    model: str | None = None
    api_key: str | None = None


def _slug(text: str, fallback: str = "provider") -> str:
    value = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    value = value[:24]
    return value or fallback


def _generate_provider_id(name: str) -> str:
    existing = {p.get("id", "") for p in config.providers}
    base = _slug(name, "provider")
    for _ in range(8):
        candidate = f"{base}-{uuid4().hex[:6]}"
        if candidate not in existing:
            return candidate
    return f"provider-{uuid4().hex}"


@router.get("")
async def list_providers():
    """列出所有提供商（掩码 API Key）"""
    return [_safe_provider(p) for p in config.providers]


@router.post("")
async def create_provider(body: ProviderCreate):
    """创建提供商（ID 自动生成）"""
    data = body.model_dump()
    data["id"] = _generate_provider_id(body.name)
    config.add_provider(data)
    return {"ok": True, "id": data["id"]}


class ListModelsRequest(BaseModel):
    type: str = “openai_compat”
    base_url: str = “”
    api_key: str = “”


@router.post(“/list-models”)
async def list_available_models(body: ListModelsRequest):
    “””根据类型、base_url、api_key 查询可用模型列表”””
    if not body.base_url or not body.api_key:
        raise HTTPException(400, “请填写 Base URL 和 API Key”)

    try:
        if body.type == “claude”:
            base = body.base_url.rstrip(“/”) if body.base_url else “https://api.anthropic.com”
            url = f”{base}/v1/models”
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url, headers={
                    “x-api-key”: body.api_key,
                    “anthropic-version”: “2023-06-01”,
                })
                resp.raise_for_status()
                data = resp.json()
                models = sorted([m[“id”] for m in data.get(“data”, [])])
        else:
            url = f”{body.base_url.rstrip('/')}/models”
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url, headers={
                    “Authorization”: f”Bearer {body.api_key}”,
                })
                resp.raise_for_status()
                data = resp.json()
                models = sorted([m[“id”] for m in data.get(“data”, [])])
        return {“ok”: True, “models”: models}
    except httpx.HTTPStatusError as e:
        raise HTTPException(e.response.status_code, f”API 请求失败: {e.response.status_code}”)
    except httpx.RequestError as e:
        raise HTTPException(502, f”无法连接: {e}”)


@router.get(“/{provider_id}”)
async def get_provider(provider_id: str):
    “””获取单个提供商（掩码 API Key）”””
    p = config.get_provider(provider_id)
    if not p:
        raise HTTPException(404, “提供商不存在”)
    return _safe_provider(p)


@router.put(“/{provider_id}”)
async def update_provider(provider_id: str, body: ProviderUpdate):
    “””更新提供商”””
    data = body.model_dump()
    data[“id”] = provider_id
    # 如果传入的 api_key 是掩码格式或空字符串，保留原值
    if not data.get(“api_key”) or “****” in data.get(“api_key”, “”):
        existing = config.get_provider(provider_id)
        if existing:
            data[“api_key”] = existing[“api_key”]
    config.add_provider(data)
    return {“ok”: True}


@router.patch(“/{provider_id}/model-key”)
async def update_provider_model_key(provider_id: str, body: ProviderModelKeyUpdate):
    “””仅更新已存在提供商的模型与 API Key”””
    existing = config.get_provider(provider_id)
    if not existing:
        raise HTTPException(404, “提供商不存在”)

    data = dict(existing)

    if body.model is not None:
        data[“model”] = body.model

    if body.api_key is not None:
        # 掩码或空字符串都视为”不修改”
        if “****” not in body.api_key and body.api_key.strip() != “”:
            data[“api_key”] = body.api_key

    config.add_provider(data)
    return {“ok”: True}


@router.delete(“/{provider_id}”)
async def delete_provider(provider_id: str):
    “””删除提供商”””
    if config.delete_provider(provider_id):
        return {“ok”: True}
    raise HTTPException(404, “提供商不存在”)

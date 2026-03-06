"""角色 CRUD API"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import config

router = APIRouter()


class PersonaCreate(BaseModel):
    name: str
    system_prompt: str
    builtin: bool = False


class PersonaUpdate(BaseModel):
    name: str
    system_prompt: str


@router.get("")
async def list_personas():
    """列出所有角色"""
    return config.personas


@router.post("")
async def create_persona(body: PersonaCreate):
    """创建角色（自动生成 ID）"""
    import re
    from uuid import uuid4
    slug = re.sub(r"[^a-z0-9]+", "-", body.name.lower()).strip("-")[:20] or "persona"
    existing_ids = {p.get("id", "") for p in config.personas}
    pid = f"{slug}-{uuid4().hex[:6]}"
    while pid in existing_ids:
        pid = f"{slug}-{uuid4().hex[:6]}"
    data = body.model_dump()
    data["id"] = pid
    config.add_persona(data)
    return {"ok": True, "id": pid}


@router.get("/{persona_id}")
async def get_persona(persona_id: str):
    """获取单个角色"""
    p = config.get_persona(persona_id)
    if not p:
        raise HTTPException(404, "角色不存在")
    return p


@router.put("/{persona_id}")
async def update_persona(persona_id: str, body: PersonaUpdate):
    """更新角色"""
    existing = config.get_persona(persona_id)
    if not existing:
        raise HTTPException(404, "角色不存在")
    data = dict(existing)
    data.update(body.model_dump())
    config.add_persona(data)
    return {"ok": True}


@router.delete("/{persona_id}")
async def delete_persona(persona_id: str):
    """删除角色"""
    if config.delete_persona(persona_id):
        return {"ok": True}
    raise HTTPException(404, "角色不存在")

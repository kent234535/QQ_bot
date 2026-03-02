"""角色 CRUD API"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import config

router = APIRouter()


class PersonaCreate(BaseModel):
    id: str
    name: str
    system_prompt: str
    builtin: bool = False


@router.get("")
async def list_personas():
    """列出所有角色"""
    return config.personas


@router.post("")
async def create_persona(body: PersonaCreate):
    """创建或更新角色"""
    config.add_persona(body.model_dump())
    return {"ok": True}


@router.get("/{persona_id}")
async def get_persona(persona_id: str):
    """获取单个角色"""
    p = config.get_persona(persona_id)
    if not p:
        raise HTTPException(404, "角色不存在")
    return p


@router.put("/{persona_id}")
async def update_persona(persona_id: str, body: PersonaCreate):
    """更新角色"""
    data = body.model_dump()
    data["id"] = persona_id
    config.add_persona(data)
    return {"ok": True}


@router.delete("/{persona_id}")
async def delete_persona(persona_id: str):
    """删除角色"""
    if config.delete_persona(persona_id):
        return {"ok": True}
    raise HTTPException(404, "角色不存在")

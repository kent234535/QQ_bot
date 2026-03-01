"""Bot 状态 API"""

from __future__ import annotations

import time

from fastapi import APIRouter

from config import config

router = APIRouter()

_start_time = time.time()


@router.get("")
async def get_status():
    """获取 Bot 运行状态"""
    provider = config.get_active_provider()
    persona = config.get_persona(config.settings.active_persona_id)

    return {
        "uptime_seconds": int(time.time() - _start_time),
        "active_provider": provider["name"] if provider else None,
        "active_persona": persona["name"] if persona else None,
        "providers_count": len(config.providers),
        "personas_count": len(config.personas),
    }

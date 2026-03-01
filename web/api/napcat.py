"""NapCat 启停 / 二维码代理 API"""

from __future__ import annotations

import asyncio
import subprocess

from fastapi import APIRouter
from fastapi.responses import Response

import httpx

router = APIRouter()

# NapCat 进程引用
_napcat_proc: subprocess.Popen | None = None

NAPCAT_WEBUI_URL = "http://127.0.0.1:6099"
QQ_APP_PATH = "/Applications/QQ.app/Contents/MacOS/QQ"
QQ_ACCOUNT = "3540159556"


@router.get("/status")
async def napcat_status():
    """获取 NapCat 状态"""
    global _napcat_proc
    running = _napcat_proc is not None and _napcat_proc.poll() is None

    # 尝试检测 NapCat WebUI 是否可达
    webui_reachable = False
    if running:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.get(f"{NAPCAT_WEBUI_URL}/api/get/robot/status")
                webui_reachable = resp.status_code == 200
        except Exception:
            pass

    return {
        "process_running": running,
        "webui_reachable": webui_reachable,
        "pid": _napcat_proc.pid if running else None,
    }


@router.post("/start")
async def start_napcat():
    """启动 NapCat（QQ --no-sandbox 模式）"""
    global _napcat_proc

    if _napcat_proc is not None and _napcat_proc.poll() is None:
        return {"ok": True, "message": "NapCat 已在运行", "pid": _napcat_proc.pid}

    try:
        _napcat_proc = subprocess.Popen(
            [QQ_APP_PATH, "--no-sandbox", "-q", QQ_ACCOUNT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # 等待一小段时间让进程启动
        await asyncio.sleep(2)

        if _napcat_proc.poll() is not None:
            return {"ok": False, "message": "NapCat 启动失败（进程已退出）"}

        return {"ok": True, "pid": _napcat_proc.pid}
    except FileNotFoundError:
        return {"ok": False, "message": f"QQ 未找到: {QQ_APP_PATH}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}


@router.post("/stop")
async def stop_napcat():
    """停止 NapCat"""
    global _napcat_proc

    if _napcat_proc is None or _napcat_proc.poll() is not None:
        _napcat_proc = None
        return {"ok": True, "message": "NapCat 未在运行"}

    _napcat_proc.terminate()
    try:
        _napcat_proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _napcat_proc.kill()

    _napcat_proc = None
    return {"ok": True, "message": "NapCat 已停止"}


@router.get("/qrcode")
async def proxy_qrcode():
    """代理 NapCat WebUI 的登录二维码"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{NAPCAT_WEBUI_URL}/api/get/robot/qrcode")
            if resp.status_code == 200:
                return resp.json()
            return {"ok": False, "message": f"NapCat 返回 {resp.status_code}"}
    except Exception as e:
        return {"ok": False, "message": f"无法连接 NapCat WebUI: {e}"}

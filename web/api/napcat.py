"""NapCat 启停 / 二维码代理 API"""

from __future__ import annotations

import asyncio
import subprocess

from fastapi import APIRouter

import httpx

router = APIRouter()

NAPCAT_WEBUI_URL = "http://127.0.0.1:6099"
QQ_APP_PATH = "/Applications/QQ.app/Contents/MacOS/QQ"
QQ_ACCOUNT = "3540159556"


def _find_napcat_pids() -> list[int]:
    """查找系统中所有 --no-sandbox 模式的 QQ 主进程 PID"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "QQ.app.*--no-sandbox"],
            capture_output=True, text=True, timeout=3,
        )
        return [int(p) for p in result.stdout.strip().split("\n") if p.strip()]
    except Exception:
        return []


async def _probe_webui() -> bool:
    """探测 NapCat WebUI 是否可达"""
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(f"{NAPCAT_WEBUI_URL}/api/get/robot/status")
            return resp.status_code == 200
    except Exception:
        return False


@router.get("/status")
async def napcat_status():
    """获取 NapCat 状态 — 以系统进程 + WebUI 探测为准"""
    pids = _find_napcat_pids()
    webui_reachable = await _probe_webui()

    return {
        "process_running": len(pids) > 0,
        "webui_reachable": webui_reachable,
        "pids": pids,
    }


@router.post("/start")
async def start_napcat():
    """启动 NapCat（QQ --no-sandbox 模式）"""
    # 已有进程或 WebUI 可达 → 不重复启动
    pids = _find_napcat_pids()
    if pids:
        return {"ok": True, "message": f"NapCat 已在运行（PID: {pids}）"}

    if await _probe_webui():
        return {"ok": True, "message": "NapCat WebUI 已可达"}

    try:
        # macOS Electron 应用：launcher 进程会 fork 后退出，不能用 Popen 跟踪
        subprocess.Popen(
            [QQ_APP_PATH, "--no-sandbox", "-q", QQ_ACCOUNT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return {"ok": False, "message": f"QQ 未找到: {QQ_APP_PATH}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}

    # 等待 QQ 进程树建立（launcher fork 后退出，真正的 QQ 需要几秒）
    for _ in range(10):
        await asyncio.sleep(1)
        pids = _find_napcat_pids()
        if pids:
            return {"ok": True, "message": "NapCat 已启动，等待登录确认...", "pids": pids}

    return {"ok": True, "message": "启动命令已发送，请在 QQ 窗口确认登录"}


@router.post("/stop")
async def stop_napcat():
    """停止所有 NapCat QQ 进程"""
    pids = _find_napcat_pids()
    if not pids:
        return {"ok": True, "message": "NapCat 未在运行"}

    for pid in pids:
        try:
            subprocess.run(["kill", str(pid)], timeout=5)
        except Exception:
            pass

    # 等待进程退出
    await asyncio.sleep(2)
    remaining = _find_napcat_pids()
    if remaining:
        # 强制 kill
        for pid in remaining:
            try:
                subprocess.run(["kill", "-9", str(pid)], timeout=3)
            except Exception:
                pass

    return {"ok": True, "message": f"已终止 NapCat 进程（PID: {pids}）"}


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

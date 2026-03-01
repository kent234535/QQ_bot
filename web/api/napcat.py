"""NapCat 启停 / 二维码代理 API"""

from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
from pathlib import Path

from fastapi import APIRouter

import httpx

router = APIRouter()

NAPCAT_WEBUI_URL = "http://127.0.0.1:6099"
QQ_APP_PATH = "/Applications/QQ.app/Contents/MacOS/QQ"
QQ_PACKAGE_JSON = Path("/Applications/QQ.app/Contents/Resources/app/package.json")
QQ_ACCOUNT = "3540159556"

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
NAPCAT_PACKAGE = PROJECT_DIR / "package.json.napcat"
ORIGINAL_PACKAGE = PROJECT_DIR / "package.json.original"


# ─── 工具函数 ───

def _is_napcat_mode() -> bool:
    """检查当前 QQ 的 package.json 是否已切换到 NapCat 模式"""
    try:
        data = json.loads(QQ_PACKAGE_JSON.read_text(encoding="utf-8"))
        return "napcat" in data.get("main", "").lower()
    except Exception:
        return False


def _switch_to_napcat() -> tuple[bool, str]:
    """切换 QQ 到 NapCat 模式：替换 package.json + 重签名"""
    if not NAPCAT_PACKAGE.exists():
        return False, f"NapCat package.json 不存在: {NAPCAT_PACKAGE}"

    try:
        shutil.copy2(NAPCAT_PACKAGE, QQ_PACKAGE_JSON)
        subprocess.run(
            ["codesign", "--force", "--deep", "--sign", "-", "/Applications/QQ.app"],
            capture_output=True, timeout=30,
        )
        subprocess.run(
            ["xattr", "-cr", "/Applications/QQ.app"],
            capture_output=True, timeout=10,
        )
        return True, "已切换到 NapCat 模式"
    except Exception as e:
        return False, f"切换失败: {e}"


def _switch_to_normal() -> tuple[bool, str]:
    """切换 QQ 回普通模式"""
    if not ORIGINAL_PACKAGE.exists():
        return False, f"原版 package.json 不存在: {ORIGINAL_PACKAGE}"

    try:
        shutil.copy2(ORIGINAL_PACKAGE, QQ_PACKAGE_JSON)
        subprocess.run(
            ["codesign", "--force", "--deep", "--sign", "-", "/Applications/QQ.app"],
            capture_output=True, timeout=30,
        )
        subprocess.run(
            ["xattr", "-cr", "/Applications/QQ.app"],
            capture_output=True, timeout=10,
        )
        return True, "已切换回普通模式"
    except Exception as e:
        return False, f"切换失败: {e}"


def _find_all_qq_pids() -> list[int]:
    """查找所有 QQ 相关进程（主进程 + Helper + Renderer + QQEXDOC）"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "QQ.app"],
            capture_output=True, text=True, timeout=3,
        )
        return [int(p) for p in result.stdout.strip().split("\n") if p.strip()]
    except Exception:
        return []


def _kill_all_qq() -> bool:
    """彻底杀掉所有 QQ 相关进程（主进程 + 子进程 + QQEXDOC）"""
    # 先 SIGTERM 优雅退出
    subprocess.run(["pkill", "-f", "QQ.app"], capture_output=True, timeout=5)
    subprocess.run(["pkill", "-f", "QQEXDOC"], capture_output=True, timeout=5)
    return True


def _force_kill_all_qq() -> None:
    """强制杀掉所有 QQ 残留进程"""
    subprocess.run(["pkill", "-9", "-f", "QQ.app"], capture_output=True, timeout=5)
    subprocess.run(["pkill", "-9", "-f", "QQEXDOC"], capture_output=True, timeout=5)


def _is_qq_running() -> bool:
    """检查是否有任何 QQ 进程在运行"""
    return len(_find_all_qq_pids()) > 0


def _find_napcat_main_pid() -> int | None:
    """
    查找 NapCat 模式的 QQ 主进程 PID。
    只匹配 /Applications/QQ.app/Contents/MacOS/QQ 主进程（不含 Helper/Renderer 子进程）。
    """
    try:
        result = subprocess.run(
            ["pgrep", "-f", "QQ.app/Contents/MacOS/QQ$"],
            capture_output=True, text=True, timeout=3,
        )
        pids = [int(p) for p in result.stdout.strip().split("\n") if p.strip()]
        return pids[0] if pids else None
    except Exception:
        return None


async def _probe_webui() -> bool:
    """探测 NapCat WebUI 是否可达"""
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(f"{NAPCAT_WEBUI_URL}/api/get/robot/status")
            return resp.status_code == 200
    except Exception:
        return False


async def _ensure_qq_killed() -> None:
    """确保所有 QQ 进程已退出，最多等 8 秒"""
    _kill_all_qq()
    for _ in range(4):
        await asyncio.sleep(2)
        if not _is_qq_running():
            return
    # 还有残留就强杀
    _force_kill_all_qq()
    await asyncio.sleep(1)


# ─── API 路由 ───

@router.get("/status")
async def napcat_status():
    """获取 NapCat 状态"""
    napcat_mode = _is_napcat_mode()
    qq_pid = _find_napcat_main_pid()
    qq_running = _is_qq_running()
    webui_reachable = await _probe_webui()

    return {
        "napcat_mode": napcat_mode,
        "qq_running": qq_running,
        "qq_main_pid": qq_pid,
        "webui_reachable": webui_reachable,
    }


@router.post("/start")
async def start_napcat():
    """一键启动 NapCat：杀全部 QQ → 切换模式 → 启动"""
    # 已经 WebUI 可达 → 不重复操作
    if await _probe_webui():
        return {"ok": True, "message": "NapCat 已在运行且 WebUI 可达"}

    # Step 1: 彻底杀掉所有 QQ 进程（含 Helper/Renderer/QQEXDOC）
    if _is_qq_running():
        await _ensure_qq_killed()
        if _is_qq_running():
            return {"ok": False, "message": "无法关闭现有 QQ 进程，请手动退出 QQ 后重试"}

    # Step 2: 切换到 NapCat 模式
    if not _is_napcat_mode():
        ok, msg = _switch_to_napcat()
        if not ok:
            return {"ok": False, "message": msg}

    # Step 3: 启动 QQ --no-sandbox
    try:
        subprocess.Popen(
            [QQ_APP_PATH, "--no-sandbox", "-q", QQ_ACCOUNT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return {"ok": False, "message": f"QQ 未找到: {QQ_APP_PATH}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}

    # Step 4: 等待 WebUI 就绪（最多 40 秒）
    for i in range(20):
        await asyncio.sleep(2)
        if await _probe_webui():
            return {"ok": True, "message": "NapCat 启动成功，WebUI 已就绪"}

    if _is_qq_running():
        return {"ok": True, "message": "QQ 已启动，WebUI 尚未就绪（请在 QQ 窗口确认登录）"}

    return {"ok": False, "message": "启动超时，QQ 进程未检测到"}


@router.post("/stop")
async def stop_napcat():
    """停止 NapCat 并切换回普通模式"""
    if not _is_qq_running() and not await _probe_webui():
        return {"ok": True, "message": "NapCat 未在运行"}

    # 彻底杀掉所有 QQ 进程
    await _ensure_qq_killed()

    # 切换回普通模式
    ok, msg = _switch_to_normal()

    return {"ok": True, "message": f"NapCat 已停止。{msg}"}


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

import os
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBot11Adapter


def _read_env_value(name: str) -> str | None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return None
    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == name:
                return value.strip().strip('"').strip("'")
    except OSError:
        return None
    return None


def _default_host() -> str:
    return os.environ.get("HOST") or _read_env_value("HOST") or "127.0.0.1"


def _default_port() -> int:
    value = os.environ.get("PORT") or _read_env_value("PORT") or "18080"
    try:
        return int(value)
    except (TypeError, ValueError):
        return 18080


nonebot.init(_env_file=".env", host=_default_host(), port=_default_port())

driver = nonebot.get_driver()
driver.register_adapter(OneBot11Adapter)

nonebot.load_plugins("plugins")

# 挂载 Web 控制台（API + 静态文件）
from web import mount_web_app
mount_web_app(driver)

if __name__ == "__main__":
    nonebot.run()

#!/usr/bin/env bash
# 启动 QQ Bot（NoneBot2 + Web 控制台）
set -e
cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN="python3"
    else
        PYTHON_BIN="python"
    fi
fi

HOST_VALUE="127.0.0.1"
PORT_VALUE="18080"
if [ -f ".env" ]; then
    ENV_HOST="$(sed -n 's/^HOST=//p' .env | tail -n 1)"
    ENV_PORT="$(sed -n 's/^PORT=//p' .env | tail -n 1)"
    if [ -n "$ENV_HOST" ]; then HOST_VALUE="$ENV_HOST"; fi
    if [ -n "$ENV_PORT" ]; then PORT_VALUE="$ENV_PORT"; fi
fi

# 激活虚拟环境（若存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

"$PYTHON_BIN" -m pip install -q -r requirements.txt 2>/dev/null || true
echo "[QQ Bot] 启动中，监听 ${HOST_VALUE}:${PORT_VALUE} ..."
"$PYTHON_BIN" bot.py

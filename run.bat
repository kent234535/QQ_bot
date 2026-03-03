@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

pip install -q -r requirements.txt 2>nul
echo [QQ Bot] 启动中，监听 127.0.0.1:8080 ...
python bot.py
pause

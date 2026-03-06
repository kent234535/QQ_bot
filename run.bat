@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

set "PYTHON_BIN=python"
where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if not errorlevel 1 set "PYTHON_BIN=py -3"
)

set "BOT_HOST=127.0.0.1"
set "BOT_PORT=18080"
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        if /I "%%A"=="HOST" set "BOT_HOST=%%B"
        if /I "%%A"=="PORT" set "BOT_PORT=%%B"
    )
)

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

%PYTHON_BIN% -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [QQ Bot] 依赖安装失败，请检查网络或 Python 环境
    pause
    exit /b 1
)
echo [QQ Bot] 启动中，监听 %BOT_HOST%:%BOT_PORT% ...
%PYTHON_BIN% bot.py
pause

<p align="center">
  <h1 align="center">QQ Bot</h1>
  <p align="center"><strong>QQ AI Chatbot with Web Console</strong></p>
  <p align="center">An AI-powered QQ auto-reply chatbot with a built-in web dashboard</p>
  <p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://nonebot.dev/"><img src="https://img.shields.io/badge/NoneBot2-Framework-ea5252?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHJlY3Qgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiByeD0iMyIgZmlsbD0id2hpdGUiLz48L3N2Zz4=" alt="NoneBot2"></a>
    <a href="https://vuejs.org/"><img src="https://img.shields.io/badge/Vue_3-Frontend-4fc08d?logo=vuedotjs&logoColor=white" alt="Vue 3"></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/License-LRL-blue" alt="License"></a>
    <img src="https://img.shields.io/badge/macOS-Recommended-brightgreen?logo=apple&logoColor=white" alt="macOS Recommended">
  </p>
  <p align="center">
    <a href="#features">Features</a> ·
    <a href="#screenshots">Screenshots</a> ·
    <a href="#quick-start">Quick Start</a> ·
    <a href="#web-console">Console</a> ·
    <a href="#license">License</a>
  </p>
  <p align="center">
    <a href="./README.md"><img src="https://img.shields.io/badge/🌐_English-4361ee?style=for-the-badge" alt="English"></a>&nbsp;
    <a href="./README_zh.md"><img src="https://img.shields.io/badge/🇨🇳_简体中文-gray?style=for-the-badge" alt="简体中文"></a>
  </p>
</p>

> A **QQ AI chatbot** powered by DeepSeek, Claude, Qwen, or any OpenAI-compatible LLM. Features a built-in **web console** for configuration, **custom AI personas**, and **QR code login**. Works on **macOS** and **Windows**.

> [!NOTE]
> **Recommended platform: macOS.** The current release is most stable on macOS. Windows support is available but still being improved.
>
> Default local console URL: `http://127.0.0.1:18080/web/`

---

## Features

- **Built-in Web Console** — Configure everything in the browser, no config files to edit
- **Bring Your Own API Key** — Supports DeepSeek, Alibaba Cloud (Qwen), OpenRouter, Anthropic Claude, and any OpenAI-compatible provider
- **Custom AI Personas** — Ships with cat-girl / assistant / programmer presets, or create your own with custom System Prompts
- **QR Code Login** — One-click NapCat connection, scan to log in, switch QQ accounts anytime
- **Multi-QQ App Detection** — Automatically detects all QQ installations on your machine (e.g. QQ.app, QQ_alt.app) and lets you switch between them in the console
- **Context-Aware Chat** — Auto-reply to private messages with conversation memory
- **Cross-Platform** — Runs on both macOS and Windows (macOS recommended for best stability)

---

## Screenshots

| Persona Management | Model Configuration |
|:---:|:---:|
| ![Personas](image/主界面(角色).png) | ![Models](image/模型界面.png) |

| Connection Management | Settings |
|:---:|:---:|
| ![Connection](image/连接界面.png) | ![Settings](image/设置界面.png) |

---

## Quick Start

> Prerequisites: [QQ Desktop (QQNT)](https://im.qq.com) and [NapCat](https://github.com/NapNeko/NapCatQQ) must be installed first.
>
> If QQ or NapCat is installed in a non-standard location, you can set `QQ_APP_DIR`, `QQ_EXE`, `QQ_PACKAGE_JSON`, `NAPCAT_LOADER`, or `NAPCAT_WEBUI_CONFIG` in `.env`.

**Choose your operating system:**

<a href="#macos-setup">
  <img src="https://img.shields.io/badge/macOS-Setup_Guide_(Recommended)-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS">
</a>
&nbsp;&nbsp;
<a href="#windows-setup">
  <img src="https://img.shields.io/badge/Windows-Setup_Guide-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
</a>

---

### macOS Setup

#### 1. Install Prerequisites

```bash
# Install Xcode Command Line Tools (includes Git)
xcode-select --install

# Install Homebrew (macOS package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.12

# Verify
python3 --version   # Should output Python 3.12.x or higher
```

#### 2. Install NapCat

Download the latest `.dmg` installer from [NapCat-Mac-Installer Releases](https://github.com/NapNeko/NapCat-Mac-Installer/releases) and follow the prompts.

> **Alternative** — command-line installation:
> ```bash
> curl -o napcat.sh https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.sh
> sudo bash napcat.sh --tui
> ```

Verify installation:

```bash
ls ~/Library/Containers/com.tencent.qq/Data/Documents/loadNapCat.js 2>/dev/null \
  || ls ~/Library/Application\ Support/QQ/loadNapCat.js 2>/dev/null \
  && echo "NapCat installed" || echo "NapCat not found"
```

#### 3. Deploy

```bash
cd ~/Desktop
git clone https://github.com/kent234535/qq-ai-auto-reply.git
cd ~/Desktop/qq-ai-auto-reply

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

#### 4. Run

```bash
cd ~/Desktop/qq-ai-auto-reply
source venv/bin/activate
python3 bot.py
```

Open **http://127.0.0.1:18080/web/** in your browser. Configure an AI model, pick a persona, click Connect and scan the QR code to log in.

---

### Windows Setup

#### 1. Install Git

Download from https://git-scm.com/download/win and install with default options. Open **Git Bash** from the Start menu.

> All commands below should be run in **Git Bash**.

#### 2. Install Python

```bash
# Install via winget (built into Windows 10 1709+)
winget install Python.Python.3.12

# Reopen Git Bash after install, then verify
python --version   # Should output Python 3.12.x or higher
```

> If `winget` is not available, download from https://www.python.org/downloads/ — **make sure to check "Add Python to PATH"**.

#### 3. Install NapCat

Run in **PowerShell (Administrator)**:

```powershell
curl -o install.ps1 https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.ps1
powershell -ExecutionPolicy ByPass -File ./install.ps1 -verb runas
```

> If this fails on Windows 10, download manually from [NapCat-Installer Releases](https://github.com/NapNeko/NapCat-Installer/releases).

#### 4. Deploy

Back in **Git Bash**:

```bash
cd ~/Desktop
git clone https://github.com/kent234535/qq-ai-auto-reply.git
cd ~/Desktop/qq-ai-auto-reply

python -m venv venv
source venv/Scripts/activate
python -m pip install -r requirements.txt
```

#### 5. Run

**Command line**:

```bash
cd ~/Desktop/qq-ai-auto-reply
source venv/Scripts/activate
python bot.py
```

**Or double-click** `run.bat` in the project root.

Open **http://127.0.0.1:18080/web/** in your browser. Configure an AI model, pick a persona, click Connect and scan the QR code to log in.

> If you see permission errors when connecting, run as Administrator.

---

## Web Console

Visit `http://127.0.0.1:18080/web/` after startup. The sidebar has four pages:

### Model Configuration

Add your own AI API keys. Supported providers:

| Provider | Type | Base URL | Model Example |
|----------|------|----------|---------------|
| DeepSeek | OpenAI Compatible | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Alibaba Cloud | OpenAI Compatible | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |
| OpenRouter | OpenAI Compatible | `https://openrouter.ai/api/v1` | `meta-llama/llama-3-70b` |
| Anthropic | Claude | `https://api.anthropic.com` | `claude-sonnet-4-20250514` |

> You need to register and obtain API keys from each provider. Most offer free credits.

### Persona Management

Comes with three built-in personas: cat-girl, smart assistant, and programmer. Create custom personas by writing your own System Prompt to define AI personality and behavior.

### Connection Management

The console **automatically detects all QQ installations** on your machine. If you have multiple QQ apps (e.g. for different accounts), they will all appear as selectable options — just pick one and click Connect.

Connect, scan the QR code, and disconnect or switch accounts at any time.

### Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| Max interactions per user | Max conversation rounds per user per session | 20 |
| Max tokens | Max AI response length per message | 2000 |
| Temperature | Higher = more random, lower = more deterministic | 0.8 |
| API timeout | Max seconds to wait for AI response | 20 |
| Cooldown | Min seconds between messages from same user | 5 |
| Max context messages | How many recent messages AI remembers | 20 |

---

## Daily Usage

After setup, send a private message to the bot's QQ account **from a different QQ account** to receive AI replies.

Each session: just start the program and click Connect in the console. Press `Ctrl + C` to stop.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | NoneBot2 + FastAPI |
| Protocol | OneBot V11 (NapCat Reverse WebSocket) |
| AI Integration | OpenAI-compatible API / Anthropic Claude API |
| Frontend | Vue 3 + TypeScript + Vite |
| Persistence | JSON files (Pydantic model validation) |

## Project Structure

```
qq-ai-auto-reply/
├── bot.py                      # NoneBot2 entry point
├── .env                        # Framework config (HOST / PORT / log level)
├── requirements.txt            # Python dependencies
├── run.sh                      # macOS / Linux start script
├── run.bat                     # Windows start script
├── config/                     # Configuration system
│   ├── __init__.py             #   Config loader (singleton)
│   ├── settings.py             #   Pydantic settings model
│   └── defaults.py             #   Defaults & built-in persona presets
├── providers/                  # AI provider adapters
│   ├── base.py                 #   Abstract base class AIProvider
│   ├── openai_compat.py        #   OpenAI-compatible adapter
│   └── claude.py               #   Anthropic Claude adapter
├── plugins/
│   └── ai_chat.py              # Core chat plugin
├── web/                        # Web console backend
│   ├── __init__.py             #   Mount API + static files to FastAPI
│   ├── api/                    #   REST API routes
│   └── frontend/dist/          #   Vue 3 frontend build output
├── frontend/                   # Vue 3 frontend source
└── data/                       # Runtime data (auto-generated, gitignored)
```

## Frontend Development

```bash
cd frontend
npm install
npm run dev      # Dev mode, API proxied to :18080
npm run build    # Build to web/frontend/dist/
```

---

## Security

To avoid credential leaks:

1. **Never store real secrets in tracked `.env` or `data/`** — the repo `.env` should only keep local HOST / PORT defaults, while API keys live in `data/providers.json`.
2. **API is local-only by default** — Remote access to `/api/*` is rejected unless explicitly enabled.
3. **For remote access** — Set `ALLOW_REMOTE_WEB=1` and configure authentication in your reverse proxy (Basic Auth / OAuth / IP whitelist).
4. **Pre-publish check** — Run `git status --short` to ensure no `data/*.json`, `.env`, or key files are staged.
5. **Key rotation** — If you ever committed an API key in history, rotate it immediately on the provider's dashboard.

---

## Acknowledgements

- **[NoneBot2](https://github.com/nonebot/nonebot2)** — Cross-platform Python async bot framework
- **[NapCatQQ](https://github.com/NapNeko/NapCatQQ)** — Modern NTQQ-based bot protocol implementation
- **[Vue.js](https://github.com/vuejs/core)** — Progressive JavaScript framework
- **[Vite](https://github.com/vitejs/vite)** — Next-generation frontend build tool
- **[FastAPI](https://github.com/fastapi/fastapi)** — Modern, high-performance Python web framework
- **[Pydantic](https://github.com/pydantic/pydantic)** — Data validation and settings management

## Related Projects

| Project | Description |
|---------|-------------|
| [NapCatQQ](https://github.com/NapNeko/NapCatQQ) | QQ protocol implementation |
| [NapCat-Installer](https://github.com/NapNeko/NapCat-Installer) | NapCat cross-platform installer |
| [NapCat-Mac-Installer](https://github.com/NapNeko/NapCat-Mac-Installer) | NapCat macOS installer |
| [NoneBot2 Docs](https://nonebot.dev/) | NoneBot2 official documentation |
| [OneBot V11](https://github.com/botuniverse/onebot-11) | OneBot V11 protocol specification |

---

## License

This project is licensed under the [Limited Redistribution License](./LICENSE).

- Commercial use is prohibited
- Redistribution is allowed with license and copyright notice retained
- Modified code may not be publicly distributed

See [LICENSE](./LICENSE) for details.

## Disclaimer

**Please read the following before using this project:**

1. **This project is for learning and personal use only.** It must not be used for commercial purposes or any activity that violates applicable laws.

2. **This project relies on [NapCatQQ](https://github.com/NapNeko/NapCatQQ) for QQ protocol integration.** NapCat works by modifying the QQ client, which may violate Tencent's QQ Terms of Service. Using this project may result in QQ account restrictions or bans.

3. **The author assumes no liability for any direct or indirect damages** arising from the use of this project, including but not limited to account bans, data loss, or financial loss.

4. **Please do not mention this project in other communities** (including other protocol or bot project communities) to avoid unnecessary disputes. For suggestions, please use GitHub Issues.

5. **Users must comply with the laws and regulations of their jurisdiction.** All consequences arising from misuse of this project are the sole responsibility of the user.

**By downloading, installing, or using this project, you acknowledge that you have read and agreed to the above statement.**

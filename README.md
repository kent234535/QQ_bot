<p align="center">
  <h1 align="center">QQ Bot</h1>
  <p align="center">基于 NoneBot2 + NapCat 的 QQ AI 聊天机器人</p>
  <p align="center">
    <a href="#功能特性">功能</a> ·
    <a href="#快速开始">快速开始</a> ·
    <a href="#web-控制台">控制台</a> ·
    <a href="#项目结构">结构</a> ·
    <a href="#许可证">许可证</a>
  </p>
</p>

---

## 功能特性

- **私聊 AI 对话** — 自动回复私聊消息，支持上下文连续对话
- **多平台 AI 支持** — OpenAI 兼容 API（阿里云百炼、DeepSeek、OpenRouter、SiliconFlow 等）及 Anthropic Claude
- **多角色切换** — 内置猫娘、智能助手、程序员角色，支持自定义
- **Web 控制台** — 浏览器管理所有配置，无需手动编辑文件
- **一键连接** — Web 端启动 NapCat、扫码登录 QQ，全程可视化
- **跨平台** — 支持 macOS 和 Windows

## 技术栈

| 层 | 技术 |
|---|------|
| 后端框架 | NoneBot2 + FastAPI |
| 协议适配 | OneBot V11（NapCat 反向 WebSocket） |
| AI 接入 | OpenAI 兼容 API / Anthropic Claude API |
| 前端 | Vue 3 + TypeScript + Vite |
| 数据持久化 | JSON 文件（Pydantic 模型校验） |

## 前置要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | >= 3.10 | 运行后端 |
| Git | 任意 | 拉取代码 |
| QQ 桌面版 | QQNT 架构 | [下载地址](https://im.qq.com) |
| NapCat | 最新版 | QQ 协议端，见下方安装说明 |

---

## 快速开始

> 以下步骤假设你的电脑上尚未安装任何依赖。请根据操作系统选择对应章节。

### macOS

#### 1. 安装基础工具

```bash
# 安装 Xcode Command Line Tools（包含 Git）
xcode-select --install

# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python 3.12
brew install python@3.12

# 验证
python3 --version   # 应输出 Python 3.12.x 或更高
git --version
```

#### 2. 安装 QQ 桌面版

前往 [im.qq.com](https://im.qq.com) 下载并安装 QQ 桌面版（QQNT 版本）。

安装完成后**无需登录**，后续通过 NapCat 启动并扫码登录。

QQ 默认安装位置：`/Applications/QQ.app`

#### 3. 安装 NapCat

macOS 使用 NapCat 官方安装器：

```bash
# 下载 NapCat macOS 安装器
# 前往 https://github.com/NapNeko/NapCat-Mac-Installer/releases 下载最新版 .dmg 文件

# 打开安装器并按提示完成安装
# 安装器会自动将 NapCat 部署到以下位置：
#   ~/Library/Containers/com.tencent.qq/Data/Documents/loadNapCat.js
```

> **备选方案**：如果安装器不可用，也可使用 Shell 脚本安装：
> ```bash
> curl -o napcat.sh https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.sh
> sudo bash napcat.sh --tui
> ```

安装完成后可验证：

```bash
ls ~/Library/Containers/com.tencent.qq/Data/Documents/loadNapCat.js
# 或
ls ~/Library/Application\ Support/QQ/loadNapCat.js
```

如果文件存在，说明 NapCat 安装成功。

#### 4. 部署项目

```bash
# 克隆仓库
cd ~/Desktop
git clone https://github.com/kent234535/QQ_bot.git
cd ~/Desktop/QQ_bot

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt
```

#### 5. 启动

```bash
cd ~/Desktop/QQ_bot
source venv/bin/activate
python bot.py
```

看到以下输出即启动成功：

```
[QQ Bot] 启动中，监听 127.0.0.1:8080 ...
```

打开浏览器访问 **http://127.0.0.1:8080/web/** 进入控制台。

---

### Windows

#### 1. 安装 Git

1. 前往 https://git-scm.com/download/win 下载安装包
2. 运行安装程序，全部默认选项，点 **Next** 直到完成
3. 安装后在开始菜单搜索 **Git Bash** 并打开

> 后续所有命令均在 **Git Bash** 中执行。

#### 2. 安装 Python

1. 前往 https://www.python.org/downloads/ 下载最新版
2. 运行安装程序，**务必勾选底部 "Add Python to PATH"**，然后点 **Install Now**
3. 在 Git Bash 中验证：

```bash
python --version   # 应输出 Python 3.12.x 或更高
```

> **注意**：Windows 使用 `python` 命令，macOS 使用 `python3`。下文 Windows 章节统一使用 `python`。

#### 3. 安装 QQ 桌面版

前往 [im.qq.com](https://im.qq.com) 下载并安装 QQ 桌面版（QQNT 版本）。

安装完成后**无需登录**。

QQ 默认安装位置：`C:\Program Files\Tencent\QQNT`

#### 4. 安装 NapCat

在 **PowerShell**（以管理员身份运行）中执行：

```powershell
# Windows 11
curl -o install.ps1 https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.ps1
powershell -ExecutionPolicy ByPass -File ./install.ps1 -verb runas
```

> **Windows 10** 用户如果上述命令失败，请前往 [NapCat-Installer Releases](https://github.com/NapNeko/NapCat-Installer/releases) 手动下载安装。

安装完成后，NapCat loader 通常位于以下位置之一：

```
%USERPROFILE%\Documents\loadNapCat.js
%LOCALAPPDATA%\NapCat\loadNapCat.js
```

#### 5. 部署项目

回到 **Git Bash** 中执行：

```bash
# 克隆仓库
cd ~/Desktop
git clone https://github.com/kent234535/QQ_bot.git
cd ~/Desktop/QQ_bot

# 创建并激活虚拟环境
python -m venv venv
source venv/Scripts/activate

# 安装 Python 依赖
python -m pip install -r requirements.txt
```

#### 6. 启动

**方式一：命令行启动**

```bash
cd ~/Desktop/QQ_bot
source venv/Scripts/activate
python bot.py
```

**方式二：双击启动**

直接双击项目根目录下的 `run.bat`。

看到以下输出即启动成功：

```
[QQ Bot] 启动中，监听 127.0.0.1:8080 ...
```

打开浏览器访问 **http://127.0.0.1:8080/web/** 进入控制台。

> **注意**：如果连接 QQ 时提示权限错误，请以管理员身份运行 Git Bash 或 `run.bat`。

---

## Web 控制台

启动后访问 `http://127.0.0.1:8080/web/`，左侧菜单包含四个页面：

### 模型配置

1. 点击 **+ 添加模型**
2. 填写名称、类型、Base URL、API Key、模型名称
3. 点击 **保存**，然后在卡片上点击 **启用**

常见 AI 平台配置参考：

| 平台 | 类型 | Base URL | 模型示例 |
|------|------|----------|----------|
| DeepSeek | OpenAI 兼容 | `https://api.deepseek.com/v1` | `deepseek-chat` |
| 阿里云百炼 | OpenAI 兼容 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |
| OpenRouter | OpenAI 兼容 | `https://openrouter.ai/api/v1` | `meta-llama/llama-3-70b` |
| Anthropic | Claude | `https://api.anthropic.com` | `claude-sonnet-4-20250514` |

> API Key 需要到对应平台官网注册并申请，大部分平台提供免费额度。

### 角色管理

- 内置三个角色：猫娘、智能助手、程序员
- 点击 **启用** 切换当前角色
- 支持 **+ 添加角色** 创建自定义角色

### 连接管理

1. 如果检测到多个 QQ 应用，选择要使用的那个
2. 点击 **连接**，等待 QQ 启动
3. 出现二维码后，用手机 QQ 扫码登录
4. 状态变为 **已连接** 即可

### 参数设置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 每用户最大交互次数 | 每个用户每次重启前最多聊多少轮 | 20 |
| 单次最大 Token 数 | AI 单次回复的最大长度 | 2000 |
| 生成温度 | 越高越随机，越低越稳定 | 0.8 |
| API 超时 | 等待 AI 回复的最大秒数 | 20 |
| 消息冷却时间 | 同一用户两次发消息的最短间隔（秒） | 5 |
| 最大上下文消息数 | AI 记住最近多少条对话 | 20 |

---

## 使用方式

配置完成后，用**另一个 QQ 号**给机器人 QQ 发私聊消息，即可收到 AI 回复。

日常使用只需启动程序并在控制台点击连接：

**macOS：**

```bash
cd ~/Desktop/QQ_bot
source venv/bin/activate
python bot.py
```

**Windows：**

双击 `run.bat`，或：

```bash
cd ~/Desktop/QQ_bot
source venv/Scripts/activate
python bot.py
```

按 `Ctrl + C` 停止程序。

---

## 项目结构

```
QQ_bot/
├── bot.py                      # NoneBot2 入口
├── .env                        # 框架配置（HOST / PORT / 日志级别）
├── requirements.txt            # Python 依赖
├── run.sh                      # macOS / Linux 启动脚本
├── run.bat                     # Windows 启动脚本
├── config/                     # 配置系统
│   ├── __init__.py             #   配置加载器（单例模式）
│   ├── settings.py             #   Pydantic 设置模型
│   └── defaults.py             #   默认值与内置角色预设
├── providers/                  # AI 提供商适配器
│   ├── base.py                 #   抽象基类 AIProvider
│   ├── openai_compat.py        #   OpenAI 兼容适配器
│   └── claude.py               #   Anthropic Claude 适配器
├── plugins/
│   └── ai_chat.py              # 核心聊天插件
├── web/                        # Web 控制台后端
│   ├── __init__.py             #   挂载 API + 静态文件到 FastAPI
│   ├── api/                    #   REST API 路由
│   │   ├── settings.py         #     设置 CRUD
│   │   ├── providers.py        #     模型 CRUD
│   │   ├── personas.py         #     角色 CRUD
│   │   └── napcat.py           #     NapCat 连接管理
│   └── frontend/dist/          #   Vue 3 前端构建产物
├── frontend/                   # Vue 3 前端源码
│   ├── src/views/              #   页面组件
│   └── src/api/client.ts       #   API 客户端
└── data/                       # 运行时数据（自动生成，不纳入版本控制）
    ├── settings.json
    ├── providers.json
    └── personas.json
```

## 前端开发

如果需要修改前端界面：

```bash
cd ~/Desktop/QQ_bot/frontend
npm install
npm run dev      # 开发模式，API 代理到 :8080
npm run build    # 构建到 web/frontend/dist/
```

---

## 致谢

本项目的实现离不开以下开源项目：

- **[NoneBot2](https://github.com/nonebot/nonebot2)** — 跨平台 Python 异步机器人框架
- **[NapCatQQ](https://github.com/NapNeko/NapCatQQ)** — 现代化的基于 NTQQ 的 Bot 协议端实现
- **[Vue.js](https://github.com/vuejs/core)** — 渐进式 JavaScript 框架
- **[Vite](https://github.com/vitejs/vite)** — 下一代前端构建工具
- **[FastAPI](https://github.com/fastapi/fastapi)** — 现代、高性能的 Python Web 框架
- **[Pydantic](https://github.com/pydantic/pydantic)** — 数据验证与设置管理

## 相关项目

| 项目 | 说明 |
|------|------|
| [NapCatQQ](https://github.com/NapNeko/NapCatQQ) | QQ 协议端实现 |
| [NapCat-Installer](https://github.com/NapNeko/NapCat-Installer) | NapCat 跨平台安装脚本 |
| [NapCat-Mac-Installer](https://github.com/NapNeko/NapCat-Mac-Installer) | NapCat macOS 安装器 |
| [NoneBot2 文档](https://nonebot.dev/) | NoneBot2 官方文档 |
| [OneBot V11 标准](https://github.com/botuniverse/onebot-11) | OneBot V11 协议规范 |

---

## 许可证

本项目采用 [Limited Redistribution License](./LICENSE) 许可证。

- 未经许可，禁止用于商业用途
- 允许在保留许可证全文和版权信息的前提下进行再分发
- 允许进行小规模修改用于再分发，但修改后的代码不得公开发布

详见 [LICENSE](./LICENSE) 文件。

## 免责声明

**使用本项目前，请务必阅读以下内容：**

1. **本项目仅供学习和个人使用**，不得用于商业用途或任何违反法律法规的场景。

2. **本项目依赖 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 实现 QQ 协议对接。** NapCat 通过修改 QQ 客户端实现功能，这可能违反腾讯 QQ 用户协议。使用本项目可能导致 QQ 账号被限制或封禁。

3. **作者不对因使用本项目而产生的任何直接或间接损失承担责任**，包括但不限于账号封禁、数据丢失、财产损失等。

4. **请勿在其他社区（包括其他协议端项目或相关应用项目的社区）中提及本项目**，以避免不必要的争议。如有建议，请通过 GitHub Issue 反馈。

5. **用户应自行遵守所在地区的法律法规。** 因滥用本项目而产生的一切问题，由使用者自行承担全部责任。

**下载、安装或使用本项目即表示您已阅读并同意上述声明。**

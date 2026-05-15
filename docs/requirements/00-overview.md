# 00 — 产品概述

> 版本：0.0.1

## 1. 产品定位

**WowooAI 是人力窝面向日常办公与业务流程自动化的全能数字员工平台。**

- 用户在桌面端打开 WowooAI，就拥有一个或多个"数字员工"，每个数字员工有自己的人格、技能、记忆和接入渠道。
- 数字员工通过对话理解用户需求，调用本地工具（文件、Shell、浏览器、桌面应用）、MCP 工具、内置 skill 完成任务。
- 数字员工也可以挂接到外部渠道（钉钉、飞书、Telegram、iMessage、微信、Mattermost、QQ 等），在这些渠道里直接服务团队。

**不是什么**：
- 不是网页版 SaaS——核心交付形态是**本地桌面客户端**。
- 不是单纯的 chatbot——具备本机文件操作、浏览器自动化、定时任务等"能干活"的能力。
- 不是 IDE 插件 / Coding Agent——目标场景是办公自动化与业务流程，不是软件开发。

## 2. 目标用户

| 用户类型 | 典型需求 |
|---|---|
| HR / 社保运行岗 | 多系统操作（renliwo 主站、QD 外包系统）、合同/账单/报表导出、政策跟踪、群消息提醒 |
| 业务运营 | 表格处理（xlsx/docx/pdf）、定时数据汇报、跨系统数据搬运、客户问题响应 |
| 团队管理者 | 在钉钉/飞书群里挂数字员工、群消息汇报、心跳巡检 |
| 内部技术人员 | 调用 MCP 工具、对接内部系统、定制 skill |

明确**不优先**的用户群：开发者 coding assistant、海外消费级 chat 用户。

## 3. 核心价值主张

| # | 价值 | 落地方式 |
|---|---|---|
| 1 | **零依赖即开即用** | macOS .app / Windows .msi 解压即用，无需用户安装 Python / Node / Chrome |
| 2 | **本机闭环** | 业务数据、记忆、配置全部留在用户机器；不强��云端中转 |
| 3 | **多渠道统一** | 一个数字员工同时接入控制台 / 群聊 / 邮件 / 工单系统 |
| 4 | **多模型可切换** | 支持 OpenAI / Anthropic / Gemini / DashScope / Ollama / LMStudio / OpenRouter 等 |
| 5 | **可扩展技能** | 内置 skill_pool + 用户工作区自定义 skill；skill 是 markdown，模型自然加载 |
| 6 | **生产级守卫** | 工具守卫 / 文件守卫 / 技能扫描 / 副本沙箱，避免误改用户原始文件 |

## 4. 总体架构

```
┌──────────────────── 桌面客户端（.app / .msi）─────────────────────┐
│                                                                  │
│  ┌────────────┐                                                  │
│  │ pywebview  │  WKWebView / EdgeChromium 加载 console/dist     │
│  │  (UI)      │  ↕ HTTP (127.0.0.1:8088 or random)              │
│  └─────┬──────┘                                                  │
│        │                                                          │
│  ┌─────▼─────────────────────────────────────────────────────┐  │
│  │ FastAPI 后端（src/wowooai/app）                            │  │
│  │   - 路由 / 鉴权 / SSE 推流                                  │  │
│  │   - MultiAgentManager: 管理 N 个数字员工实例                │  │
│  │   - 渠道接入（console / 钉钉 / 飞书 / iMessage / ...）       │  │
│  │   - Cron 调度器                                            │  │
│  └──────┬────────────────────────────────────────────────────┘  │
│         │                                                         │
│   ┌─────▼────────┐  ┌──────────────┐  ┌──────────────────┐      │
│   │ ReActAgent   │  │ Toolkit      │  │ LightContextMgr  │      │
│   │ (agentscope) │←→│ (内置工具    │←→│ ReMeMemoryMgr    │      │
│   │              │  │  + MCP)      │  │ (记忆与压缩)      │      │
│   └──────────────┘  └──────────────┘  └──────────────────┘      │
│         │                  │                                      │
│         ▼                  ▼                                      │
│   ┌──────────┐       ┌──────────────┐                            │
│   │ Provider │       │ Built-in     │                            │
│   │ (LLM     │       │ Tools:       │                            │
│   │  API)    │       │ shell /      │                            │
│   └──────────┘       │ file_io /    │                            │
│                      │ browser_use /│                            │
│                      │ desktop_* /  │                            │
│                      │ renliwo_*    │                            │
│                      └──────────────┘                            │
│                                                                  │
│  bundled deps: Python 3.11 env / Playwright Chromium /          │
│                Node.js 22 + agent-browser / pandoc              │
└─────────────────────────────────────────────────────────────────┘
                              ↑
                              │ 外部渠道（可选）
                              │
        ┌──────┬────┬─────┬───┴───┬──────┬────────┐
        ▼      ▼    ▼     ▼       ▼      ▼        ▼
      钉钉   飞书 Telegram iMessage 微信 Matrix Mattermost ...
```

## 5. 关键非功能需求

| 类目 | 要求 |
|---|---|
| 安装 | 用户解压即用；不需要任何先决依赖（Python / Node / Chrome 都已 bundle） |
| 启动 | 首启 ≤ 20 秒到窗口可见；后续启动 ≤ 10 秒 |
| 包体 | macOS .app ≤ 2.5GB；Windows installer ≤ 1.5GB（解压后 ≤ 2.5GB） |
| 隐私 | 凭据、对话、记忆默认全在用户机器；不主动上传任何文件 |
| 安全 | 工具守卫拦截危险 shell；副本沙箱防误改 Desktop/Documents/Downloads 下原始文件 |
| 多平台 | macOS 11+（Apple Silicon + Intel）、Windows 10 21H1+ / Windows 11 |
| 多语言 | 默认中文；UI 全套支持中英；SKILL.md 双语 |

## 6. 版本范围（0.0.1）

**包含**：
- 完整的数字员工管理（创建 / 切换 / 配置 / 删除）
- 9 类内置工具（shell / file_io / browser_use / renliwo_browser / desktop_* / view_image / view_video / send_file / get_token_usage 等）
- 11 个默认预装 skill（make_plan / file_reader / pdf / docx / xlsx / pptx / cron / browser_visible / browser_cdp / desktop_control / agent_browser）
- 14 个渠道适配器（不强制开启，按需启用）
- 12 个 LLM provider 类型
- macOS + Windows 桌面打包
- Cron 定时任务系统
- ReMe 记忆 + Light context manager 组合
- MCP 与 ACP 接入能力

**不包含**：见 [12-out-of-scope.md](12-out-of-scope.md)。

## 7. 版本号

```python
# src/wowooai/__version__.py
__version__ = "0.0.1"
```

升级到 0.0.2 / 0.1.0 的判定见 [`docs/changelog/backend.md`](../changelog/backend.md) 各 `§N` 是否累计触发版本号变更。本目录在 minor / major 版本变更时同步刷新。

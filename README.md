<div align="center">

# WowooAI

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black.svg?logo=github)](https://github.com/agentscope-ai/wowooai)
[![PyPI](https://img.shields.io/pypi/v/wowooai?color=3775A9&label=PyPI&logo=pypi)](https://pypi.org/project/wowooai/)
[![Documentation](https://img.shields.io/badge/Docs-Website-green.svg?logo=readthedocs&label=Docs)](https://wowooai.agentscope.io/)
[![Python Version](https://img.shields.io/badge/python-3.10%20~%20%3C3.14-blue.svg?logo=python&label=Python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-red.svg?logo=apache&label=License)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join_Us-blueviolet.svg?logo=discord)](https://discord.gg/eYMpfnkG8h)
[![X](https://img.shields.io/badge/X-Follow_Us-black.svg?logo=x)](https://x.com/agentscope_ai)
[![DingTalk](https://img.shields.io/badge/DingTalk-Join_Us-orange.svg)](https://qr.dingtalk.com/action/joingroup?code=v1,k1,OmDlBXpjW+I2vWjKDsjvI9dhcXjGZi3bQiojOq3dlDw=&_dt_no_comment=1&origin=11)

<p align="center">
  <img src="docs/changelog/brand/wowooai-logo.svg" alt="WowooAI Logo" width="120">
</p>

<p align="center"><b>Works for you, grows with you.</b></p>

<p align="center">懂你所需，伴你左右。</p>

</div>

---

Your personal AI assistant — easy to install, deploy locally or in the cloud, connect across channels, extend with ease.

你的个人 AI 助手 — 安装极简、本地与云上均可部署、多端接入、能力轻松扩展。

---

## Features / 核心特性

| # | EN | 中文 |
|---|---|------|
| 1 | **Under Your Control** — Memory & personalization fully under your control. Deploy locally (data stays on your machine) or in the cloud. No third-party hosting, no data upload. | **由你掌控** — 记忆与个性化完全由你掌控，支持本地或云端部署。无第三方托管，无数据上传。 |
| 2 | **Skills Extension** — Built-in scheduling, PDF/Office processing, news digest; custom skills auto-loaded, no lock-in. Skills determine what WowooAI can do. | **Skills 扩展** — 内置定时任务、PDF/Office 处理、新闻摘要；自定义技能自动加载，无绑定。通过 Skills 决定 WowooAI 能做什么。 |
| 3 | **Multi-agent Collaboration** — Create multiple independent agents, each with their own role; enable collaboration skills for inter-agent communication to tackle complex tasks together. | **多智能体协作** — 创建多个独立智能体，各司其职；启用协作技能，智能体间互相通信共同完成复杂任务。 |
| 4 | **Multi-layer Security** — Tool guard, file access control, skill security scanning to ensure safe operation. | **多层安全防护** — 工具防护、文件访问控制、技能安全扫描，保障运行安全。 |
| 5 | **Every Channel** — DingTalk, Feishu, WeChat, Discord, Telegram, QQ, WeCom, and more. One WowooAI, connect as needed. | **全域触达** — 钉钉、飞书、微信、QQ、企业微信、Discord、Telegram 等频道，一个 WowooAI 按需连接。 |
| 6 | **Memory-Evolving & Proactive** — Agent learns from interactions, reflects on experience, and proactively serves you. Gets smarter the more you use it. | **记忆进化与主动交互** — 智能体从交互中学习、反思经验、主动服务，越用越聪明。 |

---

## What You Can Do / 你可以用它做什么

- **Social Media** — Daily hot post digests (Xiaohongshu, Zhihu, Reddit), Bilibili/YouTube video summaries.
- **Productivity** — Email & newsletter highlights pushed to DingTalk/Feishu/QQ; email & calendar organization.
- **Creative & Building** — Describe your goal before sleep, auto-execute, wake up to a prototype.
- **Research & Learning** — Track tech & AI news, personal knowledge base search and reuse.
- **Desktop & Files** — Organize and search local files, read & summarize documents, request files in chat.
- **Explore More** — Combine Skills with scheduled tasks into your own agentic app.

---

- **社交媒体** — 每日热帖摘要（小红书、知乎、Reddit），B 站/YouTube 新视频摘要。
- **生产力** — 邮件与 Newsletter 精华推送到钉钉/飞书/QQ，邮件与日历整理。
- **创意与构建** — 睡前说明目标、自动执行，次日获得雏形。
- **研究与学习** — 追踪科技与 AI 资讯，个人知识库检索复用。
- **桌面与文件** — 整理与搜索本地文件、阅读与摘要文档，在会话中索要文件。
- **探索更多** — 用 Skills 与定时任务组合成你自己的 agentic app。

---

## Quick Start / 快速开始

### Install / 安装

```bash
pip install wowooai
```

### CLI Mode / 命令行模式

```bash
wowooai app
```

Open the web console at `http://127.0.0.1:8088` in your browser.

浏览器打开 `http://127.0.0.1:8088` 访问控制台。

### Desktop Client / 桌面客户端

```bash
wowooai desktop
```

A native desktop window will launch with the console built in.

桌面客户端启动后直接弹出控制台窗口，无需浏览器。

### From Source / 源码安装

```bash
git clone https://github.com/agentscope-ai/wowooai.git
cd wowooai
pip install -e ".[dev]"
```

---

## Project Structure / 项目结构

```
wowooai/
├── src/wowooai/          # Python package source
│   ├── agents/           # Agent definitions, skills, tools
│   ├── app/              # Core application (routing, workspace, services)
│   ├── channels/         # Channel implementations (DingTalk, Feishu, etc.)
│   ├── cli/              # CLI entry points (app, desktop commands)
│   ├── config/           # Configuration management
│   └── console/          # Web console frontend (built assets)
├── console/              # Web console source (TypeScript/React)
├── docs/                 # Documentation & changelog
└── tests/                # End-to-end tests
```

---

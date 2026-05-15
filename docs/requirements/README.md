# WowooAI 0.0.1 需求文档

> 版本：**0.0.1**
> 状态：初始版本（First Public Build）
> 适用范围：本仓库（`/Users/rlw/AI项目/wowooai`）的所有后端、前端、技能、打包产物

本目录记录 WowooAI 0.0.1 版本各子模块的需求规格。所有变更与"为什么这么做"的历史决策见 [`docs/changelog/`](../changelog/)；本目录只描述"当前版本应该是什么样"。

---

## 文档结构

文档分两部分：

- **Part 1（00–12）** —— 模块规格，按"用户可配置面"切分，面向"接入 / 配置 / 复刻"读者。
- **Part 2（13–26）** —— 机制深入，按"系统能力 / 内部协议"切分，面向"读完代码也能讲清原理"读者。

### Part 1 — 模块规格

| 文件 | 范围 |
|---|---|
| [00-overview.md](00-overview.md) | 产品概述、目标用户、核心定位、整体架构 |
| [01-agents.md](01-agents.md) | 数字员工（Agent）系统：profile、模板、运行时、上下文/记忆管理 |
| [02-tools.md](02-tools.md) | 内置工具：file_io / shell / browser / desktop / send_file 等 |
| [03-skills.md](03-skills.md) | 内置 skill 与 skill_pool、技能预装策略 |
| [04-channels.md](04-channels.md) | 外部渠道集成（console / 钉钉 / 飞书 / Telegram / iMessage / 微信 等） |
| [05-providers.md](05-providers.md) | LLM 模型供应商（OpenAI / Anthropic / Gemini / Ollama / OpenRouter 等） |
| [06-security.md](06-security.md) | 工具守卫、文件守卫、技能扫描、审批级别、副本沙箱 |
| [07-frontend.md](07-frontend.md) | 前端控制台：导航、聊天页、配置页、术语统一 |
| [08-cron-heartbeat.md](08-cron-heartbeat.md) | 定时任务与心跳 |
| [09-mcp-acp.md](09-mcp-acp.md) | MCP（外部工具协议）与 ACP（外�� agent 协议） |
| [10-packaging.md](10-packaging.md) | macOS / Windows 桌面打包，零依赖、即开即用 |
| [11-startup-runtime.md](11-startup-runtime.md) | 启动流程、launcher、进程守护 |
| [12-out-of-scope.md](12-out-of-scope.md) | 本版本明确不做的事 |

### Part 2 — 机制深入

| 文件 | 范围 |
|---|---|
| [13-agent-engine.md](13-agent-engine.md) | ReAct 循环、auto-continue、LLM 限流重试、中断恢复、模型调用栈 |
| [14-prompt-system.md](14-prompt-system.md) | 提示词文件（AGENTS/SOUL/PROFILE/BOOTSTRAP）加载顺序、动态 section、PromptBuilder |
| [15-context-compaction.md](15-context-compaction.md) | 上下文压缩 + 工具结果裁剪两套机制的触发、保留、落盘 |
| [16-memory.md](16-memory.md) | 每日日志、MEMORY.md、dream cron、proactive memory、embedding |
| [17-mission-orchestration.md](17-mission-orchestration.md) | Mission 两阶段任务编排、PRD schema、状态机 |
| [18-streaming.md](18-streaming.md) | SSE 协议、消息块类型、task_tracker、Console push store |
| [19-sub-agents.md](19-sub-agents.md) | chat_with_agent / submit_to_agent / delegate_external_agent、session 边界 |
| [20-approval-flow.md](20-approval-flow.md) | ApprovalService、PendingApproval、跨 session 审批路由 |
| [21-plan-mode.md](21-plan-mode.md) | Plan 模式、subtask 状态机、SSE 广播、与 ReAct 的钩接 |
| [22-runner-queue.md](22-runner-queue.md) | AgentRunner / TaskTracker / ChatManager / 命令派发 / daemon |
| [23-plugins.md](23-plugins.md) | 插件体系（provider / hook / control command 扩展点） |
| [24-backup.md](24-backup.md) | 备份与恢复（范围 / 凭据隐私 / safe_swap 原子替换） |
| [25-tunnel.md](25-tunnel.md) | Cloudflare Quick Tunnel 内网穿透 |
| [26-cli.md](26-cli.md) | CLI 子命令总览、doctor、shutdown、uninstall |

---

## 阅读建议

- **想了解产品做什么**：从 [00-overview.md](00-overview.md) 开始。
- **想接入一个新渠道 / 模型供应商 / 工具**：直接看 Part 1 对应模块。
- **想了解某项能力为什么这样设计**：去 Part 2 找对应机制文档。
- **想知道某次具体改动的历史**：去 [`docs/changelog/backend.md`](../changelog/backend.md) 找对应 `§N`。
- **想打包发版**：[10-packaging.md](10-packaging.md) + [`docs/changelog/packaging-macos.md`](../changelog/packaging-macos.md) / [`docs/changelog/packaging-windows.md`](../changelog/packaging-windows.md)。

---

## 与 changelog 的关系

| 维度 | 需求文档（本目录） | 变更日志（changelog/） |
|---|---|---|
| 时态 | "当前版本应是什么样" | "做了什么、为什么" |
| 粒度 | 模块级 / 机制级 | 提交级 |
| 读者 | 新加入的开发 / 产品 / 复刻者 | 维护者 / 排查问题 |
| 更新时机 | 大版本（0.0.1 / 0.1.0 / 1.0.0） | 每次落地一项变更 |

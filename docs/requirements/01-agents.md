# 01 — 数字员工（Agent）系统

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/](../../src/wowooai/agents/) · [src/wowooai/app/multi_agent_manager.py](../../src/wowooai/app/multi_agent_manager.py) · [src/wowooai/config/config.py](../../src/wowooai/config/config.py)

## 1. 概念

一个 **数字员工（Agent）** 由以下要素构成：

| 要素 | 存储位置 | 说明 |
|---|---|---|
| Profile ref | `~/.wowooai/config.json > agents.profiles[id]` | id、workspace_dir、enabled |
| 完整配置 | `<workspace>/agent.json` | 名称、描述、模型、渠道、工具、安全级别、scene prompts |
| 系统提示词 | `<workspace>/AGENTS.md` `SOUL.md` `PROFILE.md` `BOOTSTRAP.md` | 行为约束 + 人格 + 身份 |
| 技能 | `<workspace>/skills/<name>/SKILL.md` | 按需启用的领域 skill |
| 记忆 | `<workspace>/MEMORY.md` + `memory/YYYY-MM-DD.md` | 长期记忆 + 每日日志 |
| 对话历史 | `<workspace>/sessions/*.json` | 多会话归档 |
| 定时任务 | `<workspace>/jobs.json` | Cron 任务列表 |

## 2. 默认数字员工

首次安装后必须存在 **id="default"** 的数字员工：

- 名称：`wowooai`
- 描述：`wowooai 是人力窝的全能数字员工，面向日常办公与业务流程自动化...`
- 工作区：`~/.wowooai/workspaces/default/`
- 模板：`DEFAULT_AGENT_TEMPLATE`
- 语言：`zh`
- 审批级别：`AUTO`

**预装技能（11 个）**：

```python
DEFAULT_TEMPLATE_SKILL_NAMES = (
    "make_plan",
    "file_reader",
    "pdf",
    "docx",
    "xlsx",
    "pptx",
    "cron",
    "browser_visible",
    "browser_cdp",
    "desktop_control",
    "agent_browser",
)
```

## 3. ��置 QA Agent

每次安装额外存在 **id="wowooai_QA_Agent_0.2"**：

- 用途：内置文档/源码 QA，回答关于 WowooAI 自身的问题
- 工作区：`~/.wowooai/workspaces/wowooai_QA_Agent_0.2/`
- 预装技能：`QA_source_index`、`guidance`
- 工具集：通过 `build_qa_agent_tools_config()` 限制为 `execute_shell_command / read_file / write_file / edit_file / view_image`，其他全部禁用

## 4. Agent ID 规则

- 长度：2–64 字符
- 字符集：字母、数字、`-`、`_`
- 不能以 `-` / `_` 开头或结尾
- 不能等于 `default` 之外的保留字
- 全局唯一

## 5. 创建新 Agent

UI 路径：`/agents` → "新增"。后端：

1. 验证 ID（[config.py:150 `validate_agent_id`](../../src/wowooai/config/config.py#L150)）
2. 根据 `template_id` 选模板（见 [templates.py](../../src/wowooai/agents/templates.py)）
3. 生成 workspace 目录
4. 复制 `agents/md_files/<lang>/` 下的 MD 模板到 workspace
5. 安装模板指定的 `initial_skill_names`
6. 写入 `agent.json` 与 `config.json` profile ref
7. 启动 workspace（`MultiAgentManager.start_workspace`）

## 6. 切换 / 删除 Agent

- 切换：UI 顶部下拉选择；后端通过 `config.agents.active_agent` 持久化。
- 删除：禁止删除 `default`；删除其他 agent 时停止 workspace、移除 profile ref、保留 workspace 目录（用户决定是否手动清理）。

## 7. AgentProfileConfig 字段总览

| 字段 | 类型 | 默认 | 用途 |
|---|---|---|---|
| `id` | str | — | 唯一标识 |
| `name` | str | — | 人类可读名称 |
| `description` | str | "" | 简介 |
| `workspace_dir` | str | 自动生成 | 工作区绝对路径 |
| `template_id` | str? | None | 创建时的模板 ID |
| `channels` | ChannelConfig? | None | 各渠道独立配置 |
| `mcp` | MCPConfig? | None | MCP client 列表 |
| `heartbeat` | HeartbeatConfig? | None | 心跳任务 |
| `running` | AgentsRunningConfig | 默认 | 运行时（迭代上限、压缩、限流） |
| `llm_routing` | AgentsLLMRoutingConfig | 默认 | 本地/云端切换路由 |
| `active_model` | ModelSlotConfig? | None | 当前用的模型槽 |
| `language` | str | "zh" | UI / SKILL 语言 |
| `approval_level` | str | "AUTO" | OFF / AUTO / SMART / STRICT |
| `system_prompt_files` | list[str] | `["AGENTS.md","SOUL.md","PROFILE.md"]` | 加载顺序 |
| `tools` | ToolsConfig? | None | 工具开关 |
| `security` | SecurityConfig? | None | 守卫 / 扫描 |
| `acp` | ACPConfig? | None | 外部 agent 接入 |
| `plan` | PlanConfig | 默认 | 计划模式开关 |
| `scene_prompts` | list[ScenePrompt] | [] | 欢迎页快速提问卡片 |

## 8. 运行时行为（AgentsRunningConfig）

| 字段 | 默认 | 行为 |
|---|---|---|
| `max_iters` | 100 | ReAct 单次回合上限 |
| `auto_continue_on_text_only` | True | 模型只返回文本时自动追加 hint 再跑一轮 |
| `llm_retry_enabled` / `llm_max_retries` | True / 3 | 瞬态错误自动重试 |
| `llm_backoff_base` / `llm_backoff_cap` | 1.0 / 30.0 | 指数退避 |
| `llm_max_concurrent` | 10 | 全局并发 |
| `llm_max_qpm` | 0（关） | 60 秒滑窗 QPM 限速 |
| `llm_rate_limit_pause` / `_jitter` | 60 / 5 | 429 触发后全局暂停 |
| `llm_acquire_timeout` | 600 | 等待限流槽超时 |
| `shell_command_timeout` | 60 | shell 默认超时 |
| `max_input_length` | 128 \* 1024 | 上下文窗口 |

## 9. 上下文管理（LightContextConfig）

- backend: `light`
- `dialog_path`: 对话归档到 `<workspace>/dialog/*.jsonl`
- `token_count_estimate_divisor`: 4（按字节/4 估 token）

### 9.1 自动压缩（ContextCompactConfig）

| 字段 | 默认 |
|---|---|
| `enabled` | True |
| `compact_threshold_ratio` | 0.8 |
| `reserve_threshold_ratio` | 0.1 |
| `compact_with_thinking_block` | True |

### 9.2 工具结果裁剪（ToolResultPruningConfig）

| 字段 | 默认 | 用途 |
|---|---|---|
| `enabled` | True | 开关 |
| `pruning_recent_n` | **4** | 最近 N 条用 recent 上限 |
| `pruning_old_msg_max_bytes` | **8000** | 老消息 tool_result 字节上限（中文 ≈ 2700 字） |
| `pruning_recent_msg_max_bytes` | 50000 | 最近 N 条不超过这个字节 |
| `offload_retention_days` | 5 | 落盘 tool result 保留天数 |
| `tool_results_cache` | `tool_results` | 落盘目录名 |
| `exempt_file_extensions` | `[".md"]` | 不被裁剪的扩展名（read_file） |
| `exempt_tool_names` | `["chat_with_agent"]` | 不被裁剪的工具 |

> 这两个默认值由 [changelog/backend.md §38](../changelog/backend.md#38) 调整，旨在不压扁中文多步工具链。

## 10. 记忆系统（ReMeLightMemoryConfig）

| 字段 | 默认 |
|---|---|
| `summarize_when_compact` | True |
| `auto_memory_interval` | **5**（每 5 轮用户消息后写入 daily log） |
| `dream_cron` | `0 23 * * *`（每晚 23:00 把 daily log 提炼到 MEMORY.md） |
| `auto_memory_search_config.enabled` | False |
| `auto_memory_search_config.max_results` | 2 |
| `auto_memory_search_config.min_score` | 0.3 |
| `rebuild_memory_index_on_start` | False |
| `recursive_file_watcher` | False |
| `embedding_model_config` | 默认 OpenAI embedding，1024 维 |

### 10.1 记忆两层结构

```
<workspace>/
├─ MEMORY.md           ← 长期沉淀（dream cron 每晚刷新）
└─ memory/
   ├─ 2026-05-12.md   ← 当天的对话精华（summarizer 实时写）
   ├─ 2026-05-13.md
   └─ 2026-05-14.md
```

## 11. LLM 路由（AgentsLLMRoutingConfig）

| 字段 | 默认 | 说明 |
|---|---|---|
| `enabled` | False | 关 = 只用 active_model |
| `mode` | `local_first` | `local_first` / `cloud_first` |
| `local` | 默认空槽 | provider_id + model |
| `cloud` | None | 不填则用 providers.json 的 active_llm |

未来扩展智能切换（按 token / 延迟 / 失败率），0.0.1 不在范围。

## 12. 计划模式（PlanConfig）

| 字段 | 默认 |
|---|---|
| `enabled` | False |

启用后数字员工在执行前先输出计划；用户确认后再执行。

## 13. 场景提示（ScenePrompt）

聊天页欢迎卡片，每个项：

```json
{ "label": "导出本月合同报表", "value": "请打开 renliwo 并导出 5 月合同..." }
```

推荐 0–6 项；通过 `agent.json > scene_prompts` 维护。

## 14. 兼容性约束

- `AgentsConfig` 必须保留 legacy 字段 (`defaults` / `running` / `llm_routing` / `language` / `system_prompt_files` 等) 以便降级。
- `~/.wowooai/config.json` 与 `<workspace>/agent.json` 双层写入；升级时不破坏旧 agent。
- 全新安装跳过 legacy migration（changelog §22 / §23）。

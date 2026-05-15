# 16 — 记忆系统

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/memory/](../../src/wowooai/agents/memory/) · `ReMeLightMemoryConfig`

## 1. 概念

数字员工的"记忆"分两层：

| 层 | 文件 | 何时写 | 何时读 |
|---|---|---|---|
| **每日日志（daily logs）** | `<workspace>/memory/YYYY-MM-DD.md` | 每 N 条用户消息 / 上下文压缩时 | 检索时聚合 |
| **长期记忆（MEMORY.md）** | `<workspace>/MEMORY.md` | dream cron 每晚提炼 | 系统提示注入（reference）+ 检索 |

加上：
- 对话归档 `dialog/*.jsonl`（详见 [15-context-compaction.md §5](15-context-compaction.md)）；
- 落盘工具结果 `tool_results/*.txt`（详见 [15 §2.2](15-context-compaction.md)）；

均位于 workspace 内。

## 2. ReMeLightMemoryConfig 默认值

| 字段 | 默认 | 说明 |
|---|---|---|
| `summarize_when_compact` | True | 上下文压缩时同步触发 summarizer 写 daily log |
| `auto_memory_interval` | **5** | 每 5 条用户消息触发一次 daily log（None 关闭） |
| `dream_cron` | `0 23 * * *` | 每晚 23:00 把 daily log 提炼到 MEMORY.md |
| `auto_memory_search_config.enabled` | False | 自动检索（默认关；显式调 `memory_search` 工具）|
| `auto_memory_search_config.max_results` | 2 | 检索条数上限 |
| `auto_memory_search_config.min_score` | 0.3 | 相似度阈值 |
| `rebuild_memory_index_on_start` | False | 启动时重建 embedding 索引 |
| `recursive_file_watcher` | False | 是否递归监听 memory/ 子目录 |
| `embedding_model_config` | OpenAI text-embedding-3-small，1024 维 | embedding 模型 |
| `daily_memory_dir` | `memory` | daily log 目录名 |

参考：[commit 5a20e1ec — fix(memory): enable auto_memory_interval by default (None → 5)](../changelog/backend.md)。

## 3. 写入路径

### 3.1 Auto memory（每 N 条用户消息）

`auto_memory_interval=5`：每收到第 5 条用户消息时：

1. 取最近一段对话（pre 压缩的原始 messages）；
2. 调 `summarize(messages)` → ReMe 内部 LLM 生成 markdown 摘要；
3. 追加到 `<workspace>/memory/<today>.md`。

不会阻塞当前回合 — 异步任务。

### 3.2 Compaction-driven（压缩时同写）

`summarize_when_compact=True`：上下文压缩触发时，把"将被替换的历史"喂给 summarizer，写到 daily log。

这样即使一次回合超长压缩，也不会丢失关键事实。

### 3.3 Dream cron（每晚提炼）

`dream_cron = "0 23 * * *"` 默认 23:00 触发 [reme_light_memory_manager.py:526 `dream`](../../src/wowooai/agents/memory/reme_light_memory_manager.py#L526)：

1. 备份当前 `MEMORY.md` 到 `<workspace>/backup/memory_backup_<timestamp>.md`；
2. 起一个临时 `DreamOptimizer` ReActAgent（不打印控制台）；
3. 喂 `DREAM_OPTIMIZATION_ZH/EN` prompt（含 `current_date`）；
4. agent 读最近 daily logs + 现有 MEMORY.md → 输出新的 MEMORY.md；
5. 落盘覆盖原文件。

设计意图：让"白天记事 → 夜里整理"接近人脑的睡眠记忆固化模型。

### 3.4 模型与工具

`DreamOptimizer` 用当前 agent 的 `active_model`（不是单独的小模型），共享 LLM 限流与重试。工具集是 `summary_toolkit` —— 只暴露文件读写（不允许 dream 过程调浏览器、shell）。

## 4. 读取路径

### 4.1 系统提示注入

`PromptBuilder` 在 `AGENTS.md` 末尾追加 memory prompt（详见 [14-prompt-system.md §4.2](14-prompt-system.md)）—— **内容是"如何记 / 如何忘"的元指令**，不是 MEMORY.md 正文。

`MEMORY.md` 正文不默认进 system prompt — 由模型在需要时通过工具读取。

### 4.2 `memory_search` 工具

[reme_light_memory_manager.py:340 `memory_search`](../../src/wowooai/agents/memory/reme_light_memory_manager.py#L340)：

- 输入：自然语言 query；
- 行为：在 MEMORY.md + memory/*.md 内做语义检索（embedding + BM25 混合）；
- 返回：top-K 命中片段。

启动时若 `auto_memory_search_config.enabled=True`，pre_reply 自动跑一次检索把命中拼到 context。**默认 False**，避免每回合 embedding 调用产生额外 token / 延迟。

### 4.3 Tokenize 与 CJK

[reme_light_memory_manager.py:280 `_is_cjk` / `tokenize_query`](../../src/wowooai/agents/memory/reme_light_memory_manager.py#L280)：中文 query 不走空格分词，按字 + bigram；英文走标准 tokenizer。

## 5. Proactive Memory（主动记忆 / 任务驱动唤醒）

[memory/proactive/](../../src/wowooai/agents/memory/proactive/)

让数字员工根据"记忆中的待办"在合适时机**主动向用户发消息**（不等用户提问）：

| 模块 | 用途 |
|---|---|
| `proactive_trigger.py` | 后台 loop，判定"该不该说话" |
| `proactive_responder.py` | 命中触发条件后生成 + 发送消息 |
| `proactive_prompts.py` | 主动消息生成模板 |
| `proactive_types.py` | `ProactiveTask` 数据结构 |

### 5.1 启用

通过 `enable_proactive_for_session(workspace, ...)` 显式打开（默认不开）。

### 5.2 触发判定

`_should_trigger_proactive`：
- 检查最近一次用户活跃时间；
- 从 MEMORY.md 抽出 `ProactiveTask`（含截止时间 / 提醒条件）；
- 命中条件 → `_handle_proactive_trigger`。

### 5.3 发送

通过 `send_proactive_message_via_http`（走当前 workspace 的渠道 API），不是直接调 agent.reply。避免主动消息和用户消息并发到同一个 agent。

## 6. AgentMdManager（前端读写）

[agent_md_manager.py](../../src/wowooai/agents/memory/agent_md_manager.py)

| 方法 | 路径 |
|---|---|
| `list_memory_mds()` | 列 `<workspace>/memory/*.md` |
| `read_memory_md(name)` | 读单个 daily log |
| `write_memory_md(name, content)` | 写单个 daily log（用户直接编辑） |
| `list_working_mds()` / `read/write_working_md` | MEMORY.md 也走这里 |

前端 `/agent/workspace` 可视化编辑。

## 7. 备份策略

每次 dream 前自动备份 MEMORY.md 到 `<workspace>/backup/memory_backup_<timestamp>.md`。
不做自动清理 — 用户机器磁盘充足，保留全历史。

## 8. Embedding 后端

| 字段 | 默认 |
|---|---|
| `embedding_model_config.provider` | `openai` |
| `embedding_model_config.model` | `text-embedding-3-small` |
| `embedding_model_config.dimensions` | 1024 |

embedding 调用走与 chat 同一套 provider 凭据（`providers.json`）。无凭据 → memory_search 退化为纯关键词。

`MEMORY_STORE_BACKEND` 环境变量可切换底层（auto / sqlite / fs），默认 auto。

## 9. 失败与降级

- LLM 失败 → daily log 跳过本轮（不阻断对话）；
- Dream 失败 → 警告，下次 cron 重试；不破坏 MEMORY.md（有备份）；
- Embedding 端点不可达 → `memory_search` 退化为关键词检索。

## 10. 凭据隐私（绝对约束）

- MEMORY.md / memory/*.md 是**用户私有**内容，仅存 workspace 内。
- 严禁把任何用户机器上的 MEMORY 内容写入仓库的模板（`md_files/zh/MEMORY.md` / `md_files/en/MEMORY.md`）。
- 模板里只能放"骨架与示例"，不允许包含真实账号 / SSH 主机 / 内部 URL。

## 11. 0.0.1 不做

- 不做跨数字员工共享记忆（每个 agent 工作区独立）。
- 不做记忆图谱 / 知识图谱（仅平铺 markdown + embedding）。
- 不做服务端记忆（不上云、不跨设备同步）。
- 不做记忆质量打分 / 重要度排序（dream 由 LLM 自行判定）。
- 不做老 daily log 自动归档 / 删除（用户决定何时清）。

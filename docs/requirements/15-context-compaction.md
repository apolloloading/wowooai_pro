# 15 — 上下文压缩与工具结果裁剪

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/context/light_context_manager.py](../../src/wowooai/agents/context/light_context_manager.py) · [src/wowooai/agents/context/compactor_prompts.py](../../src/wowooai/agents/context/compactor_prompts.py)

## 1. 两种"瘦身"机制

| 机制 | 触发 | 对象 | 何时丢失 |
|---|---|---|---|
| **工具结果裁剪（pruning）** | 每次 pre_reply | 历史消息里的 `ToolResultBlock` | 不丢失（原文落盘到 `tool_results/`） |
| **上下文压缩（compaction）** | token 超过阈值 | 整段历史 | 原始消息替换为摘要（保留摘要 + 最近 N 条） |

裁剪是"廉价、随时跑"；压缩是"昂贵、调 LLM、有损"。先裁剪、不够再压缩。

## 2. 工具结果裁剪（ToolResultPruningConfig）

### 2.1 默认值

| 字段 | 默认 |
|---|---|
| `enabled` | True |
| `pruning_recent_n` | **4** |
| `pruning_old_msg_max_bytes` | **8000** |
| `pruning_recent_msg_max_bytes` | **50000** |
| `offload_retention_days` | 5 |
| `tool_results_cache` | `tool_results` |
| `exempt_file_extensions` | `[".md"]` |
| `exempt_tool_names` | `["chat_with_agent"]` |

### 2.2 行为

[light_context_manager.py:229 `_prune_tool_result`](../../src/wowooai/agents/context/light_context_manager.py#L229)

每次 `pre_reply` 遍历历史消息：

1. 标记最近 `pruning_recent_n=4` 个 tool_result 为"recent"，其余为"old"；
2. 检测 exempt（tool name 在 `exempt_tool_names`，或 read_file 的扩展名在 `exempt_file_extensions`）；
3. 对每个 tool_result：
   - exempt → 使用 `pruning_recent_msg_max_bytes`（宽松）；
   - recent → 用 `pruning_recent_msg_max_bytes=50000`；
   - old → 用 `pruning_old_msg_max_bytes=8000`；
4. 超限时调 `_truncate_tool_result`：原文写到 `<workspace>/tool_results/<uuid>.txt`，原位置替换为前 N 字节 + `[TRUNCATED, full content at /path/to/file]` notice。

### 2.3 为什么是 8000 / 50000

[changelog/backend.md §38](../changelog/backend.md) 的调整理由：8000 字节中文≈2700 字，足够包含一次工具调用的"上下文骨架"（命令 + 关键输出片段），但不至于让多步工具链把窗口撑爆。50000 给最近的工具调用更宽容，因为模型多半要基于刚刚的结果再做一两轮决策。

### 2.4 落盘清理

`offload_retention_days=5` — 启动时清理 `tool_results/` 中早于 5 天的文件（[light_context_manager.py:87 `_cleanup_expired_tool_result_files`](../../src/wowooai/agents/context/light_context_manager.py#L87)）。

## 3. 上下文压缩（ContextCompactConfig）

### 3.1 默认值

| 字段 | 默认 |
|---|---|
| `enabled` | True |
| `compact_threshold_ratio` | **0.8** |
| `reserve_threshold_ratio` | **0.1** |
| `compact_with_thinking_block` | True |

### 3.2 触发条件

`pre_reply` 时：
1. 估算当前消息总 token（`bytes / 4`）；
2. 阈值 = `max_input_length × compact_threshold_ratio = 128*1024 × 0.8 ≈ 104857`；
3. 超阈值 → 调用 `_compact_context`。

### 3.3 压缩动作

[light_context_manager.py:386 `_compact_context`](../../src/wowooai/agents/context/light_context_manager.py#L386)

1. 把历史消息（除系统提示和最近 reserve 部分）格式化为字符串；
2. 喂给 LLM（同一个 active_model），用 `compactor_prompts.py` 中的 system prompt 要求"输出 markdown 摘要，## 分级"；
3. LLM 返回摘要 → `_is_valid_summary` 校验（非空、含 `##`）；
4. 替换原历史：`[system] + [summary as system] + [recent N kept]`。

### 3.4 reserve_threshold_ratio

保留比例 0.1 = 压缩后留 10% 窗口给当前回合，避免"压完立刻又超"。

### 3.5 失败兜底

[light_context_manager.py:555 `_compact_context_safe`](../../src/wowooai/agents/context/light_context_manager.py#L555) 兜底：

- LLM 调用失败 / 摘要非法 → 不替换，仅记录警告；
- 当前回合按未压缩状态继续，下次 pre_reply 重试；
- 极端情况下窗口被撑爆 → 由 provider 端 4xx 触发上层 LLM retry。

## 4. 压缩与 thinking block

`compact_with_thinking_block=True` 默认把 thinking 内容也喂给 compactor（思考链中常含关键事实）。性能敏感时可关。

## 5. dialog 归档

`light_context_config.dialog_path` 指向 `<workspace>/dialog/*.jsonl`：

- `post_reply` 每次把当前回合落盘；
- 与压缩独立——压缩抹掉的是"工作内存"，dialog 保留完整原始流；
- 用于会话回放、调试、记忆 summarizer。

## 6. 状态机简图

```
pre_reply ───┬─► prune tool_results (always)
             │
             ├─► estimate tokens
             │
             ├─ tokens > 0.8 × max_input_length?
             │     │
             │     yes ─► _compact_context
             │     │        │
             │     │        ├─ success: replace history with summary
             │     │        └─ fail:    keep original, warn
             │     │
             │     no  ─► no-op
             │
             └─► proceed to reasoning

post_reply ──► flush dialog jsonl ─► trigger memory summarizer (异步)
```

## 7. 与记忆的边界

- 压缩 = **本回合内**的工作内存瘦身（agent 还"记得"，只是换成摘要）；
- 记忆 = **跨回合 / 跨日**的长期沉淀（写到 `MEMORY.md` / `memory/*.md`）；

两者独立但协作：summarizer 接受的输入正是压缩前的原始 dialog（不是被压缩后的摘要）。详见 [16-memory.md](16-memory.md)。

## 8. 0.0.1 不做

- 不做按 token 实际计数（用 `bytes / 4` 估算，简单可靠）。
- 不做多语言专属 token 计数（中文 / 日文 / 韩文都按 bytes 估）。
- 不做压缩内容的二次压缩（一次回合内最多压一次）。
- 不做按 message 重要度打分的差异化保留（recent N 一刀切）。

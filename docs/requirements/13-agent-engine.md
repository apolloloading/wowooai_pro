# 13 — Agent 引擎（ReAct 运行时）

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/react_agent.py](../../src/wowooai/agents/react_agent.py) · [agentscope](https://github.com/modelscope/agentscope) 1.0.19.post1

## 1. 定位

`wowooaiAgent`（继承 agentscope `ReActAgent`）是数字员工的运行时核心。一次"对话回合"指：用户发一条消息 → agent 跑若干轮 reasoning + acting → 最终输出文本回复。

## 2. 单回合主流程

```
reply(user_msg)
  └─ pre_reply hook   ← context_manager.pre_reply
       └─ 加载历史消息、压缩判定、注入工具结果
  └─ for i in range(max_iters):
       ├─ _reasoning()          ← 调 LLM，得到下一步 (tool calls or text)
       ├─ if has tool_calls:
       │    └─ _acting(tool_call)  ← 串行执行工具，注入 result
       │    continue
       └─ if text only:
            └─ _auto_continue_if_text_only()
                 └─ if 应继续: 注入 system hint, continue
                 └─ else:      break
  └─ post_reply hook  ← context_manager.post_reply
       └─ flush 对话归档、触发记忆/压缩
```

## 3. 关键参数（AgentsRunningConfig）

| 字段 | 默认 | 含义 |
|---|---|---|
| `max_iters` | **100** | 单回合 reasoning + acting 上限；触顶强制收尾 |
| `auto_continue_on_text_only` | **True** | 模型只返回文本时再追加一轮（避免提前停） |
| `max_input_length` | **128 × 1024** | 上下文窗口（字节，估 token 用 ÷4） |
| `shell_command_timeout` | **60** 秒 | shell 工具默认超时 |

## 4. Auto-continue（文本-only 自动续跑）

[react_agent.py:798 `_auto_continue_if_text_only`](../../src/wowooai/agents/react_agent.py#L798)

模型仅输出 TextBlock（无 tool_call）时：

1. 取消 plan 模式下的 hint（`should_skip_auto_continue`）；
2. 取最近一条 assistant message 的尾部（`_auto_continue_tail_context`，截取若干字符）；
3. 注入系统 hint（[react_agent.py:766](../../src/wowooai/agents/react_agent.py#L766)）："如果任务未完成，继续；如果完成，回复一句简短文本（不调工具）"；
4. 再跑一轮 `_reasoning`。

设计意图：让模型在"边思考边汇报"的中文对话里不会卡住。用户嫌啰嗦可关：`auto_continue_on_text_only=False`。

## 5. LLM 限流 / 重试

| 字段 | 默认 | 行为 |
|---|---|---|
| `llm_retry_enabled` | True | 瞬态错误（5xx / 网络）自动重试 |
| `llm_max_retries` | 3 | 最大重试次数 |
| `llm_backoff_base` / `llm_backoff_cap` | 1.0 / 30.0 | 指数退避（min(base × 2^n, cap)） |
| `llm_max_concurrent` | 10 | 全局并发上限（跨 agent 共享） |
| `llm_max_qpm` | 0 | 60 秒滑窗 QPM 限速；0 = 关 |
| `llm_rate_limit_pause` / `_jitter` | 60 / 5 | 收到 429 后全局暂停 60±5 秒 |
| `llm_acquire_timeout` | 600 | 等待限流槽超时 |

并发与限流参数**仅在第一次初始化时生效**——多 agent 启动后修改不会重新打开槽位。

## 6. 中断与恢复

### 6.1 软中断

`wowooaiAgent.interrupt()`（[react_agent.py:1344](../../src/wowooai/agents/react_agent.py#L1344)）：

1. 取消 `_reply_task`（若仍在跑）；
2. 等待清理完毕（最多 5 秒）；
3. post_reply hook 仍会跑（保证对话归档落盘）。

UI "停止生成" 按钮走这条路径。

### 6.2 硬中断

进程退出（关窗 / SIGTERM）：launcher 给 5 秒收尾，否则 SIGKILL。当前回合的 LLM 流式响应丢弃；已落盘的工具调用结果保留。

### 6.3 不做：跨进程续跑

0.0.1 不做"重启后续跑当前回合"。重启后从最后一条已落盘的消息继续新回合即可。

## 7. 钩子（hooks）

注册于 [react_agent.py:440-457](../../src/wowooai/agents/react_agent.py#L440-L457)：

| 类型 | 名称 | 来源 |
|---|---|---|
| `pre_reply` | `context_pre_reply` | `context_manager.pre_reply` |
| `post_reply` | `context_post_reply` | `context_manager.post_reply` |

agentscope 标准接口，不允许多链多次注册同名钩子。

## 8. 模型调用栈

```
ReAct._reasoning
  └─ self.model.chat(messages, tools=...)
       └─ RoutingChatModel       ← agents/routing_chat_model.py
            └─ ProviderClient    ← providers/<name>_provider.py
                 ├─ retry / backoff
                 ├─ qpm / concurrent gate
                 └─ HTTP / SDK 调用
```

`RoutingChatModel` 按 `agent.json > llm_routing` 在 local / cloud 两槽间选；未启用时直接用 `active_model`。

## 9. 工具调用边界

- `_acting` 串行执行（不并发跑工具）。
- 单工具默认无超时（除 shell 有 `shell_command_timeout=60`）。
- 工具异常 → 注入 `ToolResultBlock(error=...)`，agent 看见后自行决定是否重试。
- 审批级别拦截发生在 `_acting` 入口（详见 [06-security.md](06-security.md)）。

## 10. 命令路由

[react_agent.py:1290 `reply`](../../src/wowooai/agents/react_agent.py#L1290) 在进入 ReAct 循环前先：

1. 处理 file blocks（图片 / 文件落地到 sandbox）；
2. 走 `command_handler` 检查是否是斜杠命令（`/mission` / `/plan` 等），命中则不进 ReAct，转专用 handler；
3. 否则进 `super().reply(...)` 走标准 ReAct。

## 11. 0.0.1 不做

- 不做并行 tool calling（一次回合内多个 tool 仍串行）。
- 不做"工具搜索 / 动态加载"（toolkit 启动时全量注册）。
- 不做跨进程恢复中断的回合。
- 不做模型级 fallback 链（用户在路由层手动切）。

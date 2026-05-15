# 19 — 子代理 / 跨代理协作

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/tools/agent_management.py](../../src/wowooai/agents/tools/agent_management.py) · [src/wowooai/agents/tools/delegate_external_agent.py](../../src/wowooai/agents/tools/delegate_external_agent.py)

## 1. 三种委派路径

| 路径 | 工具 | 跨进程？ | 协议 |
|---|---|---|---|
| **同实例跨 agent**（前台） | `chat_with_agent` | 否（同一 wowooai 后端进程内） | HTTP 内部调用 |
| **同实例跨 agent**（后台） | `submit_to_agent` | 否 | HTTP 内部调用 + task handle |
| **外部 agent runner** | `delegate_external_agent` | 是 | ACP（详见 [09 §2](09-mcp-acp.md)） |

## 2. chat_with_agent（前台）

[agent_management.py:426](../../src/wowooai/agents/tools/agent_management.py#L426)

### 2.1 签名

```python
chat_with_agent(
    to_agent: str,           # 目标 agent ID（来自 list_agents）
    text: str,               # 消息文本
    session_id: str | None,  # 可选；不传则新建
    timeout: int = 300,      # 等待目标完成的秒数
) -> ToolResponse
```

### 2.2 行为

1. 校验 `to_agent` 存在；
2. 拿调用方当前 `session_id` / `root_session_id`（从 [app/agent_context.py](../../src/wowooai/app/agent_context.py)）；
3. 把这两个写入新请求 payload，让目标 agent 共享审批上下文；
4. 通过 internal HTTP 调目标 agent，**阻塞等待**最终文本回复；
5. 返回 `[SESSION: <sid>]` 头 + 回复文本，调用方可复用 session 继续。

### 2.3 不被裁剪

`chat_with_agent` 在 `ToolResultPruningConfig.exempt_tool_names` 里（[15 §2.1](15-context-compaction.md)）—— 跨 agent 回复通常关键，不被 8000 字节裁剪。

### 2.4 审批继承

调用方的 `root_session_id` 会传给被调方。如果被调方也触发审批，UI 把审批关联到**调用方的根会话**，避免审批弹窗"飘到别处"。

## 3. submit_to_agent（后台）

[agent_management.py:516+](../../src/wowooai/agents/tools/agent_management.py#L516)

- 立即返回 task metadata（不等结果）；
- 适合"派发后做别的事，回头再问"的场景；
- 任务进度通过 task_tracker 暴露（[18-streaming.md §4](18-streaming.md)）。

## 4. delegate_external_agent（ACP）

详见 [09-mcp-acp.md §2](09-mcp-acp.md)。

要点：
- **跨进程**：通过 stdio 启动一个外部 agent runner（`opencode` / `qwen` / `claude-agent-acp` / `codex-acp`）；
- **协议**：ACP（Agent Communication Protocol）；
- **默认禁用**：`delegate_external_agent.enabled = False`，需用户在 UI 显式开启；
- 工具调用解析模式：`call_title` / `call_detail` / `update_detail`。

## 5. session 与上下文边界

```
caller_agent (root_session_id=R)
  ├─ chat_with_agent(to=B)
  │     └─ B 收到 root_session_id=R，session_id=新生成或传入
  │     └─ B 内部可继续 chat_with_agent(to=C, root_session_id=R)
  │     └─ 嵌套调用栈共享同一 root_session_id（用于审批关联）
  │
  └─ delegate_external_agent(runner=claude_code)
        └─ 子进程 runner，session 与本进程 session 解耦
        └─ 审批不跨进程继承
```

`agent_context.py` 用 contextvars 维护 caller 信息，确保嵌套调用时 `get_current_session_id()` 拿到正确值。

## 6. 工具消息过滤（per-agent）

每个 agent 的 ChannelConfig 有 `filter_tool_messages` / `filter_thinking`，影响**渠道侧**显示，**不影响** `chat_with_agent` 跨调用接收 — 后者拿到的是最终文本。

## 7. 跨 agent 调用的"无限递归"防护

0.0.1 不做硬限制。约束靠：

- 目标 agent 的 `max_iters=100`（[13 §3](13-agent-engine.md)）—— 不能无限跑；
- `chat_with_agent.timeout=300` —— 超时即返回错误；
- 全局 LLM 限流（`llm_max_concurrent=10`）—— 自然背压。

如未来发现循环调用问题，再加显式深度限制。

## 8. CLI 等价物

```bash
wowooai chats send --agent-id <to> --text "..."   # 类似 chat_with_agent
wowooai chats list --agent-id <id>
```

入口：[cli/chats_cmd.py](../../src/wowooai/cli/chats_cmd.py)。

## 9. 凭据隐私

- `chat_with_agent` 在同一后端进程内调用，凭据共享（同一 `providers.json`）；
- `delegate_external_agent` 调外部 CLI，环境变量通过 `acp.<agent>.env` 传递，**严禁**写入仓库默认值；
- 跨调用消息内容可能含敏感信息（任务派发上下文）—— 不上报、仅落本地 dialog/log。

## 10. 0.0.1 不做

- 不做 agent 能力发现 / 路由（调用方必须知道 `to_agent` ID）。
- 不做跨调用的工具结果回放（B 调用的工具结果不会自动回灌给 A）。
- 不做"agent 池"或"agent teams"概念（无 team / role 抽象）。
- 不做调用图可视化（仅 dialog log）。

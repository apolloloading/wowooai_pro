# 22 — Runner 与任务派发

> 版本：0.0.1
> 对应代码：[src/wowooai/app/runner/](../../src/wowooai/app/runner/) · `TaskTracker` · `ChatManager` · `AgentRunner`

## 1. 职责划分

| 组件 | 职责 |
|---|---|
| `AgentRunner`（[runner.py](../../src/wowooai/app/runner/runner.py)） | 单 agent 实例的查询处理器（绑 agent + toolkit + chat_manager + mcp_manager） |
| `TaskTracker`（[task_tracker.py](../../src/wowooai/app/runner/task_tracker.py)） | 进程内活跃任务表 + 订阅 fan-out |
| `ChatManager`（[manager.py](../../src/wowooai/app/runner/manager.py)） | Chat 元数据 CRUD（session_id ↔ chat_id ↔ sender） |
| `command_dispatch`（[command_dispatch.py](../../src/wowooai/app/runner/command_dispatch.py)） | 区分用户消息 vs 命令（`/mission` / `/plan` / `/approval`） |
| `mission_dispatch`（[mission_dispatch.py](../../src/wowooai/app/runner/mission_dispatch.py)） | Mission 命令的专用入口 |
| `daemon_commands`（[daemon_commands.py](../../src/wowooai/app/runner/daemon_commands.py)） | 守护进程级控制（restart / shutdown 协调） |
| `query_error_dump`（[query_error_dump.py](../../src/wowooai/app/runner/query_error_dump.py)） | 把异常 query 落盘，便于排查 |

## 2. TaskTracker

### 2.1 数据结构

```python
@dataclass
class _RunState:
    queue: asyncio.Queue       # 流式事件队列
    subscribers: list[Queue]   # 订阅者列表（fan-out 用）
    task: asyncio.Task | None  # 生产者协程
    status: "starting" | "running" | "done" | "error" | "stopped"
```

每个活跃任务以 `run_key`（通常是 `chat_id`）为键。

### 2.2 关键方法

| 方法 | 用途 |
|---|---|
| `attach_or_start(run_key, payload, runner_fn)` | 已有任务 → 附加订阅；没有 → 启动新任务 |
| `attach(run_key)` | 仅附加（找不到返回 None，用于 reconnect 场景） |
| `request_stop(run_key)` | 软停止当前任务（触发 agent.interrupt） |
| `register_external_task(run_key)` / `unregister_external_task(run_key)` | 外部任务（cron / heartbeat / proactive）登记，参与 `has_active_tasks` 判断 |
| `has_active_tasks()` | 进程是否还有任务在跑（关停前要等） |
| `wait_all_done(timeout=300)` | 等所有任务结束（shutdown 时调） |
| `list_active_tasks()` | 列当前活跃任务（CLI / debug 用） |
| `stream_from_queue(queue, run_key)` | 把 queue 转 SSE 帧；客户端断开时调 `detach_subscriber` 清理 |

### 2.3 一对多订阅

同一 `run_key` 多个客户端订阅时：

- 生产者只跑一次；
- 事件 fan-out 到每个 subscriber 的 queue；
- 客户端 detach 不会停生产者；
- 全部 detach 后生产者仍跑到自然结束（任务后台续跑）。

## 3. AgentRunner

[runner.py:107 `AgentRunner`](../../src/wowooai/app/runner/runner.py#L107)

继承 agentscope `Runner`，负责把一次 `query` 转成 agent 调用 + 流式输出 + plan 事件 + chat 元数据更新。

### 3.1 核心入口

```python
AgentRunner.query_handler(query, ...) -> AsyncGenerator
```

[runner.py:286](../../src/wowooai/app/runner/runner.py#L286) 流程（节选）：

1. `command_dispatch.run_command_path` 判定是否是 `/...` 命令；
2. `_parse_skill_query` / `_maybe_inject_skill` —— 如果用户用了 `#skill` 引用，自动把技能内容拼到提示；
3. `_rewrite_last_message_text` —— 部分场景重写最后一条 user message（如把 `@agent` 解析成内部引用）；
4. 调 `agent.reply(...)`；
5. 把流转成事件 push 到 queue；
6. 注册 `_on_plan_change` 钩子（plan 变化 → SSE 广播）；
7. 异常 → `query_error_dump` 落盘 + push `type=error` 事件。

### 3.2 init / shutdown

- `init_handler` 启动时调（一次性初始化）；
- `shutdown_handler` 后端 graceful shutdown 时调，等待当前回合结束。

## 4. ChatManager

[manager.py:17 `ChatManager`](../../src/wowooai/app/runner/manager.py#L17)

Chat 元数据存于 `<workspace>/chats.json`（或 sqlite）：

| 方法 | 用途 |
|---|---|
| `list_chats(...)` | 分页列出，可按 channel / session 过滤 |
| `get_or_create_chat(session_id, sender_id, channel_id, name)` | 入口最常用 |
| `create_chat(spec)` | 显式新建 |
| `patch_chat(...)` | 改 name / 元数据 |
| `touch_chat(chat_id)` | 更新 `last_active_at` |
| `delete_chats([id, ...])` | 批量删 |
| `count_chats(...)` | 计数（统计页用） |
| `get_chat_id_by_session(...)` | session → chat 反查 |

详细 chat 数据结构见 [routers/messages.py](../../src/wowooai/app/routers/messages.py)。

## 5. 命令派发

[command_dispatch.py](../../src/wowooai/app/runner/command_dispatch.py)

`_is_command(query)` 判定是否以斜杠开头：

| 类型 | 例子 | 入口 |
|---|---|---|
| Conversation command | `/clear` `/rename` `/new` | runner 内部处理 |
| Control command | `/approval approve <id>` `/mission status` | 路由到对应 handler |
| Mission command | `/mission ...` | `mission_dispatch` |

非命令 → 进 ReAct 标准循环。

## 6. Daemon Commands

[daemon_commands.py](../../src/wowooai/app/runner/daemon_commands.py)

后端进程级控制（不依赖 agent）：

| 异常 | 用途 |
|---|---|
| `RestartInProgressError` | 当前正在重启，拒绝新请求 |

`DaemonContext` 协调：

- 重启请求 → 等当前活跃任务结束（最多 timeout） → 走 launcher 重启路径；
- shutdown → `wait_all_done` → 关闭 channels / cron → exit。

CLI 入口：`wowooai daemon ...`（[cli/daemon_cmd.py](../../src/wowooai/cli/daemon_cmd.py)）。

## 7. 与 SSE 的协作

详见 [18-streaming.md §4](18-streaming.md)。简要：

- TaskTracker 是 SSE 的 ground truth（订阅、心跳、reconnect）；
- AgentRunner 是事件生产者；
- 路由层（`routers/console.py`）把两者粘起来。

## 8. 与外部任务的协作

cron / heartbeat / proactive memory 是"非 chat 触发"的 agent 调用：

1. 触发器调 `tracker.register_external_task(run_key)`；
2. 走 `agent.reply(...)` 跑完；
3. `unregister_external_task(run_key)`；

期间 `has_active_tasks()` 返回 True，shutdown 会等它。

## 9. 凭据隐私

- `query_error_dump` 落盘时**严禁**把完整 LLM API key 写入 — 已做 mask。
- chat 元数据可能含用户名 / 渠道 ID — 仅本地存储。

## 10. 0.0.1 不做

- 不做分布式 runner（多机集群）。
- 不做任务优先级 / 队列调度（先到先服务）。
- 不做任务持久化（重启后内存中的活跃任务全丢）。
- 不做任务回溯重播（仅 dialog log 可读，不能回放）。

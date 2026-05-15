# 18 — 流式传输（SSE / 消息块）

> 版本：0.0.1
> 对应代码：[src/wowooai/app/routers/console.py](../../src/wowooai/app/routers/console.py) · [src/wowooai/app/console_push_store.py](../../src/wowooai/app/console_push_store.py) · `task_tracker`

## 1. 协议

后端 → 前端的实时通信全部走 **Server-Sent Events (SSE)**，`Content-Type: text/event-stream`。

| 维度 | 取值 |
|---|---|
| 协议 | HTTP/1.1 + SSE |
| 编码 | UTF-8 |
| 帧格式 | `data: <json>\n\n` |
| 心跳 | 由 `task_tracker` 控制（约每 15-30 秒一个 keep-alive） |
| 鉴权 | 与普通 API 一致（详见 [06-security.md §9](06-security.md)） |

不使用 WebSocket — 单向推流足够，SSE 在 pywebview / 浏览器 / Docker 反代下兼容性最好。

## 2. 主推流端点

| 路径 | 用途 |
|---|---|
| `POST /api/console/chat` | 聊天主流（SSE） |
| `POST /api/console/chat/stop` | 停止流（中断当前回合） |
| `GET /api/plan/stream` | 计划模式 SSE 推流 |
| `GET /api/backup/stream` | 备份/恢复进度 SSE |
| `GET /api/skills/stream` | 技能安装进度 SSE |

请求体重连：`{"reconnect": true}` 把新连接挂到同一 chat 的运行中流，避免任务从头来。

## 3. 消息块类型

agent 输出由若干 **block** 组成，前端按块渲染：

| Block | 来源 | 前端渲染 |
|---|---|---|
| `TextBlock` | LLM 文本输出 | Markdown 文本 |
| `ThinkingBlock` | LLM thinking 输出（claude / o-series） | 可折叠的思考块 |
| `ImageBlock` | 工具输出 / 用户上传 | 图片缩略图 + 点开预览 |
| `FileBlock` | `send_file_to_user` 工具 | 文件卡片（下载） |
| `ToolUseBlock` | agent 决定调工具 | 折叠卡：工具名 + 参数 |
| `ToolResultBlock` | 工具执行结果 | 折叠卡：结果（受 [15 §2](15-context-compaction.md) 裁剪） |

详见 [07-frontend.md §3.2](07-frontend.md)。

## 4. 任务跟踪器（task_tracker）

每个 workspace 持有 `task_tracker`（[app/runner/task_tracker.py](../../src/wowooai/app/runner/task_tracker.py)）：

| 方法 | 用途 |
|---|---|
| `attach_or_start(chat_id, payload, runner)` | 新对话或附加到运行中任务 |
| `attach(chat_id)` | 仅附加（重连场景；找不到返回 None） |
| `stream_from_queue(queue, chat_id)` | 把 queue 中的事件转 SSE 帧 |
| `detach_subscriber(...)` | 客户端断开时清理订阅 |

### 4.1 一对多订阅

同一 chat 可以有多个 SSE 连接（如桌面 + 浏览器 + 调试）。task_tracker 维护订阅列表，事件 fan-out 给全部订阅者。

### 4.2 后台续跑

客户端断开 ≠ 任务取消。`attach_or_start` 让 agent 在后台继续跑；用户重连 `reconnect=true` 立即拿到剩余流。
显式取消通过 `POST /api/console/chat/stop`。

## 5. Console push store

[app/console_push_store.py](../../src/wowooai/app/console_push_store.py)

让**非 chat 路径产生的消息**（心跳、proactive memory、cron 触发的 agent 任务）能推到 console 前端：

| 方法 | 用途 |
|---|---|
| `append(session_id, text, sticky=False)` | 入队一条消息 |
| `take(session_id)` | 取并清空（chat 接入时拉取） |
| `take_all()` | 全 session 拉取 |
| `get_recent(...)` | 最近 N 条（含 TTL 清理） |

`sticky=True` 的消息**不被取出后立刻丢弃**，重连时仍能看到（如"心跳跳过：不在活跃时段"）。

## 6. SSE 事件分类

事件 `data: {...}` 中的字段（节选，具体以代码为准）：

| 字段 | 用途 |
|---|---|
| `type` | `message` / `tool_use` / `tool_result` / `thinking` / `done` / `error` |
| `block` | 完整 block 内容 |
| `delta` | 流式增量（token-by-token） |
| `chat_id` | 当前会话 ID |
| `ts` | 时间戳 |
| `meta` | 渠道 / 工具调用元信息 |

前端按 `type` 分发到 store；同一 block 的多个 delta 拼成最终内容。

## 7. 与 SSE 心跳的关系

| 概念 | 用途 |
|---|---|
| **SSE 心跳** | 防止反向代理（nginx / cloudflare）超时断连，约每 15-30 秒发空帧 |
| **agent 心跳**（HeartbeatConfig） | 让数字员工每 N 分钟主动跑一次 `HEARTBEAT.md`（详见 [08 §2](08-cron-heartbeat.md)） |

两者无关。SSE 心跳由 task_tracker 自动维护，用户不可配；agent 心跳由用户在 UI 显式开关。

## 8. 错误处理

| 错误 | 行为 |
|---|---|
| LLM 失败（限流 / 网络） | 走 [13 §5](13-agent-engine.md) 重试逻辑；最终失败发 `type=error` 帧 |
| 工具执行异常 | 写 `ToolResultBlock(error=...)`；流不中断，agent 继续决策 |
| 客户端断开 | 任务后台续跑；订阅清理 |
| 中断 (`/chat/stop`) | post_reply hook 仍跑（保证 dialog 落盘） |
| 流内部异常 | 发 `data: {"error": "..."}` 后关闭 |

## 9. 0.0.1 不做

- 不做 WebSocket（仅 SSE）。
- 不做服务端推送过滤 / 订阅条件（一律全推）。
- 不做断点续传级别的精确恢复（重连后从订阅时刻开始拉，已发送的 delta 不补）。
- 不做流压缩（gzip / brotli）。

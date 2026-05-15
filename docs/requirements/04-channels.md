# 04 — 外部渠道（Channels）

> 版本：0.0.1
> 对应代码：[src/wowooai/app/channels/](../../src/wowooai/app/channels/) · [src/wowooai/config/config.py](../../src/wowooai/config/config.py)（`ChannelConfig`）

## 1. 渠道清单（14 个 + 控制台 + 语音两套）

| 渠道 | Config 类 | 默认开关 | 说明 |
|---|---|---|---|
| `console` | `ConsoleConfig` | `enabled=True` | 桌面客户端 / Web 控制台聊天，stdout 渲染 |
| `imessage` | `IMessageChannelConfig` | False | 仅 macOS：从 `~/Library/Messages/chat.db` 拉消息 |
| `discord` | `DiscordConfig` | False | bot_token + http_proxy |
| `dingtalk` | `DingTalkConfig` | False | client_id / client_secret / robot_code |
| `feishu` | `FeishuConfig` | False | app_id / app_secret，`domain ∈ {feishu, lark}` |
| `qq` | `QQConfig` | False | app_id / client_secret |
| `onebot` | `OneBotConfig` | False | OneBot v11 反向 WS（NapCat / go-cqhttp / Lagrange） |
| `telegram` | `TelegramConfig` | False | bot_token + 可选 http_proxy |
| `mqtt` | `MQTTConfig` | False | 通用 MQTT 接入 |
| `mattermost` | `MattermostConfig` | False | url + bot_token，WebSocket polling |
| `matrix` | `MatrixConfig` | False | homeserver + access_token，可选 E2E 加密 |
| `voice` | `VoiceChannelConfig` | False | Twilio ConversationRelay + Cloudflare Tunnel |
| `sip` | `SIPChannelConfig` | False | dual-track（pyVoIP dev / LiveKit prod） |
| `wecom` | `WecomConfig` | False | 企业微信 AI Bot |
| `weixin` | `WeixinConfig` | False | iLink Bot 个人微信号 |
| `xiaoyi` | `XiaoYiConfig` | False | 华为 A2A 协议 WebSocket |

`ChannelConfig` 用 `model_config = ConfigDict(extra="allow")`，允许插件渠道动态注入。

## 2. 通用配置字段（BaseChannelConfig）

| 字段 | 默认 | 用途 |
|---|---|---|
| `enabled` | False | 渠道开关 |
| `bot_prefix` | "" | 命令前缀（如 `/wowooai`） |
| `filter_tool_messages` | False | 是否过滤工具调用消息 |
| `filter_thinking` | False | 是否过滤 thinking 块 |
| `dm_policy` | `open` | `open` / `allowlist` 私聊策略 |
| `group_policy` | `open` | 群聊策略 |
| `allow_from` | `[]` | 允许列表（user_id / group_id） |
| `deny_message` | "" | 拒绝时的回复 |
| `require_mention` | False | 群聊是否必须 @ 才响应 |

## 3. 配置存储

- 当前数字员工的渠道配置存在 `<workspace>/agent.json > channels`。
- 兼容性：`config.json > channels` 仍存在（迁移期保留），但优先读 agent 级别。

## 4. 渠道生命周期

| 阶段 | 行为 |
|---|---|
| 启动 | `MultiAgentManager.start_workspace` 时按 `channels.<name>.enabled` 启动对应渠道 |
| 接收 | 渠道 → `unified_queue_manager` → `runner.run` |
| 回复 | runner 输出 → renderer → 渠道发送 |
| 心跳 | `HeartbeatConfig` 周期任务可向指定渠道发起请求 |
| 关闭 | workspace 停止时反向关闭 |

## 5. 媒体目录（media_dir）

多数渠道支持 `media_dir`：从渠道下载的图片 / 文件落到该目录；不配置则用默认 workspace 路径。`max_decoded_size`（iMessage）默认 10MB，限制 Base64 解码体积。

## 6. 隐私 / 凭据

- 所有 token / secret / key 只存在 `agent.json`（用户机器）。
- 后端不主动上报、不上传、不集中存储。
- 严禁把任何渠道凭据写进仓库或 SKILL.md（详见 [06-security.md](06-security.md)）。

## 7. 渠道适配器约束

- 适配器必须实现：`start()` / `stop()` / `send_text()` / `send_file()` / `on_event()`。
- 必须把消息标准化为内部 schema：`channel`, `user_id`, `session_id`, `message_blocks`。
- 工具调用结果 / thinking 块根据 `filter_*` 配置在出口处剔除。

## 8. 控制台（console）特殊性

- 始终 `enabled=True`，无法关闭（前端聊天页依赖）。
- 不需要外部 token / secret。
- 是 `cron` 默认 `--channel` 取值。

## 9. 渠道注册路径

- [src/wowooai/app/channels/registry.py](../../src/wowooai/app/channels/registry.py) — channel name → adapter class
- [src/wowooai/app/channels/manager.py](../../src/wowooai/app/channels/manager.py) — 生命周期管理
- 新增渠道适配器需在 `registry` 与 `ChannelConfig` 同步登记

## 10. 0.0.1 不做

- 未在内置列表的 SaaS 平台（如 Slack workspace、Microsoft Teams 等）需要用户自行编写适配器 + plugin。
- 不内置渠道间消息桥接 / 转发逻辑（这是 plugin / 用户脚本的职责）。

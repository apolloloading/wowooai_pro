# 08 — 定时任务与心跳

> 版本：0.0.1
> 对应代码：[src/wowooai/app/crons/](../../src/wowooai/app/crons/) · `HeartbeatConfig` · [src/wowooai/cli/cron_cmd.py](../../src/wowooai/cli/cron_cmd.py)

## 1. Cron 系统

### 1.1 存储

每个数字员工的定时任务存在：

```
<workspace>/jobs.json
```

字段：`jobs: List[JobSpec]`，每条任务包含 `id` / `name` / `cron` / `type` / `text` / `target` / `runtime`。

### 1.2 JobSpec 类型

| `type` | 行为 |
|---|---|
| `text` | 到时直接把 `text` 字段发到目标 channel，不经过 agent，不调工具 |
| `agent` | 到时把 `text` 包装成用户消息发给 agent，agent 完整执行（调工具、调浏览器、回复） |

### 1.3 JobRuntimeSpec 默认

| 字段 | 默认 | 说明 |
|---|---|---|
| `max_concurrency` | 1 | 同一 job 不并发 |
| `timeout_seconds` | **1200** | 单次执行超时（避免长任务被默认 120s 中断） |
| `misfire_grace_seconds` | 60 | 错过触发后多久内仍可补跑 |

`timeout_seconds` 默认值在三处必须保持一致：
- [src/wowooai/app/crons/models.py](../../src/wowooai/app/crons/models.py)（后端 model）
- [src/wowooai/cli/cron_cmd.py](../../src/wowooai/cli/cron_cmd.py)（CLI 创建路径）
- [console/src/pages/Control/CronJobs/components/constants.ts](../../console/src/pages/Control/CronJobs/components/constants.ts)（前端默认值）

### 1.4 触发目标

每个 job 必须显式指定：

| 字段 | 说明 |
|---|---|
| `channel` | 默认 `console` |
| `target_user` | 默认 `default` |
| `target_session` | 默认当前 session ID |
| `agent_id` | 必填（CLI 强制） |

### 1.5 CLI 接口

```bash
wowooai cron list   --agent-id <id>
wowooai cron get    <job_id> --agent-id <id>
wowooai cron state  <job_id> --agent-id <id>
wowooai cron create --agent-id <id> --type {text|agent} --name ... --cron "0 9 * * *" \
                    --channel console --target-user default --target-session <sid> \
                    --text "..."
wowooai cron pause  <job_id> --agent-id <id>
wowooai cron resume <job_id> --agent-id <id>
wowooai cron delete <job_id> --agent-id <id>
wowooai cron run    <job_id> --agent-id <id>
```

CLI 没有 `update`：要修改先 `delete` 再 `create`。

### 1.6 SKILL: cron

[cron-zh / cron-en SKILL.md](../../src/wowooai/agents/skills/cron-zh/SKILL.md) v2.1。强制规则：

- 只在"未来定时执行"或"周期执行"场景才创建 cron；只是"立即执行一次"不要用 cron。
- 所有命令必须显式带 `--agent-id`，否则任务可能错落到 default agent 的 workspace。
- 选 `--type` 时问自己："到达时间后这段文本是被『读出来』，还是需要被『执行』？" 读 → text，执行 → agent。
- agent 类型的 `--text` 必须包含完整上下文（agent 触发时无当前会话记忆）：网址、账户位置、文件路径、输出要求等。

### 1.7 Web UI

`/control/cronjobs` 页面提供完整 CRUD（创建、暂停、恢复、删除、立即执行、查看历史）。

## 2. 心跳（HeartbeatConfig）

### 2.1 用途

让数字员工在指定时段每隔 N 分钟自动跑一次 `HEARTBEAT.md` 内容（如巡检、群消息汇报）。

### 2.2 字段

| 字段 | 默认 | 说明 |
|---|---|---|
| `enabled` | False | 心跳开关 |
| `every` | 系统常量 `HEARTBEAT_DEFAULT_EVERY` | 间隔表达式 |
| `target` | 系统常量 `HEARTBEAT_DEFAULT_TARGET` | 目标渠道 / 用户 |
| `active_hours` | None | 可选活跃时段（如 08:00–22:00） |

### 2.3 ActiveHoursConfig

```json
{ "start": "08:00", "end": "22:00" }
```

不在活跃时段内的心跳跳过执行。

### 2.4 配置位置

- 当前数字员工：`agent.json > heartbeat`
- 兼容性：`config.json > agents.defaults.heartbeat` 仍存在（迁移期）

### 2.5 心跳模板

`<workspace>/HEARTBEAT.md` 是心跳触发时的"用户消息"模板。每次心跳到来时把它作为查询发给 agent。

## 3. 调度器

- 后端调度器基于 APScheduler。
- 启动 workspace 时加载 `jobs.json` 并注册到调度器。
- 调度器与 agent 实例 1:1 绑定（不跨 workspace 共享 job）。
- 桌面包关闭时调度器随主进程退出。

## 4. 异常与可观测

- 每次执行结果（成功 / 失败 / 超时 / cancelled）写入 job state，用 `wowooai cron state <job_id>` 查看。
- 失败不会自动停用任务（除非显式 `pause`）。
- 长任务超过 `timeout_seconds` 触发 `asyncio.TimeoutError`，job state 标记失败。

## 5. 0.0.1 不做

- 不做跨设备 / 跨 agent 的全局调度（每个 workspace 各自独立）。
- 不做任务依赖图 / DAG 编排。
- 不做 retry policy（失败就失败，不自动重跑；用户可用 `cron run` 手动补跑）。

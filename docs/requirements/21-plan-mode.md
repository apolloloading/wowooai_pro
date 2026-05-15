# 21 — 计划模式（Plan Mode）

> 版本：0.0.1
> 对应代码：[src/wowooai/plan/](../../src/wowooai/plan/) · [src/wowooai/app/routers/plan.py](../../src/wowooai/app/routers/plan.py) · agentscope `Plan` / `PlanNotebook`

## 1. 定位

**计划模式**让数字员工在动手前先输出 `Plan`（含 N 个 `SubTask`），用户可在 UI 看到任务分解和执行状态，必要时干预。

与 [Mission（17）](17-mission-orchestration.md) 的区别：

| 维度 | Plan Mode | Mission |
|---|---|---|
| 触发 | 自然对话中按需触发 | 显式 `/mission <task>` |
| 产出 | `Plan` (subtasks，状态机) | `prd.json` (userStories，可验证) |
| 阶段 | 单阶段 | Phase 1 / Phase 2 |
| 适用 | 普通对话中"想清楚再做" | 长流程、可验证、需多轮迭代 |

两者可以共存（Mission Phase 2 内仍可用 plan）。

## 2. 配置（PlanConfig）

`agent.json > plan`：

| 字段 | 默认 |
|---|---|
| `enabled` | **False** |

启用后 agent 会按场景生成 / 更新 plan；关闭则不生成。

## 3. 数据结构

[plan/schemas.py](../../src/wowooai/plan/schemas.py)

### 3.1 PlanStateResponse

```python
{
  "id": str,
  "name": str,
  "description": str,
  "expected_outcome": str,
  "state": "todo" | "in_progress" | "done" | "abandoned",
  "subtasks": [SubTaskResponse, ...],
  "created_at": str | None,
  "finished_at": str | None,
  "outcome": str | None
}
```

### 3.2 SubTaskResponse

```python
{
  "name": str,
  "description": str,
  "expected_outcome": str,
  "outcome": str | None,
  "state": "todo" | "in_progress" | "done" | "abandoned",
  "created_at": str | None,
  "finished_at": str | None
}
```

状态机：`todo → in_progress → done | abandoned`。

## 4. 实时推流

每个 agent 在 process 内维护一个"live plan"，更新时通过 SSE 广播给订阅方。

### 4.1 broadcast 接口

[plan/broadcast.py](../../src/wowooai/plan/broadcast.py)

| 函数 | 用途 |
|---|---|
| `register_sse_client(agent_id)` | 订阅，返回 asyncio.Queue |
| `unregister_sse_client(agent_id, q)` | 取消订阅（断连清理） |
| `get_live_plan(agent_id, session_id)` | 拿当前 plan 快照 |
| `clear_live_plan(agent_id, session_id)` | 清空（agent 完成或重置） |
| `broadcast_plan_update(...)` | 广播给所有订阅者 |

### 4.2 API 路径

| 方法 | 路径 | 用途 |
|---|---|---|
| `GET` | `/api/plan/current` | 拿当前 plan 状态快照 |
| `GET` | `/api/plan/stream` | SSE 订阅 plan 更新 |
| `GET` | `/api/plan/config` | 读 plan 配置 |
| `PUT` | `/api/plan/config` | 改 plan 配置（开关） |

## 5. Plan Hints（提示注入）

[plan/hints.py](../../src/wowooai/plan/hints.py) 控制"plan 状态如何影响 ReAct 循环"：

| 函数 | 用途 |
|---|---|
| `set_plan_gate(...)` / `check_plan_tool_gate(...)` | 在工具调用前判断是否被 plan 锁定（如 plan 状态为 done 时禁止再调修改类工具） |
| `should_skip_auto_continue(nb)` | plan 显示已完成时跳过 [13 §4](13-agent-engine.md) auto-continue |
| `_hint_no_plan(nb)` | 没有 plan 时给 agent 的提示 |
| `_hint_with_plan(plan, nb)` | 有 plan 时把当前 plan 状态注入下一轮 |
| `SimplePlanToHint` | 实现 agentscope `DefaultPlanToHint` 接口，做"plan → 文本提示"渲染 |

## 6. 与 ReAct 主循环的钩接

agentscope 提供 `Plan` 抽象 + 工具（`create_plan` / `update_subtask` 等）。本仓库在此之上：

1. PlanBuilder 注入 hints（`SimplePlanToHint`）→ ReAct 每轮把 plan 状态拼到上下文；
2. `should_skip_auto_continue` 让 agent 在 plan 完成后不再"被动续跑"；
3. `broadcast_plan_update` 让前端实时看到状态变化。

## 7. 与审批的关系

plan 工具调用本身（创建 / 更新 / abandon subtask）**不需要**审批。
plan 中执行的具体工具调用（如 shell / file_io）按 [20-approval-flow.md](20-approval-flow.md) 走正常审批。

## 8. UI

聊天页右侧（或下方）显示 plan 卡片：

- 任务名 + 整体状态徽章；
- subtasks 列表 + 各自状态；
- 实时刷新（SSE）；
- 用户可选择手动 abandon 整个 plan（调 API），让 agent 重新规划。

## 9. 0.0.1 不做

- 不做 plan 编辑器（用户不能直接改 subtasks，只能让 agent 重新规划或 abandon）。
- 不做 plan 模板库 / 复用。
- 不做跨 session 的 plan 持久化（重启后 live plan 清空）。
- 不做 plan 的版本回滚（只前进、不后退）。

# 20 — 审批流程（Approval Loop）

> 版本：0.0.1
> 对应代码：[src/wowooai/app/approvals/service.py](../../src/wowooai/app/approvals/service.py) · [src/wowooai/app/routers/approval.py](../../src/wowooai/app/routers/approval.py) · [src/wowooai/security/tool_guard/](../../src/wowooai/security/tool_guard/) · [src/wowooai/agents/tool_guard_mixin.py](../../src/wowooai/agents/tool_guard_mixin.py)

## 1. 关系图

```
agent._acting(tool_call)
   └─ tool_guard_mixin._before_tool
        └─ ToolGuard 执行规则
             ├─ 命中 denied_tools          → 直接拒绝（不可审批）
             ├─ approval_level=OFF        → 全部放行
             ├─ approval_level=AUTO + 非 guarded → 仅跑 always-run guardian
             ├─ approval_level=SMART + LOW/INFO → 自动放行
             └─ 否则                       → ApprovalService.create_pending
                                              └─ 返回 PendingApproval（含 Future）
                                              └─ 阻塞等待用户决定
                                              └─ 用户在 UI 点 approve / deny
                                                  └─ POST /api/approval/approve|deny
                                                  └─ ApprovalService.resolve_request
                                                  └─ Future.set_result → agent 继续
```

详见 [06-security.md](06-security.md) §1-3 的级别定义。

## 2. ApprovalService（单例）

[approvals/service.py:63 `ApprovalService`](../../src/wowooai/app/approvals/service.py#L63)

进程内全局单例，跨 agent / 跨 session 统一管理待审批工具调用。

| 方法 | 用途 |
|---|---|
| `create_pending(...)` | 写入 `PendingApproval`，返回 Future，阻塞调用方 |
| `resolve_request(req_id, decision)` | 设置 Future（approve / deny / deny_with_msg） |
| `get_pending_by_session(sid)` | 取下一条 FIFO 待审批 |
| `get_all_pending_by_session(sid)` | 取该 session 全部 |
| `list_pending_by_session(sid, include_subagents)` | 含 / 不含子 agent 的待审批 |
| `get_pending_by_root_session(root_sid)` | 含子调用的全树待审批（详见 [19 §2.4](19-sub-agents.md)） |

## 3. PendingApproval 字段

```python
@dataclass
class PendingApproval:
    request_id: str
    session_id: str
    root_session_id: str       # 用于跨 session 路由
    agent_id: str              # 哪个 agent 在请求
    tool_name: str
    tool_args: dict
    findings: list[Finding]    # 命中的规则
    summary: str               # format_findings_summary() 的人类可读摘要
    created_at: datetime
    future: asyncio.Future     # 等待用户决定
```

## 4. API 路径

| 方法 | 路径 | 用途 |
|---|---|---|
| `GET` | `/api/approval/list` | 列出待审批（按 root_session 过滤） |
| `POST` | `/api/approval/approve` | 批准一条 |
| `POST` | `/api/approval/deny` | 拒绝一条（可附理由） |

请求体（approve）：

```json
{ "request_id": "<uuid>" }
```

请求体（deny）：

```json
{ "request_id": "<uuid>", "reason": "可选的拒绝原因，注入给 agent" }
```

## 5. UI 行为

- 前端在 SSE 流里收到 `pending_approval` 事件 → 弹出审批卡片；
- 显示 `tool_name`、`tool_args`（脱敏）、`findings.summary`；
- 用户点"批准"/"拒绝"→ 调对应 API；
- agent 端 Future resolve → 工具执行 / 跳过。

## 6. 跨 session 路由

`root_session_id` 让嵌套 `chat_with_agent` 调用产生的审批挂到**调用方根 session** 上：

- 用户从主 chat 触发任务 → 任务里 agent A 调 agent B → B 触发 shell 审批
- 审批弹窗仍在主 chat 显示（不会"飘"到 B 的隐藏 session）

详见 [19-sub-agents.md §2.4](19-sub-agents.md)。

## 7. 渠道集成

`set_channel_manager(channel_manager)` 让 ApprovalService 可以**通过 channel 推送**审批通知（如发到钉钉群里让管理员审批）。

0.0.1 默认仍以 console 渠道为主审批入口；其他渠道审批 UI 不强制要求。

## 8. 超时策略

0.0.1 **没有自动超时**：

- pending approval 不会自动过期；
- 用户重启后端 → in-memory 状态丢失 → agent 在那次回合的 Future 永不 resolve（但因后端重启，回合本身已被打断）；
- 不做磁盘持久化。

下版本可能加默认超时（如 1 小时自动 deny）。

## 9. denied_tools 优先级

`ToolGuardConfig.denied_tools` 内的工具**直接拒绝**，不进入 ApprovalService —— 不能审批通过。
用途：永久禁掉某个工具（如禁 `execute_shell_command`），不希望任何弹窗。

## 10. 凭据隐私

- 审批卡片显示 `tool_args` 时，前端做基本脱敏（API key 字段 → `****`）；
- 审批日志只在内存 + dialog log，不上报；
- 审批拒绝理由由用户输入，可能含敏感词，仅落本地。

## 11. 0.0.1 不做

- 不做审批超时自动 deny。
- 不做审批审计日志单独导出。
- 不做多人会签 / 角色审批（单机单用户）。
- 不做"审批后批量信任"（每次工具调用独立审批）。

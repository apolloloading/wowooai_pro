# 17 — Mission（任务编排）

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/mission/](../../src/wowooai/agents/mission/) · [src/wowooai/app/runner/mission_dispatch.py](../../src/wowooai/app/runner/mission_dispatch.py)

## 1. 定位

Mission 是数字员工的**两阶段任务编排**：

- **Phase 1（PRD 生成）**：把用户的模糊请求结构化为 `prd.json`，列出可验证的 `userStories[]`。
- **Phase 2（迭代执行）**：按 PRD 循环执行，每轮检查 stories 是否全部 `passes`，未通过自动续跑。

适用于"需要分解、可验证、多轮"的任务（如"把一份文档转成 4 个格式 + 校对 + 邮寄"）。
**不适用**普通问答 / 简单工具调用——那些走标准 ReAct 即可。

## 2. 触发

通过斜杠命令进入：

```
/mission <task description>
/mission --verify <commands> <task>
/mission --max-iterations <N> <task>
/mission status
/mission list
```

[mission/handler.py:43 `is_mission_command`](../../src/wowooai/agents/mission/handler.py#L43) 在 [react_agent.py reply](../../src/wowooai/agents/react_agent.py#L1290) 中拦截，不进 ReAct 标准循环。

## 3. 参数

| 参数 | 默认 | 范围 | 说明 |
|---|---|---|---|
| `--max-iterations` | 20 | `[_MIN, _MAX]` 自动 clamp | Phase 2 最大循环次数 |
| `--verify` | 无 | — | 验证命令（agent 在 Phase 2 末尾执行以判定通过）|

## 4. 工作目录结构

```
<workspace>/missions/mission-<timestamp>/
├─ loop_config.json     ← 阶段、session_id、git context
├─ task.md              ← 用户原始任务文本
├─ prd.json             ← Phase 1 产出（必含 userStories[]）
├─ progress.txt         ← 每轮进度
└─ (其他��程文件)
```

按 mission 目录隔离，同 workspace 可存在多个历史 mission。

### 4.1 prd.json schema

[mission_runner.py:112 `_REQUIRED_PRD_FIELDS`](../../src/wowooai/agents/mission/mission_runner.py#L112)

```json
{
  "userStories": [
    {
      "id": "us-001",
      "description": "...",
      "verify": "...",
      "passes": false
    }
  ]
}
```

必含字段：顶层 `userStories`（数组，非空）；每个 story 必含 `id` / `description` / `verify` / `passes`。

校验入口：[`validate_prd(prd)`](../../src/wowooai/agents/mission/mission_runner.py#L129)。

## 5. 状态机

```
new (/mission <task>)
  └─► phase1            ← run_mission_phase1
       ├─ agent 生成 prd.json
       ├─ validate_prd 失败 → 自动注入修正提示，最多 _MAX_PRD_FIX_ATTEMPTS 次
       └─ agent 在 loop_config.json 设 current_phase="execution_confirmed"
              └─► phase2  ← run_mission_phase2
                   ├─ loop:
                   │   ├─ agent 执行一轮
                   │   ├─ 读 prd.json
                   │   ├─ 全部 passes=True? → done
                   │   └─ 否 → 注入"继续未完成的 stories"提示，继续
                   ├─ 达到 max_iterations → 停止
                   └─ 写 progress.txt
```

状态字段：`loop_config.json > current_phase`，值：

- `prd_generation` — Phase 1 进行中
- `execution_confirmed` — Phase 1 完成、待进 Phase 2
- `phase2` — Phase 2 进行中（隐式）
- `done` — 全部 stories passes

更新入口：[`_update_phase(loop_dir, phase)`](../../src/wowooai/agents/mission/mission_runner.py#L208)。

## 6. Phase 2 工具受限

`set_phase2_tool_restrictions(agent)`（[mission_runner.py:187](../../src/wowooai/agents/mission/mission_runner.py#L187)）���
- 用 `migrate_tools_to_group` 把工具按组分类；
- 临时禁用"implementation"组的部分工具，防止 Phase 2 在不该改文件时改文件；
- Mission 结束后 `restore_tools(agent)` 恢复。

具体禁用清单由当前实现决定（**不**作为公开 API 承诺）。

## 7. Session 绑定

每个 mission 关联 `session_id`（写入 `loop_config.json`）：

- `/mission status` 默认查**当前 session** 的最近 mission（[state.py:206 `get_active_loop_dir`](../../src/wowooai/agents/mission/state.py#L206)）；
- 不同 session 互不干扰；
- 无 `session_id`（兼容旧逻辑）→ 取全局最新。

## 8. Git 集成

`detect_git_context(workspace_dir)`（[state.py:57](../../src/wowooai/agents/mission/state.py#L57)）：

- 启动 mission 时探测是否在 git 仓库；
- 记录 `branch_name` 到 `loop_config.json > git_installed / is_git_repo / branch_name`；
- 仅作信息记录，不强制 commit。

## 9. Mission Dispatch（后端调度）

[app/runner/mission_dispatch.py](../../src/wowooai/app/runner/mission_dispatch.py) 把 mission 的"长任务"挂到 runner 框架下：

- 不阻塞主对话；
- 任务进度通过 SSE 推到前端；
- 详见 [18 — runner / 任务派发文档（待补）] —— 0.0.1 实现细节见代码。

## 10. CLI

```bash
wowooai mission list   --agent-id <id>
wowooai mission status --agent-id <id>
wowooai mission run    --agent-id <id> --task "..." [--verify "..."] [--max-iterations 20]
```

入口：[cli/mission_cmd.py](../../src/wowooai/cli/mission_cmd.py)。

## 11. 凭据隐私

- `prd.json` / `task.md` 可能含用户业务描述 → 仅留 workspace 本地。
- 不上报、不上传。
- 模板 / 示例**严禁**包含真实业务、账号、内部 URL。

## 12. 0.0.1 不做

- 不做 mission 间依赖（DAG / 并行 mission）。
- 不做 mission 暂停 / resume（要么跑完，要么停止）。
- 不做 Phase 3+（仅两阶段）。
- 不做跨 agent 的 mission 共享（mission 绑定到单一 workspace）。
- 不做 mission 失败自动 rollback（git commit 由用户决定）。

---
name: ai_create_cron_job
description: |
  Create a scheduled / recurring job (cron job) for the current wowooai
  digital employee. Use whenever the user asks to set up a recurring
  reminder / report / push — either explicitly via the front-end button
  (which prefixes the chat with `[使用技能：AI创建定时任务]`), or through
  free-form requests like "每天早上 9 点提醒我 / 每周一发周报 / set up a daily
  cron / schedule a recurring task".
  | 当用户要求为当前数字员工创建定时 / 周期任务时使用：可由「定时任务」页右上角
  「AI 创建任务」按钮触发（自动注入前缀 `[使用技能：AI创建定时任务]`），也可由
  用户口述「每天 9 点提醒我」「每周一发周报」「设置一个定时任务」等触发。
  会通过访谈把"时间 / 内容 / 渠道 / 目标"补齐 → 翻译为 cron 表达式 →
  调用后端 API 创建并汇报结果。
metadata:
  builtin_skill_version: "2.2"
  wowooai:
    emoji: "⏱️"
---

# AI 创建定时任务

## 触发条件

- 用户消息以 `[使用技能：AI创建定时任务]` 开头（前端按钮触发）
- 用户口语化请求："每天 9 点提醒我喝水"、"每周一发个周报给老板"、"set up a recurring reminder"
- 用户表达了「定时 / 周期 / 每天 / 每周 / 每月」等时间含义但参数不完整

不要用于：
- 用户已经给出了**完整且明确**的 cron 表达式 + 渠道 + 内容 → 走 `cron` 技能或直接 `POST /api/cron/jobs`
- 暂停 / 恢复 / 删除 / 立即执行已有任务 → `cron` 技能

## 工作流程

### 第一步 — 把意图拆成关键字段

**核心原则：尽量少问用户问题。** 多数字段已经能从当前会话上下文里取到，**不要重复追问**。

| 字段 | 在 payload 中的位置 | 怎么拿到 |
|---|---|---|
| 任务名 `name` | 顶层 | 自己根据用户描述生成一个简洁中文名（如"每日早安提醒"），**不要问用户** |
| Cron 表达式 | `schedule.cron` | 自己把"人话"翻译成 5 字段 cron，回读确认即可（见第二步） |
| 任务类型 | `task_type` | 默认 `agent`（数字员工生成回复后发送）；只有用户明确说"发送固定文案"才用 `text` |
| 内容 | `request.input`（agent 类型）或 `text`（text 类型） | **必须使用用户原话**——不要改写、概括、润色，把用户描述任务时的原文（去掉时间/渠道相关字眼后剩下的任务部分）原样填入 |
| 渠道 `dispatch.channel` | dispatch | **默认 `console`，不要问用户**。除非用户明确说"发到钉钉/飞书/iMessage" |
| 收件人 `dispatch.target.user_id` | dispatch | **默认取当前会话的 `User ID`**（见系统提示词「==」框中的 `User ID:` 字段），**不要问用户** |
| 会话 `dispatch.target.session_id` | dispatch | **默认取当前会话的 `Session ID`**（见系统提示词「==」框中的 `Session ID:` 字段），**不要问用户** |

可选：

| 字段 | 何时填 | 备注 |
|---|---|---|
| `schedule.timezone` | 跨时区 | 默认 `Asia/Shanghai` |
| `dispatch.mode` | — | 本技能统一传 `final`（任务完成后一次性投递；后端默认是 `stream`） |
| `enabled` | 想先创建后启用 | 默认 `true`；显式传 `false` 可创建为暂停 |
| `agent_id` | — | 不在 payload 里，靠 `X-Agent-Id` 头指定（取系统提示词 `agent.id`） |

> **唯一允许追问的场景**：用户描述里完全没有时间含义（不像定时任务），或时间含义模糊（"经常"、"过段时间"），才反问一句确认时间。其余字段一律不问。

### 第二步 — 把"人话"翻译成 cron 表达式

| 用户说 | Cron |
|---|---|
| 每天 09:00 | `0 9 * * *` |
| 每天 18:30 | `30 18 * * *` |
| 每周一 08:30 | `30 8 * * 1` |
| 工作日 09:00（周一到周五） | `0 9 * * 1-5` |
| 周末 10:00 | `0 10 * * 0,6` |
| 每 2 小时整点 | `0 */2 * * *` |
| 每 15 分钟 | `*/15 * * * *` |
| 每月 1 号 09:00 | `0 9 1 * *` |

> 翻译完后**必须**回读给用户确认：
> "根据你的描述，执行时间为 `0 9 * * 1-5`（工作日早上 9:00），这样对吗？"

### 第三步 — 调用 wowooai 后端创建

**优先用后端 API**（实时生效）。注意 wowooai 的 cron 任务是按 `schedule / dispatch / request` 三段式定义的。

**关键约束**：
- `task_type=agent` 时，`request.input` 必须是 **`List[Message]`**（一段 user 消息，content 是 text 块的数组），**不能是裸字符串**——后端 `stream_query` 内部会用 `AgentRequest` 校验，传字符串会直接抛 `ValidationError`。
- text 内容**必须使用用户描述任务时的原文**，不要改写、概括、润色。
- `task_type=text` 时不要带 `request`，只带顶层 `text` 字符串（固定文案）。
- `dispatch.target.user_id` / `session_id` **从当前会话上下文取**（见系统提示词环境块），不要问用户。
- `dispatch.channel` 默认 `console`，不要问用户。

```bash
BASE_URL="${WOWOOAI_API_BASE_URL:-http://127.0.0.1:8088}"
AGENT_ID="<当前数字员工 id，从系统提示获取>"
CURRENT_USER_ID="<从系统提示词 'User ID:' 取>"
CURRENT_SESSION_ID="<从系统提示词 'Session ID:' 取>"

# task_type=agent（默认）：数字员工执行任务后投递到渠道
# 注意 request.input 必须是 List[Message]，不能写裸字符串
curl -fsS -X POST "$BASE_URL/api/cron/jobs" \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: $AGENT_ID" \
  --data-binary @- <<JSON
{
  "name": "<自动生成的任务名>",
  "enabled": true,
  "schedule": {
    "type": "cron",
    "cron": "<cron 表达式>",
    "timezone": "Asia/Shanghai"
  },
  "task_type": "agent",
  "request": {
    "input": [
      {
        "role": "user",
        "type": "message",
        "content": [
          {"type": "text", "text": "<用户原话，不改写>"}
        ]
      }
    ]
  },
  "dispatch": {
    "type": "channel",
    "channel": "console",
    "target": {
      "user_id": "$CURRENT_USER_ID",
      "session_id": "$CURRENT_SESSION_ID"
    },
    "mode": "final"
  }
}
JSON

# task_type=text：仅当用户明确要求"发送固定文案"才用，把上面 task_type/request 整段替换为：
#   "task_type": "text",
#   "text": "<要发送的固定文案>"
# 注意：task_type=text 时不要再带 request 字段。
```

如果用户偏好 CLI（已经登录到本机 shell）：

```bash
wowooai cron create \
  --agent-id "$AGENT_ID" \
  --type agent \
  --name "<name>" \
  --cron "<cron>" \
  --channel "<channel>" \
  --target-user "<target_user>" \
  --target-session "<target_session>" \
  --text "<text>"
```

> 注意：CLI 默认 `--agent-id default`，对当前 wowooai 必须显式传 `wowooai`（或当前数字员工 id），否则任务会挂到 legacy `default` 工作区。CLI 内部会把这些参数装配成上面的 `schedule / dispatch / request` 三段式 payload，行为等价。

### 第四步 — 失败处理

| 情况 | 处理 |
|---|---|
| `schedule.cron` 表达式无效（5 字段格式错误） | 把 wowooai 后端报错原文展示给用户，引导重新描述时间 |
| `dispatch.channel` 不存在 / 未启用 | 让用户先到「外部频道」页启用对应渠道 |
| `dispatch.target.user_id` / `session_id` 缺失导致无法投递 | 询问当前会话所在渠道的对应 ID，或建议先发一条消息再来设置 |
| `task_type=agent` 但漏传 `request.input` | 提示用户补上"任务执行时给数字员工的 prompt" |
| `task_type=text` 但漏传 `text` | 提示用户补上"要发送的固定文案" |
| 5xx | 检查 `~/.wowooai/wowooai.log`，可能是定时器服务未启动 |

### 第五步 — 汇报结果

```markdown
✅ 定时任务「<name>」已创建！

- 执行时间：`<schedule.cron>`（<人类可读描述>）
- 类型：<task_type>（agent / text）
- 内容：<request.input 或 text>
- 渠道：<dispatch.channel>（→ user_id=<target.user_id>, session_id=<target.session_id>）
- 时区：<schedule.timezone>

可以：
- 在「定时任务」页查看 / 编辑 / 暂停 / 立即执行；
- 或者命令行：`wowooai cron list --agent-id <agent_id>`
```

## 注意事项

- **`request.input` 是用户原话**——不要改写、概括、润色，否则定时执行时数字员工拿到的 prompt 与用户期望脱节。
- **Renliwo keyword detection (REQUIRED)**: when the user's text matches any of these keywords, the generated `request.input` text MUST be prefixed with `[使用工具：renliwo_browser] ` (with trailing space), preserving the user's original words after the prefix:
  - Domains: `renliwo.com`, `ereference-v-uat.renliwo.com`
  - Keywords: `Renliwo`, `renliwo`, `人力沃`, `合同产品列表`, `综合管理`, `合同管理`, `认款`, `渠道费`, `费用结算`
  - Example: user says "每天 0 点登录 renliwo 导出合同产品列表" → `request.input` text becomes `[使用工具：renliwo_browser] 每天 0 点登录 renliwo 导出合同产品列表`
  - Reason: `browser_use` now hard-refuses *.renliwo.com URLs; the cron must explicitly route through `renliwo_browser` or it will fail at execution time.
- `dispatch.target.user_id` / `session_id` / `channel` 默认全部走当前会话上下文（`User ID` / `Session ID` 在系统提示词环境块里，channel 默认 `console`），**不要问用户**。
- `task_type=agent` 时，**`request.input` 是给数字员工的"提问"**——执行时数字员工会先生成一段回复再发给渠道；如果用户明确要求"推送一段固定文案"，才改用 `task_type=text` + `text` 字段。
- 创建后默认 `enabled: true`，会立即被调度器纳入计划；如果用户明确说"先创建好，待会儿再启用"，才传 `enabled: false`。
- `timezone` 默认 `Asia/Shanghai`；除非用户明确说在其它时区，否则不要换。

## 端上自测 prompt（v2.2）

复制以下任意一句到对话框，验证本技能能正确触发：

- `[使用技能：AI创建定时任务]，帮我创建一个定时任务`（前端按钮等价 prompt）
- `每天早上 9 点提醒我喝水`
- `工作日下午 6 点给我汇总今天的待办`
- `每周一 8:30 给老板发上周周报`
- `daily 9am, send me a summary of yesterday's tasks via console`

期望：数字员工识别到本技能 → 把"人话"翻译成 cron 表达式并回读确认 → **直接用当前会话的 user_id / session_id / channel=console 默认值** + **用户原话作为 `request.input`** → 调用 `POST /api/cron/jobs` → 给出创建结果。**不应反问 user_id / session_id / 渠道 / 任务名。**

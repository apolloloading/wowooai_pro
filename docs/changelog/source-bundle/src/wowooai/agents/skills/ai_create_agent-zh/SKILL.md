---
name: ai_create_agent
description: |
  Create a new digital employee (agent) for WowooAI. Use whenever the user
  asks to add a new digital employee — either explicitly via the front-end
  button (which prefixes the chat with `[使用技能：AI创建数字员工]`), or
  through free-form requests like "帮我创建一个 XX 员工 / 加一个负责 XX 的同事 /
  add a new agent / new digital employee".
  | 当用户要求创建新数字员工时使用：可由「数字员工管理」页右上角「AI 创建数字员工」按钮触发
  （会自动注入前缀 `[使用技能：AI创建数字员工]`），也可以直接由用户口述
  「帮我创建一个 XX 员工」「新增一个负责 XX 的同事」等触发。
  通过访谈收集名称 + 职责描述 → 调用 wowooai 后端 API 完成创建并汇报结果。
metadata:
  builtin_skill_version: "2.2"
  wowooai:
    emoji: "🧑‍💼"
---

# AI 创建数字员工

## 触发条件

- 用户消息以 `[使用技能：AI创建数字员工]` 开头（前端按钮触发）
- 用户口语化请求："帮我创建一个 XX 员工"、"新增一个负责 XX 的数字员工"、"add a new agent"
- 用户描述了一个**新的角色/职责**而当前数字员工列表里没有合适人选

不要用于：
- 修改 / 重命名 / 删除已有数字员工 → 让用户去「数字员工管理」页
- 仅询问"我有哪些数字员工" → 用 `chat_with_agent` 或直接调用 `GET /api/agents`

## 工作流程

### 第一步 — 收集必要信息

需要至少两项：

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 数字员工的中文 / 英文名（≤ 32 字符，建议短而记得住） |
| `description` | ✅ | 一两句职责描述。会被写入新数字员工的 `SOUL.md` 工作指南 |
| `language` | 可选 | 默认沿用当前 wowooai 配置的 `agents.language`（一般是 `zh`） |

如果用户只给了名称没给职责，**主动追问**一次：

> 好的，我可以帮你创建数字员工「<name>」。请问 ta 主要负责什么工作？
> 一两句话描述即可，内容会写入 ta 的工作指南。

如果名称也没有，按"名称 / 职责"两问搜集后再继续。

### 第二步 — 调用后端 API 创建

```bash
# 解析出当前 wowooai 服务的 base url（尊重用户启动时的 --host/--port）
BASE_URL="${WOWOOAI_API_BASE_URL:-http://127.0.0.1:8088}"

curl -fsS -X POST "$BASE_URL/api/agents" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "name": "<name>",
  "description": "<description>",
  "language": "zh",
  "skill_names": [
    "onboarding-guide",
    "ai_create_agent",
    "ai_create_cron_job",
    "ai_create_skill"
  ]
}
JSON
```

> **不要**自行设置 `id` 字段——后端会按 `name` 自动生成稳定 ID，传 `id` 反而容易和现有数字员工撞车。
>
> `skill_names` 必须显式传入。后端 `_install_initial_skills` 默认会用空列表，新员工会缺少基础引导/自助创建技能；上面 4 个是与默认 `wowooai` 数字员工一致的最小集合。

`POST /api/agents` 返回结构（成功）：

```json
{
  "id": "abc123",
  "workspace_dir": "/Users/.../.wowooai/workspaces/abc123",
  "enabled": true
}
```

返回的 `id` 即未来切换 / 删除该数字员工时使用的稳定标识。

### 第三步 — 失败处理

| HTTP | 含义 | 回应用户 |
|------|------|---------|
| 4xx `name conflict` 或 `id already exists` | 同名 / 同 id 已存在 | 询问是否换个名字，或者建议在原数字员工里加技能 |
| 4xx `invalid language` | 语言不支持 | 告知支持 `zh` / `en` / `ru` 后重试 |
| 5xx | 后端异常 | 让用户截图后台日志 (`tail -f ~/.wowooai/wowooai.log`)，并尝试重启 wowooai |

不要静默吞掉错误，永远把后端返回的 message 直接展示给用户。

### 第四步 — 汇报结果

```markdown
✅ 数字员工「<name>」已创建！

- ID：`<id>`
- 工作指南：已根据你的描述写入 `SOUL.md`
- 工作目录：`<workspace_dir>`

你可以：
- 在左侧顶部的数字员工选择器里切换到 ta；
- 在「数字员工管理」页里继续完善：渠道（DingTalk / Feishu / iMessage）、模型 provider、技能等；
- 在「记忆」里查看并编辑 ta 的「员工身份 / 工作指南 / 用户档案 / 记忆日志」四份档案。
```

## 注意事项

- `description` 写得越具体，新数字员工的工作指南质量越高；如果用户给了一个很短的角色名（"招聘 HR"），鼓励 ta 多说一两句细节。
- 创建后**不会**自动启用任何渠道；需要用户去「外部频道」页手动开启并填配置。
- 创建后的默认技能集（`onboarding-guide` + 三个 `ai_create_*` 自助技能）由本技能显式传入 `skill_names`，与默认 `wowooai` 数字员工一致；不要省略这个字段，否则新员工会"光秃秃"什么技能都没有。
- 不要用本技能创建跟 `wowooai` 同 id 的数字员工；也不要自己传 `id`，让后端按 `name` 自动分配。

## 端上自测 prompt（v2.2）

复制以下任意一句到对话框，验证本技能能正确触发：

- `[使用技能：AI创建数字员工]，帮我创建一个数字员工`（前端按钮等价 prompt）
- `帮我新建一个负责招聘的数字员工，名字叫"招聘小助手"`
- `我想加一个数字员工：法务合同审查，专门帮我看劳动合同条款`
- `new digital employee: customer support specialist, handle FAQ in English`

期望：数字员工识别到本技能 → 主动追问职责（如未给）→ 调用 `POST /api/agents` → 给出创建结果。

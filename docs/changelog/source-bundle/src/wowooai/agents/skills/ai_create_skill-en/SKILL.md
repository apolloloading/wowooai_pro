---
name: ai_create_skill
description: |
  Author and install a new SKILL.md for the currently active wowooai
  digital employee. Use whenever the user asks to add / build / write a
  new skill — either explicitly via the front-end button (which prefixes
  the chat with `[使用技能：AI创建技能]`), or through free-form requests
  like "帮我写一个能 XX 的 skill / 给我一个 XX 工具技能 / build me a skill
  that does XX".
  | 当用户要求为当前数字员工新建技能时使用：可由「我的技能」页右上角
  「AI 创建技能」按钮触发（会自动注入前缀 `[使用技能：AI创建技能]`），也
  可以直接由用户口述「帮我写一个 XX 技能 / 我需要一个能 XX 的工具」等触发。
  会基于用户需求生成 SKILL.md → 写入工作区 → 调用 refresh 接口让 wowooai
  立即识别 → 引导用户到「我的技能」页启用。
metadata:
  builtin_skill_version: "2.2"
  wowooai:
    emoji: "🛠️"
---

# AI 创建技能

## 触发条件

- 用户消息以 `[使用技能：AI创建技能]` 开头（前端按钮触发）
- 用户口语化请求："帮我写一个 XX 技能"、"新建一个能 XX 的 skill"、"build me a skill that does XX"
- 现有技能库中确实没有满足需求的技能

不要用于：
- 调整 / 删除现有技能 → 让用户去「我的技能」页直接编辑
- 用户仅询问"有哪些技能"→ 用 `GET /api/skills` 查询

## 工作流程

### 第一步 — 提取技能要素

至少要拿到 4 项信息（缺哪几项就追问哪几项）：

| 字段 | 必填 | 约束 |
|---|---|---|
| 名称 (`<skill_name>`) | ✅ | 英文小写 + 下划线，≤ 32 字符，须与目录名一致；不能与现有技能重名 |
| 触发描述 (`description`) | ✅ | 一句话说清楚"什么时候 / 什么样的用户输入会触发这个技能"。是模型决策时最重要的字段 |
| 工作流程 | ✅ | 步骤化的执行说明（也可以是引导式访谈） |
| 依赖 / 副作用 | 可选 | 是否调用外部 API、是否写文件、是否需要某些环境变量 |

> 技能名称冲突？先 `GET /api/skills` 列出已有名字，提示用户换一个或加后缀。

### 第二步 — 起草 SKILL.md 内容

在内存里生成完整 SKILL.md 文本（**不要**直接写文件），骨架：

```markdown
---
name: <skill_name>
description: <一句话说明何时触发，建议同时给出中文 + English>
metadata:
  wowooai:
    emoji: "🎯"
---

# <技能标题>

## 触发条件

- <场景 1>
- <场景 2>

## 工作流程

### 第一步 — ...
### 第二步 — ...
### 第三步 — 失败处理

## 注意事项

- ...
```

> 工作流程请按"第一步 / 第二步 / ..."写出可执行步骤，避免只罗列要点。

### 第三步 — 调 `POST /api/skills` 创建并启用

**必须**走专门的创建端点，由后端 `SkillService.create_skill` 做命名/冲突校验、写文件并自动 reload：

```bash
BASE_URL="${WOWOOAI_API_BASE_URL:-http://127.0.0.1:8088}"
# X-Agent-Id 必须填当前数字员工 id（系统提示词里的 agent.id）
curl -fsS -X POST "$BASE_URL/api/skills" \
  -H "X-Agent-Id: <当前数字员工 id>" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "name": "<skill_name>",
  "content": "<完整 SKILL.md 文本，含 frontmatter>",
  "enable": true
}
JSON
```

接口行为：

1. 校验 name 与现有技能不冲突（重名直接 4xx，不会覆盖）；
2. 写入 `<workspace>/skills/<name>/SKILL.md`；
3. `enable=true` 时自动加入数字员工 manifest 并 schedule reload，无需再调 `/api/skills/refresh`；
4. 返回创建后的 SkillRef。

> 不要再走「shell 写文件 + POST /api/skills/refresh」的旧路径——会跳过校验、可能静默覆盖用户已有技能、且 enable 状态需用户手动再开。

### 第四步 — 错误处理

| 情况 | 处理 |
|---|---|
| 4xx：name 冲突 / 校验失败 | 把响应体直接展示给用户，提示改名或修正 frontmatter |
| 4xx：JSON 体里包含特殊字符导致解析失败 | 用 `--data-binary @file.json` 方式发送，避免 shell 转义 |
| 5xx | 引导用户检查 `~/.wowooai/wowooai.log` |

### 第五步 — 汇报结果

```markdown
✅ 技能「<skill_name>」已写入工作区！

- 文件：`<workspace>/skills/<skill_name>/SKILL.md`
- 触发说明：<description>
- 当前状态：**已启用**

技能已自动启用并加入系统提示词，可以立即在对话中触发。如需调整可去「我的技能」页直接编辑。
```

## 注意事项

- 技能目录名 = `name` 字段值，必须严格一致；都用英文小写 + 下划线。
- `description` 是模型选用本技能的关键依据，请把"何时使用 / 不使用"写清楚。
- 涉及外部 API / 写本地文件 / 调用 Shell 等"副作用"必须在 SKILL.md 里**显式声明**，否则审批策略可能拦截执行。
- 如果用户描述里出现 API Key、Token 等敏感信息，**不要**直接写进 SKILL.md，而是引导用户用 `os.environ.get(...)` 读取。
- 涉及多语言用户的 skill，建议同时提供 `<name>-zh` 和 `<name>-en` 两个变体目录。

## 端上自测 prompt（v2.2）

复制以下任意一句到对话框，验证本技能能正确触发：

- `[使用技能：AI创建技能]，帮我创建一个技能`（前端按钮等价 prompt）
- `帮我写一个能查天气的 skill，输入城市名，返回未来 3 天预报`
- `新建一个技能：把当前 Markdown 文件转成 PDF`
- `build me a skill that pings a URL every minute and alerts on non-200`

期望：数字员工识别到本技能 → 追问技能名称 / 触发条件 / 工作流程 → `POST /api/skills` 创建并启用 → 引导用户对话中直接触发。

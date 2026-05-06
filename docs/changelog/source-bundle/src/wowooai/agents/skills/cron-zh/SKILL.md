---
name: cron
description: 仅在需要未来定时执行或周期执行任务时，使用本 skill。使用 wowooai cron list/create/get/state/pause/resume/delete/run 管理任务，并始终显式传入 --agent-id。
metadata:
  builtin_skill_version: "2.1"
  wowooai:
    emoji: "⏰"
---

# 定时任务管理

## 什么时候用

只有在需要**未来某个时间自动执行**，或**按周期重复执行**时，使用本 skill。

### 应该使用
- 用户要求"每天 / 每周 / 每小时"执行某事
- 用户要求"明天 9 点 / 下周一 / 某个时间"自动提醒或执行操作
- 需要长期周期性通知、检查、汇报、数据导出

### 不应使用
- 只是要**现在立即执行一次**
- 只是当前会话中的正常回复
- 用户没有明确执行时间或周期
- 目标 channel / user / session 还不明确

---

## 决策规则

1. **只有在未来定时执行或周期执行时才使用 cron**
2. **如果只是立即做一次，通常不要创建 cron**
3. **创建前必须确认执行时间/周期、目标 channel、target-user、target-session**
4. **所有 cron 命令都必须显式传 `--agent-id`**
5. **不要依赖默认 agent，否则任务可能落到 default workspace**

---

## 关键：如何选择 `--type`

这是最容易出错的地方。创建任务时必须根据**用户需求的本质**选择类型：

### `--type text`：只发送一条固定消息

**适用场景**：只需要在目标时间发一条**纯文本消息**，不需要任何计算、查询、操作。

**触发后的行为**：系统直接把 `--text` 的文本发到目标 channel，**不经过 agent**，**不执行任何工具调用**。

### `--type agent`：触发 agent 执行完整任务

**适用场景**：需要在目标时间让 agent **执行某个任务**，包括——但不限于：
- 浏览器操作（登录网站、导出数据、填写表单）
- 数据处理（读取文件、关联表格、生成报表）
- Shell 命令（运行脚本、检查系统状态）
- MCP 工具调用（查询 API、操作外部系统）
- 综合工作流（先查数据、再处理、最后发送结果）

**触发后的执行链路**：
1. 系统把 `--text` 的内容包装成一个 agent 请求（等同于用户在对话中发了这条消息）
2. Agent 收到这个消息后，**像处理用户消息一样正常执行**：
   - 根据任务描述调用相应工具（浏览器、Shell、文件读写、MCP 等）
   - 生成回复内容
3. 回复通过 channel 发送到目标 session

### 判断方法

> 问自己：**"到达时间后，这段文本是需要被『读出来』，还是需要被『执行』？"**
> - 读出来 → `--type text`
> - 执行 → `--type agent`

---

## 参数说明

### 默认值

以下参数如果用户没有特别说明，使用这些默认值：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--channel` | `console` | 默认发送到当前控制台 |
| `--target-user` | `default` | 默认发送给当前用户 |
| `--target-session` | 当前 session ID | 默认发送到当前会话（从系统提示中获取） |

### `--text` 参数的含义

根据 `--type` 不同，`--text` 的含义不同：

| 类型 | `--text` 的含义 | 内容要求 | 示例 |
|---|---|---|---|
| **text** | 最终发送给用户的消息内容 | 可以美化、润色用户的原始描述，使其更友好、更自然 | 用户说"提醒我喝水" → `--text`："该喝水了！记得保持水分，多喝水身体好" |
| **agent** | 任务指令，等同于用户在对话中发的消息 | 应该包含所有 agent 执行时需要的信息：操作路径、账户凭证、处理规则、输出要求。**尽量使用用户的原描述，不要改写或简化** | "请打开 https://xxx.com ，使用账户 xxx 登录，导航到合同管理，导出报表并发送给我" |

### `--text` 过长时的处理

如果任务描述很长（超过 500 字符），建议先生成 JSON 文件，用 `wowooai cron create --agent-id <agent_id> -f job_spec.json` 创建。

---

## 创建 agent 任务时的注意事项

agent 任务在触发时是**独立执行**的——它不会继承当前会话的上下文。因此 `--text` 中必须包含：

- 所有操作需要的信息（网址、账户、密码、文件路径等）
- 期望的输出格式和发送方式
- 任何 agent 在执行时需要的上下文

**如果用户描述不够清楚，必须先追问清楚再创建**：
- 用户说"每天检查一下服务器" → 追问：检查什么？CPU？内存？服务响应？用什么方式？
- 用户说"每天导出报表" → 追问：哪个网站？登录凭证是什么？导出后怎么处理？
- 用户说"提醒我开会" → 这种是纯消息，用 `--type text`

**尽量保留用户原描述**：如果用户的描述已经足够清晰（包含了操作路径、账户、输出要求），直接作为 `--text` 使用，不要改写或简化。只在用户描述模糊时追问补充。

---

## 硬规则

### 必须显式指定 `--agent-id`

所有 `wowooai cron` 命令都**必须**传：

```bash
--agent-id <your_agent_id>
```

你的 agent_id 在系统提示中的 Agent Identity 部分（Your agent id is ...）。
不得省略，否则任务可能错误创建到 default agent 的 workspace。

---

## 常用命令

```bash
# 列出任务
wowooai cron list --agent-id <agent_id>

# 查看任务详情
wowooai cron get <job_id> --agent-id <agent_id>

# 查看任务状态
wowooai cron state <job_id> --agent-id <agent_id>

# 创建任务
wowooai cron create --agent-id <agent_id> ...

# 删除任务
wowooai cron delete <job_id> --agent-id <agent_id>

# 暂停 / 恢复任务
wowooai cron pause <job_id> --agent-id <agent_id>
wowooai cron resume <job_id> --agent-id <agent_id>

# 立即执行一次已有任务
wowooai cron run <job_id> --agent-id <agent_id>
```

> **注意**：CLI 没有 `update` 命令。要修改已有任务，需要先获取详情 → 删除 → 重新创建。

---

## 创建任务

### 创建前最少要确认
- `--type`（text 还是 agent？见上方决策指南）
- `--name`
- `--cron`
- `--channel`
- `--target-user`
- `--target-session`
- `--text`
- `--agent-id`

如果缺少这些信息，应先向用户确认，再创建任务。

### `--type text` 创建示例

```bash
wowooai cron create \
  --agent-id <agent_id> \
  --type text \
  --name "喝水提醒" \
  --cron "0 9 * * *" \
  --channel console \
  --target-user default \
  --target-session "1777892768390" \
  --text "该喝水了！记得保持水分，多喝水对身体好"
```

> `--text` 是最终用户看到的提醒文案，可以美化、润色，使其更友好。

### `--type agent` 创建示例（简单问答）

```bash
wowooai cron create \
  --agent-id <agent_id> \
  --type agent \
  --name "检查待办" \
  --cron "0 */2 * * *" \
  --channel console \
  --target-user default \
  --target-session "1777892768390" \
  --text "我有什么待办事项？"
```

### `--type agent` 创建示例（复杂工作流）

```bash
wowooai cron create \
  --agent-id <agent_id> \
  --type agent \
  --name "每日合同报表导出" \
  --cron "0 8 * * *" \
  --channel console \
  --target-user default \
  --target-session "1777892768390" \
  --text "请执行以下操作：
1. 打开 https://ereference-v-uat.renliwo.com/ ，使用账户 17758000644，密码 admin12345677 登录
2. 进入网站后，点击左侧【合同管理】下子菜单【合同产品列表】
3. 点击页面【查询】按钮
4. 点击【查询导出】，将下载路径修改为电脑桌面，保存为表1
5. 读取桌面上的表2：关联数据.xlsx
6. 关联两张表并拆分结果，将处理后的表发送给我"
```

> **注意**：`--type agent` 的 `--text` 是**完整的任务描述**，应该包含所有 agent 需要的信息。尽量使用用户的原描述，不要改写或简化。

### 从 JSON 创建

```bash
wowooai cron create --agent-id <agent_id> -f job_spec.json
```

---

## 修改已有任务

CLI 没有 `update` 命令。要修改任务（如更改时间、内容、名称等），按以下步骤操作：

```bash
# 1. 获取任务详情
wowooai cron get <job_id> --agent-id <agent_id>

# 2. 删除旧任务
wowooai cron delete <job_id> --agent-id <agent_id>

# 3. 用新参数重新创建
wowooai cron create --agent-id <agent_id> ...
```

---

## 最小工作流

```
1. 判断是否真的是"未来定时"或"周期执行"
2. 确认执行时间/周期
3. 确认 channel、target-user、target-session（未指定则用默认值：console / default / 当前 session）
4. 【关键】判断任务性质：纯消息 → text；需要执行操作 → agent
5. 如果用户描述不清楚，追问补充；如果已清晰，agent 任务使用用户原描述，text 任务可以美化文案
6. 显式带上 --agent-id
7. wowooai cron create 创建任务
8. 后续用 list / state / pause / resume / delete 管理
```

---

## Cron 表达式示例

```
0 9 * * *      每天 9:00
0 */2 * * *    每 2 小时
30 8 * * 1-5   工作日 8:30
0 0 * * 0      每周日零点
*/15 * * * *   每 15 分钟
```

---

## 常见错误

### 错误 1：把一次性立即执行当成 cron

如果只是现在执行一次，通常不要创建 cron。

### 错误 2：没传 `--agent-id`

这会导致任务落到错误的 agent / workspace。所有 cron 命令都必须显式传 `--agent-id`。

### 错误 3：信息没补全就创建

如果用户没说明时间、周期、目标 channel 或目标 session，应先追问。

**对于 agent 任务**，还需要确认 `--text` 中是否包含了所有执行需要的信息（网址、账户、文件路径等）。如果用户描述模糊，必须追问清楚。

### 错误 4：操作已有任务前不先查

暂停、恢复、删除前，先用：

```bash
wowooai cron list --agent-id <agent_id>
```

找到正确的 `job_id`。

### 错误 5：需要 agent 执行任务时选了 `--type text`

如果用户要求定时执行某个操作（如"每天 8 点自动导出报表"、"每小时检查服务器状态"），但创建时选了 `--type text`，则**系统只会把这段文本发出去，不会执行任何操作**。

正确做法是用 `--type agent`，让 agent 在触发时真正执行任务。

**判断方法**：
- `text` 触发后 = 文本被原样打印出来
- `agent` 触发后 = agent 收到消息 → 调用工具 → 执行任务 → 发送结果

---

## 使用建议

- 缺少参数时，先问用户再创建
- text 任务的 `--text` 可以美化、润色用户的原始描述，使其更友好
- agent 任务的 `--text` 尽量使用用户的原描述，除非用户描述不清楚
- agent 任务的 `--text` 需要包含完整上下文（agent 触发时没有当前会话的记忆）
- 修改任务时，先 `get` 详情 → `delete` → `create`
- 修改/暂停/删除前，先 `wowooai cron list --agent-id <agent_id>`
- 排查问题时，用 `wowooai cron state <job_id> --agent-id <agent_id>`
- 给用户展示命令时，提供完整、可直接复制的版本

---

## 帮助信息

```bash
wowooai cron -h
wowooai cron list -h
wowooai cron create -h
wowooai cron get -h
wowooai cron state -h
wowooai cron pause -h
wowooai cron resume -h
wowooai cron delete -h
wowooai cron run -h
```

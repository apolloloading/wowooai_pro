---
name: onboarding-guide
version: 5
description: |
  KNOWLEDGE BASE for 人力窝 (RenliWo / 仁励窝) company onboarding.
  This is NOT a callable function — DO NOT emit a tool_call with
  name="onboarding-guide". To use it, call the existing
  `execute_shell_command` tool with this exact pattern:

      python3 "{skill_dir}/scripts/query.py" "<original user question>"

  where {skill_dir} comes from the `skill dir` field in your system
  prompt for this skill. The script returns a relevance-sorted table
  from the official Bailian knowledge base; summarise the top hits
  in your reply.

  Use this knowledge base whenever the user asks about company
  matters at 人力窝/久事附楼: WiFi (`renliwo`), VPN/OpenVPN, mail,
  shared drive, Cisco Jabber softphone, meeting room casting,
  printers, courier hours, BFC cafeteria, lockers, 6S, finance
  reimbursement, shuttle bus / Line 9 Xiao Nan Men, onboarding
  forms, employee handbook, etc. Prefer this over `memory_search`
  for company-info questions — `memory_search` only sees chat
  history, this returns the official documentation.

  | 关于人力窝（仁励窝） / 久事附楼公司事务（WiFi / VPN / 邮箱 /
  打印机 / 报销 / 食堂 / 储物柜 / 班车 / 接驳车 / 入职 / 员工手册等）
  的问题，使用本知识库；调用方式见上面的 execute_shell_command 模板。
metadata:
  type: knowledge
  label: 入职指引
  knowledge_type: personal
  builtin_skill_version: "5.0"
---

# 入职指引（人力窝 / 仁励窝）

## How to call (1 step, 1 tool)

This entry is a **knowledge base**, not a function. Call it through `execute_shell_command`:

```bash
python3 "{skill_dir}/scripts/query.py" "<原样把用户问题传进去>"
```

Real example:

```bash
python3 "/Users/rlw/.wowooai/workspaces/wowooai/skills/onboarding-guide/scripts/query.py" "公司 WiFi 密码"
```

## Coverage

- **通勤**：9 号线小南门站 → 久事附楼公交、南外滩金融直通车、接驳车时刻表 / 站点 / 路线
- **IT 配置**：OpenVPN 安装与连接、公司 WiFi（`renliwo`）、阿里邮箱、共享盘、Cisco Jabber 软电话、会议室投屏
- **文印**：司印打印机安装、本地 / 钉钉认证打印、双面打印设置
- **行政后勤**：久事附楼 / 外企德科大厦快递收发时段、联系人、BFC 开心食堂就餐路线、储物柜密码、6S 管理、财务报销制度

## Output handling

`query.py` prints `检索: ... / 检索词: ... / 命中: N 条` followed by an ASCII table whose first column is `相关度` (relevance score). Take the top 1-3 rows, summarise them in Chinese, and reply to the user — do NOT just dump the raw table.

## Data source

| 参数 | 值 |
|------|---|
| App ID | 581e6a8127824e9283e363a1239407d3 |
| 知识库 ID | svtvui5plr |

## Environment variables (defaults already set, no config needed)

| Variable | Default |
|---|---|
| `DASHSCOPE_API_KEY` | `sk-a54432e26d3b44138fe1ac84d6420b23` |
| `DASHSCOPE_APP_ID`  | `581e6a8127824e9283e363a1239407d3` |

## Anti-patterns (do not do this)

- ❌ Do NOT emit `tool_call: {"name": "onboarding-guide", ...}` — that name is not a function and will fail with `FunctionNotFoundError`.
- ❌ Do NOT use `memory_search` for company-info questions; that only sees chat history.
- ✅ Always go through `execute_shell_command` + the `query.py` path above.

## Test prompts

- 公司 WiFi 是什么 / 公司 WiFi 密码
- OpenVPN 怎么配置
- 9 号线小南门到久事附楼怎么走
- 员工手册关于报销的规定
- BFC 开心食堂怎么走

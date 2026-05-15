# 03 — 技能（Skill）系统

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/skills/](../../src/wowooai/agents/skills/) · [src/wowooai/agents/templates.py](../../src/wowooai/agents/templates.py) · `SkillPoolService`

## 1. 概念

**Skill** = 一份 markdown 文档（`SKILL.md`），告诉模型 "在某种场景下如何调用工具完成某类任务"。

| 要素 | 形式 |
|---|---|
| 定义 | `<workspace>/skills/<name>/SKILL.md` |
| 加载方式 | 工作区目录扫描；frontmatter 中 `enabled` 控制是否注入 |
| 来源 | 内置 skill_pool（仓库 `agents/skills/<name>-<lang>/`）/ 用户工作区自定义 |

Skill 是**纯文档**：不是 Python 代码，不是工具。模型在 system prompt 中读到 SKILL.md 后，按文档指导调用已经存在的内置工具或 shell 命令。

## 2. SKILL.md 格式

```markdown
---
name: <skill_name>
description: <一句话场景描述，告诉模型何时启用>
metadata:
  builtin_skill_version: "x.y"
  wowooai:
    emoji: "🔧"
    requires:
      bins: ["npx"]      # 可选：依赖外部二进制
      tools: ["browser_use"]  # 可选：依赖内置工具
---

# 标题

## 何时使用 / 不使用
...

## 强制规则
...

## 示例
...
```

## 3. 内置 skill_pool（0.0.1）

仓库内置 22+ 对双语 skill（`<name>-zh` / `<name>-en`）：

| 类别 | Skill |
|---|---|
| 计划 | `make_plan` |
| 文件读取 | `file_reader` |
| Office | `pdf` / `docx` / `xlsx` / `pptx` |
| 定时任务 | `cron` |
| 浏览器 | `browser_visible` / `browser_cdp` / `agent_browser` |
| 桌面 | `desktop_control` |
| 多 agent | `multi_agent_collaboration` / `chat_with_agent` |
| 渠道 | `channel_message` / `dingtalk_channel` |
| 内置 QA | `QA_source_index` / `guidance` |
| 入门指引 | `onboarding-guide`（zh / en / ru） |
| 业务 | `news` / `himalaya` |

完整目录见 [src/wowooai/agents/skills/](../../src/wowooai/agents/skills/)。

## 4. 默认数字员工预装（11 个）

[templates.py `DEFAULT_TEMPLATE_SKILL_NAMES`](../../src/wowooai/agents/templates.py)：

```python
DEFAULT_TEMPLATE_SKILL_NAMES = (
    "make_plan",
    "file_reader",
    "pdf",
    "docx",
    "xlsx",
    "pptx",
    "cron",
    "browser_visible",
    "browser_cdp",
    "desktop_control",
    "agent_browser",
)
```

不预装：`channel_message` / `dingtalk_channel` / `multi_agent_collaboration` / `news` / `himalaya` / `QA_source_index` 等专项技能（避免新用户默认上下文过重或误触发流程）。

## 5. 内置 QA Agent 预装

`wowooai_QA_Agent_0.2` 只装：
- `QA_source_index`
- `guidance`

并通过 `build_qa_agent_tools_config()` 把工具集限定为 5 个（execute_shell_command / read_file / write_file / edit_file / view_image）。

## 6. 安装与启用

### 6.1 创建新 agent 时

`_initialize_agent_workspace()` 在创建工作区后：
1. 复制 `agents/md_files/<lang>/` 下的 MD 模板到 workspace。
2. 调用 `_install_initial_skills()` → `SkillPoolService.download_to_workspace()` 把 `initial_skill_names` 中的每个 skill 拷入 `<workspace>/skills/<name>/`。
3. 在 `<workspace>/skill.json` manifest 中标记 `enabled=True`。

### 6.2 用户后续操作

- UI `/skills` 页：从 skill_pool 安装 / 卸载 / 启用 / 禁用 / 编辑。
- 用户编辑后的 skill：保留在 workspace，启动时不会被 skill_pool 覆盖。
- 删除 skill 目录与 manifest 项才会真正卸载。

### 6.3 不重复覆盖

只有首次创建 default agent（`agent.json` 不存在）时才安装预装 skill；已存在 default agent 不会再次写入。

## 7. SKILL.md 双语策略

`<name>-zh` 与 `<name>-en` 内容必须功能等价：

- 同步版本号 `builtin_skill_version`。
- 同步示例命令、参数说明、强制规则。
- 同步反模式（anti-patterns）。
- 翻译只保留必要的术语统一（如"数字员工"）。

新增 skill 时双语必须同步落地。

## 8. 版本号

`builtin_skill_version` 是 skill 的语义版本号，落在 frontmatter 中。复刻或升级 skill 时：

- 改文档内容必须升 minor（如 1.0 → 1.1）。
- 改强制规则、参数 schema 必须升 major（1.x → 2.0）。
- 升版后双语两个文件都要同步。

## 9. 安全：技能扫描器（SkillScanner）

`security.skill_scanner` 在加载 SKILL.md 时进行内容审查。

| 模式 | 行为 |
|---|---|
| `block` | 扫描并阻止不安全 skill 加载 |
| `warn`（默认） | 仅记录警告日志，不阻止 |
| `off` | 完全禁用扫描 |

白名单：`SkillScannerWhitelistEntry(skill_name, content_hash)`，content_hash 为空表示该 skill 任何内容都放行。详见 [06-security.md](06-security.md)。

## 10. 凭据隐私（绝对约束）

任何 skill 文档不得包含：

- 真实账号、密码、API key、token、证书。
- 测试 / 演示用的"已脱敏但实际可用"的凭据。

凭据必须由用户在运行时通过：
- `config.json > plugins.<plugin_id>` 配置；或
- 浏览器有头模式手动登录。

skill 文档只描述"在哪里、如何让用户填入凭据"，不携带任何凭据本身。

## 11. 兼容性

- 从 legacy 单 agent 工作区迁移时，`migrate_legacy_skills_to_skill_pool()` 把旧 `active_skills/` 与 `customized_skills/` 合并到新 `skill.json` manifest。
- 新内置 skill 加入 skill_pool 后不会自动塞进已有 agent；用户必须从 UI 主动安装。

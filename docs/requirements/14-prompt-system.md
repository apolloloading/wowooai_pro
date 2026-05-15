# 14 — 提示词系统

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/prompt.py](../../src/wowooai/agents/prompt.py) · [src/wowooai/agents/md_files/](../../src/wowooai/agents/md_files/) · [src/wowooai/agents/context/compactor_prompts.py](../../src/wowooai/agents/context/compactor_prompts.py)

## 1. 系统提示来源

数字员工的 system prompt 由 workspace 里的 markdown 文件**按顺序拼接**而成。每个文件是独立的"提示词单元"，便于分开维护与覆盖。

## 2. 默认加载顺序

`agent.json > system_prompt_files` 默认：

```python
PromptConfig.system_prompt_files = [
    "AGENTS.md",
    "SOUL.md",
    "PROFILE.md",
]
```

加载方式（[prompt.py:42 `PromptBuilder`](../../src/wowooai/agents/prompt.py#L42)）：

1. 按顺序遍历列表；
2. 每个文件读 `<workspace>/<filename>`；
3. 拼接为 `# <filename>\n\n<content>`，多个之间用空行分隔；
4. 全部缺失则用 fallback default prompt。

## 3. 模板文件总览

模板源：[src/wowooai/agents/md_files/{zh,en}/](../../src/wowooai/agents/md_files/)。新建 agent 时按 `language` 复制到 `<workspace>/`。

| 文件 | 默认加载 | 内容 |
|---|---|---|
| `AGENTS.md` | ✅ | 工作流、规则、安全准则、心跳 / 记忆 section |
| `SOUL.md` | ✅ | 人格、核心准则、边界、风格 |
| `PROFILE.md` | ✅ | 身份（名字 / 定位 / 风格）+ 用户资料（用户填） |
| `BOOTSTRAP.md` | ❌（不在默认列表） | 启动检查项 / 一次性引导 |
| `HEARTBEAT.md` | — | 心跳触发时作为用户消息发给 agent（不进 system prompt） |
| `MEMORY.md` | — | 长期记忆（dream cron 写）；通过 memory prompt 注入 |

> `BOOTSTRAP.md` 默认不加载；用户可手动加进 `system_prompt_files` 让其生效（如复刻 Anthropic CLI 的 bootstrap 风格）。

## 4. 动态 section 注入

[prompt.py:106-196](../../src/wowooai/agents/prompt.py#L106) 在加载 `AGENTS.md` 时做两个特殊处理：

### 4.1 心跳 section

`heartbeat_enabled=False` 时把 `AGENTS.md` 中的"心跳指令"段过滤掉，避免给关闭心跳的 agent 灌"巡检群"等无用指令。

### 4.2 记忆 section

无论 `AGENTS.md` 里是否提到记忆，最终都会**追加** memory_manager 的标准记忆提示：

- `memory_manager.get_memory_prompt(language)` → 返回 `MEMORY_GUIDANCE_ZH` / `MEMORY_GUIDANCE_EN`（[memory/prompts.py](../../src/wowooai/agents/memory/prompts.py)）
- 内容：MEMORY.md 的写法约定、何时记 / 何时忘、四种 memory type（user / feedback / project / reference）

设计意图：让记忆指令的"事实部分"集中在一处维护，AGENTS.md 只放"骨架"。

## 5. PromptBuilder 接口

```python
PromptBuilder(
    working_dir,                # workspace 目录
    enabled_files,              # system_prompt_files 列表
    agent_id,                   # 注入到 prompt 头部，多 agent 互相区分
    heartbeat_enabled=False,
    language="zh",
    memory_manager=...,         # 用于拿 memory prompt
).build() -> str
```

调用方：[react_agent.py](../../src/wowooai/agents/react_agent.py) 在 agent 初始化时调一次，结果作为 ReActAgent 的 system message。

修改 markdown **不会热重载**；要让改动生效需重启 workspace（`MultiAgentManager.restart_workspace`）或重启后端。

## 6. AgentMdManager（前端读写接口）

[agent_md_manager.py](../../src/wowooai/agents/memory/agent_md_manager.py)

| 方法 | 用途 |
|---|---|
| `list_working_mds()` | 列出 workspace 根的 .md（AGENTS / SOUL / PROFILE / BOOTSTRAP / HEARTBEAT / MEMORY） |
| `read_working_md(name)` | 读单个 md |
| `write_working_md(name, content)` | 写单个 md |
| `list_memory_mds()` | 列 `<workspace>/memory/*.md`（每日记忆） |
| `read/write_memory_md` | 读写单个每日记忆 |

前端 `/agent/workspace` 页通过 `/api/agent/workspace/...` 走这些方法。

## 7. Compactor 提示词

[context/compactor_prompts.py](../../src/wowooai/agents/context/compactor_prompts.py) 定义上下文压缩用的 prompt：

- 触发条件、保留要点、忽略什么、输出格式（json schema）。
- 由 `LightContextManager._compact_context` 在压缩时调用。

详见 [15-context-compaction.md](15-context-compaction.md)。

## 8. Memory 提示词

[memory/prompts.py](../../src/wowooai/agents/memory/prompts.py)：

- `MEMORY_GUIDANCE_ZH` / `MEMORY_GUIDANCE_EN` — 注入到 system prompt 末尾，告诉 agent"什么该记"。
- `DREAM_PROMPT_ZH` / `DREAM_PROMPT_EN` — dream cron 把 daily logs 提炼到 MEMORY.md 时用的指令。

详见 [16-memory.md](16-memory.md)。

## 9. SKILL.md 不在 system prompt 中

技能正文**不会**默认拼到 system prompt——agent 通过工具 / 文件读 SKILL.md 按需加载，避免提示词膨胀。详见 [03-skills.md](03-skills.md)。

## 10. 占位符与变量

当前模板**不做模板引擎渲染**（不展开 `{{var}}`）：

- PROFILE.md 中的"挑个名字"是 markdown 内的提示文字，由用户手动填；
- 不做 jinja2 / mustache。

`agent_id` 由 PromptBuilder 单独拼到 prompt 头部，不通过模板变量。

## 11. 凭据隐私

任何模板（`md_files/zh/*.md` / `md_files/en/*.md`）**严禁**包含：

- 真实账号 / 密码 / API key / token；
- 测试 / 演示用的"已脱敏但可用"凭据；
- 用户工作区路径、用户机器名等可识别信息。

模板要保持"通用骨架 + 用户填写"风格。

## 12. 0.0.1 不做

- 不做模板变量渲染（`{{user}}` / `{{date}}` 等）。
- 不做 markdown 修改的热重载。
- 不做基于 token 预算的提示词自动裁剪（提示词由用户负责控制长度）。
- 不做提示词的 A/B 实验框架。

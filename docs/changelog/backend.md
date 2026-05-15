# 后端改造说明

> 本文面向一份**干净的原 copaw 后端源码**：只记录本轮需要复刻的后端变更。除本文列出的 §1 / §5 / §8 外，其他后端模块不要调整。
>
> 完整目标源码以 [source-bundle/](source-bundle/) 为准；涉及大文件时，优先从 source-bundle 按同路径复制。

---

## 目录

> **编号说明**：本文沿用历史编号（§1 → §30）。原始记录中存在跨日期同号情况（§12 / §13 / §14 各出现两次），为保持外部交叉引用稳定，**未做编号调整**。同号节点在标题中已带日期区分，TOC 也按主题与时间双维度索引。§2、§3、§4、§6、§7、§15–§19、§28 在原始记录中未使用。

### 一、项目元数据与基础工具（§1、§5、§8、§9）
- [§1 项目元数据 / 重命名](#1-项目元数据--重命名)
- [§5 内置工具：renliwo_browser](#5-内置工具renliwo_browser)
- [§8 文件修改沙箱（写入 / 编辑 / 覆盖原始文件）](#8-文件修改沙箱写入--编辑--覆盖原始文件)
- [§9 工具执行安全审批级别](#9-工具执行安全审批级别)
- [启动联调补齐项](#启动联调补齐项)

### 二、2026-04-30 实际落地复刻顺序与默认数字员工（§10–§14、§20）
- [§10 2026-04-30 实际落地复刻顺序（后端）](#10-2026-04-30-实际落地复刻顺序后端)
- [§11 2026-04-30 增量：Cron 默认执行超时 120s → 1200s](#11-2026-04-30-增量cron-默认执行超时-120s--1200s)
- [§12 2026-04-30 增量：默认数字员工标识确认](#12-2026-04-30-增量默认数字员工标识确认)
- [§13 2026-04-30 增量：受保护用户目录扩展（Desktop / Documents / Downloads）](#13-2026-04-30-增量受保护用户目录扩展desktop--documents--downloads)
- [§14 2026-04-30 增量：本机启动规范固化](#14-2026-04-30-增量本机启动规范固化)
- [§20 2026-04-30 增量：默认 agent 名称 / 描述 / 工作区 MD 兜底](#20-2026-04-30-增量默认-agent-名称--描述--工作区-md-兜底)

### 三、2026-05-03 默认数字员工技能预装与 fresh-install 修复（§21–§23）
- [§21 2026-05-03 增量：默认数字员工首次预装精选技能](#21-2026-05-03-增量默认数字员工首次预装精选技能)
- [§22 2026-05-03 修复：全新安装误触发 legacy migration 导致 default 技能为空](#22-2026-05-03-修复全新安装误触发-legacy-migration-导致-default-技能为空)
- [§23 2026-05-03 修复：CLI 启动先写 `last_api` 时仍应跳过 fresh install legacy migration](#23-2026-05-03-修复cli-启动先写-last_api-时仍应跳过-fresh-install-legacy-migration)

### 四、2026-05-04 桌面打包、MCP、副本沙箱收敛、文件下载（§24–§27）
- [§24 2026-05-04 增量：桌面打包依赖与 launcher 孤儿进程兜底](#24-2026-05-04-增量桌面打包依赖与-launcher-孤儿进程兜底)
- [§25 2026-05-04 修复：MCP 已连接但对话运行时未注册到 Toolkit](#25-2026-05-04-修复mcp-已连接但对话运行时未注册到-toolkit)
- [§26 2026-05-04 收敛：副本沙箱只覆盖文件修改，不特殊拦截删除](#26-2026-05-04-收敛副本沙箱只覆盖文件修改不特殊拦截删除)
- [§27 2026-05-04 修复：`send_file_to_user` 改用同源 HTTP URL，恢复客户端文件下载](#27-2026-05-04-修复send_file_to_user-改用同源-http-url恢复客户端文件下载)

### 五、Cron 相关（§11、§12.1、§13-2026-05-05）
- [§11 Cron 默认执行超时 120s → 1200s](#11-2026-04-30-增量cron-默认执行超时-120s--1200s)
- [§12.1 2026-05-04 修复：CLI 创建 cron job 默认超时 120s → 1200s](#121-2026-05-04-修复cli-创建-cron-job-默认超时-120s--1200s)
- [§13 2026-05-05 Cron SKILL.md v2.1 完整内容（可复用参考）](#13-2026-05-05-cron-skillmd-v21-完整内容可复用参考)

### 六、桌面端文件下载（§14-2026-05-05）
- [§14 2026-05-05 修复：桌面端文件下载保存对话框无文件后缀（Windows/macOS）](#14-2026-05-05-修复桌面端文件下载保存对话框无文件后缀windowsmacos)

### 七、2026-05-06 性能优化（暂无）

### 八、2026-05-07 桌面依赖打包（§31）
- [§31 内置 pandoc 即开即用（pypandoc-binary + PATH 注入）](#31-2026-05-07-增量内置-pandoc-即开即用pypandoc-binary--path-注入)

### 九、2026-05-09 记忆系统修复（§32）
- [§32 默认开启 auto_memory_interval，修复记忆系统空转](#32-2026-05-09-修复默认开启-auto_memory_interval修复记忆系统空转)

### 十、2026-05-12 桌面应用控制能力（§33）
- [§33 新增 desktop_input / desktop_app 工具与 desktop_control 内置 skill](#33-2026-05-12-增量新增-desktop_input--desktop_app-工具与-desktop_control-内置-skill)

### 十一、2026-05-14 renliwo_browser 多站点改造（§34）
- [§34 renliwo_browser 多站点适配：新增 qd_system，host 前缀通配自动路由](#34-2026-05-14-增量renliwo_browser-多站点适配新增-qd_systemhost-前缀通配自动路由)

### 十二、2026-05-14 浏览器默认有头模式与登录隐私安全（§35）
- [§35 browser_use / renliwo_browser 默认有头模式 + 登录交给用户](#35-2026-05-14-增量browser_use--renliwo_browser-默认有头模式--登录交给用户)

### 十三、2026-05-14 macOS Dock 图标修复（§36）
- [§36 macOS Dock 图标错误显示为通用 "exec" 图标（desktop_cmd.py 平台分流）](#36-2026-05-14-修复macos-dock-图标错误显示为通用-exec-图标desktop_cmdpy-平台分流)

### 十四、2026-05-14 agent-browser 高级浏览器能力（§37）
- [§37 集成 agent-browser 高级浏览器能力（npx 外挂 + 三浏览器共享 CDP）](#37-2026-05-14-增量集成-agent-browser-高级浏览器能力npx-外挂--三浏览器共享-cdp)

### 十五、2026-05-14 tool_result 截断阈值放宽（§38）
- [§38 tool_result 截断阈值放宽（中文多步工具链不再被压扁）](#38-2026-05-14-调优tool_result-截断阈值放宽中文多步工具链不再被压扁)

---

## §1 项目元数据 / 重命名

### 1.1 包名、CLI 命令与残留标识统一改为 `wowooai`

**目的**：把原源码中的 `qwenpaw` 和 `copaw` 全部统一为 `wowooai`。无论原字符串大小写如何（如 `QwenPaw` / `CoPaw` / `COPAW` / `qwenpaw`），本轮都按目标场景替换为 `wowooai`（代码包名、import、CLI、配置键、路径、元数据均使用小写）。

**关键改造**：
- 目录：`src/qwenpaw/**` 或 `src/copaw/**` → `src/wowooai/**`
- import：全工程 `qwenpaw` / `copaw`（大小写不敏感）→ `wowooai`
- 项目元数据：`pyproject.toml` 的 `[project].name` / `[project.scripts]` / `[tool.setuptools.dynamic].version` 全部指向 `wowooai`
- 包数据：`[tool.setuptools.package-data]` 使用 `"wowooai"`
- 版本文件：`src/wowooai/__version__.py` 重置为新版本号

**关键文件**：
- `pyproject.toml`
- `src/wowooai/__version__.py`
- `src/wowooai/**`（由 `src/qwenpaw/**` 或 `src/copaw/**` 整体重命名而来）

**建议替换方式**：

```bash
# 先改目录名；如果两个旧目录同时存在，先人工合并后只保留 src/wowooai
mv src/qwenpaw src/wowooai 2>/dev/null || true
mv src/copaw src/wowooai 2>/dev/null || true

# 文本层面对 qwenpaw / copaw 做大小写不敏感替换
python - <<'PY'
from pathlib import Path
import re

roots = [Path('pyproject.toml'), Path('setup.py'), Path('src'), Path('tests'), Path('scripts')]
patterns = [re.compile(r'qwenpaw', re.I), re.compile(r'copaw', re.I)]
for root in roots:
    paths = [root] if root.is_file() else root.rglob('*') if root.exists() else []
    for path in paths:
        if not path.is_file() or path.suffix in {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.db'}:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new_text = text
        for pattern in patterns:
            new_text = pattern.sub('wowooai', new_text)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
PY
```

**`pyproject.toml` 关键字段**：

```toml
[project]
name = "wowooai"
dynamic = ["version"]
requires-python = ">=3.10,<3.14"

[tool.setuptools.dynamic]
version = {attr = "wowooai.__version__.__version__"}

[tool.setuptools]
packages = { find = { where = ["src"] } }
include-package-data = true

[tool.setuptools.package-data]
"wowooai" = [
    "console/**",
    "agents/md_files/**",
    "agents/skills/**",
    "tokenizer/**",
    "security/tool_guard/rules/**",
    "security/skill_scanner/rules/**",
    "security/skill_scanner/data/**",
]

[project.scripts]
wowooai = "wowooai.cli.main:cli"
```

**`src/wowooai/__version__.py`**：

```python
__version__ = "0.0.1"
```

**复刻校验**：

```bash
python -c "import wowooai; print(wowooai.__version__.__version__)"
# 期望：0.0.1

python -m wowooai --help | head -3
# 期望：能看到 wowooai CLI 帮助

grep -RniE 'qwenpaw|copaw' pyproject.toml setup.py src tests scripts 2>/dev/null || true
# 期望：无输出
```

---

## §5 内置工具：renliwo_browser

**目的**：把人力沃流程的浏览器自动化动作封装为内置工具 `renliwo_browser`，用于登录、导出、按合同号筛选等 Renliwo 相关操作。Renliwo 页面结构手册由工具自身自动加载，不再依赖单独安装 / 启用 `renliwo_browser` skill。

**完整源码按 source-bundle 复制后即为最终形态**：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser.py \
   src/wowooai/agents/tools/renliwo_browser.py

# 页面结构手册数据属于工具包，不再放在 skills/renliwo_browser 下。
mkdir -p src/wowooai/agents/tools/renliwo_browser_data
cp docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json \
   src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json
cp docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md \
   src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md

# 终极方案：不要保留 renliwo_browser skill，避免依赖技能启用状态。
rm -rf src/wowooai/agents/skills/renliwo_browser
```

**新文件清单**：
- `src/wowooai/agents/tools/renliwo_browser.py`
- `src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md`
- `src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json`

**不再需要的文件**：
- `src/wowooai/agents/skills/renliwo_browser/SKILL.md`
- `src/wowooai/agents/skills/renliwo_browser/data/**`

**注册路径**：

`src/wowooai/agents/tools/__init__.py`：

```python
from .renliwo_browser import renliwo_browser
```

`src/wowooai/config/config.py` 的 `_default_builtin_tools()`：

```python
"renliwo_browser": BuiltinToolConfig(
    name="renliwo_browser",
    enabled=True,
    description="Renliwo HR browser automation (login, export, filter)",
    icon="🧑‍💼",
),
```

`src/wowooai/agents/react_agent.py` 的 `tool_functions` 字典：

```python
"renliwo_browser": renliwo_browser,
```

**工具内置页面手册要求**：

`src/wowooai/agents/tools/renliwo_browser.py` 必须从工具数据目录加载索引：

```python
Path(__file__).parent / "renliwo_browser_data" / "renliwo_guide_index.json"
```

工具 import 时只加载 `renliwo_guide_index.json` 到内存，不读取完整 Markdown。进入具体页面时根据当前 URL hash 查询 compact guide，并在返回值中附带：

```json
"guide": {
  "module": "...",
  "page_name": "...",
  "route": "#/...",
  "tabs": [],
  "export_mode": "direct_download",
  "export_buttons": [],
  "all_buttons": [],
  "select_fields": {},
  "filter_count": 0,
  "notes": [],
  "doc_ref": ".../Renliwo页面结构文档_完整版.md",
  "guide_version": "..."
}
```

必须存在显式手册查询 action：

```python
action="guide"
```

行为：
- 未传 `url` 时，按当前 `page_id` 的当前页面 URL 查 guide。
- 传完整 Renliwo URL 或 `#/route` 时，按该路由查 guide。
- 未命中时返回 route summary 和完整文档 `doc_ref`，不把完整 Markdown 自动塞进上下文。

自动附带 guide 的时机：
- `action="login"` 登录成功后。
- `action="nav_submenu", is_leaf=True` 进入叶子业务页面后。
- `action="export"` 导出成功后。

`pyproject.toml` 包数据必须包含工具手册目录：

```toml
[tool.setuptools.package-data]
"wowooai" = [
    "agents/skills/**",
    "agents/tools/renliwo_browser_data/**",
]
```

**复刻校验**：

```bash
python -m py_compile src/wowooai/agents/tools/renliwo_browser.py

test -f src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json
test -f src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md
test ! -d src/wowooai/agents/skills/renliwo_browser

grep -n "action == \"guide\"\|renliwo_browser_data\|_guide_for_current_page" \
  src/wowooai/agents/tools/renliwo_browser.py

grep -n 'agents/tools/renliwo_browser_data/\*\*' pyproject.toml

python - <<'PY'
from wowooai.agents.tools.renliwo_browser import _guide_for_route
print(bool(_guide_for_route('#/exportCenter/asyncExportList')))
PY
# 期望：True

curl -fsS http://127.0.0.1:8088/api/tools | jq '.[] | select(.name=="renliwo_browser")'
# 期望：返回工具元数据
```

---

## §9 工具执行安全审批级别

> 配套前端 [frontend.md §8](frontend.md#8-工具执行安全独立页)。前端通过 `agentsApi.getAgent/updateAgent` 读写当前数字员工 profile 的 `approval_level`，后端必须持久化该字段，并在工具执行前按级别调整审批策略。

### 9.1 AgentProfileConfig 新增字段

**文件**：`src/wowooai/config/config.py`

在 `AgentProfileConfig` 中、`language` 后新增：

```python
approval_level: str = Field(
    default="AUTO",
    description=(
        "Tool execution security level: "
        "STRICT (all tools need approval), "
        "SMART (low-risk auto-allowed), "
        "AUTO (only guarded tools), "
        "OFF (guard disabled)"
    ),
)
```

效果：

- `GET /api/agents/{agentId}` 返回 `approval_level`。
- `PUT /api/agents/{agentId}` 的 `AgentProfileConfig` 不再丢弃该字段，`save_agent_config()` 会写回 agent 的 `agent.json`。
- 旧 agent 配置未包含该字段时自动使用默认值 `AUTO`。

### 9.2 ToolGuardMixin 按审批级别生效

**文件**：`src/wowooai/agents/tool_guard_mixin.py`

`_decide_guard_action()` 从当前 agent 配置读取：

```python
approval_level = str(
    getattr(self._agent_config, "approval_level", "AUTO") or "AUTO",
).upper()
```

四档行为：

| 值 | 行为 |
|---|---|
| `OFF` | 直接跳过 tool guard，所有工具按原流程执行 |
| `STRICT` | 所有工具调用都视为需要审批；批准后再执行 |
| `SMART` | 低风险（`LOW` / `INFO`）发现自动放行，中高风险进入审批 |
| `AUTO` | 保持原默认逻辑：仅 guarded tools 执行完整规则；非 guarded tools 只跑 always-run guardian（如文件防护） |

`denied_tools` 仍优先于上述级别：只要工具命中禁止列表，仍自动拦截且不可审批。

### 9.3 校验

```bash
python -m py_compile \
  src/wowooai/config/config.py \
  src/wowooai/agents/tool_guard_mixin.py

grep -n 'approval_level' src/wowooai/config/config.py \
  src/wowooai/agents/tool_guard_mixin.py
```

运行后可通过前端"安全防护"页面保存任一模式，再检查对应 workspace 的 `agent.json` 是否出现：

```json
"approval_level": "STRICT"
```

---

## §8 文件修改沙箱（写入 / 编辑 / 覆盖原始文件）

**目的**：写入、编辑、覆盖用户原始文件（如 Desktop、Documents、Downloads 下的文件）时，默认不原地覆盖；必须在工作区沙箱中写到 `_副本`，避免误改用户原文件。删除类操作不作为副本沙箱规则的一部分，只按普通风险操作处理。

**完整源码按 source-bundle 复制**：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/tools/file_io.py \
   src/wowooai/agents/tools/file_io.py
cp docs/changelog/source-bundle/src/wowooai/agents/tools/shell.py \
   src/wowooai/agents/tools/shell.py
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/zh/AGENTS.md \
   src/wowooai/agents/md_files/zh/AGENTS.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/en/AGENTS.md \
   src/wowooai/agents/md_files/en/AGENTS.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/zh/SOUL.md \
   src/wowooai/agents/md_files/zh/SOUL.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/en/SOUL.md \
   src/wowooai/agents/md_files/en/SOUL.md
```

**必须同时生效的三层约束**：
1. 提示词层：`AGENTS.md` / `SOUL.md` 写明写入、编辑、覆盖原始文件时需在工作区沙箱中写到 `_副本`，删除类操作不属于副本沙箱规则。
2. 文件工具层：`file_io.py` 的 `_sandbox_copy_for_write` 把工作区外写入重定向到 workspace `.sandbox/input/` 下的 `_副本` 文件。
3. Shell 工具层：`shell.py` 的 `_check_destructive_command` 拦截可绕过文件工具的写入、编辑、覆盖命令；`rm` / `rmdir` / `unlink` 等删除类命令不因副本沙箱规则被特殊拦截。

### 8.1 SOUL.md 沙箱准则

**文件**：`src/wowooai/agents/md_files/zh/SOUL.md` 与 `en/SOUL.md`

**zh 关键内容**：

```markdown
## 文件修改沙箱准则

写入、编辑、覆盖用户原始文件（如桌面、Documents、Downloads）时：
1. 不要原地覆盖；先在工作区沙箱中写到 `<原名>_副本.<后缀>`
2. shell 工具只按副本沙箱拦截写入、编辑、覆盖类命令
3. 删除类操作不作为副本沙箱规则的一部分，只按普通风险操作处理
4. 例外：用户在当次会话明确说“原地修改 / 覆盖原文件”才允许覆盖
```

### 8.2 `tools/file_io.py` 沙箱写入

**关键函数**：

```python
def _is_outside_workspace(path: Path) -> bool:
    workspace = _current_workspace_dir()
    try:
        path.resolve().relative_to(workspace.resolve())
        return False
    except ValueError:
        return True


def _copy_suffix_name(path: Path) -> str:
    if "_副本" in path.name:
        return path.name
    return f"{path.stem}_副本{path.suffix}"


def _sandbox_copy_for_write(resolved_path: str) -> str:
    workspace = get_current_workspace_dir()
    if workspace is None:
        return resolved_path
    if not _is_outside_workspace(resolved_path, workspace):
        return resolved_path

    sandbox_dir = Path(workspace) / ".sandbox" / "input"
    sandbox_dir.mkdir(parents=True, exist_ok=True)
    redirected = sandbox_dir / _copy_suffix_name(Path(resolved_path).expanduser())
    if not redirected.exists() and os.path.isfile(resolved_path):
        shutil.copy2(resolved_path, redirected)
    return str(redirected)
```

`write_file` / `edit_file` / `append_file` 等写入入口都必须在写之前经过 `_sandbox_copy_for_write`。

### 8.3 `tools/shell.py` 文件修改命令拦截

**必须覆盖的绕过路径**：

```python
_IN_PLACE_MODIFY_BINARIES = {"mv", "dd", "shred", "truncate"}
_WRITE_TARGET_BINARIES = {"tee", "cp", "install", "ln", "rsync", "touch", "chmod", "chown"}
_EDITOR_BINARIES = {"vim", "vi", "nano", "emacs", "ed", "code", "subl", "open"}
_INLINE_EDIT_FLAGS = {
    "sed":  ("-i", "--in-place"),
    "perl": ("-i",),
    "ruby": ("-i",),
    "gawk": ("-i",),
    "awk":  ("-i",),
}
_INTERPRETERS = {"python", "python3", "node", "ruby", "perl"}
_INTERPRETER_INLINE_FLAGS = {"-c", "-e", "-p", "-pe", "-ne"}
_REDIRECT_RE = re.compile(r"(?:^|\s)(?:&|[12])?>{1,2}\s*([^\s|;&<>]+)")
```

**关键行为**：`_check_destructive_command(command)` 要检查命令分段、写入目标参数、编辑器参数、inline edit flag、解释器 inline payload、重定向目标；只要目标疑似 Desktop / Documents / Downloads 下的原始文件，就拒绝执行。删除类命令（如 `rm`、`rmdir`、`unlink`）不属于副本沙箱拦截范围。

### 8.4 `migration.py` 取自上游 QwenPaw 原始版本

**文件**：`src/wowooai/app/migration.py`、`src/wowooai/agents/templates.py`

`migration.py` 直接采用上游 QwenPaw `main` 分支原始内容，不再二次重写：

```bash
# 通过代理 7897 拉取，避免本地分支飘逸
curl -s --proxy http://127.0.0.1:7897 \
  https://raw.githubusercontent.com/agentscope-ai/QwenPaw/main/src/qwenpaw/app/migration.py \
  -o src/wowooai/app/migration.py
curl -s --proxy http://127.0.0.1:7897 \
  https://raw.githubusercontent.com/agentscope-ai/QwenPaw/main/src/qwenpaw/agents/templates.py \
  -o src/wowooai/agents/templates.py
# 文本层把 QwenPaw / qwenpaw / QWENPAW_ 替换为 wowooai 系列
```

为让原始 `migration.py` 与 `templates.py` 能成功 import，需要补齐它们引用、但仓库当前缺失的下列符号：

| 文件 | 新增内容 |
|---|---|
| `src/wowooai/constant.py` | 常量 `LEGACY_QA_AGENT_ID = "CoPaw_QA_Agent_0.1beta1"`，用于在新内置 QA 创建时禁用旧版 |
| `src/wowooai/config/config.py` | 新增 `build_local_agent_tools_config()`，与上游同义，给本地协作 agent 用 |
| `src/wowooai/app/routers/agents.py` | `_initialize_agent_workspace` 增加 `md_template_id: str \| None = None` 形参；当 `md_template_id == "qa"` 时把 `builtin_qa_md_seed` 置 `True`，行为兼容上游 QA 模板初始化 |

启动后默认 agent 列表只有：
- `default`：迁移 / 初始化生成的默认 agent
- `WowooAI_QA_Agent_0.1beta1`：内置 QA agent

不会出现额外的 `wowooai` agent。

**复刻校验**：

```bash
python -m py_compile \
  src/wowooai/agents/tools/file_io.py \
  src/wowooai/agents/tools/shell.py \
  src/wowooai/app/migration.py

grep -n "def _sandbox_copy_for_write" src/wowooai/agents/tools/file_io.py
grep -n "def _check_destructive_command" src/wowooai/agents/tools/shell.py

grep -E "_IN_PLACE_MODIFY_BINARIES|_WRITE_TARGET_BINARIES|_EDITOR_BINARIES|_INLINE_EDIT_FLAGS|_INTERPRETERS" \
  src/wowooai/agents/tools/shell.py | wc -l
# 期望：≥ 5

python -m wowooai app --port 8088 &
sleep 5
ls ~/.wowooai/workspaces/default/*.md
grep -l "_副本" ~/.wowooai/workspaces/default/SOUL.md
```

---

## 启动联调补齐项

### 1. `shell.py` 依赖 `get_current_shell_command_timeout`

`src/wowooai/agents/tools/shell.py` 使用 shell command timeout context，因此 `src/wowooai/config/context.py` 同步补齐：

```python
current_shell_command_timeout: ContextVar[float | None]
get_current_shell_command_timeout()
set_current_shell_command_timeout(timeout: float | None)
```

### 2. `migration.py` 依赖补齐

`app/migration.py` 与 `agents/templates.py` 采用上游 QwenPaw 原始内容并做品牌字符串替换；同时补齐它们需要的依赖：

1. `constant.py` 新增 `LEGACY_QA_AGENT_ID`。
2. `config/config.py` 新增 `build_local_agent_tools_config()`。
3. `app/routers/agents.py` 的 `_initialize_agent_workspace` 增加 `md_template_id: str | None = None` 形参；当 `md_template_id == "qa"` 时启用 QA markdown seed。

---

## §10 2026-04-30 实际落地复刻顺序（后端）

> 本节把 `applied-2026-04-30.md` 中的后端实际落地内容合并到 backend changelog。以后复刻时不需要再看 applied 文件，按本节顺序执行即可。

### §10.1 从干净上游源码开始

前置假设：根目录是 `/Users/rlw/AI项目/wowooai/`，原始包名可能是 `qwenpaw` 或 `copaw`，后端根目录不是 git 仓库。

```bash
cd /Users/rlw/AI项目/wowooai
```

复刻时不要修改 `docs/changelog/**`、`.git`、`node_modules`、`console/dist`、`__pycache__` 等说明/构建/缓存目录。

### §10.2 包重命名 `qwenpaw / copaw → wowooai`

```bash
cd /Users/rlw/AI项目/wowooai

# 目录重命名：按实际存在的目录执行
if [ -d src/qwenpaw ] && [ ! -d src/wowooai ]; then mv src/qwenpaw src/wowooai; fi
if [ -d src/copaw ] && [ ! -d src/wowooai ]; then mv src/copaw src/wowooai; fi
```

文本替换脚本（排除 changelog 与构建缓存，避免污染复刻说明）：

```bash
python - <<'PY'
from pathlib import Path
import re

roots = [
    Path('pyproject.toml'),
    Path('setup.py'),
    Path('src'),
    Path('tests'),
    Path('scripts'),
    Path('Makefile'),
]
skip_parts = {
    'docs', '.git', 'node_modules', 'dist', '__pycache__', '.venv',
    'client', '.mypy_cache', '.pytest_cache', '.ruff_cache',
}
binary_suffixes = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.db', '.sqlite',
    '.woff', '.woff2', '.ttf', '.otf', '.pyc', '.zip', '.tar', '.gz',
}
patterns = [re.compile(r'qwenpaw', re.I), re.compile(r'copaw', re.I)]

for root in roots:
    if not root.exists():
        continue
    paths = [root] if root.is_file() else root.rglob('*')
    for path in paths:
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.suffix.lower() in binary_suffixes:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new_text = text
        for pattern in patterns:
            new_text = pattern.sub('wowooai', new_text)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
PY
```

`pyproject.toml` 必须确认如下关键字段：

```toml
[project]
name = "wowooai"
dynamic = ["version"]

[project.scripts]
wowooai = "wowooai.cli.main:cli"

[tool.setuptools.dynamic]
version = {attr = "wowooai.__version__.__version__"}

[tool.setuptools.package-data]
"wowooai" = [
    "console/**",
    "agents/md_files/**",
    "agents/skills/**",
    "tokenizer/**",
    "security/tool_guard/rules/**",
    "security/skill_scanner/rules/**",
    "security/skill_scanner/data/**",
]
```

`src/wowooai/__version__.py` 重置：

```python
__version__ = "0.0.1"
```

### §10.3 落地 `renliwo_browser` 内置工具与页面手册

从 source-bundle 复制工具源码，并把 Renliwo 页面结构手册放入工具包数据目录；不再安装 / 保留 `renliwo_browser` skill：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser.py \
   src/wowooai/agents/tools/renliwo_browser.py

mkdir -p src/wowooai/agents/tools/renliwo_browser_data
cp docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json \
   src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json
cp docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md \
   src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md

rm -rf src/wowooai/agents/skills/renliwo_browser
```

注册点必须包含：

```python
# src/wowooai/agents/tools/__init__.py
from .renliwo_browser import renliwo_browser
```

```python
# src/wowooai/config/config.py 的 _default_builtin_tools()
"renliwo_browser": BuiltinToolConfig(
    name="renliwo_browser",
    enabled=True,
    description="Renliwo HR browser automation (login, export, filter)",
    icon="🧑‍💼",
),
```

```python
# src/wowooai/agents/react_agent.py 的 tool_functions 字典
"renliwo_browser": renliwo_browser,
```

`pyproject.toml` 包数据必须包含工具手册目录：

```toml
"agents/tools/renliwo_browser_data/**",
```

工具必须支持：

- import 时只加载 `renliwo_guide_index.json`，不自动读取完整 Markdown。
- `action="guide"`：按当前页面、完整 Renliwo URL 或 `#/route` 返回 compact guide。
- 登录成功、进入叶子业务页面、导出成功后自动在返回值附带 `guide`。
- 未命中页面时返回 route summary 与完整文档 `doc_ref`。

校验：

```bash
python -m py_compile src/wowooai/agents/tools/renliwo_browser.py

test -f src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json
test -f src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md
test ! -d src/wowooai/agents/skills/renliwo_browser

grep -n "action == \"guide\"\|renliwo_browser_data\|_guide_for_current_page" \
  src/wowooai/agents/tools/renliwo_browser.py
grep -n 'agents/tools/renliwo_browser_data/\*\*' pyproject.toml
```

### §10.4 落地沙箱三层约束

复制 source-bundle 的权威实现：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/tools/file_io.py \
   src/wowooai/agents/tools/file_io.py
cp docs/changelog/source-bundle/src/wowooai/agents/tools/shell.py \
   src/wowooai/agents/tools/shell.py
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/zh/SOUL.md \
   src/wowooai/agents/md_files/zh/SOUL.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/en/SOUL.md \
   src/wowooai/agents/md_files/en/SOUL.md
```

必须存在的符号：

```bash
grep -n "def _sandbox_copy_for_write\|def _is_outside_workspace" src/wowooai/agents/tools/file_io.py
grep -n "_IN_PLACE_MODIFY_BINARIES\|def _check_destructive_command" src/wowooai/agents/tools/shell.py
grep -n "副本\|sandbox\|Desktop" src/wowooai/agents/md_files/zh/SOUL.md src/wowooai/agents/md_files/en/SOUL.md
```

### §10.5 后端完整校验

```bash
cd /Users/rlw/AI项目/wowooai

python -m py_compile $(find src/wowooai -name '*.py')
python -c "import wowooai; print(wowooai.__version__.__version__)"
# 期望：0.0.1

python -m wowooai --help | head -3
# 期望：能看到 wowooai CLI 帮助

grep -RniE 'qwenpaw|copaw' pyproject.toml setup.py src tests scripts 2>/dev/null
# 期望：无输出

python - <<'PY'
from wowooai.agents.tools import renliwo_browser
from wowooai.agents.tools import file_io, shell
print(callable(renliwo_browser))
print(hasattr(file_io, '_sandbox_copy_for_write'))
print(hasattr(shell, '_check_destructive_command'))
PY
# 期望：三行 True
```

运行联调：

```bash
/Users/rlw/AI项目/wowooai/client/bundled-venv/bin/python3 \
  -m wowooai app --host 127.0.0.1 --port 8088

curl -sS http://127.0.0.1:8088/api/version
# 期望：{"version":"0.0.1"}
```

---

## §11 2026-04-30 增量：Cron 默认执行超时 120s → 1200s

> 本节记录定时任务默认 runtime 超时的前后端同步改动。目的：避免较长任务在默认 120 秒时被 cron runner 提前中断。

### §11.1 后端默认值

**文件**：`src/wowooai/app/crons/models.py`

定位：`JobRuntimeSpec`：

```python
class JobRuntimeSpec(BaseModel):
    max_concurrency: int = Field(default=1, ge=1)
    timeout_seconds: int = Field(default=1200, ge=1)
    misfire_grace_seconds: int = Field(default=60, ge=0)
```

关键点：

- 只调整 `timeout_seconds` 默认值：`120` → `1200`。
- `ge=1` 校验不变。
- 已存在任务若显式保存了 `runtime.timeout_seconds`，仍以任务配置为准；该改动只影响新建 / 默认 runtime。

### §11.2 配套前端默认值

前端位置详见 [frontend.md](frontend.md) §18。

**文件**：`console/src/pages/Control/CronJobs/components/constants.ts`

```ts
runtime: {
  max_concurrency: 1,
  timeout_seconds: 1200,
  misfire_grace_seconds: 60,
},
```

### §11.3 复刻校验

```bash
grep -n 'timeout_seconds: int = Field(default=1200' \
  src/wowooai/app/crons/models.py

grep -n 'timeout_seconds: 1200' \
  console/src/pages/Control/CronJobs/components/constants.ts

python -m py_compile src/wowooai/app/crons/models.py
```

---

## §12.1 2026-05-04 修复：CLI 创建 cron job 默认超时 120s → 1200s

### 现象

通过 `wowooai cron create` CLI 命令创建的 agent 类型定时任务，运行约 2 分钟后被取消（`CancelledError`），即使 job spec 中未显式指定 `timeout_seconds`。

### 根因

CLI 的 `_build_spec_from_cli` 函数中 `runtime.timeout_seconds` 硬编码为 `120`：

```python
# src/wowooai/cli/cron_cmd.py:146-150
runtime = {
    "max_concurrency": 1,
    "timeout_seconds": 120,    # ← 只有 120 秒
    "misfire_grace_seconds": 60,
}
```

而 `JobRuntimeSpec` 模型默认值已经是 `1200`，前端 UI 的 `constants.ts` 也已是 `1200`，但 CLI 创建路径没有对齐。

实际写入 `jobs.json` 后，executor 在 `_execute_once` 中使用 `job.runtime.timeout_seconds` 作为 `asyncio.wait_for` 的超时值，120 秒一到就触发 `TimeoutError`。

### 修复

**文件**：`src/wowooai/cli/cron_cmd.py`，第 148 行：

```python
    runtime = {
        "max_concurrency": 1,
        "timeout_seconds": 1200,   # 改为 1200 秒（20 分钟）
        "misfire_grace_seconds": 60,
    }
```

### 已修复存量数据

通过直接修改 `~/.wowooai/workspaces/*/jobs.json`，将已存在且 `timeout_seconds=120` 的 job 更新为 `1200`：

```
Updated: /Users/rlw/.wowooai/workspaces/default/jobs.json
  - Daily Water Reminder: 120 → 1200
  - Daily Contract Report Processing: 120 → 1200
```

### 验证

```bash
grep -n 'timeout_seconds.*1200' src/wowooai/cli/cron_cmd.py
# 期望输出: 148:        "timeout_seconds": 1200,

grep -n 'timeout_seconds: int = Field(default=1200' \
  src/wowooai/app/crons/models.py
# 期望输出: 106:    timeout_seconds: int = Field(default=1200, ge=1)

grep -n 'timeout_seconds: 1200' \
  console/src/pages/Control/CronJobs/components/constants.ts
# 期望输出: 30:    timeout_seconds: 1200,
```

---

## §14 2026-05-05 修复：桌面端文件下载保存对话框无文件后缀（Windows/macOS）

### 现象

桌面客户端中点击文件下载图标后，弹出系统保存对话框时文件名可能缺少后缀（如 `关联数据` 而非 `关联数据.xlsx`），尤其在 Windows 上导致保存的文件无法用正确应用打开。

### 根因

`save_file` 的 `filename` 参数来自前端 `window.open` 拦截器中从 URL 路径段解码得到的文件名。虽然正常链路下后缀不会丢失，但 Windows 的 `create_file_dialog` 不会自动推断后缀——一旦 `filename` 中无后缀，保存的文件就是无后缀的裸文件。

### 修复

**文件**：`src/wowooai/cli/desktop_cmd.py`，`save_file` 方法内，第 64 行之后。

在 `safe_name` 计算后，增加后缀兜底逻辑：

```python
if "." not in safe_name:
    import mimetypes
    # Try extracting extension from URL path segment
    url_path = url.split("?")[0]
    url_name = url_path.split("/")[-1]
    if "." in url_name:
        ext = url_name.rsplit(".", 1)[-1]
        if ext and 1 <= len(ext) <= 10:
            safe_name = f"{safe_name}.{ext}"
    # Fallback: infer from Content-Type header
    if "." not in safe_name:
        try:
            with urllib.request.urlopen(url) as resp:
                ct = resp.headers.get("Content-Type", "")
                ext = mimetypes.guess_extension(ct)
                if ext:
                    safe_name = f"{safe_name}{ext}"
        except Exception:
            pass
```

### 效果

| 场景 | 行为 |
|---|---|
| `safe_name` 已有后缀 | 跳过兜底，直接用 |
| `safe_name` 无后缀，URL 路径段有 | 从 URL 提取（如 `.xlsx`） |
| 都无后缀 | 从 HTTP Content-Type 推断（如 `.xls`） |
| 都无 | 保持原样（极罕见） |

### 验证

```bash
python -c "
from urllib.parse import quote
# 正常路径：后缀存在
url = '/api/files/preview/Users/rlw/Desktop/%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE.xlsx'
print(url.split('/')[-1])  # → %E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE.xlsx
"
```

---

## §13 2026-05-05 Cron SKILL.md v2.1 完整内容（可复用参考）

> 以下完整记录 v2.1 版本的 cron-zh SKILL.md 内容，复刻项目时可直接复制使用。

<details>
<summary>点击展开 cron-zh/SKILL.md v2.1 完整内容</summary>

```markdown
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
```

</details>

---

## §12 2026-04-30 增量：默认数字员工标识确认

> 本节记录本轮确认的默认数字员工初始化结果。该项与 §8.4 `migration.py` / `templates.py` 上游版复刻相关，不是运行态端口问题。

### §12.1 源码默认值

**文件**：`src/wowooai/app/migration.py`

默认数字员工常量必须为：

```python
_DEFAULT_AGENT_NAME = "Default Agent"
_DEFAULT_AGENT_DESCRIPTION = "Default wowooai agent"
```

创建默认 agent 时使用：

```python
template_result = create_agent_from_template(
    DEFAULT_AGENT_TEMPLATE,
    name=_DEFAULT_AGENT_NAME,
    agent_id="default",
    workspace_dir=default_workspace,
    description=_DEFAULT_AGENT_DESCRIPTION,
)
```

兼容旧单 agent 迁移时，`migrate_legacy_workspace_to_default_agent()` 构造的 `AgentProfileConfig` 中：

```python
id="default"
name="Default Agent"
description="Default wowooai agent (migrated from legacy config)"
```

### §12.2 实际配置预期

`~/.wowooai/config.json` 中应至少包含：

```json
{
  "agents": {
    "active_agent": "default",
    "profiles": {
      "default": {
        "id": "default"
      },
      "wowooai_QA_Agent_0.2": {
        "id": "wowooai_QA_Agent_0.2"
      }
    }
  }
}
```

关键预期：

- `default` 是 active profile。
- QA profile 可存在：`wowooai_QA_Agent_0.2`。
- 不应再额外生成一个 id 为 `wowooai` 的普通 agent。

### §12.3 复刻校验

```bash
grep -n '_DEFAULT_AGENT_NAME\|_DEFAULT_AGENT_DESCRIPTION\|agent_id="default"' \
  src/wowooai/app/migration.py

python - <<'PY'
import json
from pathlib import Path
cfg = json.loads(Path('~/.wowooai/config.json').expanduser().read_text())
agents = cfg.get('agents', {})
print(agents.get('active_agent'))
print(sorted((agents.get('profiles') or {}).keys()))
PY
# 期望 active_agent 为 default；profiles 至少包含 default 与 wowooai_QA_Agent_0.2
```

---

## §13 2026-04-30 增量：受保护用户目录扩展（Desktop / Documents / Downloads）

> 本节是在 §8 沙箱三层约束基础上的扩展。原始实现只把 `~/Desktop` 视为"用户原始数据"，本轮把保护范围扩到 `~/Desktop`、`~/Documents`、`~/Downloads` 三个目录，并同步更新提示词与 shell 沙箱拒绝消息。

### §13.1 `src/wowooai/agents/tools/shell.py`

**改动 1：常量 `_PROTECTED_USER_DIRS` 由单目录改为三目录**

定位：`_IN_PLACE_MODIFY_BINARIES` / `_WRITE_TARGET_BINARIES` / `_EDITOR_BINARIES` / `_INLINE_EDIT_FLAGS` / `_INTERPRETERS` / `_REDIRECT_RE` 常量声明区块之后，`_path_is_outside_workspace` 之后、`_looks_like_desktop_original` 之前新增：

```python
_PROTECTED_USER_DIRS = ("Desktop", "Documents", "Downloads")
```

**改动 2：`_looks_like_desktop_original(target: str) -> bool` 改为基于 `_PROTECTED_USER_DIRS` 循环判断**

不再只比较 `~/Desktop`，而是对 `_PROTECTED_USER_DIRS` 中每个子目录都比较一次：

```python
def _looks_like_desktop_original(target: str) -> bool:
    """A path is considered a 'protected user original' when it lives under
    one of the user's data directories (``~/Desktop``, ``~/Documents``,
    ``~/Downloads``) AND the basename does not carry the ``_副本`` copy
    suffix.
    """
    try:
        p = Path(target).expanduser()
    except (OSError, RuntimeError):
        return False
    if "_副本" in p.name:
        return False
    home = Path.home()
    try:
        resolved = p.resolve(strict=False)
    except (OSError, RuntimeError):
        return False
    for sub in _PROTECTED_USER_DIRS:
        protected = (home / sub).resolve(strict=False)
        try:
            resolved.relative_to(protected)
            return True
        except ValueError:
            continue
    return False
```

**改动 3：`_refuse(binary, target, kind)` 拒绝消息中的目录范围扩到三处**

```python
def _refuse(binary: str, target: str, kind: str) -> str:
    return (
        f"Refused: `{binary}` would {kind} the user's original file "
        f"`{target}` (under ~/Desktop, ~/Documents, or ~/Downloads). "
        f"Write to a `_副本`-suffixed copy in the workspace sandbox first."
    )
```

**改动 4：`_check_destructive_command()` 第 6 类（重定向覆盖）拒绝消息同步**

定位：`_check_destructive_command` 内 `for match in _REDIRECT_RE.finditer(seg)` 分支：

```python
return (
    f"Refused: shell redirect would overwrite the user's "
    f"original file `{target}` (under ~/Desktop, "
    f"~/Documents, or ~/Downloads). Write to a "
    f"`_副本`-suffixed copy in the workspace sandbox instead."
)
```

**改动 5：`execute_shell_command()` docstring 中"Sandbox rules"段落文案同步**

把原 docstring 中"Files under ``~/Desktop`` are treated as the user's **original** data"扩成三目录，并把沙箱范围收敛为文件修改：重定向 / in-place editor / in-place 修改二进制 / 覆盖类拷贝 / 编辑器 / 解释器 inline 写入。删除类操作不作为副本沙箱规则的一部分。落地形态见仓库当前 `execute_shell_command` 顶部 docstring。

### §13.2 `src/wowooai/agents/md_files/zh/SOUL.md`

把"## 边界"中桌面沙箱条目改写为：

```markdown
- **桌面（`~/Desktop`）、`~/Documents`、`~/Downloads` 上的文件视为用户原始数据**：写入、编辑或覆盖这些原始文件时，不要原地改原文件，必须在工作区沙箱中生成带 `_副本` 后缀的新文件（如 `数据_副本.xlsx`）。仅当用户在当次请求里明确说"覆盖"时才允许覆盖原文件。处理完成后，用 `send_file_to_user` 通知用户沙箱产物位置。删除类操作不属于副本沙箱规则，只按普通风险操作处理。
- **`execute_shell_command` 文件修改沙箱**：对上面这些原始文件路径，禁止使用 `>`、`>>`、`tee` 重定向覆盖，禁止 `sed -i`、`perl -i`、`awk -i inplace` 原地修改，禁止 `cp`、`rsync`、`install`、`ln`、`touch`、`chmod`、`chown` 写到原文件路径。应在沙箱中生成 `<原名>_副本.<扩展名>`，再对沙箱副本操作。删除类命令（如 `rm`、`rmdir`、`unlink`）不因副本沙箱规则被特殊拦截。
```

### §13.3 `src/wowooai/agents/md_files/en/SOUL.md`

英文版同步成：

```markdown
- **Files under `~/Desktop`, `~/Documents`, and `~/Downloads` are treated as original user data**: when writing, editing, or overwriting those original files, do not change the original in place; create a `_副本`-suffixed file in the workspace sandbox first (e.g. `data_副本.xlsx`). Only overwrite if the user explicitly says "overwrite" in the current request. After processing, use `send_file_to_user` to notify the user where the sandbox artifact is. Delete operations are not part of the copy-sandbox rule; handle them as ordinary risk-sensitive operations.
- **`execute_shell_command` file-modification sandbox**: for those original user paths, do not use `>`, `>>`, or `tee` to overwrite them; do not use `sed -i`, `perl -i`, or `awk -i inplace`; do not use `cp`, `rsync`, `install`, `ln`, `touch`, `chmod`, or `chown` against the original path. Create `<original_name>_副本.<extension>` in the sandbox first, then operate on the sandbox copy. Delete commands such as `rm`, `rmdir`, and `unlink` are not specially blocked by the copy-sandbox rule.
```

### §13.4 复刻校验

```bash
grep -n '_PROTECTED_USER_DIRS\s*=\s*("Desktop", "Documents", "Downloads")' \
  src/wowooai/agents/tools/shell.py
# 期望：1 行命中

grep -nE '~/Desktop, ~/Documents, or ~/Downloads' src/wowooai/agents/tools/shell.py | wc -l
# 期望：≥ 2（_refuse + 重定向分支）

grep -nE '~/Documents|~/Downloads|Documents.*Downloads' \
  src/wowooai/agents/md_files/zh/SOUL.md \
  src/wowooai/agents/md_files/en/SOUL.md
# 期望：zh/en 各至少命中 1 次
```

启动后端 + 跑一条故意越界的命令应被沙箱拦截，例如：

```bash
curl -s -X POST http://127.0.0.1:8088/api/agents/default/tools/execute_shell_command \
  -H 'Content-Type: application/json' \
  -d '{"command": "echo hi > ~/Documents/foo.txt"}'
# 期望返回 Refused 文本，包含 "~/Desktop, ~/Documents, or ~/Downloads"
```

---

## §14 2026-04-30 增量：本机启动规范固化

> 详见独立文档 [docs/changelog/startup.md](startup.md)。本节只列与代码无关的运维约束，方便复刻者一并复制。

新增文件 `docs/changelog/startup.md`，固定本机后端启动方式，要点：

1. 启动前必须用 `lsof -i :8088 -P -n` 检查端口，再用 `lsof -p <pid> | grep cwd` 确认旧进程是否指向 `/Users/rlw/AI项目/wowooai_last/`，是则先 `kill`。
2. 后端启动**必须使用绝对路径**：

   ```bash
   cd /Users/rlw/AI项目/wowooai
   /Users/rlw/AI项目/wowooai/.venv/bin/python3 -m wowooai app --host 127.0.0.1 --port 8088
   ```

   禁止 `python -m wowooai ...` / `.venv/bin/python -m wowooai ...` 这类相对命令（容易在旧仓库下被误启动成 PPID=1 孤儿进程）。
3. 启动后必须再次用 `lsof -p <pid> | grep cwd` 复核 cwd，并 `curl` 验证 `/api/workspace/files`、`/api/workspace/system-prompt-files`、`/api/agents` 三个接口。
4. 故障判断顺序：「我的记忆」页面 404 时，**第一反应不是改前端请求路径**，而是先核对 8088 cwd。


---

## §20 2026-04-30 增量：默认 agent 名称 / 描述 / 工作区 MD 兜底

> 上游 QwenPaw 的 `_do_ensure_default_agent` 只补 `chats.json / jobs.json`，不复制 `AGENTS.md / SOUL.md / PROFILE.md / BOOTSTRAP.md`，导致首次启动后 `~/.wowooai/workspaces/default/` 只有 `MEMORY.md`，模型缺失行为准则与身份档案。本节记录最小改动：默认 agent 改名为 `wowooai`、补长描述、并在初始化路径补一行模板兜底复制。

### §20.1 文件：`src/wowooai/app/migration.py`

**改动 1：import 区**

```python
from ..agents.utils.setup_utils import copy_workspace_md_files
```

**改动 2：模块级常量**

```python
_DEFAULT_AGENT_NAME = "wowooai"
_DEFAULT_AGENT_DESCRIPTION = (
    "wowooai 是人力窝的全能数字员工，面向日常办公与业务流程自动化，"
    "能够理解用户需求并调用工具、技能和自动化能力，"
    "协助完成文件处理、数据整理、系统操作、浏览器操作、信息查询和定时任务等各类工作。"
)
```

`agent_id` 仍保持 `"default"`，不引入 id 为 `wowooai` 的额外 agent。

**改动 3：`_do_ensure_default_agent` 增加 MD 兜底**

在 `_ensure_workspace_json_files(default_workspace, "default agent")` 之后追加：

```python
copy_workspace_md_files(
    config.agents.language or "zh",
    default_workspace,
    only_if_missing=True,
)
```

效果：

- 默认 agent 工作区缺 `AGENTS.md / SOUL.md / PROFILE.md / BOOTSTRAP.md` 等任意通用模板时，从 wheel 内 `agents/md_files/<lang>/` 用 `shutil.copy2` 字节级补齐。
- `only_if_missing=True`：已有文件不动，避免覆盖用户编辑。
- 每次启动都会跑一次（不只新建分支），既能修复历史遗漏，也对正常用户无影响。

### §20.2 复刻校验

```bash
cd /Users/rlw/AI项目/wowooai
python -m py_compile src/wowooai/app/migration.py

grep -n '_DEFAULT_AGENT_NAME\|_DEFAULT_AGENT_DESCRIPTION\|copy_workspace_md_files' \
  src/wowooai/app/migration.py
# 期望：
#   - _DEFAULT_AGENT_NAME = "wowooai"
#   - _DEFAULT_AGENT_DESCRIPTION = (...新长描述...)
#   - import + _do_ensure_default_agent 内的 copy_workspace_md_files(...) 调用各 1 处

# 清掉旧默认工作区（确认无重要数据后）
rm -rf ~/.wowooai/workspaces/default

/Users/rlw/AI项目/wowooai/.venv/bin/python3 -m wowooai app --host 127.0.0.1 --port 8088 &
sleep 4

ls ~/.wowooai/workspaces/default/
# 期望至少包含：AGENTS.md  SOUL.md  PROFILE.md  MEMORY.md  chats.json  jobs.json

python - <<'PY'
import json, pathlib
cfg = json.loads(pathlib.Path('~/.wowooai/config.json').expanduser().read_text())
prof = cfg['agents']['profiles']['default']
print(prof.get('id'))
ag = json.loads((pathlib.Path(prof['workspace_dir']).expanduser() / 'agent.json').read_text())
print(ag.get('name'))
print(ag.get('description'))
PY
# 期望：default / wowooai / 新长描述
```

---

## §21 2026-05-03 增量：默认数字员工首次预装精选技能

> 本节是在 §20 的默认数字员工初始化基础上继续收敛：只针对首次创建的 `id="default"`、名称为 `wowooai` 的默认数字员工，自动预装一组办公常用精选技能。用户后续新增、禁用、删除或修改技能后，启动流程不会再次覆盖。

### §21.1 复刻文件

从 source-bundle 复制最终源码：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/templates.py \
   src/wowooai/agents/templates.py
cp docs/changelog/source-bundle/src/wowooai/app/migration.py \
   src/wowooai/app/migration.py
```

### §21.2 `src/wowooai/agents/templates.py`

在 `LOCAL_TEMPLATE_SKILL_NAMES` 后新增默认数字员工精选技能列表：

```python
LOCAL_TEMPLATE_SKILL_NAMES = ("make_plan",)
DEFAULT_TEMPLATE_SKILL_NAMES = (
    "make_plan",
    "file_reader",
    "pdf",
    "docx",
    "xlsx",
    "pptx",
    "cron",
    "browser_visible",
)
```

`build_agent_template(DEFAULT_AGENT_TEMPLATE, ...)` 的返回值中，`initial_skill_names` 不再为空，而是使用该精选列表：

```python
return AgentTemplateBuildResult(
    agent_config=agent_config,
    initial_skill_names=DEFAULT_TEMPLATE_SKILL_NAMES,
    md_template_id=get_workspace_md_template_id(template_id),
)
```

技能选择原则：覆盖计划制定、文本/PDF/Office 文件处理、定时任务和基础浏览器启动说明；不默认启用渠道类、源码 QA、喜马拉雅、多数字员工协作等专项技能，避免新用户默认上下文过重或误触专项流程。

### §21.3 `src/wowooai/app/migration.py`

在 `_do_ensure_default_agent()` 的 `if not agent_existed:` 首次创建分支里，`build_agent_template(...)` 之后、写入 profile 之前，调用现有 workspace 初始化流程安装精选技能：

```python
from .routers.agents import _initialize_agent_workspace

_initialize_agent_workspace(
    default_workspace,
    skill_names=list(template_result.initial_skill_names),
    md_template_id=template_result.md_template_id,
    language=config.agents.language or "zh",
)
```

关键约束：

- 只在 `default` 不存在、首次创建默认数字员工时执行。
- 已存在 `default` 时不会再次安装技能。
- 不会重新启用用户已禁用的技能。
- 不会覆盖用户后续添加、删除或修改的技能配置。
- 安装走 `_initialize_agent_workspace()` → `_install_initial_skills()` → `SkillPoolService.download_to_workspace()`，确保技能目录和 `skill.json` manifest 同步写入，且目标技能为 `enabled=True`。

### §21.4 复刻校验

```bash
python -m py_compile \
  src/wowooai/agents/templates.py \
  src/wowooai/app/migration.py

grep -n 'DEFAULT_TEMPLATE_SKILL_NAMES\|initial_skill_names=DEFAULT_TEMPLATE_SKILL_NAMES' \
  src/wowooai/agents/templates.py

grep -n '_initialize_agent_workspace(' src/wowooai/app/migration.py
```

首次启动全新工作区后检查默认数字员工技能 manifest：

```bash
python - <<'PY'
import json
from pathlib import Path
skill_json = Path('~/.wowooai/workspaces/default/skill.json').expanduser()
data = json.loads(skill_json.read_text(encoding='utf-8'))
for name in [
    'make_plan', 'file_reader', 'pdf', 'docx',
    'xlsx', 'pptx', 'cron', 'browser_visible',
]:
    entry = data.get('skills', {}).get(name)
    print(name, bool(entry and entry.get('enabled')))
PY
# 期望：上述技能均输出 True
```

---

## §22 2026-05-03 修复：全新安装误触发 legacy migration 导致 default 技能为空

> 本节修复 §21 的一个首启边界问题：删除 `~/.wowooai` 与 `~/.wowooai.secret` 后首次启动时，`config.json` 不存在，`load_config()` 会返回默认 `Config()`；默认 `AgentsConfig.profiles` 自带 `default` 引用，旧迁移函数会误判为 legacy 单 agent 配置并抢先创建 `Default Agent (migrated from legacy config)`，导致 `_do_ensure_default_agent()` 不再进入首次创建分支，最终 `default` 的 `skill.json` 为空。

### §22.1 复刻文件

从 source-bundle 复制最终源码：

```bash
cp docs/changelog/source-bundle/src/wowooai/app/migration.py \
   src/wowooai/app/migration.py
```

### §22.2 `src/wowooai/app/migration.py`

`constant.py` import 中补入 `CONFIG_FILE`：

```python
from ..constant import (
    BUILTIN_QA_AGENT_ID,
    CONFIG_FILE,
    LEGACY_QA_AGENT_ID,
    WORKING_DIR,
)
```

在 `_WORKSPACE_JSON_DEFAULTS` 后新增 fresh-install guard：

```python
_LEGACY_WORKSPACE_MARKERS = tuple(
    name for name, _ in _WORKSPACE_ITEMS_TO_MIGRATE
)


def _has_legacy_workspace_payload(root: Path) -> bool:
    if not root.exists():
        return False
    if any((root / name).exists() for name in _LEGACY_WORKSPACE_MARKERS):
        return True
    return any(root.glob("*.md"))


def _should_run_legacy_workspace_migration() -> bool:
    root = Path(WORKING_DIR).expanduser()
    config_path = root / CONFIG_FILE
    if not config_path.exists() and not _has_legacy_workspace_payload(root):
        logger.debug(
            "No legacy config or workspace payload found; "
            "skipping legacy migration for fresh install",
        )
        return False
    return True
```

`_do_migrate_legacy_workspace()` 开头先判断是否是真正 legacy 场景：

```python
def _do_migrate_legacy_workspace() -> bool:
    """Internal implementation of legacy workspace migration."""
    if not _should_run_legacy_workspace_migration():
        return False

    try:
        config = load_config()
```

同时修正 `_do_ensure_default_agent()` 对“默认 profile 只是 Pydantic 默认值”的误判：只有 `agent.json` 真实存在才视为 default 已存在。

```python
if "default" in config.agents.profiles:
    agent_ref = config.agents.profiles["default"]
    default_workspace = Path(agent_ref.workspace_dir).expanduser()
    agent_existed = (default_workspace / "agent.json").exists()
else:
    default_workspace = Path(
        f"{WORKING_DIR}/workspaces/default",
    ).expanduser()
    agent_existed = False
```

效果：

- 全新安装、无 `config.json`、无 legacy 工作区文件时，跳过 legacy migration。
- `ensure_default_agent_exists()` 会创建 `id="default"`、名称 `wowooai` 的默认数字员工。
- §21 的精选技能会在首次创建时写入 `~/.wowooai/workspaces/default/skills/` 与 `skill.json`。
- 真实旧用户迁移不受影响：只要根工作区存在 legacy markers（`sessions/`、`memory/`、`active_skills/`、`customized_skills/`、`chats.json`、`jobs.json`、`*.md` 等），仍走原 legacy migration。

### §22.3 复刻校验

编译：

```bash
python -m py_compile src/wowooai/app/migration.py src/wowooai/agents/templates.py
```

隔离模拟全新安装：

```bash
TMPDIR=$(mktemp -d /tmp/wowooai-fresh.XXXXXX)
wowooai_WORKING_DIR="$TMPDIR" python - <<'PY'
import json
from pathlib import Path
from wowooai.app.migration import (
    migrate_legacy_workspace_to_default_agent,
    ensure_default_agent_exists,
    migrate_legacy_skills_to_skill_pool,
    ensure_qa_agent_exists,
)
from wowooai.constant import WORKING_DIR

print('legacy_migrated', migrate_legacy_workspace_to_default_agent())
ensure_default_agent_exists()
migrate_legacy_skills_to_skill_pool()
ensure_qa_agent_exists()
root = Path(WORKING_DIR)
default_agent = json.loads((root / 'workspaces/default/agent.json').read_text())
default_skills = json.loads((root / 'workspaces/default/skill.json').read_text())
qa_skills = json.loads((root / 'workspaces/wowooai_QA_Agent_0.2/skill.json').read_text())
print(default_agent.get('name'))
print(sorted(default_skills.get('skills', {}).keys()))
print(sorted(qa_skills.get('skills', {}).keys()))
PY
```

期望：

```text
legacy_migrated False
wowooai
['browser_visible', 'cron', 'docx', 'file_reader', 'make_plan', 'pdf', 'pptx', 'xlsx']
['QA_source_index', 'guidance']
```

隔离模拟真实 legacy 工作区仍可迁移：

```bash
TMPDIR=$(mktemp -d /tmp/wowooai-legacy.XXXXXX)
printf '# legacy memory\n' > "$TMPDIR/MEMORY.md"
wowooai_WORKING_DIR="$TMPDIR" python - <<'PY'
import json
from pathlib import Path
from wowooai.app.migration import migrate_legacy_workspace_to_default_agent
from wowooai.constant import WORKING_DIR

print('legacy_migrated', migrate_legacy_workspace_to_default_agent())
root = Path(WORKING_DIR)
agent = json.loads((root / 'workspaces/default/agent.json').read_text())
print(agent.get('name'))
print((root / 'workspaces/default/MEMORY.md').exists())
PY
```

期望：

```text
legacy_migrated True
Default Agent
True
```

---

## §23 2026-05-03 修复：CLI 启动先写 `last_api` 时仍应跳过 fresh install legacy migration

> 本节补齐 §22 的真实启动链路边界：`wowooai app` 在 FastAPI lifespan / migration 之前会先调用 `write_last_api()`，这会在全新安装目录下提前生成 `config.json`。因此 legacy migration 不能只用 `config.json` 是否存在判断是否为旧安装；必须识别“仅由运行态 `last_api` 写出的默认空配置”。

### §23.1 复刻文件

从 source-bundle 复制最终源码：

```bash
cp docs/changelog/source-bundle/src/wowooai/app/migration.py \
   src/wowooai/app/migration.py
```

### §23.2 `src/wowooai/app/migration.py`

`config.config` import 中补入根配置模型 `Config`：

```python
from ..config.config import (
    AgentProfileConfig,
    AgentProfileRef,
    AgentsConfig,
    AgentsLLMRoutingConfig,
    AgentsRunningConfig,
    Config,
    save_agent_config,
)
```

在 `_has_legacy_workspace_payload()` 后新增默认运行态配置识别 helper：

```python
def _config_without_runtime_fields(config: Config) -> dict:
    payload = config.model_dump(mode="json", by_alias=True)
    payload.pop("last_api", None)
    payload.pop("user_timezone", None)
    return payload


def _is_default_runtime_only_config(config: Config) -> bool:
    return _config_without_runtime_fields(config) == _config_without_runtime_fields(
        Config(),
    )
```

`_should_run_legacy_workspace_migration()` 改为同时检查工作区 payload 与 config 内容：

```python
def _should_run_legacy_workspace_migration() -> bool:
    root = Path(WORKING_DIR).expanduser()
    has_legacy_payload = _has_legacy_workspace_payload(root)
    config_path = root / CONFIG_FILE
    if not config_path.exists():
        if not has_legacy_payload:
            logger.debug(
                "No legacy config or workspace payload found; "
                "skipping legacy migration for fresh install",
            )
            return False
        return True

    try:
        config = load_config()
    except Exception as e:
        logger.warning(
            "Failed to inspect config before legacy migration: %s",
            e,
        )
        return True

    if not has_legacy_payload and _is_default_runtime_only_config(config):
        logger.debug(
            "Only default runtime config found; "
            "skipping legacy migration for fresh install",
        )
        return False
    return True
```

关键效果：

- 全新安装即使 `write_last_api()` 已先写出 `config.json`，也会跳过 legacy migration。
- `ensure_default_agent_exists()` 会走首次创建分支，生成 `id="default"`、名称 `wowooai` 的默认数字员工，并预装 §21 的 8 个精选技能。
- `last_api` 和 `user_timezone` 被视为运行态字段，比较默认空配置时忽略，避免启动前写入端口或系统时区导致误判。
- 只要根工作区存在 legacy markers（如 `MEMORY.md`、`sessions/`、`active_skills/`、`chats.json` 等），仍正常执行旧用户迁移。
- 如果配置读取失败，保守返回 `True`，避免跳过可能需要的真实迁移。

### §23.3 复刻校验

编译：

```bash
python -m py_compile src/wowooai/app/migration.py src/wowooai/agents/templates.py
```

模拟真实 CLI 启动顺序：先写 `last_api`，再跑 migration / default / QA 初始化：

```bash
TMPDIR=$(mktemp -d /tmp/wowooai-startup-fresh.XXXXXX)
wowooai_WORKING_DIR="$TMPDIR" python - <<'PY'
import json
from pathlib import Path
from wowooai.config.utils import write_last_api
from wowooai.app.migration import (
    migrate_legacy_workspace_to_default_agent,
    ensure_default_agent_exists,
    migrate_legacy_skills_to_skill_pool,
    ensure_qa_agent_exists,
)
from wowooai.constant import WORKING_DIR

write_last_api('127.0.0.1', 8088)
print('config_exists_before_migration', (Path(WORKING_DIR) / 'config.json').exists())
print('legacy_migrated', migrate_legacy_workspace_to_default_agent())
ensure_default_agent_exists()
migrate_legacy_skills_to_skill_pool()
ensure_qa_agent_exists()
root = Path(WORKING_DIR)
default_agent = json.loads((root / 'workspaces/default/agent.json').read_text())
default_skills = json.loads((root / 'workspaces/default/skill.json').read_text())
qa_skills = json.loads((root / 'workspaces/wowooai_QA_Agent_0.2/skill.json').read_text())
print(default_agent.get('name'))
print(sorted(default_skills.get('skills', {}).keys()))
print(sorted(qa_skills.get('skills', {}).keys()))
PY
rm -rf "$TMPDIR"
```

期望：

```text
config_exists_before_migration True
legacy_migrated False
wowooai
['browser_visible', 'cron', 'docx', 'file_reader', 'make_plan', 'pdf', 'pptx', 'xlsx']
['QA_source_index', 'guidance']
```

模拟真实 legacy 工作区仍会迁移：

```bash
TMPDIR=$(mktemp -d /tmp/wowooai-legacy-check.XXXXXX)
printf '# legacy memory\n' > "$TMPDIR/MEMORY.md"
wowooai_WORKING_DIR="$TMPDIR" python - <<'PY'
import json
from pathlib import Path
from wowooai.config.utils import write_last_api
from wowooai.app.migration import migrate_legacy_workspace_to_default_agent
from wowooai.constant import WORKING_DIR

write_last_api('127.0.0.1', 8088)
print('legacy_migrated', migrate_legacy_workspace_to_default_agent())
root = Path(WORKING_DIR)
agent = json.loads((root / 'workspaces/default/agent.json').read_text())
print(agent.get('name'))
print((root / 'workspaces/default/MEMORY.md').exists())
PY
rm -rf "$TMPDIR"
```

期望：

```text
legacy_migrated True
Default Agent
True
```

---

## §24 2026-05-04 增量：桌面打包依赖与 launcher 孤儿进程兜底

> 配套打包执行说明见 [packaging-macos.md](packaging-macos.md) / [packaging-windows.md](packaging-windows.md)。本节只记录需要复刻到源码的后端 / 打包脚本变更；打包文档不再承载代码改造逻辑。

### §24.1 复刻文件

```bash
cp docs/changelog/source-bundle/pyproject.toml \
   pyproject.toml
cp docs/changelog/source-bundle/src/wowooai/cli/app_cmd.py \
   src/wowooai/cli/app_cmd.py
cp docs/changelog/source-bundle/src/wowooai/cli/desktop_cmd.py \
   src/wowooai/cli/desktop_cmd.py
cp docs/changelog/source-bundle/scripts/pack/build_common.py \
   scripts/pack/build_common.py
cp docs/changelog/source-bundle/scripts/pack/build_macos.sh \
   scripts/pack/build_macos.sh
```

### §24.2 `pyproject.toml`：新增桌面 extras 与 e2e marker

`[project.optional-dependencies]` 新增 `desktop`，供桌面包一次性安装 Office / PDF / 浏览器辅助依赖：

```toml
desktop = [
    "typing-extensions>=4.12",
    "selenium>=4.0",
    "playwright-stealth>=2.0",
    "python-docx>=1.1",
    "python-pptx>=1.0",
    "openpyxl>=3.1",
    "xlsxwriter>=3.2",
    "xlrd>=2.0.1",
    "pypdf>=4.0",
    "pypdfium2>=4.0",
    "pdfplumber>=0.10",
    "pdf2image>=1.17",
    "reportlab>=4.0",
    "opencv-python-headless>=4.9",
    "lxml>=5.0",
    "defusedxml>=0.7",
    "beautifulsoup4>=4.12",
    "markdownify>=0.13",
]
```

pytest markers 增加：

```toml
"e2e: marks tests as end-to-end tests",
```

### §24.3 `src/wowooai/cli/app_cmd.py`：父进程 watchdog

新增 `_start_parent_watchdog()`，仅当环境变量 `WOWOOAI_PARENT_PID` 存在时启用。桌面 launcher 被 Force Quit / SIGKILL / 崩溃后，后端检测到 `os.getppid()` 不再等于预期父进程 PID，就立即退出，避免孤儿进程占用端口或 SQLite 锁。

关键片段：

```python
def _start_parent_watchdog() -> None:
    raw = os.environ.get("WOWOOAI_PARENT_PID")
    if not raw:
        return
    try:
        expected_ppid = int(raw)
    except ValueError:
        return
    if expected_ppid <= 1:
        return

    log = logging.getLogger(__name__)

    def _watch() -> None:
        while True:
            time.sleep(1.0)
            try:
                current_ppid = os.getppid()
            except OSError:
                current_ppid = 1
            if current_ppid != expected_ppid:
                log.warning(
                    "Parent process (pid=%d) is gone (current ppid=%d); "
                    "exiting to avoid becoming an orphan.",
                    expected_ppid,
                    current_ppid,
                )
                os._exit(0)

    threading.Thread(
        target=_watch,
        name="parent-watchdog",
        daemon=True,
    ).start()
```

`app_cmd()` 中 `setup_logger(log_level)` 后调用：

```python
setup_logger(log_level)
_start_parent_watchdog()
```

### §24.4 `src/wowooai/cli/desktop_cmd.py`：注入父进程 PID

launcher 启动后端 subprocess 前注入：

```python
env = os.environ.copy()
env[LOG_LEVEL_ENV] = log_level
env["WOWOOAI_PARENT_PID"] = str(os.getpid())
```

同时把桌面窗口标题和启动文案统一为 `WowooAI`，不改变运行架构。

### §24.5 `scripts/pack/build_common.py`：支持 `--extras`

新增参数：

```python
parser.add_argument(
    "--extras",
    default="desktop",
    help=(
        "Package extras to install from the wheel "
        "(default: desktop; use full for local/whisper dependencies)."
    ),
)
```

安装 wheel 时使用：

```python
f"wowooai[{args.extras}] @ {wheel_uri}"
```

### §24.6 `scripts/pack/build_macos.sh`：DMG 与桌面依赖打包

关键行为：

- 默认 `EXTRAS=desktop`，传给 `build_common.py --extras`。
- 构建前检查现有 wheel 是否包含 `wowooai/console/index.html`；缺失则删除并重建，避免桌面包白屏。
- 产物名统一为 `WowooAI.app`。
- 默认创建 `dist/WowooAI-<version>-macOS.dmg`，DMG 内包含 `WowooAI.app` 与 `/Applications` 软链。
- 如存在 Playwright Chromium 缓存，复制到 `.app/Contents/Resources/playwright-browsers/`，launcher 设置 `PLAYWRIGHT_BROWSERS_PATH`。

### §24.7 复刻校验

```bash
python -m py_compile \
  src/wowooai/cli/app_cmd.py \
  src/wowooai/cli/desktop_cmd.py \
  scripts/pack/build_common.py

grep -n 'desktop = \[' pyproject.toml
grep -n 'e2e:' pyproject.toml
grep -n 'WOWOOAI_PARENT_PID\|_start_parent_watchdog' \
  src/wowooai/cli/app_cmd.py \
  src/wowooai/cli/desktop_cmd.py
grep -n -- '--extras\|args.extras' scripts/pack/build_common.py
grep -n 'APP_NAME="WowooAI"\|hdiutil create\|PLAYWRIGHT_BROWSERS_PATH\|console/index.html' \
  scripts/pack/build_macos.sh
```

桌面依赖验证：

```bash
python3 -m venv /tmp/wowooai-desktop-check
/tmp/wowooai-desktop-check/bin/pip install 'dist/wowooai-*.whl[desktop]'
/tmp/wowooai-desktop-check/bin/python -c 'import openpyxl, docx, pptx, pdfplumber; print("ok")'
rm -rf /tmp/wowooai-desktop-check
```

---

## §25 2026-05-04 修复：MCP 已连接但对话运行时未注册到 Toolkit

> 症状：手工配置的 Tavily / 钉钉通讯录 / 钉钉日历 MCP 在 `/api/mcp` 中显示 enabled，`/api/mcp/{client_key}/tools` 也能正常列工具，但对话里数字员工无法看到或调用这些 MCP 工具。

### §25.1 根因

MCP 配置和连接链路本身正常：

- agent 级配置位于 `~/.wowooai/workspaces/default/agent.json`，不是根配置 `~/.wowooai/config.json`。
- `src/wowooai/app/workspace/service_factories.py` 会从 `ws._config.mcp` 初始化 `MCPClientManager`。
- `src/wowooai/app/runner/runner.py` 每次 query 会从 manager 取 active MCP clients，并传给 `wowooaiAgent`。

真正失败点在 `src/wowooai/agents/react_agent.py`：当前依赖 `agentscope==1.0.19.post1` 对应的 `Toolkit.register_mcp_client()` 不支持 `execution_timeout` 参数，但旧代码注册 MCP 时传入了该参数，导致每个 MCP client 都被跳过：

```text
Toolkit.register_mcp_client() got an unexpected keyword argument 'execution_timeout'
```

### §25.2 复刻文件

从 source-bundle 复制最终源码：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/react_agent.py \
   src/wowooai/agents/react_agent.py
```

### §25.3 `src/wowooai/agents/react_agent.py`

`register_mcp_clients()` 不再直接向 AgentScope Toolkit 传 `execution_timeout`，统一走兼容 helper：

```python
await self._register_mcp_client_compat(
    client,
    namesake_strategy=namesake_strategy,
)
```

recovery 后重新注册也走同一 helper：

```python
await self._register_mcp_client_compat(
    recovered_client,
    namesake_strategy=namesake_strategy,
)
```

新增兼容 helper：

```python
async def _register_mcp_client_compat(
    self,
    client: Any,
    namesake_strategy: NamesakeStrategy,
) -> None:
    await self.toolkit.register_mcp_client(
        client,
        namesake_strategy=namesake_strategy,
    )
```

### §25.4 复刻校验

```bash
python -m py_compile src/wowooai/agents/react_agent.py

# 不应再有 execution_timeout / exeution_timeout 参数残留
grep -n 'execution_timeout\|exeution_timeout' src/wowooai/agents/react_agent.py
# 期望无输出

# 应存在兼容 helper 与两处调用
grep -n '_register_mcp_client_compat' src/wowooai/agents/react_agent.py

# MCP 配置与连接校验
curl -sS http://127.0.0.1:8088/api/mcp
curl -sS http://127.0.0.1:8088/api/mcp/tavily_search/tools
```

启动后端并发起一次对话后，日志不应再出现：

```text
Toolkit.register_mcp_client() got an unexpected keyword argument 'execution_timeout'
```

---

## §26 2026-05-04 收敛：副本沙箱只覆盖文件修改，不特殊拦截删除

> 本节修正 §8 / §13 中旧口径：副本沙箱不是“删除命令沙箱”。它只处理写入、编辑、覆盖用户原始文件时的误改风险；删除类操作仍属于风险操作，但不通过 `_副本` 规则特殊拦截。

### §26.1 复刻文件

从 source-bundle 复制最终源码和模板：

```bash
cp docs/changelog/source-bundle/src/wowooai/agents/tools/file_io.py \
   src/wowooai/agents/tools/file_io.py
cp docs/changelog/source-bundle/src/wowooai/agents/tools/shell.py \
   src/wowooai/agents/tools/shell.py
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/zh/AGENTS.md \
   src/wowooai/agents/md_files/zh/AGENTS.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/en/AGENTS.md \
   src/wowooai/agents/md_files/en/AGENTS.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/zh/SOUL.md \
   src/wowooai/agents/md_files/zh/SOUL.md
cp docs/changelog/source-bundle/src/wowooai/agents/md_files/en/SOUL.md \
   src/wowooai/agents/md_files/en/SOUL.md
```

当前默认工作区也需同步同一口径：

```bash
cp src/wowooai/agents/md_files/zh/AGENTS.md ~/.wowooai/workspaces/default/AGENTS.md
cp src/wowooai/agents/md_files/zh/SOUL.md ~/.wowooai/workspaces/default/SOUL.md
```

### §26.2 `src/wowooai/agents/tools/file_io.py`

`_sandbox_copy_for_write()` 保留 workspace 沙箱概念：工作区外的写入、编辑、追加不会落到用户原目录，而是重定向到 workspace `.sandbox/input/` 下的 `_副本` 文件：

```python
def _copy_suffix_name(path: Path) -> str:
    if "_副本" in path.name:
        return path.name
    return f"{path.stem}_副本{path.suffix}"
```

若原文件已存在，首次编辑 / 追加前复制原文件内容到沙箱副本，后续只修改沙箱里的 `_副本`。

### §26.3 `src/wowooai/agents/tools/shell.py`

副本沙箱检查范围收敛为文件修改：

- 拦截重定向覆盖：`>`、`>>`、`&>`、`2>>` 等写到原始文件。
- 拦截 inline edit：`sed -i`、`perl -i`、`awk -i inplace` 等编辑原始文件。
- 拦截 in-place 修改工具：`mv`、`dd`、`shred`、`truncate` 作用于原始文件。
- 拦截写入目标类命令：`tee`、`cp`、`install`、`ln`、`rsync`、`touch`、`chmod`、`chown` 写到原始文件。
- `cp` / `install` / `ln` / `rsync` 只检查目标参数，允许 `cp 原文件 原文件_副本.ext`。
- 删除类命令 `rm` / `rmdir` / `unlink` 不属于副本沙箱特殊拦截范围。

### §26.4 提示词模板

`AGENTS.md` / `SOUL.md` 同步写明：写入、编辑、覆盖用户原始文件时必须在工作区沙箱中写到 `_副本`；删除类操作不属于副本沙箱规则，只按普通风险操作处理。

### §26.5 复刻校验

```bash
python -m py_compile \
  src/wowooai/agents/tools/file_io.py \
  src/wowooai/agents/tools/shell.py

# 不应再有旧删除沙箱集合
grep -n '_DESTRUCTIVE_BINARIES' src/wowooai/agents/tools/shell.py
# 期望无输出

# 删除类命令应只作为说明出现，不在拦截集合中
grep -n '_IN_PLACE_MODIFY_BINARIES' src/wowooai/agents/tools/shell.py
grep -n 'rm.*rmdir.*unlink\|删除类操作不属于副本沙箱规则' \
  src/wowooai/agents/md_files/zh/SOUL.md \
  src/wowooai/agents/md_files/en/SOUL.md

# 写入原始文件仍应被拒绝；删除不因副本沙箱规则被拒绝；文件工具写到沙箱 _副本
python - <<'PY'
import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from wowooai.config.context import set_current_workspace_dir
from wowooai.agents.tools.shell import _check_destructive_command
from wowooai.agents.tools.file_io import _sandbox_copy_for_write

with TemporaryDirectory() as tmp:
    set_current_workspace_dir(Path(tmp))
    print(_check_destructive_command('echo hi > ~/Documents/foo.txt'))
    print(_check_destructive_command('rm ~/Documents/foo.txt'))
    print(_check_destructive_command('cp ~/Documents/foo.txt ~/Documents/foo_副本.txt'))
    print(Path(_sandbox_copy_for_write('/Users/example/Documents/foo.txt')).as_posix().endswith('/.sandbox/input/foo_副本.txt'))
PY
# 期望：第一行 Refused；第二、三行为 None；第四行为 True
```




## §27 2026-05-04 修复：`send_file_to_user` 改用同源 HTTP URL，恢复客户端文件下载

### 现象

桌面客户端中 bot 通过 `send_file_to_user` 发送的文件，对话气泡里点击没有任何反应：

- 没有触发系统保存对话框
- 没有打开新窗口
- `~/.wowooai/desktop.log` 里完全没有 `save_file` / `pywebview` 调用记录
- 后端日志也没有任何下载请求

### 根因（前端→lib→桌面端三层全部失效）

`send_file_to_user` 在改用本地 URL 之后，输出的 `FileBlock` 形如：

```json
{
  "type": "file",
  "source": {"type": "url", "url": "file:///Users/rlw/.wowooai/workspaces/default/%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE_%E5%89%AF%E6%9C%AC.xlsx"},
  "filename": "关联数据_副本.xlsx"
}
```

链条上有 **三个独立断点**：

1. **`console/src/pages/Chat/sessionApi/index.ts: resolveContentItemUrl`** 只在 `c.file_url || c.file_id` 存在时才规范化 URL；后端只塞了 `source.url`，分支不命中，content 原样下发。
2. **`@agentscope-ai/chat` Response/Message.js** 只读 `item.file_url` / `item.file_name`；上一层没补字段，传给 `Files` 卡片的 `data[0].url` 是 `undefined`。
3. **`@agentscope-ai/chat` DefaultCards/Files** 在 `fileInfo.url` 为 falsy 时**根本不渲染下载图标**——所以 DOM 里没有可点击的元素，`save_file` 永远不会被调用。

即便前 3 个断点修复，链接还是 `file://`：pywebview WebView 拒绝从 `http://` 同源页跨协议导航，`WebViewAPI.save_file` 又显式只接受 `http(s)`，依旧死路。

### 修复（方案 1：后端统一输出同源 HTTP 相对路径）

`src/wowooai/agents/tools/send_file.py`：

- 删除 `_path_to_file_url`，改用 `_path_to_preview_url`，输出 `/api/files/preview/<percent-encoded-absolute-path>`。
- `FileBlock` 同时填 `source.url`、`file_url`、`file_name`，让 `@agentscope-ai/chat` 默认卡片直接命中。

`src/wowooai/agents/schema.py`：

- `FileBlock` 新增可选字段 `file_url`、`file_name`，与 lib 期望对齐。

`src/wowooai/app/routers/files.py` **无需改动**：preview 路由本来就接受任意绝对路径并 `FileResponse` 返回，沿用既有路径解析（`Path("/" + normalized).resolve()`）。

### 为什么不动前端

`chat/utils.ts: toDisplayUrl` 已经能把 `/Users/...` 转成 `chatApi.filePreviewUrl(...)`；`sessionApi.resolveContentItemUrl` 一旦看到 `file_url` 字段就会规范化。所以只要后端把字段补齐、URL 形态正确，整条链就贯通，前端、第三方 lib、桌面端 `WebViewAPI` 全都不用改。

这跟 §9（前端 API base URL 走同源相对路径）的思路一致：URL 越统一，部署形态越能复用同一套代码。

### 三种部署场景对照

| 场景 | URL 形态 | 浏览器解析后的实际地址 |
|---|---|---|
| 桌面包随机端口 60494 | `/api/files/preview/...` | `http://127.0.0.1:60494/api/files/preview/...` |
| `wowooai app` 默认 8088 | `/api/files/preview/...` | `http://127.0.0.1:8088/api/files/preview/...` |
| Docker 反代 | `/api/files/preview/...` | `https://<domain>/api/files/preview/...` |

### 验证

```python
from wowooai.agents.tools.send_file import _path_to_preview_url
assert _path_to_preview_url('/Users/rlw/.wowooai/workspaces/default/关联数据_副本.xlsx') == \
  '/api/files/preview/Users/rlw/.wowooai/workspaces/default/%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE_%E5%89%AF%E6%9C%AC.xlsx'
```

打包后人工验收：

1. 让 bot 调用 `send_file_to_user` 给某个本地文件
2. DevTools Network 应能看到 `GET /api/files/preview/...` 200，文件卡片下载图标显示
3. 点击下载图标：浏览器场景下 `window.open` 新开页 / 或直接下载；桌面包场景下沿用 `Files` 默认行为也能拉起浏览器内置下载（如需弹原生 OS 保存对话框，可后续再叠加自定义 Files Card 走 `pywebview.api.save_file`）

### 风险与回归

| 场景 | 影响 |
|---|---|
| 历史会话里仍是 `file://` URL 的旧消息 | ⚠️ 仍点不开（无字段、无 HTTP URL）；仅影响存量记录，无法回填 |
| 跨平台路径（Windows 盘符 / UNC） | ✅ `_path_to_preview_url` 沿用原 Windows 处理逻辑；preview 路由的 `/C:/...` 归一化也保留 |
| 文件路径含中文 / 空格 / `%` | ✅ `quote(safe="/:@")` 全部 percent-encode |
| 浏览器模式 (`wowooai app`) | ✅ 同源相对路径直接可用 |
| Docker / 反代 | ✅ 同源相对路径直接可用 |
| 桌面 WebView | ✅ 同源 HTTP URL 不再触发跨协议拒绝；`save_file` 白名单也通过 |

---

## §29 2026-05-06 修复：pywebview Windows 标题栏 / 任务栏图标缺失（WM_SETICON + AppUserModelID）

### 现象

Windows 桌面包启动后,主窗口左上角标题栏图标 / 任务栏 Alt-Tab 缩略图仍显示 `python.exe` 的默认图标(或 pywebview 占位图),而不是品牌蓝色 W。macOS 不受影响——`.app` 包通过 `CFBundleIconFile` 自动继承 `icon.icns`。

### 根因

仅传 `webview.create_window(icon=...)` / `webview.start(icon=...)` 在 Windows 上不够:
1. EdgeChromium 后端绘制的 title bar 用得到该参数,但 **OS 真正读取的标题栏图标 / 任务栏图标来自宿主进程**(本场景是 `python.exe`),需要 `WM_SETICON` 显式注入。
2. Win11 默认按"宿主可执行文件"对窗口分组,会把 WowooAI 与所有 `python.exe` 窗口归为一组并显示 python 图标。需 `SetCurrentProcessExplicitAppUserModelID` 单独建组。

### 修复

**文件**:`src/wowooai/cli/desktop_cmd.py`

废弃旧的 `_resolve_window_icon()` + `create_window(icon=)` 方案;改为:
- 在 `desktop_cmd()` 内联探测 `icon.ico` 路径(`<env_root>/icon.ico` → `<repo>/scripts/pack/assets/icon.ico`)。
- 找到后 `webview.start(icon=icon_path)` 仍传给 EdgeChromium。
- **额外** Windows 调用新增的 `_apply_win_icon(window, icon_path)`:设置 AppUserModelID,然后后台线程轮询 `FindWindowW("WowooAI Desktop")`,拿到 HWND 后通过 `SendMessageW(hwnd, WM_SETICON, ICON_SMALL/ICON_BIG, hIcon)` 强制覆盖 OS 标题栏 + 任务栏图标。

```python
def _apply_win_icon(window, icon_path: str) -> None:
    """Force the Windows title-bar AND taskbar icon to *icon_path*."""
    import ctypes
    from ctypes import wintypes

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "AgentScope.WowooAI.Desktop.1",
        )
    except Exception as e:
        logger.warning(f"SetCurrentProcessExplicitAppUserModelID failed: {e}")

    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    LR_DEFAULTSIZE = 0x00000040

    user32 = ctypes.windll.user32
    user32.LoadImageW.restype = wintypes.HANDLE
    user32.LoadImageW.argtypes = [
        wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
        ctypes.c_int, ctypes.c_int, wintypes.UINT,
    ]
    user32.SendMessageW.restype = ctypes.c_long
    user32.SendMessageW.argtypes = [
        wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
    ]
    user32.FindWindowW.restype = wintypes.HWND
    user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]

    def _set_icons() -> None:
        # pywebview 的 'shown'/'loaded' 事件在 EdgeChromium 后端不稳定,
        # 改为按窗口标题轮询 FindWindow,最长 10s。
        hwnd = 0
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            hwnd = user32.FindWindowW(None, "WowooAI Desktop")
            if hwnd:
                break
            time.sleep(0.2)
        if not hwnd:
            logger.warning("Window HWND not found; icon not applied.")
            return

        small = user32.LoadImageW(
            None, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE,
        )
        big = user32.LoadImageW(
            None, icon_path, IMAGE_ICON, 32, 32,
            LR_LOADFROMFILE | LR_DEFAULTSIZE,
        )
        if small:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, small)
        if big:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, big)
        logger.info(
            f"WM_SETICON applied (small={bool(small)}, big={bool(big)})",
        )

    threading.Thread(target=_set_icons, daemon=True).start()
```

`desktop_cmd()` 内 `create_window` / `webview.start` 调用改造:

```python
api = WebViewAPI()
window = webview.create_window(
    "WowooAI Desktop",
    url,
    width=1280,
    height=800,
    text_select=True,
    js_api=api,
)
logger.info("Calling webview.start() (blocks until closed)...")
# Locate icon.ico for the window title-bar / taskbar.
# 打包后(build_win.ps1)icon.ico 与 python.exe 同目录;
# 源码运行时位于 scripts/pack/assets/icon.ico。
icon_path = None
for cand in (
    os.path.join(os.path.dirname(sys.executable), "icon.ico"),
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))),
        "scripts", "pack", "assets", "icon.ico",
    ),
):
    if os.path.exists(cand):
        icon_path = cand
        break
if icon_path:
    logger.info(f"Window icon: {icon_path}")
    if sys.platform == "win32":
        _apply_win_icon(window, icon_path)
webview.start(
    private_mode=False,
    icon=icon_path,
)
```

### 边界

| 场景 | 行为 |
|---|---|
| Windows 打包后启动 | ✅ 命中 `<env_root>/icon.ico`(由 `build_win.ps1` 拷贝),AppUserModelID + WM_SETICON 双重注入,标题栏 / 任务栏均显示品牌蓝色 W,Win11 不再分组到 python.exe |
| Windows 源码运行 | ✅ 命中仓库 `scripts/pack/assets/icon.ico`,行为同上 |
| macOS 任意场景 | ✅ 候选路径均使用 `icon.ico`(macOS bundle 用 `icon.icns` 且不在这两处),`os.path.exists` 均 False → `icon_path = None` → `webview.start(icon=None)`,Cocoa 后端 no-op,继续走 `.app` Resources/icon.icns;`_apply_win_icon` 因 `sys.platform == "win32"` 守卫**不会被调用**,`ctypes.windll` 永远不被触达 |
| HWND 在 10s 内查不到 | ✅ 后台线程 warning 日志后退出,`webview.start(icon=icon_path)` 已生效,降级体验仍正常 |

### 校验

```bash
.venv/bin/python -m py_compile src/wowooai/cli/desktop_cmd.py && echo OK

grep -n '_apply_win_icon\|SetCurrentProcessExplicitAppUserModelID\|WM_SETICON' \
    src/wowooai/cli/desktop_cmd.py
# 期望:函数定义 + sys.platform == "win32" 守卫的调用各 1 处

grep -n '_resolve_window_icon\|window_kwargs' src/wowooai/cli/desktop_cmd.py
# 期望:无命中(旧实现已被取代)
```


## §30 2026-05-06 修复：`save_file` 下载非 ASCII 文件名报 UnicodeEncodeError

### 现象

Windows 桌面包(macOS 同样受影响)中,前端 `pywebview.api.save_file(url, filename)` 触发下载时,若文件名含中文或其他非 ASCII 字符(例:`有效合同_副本.xlsx`),静默失败、保存对话框不弹出。

### 根因

`urllib.request.urlopen()` 把 HTTP request line 当 ASCII 写入 socket。当 URL 路径直接含中文(后端 `send_file_to_user` 返回的同源 URL 不一定是预先编码),Python 在序列化请求行时抛 `UnicodeEncodeError: 'ascii' codec can't encode characters ...`,被 `try/except Exception:` 吞掉,前端只看到 `False`。

### 修复

**文件**:`src/wowooai/cli/desktop_cmd.py` `WebViewAPI.save_file`

进入下载逻辑前对 URL 的 path / query / fragment 做百分号编码,保留协议、host、保留字符不变;`%` 也在 safe list 中,因此对已编码 URL 是幂等的。

```python
# urllib.request.urlopen 把 HTTP request line 当 ASCII 写入 socket;
# 当 URL 含原始非 ASCII(常见于上传文件名 "有效合同_副本.xlsx")时
# 抛 UnicodeEncodeError。这里在所有 urlopen() 调用前一次性把
# path / query / fragment 百分号编码。
from urllib.parse import quote, urlsplit, urlunsplit

parts = urlsplit(url)
safe_chars = "/-_.~!$&'()*+,;=:@%"
encoded_url = urlunsplit((
    parts.scheme,
    parts.netloc,
    quote(parts.path, safe=safe_chars),
    quote(parts.query, safe=safe_chars + "=&"),
    quote(parts.fragment, safe=safe_chars),
))
```

后续两个 `urlopen()` 调用统一使用 `encoded_url`:

```python
# 1) 推断扩展名的 fallback HEAD/GET
with urllib.request.urlopen(encoded_url) as resp:
    ct = resp.headers.get("Content-Type", "")
    ...

# 2) 真正下载到 dest_path
with urllib.request.urlopen(encoded_url) as response:
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(response, f)
```

### 边界

| 输入 URL | 编码后行为 |
|---|---|
| `http://127.0.0.1:8088/files/有效合同_副本.xlsx` | path 部分 `quote` → `%E6%9C%89...`,`urlopen` 成功 |
| `http://127.0.0.1:8088/files/already%20encoded.pdf` | `%` 在 safe_chars,幂等不双重编码 |
| 含 `?key=值&x=1` 的 query | `quote` 保留 `=&`,值部分编码 |
| 纯 ASCII URL | `quote` 全部命中 safe_chars,字符串等价,无副作用 |
| 非 http(s) URL | 函数顶部 `if not url.startswith(("http://","https://")): return False` 提前退出,不进入编码逻辑 |

### 平台影响

| 平台 | 影响 |
|---|---|
| Windows 打包包 | ✅ 修复主诉(中文上传文件下载) |
| macOS 打包包 | ✅ 同样修复——pywebview Cocoa 后端走的是同一个 Python 调用栈,`urlopen` 的 ASCII 限制与平台无关 |
| 源码运行 | ✅ 同上,纯 stdlib 改动 |

### 校验

```bash
.venv/bin/python -m py_compile src/wowooai/cli/desktop_cmd.py && echo OK

grep -n 'encoded_url\|urlsplit\|urlunsplit' src/wowooai/cli/desktop_cmd.py
# 期望:1 处构造 encoded_url + 2 处 urlopen(encoded_url)

# 行为校验(开发机):构造一个文件名含中文的 GET endpoint,
# 通过桌面前端触发下载,期望保存对话框正常弹出且文件落盘。
```


## §31 2026-05-07 增量：内置 pandoc 即开即用（pypandoc-binary + PATH 注入）

### 背景

`docx-zh` / `docx-en` skill 通过 `execute_shell_command("pandoc ...")` 调用 pandoc 做 docx ↔ markdown 转换。客户端机器若未单独安装 pandoc，命令直接 `command not found`。仓库内无 `import pypandoc` 调用，全部为 shell CLI 形式。

### 改动一：`pyproject.toml` desktop extras 末尾追加 pypandoc-binary

**文件**：`pyproject.toml`

`[project.optional-dependencies] desktop = [...]` 列表末尾追加一行：

```toml
desktop = [
    ...
    "beautifulsoup4>=4.12",
    "markdownify>=0.13",
    "pypandoc-binary>=1.13",
]
```

`pypandoc-binary` 与 `pypandoc` 的区别：前者把 pandoc 可执行文件直接打进 wheel（落到 `site-packages/pypandoc/files/pandoc`），后者只提供 Python 包装、要求系统已装 pandoc。桌面包要"即开即用"必须用 binary 版。

### 改动二：`src/wowooai/cli/desktop_cmd.py` subprocess env 注入 PATH

**文件**：`src/wowooai/cli/desktop_cmd.py`

定位：launcher 启动后端 subprocess 前的 `env = os.environ.copy()` 之后、`env["WOWOOAI_PARENT_PID"] = str(os.getpid())` 之后追加：

```python
env = os.environ.copy()
env[LOG_LEVEL_ENV] = log_level
env["WOWOOAI_PARENT_PID"] = str(os.getpid())

try:
    import pypandoc
    pandoc_dir = os.path.dirname(pypandoc.get_pandoc_path())
    env["PATH"] = pandoc_dir + os.pathsep + env.get("PATH", "")
except Exception:
    pass
```

效果：launcher 把 pypandoc-binary 自带的 pandoc 目录前置到子进程 PATH，后端 subprocess 起来后所有 `execute_shell_command("pandoc ...")` 直接命中打包内置的 pandoc。

### 改动三：`src/wowooai/cli/app_cmd.py` 进程内 PATH 注入

**文件**：`src/wowooai/cli/app_cmd.py`

定位：`setup_logger(log_level)` / `_start_parent_watchdog()` 之后追加：

```python
setup_logger(log_level)
_start_parent_watchdog()

try:
    import pypandoc
    pandoc_dir = os.path.dirname(pypandoc.get_pandoc_path())
    os.environ["PATH"] = pandoc_dir + os.pathsep + os.environ.get("PATH", "")
except Exception:
    pass
```

效果：覆盖直接 `wowooai app` 启动（非桌面 launcher 链路）的场景。两处都做 PATH 注入是为了让两条启动路径都"即开即用"，桌面 launcher 走改动二、CLI 直起走改动三。

### 为什么不需要其它依赖做同样处理

仅 pandoc 一项是 skill 通过 shell 命令名调用的外部二进制；其它 desktop extras 全部走 Python `import`（`openpyxl` / `python-docx` / `pypdf` / `pillow` 等）或库内部直接 dlopen 自带 `.dylib`（`pypdfium2`），不依赖 OS PATH。

### 复刻校验

```bash
.venv/bin/python -m py_compile \
  src/wowooai/cli/app_cmd.py \
  src/wowooai/cli/desktop_cmd.py

grep -n 'pypandoc-binary' pyproject.toml
# 期望：1 处命中

grep -n 'pypandoc.get_pandoc_path' \
  src/wowooai/cli/app_cmd.py \
  src/wowooai/cli/desktop_cmd.py
# 期望：每个文件各 1 处命中

# 装上 desktop extras 后实际验证 pandoc 路径可解析
.venv/bin/pip install 'pypandoc-binary>=1.13'
.venv/bin/python -c "import pypandoc, os; print(os.path.dirname(pypandoc.get_pandoc_path()))"
# 期望：输出形如 /.../site-packages/pypandoc/files

# 启动后端，shell 命令应能找到 pandoc
.venv/bin/python -m wowooai app --host 127.0.0.1 --port 8088 &
curl -sS -X POST http://127.0.0.1:8088/api/agents/default/tools/execute_shell_command \
  -H 'Content-Type: application/json' \
  -d '{"command": "pandoc --version | head -1"}'
# 期望：返回 pandoc 版本字符串，无 command not found
```

---

## §32 2026-05-09 修复：默认开启 auto_memory_interval，修复记忆系统空转

### 背景

记忆系统设计了两层落盘通道：

1. **Summarizer**（由 `auto_memory_interval` 控制）：每 N 轮用户消息后，后台 ReAct agent 把对话精华写入 `memory/YYYY-MM-DD.md`。
2. **Dream**（由 `dream_cron` 控制，默认每晚 23:00）：读取 `memory/YYYY-MM-DD.md`，提炼到 `MEMORY.md`。

Dream 依赖 Summarizer 产出的 daily log。但 `auto_memory_interval` 默认值为 `None`（关闭），导致 Summarizer 从未触发 → `memory/` 目录永远为空 → Dream 每晚空转（"今日日志未生成，无增量"）→ `MEMORY.md` 永远停留在初始模板状态。

### 根因

`src/wowooai/config/config.py` 中 `ReMeLightMemoryConfig.auto_memory_interval` 默认 `None`，`post_reply` 钩子在 `light_context_manager.py:996` 直接 `return None` 跳过整个逻辑。

### 改动

**源码**（1 处）：

| 文件 | 行 | 变更 |
|---|---|---|
| `src/wowooai/config/config.py:557` | `auto_memory_interval` Field | `default=None` → `default=5` |

**文档**（6 处，同步默认值描述）：

| 文件 | 变更 |
|---|---|
| `website/public/docs/config.zh.md` | 默认值 `null` → `5` |
| `website/public/docs/config.en.md` | 默认值 `null` → `5` |
| `website/public/docs/memory.zh.md` | 默认值 `null` → `5` |
| `website/public/docs/memory.en.md` | 默认值 `null` → `5` |
| `website/public/docs/memory-evolving-and-proactive.zh.md` | "关闭/默认关闭" → "`5`（开启）/默认开启" |
| `website/public/docs/memory-evolving-and-proactive.en.md` | "Off/Disabled by default" → "`5` (On)/Enabled by default" |

### 影响范围

- **新安装用户**：自动每 5 轮对话触发 Summarizer，记忆系统即开即用。
- **已有用户（agent.json 无该字段）**：Pydantic 填充默认值 5，自动生效。
- **已有用户（agent.json 显式设为 null）**：保持关闭不变，用户主动选择不受干预。
- **Token 消耗**：每 5 轮用户消息额外一次后台 LLM 调用（Summarizer ReAct agent）。

### 复刻校验

```bash
# 验证默认值
.venv/bin/python -c "from wowooai.config.config import ReMeLightMemoryConfig; print(ReMeLightMemoryConfig().auto_memory_interval)"
# 期望：5

# 编译验证
.venv/bin/python -m py_compile src/wowooai/config/config.py
```

---

## §33 2026-05-12 增量：新增 desktop_input / desktop_app 工具与 desktop_control 内置 skill

### 背景

WowooAI 之前只能通过 `browser_use` 操作网页，无法打开本机 app（Excel、钉钉、内部 ERP 等）并触发点击/输入。`execute_shell_command` 虽已可调用 `osascript` / `powershell` 启动 app，但缺少结构化的鼠标/键盘注入与跨平台抽象，模型难以稳定完成「打开 app → 看屏幕 → 点击 → 验证」的闭环。

本次增量分阶段：**阶段 1（本次）**落地视觉派 MVP —— 截屏 + 屏幕坐标输入 + app 生命周期管理；**阶段 2（后续）**再为 1-2 个高频 app 增加结构化适配（macOS AX 树 / Windows UIA）。权限引导、签名 / notarization 不在本次范围。

### 改动一：新增内置工具 `desktop_input`

**新增文件**：`src/wowooai/agents/tools/desktop_input.py`

仿 `browser_use` 的 action-based API，单个 async 函数承载 9 个 action + 1 个预留 action：

```python
async def desktop_input(
    action: str,
    x: Optional[int] = None,
    y: Optional[int] = None,
    x2: Optional[int] = None,
    y2: Optional[int] = None,
    text: Optional[str] = None,
    keys: Optional[List[str]] = None,
    button: str = "left",
    clicks: int = 1,
    duration: float = 0.3,
    dy: int = 0,
) -> ToolResponse:
    ...
```

支持的 action：`screen_size` / `move_to` / `click` / `double_click` / `right_click` / `drag` / `type_text` / `press_keys` / `scroll` / `query`（`query` 为阶段 2 预留位，当前返回 `not_implemented`）。

底层用 `pyautogui` 注入鼠标键盘事件。跨平台键名归一化通过 `_normalize_key` 完成：

```python
_KEY_ALIAS_WIN = {"cmd": "win", "command": "win", "meta": "win",
                  "option": "alt", "return": "enter"}
_KEY_ALIAS_MAC = {"meta": "cmd", "command": "cmd", "win": "cmd",
                  "option": "alt", "return": "enter"}
```

模型始终用 macOS 写法（`cmd` / `option`），工具内部自动映射到对应平台。

安全护栏：
- 单次调用只执行 1 个 action（不接收脚本式批量）
- 屏外坐标返回错误，**不静默裁剪**（强制调用方重新评估）
- 不暴露剪贴板读写 / 截屏 / 录制（截屏走 `desktop_screenshot`，文件走 `read_file`）
- `pyautogui.FAILSAFE = False`（避免左上角触发紧急中断 abort 整个工具）

返回值统一为 `ToolResponse` 包裹 `TextBlock(json=...)`，与 `desktop_screenshot._tool_ok` / `_tool_error` 风格一致。

### 改动二：新增内置工具 `desktop_app`

**新增文件**：`src/wowooai/agents/tools/desktop_app.py`

跨平台 app 生命周期与窗口聚焦：

```python
async def desktop_app(
    action: str,
    name_or_path: Optional[str] = None,
    name: Optional[str] = None,
    title_substring: Optional[str] = None,
) -> ToolResponse:
    ...
```

5 个 action：`launch` / `activate` / `list_windows` / `focus_window` / `quit`。内部按 `sys.platform == "darwin"` / `"win32"` 分支：

| Action | macOS 实现 | Windows 实现 |
|---|---|---|
| launch | `open -a <name>` / `open <path>` | `Start-Process` (PowerShell) |
| activate | `osascript -e 'tell application "X" to activate'` | `Microsoft.VisualBasic.Interaction::AppActivate` |
| list_windows | `osascript` 枚举 System Events 窗口（`process / window`），输出 `app\ttitle` 行；解析为 `[{app, title}]` | PowerShell `Get-Process | Where-Object MainWindowTitle` → JSON |
| focus_window | AppleScript 遍历 process / window，匹配 `name of w contains <sub>`，`set frontmost` + `AXRaise` | 同 activate（按子串） |
| quit | AppleScript `tell ... to quit` | PowerShell `CloseMainWindow()` |

`list_windows` 的 AppleScript 用 try / on error 包裹 `count of windows` 和 `name of w`，避免某些进程没窗口或窗口无标题导致 `-1700` 类型错误中断整个枚举。

护栏：
- 不在 macOS/Windows 之外的平台返回结果（直接报 `desktop_app currently supports macOS and Windows only`）
- AppleScript 字符串通过 `_osa_escape` 转义反斜杠和双引号
- PowerShell 参数通过 `shlex.quote` 转义

### 改动三：注册到 toolkit（三处）

**文件 1**：`src/wowooai/agents/tools/__init__.py`

```python
from .desktop_screenshot import desktop_screenshot
from .desktop_input import desktop_input
from .desktop_app import desktop_app
# ...
__all__ = [
    ...
    "desktop_screenshot",
    "desktop_input",
    "desktop_app",
    ...
]
```

**文件 2**：`src/wowooai/agents/react_agent.py`

import 列表追加 `desktop_input`、`desktop_app`；`_create_toolkit` 内 `tool_functions` dict 追加：

```python
tool_functions = {
    ...
    "desktop_screenshot": desktop_screenshot,
    "desktop_input": desktop_input,
    "desktop_app": desktop_app,
    ...
}
```

`BuiltinToolConfig` 默认 `enabled=True`，所以未在 agent.json 显式配置时即开即用。

**文件 3**：`src/wowooai/config/config.py`

`_default_builtin_tools()` 中 `desktop_screenshot` 条目之后追加：

```python
"desktop_input": BuiltinToolConfig(
    name="desktop_input",
    enabled=True,
    description="Inject mouse / keyboard input on the local desktop",
    icon="🖱️",
),
"desktop_app": BuiltinToolConfig(
    name="desktop_app",
    enabled=True,
    description="Launch, focus and quit native desktop apps",
    icon="🪟",
),
```

### 改动四：新增双语 SKILL.md（`desktop_control`）

**新增文件**：
- `src/wowooai/agents/skills/desktop_control-zh/SKILL.md`
- `src/wowooai/agents/skills/desktop_control-en/SKILL.md`

frontmatter 仿 `browser_visible-zh/SKILL.md`：

```yaml
---
name: desktop_control
description: "当用户需要操作本机桌面应用（Excel、钉钉、内部 ERP 等）..."
metadata:
  builtin_skill_version: "1.0"
  wowooai:
    emoji: "🖥️"
    requires: {}
---
```

skill 文档强制约束：

- **强制循环**：每次 `desktop_input` 前后必须配合 `desktop_screenshot` 截屏验证
- **坐标换算**：Retina 屏截图像素是真实屏幕坐标的 2 倍，先调 `desktop_input(action="screen_size")` 取真实尺寸，再按比例换算
- **失败兜底**：点击未生效 → `desktop_app.activate` 重聚焦 → 重截屏；连续 2 次失败停止
- **职责划分**：网页任务一律 `browser_use`；Office 文件能用 Python 处理的优先用 `xlsx` / `docx` / `pptx` / `pdf` skill，不要点 GUI
- **单步动作**：一次调用只触发一个 action，批量场景拆成多次调用

### 改动五：默认 agent 模板装入新 skill

**文件**：`src/wowooai/agents/templates.py`

`DEFAULT_TEMPLATE_SKILL_NAMES` 末尾追加 `"desktop_control"`：

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
    "desktop_control",
)
```

新建 default agent 时自动启用该 skill；老 agent 不受影响（只对新创建的工作区生效）。

### 改动六：`pyproject.toml` desktop extras 追加运行时依赖

**文件**：`pyproject.toml`

`[project.optional-dependencies] desktop = [...]` 末尾追加：

```toml
desktop = [
    ...
    "markdownify>=0.13",
    "pypandoc-binary>=1.13",
    "pyautogui>=0.9.54",
    "pynput>=1.7.6",
    "pywin32>=306; sys_platform == 'win32'",
    "pyobjc-framework-Quartz>=10.0; sys_platform == 'darwin'",
]
```

依赖说明：
- `pyautogui`：跨平台鼠标键盘注入（`desktop_input` 主驱动）
- `pynput`：备选输入注入路径（未来回退用）
- `pywin32`：仅 Windows，未来 `desktop_app.list_windows` 走 `EnumWindows` 时使用
- `pyobjc-framework-Quartz`：仅 macOS，已在桌面包内可用（不会增量打包负担）

打包脚本（`scripts/pack/build_macos.sh` / `build_win.ps1`）走现有 conda env / `PACKBOT_BASE_ENV` 路径即可，新依赖随 `pip install '.[desktop]'` 进入打包环境，**无需新增 bundle 步骤**。

### 阶段 1 不做的事（明确 Out of Scope）

- 不引入 macOS Accessibility / Screen Recording 授权引导（首次使用由系统弹窗，需用户手动同意）
- 不接 macOS AX 树 / Windows UIA 结构化查询（留 `query` action 作为阶段 2 接入位）
- 不做录制 / 回放 / 宏 / OCR
- 不动 `browser_use` 任何逻辑

### 复刻校验

```bash
# 编译验证
.venv/bin/python -m py_compile \
  src/wowooai/agents/tools/desktop_input.py \
  src/wowooai/agents/tools/desktop_app.py \
  src/wowooai/agents/tools/__init__.py \
  src/wowooai/agents/react_agent.py \
  src/wowooai/config/config.py \
  src/wowooai/agents/templates.py

# 工具注册
grep -n 'desktop_input\|desktop_app' \
  src/wowooai/agents/tools/__init__.py \
  src/wowooai/agents/react_agent.py
# 期望：tools/__init__.py 4 处命中（2 import + 2 __all__），
#       react_agent.py 4 处命中（2 import + 2 tool_functions）

grep -n '"desktop_input"\|"desktop_app"' src/wowooai/config/config.py
# 期望：2 处命中

grep -n 'desktop_control' src/wowooai/agents/templates.py
# 期望：1 处命中（DEFAULT_TEMPLATE_SKILL_NAMES）

# SKILL.md 存在
ls src/wowooai/agents/skills/desktop_control-zh/SKILL.md \
   src/wowooai/agents/skills/desktop_control-en/SKILL.md

# pyproject 新依赖
grep -n 'pyautogui\|pynput\|pywin32\|pyobjc-framework-Quartz' pyproject.toml
# 期望：4 处命中

# 装上后烟测（macOS）
.venv/bin/pip install -e '.[desktop]'
.venv/bin/python - <<'PY'
import asyncio
from wowooai.agents.tools.desktop_input import desktop_input
from wowooai.agents.tools.desktop_app import desktop_app

async def main():
    print((await desktop_input(action="screen_size")).content[0])
    print((await desktop_input(action="click", x=-5, y=-5)).content[0])  # 期望 error
    print((await desktop_input(action="query")).content[0])              # 期望 not_implemented
    print((await desktop_app(action="launch")).content[0])               # 期望 error: requires name_or_path
    print((await desktop_app(action="list_windows")).content[0])         # 期望 ok（macOS 需开辅助功能授权才有内容）

asyncio.run(main())
PY
```


---

## §34 2026-05-14 增量：renliwo_browser 多站点适配（新增 qd_system，host 前缀通配自动路由）

> 让 `renliwo_browser` 工具从「只服务 ereference 一个站点」演进为「多 renliwo 子系统共用一个 Playwright 引擎」。本节落地新增 QD 外包管理系统（qd_system）支持；未来再新增 renliwo 子站时，只需 `cp -r` 一个目录、不动 Python 源码。
>
> ⚠️ **核心硬性约束（已落地）**：登录账号 / 密码 **不允许出现在源码或仓库内任何 JSON**。凭据只从 `config.json > plugins.renliwo` 运行时读取。

### §34.1 改造目标

| # | 目标 | 落地方式 |
|---|---|---|
| 1 | 一个工具支持多个 renliwo 子站 | 引入 `_SITES` 注册表，按 `renliwo_browser_data/<site_id>/site.json` 自动加载 |
| 2 | 按 host 自动识别当前站点 | `site.json.host_patterns` + `fnmatch`，支持前缀通配（如 `qd-system*.renliwo.com`） |
| 3 | hash 路由 / path 路由抽象统一 | `site.json.routing.type ∈ {"hash", "path"}`，`_route_from_url()` 分支 |
| 4 | 登录配置数据化 | `site.json.login` 提供 url_path / username_selector / password_selector / submit_selector / submit_button_text |
| 5 | 凭据按 site_id 分隔，源码零账号 | `plugins.renliwo[site_id] = {username, password}`；legacy 顶层 `{username, password}` 仅 ereference 兼容 |
| 6 | sidebar-only 站点禁用 nav_menu | `_action_nav_menu` 检测 `navigation.type == "sidebar_only"` 时直接报错并引导用户改用 `nav_submenu` |
| 7 | guide 索引兼容两种 schema | ereference 预计算 `route_index`；qd_system 只给 flat `pages[]`，工具用 `_build_route_index()` 在内存懒构建 |

### §34.2 目录布局

```
src/wowooai/agents/tools/
├── renliwo_browser.py                          # 多站点引擎（修改）
└── renliwo_browser_data/
    ├── ereference/                             # 人力窝主站（从旧的扁平结构迁入）
    │   ├── site.json
    │   ├── guide_index.json                    # 已含 route_index（预计算）
    │   └── 页面结构文档_完整版.md
    └── qd_system/                              # QD 外包管理系统（新增）
        ├── site.json
        ├── guide_index.json                    # 只有 pages[]，工具懒构建 route_index
        └── 页面结构文档_完整版.md
```

> 旧的扁平文件 `renliwo_browser_data/renliwo_guide_index.json` / `Renliwo页面结构文档_完整版.md` 已删除，相关常量 `_GUIDE_INDEX` / `_GUIDE_DOC_PATH` 在工具中也已下线，复刻时不要再保留。

### §34.3 site.json schema（**严禁含账号密码**）

```json
{
  "site_id": "qd_system",
  "system_name": "QD系统(外包管理系统)",
  "host_patterns": ["qd-system*.renliwo.com"],
  "default_base_url": "https://qd-system-front-demo.renliwo.com",
  "routing": { "type": "path", "hash_prefix": null },
  "login": {
    "url_path": "/user/login",
    "username_selector": "#username",
    "password_selector": "#password",
    "submit_selector": "button",
    "submit_button_text": "Login",
    "after_login_redirect": "/addStaff/front"
  },
  "navigation": {
    "type": "sidebar_only",
    "sidebar_selector": ".ant-menu-inline"
  },
  "guide_index": "guide_index.json",
  "doc_path": "页面结构文档_完整版.md"
}
```

ereference 版本 `routing.type="hash"` / `navigation.type="top_and_sidebar"` / `login.url_path="/#/login"`。

字段含义：
- **host_patterns**：`fnmatch` 通配。`qd-system*.renliwo.com` 同时覆盖 `qd-system-front-demo.renliwo.com` / `qd-system-uat.renliwo.com` / `qd-system-front-test.renliwo.com` 等环境。
- **routing.type**：`hash` 表示 `#/route` 形式，`path` 表示常规 `/route` 形式。决定 `_route_from_url()` 取哪一段。
- **navigation.type**：`top_and_sidebar` 允许 `nav_menu` + `nav_submenu`；`sidebar_only` 只允许 `nav_submenu`，`nav_menu` 会被工具拒绝并返回友好错误。
- **login.submit_button_text**：可选；当登录按钮没有稳定 class（QD 的 `button` 选择器太宽），用文本辅助定位 `button:has-text("Login")`。

### §34.4 凭据配置（运行时，源码零账号）

`config.json`：

```json
{
  "plugins": {
    "renliwo": {
      "ereference": { "username": "...", "password": "..." },
      "qd_system":  { "username": "...", "password": "..." }
    }
  }
}
```

兼容老用户的 ereference 旧扁平格式（**只对 ereference 生效**）：

```json
{
  "plugins": {
    "renliwo": { "username": "...", "password": "..." }
  }
}
```

工具内查找顺序（每个 site 独立）：
1. `plugins.renliwo[site_id]`（首选）
2. `plugins.renliwo.sites[site_id]`（备选 schema）
3. `plugins.renliwo` 顶层（**仅 ereference**，向后兼容；其他站点必须用 1 / 2 的嵌套形式）

### §34.5 工具源码关键改动（[src/wowooai/agents/tools/renliwo_browser.py](../../src/wowooai/agents/tools/renliwo_browser.py)）

1. 新增 imports：`import fnmatch`、`from urllib.parse import urlparse`。
2. 新增模块级注册表 `_SITES: dict[str, dict]`，`_load_all_sites()` 在 import 时扫描 `renliwo_browser_data/<site_id>/site.json` 并加载（含 guide_index 懒构建）。
3. 新增 helper：
   - `_site_for_host(host)` — fnmatch 通配匹配（大小写不敏感）
   - `_site_for_url(url)` — 解析 URL host → `_site_for_host`
   - `_site_by_id(site_id)` — 直接按 ID 取
   - `_resolve_site(state, page_id, explicit_site_id)` — 三段式优先级：explicit > 当前 page URL > `state["active_site_id"]`
   - `_route_from_url(url, site)` — 按 `routing.type` 切 hash / path
   - `_build_route_index(guide_index)` — flat pages → route_index 懒构建
   - `_guide_for_route(site, route)` / `_guide_routes_summary(site)` / `_guide_for_doc_ref(site)`
4. `_make_fresh_state()` 增加 `"active_site_id": None`，登录 / 打开成功时回写当前 site_id。
5. `_action_login` / `_action_open` / `_action_nav_menu` / `_guide_for_current_page` 全部从 site 配置取参数；不再读模块级全局。
6. `_action_nav_menu` 在 `navigation.type == "sidebar_only"` 时直接返回友好错误，提示改用 `nav_submenu`。
7. `renliwo_browser(...)` 主函数新增 `site_id: str = ""` 参数，对 `open` / `login` / `guide` 三个 action 显式透传。其他 action（snapshot / click / type / export / nav_submenu / ant_select 等）一律按当前 page URL 自动识别 site，调用方无需感知。

### §34.6 复刻步骤

1. 把 [docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser.py](source-bundle/src/wowooai/agents/tools/renliwo_browser.py) 整文件覆盖到 [src/wowooai/agents/tools/renliwo_browser.py](../../src/wowooai/agents/tools/renliwo_browser.py)。
2. 复制两个站点目录：

   ```bash
   SB=docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser_data
   DST=src/wowooai/agents/tools/renliwo_browser_data

   mkdir -p "$DST/ereference" "$DST/qd_system"
   cp "$SB/ereference/site.json"        "$DST/ereference/site.json"
   cp "$SB/ereference/guide_index.json" "$DST/ereference/guide_index.json"
   cp "$SB/ereference/页面结构文档_完整版.md" "$DST/ereference/页面结构文档_完整版.md"
   cp "$SB/qd_system/site.json"         "$DST/qd_system/site.json"
   cp "$SB/qd_system/guide_index.json"  "$DST/qd_system/guide_index.json"
   cp "$SB/qd_system/页面结构文档_完整版.md" "$DST/qd_system/页面结构文档_完整版.md"
   ```

3. 删除旧扁平文件（如果仓库内仍存在）：

   ```bash
   rm -f src/wowooai/agents/tools/renliwo_browser_data/renliwo_guide_index.json \
         src/wowooai/agents/tools/renliwo_browser_data/Renliwo页面结构文档_完整版.md
   ```

4. 在用户的 `config.json` 中按 §34.4 配置 `plugins.renliwo.<site_id> = {username, password}`。**仓库本身不再写凭据**。

### §34.7 新增 renliwo 子站的步骤（未来扩展）

无需改 Python，只需：

```bash
mkdir -p src/wowooai/agents/tools/renliwo_browser_data/<new_site_id>
# 1. 写 site.json（host_patterns 用前缀通配；routing.type 选 hash 或 path）
# 2. 写 guide_index.json（最简形式：{"pages": [{"route": "...", "module": "...", "page_name": "...", ...}]}）
# 3. （可选）放 页面结构文档_完整版.md 给模型 fallback 阅读
# 4. 在 config.json > plugins.renliwo 加上对应 site_id 的账号密码
# 5. 重启进程，工具会在 import 时自动加载
```

### §34.8 验证（已通过）

```bash
.venv/bin/python3 - <<'PY'
import sys, json
sys.path.insert(0, "src")
from wowooai.agents.tools.renliwo_browser import (
    _SITES, _resolve_site, _site_for_url, _route_from_url, _guide_for_route,
)

# 1) 多站点注册
assert sorted(_SITES) == ["ereference", "qd_system"]
assert _SITES["ereference"]["routing"]["type"] == "hash"
assert _SITES["qd_system"]["routing"]["type"] == "path"

# 2) host 前缀通配（含大小写、错字、缺前缀）
assert _site_for_url("https://qd-system-front-demo.renliwo.com/x")["site_id"] == "qd_system"
assert _site_for_url("https://qd-system-uat.renliwo.com/x")["site_id"] == "qd_system"
assert _site_for_url("https://EREFERENCE-V-UAT.renliwo.com/#/")["site_id"] == "ereference"
assert _site_for_url("https://ereferenc-v-uat.renliwo.com/x") is None    # 错字
assert _site_for_url("https://ereference.renliwo.com/x") is None         # 缺 -v 前缀
assert _site_for_url("https://example.com/x") is None

# 3) 路由抽取（hash vs path）
assert _route_from_url("https://x/#/a/b?q=1",
                       _SITES["ereference"]) == "#/a/b"
assert _route_from_url("https://x/a/b?q=1",
                       _SITES["qd_system"]) == "/a/b"

# 4) _resolve_site 三段式优先级
state = {"active_site_id": "ereference", "pages": {}}
assert _resolve_site(state, "default", "qd_system")["site_id"] == "qd_system"   # explicit 最高
assert _resolve_site(state, "default", "")["site_id"] == "ereference"           # 回退 active

# 5) sidebar_only 站点拒绝 nav_menu
assert _SITES["qd_system"]["navigation"]["type"] == "sidebar_only"

# 6) QD 懒构建 route_index 后能命中 /addStaff/front
g = _guide_for_route(_SITES["qd_system"], "/addStaff/front")
assert g and g["page_name"] == "增员派单"

print("ALL OK")
PY
```

校验源码与配置中均无明文凭据：

```bash
# 工具源码 / 站点配置 / 索引中不应出现非占位的 username/password
python3 - <<'PY'
import json, re, pathlib
for p in pathlib.Path("src/wowooai/agents/tools/renliwo_browser_data").rglob("*.json"):
    s = p.read_text(encoding="utf-8")
    for m in re.finditer(r'"(username|password)"\s*:\s*"([^"]+)"', s):
        if m.group(2) != "...":
            print("LEAK", p, m.group(0))
print("scan done")
PY
```

### §34.9 不做（明确 Out of Scope）

- 不引入 renliwo-only SKILL（按用户决策；多站点能力作为工具能力直接暴露，模型按工具 docstring 学习用法）。
- 不再用全局 `_GUIDE_INDEX` / `_GUIDE_DOC_PATH` 等模块级常量；如复刻时看到旧代码请整段删除。
- 不在工具内做凭据存储 / 加密 / 任何二次写入：账号永远只读自 `config.json`，工具不持久化、不打日志、不返回给模型。


---

## §35 2026-05-14 增量：browser_use / renliwo_browser 默认有头模式 + 登录交给用户

> 两个浏览器自动化工具统一行为：默认有头模式（可见窗口），仅当用户明确要求时才走无头；登录/账号密码/验证码一律交给用户在可见窗口手动完成，禁止自动填充。

### §35.1 改动总览

| 模块 | 改动 |
|---|---|
| `browser_control.py` | `headed` 参数默认 `True`；`_make_fresh_state` headless 默认 `False`；docstring 明确登录交给用户 |
| `renliwo_browser.py` | `headed` 参数默认 `True`；`_make_fresh_state` / `_action_status` headless 默认 `False`；docstring 明确登录交给用户；`start` 描述从"headless"改为"默认有头/可见窗口" |
| `browser_visible-zh/SKILL.md` | v1.3→1.4；描述更新；新增"登录/账号密码/验证码处理"章节；示例默认改为有头 |
| `browser_visible-en/SKILL.md` | v1.2→1.3；同上英文版 |
| `browser_cdp-zh/SKILL.md` | v1.2→1.3；示例从 `"headed": true` 改为 `"headed": false`（因默认已是有头）；Notes 增加登录规则 |
| `browser_cdp-en/SKILL.md` | v1.2→1.3；同上英文版 |

### §35.2 核心行为变更

**默认有头模式**：

```python
# browser_control.py
async def browser_use(..., headed: bool = True, ...) -> ToolResponse:
    ...

# renliwo_browser.py
async def renliwo_browser(..., headed: bool = True, ...) -> ToolResponse:
    ...
async def _action_start(state: dict, headed: bool = True) -> ToolResponse:
    ...
```

`_make_fresh_state` 中 `"headless": False`（两个工具均已统一）。

**登录交给用户**（SKILL.md 中以强制规则明确）：

- 绝对禁止使用 `action=type` 自动填写账号、密码、验证码、短信 OTP
- 确保浏览器运行在有头模式（默认即是）
- 告知用户在可见窗口里手动完成登录
- 等待用户确认"已登录"后再继续自动化操作
- 即使配置或环境变量中存在账号密码，也不要自动填充

### §35.3 涉及文件

| 文件 | 类型 |
|---|---|
| `src/wowooai/agents/tools/browser_control.py` | 修改 |
| `src/wowooai/agents/tools/renliwo_browser.py` | 修改 |
| `src/wowooai/agents/skills/browser_visible-zh/SKILL.md` | 修改 |
| `src/wowooai/agents/skills/browser_visible-en/SKILL.md` | 修改 |
| `src/wowooai/agents/skills/browser_cdp-zh/SKILL.md` | 修改 |
| `src/wowooai/agents/skills/browser_cdp-en/SKILL.md` | 修改 |

### §35.4 校验

```bash
# 1. 两个工具的 headed 默认值
grep -n 'headed.*bool.*=.*True' src/wowooai/agents/tools/browser_control.py src/wowooai/agents/tools/renliwo_browser.py
# 期望：两个文件各命中至少 1 处

# 2. _make_fresh_state headless 默认 False
grep -n '"headless": False' src/wowooai/agents/tools/browser_control.py src/wowooai/agents/tools/renliwo_browser.py
# 期望：两个文件各命中 1 处

# 3. SKILL.md 版本
grep 'builtin_skill_version' \
  src/wowooai/agents/skills/browser_visible-zh/SKILL.md \
  src/wowooai/agents/skills/browser_visible-en/SKILL.md \
  src/wowooai/agents/skills/browser_cdp-zh/SKILL.md \
  src/wowooai/agents/skills/browser_cdp-en/SKILL.md
# 期望：visible-zh=1.4, visible-en=1.3, cdp-zh=1.3, cdp-en=1.3

# 4. 登录规则存在
grep -l '禁止.*自动填' src/wowooai/agents/skills/browser_visible-zh/SKILL.md src/wowooai/agents/skills/browser_cdp-zh/SKILL.md
grep -l 'never auto-fill' src/wowooai/agents/skills/browser_visible-en/SKILL.md src/wowooai/agents/skills/browser_cdp-en/SKILL.md
# 期望：各 2 个文件命中

# 5. 编译
.venv/bin/python3 -c "from wowooai.agents.tools.browser_control import browser_use; from wowooai.agents.tools.renliwo_browser import renliwo_browser; print('OK')"
```

---

## §36 2026-05-14 修复：macOS Dock 图标错误显示为通用 "exec" 图标（desktop_cmd.py 平台分流）

### 现象

打包后的 `WowooAI.app` 在 macOS Dock / 程序坞 / Cmd-Tab 切换器中显示通用 "exec" 图标，而不是品牌蓝 W logo。

### 根因（仅记录后端侧）

[src/wowooai/cli/desktop_cmd.py:367-378](../../src/wowooai/cli/desktop_cmd.py#L367-L378)（修复前）只查找 `icon.ico`（Windows 格式），从来不查 `icon.icns`：

```python
icon_path = None
for cand in (
    os.path.join(os.path.dirname(sys.executable), "icon.ico"),
    os.path.join(..., "scripts", "pack", "assets", "icon.ico"),
):
    if os.path.exists(cand):
        icon_path = cand
        break
```

macOS .app bundle 里候选路径都不存在 → `icon_path = None` → `webview.start(icon=None)`。pywebview cocoa.py 仅在 icon 非空时调用 `setApplicationIconImage_`（[`webview/platforms/cocoa.py` 约 L628-L630]），所以运行时 Dock 图标永远不被覆盖。

> 配套的 macOS Info.plist `CFBundlePackageType=APPL` / `CFBundleInfoDictionaryVersion=6.0` 补齐属于打包脚本变更，详见 [packaging-macos.md §14](packaging-macos.md#14-2026-05-14-修复macos-dock-图标错误显示为通用-exec-图标)。

### 修复

`src/wowooai/cli/desktop_cmd.py` 的 icon 路径探测���为按平台分流：

```python
if sys.platform == "darwin":
    icon_name = "icon.icns"
    candidates = (
        os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(sys.executable))),
            icon_name,
        ),
        os.path.join(repo_assets, icon_name),
    )
else:
    icon_name = "icon.ico"
    candidates = (
        os.path.join(os.path.dirname(sys.executable), icon_name),
        os.path.join(repo_assets, icon_name),
    )
```

macOS 路径推算：`sys.executable = <bundle>/Contents/Resources/env/bin/WowooAI`，往上跳 3 层 → `<bundle>/Contents/Resources`，`icon.icns` 由 `build_macos.sh` 复制到该位置。

`webview.start(icon=icon_path)` 命中后，pywebview cocoa.py 会调用 `NSApplication.setApplicationIconImage_`，在窗口显示后立即覆盖 Dock 图标，**与 Info.plist 的 `CFBundleIconFile` 形成双保险**。

### Windows 影响评估

| 检查项 | 结论 |
|---|---|
| `icon.ico` 候选路径 | ✅ 不变 — `os.path.dirname(sys.executable) + "icon.ico"` 与 `scripts/pack/assets/icon.ico` 都保留 |
| `_apply_win_icon` 调用 | ✅ 仍在 `sys.platform == "win32"` 守卫下调用，路径未动 |
| `webview.start(icon=icon_path)` | ✅ Windows 上 `icon_path` 仍是 `.ico`，行为与 §29 一致 |

### 校验

```bash
# 平台分流逻辑存在
grep -n 'sys.platform == "darwin"' src/wowooai/cli/desktop_cmd.py
# 期望：命中 icon 选择分支

# 编译通过
.venv/bin/python -m py_compile src/wowooai/cli/desktop_cmd.py && echo OK
```

### 回退

把 [src/wowooai/cli/desktop_cmd.py](../../src/wowooai/cli/desktop_cmd.py) 中 `if sys.platform == "darwin": ... else: ...` 的分流块改回单一 `icon.ico` 候选即可。打包脚本侧的回退见 [packaging-macos.md §14.7](packaging-macos.md#147-回退)。



## §37 2026-05-14 增量：集成 agent-browser 高级浏览器能力（npx 外挂 + 三浏览器共享 CDP）

> 引入 Vercel Labs 的 `agent-browser@0.27.0` 作为外挂 CLI，与现有 `browser_use` / `renliwo_browser` 形成"renliwo → 常规 → 高级"三级分工。通过 CDP 让三个工具共享同一个 Chrome 实例，登录一次三方可用。打包阶段 bundle Node.js + 预装 agent-browser CLI，运行时通过 PATH 注入让 `execute_shell_command` 直接调用 `npx agent-browser@0.27.0`。

### §37.1 设计原则

| 原则 | 落地 |
|---|---|
| 三浏览器分工硬规则 | renliwo URL → `renliwo_browser`；一般浏览/截图/简单交互 → `browser_use`；高级能力（find role/text/label、network route、HAR、state save、视觉 diff、React、Vitals）→ `agent-browser` |
| 共享同一浏览器 | browser_use 启动时显式暴露 cdp_port，agent-browser / renliwo_browser 通过 CDP attach；登录态共享 |
| 暴露 cdp_port 时关闭 idle watchdog | 显式 `cdp_port>0` ≡ 外部工具会用这个浏览器；in-process activity timer 看不到外部活动，必须关闭 auto-stop 防止误回收 |
| 凭据隐私（继承 §35） | 任何浏览器工具一律不自动填账号 / 密码 / 验证码 / OTP / 滑动验证；登录由用户在可见窗口完成 |
| 版本锁定 | SKILL.md 全文 pin `agent-browser@0.27.0`；任何升级须同步刷新 SKILL.md |

### §37.2 后端代码改动

#### §37.2.1 `browser_use`：暴露 cdp_port 时关闭 idle watchdog

[src/wowooai/agents/tools/browser_control.py](../../src/wowooai/agents/tools/browser_control.py)

- `_make_fresh_state` 新增字段 `"external_cdp_exposed": False`
- `_reset_browser_state` 重置该字段
- `_action_start` 在 `_touch_activity(state)` 后判断：

  ```python
  external_cdp_exposed = bool(cdp_port and cdp_port > 0)
  state["external_cdp_exposed"] = external_cdp_exposed
  if not external_cdp_exposed:
      _start_idle_watchdog(state)
  ```

- `_ensure_browser` 同样守护：

  ```python
  if not state.get("external_cdp_exposed"):
      _start_idle_watchdog(state)
  ```

**Why**：当 `cdp_port>0` 显式暴露给外部时，浏览器是"共享设施"。in-process 的 watchdog 只看 wowooai 自己的 activity timer，看不到 agent-browser / renliwo_browser 通过 CDP 发起的操作；若不关闭，浏览器会在外部正在使用时被回收，导致协作链路断裂。自动挑选端口（`cdp_port=0` → 由 `_find_free_local_port` 分配）仍保留 watchdog，因为这是 wowooai 自己管的浏览器。

#### §37.2.2 `renliwo_browser`：新增 `connect_cdp` action

[src/wowooai/agents/tools/renliwo_browser.py](../../src/wowooai/agents/tools/renliwo_browser.py)

- state 新增 `"_connected_external": False`、`"cdp_url": None`
- 新增 `_action_connect_cdp(state, cdp_url)`：用 `playwright.async_api.async_playwright().chromium.connect_over_cdp(cdp_url)` 接管已有 Chrome；复用 `browser.contexts[0]`（即 browser_use 的 persistent context）共享 cookies；如已存在页面则全部注册到 `state["pages"]`，否则 `new_page()`
- `_action_stop` 在 `_connected_external=True` 时只调 `context.close() / browser.close() / playwright.stop()`（playwright 端的 disconnect-only），不会关闭外部 Chrome 进程
- 主入口 `renliwo_browser(...)` 增加 `cdp_url: str = ""` 参数；dispatcher 新增分支：

  ```python
  if action == "connect_cdp":
      return await _action_connect_cdp(state, cdp_url)
  ```

- docstring action 列表追加 `connect_cdp`；`cdp_url` 参数说明；unknown-action 错误消息列表同步

**Sync-mode 限制**：`WOWOOHR_RELOAD_MODE=1` 走的是 sync Playwright，`connect_cdp` 在此模式下直接返回错误（CDP attach 走 async API）。

#### §37.2.3 模板默认安装

[src/wowooai/agents/templates.py](../../src/wowooai/agents/templates.py)

`DEFAULT_TEMPLATE_SKILL_NAMES` 由 9 项扩到 11 项，追加 `"browser_cdp"` 和 `"agent_browser"`：

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

**Why**：首次启动自动创建的 `id=default` agent 会从 skill_pool 拷贝这个列表的 SKILL；用户无需手动安装即可使用三浏览器共享流程。

### §37.3 新增 SKILL：`agent_browser-zh` / `agent_browser-en`

- [src/wowooai/agents/skills/agent_browser-zh/SKILL.md](../../src/wowooai/agents/skills/agent_browser-zh/SKILL.md)
- [src/wowooai/agents/skills/agent_browser-en/SKILL.md](../../src/wowooai/agents/skills/agent_browser-en/SKILL.md)

frontmatter：

```yaml
name: agent_browser
builtin_skill_version: "1.0"
metadata:
  wowooai:
    emoji: "🛰️"
    requires:
      bins: ["npx"]
```

正文 8 节：三浏览器工具分工 / 共享 Chrome 标准步骤 / 常用命令清单（全部 pin `npx agent-browser@0.27.0`）/ 登录隐私规则 / 首跑下载提示 / session 隔离 / 失败兜底 / 安全提示。
所有命令示例都带 `--session $WOWOOAI_WORKSPACE_ID`，保证多 workspace 互不干扰。

### §37.4 打包：bundle Node.js + 预装 agent-browser CLI

#### §37.4.1 新增 fetch 脚本

- [scripts/pack/fetch_node.sh](../../scripts/pack/fetch_node.sh) — macOS/Linux 抓 Node.js 22.14.0 LTS 并 `npm install -g agent-browser@0.27.0` 到目标目录
- [scripts/pack/fetch_node.ps1](../../scripts/pack/fetch_node.ps1) — Windows x64 等价脚本

Chrome for Testing（~250 MB）由 agent-browser 在首次浏览器命令时按需下载，**不** bundle 进 .app / .msi（包体增量太大；用户大概率走共享 browser_use 的 Chrome 路径，根本不需要）。

#### §37.4.2 macOS 打包集成

[scripts/pack/build_macos.sh](../../scripts/pack/build_macos.sh) 在 Playwright bundling 之后插入：

```bash
NODE_DEST="${APP_DIR}/Contents/Resources/node"
bash "${PACK_DIR}/fetch_node.sh" "$NODE_DEST"
```

Launcher 中注入 PATH：

```bash
NODE_BUNDLED="$(cd "$(dirname "$0")/../Resources/node" 2>/dev/null && pwd)"
if [ -n "$NODE_BUNDLED" ] && [ -x "$NODE_BUNDLED/bin/node" ]; then
  export PATH="$NODE_BUNDLED/bin:$PATH"
  export WOWOOAI_BUNDLED_NODE="$NODE_BUNDLED"
fi
```

#### §37.4.3 Windows 打包集成

[scripts/pack/build_win.ps1](../../scripts/pack/build_win.ps1) 在 conda-unpack 修复之后插入：

```powershell
$NodeDest = Join-Path $EnvRoot "node"
& pwsh -File (Join-Path $PSScriptRoot "fetch_node.ps1") -Dest $NodeDest
```

两个 launcher .bat（`wowooai Desktop.bat` / `wowooai Desktop (Debug).bat`）都注入 PATH：

```bat
if exist "%~dp0node\node.exe" (
  set "PATH=%~dp0node;%PATH%"
  set "WOWOOAI_BUNDLED_NODE=%~dp0node"
)
```

#### §37.4.4 desktop_cmd.py / app_cmd.py PATH 兜底

[src/wowooai/cli/desktop_cmd.py](../../src/wowooai/cli/desktop_cmd.py) 与 [src/wowooai/cli/app_cmd.py](../../src/wowooai/cli/app_cmd.py) 仿照 pypandoc 的 PATH 注入模式追加：

```python
bundled_node = os.environ.get("WOWOOAI_BUNDLED_NODE")
if bundled_node:
    node_bin = (
        bundled_node
        if sys.platform == "win32"
        else os.path.join(bundled_node, "bin")
    )
    if os.path.isdir(node_bin):
        env["PATH"] = node_bin + os.pathsep + env.get("PATH", "")  # desktop_cmd
        # app_cmd 写到 os.environ["PATH"]
```

**Why**：launcher 的 PATH 通常已经包含 bundled node；但开发模式直接 `python -m wowooai app` 不经 launcher，靠 `WOWOOAI_BUNDLED_NODE` 环境变量也能让子进程 `execute_shell_command` 找到 npx。

**附带修复**：[src/wowooai/cli/app_cmd.py](../../src/wowooai/cli/app_cmd.py) 顶部缺失 `import sys`（原代码已有 `sys.platform` 引用但无 import，本次随 PATH 注入一并补上，避免触发 `NameError`）。

### §37.5 共享浏览器标准流程（运行时）

```text
1. browser_use action='start' cdp_port=9222
   → 启动 Chrome（managed CDP）→ 关闭 idle watchdog
   → 返回 cdp_url = "http://127.0.0.1:9222"

2. (可选) renliwo_browser action='connect_cdp' cdp_url='http://127.0.0.1:9222'
   → playwright connect_over_cdp → 复用 contexts[0]
   → stop 时只断开，不杀进程

3. execute_shell_command:
     npx agent-browser@0.27.0 connect 9222 --session $WOWOOAI_WORKSPACE_ID
   → agent-browser 接管同一 Chrome
   → 后续 find role / network route / state save 等命令在共享浏览器上执行
```

登录由用户在浏览器窗口完成；三方共享 cookies / localStorage / 已打开 tab。

### §37.6 校验

#### §37.6.1 Python 语法

```bash
.venv/bin/python -m py_compile \
  src/wowooai/agents/tools/browser_control.py \
  src/wowooai/agents/tools/renliwo_browser.py \
  src/wowooai/agents/templates.py \
  src/wowooai/cli/desktop_cmd.py \
  src/wowooai/cli/app_cmd.py
# 期望：无输出
```

#### §37.6.2 模板默认安装

```bash
grep -n 'browser_cdp\|agent_browser' src/wowooai/agents/templates.py
# 期望：DEFAULT_TEMPLATE_SKILL_NAMES 中均命中
```

#### §37.6.3 SKILL.md 版本锁定

```bash
grep -c 'agent-browser@0.27.0' \
  src/wowooai/agents/skills/agent_browser-zh/SKILL.md \
  src/wowooai/agents/skills/agent_browser-en/SKILL.md
# 期望：两个文件均 ≥ 10（多处示例命令）
```

#### §37.6.4 idle watchdog 守卫

```bash
grep -n 'external_cdp_exposed' src/wowooai/agents/tools/browser_control.py
# 期望：3 处（state 初始化 / reset / start 守卫）+ 1 处 _ensure_browser 守卫
```

#### §37.6.5 renliwo_browser.connect_cdp

```bash
grep -n 'connect_cdp\|_connected_external' src/wowooai/agents/tools/renliwo_browser.py
# 期望：dispatcher / _action_connect_cdp / _action_stop 中的 disconnect-only 分支均命中
```

#### §37.6.6 默认 agent 安装（首次启动后）

```bash
ls ~/.wowooai/workspaces/default/skills/agent_browser-zh/SKILL.md
ls ~/.wowooai/workspaces/default/skills/browser_cdp-zh/SKILL.md
# 期望：均存在
```

#### §37.6.7 打包脚本

```bash
bash scripts/pack/build_macos.sh
ls dist/WowooAI.app/Contents/Resources/node/bin/{node,npm,npx}
# 期望：三个均为可执行文件
du -sh dist/WowooAI.app/Contents/Resources/node
# 期望：~50–80 MB（Node.js 22 LTS + agent-browser CLI）
```

### §37.7 安全与隐私

- 登录账号 / 密码 / 验证码 / 短信 OTP / 滑动验证：所有三个浏览器工具都禁止自动填充，必须由用户在可见浏览器窗口手动完成（继承 §35）。**任何凭据不得出现在源码 / 配置 / bundled JSON 中。**
- bundled Node.js 仅用于运行 `agent-browser@0.27.0`，SKILL.md 明确不得用 npx 安装/执行其他 npm 包
- agent-browser 的 `state save` 把登录态持久化到 `~/.cache/agent-browser/`，敏感场景下在 SKILL.md 中提示用户清理

### §37.8 回退

- 想关闭 agent-browser：从 `DEFAULT_TEMPLATE_SKILL_NAMES` 移除 `"agent_browser"` 即可，已创建的 default agent 会保留旧版 skill 集；
- 想关闭共享浏览器：从 `DEFAULT_TEMPLATE_SKILL_NAMES` 移除 `"browser_cdp"`，并在 browser_use 启动时不传 `cdp_port`（保留 idle watchdog）；
- 想恢复以前的 renliwo_browser 独占模式：不调 `action='connect_cdp'` 即可，老的 `action='start'` 行为完全保留。

## §38 2026-05-14 调优：tool_result 截断阈值放宽（中文多步工具链不再被压扁）

**背景**：在 default agent 上重现到一类问题——用户提问后 agent 连续 3 次调用 `execute_shell_command` 跑同一个知识库 `query.py`（每次换关键词），最终模型只看到第 1 次结果的前 1168 字符（≈ 388 中文字）。复盘发现是 `tool_result_pruning` 的默认阈值对中文偏紧 + skill 文档没禁止"换关键词重查"。

### §38.1 改动

#### §38.1.1 `src/wowooai/config/config.py` — `ToolResultPruningConfig` 默认值

| 字段 | 旧默认 | 新默认 | 影响 |
|---|---|---|---|
| `pruning_old_msg_max_bytes` | 3000 | **8000** | 中文 utf-8 约 3 字节/字 → 旧值仅 ~1000 字，截掉 5 条命中的尾部；新值 ~2700 字，覆盖一次完整检索预览 |
| `pruning_recent_n` | 2 | **4** | 倒扫 messages 时 `recent_count` 一遇 `tool_use` 就 break，实际 recent 池≤1；调到 4 后 3-4 步连续工具链都能完整回看 |
| `pruning_recent_msg_max_bytes` | 50000 | 50000 | 不动 |

**Why**：`light_context_manager._prune_tool_result` 把"非最近"的 tool_result 按 `pruning_old_msg_max_bytes` 二次截断（[light_context_manager.py:308-333](../../src/wowooai/agents/context/light_context_manager.py#L308-L333)）。3000 字节对英文够用，但中文场景下知识库返回的 5 条命中（约 4500-5000 字节）一进 old 池就被打回 1/3，多步推理时模型看不全前一步结果就只能再调一次工具。

**预期成本**：每条历史 tool_result 多塞 ~5KB；按 3 字节/token 估算，10 条历史 ≈ +15K tokens。Qwen3.6-plus / DeepSeek 长上下文窗口下不触顶，但 `context_compact` 触发阈值（默认 0.5 × max_input_length = 64K）会更早达到——长会话（>30 轮工具调用）的 compaction 频率略升。

**How to apply**：
- 代码默认值已改，新建的 default agent 直接生效。
- 已存在的 [`~/.wowooai/workspaces/<id>/agent.json`](../../) 已固化旧值，**需手动 patch**：

  ```bash
  python3 - << 'PY'
  import json, pathlib
  fp = pathlib.Path('~/.wowooai/workspaces/default/agent.json').expanduser()
  d = json.loads(fp.read_text())
  trc = d['running']['light_context_config']['tool_result_pruning_config']
  trc['pruning_recent_n'] = 4
  trc['pruning_old_msg_max_bytes'] = 8000
  fp.write_text(json.dumps(d, ensure_ascii=False, indent=2))
  PY
  ```

#### §38.1.2 `qd-social-onboarding-training/SKILL.md`（用户工作区 skill）

`Anti-patterns` 段追加一条规则：

> ❌ Do NOT 同一主题换关键词重复检索——首查若提示截断，**直接用 `--full` 取全文**，不要用近义词、英文词或更细化的关键词再调一次 `query.py`；这会浪费 token 且容易丢失第一次的命中片段。

**Why**：复盘 session 中 thinking 块显示，模型连续换关键词（"QD社保运行核心系统" → "五大核心系统 XP系统..." → "智窝系统 易工宝..."）的策略，是因为 SKILL.md 通篇强调"逐条扫 5 条命中"，但没明确禁止换关键词重查；同时三套截断提示语义打架（系统级 `<<<TRUNCATED>>>` 教用 `read_file`，query.py 自己的"已截断" 教用 `--full`，模型在两者之间选择了第三条路：换关键词重查）。

**作用域**：仅修改用户工作区 [`~/.wowooai/workspaces/default/skills/qd-social-onboarding-training/SKILL.md`](../../)；该 skill 不在主仓 skill_pool 内，不影响其他用户。

### §38.2 校验

```bash
# 1. 默认值生效
.venv/bin/python -c "
from wowooai.config.config import ToolResultPruningConfig
c = ToolResultPruningConfig()
assert (c.pruning_recent_n, c.pruning_old_msg_max_bytes,
        c.pruning_recent_msg_max_bytes) == (4, 8000, 50000)
print('OK')
"
# 期望：OK

# 2. 现网 agent.json 已 patch
python3 -c "
import json
d = json.load(open('/Users/rlw/.wowooai/workspaces/default/agent.json'))
trc = d['running']['light_context_config']['tool_result_pruning_config']
assert trc['pruning_recent_n'] == 4 and trc['pruning_old_msg_max_bytes'] == 8000
print('OK')
"
# 期望：OK

# 3. SKILL.md anti-pattern 已写入
grep -c '同一主题换关键词重复检索' \
  ~/.wowooai/workspaces/default/skills/qd-social-onboarding-training/SKILL.md
# 期望：1
```

### §38.3 不做

- 不动 `pruning_recent_msg_max_bytes`（50KB 已足够覆盖最大单次检索）。
- 不在 [light_context_manager.py:253-262](../../src/wowooai/agents/context/light_context_manager.py#L253-L262) 改变倒扫策略（`recent_count` 一遇非 tool_result 就 break）：本次只改阈值，行为不变；将来若需要让 recent 池跨 tool_use 边界扩展，应单独评估对短对话场景的影响。
- 不动主仓 skill_pool 的其他 SKILL.md：本次只针对 qd-social-onboarding-training 这一个用户工作区 skill；其他知识库 skill 若也要加同样的反模式，由 skill 作者各自维护。

## §39 2026-05-14 内置 QA Agent 改造为「入职小助手」（人力窝公司入职指引数字员工）

**背景**：原内置 `wowooai_QA_Agent_0.2` 定位为 wowooai 官方答疑助手（技能 `guidance` + `QA_source_index`，工具几乎全开）。私有部署场景下，它的真实角色应是公司新员工入职指引；改造后保留原 builtin slot（ID 不变，避免触发 LEGACY 禁用 + 不破坏 [`routers/agent.py:250`](../../src/wowooai/app/routers/agent.py#L250) / [`routers/workspace.py:298`](../../src/wowooai/app/routers/workspace.py#L298) 的语言切换兜底分支），把名称、技能、工具、人格 MD 全部替换为公司入职指引。

### §39.1 常量与模板（[src/wowooai/constant.py](../../src/wowooai/constant.py) / [src/wowooai/agents/templates.py](../../src/wowooai/agents/templates.py)）

| 常量 | 旧值 | 新值 |
|---|---|---|
| `BUILTIN_QA_AGENT_ID` | `wowooai_QA_Agent_0.2` | **不变**（保留 LEGACY 兼容路径） |
| `BUILTIN_QA_AGENT_NAME` | `"QA Agent"` | `"入职小助手"` |
| `BUILTIN_QA_AGENT_SKILL_NAMES` | `("guidance", "QA_source_index")` | `("onboarding-guide",)` |
| `QA_TEMPLATE_DESCRIPTION` | wowooai 自身答疑文案 | 人力窝/仁励窝入职指引描述（含覆盖说明） |

**Why**：ID 不变是为了让已有用户升级时不会被当作"全新 builtin slot 创建"——`ensure_qa_agent_exists()` 看到 profile 已存在直接 `return`，不会覆盖用户后续手工调整的工具/技能选择（迁移文档原话：first-creation only）。改名只影响**新建** workspace。

### §39.2 工具预设（[src/wowooai/config/config.py:1398](../../src/wowooai/config/config.py#L1398) `build_qa_agent_tools_config()`）

启用集合从 `{execute_shell_command, read_file, write_file, edit_file, view_image}` 改为：

```python
allow = frozenset({
    "execute_shell_command",   # 调 onboarding-guide 的 query.py
    "get_current_time",        # 班车时间 / 是否工作日类问题
    "read_file",               # 读 memory/MEMORY.md 与单条记忆
    "write_file",              # 写新记忆文件
    "edit_file",               # 改 MEMORY.md 索引
    "view_image",              # 看用户上传的报错截图
})
```

**Why**：第一版只放 2 个工具（shell + time），但 `auto_memory_interval = 5`（[§5a20e1ec](../../) 默认改为 5）触发记忆刷新时会调 `read_file` / `write_file` / `edit_file`——如果不放这三个，每次到记忆触发点 Agent 报 ToolNotFound，记忆系统直接哑火。`view_image` 是低成本扩展，新员工经常截屏问"VPN 这个报错怎么办"。其余浏览器/桌面/Agent 间通信工具维持 disabled。

### §39.3 BOOTSTRAP.md 不再被强删（[src/wowooai/agents/utils/setup_utils.py:169](../../src/wowooai/agents/utils/setup_utils.py#L169)）

```python
def _remove_bootstrap_from_workspace(workspace_dir: Path) -> None:
    """Deprecated: kept as no-op for backward compatibility."""
    return
```

**Why**：原实现在 `copy_template_md_files` 末尾无条件 `unlink BOOTSTRAP.md`（[setup_utils.py:222 旧版](../../)），逻辑是"wowooai QA Agent 不需要 BOOTSTRAP 启动语"。入职小助手必须有首次欢迎语 + 阶段分流问句，故改为 no-op。函数体保留是为了兜住可能存在的旧调用点，不破坏导入。同时 `copy_template_md_files` 内部对 `_remove_bootstrap_from_workspace` 的调用直接删除（同步移除）。

### §39.4 人格 MD 替换（[src/wowooai/agents/md_files/qa/{zh,en,ru}/](../../src/wowooai/agents/md_files/qa/zh/)）

每语言 4 个文件：

| 文件 | 内容来源 |
|---|---|
| `AGENTS.md` | 角色卡：人力窝入职指引定位 + 知识库覆盖边界（明确覆盖 vs 覆盖不足）+ 7 个引导模块（G01-G07）+ 回答格式 + 工具与技能段（含 workspace 边界提示） |
| `SOUL.md` | "公司导航员"气质：亲切、直接给步骤、对敏感信息谨慎、新人陪伴感 |
| `PROFILE.md` | 简短身份卡：名字 / 定位 / 风格 / Agent ID（保留 `wowooai_QA_Agent_0.2` 字符串） |
| `BOOTSTRAP.md` | 首次欢迎语 + 4 阶段分流（入职前 / 今天刚入职 / 一周内 / 老员工查询） |

**多语言策略**：私有部署只对内，en/ru 直接用 zh 中文内容铺平（避免用户切换语言时回到旧 wowooai QA 文案）。三语副本由 `cp` 同步。

### §39.5 内置技能（[src/wowooai/agents/skills/onboarding-guide-{zh,en,ru}/](../../src/wowooai/agents/skills/onboarding-guide-zh/)）

技能源：`onboarding-guide-zh@5.0.0.zip`（百炼知识库检索型 skill，调用 `python3 scripts/query.py "<问题>"`）。

| 路径 | 来源 |
|---|---|
| `onboarding-guide-zh/` | zip 解压（含 `manifest.json` / `SKILL.md` / `scripts/query.py` / `README.md`） |
| `onboarding-guide-en/` | zh 副本（语言切换兜底） |
| `onboarding-guide-ru/` | zh 副本（语言切换兜底） |

⚠️ `SKILL.md` 中硬编码了 `DASHSCOPE_API_KEY`，仅限私有部署使用；上 git 公开仓库前必须移到环境变量。

### §39.6 前端内置技能识别（[console/src/components/SkillVisual/index.tsx:22](../../console/src/components/SkillVisual/index.tsx#L22) / [console/src/pages/Agent/Skills/components/SkillCard.tsx:41](../../console/src/pages/Agent/Skills/components/SkillCard.tsx#L41)）

两处 `textSkillIcons` 集合追加 `"onboarding-guide"`，让前端正确识别为内置技能（图标 / 不可删除标记）。保留旧的 `"guidance"` 兼容已有用户。

### §39.7 生效条件（重要）

**`ensure_qa_agent_exists()` 看到 profile 已存在就 return**（[migration.py:911](../../src/wowooai/app/migration.py#L911)），所以代码改动**只对新建 workspace 生效**。已存在的入职小助手 workspace 必须手动重建：

```bash
# 1. 关闭 wowooai 后端
# 2. 删旧 workspace
rm -rf ~/.wowooai/workspaces/wowooai_QA_Agent_0.2
# 3. 编辑 ~/.wowooai/config.json，删掉 agents.profiles 里 "wowooai_QA_Agent_0.2"
#    （若 active_agent 指向它，改成 "default"）
# 4. 重启后端 → ensure_qa_agent_exists() 用新模板重新创建
```

### §39.8 校验

```bash
# 1. 常量
python3 -c "
from wowooai.constant import BUILTIN_QA_AGENT_NAME, BUILTIN_QA_AGENT_SKILL_NAMES
assert BUILTIN_QA_AGENT_NAME == '入职小助手'
assert BUILTIN_QA_AGENT_SKILL_NAMES == ('onboarding-guide',)
print('OK')
"

# 2. 工具集
python3 -c "
from wowooai.config.config import build_qa_agent_tools_config
cfg = build_qa_agent_tools_config()
enabled = {k for k, v in cfg.builtin_tools.items() if v.enabled}
assert enabled == {'execute_shell_command', 'get_current_time',
                   'read_file', 'write_file', 'edit_file', 'view_image'}
print('OK')
"

# 3. 技能目录三语齐全
ls -d src/wowooai/agents/skills/onboarding-guide-{zh,en,ru}
# 期望：3 个目录都存在

# 4. MD 三语齐全
ls src/wowooai/agents/md_files/qa/{zh,en,ru}/{AGENTS,SOUL,PROFILE,BOOTSTRAP}.md
# 期望：12 个文件都存在

# 5. BOOTSTRAP 不再被删
grep -A 3 'def _remove_bootstrap_from_workspace' \
  src/wowooai/agents/utils/setup_utils.py
# 期望：函数体只有 'return'
```

### §39.9 不做

- **不改 `BUILTIN_QA_AGENT_ID`**：换 ID 会触发 `_apply_legacy_qa_disable_for_migration` 把当前 ID 当 LEGACY 禁用，且 `qa/zh/PROFILE.md` 中硬编码的 ID 字符串需同步改 6 个文件（zh/en/ru × AGENTS/PROFILE）。
- **不删旧的 `guidance-{zh,en}` / `QA_source_index-{zh,en}` 技能目录**：保留以兼容已有用户的 wowooai QA workspace（他们的 skills/ 目录已安装这两个，删了会让他们的 Agent 启动失败）。
- **不动 CLI `wowooai agents create` 流程**：CLI 仍走 `build_agent_template`，但 HTTP `POST /agents` 不走模板（参见 [§ 4 节"不一致"](#)），本次改造只覆盖通过 builtin slot 创建的入职小助手。
- **不在 SKILL.md 改 API Key 加载方式**：私有部署写死可接受；公开发布前必须改读 env。

### §39.10 2026-05-15 收敛：移除入职小助手的 BOOTSTRAP 引导

> 私有部署不再需要首次进入的"4 选 1"入职阶段引导，直接让用户提问即可。

**改动**：删除 3 份 BOOTSTRAP.md 模板文件——

- [src/wowooai/agents/md_files/qa/zh/BOOTSTRAP.md](../../src/wowooai/agents/md_files/qa/zh/BOOTSTRAP.md)
- [src/wowooai/agents/md_files/qa/en/BOOTSTRAP.md](../../src/wowooai/agents/md_files/qa/en/BOOTSTRAP.md)
- [src/wowooai/agents/md_files/qa/ru/BOOTSTRAP.md](../../src/wowooai/agents/md_files/qa/ru/BOOTSTRAP.md)

**为什么不需要改任何代码**：

| 链路 | 缺失 BOOTSTRAP.md 的行为 |
|---|---|
| [bootstrap.py:64-65](../../src/wowooai/agents/hooks/bootstrap.py#L64-L65) hook | `if not bootstrap_path.exists(): return None` — 直接返回，无副作用 |
| [setup_utils.py:122-135](../../src/wowooai/agents/utils/setup_utils.py#L122-L135) `_copy_template_md_files` | 候选名通过 `lang_dir.glob("*.md")` 动态扫描，源文件不存在即不进入复制列表 |
| `_TEMPLATE_OVERRIDE_FILENAMES` 集合 [setup_utils.py:17](../../src/wowooai/agents/utils/setup_utils.py#L17) | 仍包含 `BOOTSTRAP.md`，但只是"允许覆盖"的白名单；源文件不存在该项自然失效 |
| [prompt.py:338-369](../../src/wowooai/agents/prompt.py#L338-L369) `build_bootstrap_guidance` | 仅在 hook 触发时被调用，hook 不再触发即变成死代码���保留无害） |

`_remove_bootstrap_from_workspace` no-op 函数与 `_TEMPLATE_OVERRIDE_FILENAMES` 中的 `BOOTSTRAP.md` 项均**保留**——后续如再启用 BOOTSTRAP 引导，只需把对应 MD 文件放回 `md_files/<template>/<lang>/` 即可。

**对存量用户的影响**：源码删除只影响"新建 / 重置 workspace 后的首次拷贝"。已经存在 `~/.wowooai/workspaces/wowooai_QA_Agent_0.2/BOOTSTRAP.md` 的用户，其 workspace 内文件不会被自动清理；要强制干净，需手动删除：

```bash
rm -f ~/.wowooai/workspaces/wowooai_QA_Agent_0.2/BOOTSTRAP.md
```

**校验**：

```bash
ls src/wowooai/agents/md_files/qa/{zh,en,ru}/
# 期望：每个语言目录下仅有 AGENTS.md / PROFILE.md / SOUL.md，共 9 个文件
```

**§39.8 校验清单同步**：原"4. MD 三语齐全"命令应去掉 `BOOTSTRAP`：

```bash
ls src/wowooai/agents/md_files/qa/{zh,en,ru}/{AGENTS,SOUL,PROFILE}.md
# 期望：9 个文件都存在
```

---

## §40 2026-05-15 修复：desktop_app 窗口操作的"前台未稳态化"导致点错对象

### 背景

§33 落地的 `desktop_app` 在以下场景会**静默失败**——`focus_window` 报 `ok` 但目标窗口实际没切到前台，紧接着 `desktop_input.click` 就会点到 z-order 上层的其他窗口：

- 目标窗口被最小化到 Dock / 任务栏（`AXRaise` 不会展开 Dock 中的窗口；Windows `AppActivate` 对最小化窗口经常只闪任务栏）。
- macOS `name of w contains "..."` 大小写敏感，模型用小写传题目时 miss。
- macOS 进程窗口标题为空（模态 sheet、表情面板等）时，`focus_window` 直接返回"找不到"。
- Windows `LockSetForegroundWindow` 拦截 `SetForegroundWindow` 时 PowerShell **不报错**，工具层仍 `ok`。
- `list_windows` 在 macOS 下过滤掉了"无可见窗口的进程"、Windows 下过滤掉了空 `MainWindowTitle`，导致钉钉/微信等托盘 app 在结果里完全看不到，模型可能误判"app 没启动"再 `launch` 一次。

本次修复：保留 `focus_window`、`activate`、`list_windows` 接口语义，**修内部实现**；同时新增 `ensure_frontmost`（推荐组合操作）和 `zoom_window`（可选最大化）两个 action。**不**新增依赖，**不**改 ReAct / 工具注册管线。

### 改动一：`desktop_app.py` — 修 `_focus_window_mac`（A + B）

**文件**：`src/wowooai/agents/tools/desktop_app.py`

整段替换原 `_focus_window_mac`：

- 用 `ignoring case` 让窗口标题 contains 大小写不敏感（**B 修复**）
- 命中后先 `if value of attribute "AXMinimized" of w is true then set ... to false` 自动恢复最小化窗口，再 `set frontmost` + `AXRaise`（**A 修复**）
- 跳过 `wname is ""` 的窗口；提示模型对无标题窗口改用 `ensure_frontmost(name=...)`
- 返回值新增 `matched_title` 字段（向后兼容，旧消费方仍能拿到 `matched_app`）

### 改动二：`desktop_app.py` — 重写 `_focus_window_win`（A + E）

不再用 `Microsoft.VisualBasic.Interaction::AppActivate`。新版 PowerShell 脚本通过 `Add-Type` 直接 P/Invoke `user32.dll`：

```
EnumWindows (按子串大小写不敏感地匹配可见窗口)
   ↓ 命中第一个
IsIconic? → ShowWindowAsync(hwnd, SW_RESTORE=9)   # A 修复
SetForegroundWindow(hwnd)
Start-Sleep -Milliseconds 200
GetForegroundWindow == hwnd ?
   ├─ 是 → "OK\t<title>"
   └─ 否 → "RACE\t<title>"   # E 修复：被 LockSetForegroundWindow 拦截
```

Python 侧解析 `OK` / `RACE` / `NOMATCH`：`RACE` 转成 `_tool_error`，错误信息提示模型改用 `ensure_frontmost`，**不再静默 ok**。

PowerShell 模板提到模块级常量 `_PS_FOCUS_WINDOW`，避免在循环中重复构造大字符串。

### 改动三：`desktop_app.py` — 新增 `ensure_frontmost` action（C）

新增 `_ensure_frontmost_mac` / `_ensure_frontmost_win` 两个内部函数，作为"切前台 + 等动画 + 校验"的复合原子操作。模型可以一次调用就拿到稳态前台窗口，不需要自己拼 `activate` + `focus_window` + sleep + 再校验的序列。

**macOS 流程**：

1. 若传 `name`：先 `osascript ... to activate` 把进程切前台
2. 若传 `title_substring`：循环调 `_focus_window_mac`，命中后 `time.sleep(0.15)` 等动画
3. 二次校验 `tell application "System Events" to return name of first process whose frontmost is true` 等于目标 app 名
4. 不一致或没命中，按 `timeout_ms / 1000.0` 秒内每 100ms 重试一次
5. 超时返回 error，错误消息含最后一次失败原因

**Windows 流程**：

1. 直接复用修过的 `_focus_window_win`，靠它返回的 `RACE` 错误码做有限重试（每次间隔 200ms）
2. 总等待上限 `timeout_ms`（默认 1500ms，函数签名新增此参数）

### 改动四：`desktop_app.py` — 新增 `zoom_window` action（可选最大化）

为了减少"窗口太小看不清控件"导致的视觉定位失败，新增显式 opt-in 最大化能力。**不**进入 `ensure_frontmost` 默认路径——避免布局重排让模型已估算的旧坐标全部失效。

**macOS 实现**（`_zoom_window_mac`）：

```applescript
tell {process X}
  if AXMinimized then deminimize
  if AXFullScreen then exit fullscreen   # 关键：绝不让窗口进入全屏 Space
  set _btns to (every button of _w whose subrole is "AXZoomButton")
  click item 1 of _btns
end tell
```

**为什么不用 `set zoomed of {window} to true`**：实测在 Calculator 等 app 上抛 `-10006`（"不能将 zoomed of UI element 设置为 any"）。`zoomed` 是 app 字典属性而非 AX 属性，并非所有 app 都暴露。点击 `AXZoomButton`（绿灯钮）是 AX 通用方案，所有标准 macOS 窗口都有。

**Windows 实现**（`_maximize_window_win`）：

`EnumWindows` 找标题命中的第一个可见窗口，`ShowWindowAsync(hwnd, SW_MAXIMIZE=3)`。模板放在模块级常量 `_PS_MAXIMIZE_WINDOW`。

### 改动五：`desktop_app.py` — `list_windows` 区分 tray（F）

**macOS** AppleScript 调整：原来 `if wcount > 0` 分支才输出，现在每个 visible process 都输出：

- 有窗口 → 每个窗口一行 `<app>\t<title>\t0`
- 无窗口 → 一行 `<app>\t\t1`（tray 模式）

Python 解析侧每条结果新增 `tray: bool` 字段。

**Windows** PowerShell 调整：

```powershell
Get-Process | Where-Object { $_.Id -ne $PID } |
  Select-Object -Property ProcessName,
    @{N='MainWindowTitle';E={ $_.MainWindowTitle }},
    @{N='Tray';E={ [string]::IsNullOrEmpty($_.MainWindowTitle) }}
```

不再用 `MainWindowTitle -ne ''` 过滤。但 Windows 系统进程数量太多，全部输出会爆 token，所以 Python 侧加白名单 `_TRAY_KEEP_WIN`，托盘条目仅保留常见 IM / 办公 app：

```python
_TRAY_KEEP_WIN = {
    "DingTalk", "WeChat", "WeChatAppEx", "Feishu", "Lark",
    "wxwork", "WXWork", "Outlook", "Teams", "ms-teams", "Slack",
}
```

LLM 据 `tray=true` 判断"已运行但无可见窗口"，需要 `ensure_frontmost` 才能召出窗口，避免误 `launch` 第二次。

### 改动六：`desktop_app.py` — `_SUPPORTED_ACTIONS` / `desktop_app` 函数签名 / docstring

```python
_SUPPORTED_ACTIONS = (
    "launch",
    "activate",
    "list_windows",
    "focus_window",
    "ensure_frontmost",   # 新
    "zoom_window",        # 新
    "quit",
)

async def desktop_app(
    action: str,
    name_or_path: Optional[str] = None,
    name: Optional[str] = None,
    title_substring: Optional[str] = None,
    timeout_ms: int = 1500,        # 新
) -> ToolResponse:
```

dispatch 末尾追加 `ensure_frontmost` / `zoom_window` 两条分支，参数缺失返回 `_tool_error`。

docstring 改写：明确推荐 `ensure_frontmost` 替代裸 `focus_window`；`zoom_window` 标注 opt-in、调用后旧坐标作废；`list_windows` 解释 `tray` 字段语义；`focus_window` 注明 macOS 已大小写不敏感、Windows 已校验前台真实切换。

### 改动七：SKILL.md（zh + en）— 强制循环改为先稳态化

**文件**：`src/wowooai/agents/skills/desktop_control-zh/SKILL.md` / `desktop_control-en/SKILL.md`

强制循环第一步从"先截屏"改为"先稳态化窗口"：

```
1. desktop_app(action="ensure_frontmost", name="<AppName>", title_substring="<片段>")
2. desktop_screenshot
3. desktop_input(...)
4. desktop_screenshot 验证
```

"失败兜底"改写：

- "点击没反应 → `activate`" → 改为 "→ `ensure_frontmost`，自动 deminimize、抢前台、二次校验、Windows 端在 `LockSetForegroundWindow` 拦截时自动重试到超时（默认 1500ms）"
- 新增："窗口被最小化到 Dock/任务栏 → `ensure_frontmost` 会自动恢复"
- 新增："`list_windows` 返回 `tray:true` 的条目表示 app 在托盘 / 后台无窗口，需要 `ensure_frontmost` 召出窗口"

新增 "## 何时用 `zoom_window`" 小节：

- 默认**不要**最大化
- 仅在窗口太小、关键控件被裁、侧栏被折叠看不到目标时显式调
- 调用后**所有先前估算坐标全部作废**，必须立即重新 `desktop_screenshot`
- macOS 用绿灯钮等价方案，**不会**切 Space / 进入全屏
- Windows 用 `SW_MAXIMIZE`

英文版逐条同步。

### §40 不在范围

- **`desktop_input.click` 点击前 hit-test**：依赖 `AXUIElementCopyElementAtPosition` / `WindowFromPoint`，当前不引入 PyObjC AX 框架，单独评估
- **多显示器 / Retina 坐标修正**：`pyautogui.size()` 仍只返回主屏，副屏点击会被 `_in_bounds` 判越界——本次不动
- **macOS TCC（辅助功能 + 屏幕录制）授权引导**：仍由 OS 弹窗，不做 UI 引导
- **新依赖**：`pywinauto` / `uiautomation` / `pyobjc-framework-ApplicationServices` 都不引入；`zoom_window` 选 AX 绿灯钮方案就是为了避开 PyObjC
- **`zoom_window` 进默认流程**：明确不做，避免布局重排打乱坐标估算

### §40 验证

```bash
# 1. 静态导入 + action 注册
/Users/rlw/AI项目/wowooai/.venv/bin/python3 -c "
from wowooai.agents.tools.desktop_app import desktop_app, _SUPPORTED_ACTIONS
assert 'ensure_frontmost' in _SUPPORTED_ACTIONS
assert 'zoom_window' in _SUPPORTED_ACTIONS
"

# 2. macOS 端 e2e（Calculator + cmd+M 最小化）
/Users/rlw/AI项目/wowooai/.venv/bin/python3 - <<'PY'
import asyncio, json, subprocess
from wowooai.agents.tools.desktop_app import desktop_app

async def m():
    await desktop_app(action="launch", name_or_path="Calculator")
    await asyncio.sleep(1.2)
    subprocess.run(["osascript", "-e",
        'tell application "System Events" to keystroke "m" using command down'])
    await asyncio.sleep(0.6)
    r = await desktop_app(action="ensure_frontmost",
        name="Calculator", title_substring="计算器")
    print(json.loads(r.content[0]["text"]))   # 期望 ok=True
    r = await desktop_app(action="zoom_window", name="Calculator")
    print(json.loads(r.content[0]["text"]))   # 期望 ok=True
    await desktop_app(action="quit", name="Calculator")
asyncio.run(m())
PY
# 期望：cmd+M 最小化的 Calculator 被 ensure_frontmost 弹回前台；zoom_window 把窗口撑大但不切 Space

# 3. Windows 端（VM 内手动跑）
# - launch notepad，sendkeys "% n" 最小化
# - desktop_app(ensure_frontmost, title_substring="Notepad") 期望恢复并切前台
# - 用 Win+Tab 切到全屏 app，期间调 focus_window，期望返回 LockSetForegroundWindow 错误而非 ok

# 4. 旧调用站回归
# - launch / activate / quit 行为不变
# - focus_window 在 macOS 仍接受原 case-sensitive 调用，但现在大小写都行
# - list_windows 输出新增 tray 字段（向后兼容）
```

### §40 关键文件

- `src/wowooai/agents/tools/desktop_app.py`（主体修改）
- `src/wowooai/agents/skills/desktop_control-zh/SKILL.md`
- `src/wowooai/agents/skills/desktop_control-en/SKILL.md`

不动：
- `src/wowooai/agents/tools/desktop_input.py`
- `src/wowooai/agents/tools/desktop_screenshot.py`
- `src/wowooai/agents/tools/__init__.py`（不新增工具，只在 `desktop_app` 内加 action）
- `src/wowooai/agents/react_agent.py` / `src/wowooai/config/config.py`（`BuiltinToolConfig.desktop_app` 一项已覆盖）
- `pyproject.toml`（不新增依赖）




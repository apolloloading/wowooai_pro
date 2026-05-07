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


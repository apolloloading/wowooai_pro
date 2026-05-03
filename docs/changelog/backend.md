# 后端改造说明

> 本文面向一份**干净的原 copaw 后端源码**：只记录本轮需要复刻的后端变更。除本文列出的 §1 / §5 / §8 外，其他后端模块不要调整。
>
> 完整目标源码以 [source-bundle/](source-bundle/) 为准；涉及大文件时，优先从 source-bundle 按同路径复制。

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

> 配套打包执行说明见 [packaging.md](packaging.md)。本节只记录需要复刻到源码的后端 / 打包脚本变更；`packaging.md` 不再承载代码改造逻辑。

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




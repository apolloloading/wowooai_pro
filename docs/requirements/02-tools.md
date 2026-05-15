# 02 — 内置工具系统

> 版本：0.0.1
> 对应代码：[src/wowooai/agents/tools/](../../src/wowooai/agents/tools/) · [src/wowooai/config/config.py](../../src/wowooai/config/config.py)（`_default_builtin_tools`）

## 1. 工具分类

| 类别 | 工具 | 用途 |
|---|---|---|
| Shell / 文件 | `execute_shell_command` / `read_file` / `write_file` / `edit_file` / `grep_search` / `glob_search` | 本机文件读写与命令执行 |
| 浏览器 | `browser_use` / `renliwo_browser` | 通用网页 & Renliwo HR 平台自动化 |
| 桌面 app | `desktop_screenshot` / `desktop_input` / `desktop_app` | 截屏、鼠标键盘注入、app 生命周期 |
| 媒体加载 | `view_image` / `view_video` | 把图/视频塞进 LLM 上下文 |
| 用户交付 | `send_file_to_user` | 把工作区文件以同源 HTTP URL 推送给用户 |
| 时间 / 时区 | `get_current_time` / `set_user_timezone` | 时间与时区管理 |
| 使用量 | `get_token_usage` | 查询 token 用量 |
| 跨 agent | `list_agents` / `chat_with_agent` / `submit_to_agent` / `check_agent_task` | 数字员工间协作 |
| 外部 agent | `delegate_external_agent` | ACP 外挂调用（默认关） |

工具默认值由 [config.py `_default_builtin_tools()`](../../src/wowooai/config/config.py) 定义。

## 2. 通用约定

- 工具函数为 async；返回 `ToolResponse(content=[TextBlock|ImageBlock|FileBlock|...])`。
- `BuiltinToolConfig` 字段：`name` / `enabled` / `description` / `display_to_user` / `async_execution` / `icon`。
- `display_to_user=False` 的工具结果不渲染到对话气泡（如 `view_image` / `view_video`）。
- 工具结果会受 [01-agents.md §9.2 ToolResultPruningConfig](01-agents.md#92-工具结果裁剪toolresultpruningconfig) 裁剪。

## 3. Shell & 文件

### 3.1 `execute_shell_command`

| 参数 | 默认 |
|---|---|
| `command` | 必填 |
| `timeout` | `AgentsRunningConfig.shell_command_timeout`（默认 60） |
| 工作目录 | 当前 agent workspace |

副本沙箱：所有可能写入、编辑、覆盖用户原始文件的命令都会被 `_check_destructive_command` 拦截（详见 [06-security.md](06-security.md)）。

### 3.2 `read_file` / `write_file` / `edit_file`

- `_sandbox_copy_for_write`：对 workspace 外的目标自动改写到 `<workspace>/.sandbox/input/<原名>_副本.<ext>`。
- 写入前若原文件存在，先 `shutil.copy2` 到沙箱副本，再修改副本。
- `.md` 扩展名默认豁免 tool_result 裁剪。

### 3.3 `grep_search` / `glob_search`

通用模式搜索，受 workspace 范围约束；返回行数有限的结果（避免上下文爆炸）。

## 4. 浏览器

### 4.1 工具分工硬规则

| 目标 | 必须用 |
|---|---|
| `*.renliwo.com` URL | `renliwo_browser`（绝对禁止 `browser_use`） |
| 其他普通网页 / 截图 / 简单交互 | `browser_use` |
| 高级能力（role / text 定位、network route、HAR、state save、视觉 diff） | `agent-browser`（npx 外挂，通过 `execute_shell_command` 调用） |

三者通过 CDP 共享同一个 Chrome：`browser_use action='start' cdp_port=9222` 启动后，`renliwo_browser action='connect_cdp'` 与 `agent-browser connect 9222` 都接入同一浏览器（cookies / localStorage / 已打开 tab 共享）。

### 4.2 默认模式：有头窗口 + 用户手动登录

- `browser_use(headed=True)` / `renliwo_browser(headed=True)` 是默认值。
- 绝对禁止用 `action=type` 自动填写账号 / 密码 / 验证码 / 短信 OTP / 滑动验证。
- 工具不读取、不持久化、不打日志、不返回任何登录凭据。
- 登录由用户在可见浏览器窗口手动完成；agent 等待用户确认"已登录"后继续。

### 4.3 `renliwo_browser` 多站点

- 多站点注册表 `_SITES`：扫描 [renliwo_browser_data/<site_id>/site.json](../../src/wowooai/agents/tools/renliwo_browser_data/)。
- host 匹配走 `fnmatch` 前缀通配（`qd-system*.renliwo.com`）。
- 路由抽象：`routing.type ∈ {"hash", "path"}`。
- 0.0.1 内置 2 个站点：`ereference`（hash 路由，top+sidebar）、`qd_system`（path 路由，sidebar-only）。
- 凭据严禁出现在源码 / 仓库 JSON：只从 `config.json > plugins.renliwo[site_id]` 运行时读取。

`action="guide"` 自动附带页面手册（route / tabs / export_buttons / select_fields / notes / doc_ref），登录成功 / 进入叶子页 / 导出成功后默认携带 guide。

### 4.4 `browser_use` 共享浏览器

- 显式 `cdp_port > 0` 时关闭 idle watchdog（避免外部工具操作期间被回收）。
- `cdp_port=0`（自动挑选端口）保留 watchdog。
- state 字段 `external_cdp_exposed` 持久化该选择。

## 5. 桌面 app 控制

### 5.1 `desktop_screenshot`

全屏或选窗截图；返回 `ImageBlock` 给模型视觉分析。Retina 屏幕像素是真实坐标的 2 倍，模型需调 `desktop_input(action="screen_size")` 取真实尺寸做换算。

### 5.2 `desktop_input`

跨平台鼠标 / 键盘注入。Action：`screen_size` / `move_to` / `click` / `double_click` / `right_click` / `drag` / `type_text` / `press_keys` / `scroll` / `query`（`query` 阶段 2 预留位，0.0.1 返回 `not_implemented`）。

| 安全护栏 | 行为 |
|---|---|
| 单次调用 1 个 action | 不接收脚本式批量 |
| 屏外坐标 | 返回错误，不静默裁剪 |
| `pyautogui.FAILSAFE` | 设为 `False`（避免左上角紧急中断） |
| 键名映射 | 模型一律用 macOS 写法（`cmd` / `option`），工具内部映射到 Windows（`win` / `alt`） |

### 5.3 `desktop_app`

| Action | macOS | Windows |
|---|---|---|
| `launch(name_or_path)` | `open -a` / `open <path>` | PowerShell `Start-Process` |
| `activate(name)` | `osascript ... activate` | `AppActivate` |
| `list_windows()` | `osascript` 枚举 System Events | `Get-Process \| MainWindowTitle` |
| `focus_window(title_substring)` | AppleScript 遍历 `name of w contains` | 按子串 activate |
| `quit(name)` | `osascript ... quit` | `CloseMainWindow()` |

不在 macOS / Windows 之外的平台返回错误。

### 5.4 强制循环

[desktop_control SKILL.md](../../src/wowooai/agents/skills/desktop_control-zh/SKILL.md) 要求：`desktop_screenshot` → 视觉定位 → `desktop_input` → 再 `desktop_screenshot` 验证。连续 2 次失败必须停止并向用户报告。

## 6. 媒体加载

| 工具 | 行为 |
|---|---|
| `view_image(path)` | 把本地图片加载到 LLM 上下文，`display_to_user=False` |
| `view_video(path)` | 把本地视频加载到 LLM 上下文，`display_to_user=False` |

## 7. `send_file_to_user`

- 输入：工作区内的绝对路径。
- 输出：`FileBlock` 同时填 `source.url` / `file_url` / `file_name`，URL 形如 `/api/files/preview/<percent-encoded-absolute-path>`（同源 HTTP，浏览器 / 桌面 / Docker 反代均能用）。
- 不使用 `file://` URL（pywebview WebView 跨协议拒绝）。

## 8. 时间 / 时区 / 用量

| 工具 | 用途 |
|---|---|
| `get_current_time` | 返回当前时间，使用 `config.user_timezone`（默认 IANA `Asia/Shanghai`） |
| `set_user_timezone` | 修改 `config.user_timezone` |
| `get_token_usage` | 查询当前 agent 的 token 用量统计 |

## 9. 跨 agent 协作

| 工具 | 用途 |
|---|---|
| `list_agents` | 列出本地 API 中所有配置的 agent |
| `chat_with_agent(agent_id, message)` | 同步向另一个 agent 发消息并等回复 |
| `submit_to_agent(agent_id, message)` | 异步派任务到另一个 agent |
| `check_agent_task(task_id)` | 查询异步任务状态 |

`chat_with_agent` 默认在 `tool_result_pruning.exempt_tool_names` 中（不会被裁剪）。

## 10. 外部 agent（ACP）

`delegate_external_agent` 默认 `enabled=False`。启用后通过 ACP 协议把任务派给外部 agent runner（opencode / qwen_code / claude_code / codex）。详见 [09-mcp-acp.md](09-mcp-acp.md)。

## 11. 审批级别（approval_level）

| 级别 | 行为 |
|---|---|
| `OFF` | 跳过 tool guard，所有工具直接执行 |
| `STRICT` | 所有工具都需审批 |
| `SMART` | 低风险（LOW / INFO）自动放行；中高风险进入审批 |
| `AUTO`（默认） | 仅 guarded tools 走完整规则；非 guarded 只跑文件防护 |

`denied_tools` 优先级最高，命中即拒绝且不可审批。详见 [06-security.md](06-security.md)。

## 12. 工具注册路径

每个新工具必须在三处注册：

1. [src/wowooai/agents/tools/\_\_init\_\_.py](../../src/wowooai/agents/tools/__init__.py) — `from .<name> import <fn>` + `__all__`。
2. [src/wowooai/agents/react_agent.py](../../src/wowooai/agents/react_agent.py) — `tool_functions` dict。
3. [src/wowooai/config/config.py](../../src/wowooai/config/config.py) — `_default_builtin_tools()` 添加 `BuiltinToolConfig`。

## 13. 兼容性

- `ToolsConfig._merge_default_tools()` 会在加载时把新出现的内置工具自动并入旧配置；用户保存的 `enabled=False` 不会被覆盖。
- 旧配置中 `icon=None` 的条目会被默认 icon 修复。

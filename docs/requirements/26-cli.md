# 26 — CLI 接口

> 版本：0.0.1
> 对应代码：[src/wowooai/cli/](../../src/wowooai/cli/) · 入口 [cli/main.py](../../src/wowooai/cli/main.py)

## 1. 入口与共享上下文

```bash
wowooai [--host HOST] [--port PORT] <subcommand> ...
```

`--host` / `--port` 不传时优先从 `~/.wowooai/last_api.json` 读取（详见 [11-startup-runtime.md §6](11-startup-runtime.md)），最后兜底 `127.0.0.1:8088`。

实现：[cli/main.py:157 `cli`](../../src/wowooai/cli/main.py#L157)。基于 click `LazyGroup` —— 子命令按需 lazy-import，避免启动时把全部模块吃进内存。

## 2. 子命令总览

| 命令 | 文件 | 用途 |
|---|---|---|
| `app` | `app_cmd.py` | 启动后端（FastAPI + uvicorn） |
| `init` | `init_cmd.py` | 首次初始化 / 创建工作目录 |
| `auth` | `auth_cmd.py` | API token 管理 |
| `agents` / `agent` | `agents_cmd.py` | 数字员工 CRUD（创建 / 列表 / 切换 / 删除） |
| `models` | `providers_cmd.py` | LLM provider 与模型槽管理 |
| `skills` | `skills_cmd.py` | 技能安装 / 卸载 / 启停 |
| `channels` / `channel` | `channels_cmd.py` | 渠道开关与凭据 |
| `chats` / `chat` | `chats_cmd.py` | 会话列表 / 发消息 / 跨 agent 派发 |
| `cron` | `cron_cmd.py` | 定时任务（详见 [08-cron-heartbeat.md §1.5](08-cron-heartbeat.md)） |
| `mission` | `mission_cmd.py` | Mission 启动 / 状态 / 列表（详见 [17 §10](17-mission-orchestration.md)） |
| `acp` | `acp_cmd.py` | ACP 外部 agent 管理 |
| `desktop` | `desktop_cmd.py` | 桌面包专用（启动 webview / 检查依赖） |
| `daemon` | `daemon_cmd.py` | 守护进程控制（restart / 状态） |
| `task` | `task_cmd.py` | 后台任务（submit_to_agent 等）查看 |
| `env` | `env_cmd.py` | 环境变量 / 工作区环境 |
| `plugin` | `plugin_commands.py` | 插件列表 / 启停（详见 [23-plugins.md](23-plugins.md)） |
| `clean` | `clean_cmd.py` | 清理临时数据（dialog / tool_results / etc.） |
| `update` | `update_cmd.py` | 更新检查（不自动下载，仅提示） |
| `shutdown` | `shutdown_cmd.py` | 优雅停止后端 |
| `uninstall` | `uninstall_cmd.py` | 卸载（删除 `~/.wowooai/`） |
| `doctor` | `doctor_cmd.py` | 自检 / 修复 |

## 3. agent-id 全程显式

涉及到具体数字员工的命令（cron / mission / chats 等）**强制要求** `--agent-id`：

- 不带 → 报错或落到 `default` workspace（按命令区别处理）；
- 这是为了防止任务错落到错误 workspace 产生静默问题。

详见 [08 §1.5](08-cron-heartbeat.md) "cron 命令必须带 `--agent-id`"。

## 4. HTTP 客户端

[cli/http.py](../../src/wowooai/cli/http.py)：所有 CLI 子命令都通过 HTTP 调本机后端（不直接 import 后端模块），保证：

- CLI 与后端版本可松耦合；
- 后端如果跑在 docker 里，CLI 仍然能用；
- last_api.json 写入的 host/port/token 自动复用。

## 5. doctor 子命令

[cli/doctor_cmd.py](../../src/wowooai/cli/doctor_cmd.py)（含 `doctor_checks.py` / `doctor_connectivity.py` / `doctor_fix_runner.py` / `doctor_registry.py`）

```bash
wowooai doctor             # 全量自检
wowooai doctor fix         # 自动修复部分问题
```

检查项：

- working dir 合法（`~/.wowooai/` 可写）
- console 静态资源完整（`console/dist/index.html` 存在）
- web 鉴权工作（GET `/` 行为正常）
- active_llm 可达（providers.json 中当前模型实际能调通）
- server python 与当前 CLI python 是否一致（避免跑两份不同版本的环境）

每项返回 `(ok: bool, message: str)`；失败时给出 `_doctor_fix_hint` 修复建议。

## 6. clean

清理临时数据（不动用户配置 / 工作区核心内容）：

- `<workspace>/tool_results/*` 落盘工具结果（详见 [15 §2.4](15-context-compaction.md)）
- `<workspace>/backup/memory_backup_*.md` dream 备份
- `<workspace>/dialog/*.jsonl` 旧对话（按保留天数）

## 7. shutdown / daemon

```bash
wowooai shutdown              # 给后端发 graceful stop
wowooai daemon status         # 看进程 / 端口 / pid
wowooai daemon restart        # 等当前任务结束后重启
```

详见 [22-runner-queue.md §6](22-runner-queue.md)。

## 8. uninstall

```bash
wowooai uninstall             # 删除 ~/.wowooai/（要求二次确认）
```

**不**删除：

- 仓库代码（用户开发态运行）
- 桌面 `.app` / Windows 安装目录（由系统卸载器处理）

## 9. 凭据隐私

- CLI 输出**不**打印完整 API key / token —— 默认 mask（`sk-***...***xxxx`）。
- `wowooai auth show` 显式给出 token 给用户复制时仍 mask 中段。
- doctor 输出避免 echo `Authorization` header。

## 10. 0.0.1 不做

- 不做交互式 TUI（仅 click + 文本输出）。
- 不做 shell completion 自动安装（用户自行 `_WOWOOAI_COMPLETE=...`）。
- 不做 CLI 配置文件 `~/.wowooairc`（一切走 `last_api.json` 与命令行参数）。
- 不做远程 CLI（不能 `wowooai --host 公网 ...`，因为后端鉴权按 `allow_no_auth_hosts` 限制）。

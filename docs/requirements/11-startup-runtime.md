# 11 — 启动流程与运行时

> 版本：0.0.1
> 对应代码：[src/wowooai/cli/](../../src/wowooai/cli/) · [src/wowooai/app/](../../src/wowooai/app/) · launcher（打包产物）
> 关联：[docs/changelog/startup.md](../changelog/startup.md)

## 1. 启动入口

| 场景 | 入口 |
|---|---|
| 开发态（源码） | `python -m wowooai app --host 127.0.0.1 --port 8088` |
| 桌面包（macOS） | `WowooAI.app/Contents/MacOS/WowooAI` |
| 桌面包（Windows） | `WowooAI.exe` |
| CLI | `python -m wowooai <subcommand>`（cron / chat / migrate 等） |

## 2. 桌面包启动顺序（launcher）

launcher 是 PyInstaller 编译的小二进制，做以下事：

1. **解析自身路径** → 找到同级 `bundled-venv/`、`console-dist/`、`node/`。
2. **设置环境变量**：
   - `PATH` prepend `bundled-venv/bin`（macOS）/ `bundled-venv\Scripts`（Windows）
   - `PATH` prepend `node/bin` 或 `node\`
   - `PLAYWRIGHT_BROWSERS_PATH` 指向 bundle 内 Chromium
   - `WOWOOAI_PARENT_PID` = launcher 自身 PID（供 watchdog 用）
3. **挑选随机端口**（避开常用端口）：例如 60494。
4. **启动后端**：spawn `bundled-venv/bin/python3 -m wowooai app --host 127.0.0.1 --port <port>`。
5. **等待 `/api/health` 就绪**（最长 30 秒，超时报错退出）。
6. **启动 pywebview** 窗口，载入 `http://127.0.0.1:<port>`。
7. **进入主循环**；窗口关闭 → 先 SIGTERM 后端进程 → 等待 5 秒 → SIGKILL 兜底。

## 3. 后端启动顺序（`wowooai app`）

1. 加载 `~/.wowooai/config.json`（不存在则用默认创建）。
2. `write_last_api(host, port)` → 写 `~/.wowooai/last_api.json`，供其他工具发现 API。
3. **配置迁移**：检测 `config.json` 版本，按需迁移老字段（`agents.defaults.heartbeat` → `agent.json > heartbeat` 等）。
4. **`ensure_default_agent`**：若 `workspaces/default/` 不存在则创建（含默认 11 个技能 + `wowooai` 显示名）。
5. **`ensure_qa_agent`**：若 `workspaces/qa/` 不存在则创建（QA 助手，专门用 `QA_source_index` skill）。
6. 加载所有 workspace 的 `agent.json`，初始化 `MultiAgentManager`。
7. 启动渠道（仅 `enabled=True` 的）。
8. 启动 cron 调度器（APScheduler）→ 注册各 workspace 的 `jobs.json`。
9. 启动 FastAPI（uvicorn）。

## 4. Parent watchdog

桌面包后端进程检测 `WOWOOAI_PARENT_PID` 环境变量：

- 后端每 5 秒检查父进程是否还活着（`os.kill(pid, 0)`）。
- 父进程消失 → 后端自杀（避免孤儿后端继续占端口）。

源码启动（无 `WOWOOAI_PARENT_PID`）跳过此检查。

## 5. 开发态启动硬规则（避免旧目录污染）

[docs/changelog/startup.md](../changelog/startup.md) 强制规定：

- **必须用绝对路径启动**：`/Users/rlw/AI项目/wowooai/.venv/bin/python3 -m wowooai app ...`
- **禁止用相对命令**（`python -m wowooai ...` / `.venv/bin/python ...`）—— 会因 shell 当前目录而启动到错误仓库。
- 同时启动 5174 前端 dev server 时，后端必须显式允许跨域：
  ```bash
  wowooai_CORS_ORIGINS="http://127.0.0.1:5174,http://localhost:5174" ...
  ```

启动前检查 8088 端口：
```bash
lsof -nP -iTCP:8088 -sTCP:LISTEN -t
```
若有进程必须先确认 `cwd` 指向当前仓库，否则 kill 后再启动。

## 6. `last_api.json`

```json
{
  "host": "127.0.0.1",
  "port": 8088,
  "token": "<bearer>",
  "pid": 12345,
  "started_at": "2026-05-14T10:30:00"
}
```

用途：
- CLI（`wowooai cron list`）从这里读 host/port/token，无需用户传参。
- 第三方脚本可以读这个文件自动连上 API。

## 7. 端口策略

| 场景 | 端口 |
|---|---|
| `wowooai app` 默认 | 8088 |
| 桌面包 launcher | 随机（如 60494） |
| 前端 dev server | 5174 |
| Docker 反代 | 由 reverse proxy 决定 |

前端走相对路径，三种场景同一份代码（见 [07-frontend.md §5](07-frontend.md)）。

## 8. 关闭流程

- pywebview 窗口关闭 → launcher 对后端发 SIGTERM。
- 后端 FastAPI shutdown 钩子：
  1. 停止接受新请求。
  2. 停止所有渠道（disconnect bot / 关闭 websocket）。
  3. 停止 cron 调度器（等待运行中的 job 完成或超时）。
  4. 关闭所有 agent（flush memory 到磁盘）。
  5. 关闭 MCP client / ACP runner（terminate stdio 子进程）。
  6. 退出。

5 秒内未退出 → launcher 发 SIGKILL。

## 9. 0.0.1 不做

- 不做 systemd / launchd 后台服务模式。
- 不做多端口 / 多实例（一台机器同时只能跑一个桌面包实例）。
- 不做端口冲突自动重试（端口被占就报错退出，由用户处理）。
- 不做远程启动 / 远程关闭 API。

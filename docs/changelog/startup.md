# 本地启动要求

> 本文记录 WowooAI 本机联调的固定启动方式。下次启动必须按本文执行，避免 8088 端口继续跑旧仓库 `/Users/rlw/AI项目/wowooai_last/`，导致前端请求打到旧后端并出现 404。

## 背景

本机长期同时存在多个源码副本，例如：

- 当前应使用：`/Users/rlw/AI项目/wowooai/`
- 旧副本：`/Users/rlw/AI项目/wowooai_last/`

如果使用相对命令启动后端，例如 `.venv/bin/python -m wowooai ...` 或 `python -m wowooai ...`，实际启动的是“当前 shell 所在目录”的版本。只要终端曾经停留在旧目录，就可能把旧仓库启动到 8088。

曾经确认过的错误状态：

```text
PID: 69606
command: .venv/bin/python -m wowooai app --host 127.0.0.1 --port 8088
cwd: /Users/rlw/AI项目/wowooai_last
PPID: 1
```

`PPID=1` 表示这是孤儿后台进程，原启动终端已经退出，但进程仍在 8088 上存活，所以不会自动消失，必须手动 kill。

## 后端启动前检查

每次启动后端前，先检查 8088：

```bash
lsof -i :8088 -P -n
```

如果有进程，继续确认它的工作目录：

```bash
PID=$(lsof -nP -iTCP:8088 -sTCP:LISTEN -t | head -1)
[ -n "$PID" ] && lsof -p "$PID" | grep cwd
```

如果 cwd 不是：

```text
/Users/rlw/AI项目/wowooai
```

必须先停止旧进程：

```bash
[ -n "$PID" ] && kill "$PID"
```

如果普通 kill 后端口仍被占用，再执行：

```bash
[ -n "$PID" ] && kill -9 "$PID"
```

## 后端唯一启动命令

必须使用当前仓库 `.venv` 的绝对路径启动。若同时启动 5174 前端 dev server，后端必须显式允许 5174 跨域，否则浏览器会拦截前端 API 请求：

```bash
cd /Users/rlw/AI项目/wowooai
wowooai_CORS_ORIGINS="http://127.0.0.1:5174,http://localhost:5174" \
  /Users/rlw/AI项目/wowooai/.venv/bin/python3 -m wowooai app --host 127.0.0.1 --port 8088
```

禁止使用以下相对命令：

```bash
python -m wowooai app --host 127.0.0.1 --port 8088
.venv/bin/python -m wowooai app --host 127.0.0.1 --port 8088
```

原因：这些命令依赖当前目录，容易在旧仓库下启动旧版本。

## 后端启动后检查

启动后必须确认 cwd：

```bash
PID=$(lsof -nP -iTCP:8088 -sTCP:LISTEN -t | head -1)
lsof -p "$PID" | grep cwd
```

正确输出必须包含：

```text
/Users/rlw/AI项目/wowooai
```

并且不能包含：

```text
wowooai_last
```

然后验证关键接口：

```bash
curl -s -H "X-Agent-Id: default" http://127.0.0.1:8088/api/workspace/files | head -c 200
curl -s -H "X-Agent-Id: default" http://127.0.0.1:8088/api/workspace/system-prompt-files | head -c 200
curl -s http://127.0.0.1:8088/api/agents | head -c 200
curl -i -X OPTIONS http://127.0.0.1:8088/api/agents \
  -H "Origin: http://127.0.0.1:5174" \
  -H "Access-Control-Request-Method: GET" | head -n 20
```

预期：

- `/api/workspace/files` 返回 200，不再是 404
- `/api/workspace/system-prompt-files` 返回 200，不再是 404
- `/api/agents` 返回包含 `default` 和 `wowooai_QA_Agent_0.2` 的列表
- CORS 预检返回 200，响应头包含 `access-control-allow-origin: http://127.0.0.1:5174`

## 前端启动命令

前端也固定从当前仓库启动：

```bash
cd /Users/rlw/AI项目/wowooai/console
VITE_API_BASE_URL=http://127.0.0.1:8088 pnpm dev --host --port 5174
```

## 故障判断

如果“我的记忆”页面请求：

```text
/api/workspace/files
/api/workspace/system-prompt-files
```

出现 404，第一反应不是改前端请求路径，而是先检查 8088 的 cwd：

```bash
PID=$(lsof -nP -iTCP:8088 -sTCP:LISTEN -t | head -1)
lsof -p "$PID" | grep cwd
```

只要 cwd 指向 `wowooai_last` 或其他旧目录，就说明前端打到了旧后端，需要按本文重启后端。

如果 5174 页面能打开，但接口全部报错或浏览器控制台出现 CORS / Network Error，优先确认 8088 后端是否按本文带 `wowooai_CORS_ORIGINS` 启动：

```bash
curl -i -X OPTIONS http://127.0.0.1:8088/api/agents \
  -H "Origin: http://127.0.0.1:5174" \
  -H "Access-Control-Request-Method: GET" | head -n 20
```

正确结果应包含：

```text
HTTP/1.1 200 OK
access-control-allow-origin: http://127.0.0.1:5174
```

如果返回 405 或没有 `access-control-allow-origin`，说明后端缺少 CORS 环境变量，需要按“后端唯一启动命令”重启。

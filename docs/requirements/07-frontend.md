# 07 — 前端控制台（Frontend）

> 版本：0.0.1
> 对应代码：[console/src/](../../console/src/)
> 启动：`pnpm dev --host --port 5174`（开发） / `console/dist`（打包后由 FastAPI 静态托管）

## 1. 导航结构

### 1.1 顶层

| 区 | 路由 | 用途 |
|---|---|---|
| 聊天 | `/chat` | 与当前数字员工对话 |
| 数字员工 | `/agent/*` | 当前数字员工配置 |
| 控制 | `/control/*` | 渠道、定时任务、心跳、会话 |
| 设置 | `/settings/*` | 全局设置 |
| 登录 | `/login` | 首次配置 token |

### 1.2 "数字员工"子页

| 路径 | 内容 |
|---|---|
| `/agent/config` | 名称、描述、模型、审批级别、scene_prompts |
| `/agent/skills` | 当前 agent 已装技能（启停 / 编辑 / 卸载） |
| `/agent/tools` | 内置工具开关（display_to_user / async_execution） |
| `/agent/mcp` | MCP client 列表 |
| `/agent/acp` | ACP 外部 agent 配置 |
| `/agent/workspace` | 工作区文件浏览（含 MEMORY.md / memory/*.md） |

### 1.3 "控制"子页

| 路径 | 内容 |
|---|---|
| `/control/channels` | 14 个渠道开关与凭据配置 |
| `/control/cronjobs` | 定时任务管理 |
| `/control/heartbeat` | 心跳任务配置 |
| `/control/sessions` | 多会话归档 |

### 1.4 "设置"子页

| 路径 | 内容 |
|---|---|
| `/settings/agents` | 数字员工列表（创建 / 切换 / 删除 / 排序） |
| `/settings/models` | LLM provider 与模型槽 |
| `/settings/skill-pool` | 内置 + 自定义 skill 仓库 |
| `/settings/security` | 工具守卫 / 文件守卫 / 技能扫描 / 副本沙箱 |
| `/settings/environments` | 环境变量 / 工作目录 |
| `/settings/backups` | 配置与工作区备份 |
| `/settings/voice-transcription` | Whisper 设置 |
| `/settings/token-usage` | Token 用量统计 |
| `/settings/agent-stats` | 数字员工运行统计 |
| `/settings/debug` | 调试日志 / API 探测 |

## 2. 术语统一

| 后端代码 | 前端显示（用户可见） |
|---|---|
| Agent | **数字员工** |
| `default` agent | **wowooai**（默认数字员工） |
| Chat / Conversation | **对话** |
| Session | **会话** |
| Skill | **技能** |
| Tool | **工具** |
| Provider | **模型供应商** |
| Channel | **渠道** |
| Workspace | **工作区** |

**保留英文**：MCP / ACP / Agent Key / API Key / Token / SDK / CLI 等技术名词。

菜单全中文；ACP / Agent Key 等技术 ID 名保留原文。

## 3. 聊天页（/chat）

### 3.1 区块

- 顶部：数字员工下拉切换 + 模型槽显示 + token 用量。
- 中部：消息流（用户气泡 + 数字员工气泡 + 工具调用折叠卡 + thinking 折叠块）。
- 底部：输入框（支持上传 / 多模态 / @ 提及）。
- 欢迎页：scene_prompts 卡片（0-6 项，点击即发送）。

### 3.2 消息块类型

| Block | 渲染 |
|---|---|
| TextBlock | Markdown |
| ImageBlock | 图片缩略图 + 点开预览 |
| FileBlock | 文件卡片（点击下载，走 `/api/files/preview/...`） |
| ToolUseBlock | 工具调用折叠卡 |
| ToolResultBlock | 工具结果折叠（受 `tool_result_pruning` 限制） |
| ThinkingBlock | 思考折叠块（可全局过滤） |

### 3.3 文件下载

- bot 发的文件：`send_file_to_user` → 同源 HTTP 相对路径 `/api/files/preview/<path>`。
- 桌面端：通过 `WebViewAPI.save_file` 触发系统保存对话框（处理中文名、扩展名兜底）。
- 浏览器端：直接走 `window.open` 新开页下载。

## 4. 默认值同步

前端必须与后端默认值一致：

| 字段 | 默认 | 同步点 |
|---|---|---|
| `JobRuntimeSpec.timeout_seconds` | 1200 | [console/src/pages/Control/CronJobs/components/constants.ts](../../console/src/pages/Control/CronJobs/components/constants.ts) |
| `approval_level` | `AUTO` | Settings / Security 默认选项 |
| `language` | `zh` | 全局 i18n 默认 |
| 聊天 SSE 心跳 | 与后端 `/api/chat/stream` 一致 | — |

## 5. API base URL

前端走**同源相对路径**（如 `/api/...`），不写死 host:port。原因：

- 桌面包随机端口（60494 等）
- `wowooai app` 默认 8088
- Docker 反代 `https://<domain>`

三种场景下同一份代码均可用。

## 6. 多语言

- 默认中文；UI 全套支持 zh / en。
- 切换语言走 `i18next` + `<workspace>/agent.json > language`。
- SKILL.md 双语对应（`<name>-zh` / `<name>-en`），跟随 agent language。

## 7. 状态管理

- 全局：Zustand stores（agents / settings / chat / tools）。
- 实时：SSE 订阅 `/api/chat/stream` 拉消息流与工具调用事件。
- 缓存：`react-query` 用于配置类只读 API（providers / skill_pool / tools）。

## 8. 桌面集成（pywebview）

- `WebViewAPI` 暴露 `save_file(url, filename)` 给前端 `window.pywebview.api.save_file`。
- 前端拦截 `window.open` 非 http(s) 链接，转 `save_file`。
- 桌面包随机端口由 launcher 决定，前端通过相对路径无感对接。

## 9. 0.0.1 不做

- 不做插件市场页面（plugin 仅通过 config.json 配置）。
- 不做主题切换（默认浅色 + 系统色跟随）。
- 不做多用户登录（单机单用户）。
- 不做团队协作 / 实时多人编辑工作区。

# 09 — MCP 与 ACP

> 版本：0.0.1
> 对应代码：[src/wowooai/app/mcp/](../../src/wowooai/app/mcp/) · `MCPConfig` · `ACPConfig` · [src/wowooai/agents/tools/delegate_external_agent.py](../../src/wowooai/agents/tools/delegate_external_agent.py)

## 1. MCP（外部工具协议）

### 1.1 定位

MCP（Model Context Protocol）让数字员工像调用内置工具一样调用外部进程暴露的工具（搜索、知识库、API 网关等）。

### 1.2 配置存储

`agent.json > mcp.clients` 是 dict：

```json
{
  "tavily_search": {
    "name": "tavily_mcp",
    "enabled": false,
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "tavily-mcp@latest"],
    "env": { "TAVILY_API_KEY": "" }
  }
}
```

### 1.3 MCPClientConfig 字段

| 字段 | 用途 |
|---|---|
| `name` | client 名（注册到 toolkit 的命名空间前缀） |
| `description` | 显示用 |
| `enabled` | 开关 |
| `transport` | `stdio` / `streamable_http` / `sse` |
| `url` | 非 stdio 必填 |
| `headers` | HTTP 请求头 |
| `command` / `args` / `env` / `cwd` | stdio 启动参数 |

### 1.4 字段别名兼容

`_normalize_legacy_fields` 处理常见第三方示例的字段别名：

| 源字段 | 归一化为 |
|---|---|
| `isActive` | `enabled` |
| `baseUrl` | `url` |
| `type` | `transport` |
| `streamableHttp` / `http` | `streamable_http` |

URL 存在但未指定 transport 时默认推断 `streamable_http`。

### 1.5 Transport 校验

- `stdio` 必须有非空 `command`
- `streamable_http` / `sse` 必须有非空 `url`

校验失败抛 `ConfigurationException`。

### 1.6 默认 client：tavily_search

```python
"tavily_search": MCPClientConfig(
    name="tavily_mcp",
    enabled=False,
    command="npx",
    args=["-y", "tavily-mcp@latest"],
    env={"TAVILY_API_KEY": ""},
)
```

用户填入 API key 并启用后即可用。

### 1.7 注册到 ReAct toolkit

启动 workspace 时：

1. `MCPClientManager` 启动所有 `enabled=True` 的 client。
2. `ReActAgent.register_mcp_clients` 调 `_register_mcp_client_compat` 把每个 client 注册到 AgentScope `Toolkit`。
3. 兼容 helper **不**传 `execution_timeout` 参数（agentscope 1.0.19.post1 不支持）。

### 1.8 失败恢复

MCP 进程崩溃时 `MCPClientManager` 会重连；恢复后通过同一 helper 重新注册到 toolkit，确保对话运行时仍能看到工具。

### 1.9 UI

`/agent/mcp` 页提供 CRUD（新增 client / 编辑 / 启停 / 查看工具列表 `/api/mcp/<key>/tools`）。

## 2. ACP（外部 Agent 协议）

### 2.1 定位

ACP（Agent Communication Protocol）让数字员工把任务派给外部 agent runner（其他 IDE / CLI agent）。0.0.1 内置 4 个：

| 默认 agent | command | tool_parse_mode |
|---|---|---|
| `opencode` | `opencode` `acp` | `update_detail` |
| `qwen_code` | `qwen` `--acp` | `call_detail` |
| `claude_code` | `npx` `-y @zed-industries/claude-agent-acp` | `update_detail` |
| `codex` | `npx` `-y @zed-industries/codex-acp` | `call_detail` |

### 2.2 ACPAgentConfig 字段

| 字段 | 默认 |
|---|---|
| `enabled` | False（MCPConfig 中默认 client 是 True，ACP 是 False） |
| `command` | "" |
| `args` | `[]` |
| `env` | `{}` |
| `trusted` | True |
| `tool_parse_mode` | `call_title` |
| `stdio_buffer_limit_bytes` | 50 MB |

### 2.3 默认合并

`ACPConfig._merge_default_agents` 在加载用户配置后把内置 4 个默认 agent 自动并入；用户手动禁用的不会被覆盖。

### 2.4 调用入口

工具 `delegate_external_agent` 默认 `enabled=False`。启用后调用方式：

```python
delegate_external_agent(
    agent_name="claude_code",
    prompt="帮我重构这个文件",
    cwd="/path/to/project",
)
```

通过 stdio 启动 ACP agent，按 ACP 协议交换消息，把外部 agent 的工具调用 / 输出解析后回填到当前会话。

### 2.5 tool_parse_mode

| 模式 | 解析方式 |
|---|---|
| `call_title` | 只展示工具名（最简） |
| `call_detail` | 展示工具名 + 参数 |
| `update_detail` | 展示完整调用与更新（详细） |

### 2.6 信任级别

`trusted=True`：外部 agent 的工具调用直接执行，不走本地 tool guard。
`trusted=False`：外部 agent 的工具调用走本地审批流程。

### 2.7 UI

`/agent/acp` 页提供 4 个内置 agent 的开关、命令编辑、env 编辑。

## 3. MCP vs ACP 对比

| 维度 | MCP | ACP |
|---|---|---|
| 协议目标 | 工具集协议 | Agent 间通信协议 |
| 典型场景 | 调用搜索 / 知识库 / API 网关 | 把任务派给另一个 agent |
| 数据流 | 工具调用 + 结果 | 完整对话 + 工具调用 + 工具结果 |
| 默认开启 | tavily_search 默认 False | 4 个 agent 全部 False |
| 用户启用门槛 | 配置一个 API key | 安装外部 CLI（如 npx claude-agent-acp） |

## 4. 凭据隐私

- MCP env 中的 API key 仅存 `agent.json`。
- ACP command / args / env 同理。
- 严禁把任何 MCP / ACP 凭据写入仓库内置默认值。

## 5. 0.0.1 不做

- 不做内置 MCP server（仅做 client 接入）。
- 不做 ACP agent server（仅做 client 调用外部 agent）。
- 不做 MCP / ACP 间桥接（如把外部 agent 暴露成 MCP 工具）。
- 不做 MCP / ACP 的 Web 远程托管（全部本机进程）。

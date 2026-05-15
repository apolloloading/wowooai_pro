# 合入优先级评估

> 这是给你决策用的入口：先看 P0/P1，再看 P2，P3 通常跳过。

## P0-优先尝试（12）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 4 | `59ebc8e` | ✅ 直接合入 | 聊天体验/会话 | feat(chat) adjust CodeMirror line wrapping in tool call input/output blocks (#3960) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 风险较低，主要看编译和运行验证 |
| 14 | `b458910` | ✅ 直接合入 | Console UI | perf(console): Solve duplicate rendering (#4052) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 32 | `16c28e9` | ✅ 直接合入 | 通用/其他 | fix(console): respect custom name for default agent (#4073) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 38 | `67ff5aa` | ✅ 直接合入 | 打包/发布 | fix(pack): restore conda packaging tools before conda-pack (#4093) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 风险较低，主要看编译和运行验证 |
| 54 | `804cb82` | ✅ 直接合入 | 聊天体验/会话 | perf(console): skip chat history lookup for non-arrow keys (#4130) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 风险较低，主要看编译和运行验证 |
| 66 | `cf18e6c` | ✅ 直接合入 | 渠道集成 | fix(console): Immediately stop polling and clear the status after closing the drawer. (#4148) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 67 | `c3b56c0` | ✅ 直接合入 | Console UI | fix(agent-config): preserve complete config on save to prevent nested config loss (#4157) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 风险较低，主要看编译和运行验证 |
| 74 | `cc57579` | ✅ 直接合入 | Console UI | fix(console): improve text contrast in Plan Panel dark mode (#4190) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 79 | `e16a5dd` | ✅ 直接合入 | 聊天体验/会话 | Fix(session): session history disappearing and messages being routed to a different session (#4203) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 风险较低，主要看编译和运行验证 |
| 93 | `aa4961c` | 🟡 裁剪合入 | 聊天体验/会话、国际化、模型/Provider | feat(chat): refactor chat model selector into searchable flat list with provider grouping (#3876) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 会碰到我方术语/翻译定制 |
| 94 | `63cea54` | ✅ 直接合入 | Console UI | fix(console): collapse sidebar on mobile (#4225) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 107 | `207c278` | ✅ 直接合入 | 渠道集成、Console UI | fix(console): replace window.open calls with openExternalLink utility in ACPDrawer and ChannelDrawer components (#4270) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |

## P1-重点评审（1）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 46 | `c832082` | 🟠 待人工 | 聊天体验/会话 | perf(console,chat): chat performance optimization (#4110) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 风险较低，主要看编译和运行验证 |

## P1-建议移植评审（57）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 2 | `518ce42` | 🔴 跳过-冲突 | 渠道集成、安全/审批 | feat(feishu): introduce FeishuCardHandler and upgrade tool_guard approval to interactive buttons (#3941) | 增强飞书渠道能力，包括卡片交互、连接探活、语音气泡或 OAuth 创建设定。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 3 | `d9526bf` | 🔴 跳过-冲突 | 渠道集成 | fix(WeCom): keep placeholder stream alive to prevent stuck "Thinking..."  (#3950) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 5 | `90cf5ac` | 🔴 跳过-冲突 | 渠道集成 | fix(WeCom): avoid double reconnect race and cross-loop disconnect (#3963) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 12 | `534d8ba` | 🔴 跳过-冲突 | 通用/其他 | fix(message_processing): return resolved path for file:// url audio blocks (#4021) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 13 | `694d317` | 🔴 跳过-冲突 | 模型/Provider | fix(provider): increase max_token for anthropic compatible models (#4054) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 15 | `edf8ed1` | 🔴 跳过-冲突 | MCP、计划/执行器 | fix(mcp): typo fix (#4058) | 修复或增强 MCP 客户端/远程 MCP 连接，包括超时、生命周期或 OAuth。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 16 | `a8be4d7` | 🔴 跳过-冲突 | MCP、计划/执行器 | fix(mcp): use read_timeout_seconds as MCP tool execution_timeout instead of timeout (#4061) | 修复或增强 MCP 客户端/远程 MCP 连接，包括超时、生命周期或 OAuth。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 18 | `e43731e` | 🔴 跳过-冲突 | 渠道集成 | fix(telegram): telegram network retry (#4039) | 增强 Telegram 渠道重试或流式编辑消息能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 20 | `5c49769` | 🔴 跳过-冲突 | 技能系统 | fix(skill):  resilient loading for migrated or malformed skill & skill pool entries (#4016) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；可能影响我方入职小助手/技能路径 |
| 21 | `27579ce` | 🔴 跳过-冲突 | 计划/执行器、安全/审批 | fix(approval): /approve shorthand ignores request_id argument (#4014) | 调整安全规则或审批命令处理。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 27 | `769230d` | 🔴 跳过-冲突 | 渠道集成 | fix(console): avoid SSE crash on malformed surrogate text (#3553) | 调整 Console 前端页面、布局、样式或交互行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 30 | `166dc49` | 🔴 跳过-冲突 | Console UI、模型/Provider | Feat(provider): add volcengine provider (#3994) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 33 | `4ee41a8` | 🔴 跳过-冲突 | 聊天体验/会话 | fix(chat): remove redundant URL prefix stripping in file preview paths (#4089) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 36 | `3213fd1` | 🔴 跳过-冲突 | Console UI、国际化、插件系统 | plugin: add gpt-image-2 tool plugin (#3911) | 扩展插件系统或新增图像/云部署插件能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 41 | `e6e0dcd` | 🔴 跳过-冲突 | 渠道集成、定时任务/Inbox | fix(WeChat): flush WeChat merge buffer immediately for cron sends (#4106) | 调整微信/企业微信迁移或消息缓冲行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 44 | `411603e` | 🔴 跳过-冲突 | 国际化、模型/Provider、记忆系统 | feat(cron): add channel-based session isolation for session and share option for cron jobs (#4117) | 增强定时任务、收件箱、会话隔离或消息推送链路。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 47 | `b2f9417` | 🔴 跳过-冲突 | 通用/其他 | fix: use RotatingFileHandler for log rotation on all platforms (#4076) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 51 | `01750d9` | 🔴 跳过-冲突 | 计划/执行器 | fix(reload): route AgentConfigWatcher through reload_agent for graceful task draining (#4064) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 52 | `8a6d2dc` | 🔴 跳过-冲突 | Console UI、模型/Provider | feat(provider): add aliyun token plan as a built-in provider (#4122) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 53 | `9c9deab` | 🔴 跳过-冲突 | 计划/执行器 | fix(runner): rename channel variable to channel_name in command dispatch (#4134) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 55 | `ec8aad8` | 🔴 跳过-冲突 | 模型/Provider | fix(tool_schema): add sanitize tool function schemas (#4126) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 56 | `d4ebc9f` | 🔴 跳过-冲突 | 工具/浏览器/文件 | fix(cli): bypass proxies for loopback API checks (#4092) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 57 | `5c1cd03` | 🔴 跳过-冲突 | 计划/执行器 | fix(agent): replace hardcoded agent name with config-driven value (#4140) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 58 | `90a145d` | 🔴 跳过-冲突 | 渠道集成 | fix(channels): keep markdown tables renderable across split_text chunks (#4119) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 59 | `171030f` | 🔴 跳过-冲突 | 通用/其他 | fix(agent): emoji example in AGENTS.md (#4142) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 60 | `3b884f4` | 🔴 跳过-冲突 | 备份/恢复 | fix(backup): restore secrets on Docker volume mount points (#3916) | 修复 Docker volume 等场景下的备份恢复逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 63 | `8b8ddba` | 🔴 跳过-冲突 | 渠道集成、安全/审批 | feat(WeCom): tool-guard interactive approval card (#4112) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 64 | `c6019fb` | 🔴 跳过-冲突 | Console UI、国际化、模型/Provider | feat(provider): allow Dashscope base URL selection in Console UI (#4074) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 65 | `c46996b` | 🔴 跳过-冲突 | 工具/浏览器/文件 | fix(agent-tools): add safe default timeout for delegate_external_agent (#3928) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 69 | `0dc50af` | 🔴 跳过-冲突 | MCP | fix lifecycle-task leak in stateful clients and refactor shared logic into mixin (#4152) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 72 | `53cd8b1` | 🔴 跳过-冲突 | 模型/Provider | Fix(provider): fix models in VOLCENGINE Provider (#4169) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 75 | `eb01c83` | 🔴 跳过-冲突 | 渠道集成、模型/Provider、安全/审批 | fix(provider,wecom): preserve provider meta field and update tool_guard docstring in wecom (#4200) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 77 | `b8c33a1` | 🔴 跳过-冲突 | 工具/浏览器/文件 | feat(tool): browser_use add batch action support to browser_use tool (#4139) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 78 | `abd8066` | 🔴 跳过-冲突 | 记忆系统 | feat(memory): add auto-memory management features (#4204) | 增强长期记忆/自动记忆配置和管理能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 80 | `d361099` | 🔴 跳过-冲突 | Console UI、插件系统、计划/执行器 | feat(tool): Add async execution support for delegate_external_agent (#4197) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 83 | `fe13fe2` | 🔴 跳过-冲突 | 模型/Provider、技能系统、计划/执行器 | fix(exception): fix ConfigurationException key passing (#4212) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 85 | `44ffdb8` | 🔴 跳过-冲突 | 模型/Provider | perf(api): optimize async depends to fix thread pool blocking (#4229) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 86 | `c89ed13` | 🔴 跳过-冲突 | 模型/Provider | fix(model): filter out malformed tool_use blocks from OpenAI-compatible model responses (#4234) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 89 | `b1ff519` | 🔴 跳过-冲突 | 渠道集成 | fix(feishu): detect silent WebSocket connection loss in Feishu channel (#4241) | 增强飞书渠道能力，包括卡片交互、连接探活、语音气泡或 OAuth 创建设定。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 91 | `61475f2` | 🔴 跳过-冲突 | 渠道集成 | feat(channels): support native voice bubble in Feishu channel (#4202) | 增强飞书渠道能力，包括卡片交互、连接探活、语音气泡或 OAuth 创建设定。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 92 | `64e5de9` | 🔴 跳过-冲突 | 渠道集成、安全/审批 | fix(WeCom): show operator in resolved approval card (#4233) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 98 | `c1ce3db` | 🔴 跳过-冲突 | Console UI、国际化、记忆系统 | feat(memory): add ADBPG long-term memory with BaseMemoryManager architure (#2308) | 增强长期记忆/自动记忆配置和管理能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；会碰到包名/品牌/发布材料；改动很大，需单独分支验证 |
| 99 | `d4395e7` | 🔴 跳过-冲突 | MCP | fix(mcp): add monkey patch for mcp (#4245) | 修复或增强 MCP 客户端/远程 MCP 连接，包括超时、生命周期或 OAuth。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 106 | `475fe26` | 🔴 跳过-冲突 | Console UI、国际化、MCP | feat(mcp): add OAuth 2.1 PKCE support for remote MCP servers (#4256) | 修复或增强 MCP 客户端/远程 MCP 连接，包括超时、生命周期或 OAuth。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 109 | `dc2ce24` | 🔴 跳过-冲突 | 渠道集成、国际化 | feat(channel): add streaming output hooks to BaseChannel with WeCom support (#4271) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 110 | `b1770de` | 🔴 跳过-冲突 | 工具/浏览器/文件 | Fix(tool): read_file_safe allocation size (#4272) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 111 | `503390d` | 🔴 跳过-冲突 | 工具/浏览器/文件 | perf(tools): reduce maximum file read size to 200MB (#4276) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 112 | `af65842` | 🔴 跳过-冲突 | 打包/发布 | fix(QA agent): package website/public/docs into wheel and sdist (#4275) | 修复打包流程依赖或环境问题。 | 会碰到包名/品牌/发布材料 |
| 113 | `67cb469` | 🔴 跳过-冲突 | 工具/浏览器/文件 | Feat(tool): Add action="file_download" for browser use (#4261) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 114 | `9f49c91` | 🔴 跳过-冲突 | 聊天体验/会话、Console UI、国际化 | feat(cron & inbox): add inbox and optimize the cron job (#4210) | 增强定时任务、收件箱、会话隔离或消息推送链路。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 117 | `7a0b62f` | 🔴 跳过-冲突 | 模型/Provider | Fix(Provider): Fix anthropic provider max token handling (#4317) | 调整模型供应商能力、内置供应商、max_tokens 或 provider 配置 UI。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 118 | `fc6be99` | 🔴 跳过-冲突 | 渠道集成、安全/审批 | feat(WeCom): support tool_guard interactive card in streaming path (#4307) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 122 | `a49dc9e` | 🔴 跳过-冲突 | 工具/浏览器/文件 | fix(tool): browser implement activity tracking, crash monitoring, and lifecycle management (#4306) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 125 | `d8ac7f6` | 🔴 跳过-冲突 | Console UI、技能系统 | fix(skill): fix skill hub import: fix www, add skill_hub retry (#4359) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；可能影响我方入职小助手/技能路径 |
| 127 | `11f2136` | 🔴 跳过-冲突 | 技能系统 | fix(skill): fix skill path, use safer path normalizer and refactor for function naming (#4335) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；可能影响我方入职小助手/技能路径 |
| 129 | `fc5e6af` | 🔴 跳过-冲突 | 打包/发布 | fix(QA agent): bundle docs as package_data (#4280) | 修复打包流程依赖或环境问题。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到包名/品牌/发布材料；改动很大，需单独分支验证 |
| 130 | `00ede85` | 🔴 跳过-冲突 | 工具/浏览器/文件 | fix(tool): add _CDP_CONNECT_TIMEOUT_SECONDS = 30 for connect cdp (#4350) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |

## P1-按产品取舍（33）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 6 | `2709e95` | 🔴 跳过-冲突 | 渠道集成 | feat(WeCom): add share_session_in_group toggle for group chats (#3948) | 增强企业微信渠道稳定性、群聊/审批卡片/流式输出相关逻辑。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 7 | `c85361a` | 🔴 跳过-冲突 | 通用/其他 | feat(app): prevent path traversal by rejecting absolute static file paths (#3973) | 调整工具调用、浏览器控制、文件读写或工具 schema 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 8 | `9b7acb3` | 🔴 跳过-冲突 | 渠道集成、安全/审批 | feat(feishu): hint docs link on approval card when card.action.trigger is unsubscribed (#3982) | 增强飞书渠道能力，包括卡片交互、连接探活、语音气泡或 OAuth 创建设定。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 11 | `d85181a` | 🔴 跳过-冲突 | Console UI、国际化、计划/执行器 | feat(chat): generate session titles asynchronously via LLM (#3829) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 19 | `bc5a81e` | 🟠 待人工 | Console UI、国际化 | feat(i18n): add Brazilian Portuguese (pt-BR) locale support (#4009) | 小型通用维护或行为调整，需结合文件列表判断。 | 会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 23 | `678cc42` | 🔴 跳过-冲突 | 技能系统 | feat(skill): Add skill install/uninstall cli (#4053) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；可能影响我方入职小助手/技能路径 |
| 29 | `6773901` | 🔴 跳过-冲突 | 聊天体验/会话、国际化 | feat(chat): replace Web Speech API with Whisper transcription for voice input (#3574) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 31 | `e393bc1` | 🔴 跳过-冲突 | Console UI、国际化 | feat(token-usage): add token suage detailed api and trending charts (#4080) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 37 | `5edeef4` | 🔴 跳过-冲突 | Console UI、国际化、技能系统 | feat(console): Add "Enable" and "Disable" buttons to the batch operation of skills (#4091) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 39 | `d6dbf31` | 🔴 跳过-冲突 | 技能系统 | feat(skills): add cli skill test command (#3999) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 40 | `764c7e8` | 🔴 跳过-冲突 | 渠道集成、计划/执行器 | feat(feishu): surface sender nickname to agent env context (#4098) | 增强飞书渠道能力，包括卡片交互、连接探活、语音气泡或 OAuth 创建设定。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 43 | `3673176` | 🔴 跳过-冲突 | Console UI、国际化、安全/审批 | feat(security): add rule level auto deny (#4046) | 调整安全规则或审批命令处理。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 45 | `45afb7c` | 🔴 跳过-冲突 | 计划/执行器 | feat: add agent status endpoint with task tracking (#4107) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 50 | `97d2f3a` | 🔴 跳过-冲突 | 通用/其他 | feat(doctor): add Windows environment diagnostics (#4032) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 61 | `26a9344` | 🔴 跳过-冲突 | 通用/其他 | feat(settings): add pt-BR language support (#4143) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 62 | `2b9564d` | 🟠 待人工 | Console UI | feat(console): support mermaid graph (#4146) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 76 | `60a555b` | 🔴 跳过-冲突 | Console UI、插件系统、打包/发布 | feat(plugins): add reference image support to gpt-image2 plugin (#4194) | 扩展插件系统或新增图像/云部署插件能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 81 | `e455388` | ✅ 直接合入 | 聊天体验/会话 | feat(chat): enable multiple attachments support in chat page (#4206) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 风险较低，主要看编译和运行验证 |
| 82 | `43ca356` | 🔴 跳过-冲突 | 渠道集成 | feat(DingTalk): process quoted messages for user-sent replies (#4209) | 增强钉钉引用消息处理能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 84 | `6ab6979` | ✅ 直接合入 | 聊天体验/会话 | feat(console): user message support newline (#4231) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 87 | `afeea11` | ✅ 直接合入 | Console UI | feat(console): Chat floating in the menu (#4240) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 风险较低，主要看编译和运行验证 |
| 88 | `47db242` | 🔴 跳过-冲突 | Console UI、国际化、计划/执行器 | feat(shell): Add shell_command_executable` configuration to let users choose which shell uses (#4215) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；会碰到包名/品牌/发布材料；改动很大，需单独分支验证 |
| 95 | `9bc51ed` | 🔴 跳过-冲突 | Console UI、国际化 | feat(console): add Indonesian language option (#4219) | 调整 Console 前端页面、布局、样式或交互行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 96 | `aabfd6a` | 🔴 跳过-冲突 | 渠道集成、Console UI、国际化 | feat(plugins): support install/uninstall plugins on console (#4214) | 扩展插件系统或新增图像/云部署插件能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 97 | `b6611fd` | 🔴 跳过-冲突 | 渠道集成、国际化、打包/发布 | feat(feishu): add QR code bot creation via OAuth Device Flow (#4236) | 增强飞书渠道能力，包括卡片交互、连接探活、语音气泡或 OAuth 创建设定。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制 |
| 101 | `7e82329` | 🔴 跳过-冲突 | Console UI、插件系统、打包/发布 | feat(plugins): add Qwen-Image and Wan 2.7 plugins (#4248) | 扩展插件系统或新增图像/云部署插件能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；改动很大，需单独分支验证 |
| 102 | `a82ce8d` | 🔴 跳过-冲突 | 插件系统 | feat(plugins): enable register FastAPI APIRouter instances through plugin (#4255) | 扩展插件系统或新增图像/云部署插件能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 103 | `5bc599a` | 🔴 跳过-冲突 | 安全/审批 | feat: add timeout for keyring (#4263) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 104 | `cb8a8d7` | ✅ 直接合入 | Console UI | feat(console): support crosses year in TokenUsage (#4268) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 121 | `8e189a6` | 🔴 跳过-冲突 | 计划/执行器 | feat(plan mode): Strengthen plan reaffirm from the user message (#4198) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 123 | `251e700` | 🔴 跳过-冲突 | Console UI、国际化、记忆系统 | feat(agent): add Indonesian language option (#4287) | 调整 Agent 执行器、配置重载、计划模式或默认 Agent 行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 124 | `83828a8` | 🔴 跳过-冲突 | 渠道集成 | feat(telegram): add streaming output via editMessageText (#4318) | 增强 Telegram 渠道重试或流式编辑消息能力。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 128 | `799017e` | 🟠 待人工 | 插件系统、安全/审批、打包/发布 | feat(plugin): add CloudPaw plugin bundle for Alibaba Cloud deployment (#4362) | 扩展插件系统或新增图像/云部署插件能力。 | 改动很大，需单独分支验证 |

## P2-谨慎评审（6）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 28 | `62f22c7` | 🟠 待人工 | Console UI、国际化 | chore(console): Optimize language switching logic and replace with the latest language icon (#4085) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 35 | `50c8712` | 🟠 待人工 | Console UI | refactor(console): adjust and opt TokenUsage page (#4094) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 48 | `ccea67d` | 🟠 待人工 | 聊天体验/会话、Console UI、国际化 | test(console): setup Vitest and add Chat/utils/api unit tests (#3559) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 改动很大，需单独分支验证 |
| 68 | `6a7b39d` | 🟠 待人工 | 渠道集成 | refactor(console): extract QrcodeAuthBlock component and fix polling leak on drawer close (#4153) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 105 | `5dfe1ca` | 🟠 待人工 | Console UI、插件系统 | refactor(console): console/PluginManager (#4266) | 扩展插件系统或新增图像/云部署插件能力。 | 风险较低，主要看编译和运行验证 |
| 116 | `c937ffb` | 🟠 待人工 | Console UI、定时任务/Inbox | refactor(console): Inbox (#4305) | 增强定时任务、收件箱、会话隔离或消息推送链路。 | 风险较低，主要看编译和运行验证 |

## P2-可延后（5）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 17 | `ba7c4fd` | 🔴 跳过-冲突 | 通用/其他 | chore(utils): remove redundant codes (#4048) | 小型通用维护或行为调整，需结合文件列表判断。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 34 | `182528e` | 🔴 跳过-冲突 | 渠道集成、国际化、计划/执行器 | refactor(wechat): centralize legacy weixin to wechat data migrations on workspace startup (#3605) | 调整微信/企业微信迁移或消息缓冲行为。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到我方术语/翻译定制；改动很大，需单独分支验证 |
| 90 | `ec4e7d8` | 🔴 跳过-冲突 | 模型/Provider、技能系统、计划/执行器 | Refactor(skill): Add skill system (#4235) | 调整技能加载、导入、CLI、路径规范化或新技能系统。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；可能影响我方入职小助手/技能路径；改动很大，需单独分支验证 |
| 100 | `977ffe3` | 🔴 跳过-冲突 | 通用/其他 | refactor(agent_stats): streamline session file handling and remove unused code (#4250) | 改善聊天页面、会话路由、语音输入、附件或模型选择体验。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 126 | `f18a3c2` | 🟡 裁剪合入 | Console UI、国际化、定时任务/Inbox | style(console): inbox page (#4358) | 增强定时任务、收件箱、会话隔离或消息推送链路。 | 会碰到我方术语/翻译定制 |

## P3-通常不合（16）

| # | SHA | 标签 | 领域 | 标题 | 为什么看 | 风险 |
|---:|---|---|---|---|---|---|
| 1 | `8aa5f27` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bump version to 1.1.5.post1 (#3970) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 9 | `6368ca3` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bumping version to 1.1.6b1 (#4012) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 10 | `d783c3b` | ⚪ 跳过-无关 | 国际化、模型/Provider、记忆系统 | docs(website): update documentation to v1.1.5 (#4013) | 文档站或 FAQ 更新。 | 会碰到我方术语/翻译定制 |
| 22 | `30dc625` | ⚪ 跳过-无关 | 通用/其他 | docs(faq): Docs for handling APITimeoutError when running in WSL2 (NAT mode) (#4005) | 文档站或 FAQ 更新。 | 风险较低，主要看编译和运行验证 |
| 24 | `24c0610` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bumping version to 1.1.5p2 (#4071) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 25 | `18d7c15` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bump version to 1.1.6b1 (#4082) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 26 | `73e03e2` | ⚪ 跳过-无关 | 通用/其他 | test(integration): add app startup and settings/envs smoke tests (#4081) | 小型通用维护或行为调整，需结合文件列表判断。 | 风险较低，主要看编译和运行验证 |
| 42 | `9fdb426` | 🔴 跳过-冲突 | 打包/发布 | chore: fix openai version (#4118) | 版本号或发布说明更新，不包含业务修复。 | 会碰到包名/品牌/发布材料 |
| 49 | `9a03dd1` | ⚪ 跳过-无关 | 通用/其他 | test(console): frontend test (#4121) | 调整 Console 前端页面、布局、样式或交互行为。 | 风险较低，主要看编译和运行验证 |
| 70 | `047afe5` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bumping version to 1.1.6b2 (#4161) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 71 | `8cc10d2` | 🔴 跳过-冲突 | 打包/发布 | chore(release): update release note of v1.1.6 (#4163) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到包名/品牌/发布材料 |
| 73 | `95908ac` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bumping version to 1.1.7b1 (#4196) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 108 | `af50cf7` | ⚪ 跳过-无关 | Console UI | style: sidebar (#4273) | 小型通用维护或行为调整，需结合文件列表判断。 | 风险较低，主要看编译和运行验证 |
| 115 | `f684c13` | 🔴 跳过-冲突 | 打包/发布 | bumping version to 1.1.7b2 (#4283) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |
| 119 | `8e2a835` | 🔴 跳过-冲突 | 打包/发布 | chore(version): add release note for v1.1.7 (#4319) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai；会碰到包名/品牌/发布材料 |
| 120 | `f2e8b7f` | 🔴 跳过-冲突 | 打包/发布 | chore(version): bumping version to 1.1.8b1 (#4346) | 版本号或发布说明更新，不包含业务修复。 | 不能直接 cherry-pick：路径需从 qwenpaw 映射到 wowooai |

# 影响范围索引

> 按主要影响模块归类。想知道某块是否被上游改过，可以从这里进入。

## Agent 核心/执行（8）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 15 | `edf8ed1` | 🔴 跳过-冲突 | P1 | fix(mcp): typo fix (#4058) | Agent 核心/执行(1) |
| 16 | `a8be4d7` | 🔴 跳过-冲突 | P1 | fix(mcp): use read_timeout_seconds as MCP tool execution_timeout instead of timeout (#4061) | Agent 核心/执行(1), MCP(1) |
| 21 | `27579ce` | 🔴 跳过-冲突 | P1 | fix(approval): /approve shorthand ignores request_id argument (#4014) | Agent 核心/执行(1) |
| 40 | `764c7e8` | 🔴 跳过-冲突 | P1 | feat(feishu): surface sender nickname to agent env context (#4098) | Agent 核心/执行(2), 后端渠道实现(1) |
| 51 | `01750d9` | 🔴 跳过-冲突 | P1 | fix(reload): route AgentConfigWatcher through reload_agent for graceful task draining (#4064) | Agent 核心/执行(2), 其他(1) |
| 53 | `9c9deab` | 🔴 跳过-冲突 | P1 | fix(runner): rename channel variable to channel_name in command dispatch (#4134) | Agent 核心/执行(1) |
| 57 | `5c1cd03` | 🔴 跳过-冲突 | P1 | fix(agent): replace hardcoded agent name with config-driven value (#4140) | Agent 核心/执行(5), 其他(1) |
| 121 | `8e189a6` | 🔴 跳过-冲突 | P1 | feat(plan mode): Strengthen plan reaffirm from the user message (#4198) | Agent 核心/执行(2), 其他(2) |

## MCP（2）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 69 | `0dc50af` | 🔴 跳过-冲突 | P1 | fix lifecycle-task leak in stateful clients and refactor shared logic into mixin (#4152) | MCP(2) |
| 99 | `d4395e7` | 🔴 跳过-冲突 | P1 | fix(mcp): add monkey patch for mcp (#4245) | MCP(1) |

## 其他（20）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 4 | `59ebc8e` | ✅ 直接合入 | P0 | feat(chat) adjust CodeMirror line wrapping in tool call input/output blocks (#3960) | 其他(1) |
| 7 | `c85361a` | 🔴 跳过-冲突 | P1 | feat(app): prevent path traversal by rejecting absolute static file paths (#3973) | 其他(1) |
| 12 | `534d8ba` | 🔴 跳过-冲突 | P1 | fix(message_processing): return resolved path for file:// url audio blocks (#4021) | 其他(1) |
| 17 | `ba7c4fd` | 🔴 跳过-冲突 | P2 | chore(utils): remove redundant codes (#4048) | 其他(1) |
| 28 | `62f22c7` | 🟠 待人工 | P2 | chore(console): Optimize language switching logic and replace with the latest language icon (#4085) | 其他(2), 前端组件(1), 前端页面(1) |
| 32 | `16c28e9` | ✅ 直接合入 | P0 | fix(console): respect custom name for default agent (#4073) | 其他(1) |
| 47 | `b2f9417` | 🔴 跳过-冲突 | P1 | fix: use RotatingFileHandler for log rotation on all platforms (#4076) | 其他(1) |
| 48 | `ccea67d` | 🟠 待人工 | P2 | test(console): setup Vitest and add Chat/utils/api unit tests (#3559) | 其他(12), 前端页面(8), 前端 API/types(5), 前端组件(5) |
| 49 | `9a03dd1` | ⚪ 跳过-无关 | P3 | test(console): frontend test (#4121) | 其他(1) |
| 50 | `97d2f3a` | 🔴 跳过-冲突 | P1 | feat(doctor): add Windows environment diagnostics (#4032) | 其他(2) |
| 56 | `d4ebc9f` | 🔴 跳过-冲突 | P1 | fix(cli): bypass proxies for loopback API checks (#4092) | 其他(3), 测试/CI(3), 工具实现(1) |
| 59 | `171030f` | 🔴 跳过-冲突 | P1 | fix(agent): emoji example in AGENTS.md (#4142) | 其他(3) |
| 60 | `3b884f4` | 🔴 跳过-冲突 | P1 | fix(backup): restore secrets on Docker volume mount points (#3916) | 其他(5), 测试/CI(2) |
| 83 | `fe13fe2` | 🔴 跳过-冲突 | P1 | fix(exception): fix ConfigurationException key passing (#4212) | 其他(2), 技能系统(1), Agent 核心/执行(1) |
| 90 | `ec4e7d8` | 🔴 跳过-冲突 | P2 | Refactor(skill): Add skill system (#4235) | 其他(10), 技能系统(10), 后端 API 路由(3), Agent 核心/执行(2) |
| 95 | `9bc51ed` | 🔴 跳过-冲突 | P1 | feat(console): add Indonesian language option (#4219) | 其他(3), 前端组件(2), 前端国际化(2), 后端 API 路由(1) |
| 100 | `977ffe3` | 🔴 跳过-冲突 | P2 | refactor(agent_stats): streamline session file handling and remove unused code (#4250) | 其他(1) |
| 103 | `5bc599a` | 🔴 跳过-冲突 | P1 | feat: add timeout for keyring (#4263) | 其他(1) |
| 123 | `251e700` | 🔴 跳过-冲突 | P1 | feat(agent): add Indonesian language option (#4287) | 其他(8), 前端页面(1), 后端 API 路由(1) |
| 129 | `fc5e6af` | 🔴 跳过-冲突 | P1 | fix(QA agent): bundle docs as package_data (#4280) | 其他(9), 脚本/部署(5), 测试/CI(1), 配置/常量(1) |

## 前端 API/types（4）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 6 | `2709e95` | 🔴 跳过-冲突 | P1 | feat(WeCom): add share_session_in_group toggle for group chats (#3948) | 前端 API/types(1), 前端页面(1), 后端渠道实现(1), 配置/常量(1) |
| 20 | `5c49769` | 🔴 跳过-冲突 | P1 | fix(skill):  resilient loading for migrated or malformed skill & skill pool entries (#4016) | 前端 API/types(1), 其他(1), 技能系统(1), 后端 API 路由(1) |
| 33 | `4ee41a8` | 🔴 跳过-冲突 | P1 | fix(chat): remove redundant URL prefix stripping in file preview paths (#4089) | 前端 API/types(1), 前端页面(1), 后端 API 路由(1) |
| 124 | `83828a8` | 🔴 跳过-冲突 | P1 | feat(telegram): add streaming output via editMessageText (#4318) | 前端 API/types(1), 前端页面(1), 后端渠道实现(1), 配置/常量(1) |

## 前端国际化（13）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 11 | `d85181a` | 🔴 跳过-冲突 | P1 | feat(chat): generate session titles asynchronously via LLM (#3829) | 前端国际化(4), 测试/CI(3), 前端页面(2), Agent 核心/执行(2) |
| 19 | `bc5a81e` | 🟠 待人工 | P1 | feat(i18n): add Brazilian Portuguese (pt-BR) locale support (#4009) | 前端国际化(2), 文档/发布(2), 前端组件(1) |
| 29 | `6773901` | 🔴 跳过-冲突 | P1 | feat(chat): replace Web Speech API with Whisper transcription for voice input (#3574) | 前端国际化(5), 前端页面(2), 前端 API/types(1), 后端 API 路由(1) |
| 37 | `5edeef4` | 🔴 跳过-冲突 | P1 | feat(console): Add "Enable" and "Disable" buttons to the batch operation of skills (#4091) | 前端国际化(5), 前端页面(3), 前端 API/types(1), 后端 API 路由(1) |
| 44 | `411603e` | 🔴 跳过-冲突 | P1 | feat(cron): add channel-based session isolation for session and share option for cron jobs (#4117) | 前端国际化(4), Agent 核心/执行(4), 前端页面(3), 其他(3) |
| 64 | `c6019fb` | 🔴 跳过-冲突 | P1 | feat(provider): allow Dashscope base URL selection in Console UI (#4074) | 前端国际化(5), 模型 Provider(3), 前端 API/types(1), 前端页面(1) |
| 93 | `aa4961c` | 🟡 裁剪合入 | P0 | feat(chat): refactor chat model selector into searchable flat list with provider grouping (#3876) | 前端国际化(4), 前端页面(2) |
| 96 | `aabfd6a` | 🔴 跳过-冲突 | P1 | feat(plugins): support install/uninstall plugins on console (#4214) | 前端国际化(5), 插件(4), 其他(3), 前端布局(3) |
| 97 | `b6611fd` | 🔴 跳过-冲突 | P1 | feat(feishu): add QR code bot creation via OAuth Device Flow (#4236) | 前端国际化(5), 测试/CI(2), 前端页面(1), 后端渠道实现(1) |
| 98 | `c1ce3db` | 🔴 跳过-冲突 | P1 | feat(memory): add ADBPG long-term memory with BaseMemoryManager architure (#2308) | 前端国际化(5), 记忆系统(4), 前端页面(3), 文档/发布(2) |
| 106 | `475fe26` | 🔴 跳过-冲突 | P1 | feat(mcp): add OAuth 2.1 PKCE support for remote MCP servers (#4256) | 前端国际化(6), 前端页面(6), 后端 API 路由(3), 前端 API/types(2) |
| 109 | `dc2ce24` | 🔴 跳过-冲突 | P1 | feat(channel): add streaming output hooks to BaseChannel with WeCom support (#4271) | 前端国际化(5), 后端渠道实现(2), 前端 API/types(1), 前端页面(1) |
| 126 | `f18a3c2` | 🟡 裁剪合入 | P2 | style(console): inbox page (#4358) | 前端国际化(5), 前端页面(4), 前端布局(2) |

## 前端布局（3）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 87 | `afeea11` | ✅ 直接合入 | P1 | feat(console): Chat floating in the menu (#4240) | 前端布局(2) |
| 94 | `63cea54` | ✅ 直接合入 | P0 | fix(console): collapse sidebar on mobile (#4225) | 前端布局(2) |
| 108 | `af50cf7` | ⚪ 跳过-无关 | P3 | style: sidebar (#4273) | 前端布局(1) |

## 前端组件（3）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 14 | `b458910` | ✅ 直接合入 | P0 | perf(console): Solve duplicate rendering (#4052) | 前端组件(1) |
| 62 | `2b9564d` | 🟠 待人工 | P1 | feat(console): support mermaid graph (#4146) | 前端组件(5), 其他(2), 前端页面(1) |
| 74 | `cc57579` | ✅ 直接合入 | P0 | fix(console): improve text contrast in Plan Panel dark mode (#4190) | 前端组件(2) |

## 前端页面（18）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 31 | `e393bc1` | 🔴 跳过-冲突 | P1 | feat(token-usage): add token suage detailed api and trending charts (#4080) | 前端页面(11), 前端国际化(4), 前端 API/types(2), 后端 API 路由(1) |
| 35 | `50c8712` | 🟠 待人工 | P2 | refactor(console): adjust and opt TokenUsage page (#4094) | 前端页面(8) |
| 43 | `3673176` | 🔴 跳过-冲突 | P1 | feat(security): add rule level auto deny (#4046) | 前端页面(5), 前端国际化(4), 其他(3), 前端 API/types(1) |
| 46 | `c832082` | 🟠 待人工 | P1 | perf(console,chat): chat performance optimization (#4110) | 前端页面(3) |
| 54 | `804cb82` | ✅ 直接合入 | P0 | perf(console): skip chat history lookup for non-arrow keys (#4130) | 前端页面(1) |
| 66 | `cf18e6c` | ✅ 直接合入 | P0 | fix(console): Immediately stop polling and clear the status after closing the drawer. (#4148) | 前端页面(1) |
| 67 | `c3b56c0` | ✅ 直接合入 | P0 | fix(agent-config): preserve complete config on save to prevent nested config loss (#4157) | 前端页面(1) |
| 68 | `6a7b39d` | 🟠 待人工 | P2 | refactor(console): extract QrcodeAuthBlock component and fix polling leak on drawer close (#4153) | 前端页面(3) |
| 79 | `e16a5dd` | ✅ 直接合入 | P0 | Fix(session): session history disappearing and messages being routed to a different session (#4203) | 前端页面(1) |
| 80 | `d361099` | 🔴 跳过-冲突 | P1 | feat(tool): Add async execution support for delegate_external_agent (#4197) | 前端页面(1), Agent 核心/执行(1), 工具实现(1) |
| 81 | `e455388` | ✅ 直接合入 | P1 | feat(chat): enable multiple attachments support in chat page (#4206) | 前端页面(1) |
| 84 | `6ab6979` | ✅ 直接合入 | P1 | feat(console): user message support newline (#4231) | 前端页面(1) |
| 104 | `cb8a8d7` | ✅ 直接合入 | P1 | feat(console): support crosses year in TokenUsage (#4268) | 前端页面(3) |
| 105 | `5dfe1ca` | 🟠 待人工 | P2 | refactor(console): console/PluginManager (#4266) | 前端页面(7) |
| 107 | `207c278` | ✅ 直接合入 | P0 | fix(console): replace window.open calls with openExternalLink utility in ACPDrawer and ChannelDrawer components (#4270) | 前端页面(2), 其他(1) |
| 114 | `9f49c91` | 🔴 跳过-冲突 | P1 | feat(cron & inbox): add inbox and optimize the cron job (#4210) | 前端页面(27), 其他(14), 文档/发布(11), 前端 API/types(5) |
| 116 | `c937ffb` | 🟠 待人工 | P2 | refactor(console): Inbox (#4305) | 前端页面(4) |
| 125 | `d8ac7f6` | 🔴 跳过-冲突 | P1 | fix(skill): fix skill hub import: fix www, add skill_hub retry (#4359) | 前端页面(1), 技能系统(1) |

## 后端 API 路由（3）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 45 | `45afb7c` | 🔴 跳过-冲突 | P1 | feat: add agent status endpoint with task tracking (#4107) | 后端 API 路由(3), Agent 核心/执行(1) |
| 61 | `26a9344` | 🔴 跳过-冲突 | P1 | feat(settings): add pt-BR language support (#4143) | 后端 API 路由(1), 测试/CI(1) |
| 85 | `44ffdb8` | 🔴 跳过-冲突 | P1 | perf(api): optimize async depends to fix thread pool blocking (#4229) | 后端 API 路由(2) |

## 后端渠道实现（15）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 2 | `518ce42` | 🔴 跳过-冲突 | P1 | feat(feishu): introduce FeishuCardHandler and upgrade tool_guard approval to interactive buttons (#3941) | 后端渠道实现(3) |
| 3 | `d9526bf` | 🔴 跳过-冲突 | P1 | fix(WeCom): keep placeholder stream alive to prevent stuck "Thinking..."  (#3950) | 后端渠道实现(1) |
| 5 | `90cf5ac` | 🔴 跳过-冲突 | P1 | fix(WeCom): avoid double reconnect race and cross-loop disconnect (#3963) | 后端渠道实现(1), 测试/CI(1) |
| 18 | `e43731e` | 🔴 跳过-冲突 | P1 | fix(telegram): telegram network retry (#4039) | 后端渠道实现(1) |
| 27 | `769230d` | 🔴 跳过-冲突 | P1 | fix(console): avoid SSE crash on malformed surrogate text (#3553) | 后端渠道实现(3), 测试/CI(2) |
| 34 | `182528e` | 🔴 跳过-冲突 | P2 | refactor(wechat): centralize legacy weixin to wechat data migrations on workspace startup (#3605) | 后端渠道实现(10), 其他(6), 文档/发布(6), 前端国际化(5) |
| 41 | `e6e0dcd` | 🔴 跳过-冲突 | P1 | fix(WeChat): flush WeChat merge buffer immediately for cron sends (#4106) | 后端渠道实现(1) |
| 58 | `90a145d` | 🔴 跳过-冲突 | P1 | fix(channels): keep markdown tables renderable across split_text chunks (#4119) | 后端渠道实现(1) |
| 63 | `8b8ddba` | 🔴 跳过-冲突 | P1 | feat(WeCom): tool-guard interactive approval card (#4112) | 后端渠道实现(5) |
| 75 | `eb01c83` | 🔴 跳过-冲突 | P1 | fix(provider,wecom): preserve provider meta field and update tool_guard docstring in wecom (#4200) | 后端渠道实现(1), 模型 Provider(1) |
| 82 | `43ca356` | 🔴 跳过-冲突 | P1 | feat(DingTalk): process quoted messages for user-sent replies (#4209) | 后端渠道实现(1) |
| 89 | `b1ff519` | 🔴 跳过-冲突 | P1 | fix(feishu): detect silent WebSocket connection loss in Feishu channel (#4241) | 后端渠道实现(2) |
| 91 | `61475f2` | 🔴 跳过-冲突 | P1 | feat(channels): support native voice bubble in Feishu channel (#4202) | 后端渠道实现(1) |
| 92 | `64e5de9` | 🔴 跳过-冲突 | P1 | fix(WeCom): show operator in resolved approval card (#4233) | 后端渠道实现(1) |
| 118 | `fc6be99` | 🔴 跳过-冲突 | P1 | feat(WeCom): support tool_guard interactive card in streaming path (#4307) | 后端渠道实现(3) |

## 工具实现（7）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 65 | `c46996b` | 🔴 跳过-冲突 | P1 | fix(agent-tools): add safe default timeout for delegate_external_agent (#3928) | 工具实现(1) |
| 77 | `b8c33a1` | 🔴 跳过-冲突 | P1 | feat(tool): browser_use add batch action support to browser_use tool (#4139) | 工具实现(1) |
| 110 | `b1770de` | 🔴 跳过-冲突 | P1 | Fix(tool): read_file_safe allocation size (#4272) | 工具实现(2) |
| 111 | `503390d` | 🔴 跳过-冲突 | P1 | perf(tools): reduce maximum file read size to 200MB (#4276) | 工具实现(2) |
| 113 | `67cb469` | 🔴 跳过-冲突 | P1 | Feat(tool): Add action="file_download" for browser use (#4261) | 工具实现(1) |
| 122 | `a49dc9e` | 🔴 跳过-冲突 | P1 | fix(tool): browser implement activity tracking, crash monitoring, and lifecycle management (#4306) | 工具实现(1), 其他(1) |
| 130 | `00ede85` | 🔴 跳过-冲突 | P1 | fix(tool): add _CDP_CONNECT_TIMEOUT_SECONDS = 30 for connect cdp (#4350) | 工具实现(1) |

## 技能系统（2）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 39 | `d6dbf31` | 🔴 跳过-冲突 | P1 | feat(skills): add cli skill test command (#3999) | 技能系统(1) |
| 127 | `11f2136` | 🔴 跳过-冲突 | P1 | fix(skill): fix skill path, use safer path normalizer and refactor for function naming (#4335) | 技能系统(5), 其他(1), 后端 API 路由(1) |

## 插件（5）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 36 | `3213fd1` | 🔴 跳过-冲突 | P1 | plugin: add gpt-image-2 tool plugin (#3911) | 插件(8), 前端国际化(4), 其他(3), 前端页面(3) |
| 76 | `60a555b` | 🔴 跳过-冲突 | P1 | feat(plugins): add reference image support to gpt-image2 plugin (#4194) | 插件(5), 前端页面(1), 后端 API 路由(1), 配置/常量(1) |
| 101 | `7e82329` | 🔴 跳过-冲突 | P1 | feat(plugins): add Qwen-Image and Wan 2.7 plugins (#4248) | 插件(17), 前端页面(2), 后端 API 路由(1) |
| 102 | `a82ce8d` | 🔴 跳过-冲突 | P1 | feat(plugins): enable register FastAPI APIRouter instances through plugin (#4255) | 插件(2), 文档/发布(2), 其他(1) |
| 128 | `799017e` | 🟠 待人工 | P1 | feat(plugin): add CloudPaw plugin bundle for Alibaba Cloud deployment (#4362) | 插件(101) |

## 文档/发布（7）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 8 | `9b7acb3` | 🔴 跳过-冲突 | P1 | feat(feishu): hint docs link on approval card when card.action.trigger is unsubscribed (#3982) | 文档/发布(2), 后端渠道实现(1) |
| 10 | `d783c3b` | ⚪ 跳过-无关 | P3 | docs(website): update documentation to v1.1.5 (#4013) | 文档/发布(13) |
| 22 | `30dc625` | ⚪ 跳过-无关 | P3 | docs(faq): Docs for handling APITimeoutError when running in WSL2 (NAT mode) (#4005) | 文档/发布(2) |
| 23 | `678cc42` | 🔴 跳过-冲突 | P1 | feat(skill): Add skill install/uninstall cli (#4053) | 文档/发布(4), 技能系统(2) |
| 71 | `8cc10d2` | 🔴 跳过-冲突 | P3 | chore(release): update release note of v1.1.6 (#4163) | 文档/发布(7), 配置/常量(1) |
| 88 | `47db242` | 🔴 跳过-冲突 | P1 | feat(shell): Add shell_command_executable` configuration to let users choose which shell uses (#4215) | 文档/发布(6), 前端国际化(5), Agent 核心/执行(3), 前端页面(2) |
| 119 | `8e2a835` | 🔴 跳过-冲突 | P3 | chore(version): add release note for v1.1.7 (#4319) | 文档/发布(7), 配置/常量(1) |

## 模型 Provider（7）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 13 | `694d317` | 🔴 跳过-冲突 | P1 | fix(provider): increase max_token for anthropic compatible models (#4054) | 模型 Provider(4) |
| 30 | `166dc49` | 🔴 跳过-冲突 | P1 | Feat(provider): add volcengine provider (#3994) | 模型 Provider(2), 前端页面(1) |
| 52 | `8a6d2dc` | 🔴 跳过-冲突 | P1 | feat(provider): add aliyun token plan as a built-in provider (#4122) | 模型 Provider(4), 前端页面(2) |
| 55 | `ec8aad8` | 🔴 跳过-冲突 | P1 | fix(tool_schema): add sanitize tool function schemas (#4126) | 模型 Provider(1) |
| 72 | `53cd8b1` | 🔴 跳过-冲突 | P1 | Fix(provider): fix models in VOLCENGINE Provider (#4169) | 模型 Provider(2) |
| 86 | `c89ed13` | 🔴 跳过-冲突 | P1 | fix(model): filter out malformed tool_use blocks from OpenAI-compatible model responses (#4234) | 模型 Provider(1) |
| 117 | `7a0b62f` | 🔴 跳过-冲突 | P1 | Fix(Provider): Fix anthropic provider max token handling (#4317) | 模型 Provider(2) |

## 测试/CI（1）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 26 | `73e03e2` | ⚪ 跳过-无关 | P3 | test(integration): add app startup and settings/envs smoke tests (#4081) | 测试/CI(3) |

## 脚本/部署（3）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 38 | `67ff5aa` | ✅ 直接合入 | P0 | fix(pack): restore conda packaging tools before conda-pack (#4093) | 脚本/部署(1) |
| 42 | `9fdb426` | 🔴 跳过-冲突 | P3 | chore: fix openai version (#4118) | 脚本/部署(1) |
| 112 | `af65842` | 🔴 跳过-冲突 | P1 | fix(QA agent): package website/public/docs into wheel and sdist (#4275) | 脚本/部署(1) |

## 记忆系统（1）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 78 | `abd8066` | 🔴 跳过-冲突 | P1 | feat(memory): add auto-memory management features (#4204) | 记忆系统(3) |

## 配置/常量（8）

| # | SHA | 标签 | 优先级 | 标题 | 触达范围 |
|---:|---|---|---|---|---|
| 1 | `8aa5f27` | 🔴 跳过-冲突 | P3 | chore(version): bump version to 1.1.5.post1 (#3970) | 配置/常量(1) |
| 9 | `6368ca3` | 🔴 跳过-冲突 | P3 | chore(version): bumping version to 1.1.6b1 (#4012) | 配置/常量(1) |
| 24 | `24c0610` | 🔴 跳过-冲突 | P3 | chore(version): bumping version to 1.1.5p2 (#4071) | 配置/常量(1) |
| 25 | `18d7c15` | 🔴 跳过-冲突 | P3 | chore(version): bump version to 1.1.6b1 (#4082) | 配置/常量(1) |
| 70 | `047afe5` | 🔴 跳过-冲突 | P3 | chore(version): bumping version to 1.1.6b2 (#4161) | 配置/常量(1) |
| 73 | `95908ac` | 🔴 跳过-冲突 | P3 | chore(version): bumping version to 1.1.7b1 (#4196) | 配置/常量(1) |
| 115 | `f684c13` | 🔴 跳过-冲突 | P3 | bumping version to 1.1.7b2 (#4283) | 配置/常量(1) |
| 120 | `f2e8b7f` | 🔴 跳过-冲突 | P3 | chore(version): bumping version to 1.1.8b1 (#4346) | 配置/常量(1) |

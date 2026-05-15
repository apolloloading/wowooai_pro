# 逐 commit 代码影响分析（第 4 批）

> 范围：第 76 - 100 条。此文档基于 diff 提取，重点回答“commit 了什么、影响哪里”。

## [76] `60a555b` feat(plugins): add reference image support to gpt-image2 plugin (#4194)

- **完整 SHA**：`60a555b0a574a51179605ee705dc4158460ba6b0`
- **日期/作者**：`2026-05-11` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`8 文件`，`+629/-88`
- **实际影响范围**：
  - 影响插件安装、注册、工具插件或云部署插件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Agent/Tools/index.tsx` | +8/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `plugins/tool/gpt-image2/README.md` | +54/-9 | 插件 | 修改文件；文档或提示词文本调整 |
  | `plugins/tool/gpt-image2/plugin.json` | +71/-33 | 插件 | 修改文件；新增配置/字段："version": "1.1.0",；"description": "Generate and edit images using OpenAI GPT Image 2 model",；"tools": [；"name": "generate_image_gpt", |
  | `plugins/tool/gpt-image2/plugin.py` | +60/-34 | 插件 | 修改文件；新增配置/字段："name": "generate_image_gpt",；"description": (；"icon": "🎨",；"name": "edit_image_gpt", |
  | `plugins/tool/gpt-image2/tool.py` | +339/-3 | 插件 | 修改文件；新增/修改符号：async def edit_image_gpt(  # pylint: disable=too-many-statements；def _process_image_url(image_path: str) -> dict:；def _get_tool_config(tool_name: str = "generate_image_gpt") -> Optional[dict]:；新增配置/字段：prompt: str,；reference_images: List[str],；size: str = "1024x1024",；quality: str = "auto", |
  | `src/qwenpaw/app/routers/tools.py` | +67/-8 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/config/config.py` | +20/-0 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/plugins/registry.py` | +10/-0 | 插件 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [77] `b8c33a1` feat(tool): browser_use add batch action support to browser_use tool (#4139)

- **完整 SHA**：`b8c33a123048e27c758f96ba9be71dca02c7a13f`
- **日期/作者**：`2026-05-11` / `weixizi`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+276/-1`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/browser_control.py` | +276/-1 | 工具实现 | 修改文件；新增/修改符号：async def _action_batch(  # pylint: disable=too-many-nested-blocks；新增配置/字段：state: dict,；page_id: str,；actions_json: str,；"ok": False, |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [78] `abd8066` feat(memory): add auto-memory management features (#4204)

- **完整 SHA**：`abd80665ac0a9411ea842301e4329f4b6b194d22`
- **日期/作者**：`2026-05-11` / `jinliyl`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+132/-37`
- **实际影响范围**：
  - 影响记忆管理、自动记忆或长期记忆配置
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/context/light_context_manager.py` | +12/-37 | 记忆系统 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/memory/base_memory_manager.py` | +52/-0 | 记忆系统 | 修改文件；新增/修改符号：async def auto_memory_search(；async def summarize_when_compact(；async def auto_memory(；新增配置/字段：messages: list[Msg] \| Msg,；agent_name: str = "",；Args:；messages: The incoming user message(s). |
  | `src/qwenpaw/agents/memory/reme_light_memory_manager.py` | +68/-0 | 记忆系统 | 修改文件；新增/修改符号：async def auto_memory_search(；async def summarize_when_compact(；async def auto_memory(；新增配置/字段：messages: list[Msg] \| Msg,；agent_name: str = "",；messages: list[Msg],；all_messages: list[Msg], |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [79] `e16a5dd` Fix(session): session history disappearing and messages being routed to a different session (#4203)

- **完整 SHA**：`e16a5dd5f3b0558986d6d9c4be5c3b003a05b154`
- **日期/作者**：`2026-05-11` / `zhaozhuang521`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+92/-76`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Chat/sessionApi/index.ts` | +92/-76 | 前端页面 | 修改文件；新增/修改符号：const matchedExistingIds = new Set<string>();；const sExt = s as ExtendedSession;；const eExt = e as ExtendedSession;；const chatHistory = await api.getChat(backendId);；新增配置/字段：displayId: string,；backendId: string,；listEntry: ExtendedSession \| undefined,；id: displayId, |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [80] `d361099` feat(tool): Add async execution support for delegate_external_agent (#4197)

- **完整 SHA**：`d361099d8aed7364901dcd6f894182340f247cd3`
- **日期/作者**：`2026-05-11` / `x1n95c`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+531/-108`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Agent/Tools/index.tsx` | +4/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/react_agent.py` | +9/-6 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/agents/tools/delegate_external_agent.py` | +518/-101 | 工具实现 | 修改文件；新增/修改符号：class _RunnerState:；def _current_agent_id() -> str:；def _task_key(；def _format_timestamp(value: float) -> str:；新增配置/字段：agent_id: str；chat_id: str；runner: str；action: str |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [81] `e455388` feat(chat): enable multiple attachments support in chat page (#4206)

- **完整 SHA**：`e4553884d75285eeecd52d2f7bf6aeebc46e06f6`
- **日期/作者**：`2026-05-11` / `zhijianma`
- **标签/优先级**：`✅ 直接合入` / `P1`
- **总体规模**：`1 文件`，`+1/-0`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Chat/index.tsx` | +1/-0 | 前端页面 | 修改文件 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [82] `43ca356` feat(DingTalk): process quoted messages for user-sent replies (#4209)

- **完整 SHA**：`43ca356042ebc6b940657b3fe90be98d618a0881`
- **日期/作者**：`2026-05-11` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+193/-0`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/dingtalk/handler.py` | +193/-0 | 后端渠道实现 | 修改文件；新增/修改符号：def _handle_quoted_media(；def _handle_quoted_rich_text(；def _process_quoted_message(；新增配置/字段：replied_content: Any,；replied_msg_type: str,；robot_code: str,；text_parts: List[str], |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [83] `fe13fe2` fix(exception): fix ConfigurationException key passing (#4212)

- **完整 SHA**：`fe13fe230dd3b6a9f2a247f0b4b002e622b37b18`
- **日期/作者**：`2026-05-11` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+20/-2`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
  - 影响定时任务、收件箱、消息推送或 session 隔离
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/skills_hub.py` | +15/-2 | 技能系统 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/crons/manager.py` | +1/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/crons/models.py` | +3/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/session.py` | +1/-0 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [84] `6ab6979` feat(console): user message support newline (#4231)

- **完整 SHA**：`6ab6979de60787b538b488188e8a87f812fcd579`
- **日期/作者**：`2026-05-12` / `zhaozhuang521`
- **标签/优先级**：`✅ 直接合入` / `P1`
- **总体规模**：`1 文件`，`+10/-0`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Chat/index.module.less` | +10/-0 | 前端页面 | 修改文件；样式/布局调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [85] `44ffdb8` perf(api): optimize async depends to fix thread pool blocking (#4229)

- **完整 SHA**：`44ffdb8644d170d097e5d89f12bba9f0952637ac`
- **日期/作者**：`2026-05-12` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+4/-7`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/routers/local_models.py` | +2/-2 | 后端 API 路由 | 修改文件；新增/修改符号：async def get_local_model_manager(request: Request) -> LocalModelManager:；async def get_provider_manager(request: Request) -> ProviderManager: |
  | `src/qwenpaw/app/routers/providers.py` | +2/-5 | 后端 API 路由 | 修改文件；新增/修改符号：async def get_provider_manager(request: Request) -> ProviderManager: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [86] `c89ed13` fix(model): filter out malformed tool_use blocks from OpenAI-compatible model responses (#4234)

- **完整 SHA**：`c89ed132e79f68f390812668475d0da9368a3bd5`
- **日期/作者**：`2026-05-12` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+13/-1`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/providers/openai_chat_model_compat.py` | +13/-1 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [87] `afeea11` feat(console): Chat floating in the menu (#4240)

- **完整 SHA**：`afeea118f3f045c2ac9e93a3f182a99f8a91483c`
- **日期/作者**：`2026-05-12` / `zhaozhuang521`
- **标签/优先级**：`✅ 直接合入` / `P1`
- **总体规模**：`2 文件`，`+61/-6`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/layouts/Sidebar.tsx` | +12/-5 | 前端布局 | 修改文件；逻辑 hunk 调整 |
  | `console/src/layouts/index.module.less` | +49/-1 | 前端布局 | 修改文件；新增配置/字段：background: #f9f7f3;；display: flex;；gap: 10px;；width: 100%; |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [88] `47db242` feat(shell): Add shell_command_executable` configuration to let users choose which shell uses (#4215)

- **完整 SHA**：`47db242c43fd8f6a38e02153bbc272687a1609f8`
- **日期/作者**：`2026-05-12` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`20 文件`，`+189/-25`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `README.md` | +0/-1 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_ja.md` | +0/-2 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_ru.md` | +0/-2 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_zh.md` | +0/-2 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `console/src/api/types/agent.ts` | +1/-0 | 前端 API/types | 修改文件 |
  | `console/src/locales/en.json` | +3/-0 | 前端国际化 | 修改文件；新增文案 key："shellCommandExecutable": "Shell Executable",；"shellCommandExecutableTooltip": "Path to the shell used by execute_shell_command. Linux/macOS: e.g. /bin/bash, /bin/zsh；"shellCommandExecutablePlaceholder": "e.g. /bin/bash or powershell.exe (empty = auto-detect)", |
  | `console/src/locales/ja.json` | +3/-0 | 前端国际化 | 修改文件；新增文案 key："shellCommandExecutable": "Shell実行ファイル",；"shellCommandExecutableTooltip": "execute_shell_commandが使用するシェルのパス。Linux/macOS: /bin/bash、/bin/zshなど。Windows: powershell；"shellCommandExecutablePlaceholder": "例: /bin/bash または powershell.exe（空 = 自動検出）", |
  | `console/src/locales/pt-BR.json` | +3/-0 | 前端国际化 | 修改文件；新增文案 key："shellCommandExecutable": "Shell Executável",；"shellCommandExecutableTooltip": "Caminho para o shell usado pelo execute_shell_command. Linux/macOS: ex. /bin/bash, /bi；"shellCommandExecutablePlaceholder": "ex.: /bin/bash ou powershell.exe (vazio = detecção automática)", |
  | `console/src/locales/ru.json` | +3/-0 | 前端国际化 | 修改文件；新增文案 key："shellCommandExecutable": "Исполняемый файл shell",；"shellCommandExecutableTooltip": "Путь к shell, используемому execute_shell_command. Linux/macOS: например, /bin/bash, /；"shellCommandExecutablePlaceholder": "напр. /bin/bash или powershell.exe (пусто = автоопределение)", |
  | `console/src/locales/zh.json` | +3/-0 | 前端国际化 | 修改文件；新增文案 key："shellCommandExecutable": "Shell 可执行程序",；"shellCommandExecutableTooltip": "execute_shell_command 使用的 shell 路径。Linux/macOS：如 /bin/bash、/bin/zsh。Windows：支持 powersh；"shellCommandExecutablePlaceholder": "例如 /bin/bash 或 powershell.exe（留空 = 自动检测）", |
  | `console/src/pages/Agent/Config/components/ReactAgentCard.tsx` | +14/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Agent/Config/useAgentConfig.tsx` | +1/-0 | 前端页面 | 修改文件 |
  | `src/qwenpaw/agents/react_agent.py` | +4/-0 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/tools/shell.py` | +83/-5 | 工具实现 | 修改文件；新增/修改符号：def _shell_basename(executable: str) -> str:；def _is_powershell(executable: str) -> bool:；def _is_cmd(executable: str) -> bool:；def _extract_powershell_command(cmd: str) -> tuple[str \| None, str]:；新增配置/字段：shell_executable: str \| None = None,；else:；IMPORTANT: Check the 'Default Shell' field to |
  | `src/qwenpaw/app/runner/runner.py` | +15/-3 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/utils.py` | +7/-0 | Agent 核心/执行 | 修改文件；新增配置/字段：default_shell: Optional[str] = None,；default_shell: Shell executable used by execute_shell_command. |
  | `src/qwenpaw/config/config.py` | +13/-0 | 配置/常量 | 修改文件 |
  | `src/qwenpaw/config/context.py` | +24/-0 | 其他 | 修改文件；新增/修改符号：def get_current_shell_command_executable() -> str \| None:；def set_current_shell_command_executable(executable: str \| None) -> None:；新增配置/字段：current_shell_command_executable: ContextVar[str \| None] = ContextVar(；Returns:；Args:；executable: Path to the shell executable (e.g. "/bin/bash"). |
  | ... |  |  | 另有 2 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语
  - 需排除包名、项目名、发布说明等品牌化内容

---

## [89] `b1ff519` fix(feishu): detect silent WebSocket connection loss in Feishu channel (#4241)

- **完整 SHA**：`b1ff519f676fcb58cc2d355ef8c7141766277ea7`
- **日期/作者**：`2026-05-12` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+34/-0`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/feishu/channel.py` | +30/-0 | 后端渠道实现 | 修改文件；新增/修改符号：async def _patched_handle_message(msg: bytes) -> None: |
  | `src/qwenpaw/app/channels/feishu/constants.py` | +4/-0 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [90] `ec4e7d8` Refactor(skill): Add skill system (#4235)

- **完整 SHA**：`ec4e7d87918aec5f38cce4b795f1d47b280f2e97`
- **日期/作者**：`2026-05-12` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P2`
- **总体规模**：`26 文件`，`+5558/-5388`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
  - 删除代码/资源，需确认我方没有依赖
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/__init__.py` | +1/-1 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/react_agent.py` | +1/-1 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/skill_system/__init__.py` | +40/-0 | 技能系统 | 新增文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/skill_system/hub.py` | +1708/-0 | 技能系统 | 新增文件；新增/修改符号：def _build_hub_conflict(name: str) -> dict[str, Any]:；class HubSkillResult:；class HubInstallResult:；class SkillImportCancelled(RuntimeError):；新增配置/字段："reason": "conflict",；"skill_name": name,；"suggested_name": suggest_conflict_name(name),；"conflicts": [conflict], |
  | `src/qwenpaw/agents/skill_system/models.py` | +76/-0 | 技能系统 | 新增文件；新增/修改符号：class BuiltinSkillVariant:；class BuiltinSkillIdentity:；class SkillInfo(BaseModel):；class SkillRequirements(BaseModel):；新增配置/字段：name: str；language: str；source_name: str；skill_dir: Path |
  | `src/qwenpaw/agents/skill_system/pool_service.py` | +830/-0 | 技能系统 | 新增文件；新增/修改符号：class SkillPoolService:；def __init__(self):；def list_all_skills(self) -> list[SkillInfo]:；def create_skill(；新增配置/字段：Example:；skills: list[SkillInfo] = []；name: str,；content: str, |
  | `src/qwenpaw/agents/skill_system/registry.py` | +1384/-0 | 技能系统 | 新增文件；新增/修改符号：def _normalize_builtin_skill_language(；def get_builtin_skill_language_preference() -> str:；def set_builtin_skill_language_preference(language: str) -> None:；def _parse_builtin_skill_identity(；新增配置/字段：_ACTIVE_SKILL_ENV_ENTRIES: dict[str, dict[str, Any]] = {}；_builtin_cache: dict[str, Any] = {}；language: str \| None,；fallback: str = "en", |
  | `src/qwenpaw/agents/skill_system/store.py` | +797/-0 | 技能系统 | 新增文件；新增/修改符号：def _read_frontmatter_safe_from_path(；def get_skill_pool_dir() -> Path:；def get_workspace_skills_dir(workspace_dir: Path) -> Path:；def get_workspace_skill_manifest_path(workspace_dir: Path) -> Path:；新增配置/字段：try:；try:；skill_md_path: Path,；skill_name: str = "", |
  | `src/qwenpaw/agents/skill_system/workspace_service.py` | +681/-0 | 技能系统 | 新增文件；新增/修改符号：class SkillService:；def __init__(self, workspace_dir: Path):；def _read_manifest(self) -> dict[str, Any]:；def list_all_skills(self) -> list[SkillInfo]:；新增配置/字段：Example:；skills: list[SkillInfo] = []；skills: list[SkillInfo] = []；name: str, |
  | `src/qwenpaw/agents/skills/QA_source_index-en/SKILL.md` | +1/-1 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/skills/QA_source_index-zh/SKILL.md` | +1/-1 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/skills_hub.py` | +0/-1710 | 技能系统 | 删除文件；移除符号：def _build_hub_conflict(name: str) -> dict[str, Any]:；class HubSkillResult:；class HubInstallResult: |
  | `src/qwenpaw/agents/skills_manager.py` | +0/-3640 | 技能系统 | 删除文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/migration.py` | +3/-3 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/agents.py` | +1/-1 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/settings.py` | +3/-1 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/skills.py` | +16/-12 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/control_commands/skills_handler.py` | +1/-1 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | ... |  |  | 另有 8 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [91] `61475f2` feat(channels): support native voice bubble in Feishu channel (#4202)

- **完整 SHA**：`61475f26dfa0a084686532fc01132c5d3889a68f`
- **日期/作者**：`2026-05-12` / `StarTrekking`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+5/-1`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/feishu/channel.py` | +5/-1 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [92] `64e5de9` fix(WeCom): show operator in resolved approval card (#4233)

- **完整 SHA**：`64e5de99335b1f96dd28a6d91811e81db3f0ec9f`
- **日期/作者**：`2026-05-12` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+5/-5`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wecom/cards/tool_guard.py` | +5/-5 | 后端渠道实现 | 修改文件；新增配置/字段："title": _truncate(title, 36),；"desc": _truncate(desc, 44), |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [93] `aa4961c` feat(chat): refactor chat model selector into searchable flat list with provider grouping (#3876)

- **完整 SHA**：`aa4961c0c25be3fa74cc0672a581dac30055fd5c`
- **日期/作者**：`2026-05-12` / `Bowen Liang`
- **标签/优先级**：`🟡 裁剪合入` / `P0`
- **总体规模**：`6 文件`，`+276/-145`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
  - 影响多语言文案，需要校验中文“数字员工”等术语
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/locales/en.json` | +5/-1 | 前端国际化 | 修改文件；新增文案 key："switchFailed": "Failed to switch model",；"searchModels": "Search models...",；"noModelsFound": "No matching models found",；"free": "Free",；"vision": "Vision" |
  | `console/src/locales/ja.json` | +5/-1 | 前端国际化 | 修改文件；新增文案 key："switchFailed": "モデルの切り替えに失敗しました",；"searchModels": "モデルを検索...",；"noModelsFound": "一致するモデルが見つかりません",；"free": "無料",；"vision": "視覚" |
  | `console/src/locales/ru.json` | +5/-1 | 前端国际化 | 修改文件；新增文案 key："switchFailed": "Не удалось переключить модель",；"searchModels": "Поиск моделей...",；"noModelsFound": "Подходящие модели не найдены",；"free": "Бесплатно",；"vision": "Видение" |
  | `console/src/locales/zh.json` | +5/-1 | 前端国际化 | 修改文件；新增文案 key："switchFailed": "切换模型失败",；"searchModels": "搜索模型...",；"noModelsFound": "未找到匹配的模型",；"free": "免费",；"vision": "视觉" |
  | `console/src/pages/Chat/ModelSelector/index.module.less` | +152/-91 | 前端页面 | 修改文件；新增配置/字段：width: 360px;；display: flex;；overflow: hidden;；gap: 8px; |
  | `console/src/pages/Chat/ModelSelector/index.tsx` | +104/-50 | 前端页面 | 修改文件；新增/修改符号：const searchInputRef = useRef<HTMLInputElement>(null);；const trimmedSearch = searchQuery.trim();；const filteredProviders = (() => {；const query = trimmedSearch.toLowerCase();；新增配置/字段：models: ProviderInfo["models"];；models: p.models.filter( |
- **合入检查点**：
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [94] `63cea54` fix(console): collapse sidebar on mobile (#4225)

- **完整 SHA**：`63cea5470fc15d28309f44420fc49af9146b4af9`
- **日期/作者**：`2026-05-12` / `Aqil Aziz`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`2 文件`，`+73/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/layouts/Sidebar.tsx` | +37/-1 | 前端布局 | 修改文件；新增/修改符号：const MOBILE_SIDEBAR_QUERY = "(max-width: 768px)";；function isMobileSidebarViewport() {；const mediaQuery = window.matchMedia(MOBILE_SIDEBAR_QUERY);；const syncMobileSidebar = () => { |
  | `console/src/layouts/index.module.less` | +36/-0 | 前端布局 | 修改文件；新增配置/字段：height: calc(100vh - 56px);；padding: 0 8px;；flex: 0 0 auto !important;；padding: 0 6px; |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [95] `9bc51ed` feat(console): add Indonesian language option (#4219)

- **完整 SHA**：`9bc51ed1394028a5223814ef4d5154f7b5282c13`
- **日期/作者**：`2026-05-12` / `Aqil Aziz`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`9 文件`，`+565/-4`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/App.tsx` | +4/-0 | 其他 | 修改文件；新增配置/字段：id: idID,；id: "id", |
  | `console/src/components/LanguageSwitcher/LanguageSwitcher.test.tsx` | +12/-1 | 前端组件 | 修改文件；新增/修改符号：const user = userEvent.setup(); |
  | `console/src/components/LanguageSwitcher/index.tsx` | +1/-0 | 前端组件 | 修改文件；逻辑 hunk 调整 |
  | `console/src/constants/timezone.ts` | +2/-1 | 其他 | 修改文件；新增/修改符号：const locale = |
  | `console/src/i18n.ts` | +4/-0 | 前端国际化 | 修改文件；新增配置/字段：id: {；translation: id, |
  | `console/src/locales/id.json` | +539/-0 | 前端国际化 | 新增文件；新增文案 key："common": {；"save": "Simpan",；"reset": "Atur ulang",；"cancel": "Batal",；"confirm": "Konfirmasi", |
  | `console/src/test/icons-mock.ts` | +1/-0 | 其他 | 修改文件；新增/修改符号：export const SparkPtLine = makeIcon("SparkPtLine"); |
  | `src/qwenpaw/app/routers/settings.py` | +1/-1 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/routers/test_settings.py` | +1/-1 | 测试/CI | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [96] `aabfd6a` feat(plugins): support install/uninstall plugins on console (#4214)

- **完整 SHA**：`aabfd6a572503fd89a71b38f8f14f69985142ea7`
- **日期/作者**：`2026-05-12` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`22 文件`，`+2823/-149`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响模型供应商请求参数、模型列表或兼容性
  - 影响插件安装、注册、工具插件或云部署插件
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/package-lock.json` | +100/-0 | 其他 | 修改文件；新增配置/字段："jszip": "^3.10.1",；"version": "1.0.3",；"resolved": "https://registry.npmjs.org/core-util-is/-/core-util-is-1.0.3.tgz",；"integrity": "sha512-ZQBvi1DcpJ4GDqanjucZ2Hj3wEO5pZDS89BWbkcrvdxksJorwUDDZamX9ldFkp9aw2lmBDLgkObEA4DWNJ9FYQ==", |
  | `console/package.json` | +2/-1 | 其他 | 修改文件；新增配置/字段："jszip": "^3.10.1",；"mermaid": "^11.12.2", |
  | `console/src/api/modules/plugin.ts` | +109/-1 | 前端 API/types | 修改文件；新增/修改符号：export type PluginType =；export interface InstallPluginResult {；export interface PluginStatus {；const response = await fetch(getApiUrl("/plugins/install"), {；新增配置/字段：loaded: boolean;；plugin_type: PluginType;；id: string;；name: string; |
  | `console/src/layouts/MainLayout/index.tsx` | +8/-0 | 前端布局 | 修改文件；新增/修改符号：const PluginManagerPage = lazyImportWithRetry( |
  | `console/src/layouts/Sidebar.tsx` | +12/-0 | 前端布局 | 修改文件；新增配置/字段：key: "plugin-manager",；icon: <Package size={18} />,；path: "/plugin-manager",；label: t("nav.pluginManager", "Plugin Manager"), |
  | `console/src/layouts/constants.ts` | +1/-0 | 前端布局 | 修改文件 |
  | `console/src/locales/en.json` | +34/-1 | 前端国际化 | 修改文件；新增文案 key："backups": "Backups",；"pluginManager": "Plugin Manager"；"pluginManager": {；"title": "Plugin Manager",；"description": "Install, manage, and remove plugins without restarting the service.", |
  | `console/src/locales/ja.json` | +34/-1 | 前端国际化 | 修改文件；新增文案 key："backups": "バックアップ",；"pluginManager": "プラグインマネージャー"；"pluginManager": {；"title": "プラグインマネージャー",；"description": "サービスを再起動せずにプラグインのインストール、管理、削除を行います。", |
  | `console/src/locales/pt-BR.json` | +34/-1 | 前端国际化 | 修改文件；新增文案 key："backups": "Backups",；"pluginManager": "Gerenciador de Plugins"；"pluginManager": {；"title": "Gerenciador de Plugins",；"description": "Instalar, gerenciar e remover plugins sem reiniciar o serviço.", |
  | `console/src/locales/ru.json` | +34/-1 | 前端国际化 | 修改文件；新增文案 key："backups": "Резервные копии",；"pluginManager": "Менеджер плагинов"；"pluginManager": {；"title": "Менеджер плагинов",；"description": "Установка, управление и удаление плагинов без перезапуска службы.", |
  | `console/src/locales/zh.json` | +34/-1 | 前端国际化 | 修改文件；新增文案 key："backups": "备份",；"pluginManager": "插件管理"；"pluginManager": {；"title": "插件管理",；"description": "安装、管理和卸载插件，无需重启服务。", |
  | `console/src/pages/Settings/PluginManager/index.module.less` | +110/-0 | 前端页面 | 新增文件；新增配置/字段：height: 100%;；display: flex;；overflow: hidden;；flex: 1; |
  | `console/src/pages/Settings/PluginManager/index.tsx` | +582/-0 | 前端页面 | 新增文件；新增/修改符号：const PLUGIN_TYPE_CONFIG: Record<；function PluginTypeTag({ type }: { type: PluginType }) {；const cfg = PLUGIN_TYPE_CONFIG[type] ?? PLUGIN_TYPE_CONFIG.general;；const result: Array<{ path: string; file: File }> = [];；新增配置/字段：tool: {；label: "Tool",；color: "blue",；icon: <Wrench size={11} />, |
  | `plugins/tool/gpt-image2/plugin.json` | +2/-1 | 插件 | 修改文件；新增配置/字段："type": "tool",；"min_version": "1.1.7", |
  | `src/qwenpaw/app/channels/command_registry.py` | +20/-0 | 后端渠道实现 | 修改文件；新增/修改符号：def unregister_command(self, command_prefix: str) -> bool:；新增配置/字段：Args:；command_prefix: Command prefix to remove (e.g. ``"/mystatus"``).；Returns: |
  | `src/qwenpaw/app/routers/plugins.py` | +784/-43 | 后端 API 路由 | 修改文件；新增/修改符号：def _safe_extract_zip(；def _find_plugin_dir(base: Path) -> Path:；async def _post_load_setup(  # pylint: disable=too-many-branches；def _sync_plugin_tools_to_agents(loader, plugin_id: str) -> None:；新增配置/字段："author": manifest.get("author", ""),；"enabled": True,；"loaded": False,；"plugin_type": disk_manifest.plugin_type, |
  | `src/qwenpaw/app/runner/control_commands/__init__.py` | +26/-0 | Agent 核心/执行 | 修改文件；新增/修改符号：def unregister_command(command_name: str) -> bool:；新增配置/字段：Args:；command_name: Command name to remove (e.g. ``"mystatus"``；Returns: |
  | `src/qwenpaw/cli/plugin_commands.py` | +406/-92 | 其他 | 修改文件；新增/修改符号：def _get_api_base() -> Optional[str]:；def _api_install_plugin(source: str, force: bool = False) -> bool:；def _api_upload_plugin(zip_path: Path, force: bool = False) -> bool:；def _api_uninstall_plugin(plugin_id: str) -> bool:；新增配置/字段：Returns:；Args:；source: Local directory path or HTTP(S) URL of the plugin；force: Unload existing plugin first if already loaded |
  | ... |  |  | 另有 4 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [97] `b6611fd` feat(feishu): add QR code bot creation via OAuth Device Flow (#4236)

- **完整 SHA**：`b6611fd123c473a0df9dd6a0794e022319c29649`
- **日期/作者**：`2026-05-12` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`9 文件`，`+530/-2`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `.github/workflows/channel-tests.yml` | +4/-2 | 测试/CI | 修改文件；逻辑 hunk 调整 |
  | `console/src/locales/en.json` | +7/-0 | 前端国际化 | 修改文件；新增文案 key："feishuScanGuide": "Scan the QR code with Feishu to create a bot instantly. A Feishu app will be created automatically a；"feishuScanLogin": "Scan to Create Bot",；"feishuGetQrcode": "Get Feishu QR Code",；"feishuScanHint": "Scan the QR code above with Feishu. App ID and App Secret will be filled in automatically after autho；"feishuAuthSuccess": "Feishu bot created. App ID and App Secret have been filled in.", |
  | `console/src/locales/ja.json` | +7/-0 | 前端国际化 | 修改文件；新增文案 key："feishuScanGuide": "FeishuでQRコードをスキャンしてボットを作成します。スキャン後、Feishuアプリが自動作成され、App IDとApp Secretが自動入力されます。",；"feishuScanLogin": "スキャンしてボットを作成",；"feishuGetQrcode": "Feishu QRコードを取得",；"feishuScanHint": "上のQRコードをFeishuでスキャンしてください。認証後、App IDとApp Secretが自動入力されます。",；"feishuAuthSuccess": "Feishuボットが作成されました。App IDとApp Secretが自動入力されました。", |
  | `console/src/locales/pt-BR.json` | +7/-0 | 前端国际化 | 修改文件；新增文案 key："feishuScanGuide": "Scan the QR code with Feishu to create a bot instantly. A Feishu app will be created automatically a；"feishuScanLogin": "Scan to Criar Bot",；"feishuGetQrcode": "Get Feishu QR Code",；"feishuScanHint": "Scan the QR code above with Feishu. App ID and App Secret will be filled in automatically after autho；"feishuAuthSuccess": "Feishu bot created. App ID and App Secret have been filled in.", |
  | `console/src/locales/ru.json` | +7/-0 | 前端国际化 | 修改文件；新增文案 key："feishuScanGuide": "Отсканируйте QR-код в Feishu для мгновенного создания бота. Приложение Feishu будет создано автомати；"feishuScanLogin": "Сканировать для создания бота",；"feishuGetQrcode": "Получить QR-код Feishu",；"feishuScanHint": "Отсканируйте QR-код выше с помощью Feishu. App ID и App Secret будут заполнены автоматически после ав；"feishuAuthSuccess": "Бот Feishu создан. App ID и App Secret заполнены автоматически.", |
  | `console/src/locales/zh.json` | +7/-0 | 前端国际化 | 修改文件；新增文案 key："feishuScanGuide": "使用飞书扫码一键创建机器人。扫码后将自动创建飞书应用并获取 App ID 和 App Secret。",；"feishuScanLogin": "扫码创建机器人",；"feishuGetQrcode": "获取飞书二维码",；"feishuScanHint": "请使用飞书扫描上方二维码，完成授权后 App ID 与 App Secret 将自动填入。",；"feishuAuthSuccess": "飞书机器人创建成功，App ID 与 App Secret 已自动填入", |
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +33/-0 | 前端页面 | 修改文件；新增配置/字段：app_id: credentials.app_id,；app_secret: credentials.app_secret, |
  | `src/qwenpaw/app/channels/qrcode_auth_handler.py` | +189/-0 | 后端渠道实现 | 修改文件；新增/修改符号：class FeishuQRCodeAuthHandler(QRCodeAuthHandler):；async def _get_domain(self, request: Request) -> str:；def _get_accounts_domain(self, domain: str) -> str:；async def fetch_qrcode(self, request: Request) -> QRCodeResult:；新增配置/字段：try:；try:；"Content-Type": "application/x-www-form-urlencoded",；"action": "begin", |
  | `tests/unit/channels/test_qrcode_auth_handler.py` | +269/-0 | 测试/CI | 新增文件；新增/修改符号：def mock_request():；def feishu_handler():；def mock_httpx_client():；def _create_mock(responses):；新增配置/字段：Args:；responses: Single response or list of responses for side_effect；else:；"device_code": "device_123", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [98] `c1ce3db` feat(memory): add ADBPG long-term memory with BaseMemoryManager architure (#2308)

- **完整 SHA**：`c1ce3db78d5137ba6e8bc6cd14de98f80221249c`
- **日期/作者**：`2026-05-12` / `shaohuaxi`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`18 文件`，`+1867/-9`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响记忆管理、自动记忆或长期记忆配置
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/agent.ts` | +23/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface ADBPGMemoryConfig {；新增配置/字段：host: string;；port: number;；user: string;；password: string; |
  | `console/src/constants/backendMappings.ts` | +7/-0 | 其他 | 修改文件；新增配置/字段：adbpg: {；configField: "adbpg_memory_config",；component: ADBPGConfigCard,；label: "adbpg", |
  | `console/src/locales/en.json` | +23/-2 | 前端国际化 | 修改文件；新增文案 key："memoryManagerBackendTooltip": "Backend for the memory manager. Choose remelight (local files) or adbpg (cloud database)；"backendRestartWarning": "Switching backends does not support hot reload. Save and restart QwenPaw for changes to take e；"adbpgMemoryTitle": "ADBPG Long-term Memory",；"adbpgConfig": {；"title": "ADBPG Memory Configuration", |
  | `console/src/locales/ja.json` | +23/-2 | 前端国际化 | 修改文件；新增文案 key："memoryManagerBackendTooltip": "メモリマネージャーのバックエンドタイプ。remelight（ローカルファイル）または adbpg（クラウドデータベース）から選択できます。",；"saveLevelFailed": "ツール実行セキュリティレベルの保存に失敗しました",；"adbpgMemoryTitle": "ADBPG Long-term Memory",；"adbpgConfig": {；"title": "ADBPG Memory Configuration", |
  | `console/src/locales/pt-BR.json` | +1/-1 | 前端国际化 | 修改文件；新增文案 key："memoryManagerBackendTooltip": "Backend para o gerenciador de memória. Escolha remelight (arquivos locais) ou adbpg (ban |
  | `console/src/locales/ru.json` | +23/-2 | 前端国际化 | 修改文件；新增文案 key："memoryManagerBackendTooltip": "Тип бэкенда менеджера памяти. Выберите remelight (локальные файлы) или adbpg (облачная б；"saveLevelFailed": "Не удалось сохранить уровень безопасности выполнения инструментов",；"adbpgMemoryTitle": "ADBPG Long-term Memory",；"adbpgConfig": {；"title": "ADBPG Memory Configuration", |
  | `console/src/locales/zh.json` | +23/-2 | 前端国际化 | 修改文件；新增文案 key："memoryManagerBackendTooltip": "记忆管理器的后端类型，可选 remelight（本地文件）或 adbpg（云端数据库）",；"backendRestartWarning": "切换后端不支持热更新，保存后需要重启 QwenPaw 才能生效",；"adbpgMemoryTitle": "ADBPG 长期记忆",；"adbpgConfig": {；"title": "ADBPG 记忆配置", |
  | `console/src/pages/Agent/Config/components/ADBPGConfigCard.tsx` | +151/-0 | 前端页面 | 新增文件；新增/修改符号：export function ADBPGConfigCard() {；const apiMode = Form.useWatch(["adbpg_memory_config", "api_mode"]) ?? "rest"; |
  | `console/src/pages/Agent/Config/components/index.ts` | +1/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Agent/Config/useAgentConfig.tsx` | +1/-0 | 前端页面 | 修改文件 |
  | `pyproject.toml` | +3/-0 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/memory/__init__.py` | +4/-0 | 记忆系统 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/memory/adbpg_client.py` | +751/-0 | 记忆系统 | 新增文件；新增/修改符号：class ConfigurationError(Exception):；class ADBPGConfig:；def _get_shared_pool(；def close_shared_pool() -> None:；新增配置/字段：try:；host: str；port: int；user: str |
  | `src/qwenpaw/agents/memory/adbpg_memory_manager.py` | +508/-0 | 记忆系统 | 新增文件；新增/修改符号：class ADBPGMemoryManager(BaseMemoryManager):；def __init__(self, working_dir: str, agent_id: str) -> None:；async def start(self) -> None:；async def close(self) -> bool:；新增配置/字段：try:；else:；try:；"zh": ADBPG_MEMORY_GUIDANCE_ZH, |
  | `src/qwenpaw/agents/memory/adbpg_prompts.py` | +70/-0 | 记忆系统 | 新增文件；逻辑 hunk 调整 |
  | `src/qwenpaw/config/config.py` | +47/-0 | 配置/常量 | 修改文件；新增/修改符号：class ADBPGMemoryConfig(BaseModel):；新增配置/字段：host: str = ""；port: int = 5432；user: str = ""；password: str = "" |
  | `website/public/docs/memory.en.md` | +104/-0 | 文档/发布 | 修改文件；新增配置/字段："running": {；"memory_manager_backend": "adbpg",；"adbpg_memory_config": {；"host": "gp-xxxxxxxxx-master.gpdb.rds.aliyuncs.com", |
  | `website/public/docs/memory.zh.md` | +104/-0 | 文档/发布 | 修改文件；新增配置/字段："running": {；"memory_manager_backend": "adbpg",；"adbpg_memory_config": {；"host": "gp-xxxxxxxxx-master.gpdb.rds.aliyuncs.com", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语
  - 需排除包名、项目名、发布说明等品牌化内容

---

## [99] `d4395e7` fix(mcp): add monkey patch for mcp (#4245)

- **完整 SHA**：`d4395e735938c65ca21e55bbe7907bfb3e353c20`
- **日期/作者**：`2026-05-12` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+45/-1`
- **实际影响范围**：
  - 影响 MCP 工具连接生命周期、超时、OAuth 或清理逻辑
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/mcp/stateful_client.py` | +45/-1 | MCP | 修改文件；新增/修改符号：def _extract_json_schema_from_mcp_tool(tool: _Tool) -> dict[str, Any]:；新增配置/字段："type": "function",；"function": {；"name": tool.name,；"description": tool.description or "", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [100] `977ffe3` refactor(agent_stats): streamline session file handling and remove unused code (#4250)

- **完整 SHA**：`977ffe3bbffa10fd9502f8243d8dca64e2f5236c`
- **日期/作者**：`2026-05-12` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P2`
- **总体规模**：`1 文件`，`+24/-17`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agent_stats/service.py` | +24/-17 | 其他 | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

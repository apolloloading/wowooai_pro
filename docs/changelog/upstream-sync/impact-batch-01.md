# 逐 commit 代码影响分析（第 1 批）

> 范围：第 1 - 25 条。此文档基于 diff 提取，重点回答“commit 了什么、影响哪里”。

## [1] `8aa5f27` chore(version): bump version to 1.1.5.post1 (#3970)

- **完整 SHA**：`8aa5f27847a70f679ccfa9fd4d8917fda90e9cf7`
- **日期/作者**：`2026-04-30` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`1 文件`，`+1/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/__version__.py` | +1/-1 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [2] `518ce42` feat(feishu): introduce FeishuCardHandler and upgrade tool_guard approval to interactive buttons (#3941)

- **完整 SHA**：`518ce42c08bdb600df276cebcbce7a96becc8f7c`
- **日期/作者**：`2026-04-30` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+736/-1`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/feishu/card_handler.py` | +481/-0 | 后端渠道实现 | 新增文件；新增/修改符号：class CardKind:；class FeishuCardHandler:；def __init__(self, channel: "FeishuChannel") -> None:；def _register(self, kind: CardKind) -> None:；新增配置/字段：try:；name: str  # human-readable tag for logs；message_type: str  # matches ``metadata.message_type`` (outbound)；action_type: str  # matches button ``value.type`` (inbound) |
  | `src/qwenpaw/app/channels/feishu/card_templates.py` | +222/-0 | 后端渠道实现 | 新增文件；新增/修改符号：def _truncate(text: str, limit: int) -> str:；def _tool_guard_severity_template(severity: str) -> str:；def build_tool_guard_approval_card(；def build_tool_guard_resolved_card(；新增配置/字段："critical": "red",；"high": "red",；"medium": "orange",；"low": "yellow", |
  | `src/qwenpaw/app/channels/feishu/channel.py` | +33/-1 | 后端渠道实现 | 修改文件；新增/修改符号：async def on_event_message_completed(  # type: ignore[override]；新增配置/字段：request: Any,；to_handle: str,；event: Any,；send_meta: Dict[str, Any], |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [3] `d9526bf` fix(WeCom): keep placeholder stream alive to prevent stuck "Thinking..."  (#3950)

- **完整 SHA**：`d9526bf0be2c1055fa407c67d61ec556a117bc2c`
- **日期/作者**：`2026-04-30` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+85/-3`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wecom/channel.py` | +85/-3 | 后端渠道实现 | 修改文件；新增/修改符号：async def _keepalive_processing(；新增配置/字段：frame: Any,；stream_id: str,；interval: float = _PROCESSING_REFRESH_INTERVAL,；max_duration: float = _PROCESSING_MAX_DURATION, |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [4] `59ebc8e` feat(chat) adjust CodeMirror line wrapping in tool call input/output blocks (#3960)

- **完整 SHA**：`59ebc8e7c9fcd8be1a63ea73a18cf2608e4b0904`
- **日期/作者**：`2026-04-30` / `Bowen Liang`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+17/-0`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/styles/layout.css` | +17/-0 | 其他 | 修改文件 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [5] `90cf5ac` fix(WeCom): avoid double reconnect race and cross-loop disconnect (#3963)

- **完整 SHA**：`90cf5acb2f35943e6deb93ac785bcf62a40dbbb4`
- **日期/作者**：`2026-04-30` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+23/-12`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wecom/channel.py` | +13/-10 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/channels/test_wecom.py` | +10/-2 | 测试/CI | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [6] `2709e95` feat(WeCom): add share_session_in_group toggle for group chats (#3948)

- **完整 SHA**：`2709e95dc69c3ab51b52084add19e4819f4e50a0`
- **日期/作者**：`2026-04-30` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+31/-3`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/channel.ts` | +1/-0 | 前端 API/types | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +8/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/wecom/channel.py` | +19/-3 | 后端渠道实现 | 修改文件；新增配置/字段：share_session_in_group: bool = True,；"user_id": ( |
  | `src/qwenpaw/config/config.py` | +3/-0 | 配置/常量 | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [7] `c85361a` feat(app): prevent path traversal by rejecting absolute static file paths (#3973)

- **完整 SHA**：`c85361ad0d6d89343c361944a9ecef2017e67030`
- **日期/作者**：`2026-04-30` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+5/-3`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/_app.py` | +5/-3 | 其他 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [8] `9b7acb3` feat(feishu): hint docs link on approval card when card.action.trigger is unsubscribed (#3982)

- **完整 SHA**：`9b7acb3503fb75e48141d5cb2e8eaafdf0e42edd`
- **日期/作者**：`2026-04-30` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+46/-2`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/feishu/card_templates.py` | +16/-0 | 后端渠道实现 | 修改文件；新增配置/字段："tag": "markdown",；"content": ( |
  | `website/public/docs/channels.en.md` | +15/-1 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/channels.zh.md` | +15/-1 | 文档/发布 | 修改文件；文档或提示词文本调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [9] `6368ca3` chore(version): bumping version to 1.1.6b1 (#4012)

- **完整 SHA**：`6368ca37f6d757c51bac0c31d9087fa6506cfd5d`
- **日期/作者**：`2026-05-03` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`1 文件`，`+1/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/__version__.py` | +1/-1 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [10] `d783c3b` docs(website): update documentation to v1.1.5 (#4013)

- **完整 SHA**：`d783c3b0b2ff3b6d013f26c9ed12e9dc17dbc53b`
- **日期/作者**：`2026-05-03` / `Yuexiang XIE`
- **标签/优先级**：`⚪ 跳过-无关` / `P3`
- **总体规模**：`13 文件`，`+373/-79`
- **实际影响范围**：
  - 影响记忆管理、自动记忆或长期记忆配置
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `website/public/docs/cli.en.md` | +40/-16 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/cli.zh.md` | +40/-16 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/commands.en.md` | +35/-6 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/commands.zh.md` | +35/-6 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/config.en.md` | +44/-5 | 文档/发布 | 修改文件；新增配置/字段："enabled": true,；"shell_evasion_checks": {；"command_substitution": false,；"obfuscated_flags": false, |
  | `website/public/docs/config.zh.md` | +44/-5 | 文档/发布 | 修改文件；新增配置/字段："enabled": true,；"shell_evasion_checks": {；"command_substitution": false,；"obfuscated_flags": false, |
  | `website/public/docs/memory.zh.md` | +1/-1 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/models.en.md` | +3/-0 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/models.zh.md` | +3/-0 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/security.en.md` | +62/-10 | 文档/发布 | 修改文件；新增配置/字段："disabled_rules": [],；"shell_evasion_checks": {；"command_substitution": false,；"obfuscated_flags": false, |
  | `website/public/docs/security.zh.md` | +62/-10 | 文档/发布 | 修改文件；新增配置/字段："disabled_rules": [],；"shell_evasion_checks": {；"command_substitution": false,；"obfuscated_flags": false, |
  | `website/src/i18n/locales/en.json` | +2/-2 | 文档/发布 | 修改文件；新增文案 key："sub": "v1.1.5: QwenPaw custom LLMs, safety architecture, multi-agent collaboration,",；"releaseNote": "QwenPaw v1.1.5 is released", |
  | `website/src/i18n/locales/zh.json` | +2/-2 | 文档/发布 | 修改文件；新增文案 key："sub": "v1.1.5 四大方面能力升级：",；"releaseNote": "QwenPaw v1.1.5版本全新发布", |
- **合入检查点**：
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [11] `d85181a` feat(chat): generate session titles asynchronously via LLM (#3829)

- **完整 SHA**：`d85181a5335d7d45f034ceaa91cb9b8494ca9a56`
- **日期/作者**：`2026-05-04` / `Eric Zhu`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`14 文件`，`+1048/-20`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/agent.ts` | +6/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface AutoTitleConfig {；新增配置/字段：enabled: boolean;；timeout_seconds: number;；auto_title_config: AutoTitleConfig; |
  | `console/src/locales/en.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："autoGenerateSessionTitle": "Auto-generate session titles",；"autoGenerateSessionTitleTooltip": "After the first user message in a new chat, run a short background LLM call to repla |
  | `console/src/locales/ja.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："autoGenerateSessionTitle": "セッションタイトルを自動生成",；"autoGenerateSessionTitleTooltip": "新しいチャットの最初のユーザーメッセージ後、バックグラウンドで短いLLM呼び出しを実行し、切り詰められたプレースホルダを簡潔なタイトルに置き換えます。新しいチャットごと |
  | `console/src/locales/ru.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："autoGenerateSessionTitle": "Автогенерация заголовков сессий",；"autoGenerateSessionTitleTooltip": "После первого пользовательского сообщения в новом чате фоновая задача делает коротки |
  | `console/src/locales/zh.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："autoGenerateSessionTitle": "自动生成会话标题",；"autoGenerateSessionTitleTooltip": "新会话首条用户消息发送后，后台触发一次轻量 LLM 调用，把截断的占位标题替换为更贴切的短标题。每个新会话会多一次 LLM 调用；关闭后保留占位标题、不产生该开销。", |
  | `console/src/pages/Agent/Config/components/ReactAgentCard.tsx` | +9/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Agent/Config/useAgentConfig.tsx` | +4/-0 | 前端页面 | 修改文件；新增配置/字段：auto_title_config: config.auto_title_config ?? {；enabled: true,；timeout_seconds: 30.0, |
  | `src/qwenpaw/app/routers/console.py` | +47/-12 | 后端 API 路由 | 修改文件；新增/修改符号：def _extract_placeholder_name(content_parts: list) -> tuple[str, str]: |
  | `src/qwenpaw/app/runner/manager.py` | +42/-8 | Agent 核心/执行 | 修改文件；新增/修改符号：async def patch_chat_if_name_matches(；async def _patch_locked(；新增配置/字段：chat_id: str,；expected_name: str,；patch: ChatUpdate,；chat_id: str, |
  | `src/qwenpaw/app/runner/title_generator.py` | +225/-0 | Agent 核心/执行 | 新增文件；新增/修改符号：def _safe_attr(obj: Any, name: str) -> Any:；def _first_text_in_list(items: list) -> str:；def _extract_text_from_response(response: Any) -> str:；async def _consume_model_response(model: Any, messages: list) -> str:；新增配置/字段：try:；workspace: "Workspace",；chat_id: str,；user_message: str, |
  | `src/qwenpaw/config/config.py` | +40/-0 | 配置/常量 | 修改文件；新增/修改符号：class AutoTitleConfig(BaseModel):；新增配置/字段：enabled: bool = Field(；timeout_seconds: float = Field(；auto_title_config: AutoTitleConfig = Field( |
  | `tests/unit/app/test_chat_updates.py` | +55/-0 | 测试/CI | 修改文件；新增/修改符号：async def test_patch_chat_if_name_matches_applies_when_name_matches(；async def test_patch_chat_if_name_matches_skips_when_name_differs(；async def test_patch_chat_if_name_matches_returns_none_for_missing_chat(；新增配置/字段：chat_manager: ChatManager,；chat_manager: ChatManager,；chat_manager: ChatManager, |
  | `tests/unit/app/test_title_generator.py` | +524/-0 | 测试/CI | 新增文件；新增/修改符号：class TestCleanTitle:；def test_strips_surrounding_whitespace(self) -> None:；def test_strips_double_quotes(self) -> None:；def test_strips_smart_quotes(self) -> None:；新增配置/字段：chat_manager: ChatManager,；name: str = "Hello, wor",；model: AsyncMock \| MagicMock \| None = None,；factory_error: BaseException \| None = None, |
  | `tests/unit/routers/test_console_placeholder.py` | +88/-0 | 测试/CI | 新增文件；新增/修改符号：class _TextBlock:；def __init__(self, text: str) -> None:；def test_no_content_parts_returns_new_chat() -> None:；def test_string_content_part() -> None: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [12] `534d8ba` fix(message_processing): return resolved path for file:// url audio blocks (#4021)

- **完整 SHA**：`534d8ba0a3bbad52d6c15465b0f3853cff30336c`
- **日期/作者**：`2026-05-06` / `karl`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+6/-0`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/utils/message_processing.py` | +6/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [13] `694d317` fix(provider): increase max_token for anthropic compatible models (#4054)

- **完整 SHA**：`694d31712d108a286434adc940a61af841b2c1c5`
- **日期/作者**：`2026-05-06` / `Xuchen Pan`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+59/-3`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/providers/anthropic_provider.py` | +9/-1 | 模型 Provider | 修改文件；新增配置/字段：else:；timeout: float = 60, |
  | `src/qwenpaw/providers/gemini_provider.py` | +1/-1 | 模型 Provider | 修改文件 |
  | `src/qwenpaw/providers/openai_provider.py` | +1/-1 | 模型 Provider | 修改文件 |
  | `tests/unit/providers/test_anthropic_provider.py` | +48/-0 | 模型 Provider | 修改文件；新增/修改符号：def test_get_chat_model_instance_uses_configured_max_tokens(；class FakeAnthropicChatModel:；def __init__(self, **kwargs) -> None:；def test_get_chat_model_instance_uses_default_max_tokens_when_unset(；新增配置/字段：captured: dict[str, object] = {}；"max_tokens": 4096,；"temperature": 0.2,；captured: dict[str, object] = {} |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [14] `b458910` perf(console): Solve duplicate rendering (#4052)

- **完整 SHA**：`b458910f23544620b05ddc6a5053b0de37ceac51`
- **日期/作者**：`2026-05-06` / `zhaozhuang521`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+9/-2`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/components/ConsolePollService/index.tsx` | +9/-2 | 前端组件 | 修改文件；新增/修改符号：const prevApprovalsRef = { current: "" };；const serialized = JSON.stringify(res.pending_approvals); |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [15] `edf8ed1` fix(mcp): typo fix (#4058)

- **完整 SHA**：`edf8ed11644112c9c60cc714284bc99b46f364fc`
- **日期/作者**：`2026-05-06` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+1/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/react_agent.py` | +1/-1 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [16] `a8be4d7` fix(mcp): use read_timeout_seconds as MCP tool execution_timeout instead of timeout (#4061)

- **完整 SHA**：`a8be4d7cebb4147276e694c08a2e8a2141ede7d4`
- **日期/作者**：`2026-05-06` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+6/-5`
- **实际影响范围**：
  - 影响 MCP 工具连接生命周期、超时、OAuth 或清理逻辑
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/react_agent.py` | +2/-2 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/mcp/stateful_client.py` | +4/-3 | MCP | 修改文件；新增配置/字段：read_timeout_seconds: float = 60 * 5,；read_timeout_seconds: The read timeout seconds |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [17] `ba7c4fd` chore(utils): remove redundant codes (#4048)

- **完整 SHA**：`ba7c4fd2b373b68d3c04f34162c581966df94390`
- **日期/作者**：`2026-05-06` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P2`
- **总体规模**：`1 文件`，`+0/-13`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/utils/message_processing.py` | +0/-13 | 其他 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [18] `e43731e` fix(telegram): telegram network retry (#4039)

- **完整 SHA**：`e43731efc542a6b10046d194f3581d0d277a365d`
- **日期/作者**：`2026-05-06` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+159/-3`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/telegram/channel.py` | +159/-3 | 后端渠道实现 | 修改文件；新增/修改符号：class _PollingReconnectRequested(Exception):；def __init__(self, reason: str, *, attempt: int, delay: float):；def _looks_like_polling_conflict(error: Exception) -> bool:；def _looks_like_network_error(error: Exception) -> bool:；新增配置/字段：reason: str,；app: Any,；reason: str,；error: Exception, |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [19] `bc5a81e` feat(i18n): add Brazilian Portuguese (pt-BR) locale support (#4009)

- **完整 SHA**：`bc5a81eb39f85c6d11e72dc33ad4c2adc0ec8717`
- **日期/作者**：`2026-05-06` / `Jailton Fonseca`
- **标签/优先级**：`🟠 待人工` / `P1`
- **总体规模**：`5 文件`，`+2355/-2`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/components/LanguageSwitcher/index.tsx` | +11/-1 | 前端组件 | 修改文件；新增/修改符号：const knownLanguages = ["en", "zh", "ja", "ru", "pt-BR"];；const currentLangKey = knownLanguages.includes(currentLanguage)；新增配置/字段：key: "pt-BR",；label: "Português (Brasil)",；onClick: () => changeLanguage("pt-BR"),；"pt-BR": <SparkEnglish02Line />, |
  | `console/src/i18n.ts` | +4/-0 | 前端国际化 | 修改文件；新增配置/字段："pt-BR": {；translation: ptBR, |
  | `console/src/locales/pt-BR.json` | +1857/-0 | 前端国际化 | 新增文件；新增文案 key："common": {；"save": "Salvar",；"reset": "Redefinir",；"cancel": "Cancelar",；"confirm": "Confirmar", |
  | `website/src/i18n/index.ts` | +3/-1 | 文档/发布 | 修改文件；新增/修改符号：export type Lang = "zh" \| "en" \| "pt-BR"; |
  | `website/src/i18n/locales/pt-BR.json` | +480/-0 | 文档/发布 | 新增文件；新增文案 key："nav": {；"docs": "Documentacao",；"more": "Mais",；"releaseNotes": "Notas de Lancamento",；"qwenpaw": "Qwenpaw", |
- **合入检查点**：
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [20] `5c49769` fix(skill):  resilient loading for migrated or malformed skill & skill pool entries (#4016)

- **完整 SHA**：`5c49769ecd8e269911f45731c38d96418751ee2c`
- **日期/作者**：`2026-05-06` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+216/-126`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/skill.ts` | +7/-1 | 前端 API/types | 修改文件；新增/修改符号：const text = await response.text();；const contentType = response.headers.get("content-type") \|\| ""; |
  | `console/src/utils/error.ts` | +18/-5 | 其他 | 修改文件；新增/修改符号：const msg = error.message;；const idx = msg.indexOf(" - ");；const parsed = JSON.parse(msg.slice(idx + 3));；const parsed = JSON.parse(msg); |
  | `src/qwenpaw/agents/skills_manager.py` | +113/-69 | 技能系统 | 修改文件；新增/修改符号：def _normalize_skill_manifest_entry(entry: Any) -> dict[str, Any]:；新增配置/字段：try:；try:；else:；"enabled": enabled, |
  | `src/qwenpaw/app/routers/skills.py` | +78/-51 | 后端 API 路由 | 修改文件；新增配置/字段：try:；try: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [21] `27579ce` fix(approval): /approve shorthand ignores request_id argument (#4014)

- **完整 SHA**：`27579ceab33a71de50970eeff8a9cbc01e615e79`
- **日期/作者**：`2026-05-06` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+9/-5`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/runner/control_commands/approval_handler.py` | +9/-5 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [22] `30dc625` docs(faq): Docs for handling APITimeoutError when running in WSL2 (NAT mode) (#4005)

- **完整 SHA**：`30dc6257e578a24b04131eb3823703b2c11e71e0`
- **日期/作者**：`2026-05-06` / `hllqkb`
- **标签/优先级**：`⚪ 跳过-无关` / `P3`
- **总体规模**：`2 文件`，`+96/-0`
- **实际影响范围**：
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `website/public/docs/faq.en.md` | +50/-0 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/faq.zh.md` | +46/-0 | 文档/发布 | 修改文件；文档或提示词文本调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [23] `678cc42` feat(skill): Add skill install/uninstall cli (#4053)

- **完整 SHA**：`678cc4255e22a68afe28bb569d90a569c3ecd269`
- **日期/作者**：`2026-05-06` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`6 文件`，`+341/-33`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/skills_manager.py` | +109/-20 | 技能系统 | 修改文件；新增配置/字段：try:；try:；"skill_name": skill_name,；"workspace_dir": str(self.workspace_dir), |
  | `src/qwenpaw/cli/skills_cmd.py` | +176/-1 | 技能系统 | 修改文件；新增/修改符号：def _require_agent_workspace(agent_id: str) -> Path:；def _raise_conflict(exc: SkillConflictError) -> None:；def install_cmd(；def uninstall_cmd(；新增配置/字段：bundle_url: str,；agent_id: str,；enable: bool,；try: |
  | `website/public/docs/cli.en.md` | +12/-6 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/cli.zh.md` | +12/-6 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/skills.en.md` | +16/-0 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `website/public/docs/skills.zh.md` | +16/-0 | 文档/发布 | 修改文件；文档或提示词文本调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [24] `24c0610` chore(version): bumping version to 1.1.5p2 (#4071)

- **完整 SHA**：`24c06102cee234b47fdcf1e2501b6171bc6fb601`
- **日期/作者**：`2026-05-06` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`1 文件`，`+1/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/__version__.py` | +1/-1 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [25] `18d7c15` chore(version): bump version to 1.1.6b1 (#4082)

- **完整 SHA**：`18d7c15c103e4e6c4888267f996b0dc33ce4017c`
- **日期/作者**：`2026-05-07` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`1 文件`，`+1/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/__version__.py` | +1/-1 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

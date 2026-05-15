# 逐 commit 代码影响分析（第 2 批）

> 范围：第 26 - 50 条。此文档基于 diff 提取，重点回答“commit 了什么、影响哪里”。

## [26] `73e03e2` test(integration): add app startup and settings/envs smoke tests (#4081)

- **完整 SHA**：`73e03e2de121117299e3d30ef71dfed10efcd922`
- **日期/作者**：`2026-05-07` / `yutai78786`
- **标签/优先级**：`⚪ 跳过-无关` / `P3`
- **总体规模**：`3 文件`，`+329/-128`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `tests/integration/conftest.py` | +225/-0 | 测试/CI | 新增文件；新增/修改符号：def _find_free_port(host: str = "127.0.0.1") -> int:；def _tee_stream(stream, buffer: list[str]) -> None:；class AppServer:；def base_url(self) -> str:；新增配置/字段：try:；finally:；host: str；port: int |
  | `tests/integration/test_app_startup.py` | +31/-128 | 测试/CI | 修改文件；新增/修改符号：def test_api_version_ok(app_server) -> None:；def test_console_entry_or_fallback_ok(app_server) -> None: |
  | `tests/integration/test_settings_envs.py` | +73/-0 | 测试/CI | 新增文件；新增/修改符号：def test_settings_language_default_en(app_server) -> None:；def test_settings_language_put_get_roundtrip(app_server) -> None:；def test_settings_language_reject_invalid(app_server) -> None:；def test_envs_put_get_roundtrip(app_server) -> None: |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [27] `769230d` fix(console): avoid SSE crash on malformed surrogate text (#3553)

- **完整 SHA**：`769230d16bf333aff297e718abe7fa9fe5f47358`
- **日期/作者**：`2026-05-07` / `yang liu`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`5 文件`，`+199/-23`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/base.py` | +68/-6 | 后端渠道实现 | 修改文件；新增/修改符号：def _sanitize_surrogate_text(text: str) -> str:；def _sanitize_for_json(cls, value: Any) -> Any:；def _serialize_event_for_sse(self, event: Any) -> str:；新增配置/字段：try:；out: Dict[Any, Any] = {}；try:；else: |
  | `src/qwenpaw/app/channels/console/channel.py` | +7/-10 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/dingtalk/channel.py` | +1/-7 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/channels/test_base_core.py` | +63/-0 | 测试/CI | 修改文件；新增/修改符号：async def test_stream_with_tracker_falls_back_on_surrogate_json_error(；class BrokenJsonEvent:；def model_dump_json(self):；def model_dump(self, mode="python"):；新增配置/字段："object": "response",；"status": "completed",；"text": "\ud83c broken", |
  | `tests/unit/channels/test_console.py` | +60/-0 | 测试/CI | 修改文件；新增/修改符号：async def test_stream_one_falls_back_on_surrogate_json_error(；class BrokenJsonEvent:；def model_dump_json(self):；def model_dump(self, mode="python"):；新增配置/字段："object": "response",；"status": "completed",；"text": "\ud83d broken",；"sender_id": "user123", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [28] `62f22c7` chore(console): Optimize language switching logic and replace with the latest language icon (#4085)

- **完整 SHA**：`62f22c7adabd1e6eea807557001e4d1466295a08`
- **日期/作者**：`2026-05-07` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P2`
- **总体规模**：`4 文件`，`+36/-47`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/package-lock.json` | +4/-4 | 其他 | 修改文件；新增配置/字段："version": "1.0.67",；"resolved": "https://registry.npmjs.org/@agentscope-ai/icons/-/icons-1.0.67.tgz",；"integrity": "sha512-tbly1taaZTHcu9IdmBOWK9ZLLNZ/j2suVKqUgwR0hcr+BAN0kNT08r5sFRvpRDALcdxJdwLNzMlIv0670XfA3g==", |
  | `console/package.json` | +1/-1 | 其他 | 修改文件；JSON 配置/元数据调整 |
  | `console/src/components/LanguageSwitcher/index.tsx` | +27/-38 | 前端组件 | 修改文件；新增/修改符号：interface LanguageConfig {；const LANGUAGE_LIST: LanguageConfig[] = [；const KNOWN_LANG_KEYS = new Set(LANGUAGE_LIST.map((lang) => lang.key));；const currentLangKey = KNOWN_LANG_KEYS.has(currentLanguage)；新增配置/字段：key: string;；label: string;；icon: React.ReactElement;；onClick: () => changeLanguage(key), |
  | `console/src/pages/Settings/Agents/components/AgentModal.tsx` | +4/-4 | 前端页面 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [29] `6773901` feat(chat): replace Web Speech API with Whisper transcription for voice input (#3574)

- **完整 SHA**：`677390130674236ce0b94e3e3e3d50146ec95565`
- **日期/作者**：`2026-05-07` / `tqjason`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`9 文件`，`+501/-1`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/agent.ts` | +45/-0 | 前端 API/types | 修改文件；新增/修改符号：export type TranscriptionErrorCode =；export class TranscriptionError extends Error {；const formData = new FormData();；const response = await fetch(getApiUrl("/workspace/transcribe"), {；新增配置/字段：status: number;；transcribeAudio: async (file: File \| Blob): Promise<{ text: string }> => {；method: "POST",；headers: buildAuthHeaders(), |
  | `console/src/locales/en.json` | +10/-0 | 前端国际化 | 修改文件；新增文案 key："speech": {；"startRecording": "Start voice recording (Ctrl+Shift+M)",；"stopRecording": "Stop recording (Ctrl+Shift+M)",；"transcribing": "Transcribing...",；"transcriptionDisabled": "Transcription is disabled. Configure a provider in Settings > Voice Transcription.", |
  | `console/src/locales/ja.json` | +10/-0 | 前端国际化 | 修改文件；新增文案 key："speech": {；"startRecording": "音声録音を開始 (Ctrl+Shift+M)",；"stopRecording": "録音を停止 (Ctrl+Shift+M)",；"transcribing": "文字起こし中...",；"transcriptionDisabled": "文字起こしは無効です。設定 > 音声文字起こしでプロバイダーを設定してください。", |
  | `console/src/locales/pt-BR.json` | +10/-0 | 前端国际化 | 修改文件；新增文案 key："speech": {；"startRecording": "Iniciar gravação de voz (Ctrl+Shift+M)",；"stopRecording": "Parar gravação (Ctrl+Shift+M)",；"transcribing": "Transcrevendo...",；"transcriptionDisabled": "A transcrição está desativada. Configure um provedor em Configurações > Transcrição de Voz.", |
  | `console/src/locales/ru.json` | +10/-0 | 前端国际化 | 修改文件；新增文案 key："speech": {；"startRecording": "Начать запись голоса (Ctrl+Shift+M)",；"stopRecording": "Остановить запись (Ctrl+Shift+M)",；"transcribing": "Транскрибация...",；"transcriptionDisabled": "Транскрибация отключена. Настройте провайдер в Настройки > Голосовая транскрибация.", |
  | `console/src/locales/zh.json` | +10/-0 | 前端国际化 | 修改文件；新增文案 key："speech": {；"startRecording": "开始语音录制 (Ctrl+Shift+M)",；"stopRecording": "停止录制 (Ctrl+Shift+M)",；"transcribing": "正在转录...",；"transcriptionDisabled": "语音转录已禁用。请在设置 > 语音转写中配置转录服务。", |
  | `console/src/pages/Chat/components/WhisperSpeechButton/index.tsx` | +256/-0 | 前端页面 | 新增文件；新增/修改符号：const MAX_RECORDING_DURATION_MS = 5 * 60 * 1000; // 5 minutes；const MAX_AUDIO_SIZE_MB = 25;；export interface WhisperSpeechButtonRef {；interface WhisperSpeechButtonProps {；新增配置/字段：toggleRecording: () => void;；isRecording: () => boolean;；isLoading: () => boolean;；onTranscription: (text: string) => void; |
  | `console/src/pages/Chat/index.tsx` | +57/-1 | 前端页面 | 修改文件；新增/修改符号：const whisperSpeechRef = useRef<WhisperSpeechButtonRef>(null);；const handleWhisperTranscription = useCallback((text: string) => {；const senderContainer = document.querySelector('[class*="sender"]');；const textarea = senderContainer?.querySelector(；新增配置/字段：allowSpeech: !whisperEnabled,；prefix: whisperEnabled ? ( |
  | `src/qwenpaw/app/routers/workspace.py` | +93/-0 | 后端 API 路由 | 修改文件；新增/修改符号：async def post_transcribe_audio(；新增配置/字段：file: UploadFile = File(..., description="Audio file to transcribe"),；"code": "TRANSCRIPTION_DISABLED",；"message": (；"code": "UNSUPPORTED_FILE_TYPE", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [30] `166dc49` Feat(provider): add volcengine provider (#3994)

- **完整 SHA**：`166dc4942cf79565298cbeb9343ce464d1677d27`
- **日期/作者**：`2026-05-07` / `Lingrui Gu`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+267/-1`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Settings/Models/components/providerIcon.ts` | +3/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/providers/provider_manager.py` | +167/-1 | 模型 Provider | 修改文件；新增配置/字段：VOLCENGINE_MODELS: List[ModelInfo] = [；VOLCENGINE_CODINGPLAN_MODELS: List[ModelInfo] = [ |
  | `tests/unit/providers/test_volcengine_provider.py` | +97/-0 | 模型 Provider | 新增文件；新增/修改符号：def test_volcengine_providers_are_openai_compatible() -> None:；def test_volcengine_provider_configs() -> None:；def test_volcengine_models_list() -> None:；def isolated_secret_dir(monkeypatch, tmp_path): |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [31] `e393bc1` feat(token-usage): add token suage detailed api and trending charts (#4080)

- **完整 SHA**：`e393bc1efe8033cb87e195467c90ff6d63d38923`
- **日期/作者**：`2026-05-07` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`20 文件`，`+1333/-447`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/tokenUsage.ts` | +10/-1 | 前端 API/types | 修改文件 |
  | `console/src/api/types/tokenUsage.ts` | +10/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface TokenUsageRecord {；新增配置/字段：date: string; // YYYY-MM-DD；provider_id: string;；model: string;；prompt_tokens: number; |
  | `console/src/locales/en.json` | +8/-4 | 前端国际化 | 修改文件；新增文案 key："noData": "No token usage data in the selected period",；"modelTrend": "Model Usage Trend",；"tokenTypeChart": "Token Type Trend",；"selectAll": "Select All",；"allSelected": "All", |
  | `console/src/locales/ja.json` | +10/-6 | 前端国际化 | 修改文件；新增文案 key："totalTokens": "合計 Token",；"noData": "選択期間に Token 使用データがありません",；"modelTrend": "モデル使用量トレンド",；"tokenTypeChart": "トークンタイプのトレンド",；"selectAll": "すべて選択", |
  | `console/src/locales/ru.json` | +8/-4 | 前端国际化 | 修改文件；新增文案 key："noData": "Нет данных об использовании токенов за выбранный период",；"modelTrend": "Тренд использования моделей",；"tokenTypeChart": "Тренд типов токенов",；"selectAll": "Выбрать все",；"allSelected": "Все", |
  | `console/src/locales/zh.json` | +10/-6 | 前端国际化 | 修改文件；新增文案 key："totalTokens": "总 Token",；"noData": "所选时间段内暂无 Token 消耗数据",；"modelTrend": "模型用量趋势",；"tokenTypeChart": "Token 类型趋势",；"selectAll": "全选", |
  | `console/src/pages/Settings/TokenUsage/components/ChartFilterSelect.tsx` | +60/-0 | 前端页面 | 新增文件；新增/修改符号：interface ChartFilterSelectProps<T extends string> {；export function ChartFilterSelect<T extends string>({；新增配置/字段：value: T[];；onChange: (values: T[]) => void;；options: T[];；placeholder: string; |
  | `console/src/pages/Settings/TokenUsage/components/DataTables.tsx` | +137/-0 | 前端页面 | 新增文件；新增/修改符号：interface ByModelData {；interface ByDateData {；interface DataTablesProps {；export function DataTables({ byModelData, byDateData }: DataTablesProps) {；新增配置/字段：key: string;；model: string;；prompt_tokens: number;；completion_tokens: number; |
  | `console/src/pages/Settings/TokenUsage/components/ModelTrendChart.tsx` | +53/-0 | 前端页面 | 新增文件；新增/修改符号：interface ModelTrendChartProps {；export function ModelTrendChart({；新增配置/字段：chartConfig: any;；selectedModels: string[];；allModels: string[];；onModelChange: (models: string[]) => void; |
  | `console/src/pages/Settings/TokenUsage/components/SummaryCards.tsx` | +47/-0 | 前端页面 | 新增文件；新增/修改符号：interface SummaryCardsProps {；export function SummaryCards({；新增配置/字段：totalCalls: number;；totalPromptTokens: number;；totalCompletionTokens: number;；totalTokens: number; |
  | `console/src/pages/Settings/TokenUsage/components/TokenTypeChart.tsx` | +53/-0 | 前端页面 | 新增文件；新增/修改符号：const TOKEN_TYPES = ["Prompt Tokens", "Completion Tokens", "Total Tokens"];；interface TokenTypeChartProps {；export function TokenTypeChart({；新增配置/字段：chartConfig: any;；selectedTokenTypes: string[];；onTokenTypeChange: (types: string[]) => void;；display: "flex", |
  | `console/src/pages/Settings/TokenUsage/components/index.ts` | +5/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Settings/TokenUsage/hooks/useDataAggregation.ts` | +113/-0 | 前端页面 | 新增文件；新增/修改符号：interface AggregatedData {；export function useDataAggregation(records: TokenUsageRecord[]) {；const byModel: AggregatedData["by_model"] = {};；const byDate: AggregatedData["by_date"] = {};；新增配置/字段：total_prompt_tokens: number;；total_completion_tokens: number;；total_calls: number;；by_model: Record< |
  | `console/src/pages/Settings/TokenUsage/hooks/useModelTrendConfig.ts` | +152/-0 | 前端页面 | 新增文件；新增/修改符号：interface UseModelTrendConfigProps {；export function useModelTrendConfig({；const isDarkMode = isDark;；const allModelKeys = new Map<string, { provider: string; model: string }>();；新增配置/字段：byDateModel: Record<；model: string;；provider_id: string;；prompt_tokens: number; |
  | `console/src/pages/Settings/TokenUsage/hooks/useTokenTypeConfig.ts` | +156/-0 | 前端页面 | 新增文件；新增/修改符号：interface UseTokenTypeConfigProps {；const TYPE_COLORS: Record<string, string> = {；export function useTokenTypeConfig({；const isDarkMode = isDark;；新增配置/字段：byDate: Record<；prompt_tokens: number;；completion_tokens: number;；call_count: number; |
  | `console/src/pages/Settings/TokenUsage/index.module.less` | +174/-189 | 前端页面 | 修改文件；新增配置/字段：padding: 0 16px 24px;；width: 100%;；width: 200px;；width: 200px; |
  | `console/src/pages/Settings/TokenUsage/index.tsx` | +142/-171 | 前端页面 | 修改文件；新增/修改符号：const detailsData = await api.getTokenUsageDetails({；const handleRefresh = async () => {；const aggregatedData = useDataAggregation(records);；const modelTrendConfig = useModelTrendConfig({；新增配置/字段：byDateModel: aggregatedData?.by_date_model \|\| null,；byDate: aggregatedData?.by_date \|\| null,；model: key,；prompt_tokens: stats.prompt_tokens, |
  | `src/qwenpaw/app/routers/token_usage.py` | +48/-3 | 后端 API 路由 | 修改文件；新增/修改符号：async def get_token_usage_details(；新增配置/字段：start_date: str；end_date: str；model: str；provider: str |
  | ... |  |  | 另有 2 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [32] `16c28e9` fix(console): respect custom name for default agent (#4073)

- **完整 SHA**：`16c28e9712e53dcc9b991b10973a1ed4212818f2`
- **日期/作者**：`2026-05-07` / `mambo`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+8/-0`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/utils/agentDisplayName.ts` | +8/-0 | 其他 | 修改文件；新增/修改符号：export const DEFAULT_AGENT_DISPLAY_NAME = "Default Agent"; |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [33] `4ee41a8` fix(chat): remove redundant URL prefix stripping in file preview paths (#4089)

- **完整 SHA**：`4ee41a8911f1a2ffc0b7d06245eb3245103c3ad2`
- **日期/作者**：`2026-05-07` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+1/-20`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/chat.ts` | +0/-9 | 前端 API/types | 修改文件；移除符号：const previewPrefix = FILES_PREVIEW.replace(/^\/+/, ""); |
  | `console/src/pages/Chat/sessionApi/index.ts` | +1/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/files.py` | +0/-10 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [34] `182528e` refactor(wechat): centralize legacy weixin to wechat data migrations on workspace startup (#3605)

- **完整 SHA**：`182528e5de53f1c58a6df666e27cb63fc4d5e3c5`
- **日期/作者**：`2026-05-07` / `celestialhorse51D`
- **标签/优先级**：`🔴 跳过-冲突` / `P2`
- **总体规模**：`37 文件`，`+4750/-4322`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响定时任务、收件箱、消息推送或 session 隔离
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
  - 删除代码/资源，需确认我方没有依赖
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/channel.ts` | +3/-3 | 前端 API/types | 修改文件；新增/修改符号：export interface WeChatConfig extends BaseChannelConfig { |
  | `console/src/locales/en.json` | +19/-19 | 前端国际化 | 修改文件；新增文案 key："wechatSetupGuide": "WeChat personal account Bot (iLink protocol). On first start without a Bot Token, a QR code login U；"wechatContextTokenLimit": "WeChat iLink platform limitation: each user message's context_token allows a maximum of 10 r；"wechatBotToken": "Bot Token",；"wechatBotTokenTooltip": "Bearer token obtained after QR code login. Leave empty to trigger QR code login on startup.",；"wechatBotTokenPlaceholder": "Auto-filled after QR login, or paste manually", |
  | `console/src/locales/ja.json` | +19/-19 | 前端国际化 | 修改文件；新增文案 key："wechatSetupGuide": "WeChat個人アカウントBot（iLinkプロトコル）。Bot Tokenが未設定の場合、起動時にQRコードURLを表示します。スキャンして認証してください。Tokenはローカルに保存されます。"；"wechatContextTokenLimit": "WeChat iLinkプラットフォームの制限：各ユーザーメッセージのcontext_tokenで返信できるメッセージは最大10件です。これはプラットフォーム側のハード制限です。制限超；"wechatBotToken": "Bot Token",；"wechatBotTokenTooltip": "QRコードログイン後に取得したBearerトークン。空の場合は起動時にQRコードログインが案内されます。",；"wechatBotTokenPlaceholder": "QRログイン後に自動入力、または手動で貼り付け", |
  | `console/src/locales/pt-BR.json` | +19/-19 | 前端国际化 | 修改文件；新增文案 key："wechatSetupGuide": "WeChat personal account Bot (iLink protocol). On first start without a Bot Token, a QR code login U；"wechatContextTokenLimit": "WeChat iLink platform limitation: each user message's context_token allows a maximum of 10 r；"wechatBotToken": "Bot Token",；"wechatBotTokenTooltip": "Bearer token obtained after QR code login. Leave empty to trigger QR code login on startup.",；"wechatBotTokenPlaceholder": "Auto-filled after QR login, or paste manually", |
  | `console/src/locales/ru.json` | +19/-19 | 前端国际化 | 修改文件；新增文案 key："wechatSetupGuide": "Бот для личного аккаунта WeChat (протокол iLink). При первом запуске без Bot Token будет выведена с；"wechatContextTokenLimit": "Ограничение платформы WeChat iLink: context_token каждого сообщения пользователя позволяет о；"wechatBotToken": "Bot Token",；"wechatBotTokenTooltip": "Bearer-токен, полученный после входа по QR-коду. Оставьте пустым для запуска процедуры входа п；"wechatBotTokenPlaceholder": "Заполняется автоматически после QR-входа или введите вручную", |
  | `console/src/locales/zh.json` | +20/-20 | 前端国际化 | 修改文件；新增文案 key："wechat": "微信",；"wechatSetupGuide": "微信个人账号 Bot（iLink 协议）。首次启动时若未配置 Bot Token，系统将打印二维码链接，请扫码登录；Token 将自动保存到本地文件供后续使用。",；"wechatContextTokenLimit": "微信 iLink 平台限制：每条用户消息对应的 context_token 最多只能回复 10 条消息，这是平台侧的硬性限制。建议关闭思考及工具输出，或者使用消息合并功能以避免超出限制；"wechatBotToken": "Bot Token",；"wechatBotTokenTooltip": "扫码登录后获取的 Bearer Token。留空时将在启动时引导扫码登录。", |
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +34/-34 | 前端页面 | 修改文件；新增/修改符号：const wechatQrcode = useChannelQrcode({；新增配置/字段：wechat:；wechat: "https://qwenpaw.agentscope.io/docs/channels/?lang=zh#微信个人iLink",；channel: "wechat", |
  | `console/src/pages/Control/Channels/components/channelIcons.ts` | +2/-3 | 前端页面 | 修改文件；新增配置/字段：wechat:；wechat: "#07C160", |
  | `console/src/pages/Control/Channels/components/constants.ts` | +1/-1 | 前端页面 | 修改文件 |
  | `console/src/pages/Control/Channels/components/useChannelQrcode.ts` | +1/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/qrcode_auth_handler.py` | +8/-8 | 后端渠道实现 | 修改文件；新增/修改符号：class WeChatQRCodeAuthHandler(QRCodeAuthHandler): |
  | `src/qwenpaw/app/channels/registry.py` | +1/-1 | 后端渠道实现 | 修改文件 |
  | `src/qwenpaw/app/channels/wechat/__init__.py` | +6/-0 | 后端渠道实现 | 新增文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/wechat/channel.py` | +1651/-0 | 后端渠道实现 | 新增文件；新增/修改符号：class WeChatChannel(BaseChannel):；def __init__(；def from_env(；def from_config(；新增配置/字段：Authentication:；process: ProcessHandler,；enabled: bool,；bot_token: str = "", |
  | `src/qwenpaw/app/channels/wechat/client.py` | +724/-0 | 后端渠道实现 | 新增文件；新增/修改符号：class ILinkClient:；def __init__(；async def start(self) -> None:；async def stop(self) -> None:；新增配置/字段：Protocol: HTTP/JSON, no third-party SDK required.；Args:；bot_token: Bearer token obtained after QR code login.；base_url: iLink API base URL (defaults to ilinkai.weixin.qq.com). |
  | `src/qwenpaw/app/channels/wechat/utils.py` | +122/-0 | 后端渠道实现 | 新增文件；新增/修改符号：def make_headers(bot_token: str = "") -> Dict[str, str]:；def aes_ecb_decrypt(data: bytes, key_b64: str) -> bytes:；def aes_ecb_encrypt(data: bytes, key_b64: str) -> bytes:；def generate_aes_key_b64() -> str:；新增配置/字段：Authorization: Bearer <bot_token> — only set when token is available.；headers: Dict[str, str] = {；"Content-Type": "application/json",；"AuthorizationType": "ilink_bot_token", |
  | `src/qwenpaw/app/channels/weixin/__init__.py` | +0/-6 | 后端渠道实现 | 删除文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/weixin/channel.py` | +0/-1651 | 后端渠道实现 | 删除文件；移除符号：class WeixinChannel(BaseChannel):；def __init__(；def from_env( |
  | ... |  |  | 另有 19 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [35] `50c8712` refactor(console): adjust and opt TokenUsage page (#4094)

- **完整 SHA**：`50c87122df56f60290ff3fbba29e25df7c82ad22`
- **日期/作者**：`2026-05-07` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P2`
- **总体规模**：`8 文件`，`+76/-369`
- **实际影响范围**：
  - 删除代码/资源，需确认我方没有依赖
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Settings/TokenUsage/components/ChartFilterSelect.tsx` | +0/-60 | 前端页面 | 删除文件；移除符号：interface ChartFilterSelectProps<T extends string> {；export function ChartFilterSelect<T extends string>({ |
  | `console/src/pages/Settings/TokenUsage/components/ModelTrendChart.tsx` | +2/-30 | 前端页面 | 修改文件；新增/修改符号：export function ModelTrendChart({ chartConfig }: ModelTrendChartProps) { |
  | `console/src/pages/Settings/TokenUsage/components/TokenTypeChart.tsx` | +4/-30 | 前端页面 | 修改文件；新增/修改符号：export function TokenTypeChart({ chartConfig }: TokenTypeChartProps) { |
  | `console/src/pages/Settings/TokenUsage/components/index.ts` | +0/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Settings/TokenUsage/hooks/useModelTrendConfig.ts` | +11/-27 | 前端页面 | 修改文件；新增/修改符号：const allModelKeys = new Set<string>();；新增配置/字段：maxRows: 2,；itemMarkerSize: 8,；itemLabelFontSize: 11,；itemSpacing: 8, |
  | `console/src/pages/Settings/TokenUsage/hooks/useTokenTypeConfig.ts` | +9/-18 | 前端页面 | 修改文件；新增/修改符号：const allTypes = [；const colors = allTypes.map((type) => TYPE_COLORS[type]); |
  | `console/src/pages/Settings/TokenUsage/index.module.less` | +5/-134 | 前端页面 | 修改文件 |
  | `console/src/pages/Settings/TokenUsage/index.tsx` | +45/-69 | 前端页面 | 修改文件；新增/修改符号：const fetchData = useCallback(async () => {；const pageHeader = (；新增配置/字段：byDateModel: aggregatedData?.by_date_model ?? null,；byDate: aggregatedData?.by_date ?? null, |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [36] `3213fd1` plugin: add gpt-image-2 tool plugin (#3911)

- **完整 SHA**：`3213fd15848a20b0c162adf00a3d7963c3e591b5`
- **日期/作者**：`2026-05-07` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`25 文件`，`+1631/-29`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响插件安装、注册、工具插件或云部署插件
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/.prettierignore` | +15/-0 | 其他 | 新增文件；逻辑 hunk 调整 |
  | `console/src/api/modules/tools.ts` | +36/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface ToolConfigField {；新增配置/字段：name: string;；label: string;；type: "text" \| "password" \| "number" \| "boolean" \| "select" \| "textarea";；required: boolean; |
  | `console/src/locales/en.json` | +6/-1 | 前端国际化 | 修改文件；新增文案 key："asyncExecutionDisabled": "Async execution disabled",；"configure": "Configure",；"configured": "Configured",；"requiresConfig": "Requires configuration",；"configSaved": "Configuration saved", |
  | `console/src/locales/ja.json` | +6/-1 | 前端国际化 | 修改文件；新增文案 key："asyncExecutionDisabled": "非同期実行が無効です",；"configure": "設定",；"configured": "設定済み",；"requiresConfig": "設定が必要です",；"configSaved": "設定を保存しました", |
  | `console/src/locales/ru.json` | +6/-1 | 前端国际化 | 修改文件；新增文案 key："asyncExecutionDisabled": "Асинхронное выполнение отключено",；"configure": "Настроить",；"configured": "Настроено",；"requiresConfig": "Требуется настройка",；"configSaved": "Конфигурация сохранена", |
  | `console/src/locales/zh.json` | +6/-1 | 前端国际化 | 修改文件；新增文案 key："asyncExecutionDisabled": "异步执行已禁用",；"configure": "配置",；"configured": "已配置",；"requiresConfig": "需要配置",；"configSaved": "配置已保存", |
  | `console/src/pages/Agent/Tools/index.module.less` | +15/-0 | 前端页面 | 修改文件；新增配置/字段：margin: 8px 0;；color: rgba(20, 184, 166, 1);；color: #ff7f16; |
  | `console/src/pages/Agent/Tools/index.tsx` | +185/-2 | 前端页面 | 修改文件；新增/修改符号：function ToolConfigModal({；const handleSave = async () => {；const values = await form.validateFields();；const renderInput = () => {；新增配置/字段：tool: ToolInfo;；visible: boolean;；onClose: () => void;；onSave: (values: Record<string, any>) => Promise<void>; |
  | `console/src/pages/Agent/Tools/useTools.ts` | +16/-0 | 前端页面 | 修改文件；新增/修改符号：const saveToolConfig = useCallback( |
  | `plugins/tool/gpt-image2/README.md` | +103/-0 | 插件 | 新增文件；文档或提示词文本调整 |
  | `plugins/tool/gpt-image2/plugin.json` | +49/-0 | 插件 | 新增文件；新增配置/字段："id": "gpt-image2-tool",；"name": "GPT Image 2 Tool",；"version": "1.0.0",；"description": "Generate images using OpenAI GPT Image 2 model", |
  | `plugins/tool/gpt-image2/plugin.py` | +133/-0 | 插件 | 新增文件；新增/修改符号：class GPTImage2ToolPlugin:；def register(self, api: PluginApi):；def _register_tool(self):；新增配置/字段：Args:；api: PluginApi instance；try:；try: |
  | `plugins/tool/gpt-image2/requirements.txt` | +1/-0 | 插件 | 新增文件；逻辑 hunk 调整 |
  | `plugins/tool/gpt-image2/tool.py` | +275/-0 | 插件 | 新增文件；新增/修改符号：async def generate_image_gpt(；def _get_tool_config() -> Optional[dict]:；新增配置/字段：prompt: str,；size: str = "1024x1024",；quality: str = "auto",；Args: |
  | `src/qwenpaw/agents/react_agent.py` | +38/-4 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/app/routers/tools.py` | +229/-17 | 后端 API 路由 | 修改文件；新增/修改符号：class ToolConfigFieldType(str, Enum):；class ToolConfigField(BaseModel):；class ToolConfigUpdate(BaseModel):；async def get_tool_config(；新增配置/字段：name: str = Field(..., description="Field name")；label: str = Field(..., description="Display label")；type: ToolConfigFieldType = Field(；required: bool = Field( |
  | `src/qwenpaw/cli/plugin_commands.py` | +178/-0 | 其他 | 修改文件；新增/修改符号：def _sync_tool_plugin_to_agents(manifest: dict):；def _remove_tool_plugin_from_agents(manifest: dict):；新增配置/字段：Args:；manifest: Plugin manifest dictionary；try:；else: |
  | `src/qwenpaw/config/config.py` | +39/-2 | 配置/常量 | 修改文件；新增配置/字段：config: Dict[str, Any] = Field(；try: |
  | ... |  |  | 另有 7 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [37] `5edeef4` feat(console): Add "Enable" and "Disable" buttons to the batch operation of skills (#4091)

- **完整 SHA**：`5edeef4c5acd1a989dfb9fb14a5e9ab0b52847df`
- **日期/作者**：`2026-05-07` / `zhaozhuang521`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`10 文件`，`+183/-3`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响技能导入、加载、路径规范化或技能池存储
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/skill.ts` | +18/-1 | 前端 API/types | 修改文件；新增配置/字段：results: Record<；method: "POST",；body: JSON.stringify(skillNames),；batchDisableSkills: (skillNames: string[]) => |
  | `console/src/locales/en.json` | +8/-0 | 前端国际化 | 修改文件；新增文案 key："batchEnable": "Enable",；"batchDisable": "Disable",；"batchEnableSuccess": "{{count}} skills enabled",；"batchEnablePartial": "{{enabled}} enabled, {{failed}} failed",；"batchEnableFailed": "Batch enable failed", |
  | `console/src/locales/ja.json` | +8/-0 | 前端国际化 | 修改文件；新增文案 key："batchEnable": "有効化",；"batchDisable": "無効化",；"batchEnableSuccess": "{{count}}個のスキルを有効にしました",；"batchEnablePartial": "{{enabled}}個有効化、{{failed}}個失敗",；"batchEnableFailed": "一括有効化に失敗しました", |
  | `console/src/locales/pt-BR.json` | +8/-0 | 前端国际化 | 修改文件；新增文案 key："batchEnable": "Ativar",；"batchDisable": "Desativar",；"batchEnableSuccess": "{{count}} skills ativadas",；"batchEnablePartial": "{{enabled}} ativadas, {{failed}} falharam",；"batchEnableFailed": "Falha ao ativar em lote", |
  | `console/src/locales/ru.json` | +8/-0 | 前端国际化 | 修改文件；新增文案 key："batchEnable": "Включить",；"batchDisable": "Отключить",；"batchEnableSuccess": "{{count}} навыков включено",；"batchEnablePartial": "{{enabled}} включено, {{failed}} не удалось",；"batchEnableFailed": "Не удалось выполнить пакетное включение", |
  | `console/src/locales/zh.json` | +8/-0 | 前端国际化 | 修改文件；新增文案 key："batchEnable": "启用",；"batchDisable": "禁用",；"batchEnableSuccess": "已启用 {{count}} 个技能",；"batchEnablePartial": "{{enabled}} 个已启用，{{failed}} 个失败",；"batchEnableFailed": "批量启用失败", |
  | `console/src/pages/Agent/Skills/components/HeaderActions.tsx` | +20/-0 | 前端页面 | 修改文件；新增配置/字段：onBatchEnable: () => void;；onBatchDisable: () => void; |
  | `console/src/pages/Agent/Skills/index.tsx` | +4/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Agent/Skills/useSkillsPage.tsx` | +86/-0 | 前端页面 | 修改文件；新增/修改符号：const checkScanWarnings = async (skillName: string) => {；const handleBatchEnable = async () => {；const names = Array.from(selectedSkills);；const entries = Object.entries(results);；新增配置/字段：enabled: names.length - failed.length,；failed: failed.length,；disabled: names.length - failed.length,；failed: failed.length, |
  | `src/qwenpaw/app/routers/skills.py` | +15/-2 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [38] `67ff5aa` fix(pack): restore conda packaging tools before conda-pack (#4093)

- **完整 SHA**：`67ff5aa2bf7cdd8af713cc7a415326dd02c6e0bd`
- **日期/作者**：`2026-05-08` / `Jinglin Peng`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+17/-15`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `scripts/pack/build_common.py` | +17/-15 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [39] `d6dbf31` feat(skills): add cli skill test command (#3999)

- **完整 SHA**：`d6dbf317761d04db9a08ea4bca947d54a56127b3`
- **日期/作者**：`2026-05-08` / `JingHou1215`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+70/-1`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/cli/skills_cmd.py` | +70/-1 | 技能系统 | 修改文件；新增/修改符号：def _validate_skill_frontmatter(skill_dir: Path) -> None:；def _resolve_skill_test_dir(skill: str, agent_id: str) -> Path:；def _run_skill_test(skill_dir: Path) -> str:；def test_cmd(skill: str, agent_id: str) -> None:；新增配置/字段：try:；try: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [40] `764c7e8` feat(feishu): surface sender nickname to agent env context (#4098)

- **完整 SHA**：`764c7e8b1792eb9dc1e73a660e933122cfcbe2b4`
- **日期/作者**：`2026-05-08` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+13/-0`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/feishu/channel.py` | +2/-0 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/runner.py` | +6/-0 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/utils.py` | +5/-0 | Agent 核心/执行 | 修改文件；新增配置/字段：user_name: Optional[str] = None,；user_name: Optional human-readable sender name (e.g. IM nickname). |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [41] `e6e0dcd` fix(WeChat): flush WeChat merge buffer immediately for cron sends (#4106)

- **完整 SHA**：`e6e0dcd85b11212d3bf945a724adc295baa03902`
- **日期/作者**：`2026-05-08` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+5/-0`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wechat/channel.py` | +5/-0 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [42] `9fdb426` chore: fix openai version (#4118)

- **完整 SHA**：`9fdb4260d89f4794623de4ee2353dd28b7e948e5`
- **日期/作者**：`2026-05-08` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`1 文件`，`+1/-0`
- **实际影响范围**：
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `pyproject.toml` | +1/-0 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需排除包名、项目名、发布说明等品牌化内容

---

## [43] `3673176` feat(security): add rule level auto deny (#4046)

- **完整 SHA**：`3673176b726dc56df392582bfdc0d23835746c49`
- **日期/作者**：`2026-05-08` / `Ping`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`14 文件`，`+170/-4`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/security.ts` | +1/-0 | 前端 API/types | 修改文件 |
  | `console/src/locales/en.json` | +4/-0 | 前端国际化 | 修改文件；新增文案 key："autoDeny": "Auto Deny",；"autoDenyTooltip": "When enabled, tool calls matching this rule will be automatically denied without requiring manual ap；"autoDenyEnable": "Enable auto deny for this rule",；"autoDenyDisable": "Disable auto deny for this rule", |
  | `console/src/locales/ja.json` | +4/-0 | 前端国际化 | 修改文件；新增文案 key："autoDeny": "自動拒否",；"autoDenyTooltip": "有効にすると、このルールに一致するツール呼び出しは手動承認なしで自動的に拒否されます",；"autoDenyEnable": "このルールの自動拒否を有効にする",；"autoDenyDisable": "このルールの自動拒否を無効にする", |
  | `console/src/locales/ru.json` | +4/-0 | 前端国际化 | 修改文件；新增文案 key："autoDeny": "Автоотказ",；"autoDenyTooltip": "При включении вызовы инструментов, соответствующие этому правилу, будут автоматически отклонены без ；"autoDenyEnable": "Включить автоотказ для этого правила",；"autoDenyDisable": "Отключить автоотказ для этого правила", |
  | `console/src/locales/zh.json` | +4/-0 | 前端国际化 | 修改文件；新增文案 key："autoDeny": "自动拒绝",；"autoDenyTooltip": "启用后，匹配此规则的工具调用将被自动拒绝，无需人工审批",；"autoDenyEnable": "启用此规则的自动拒绝",；"autoDenyDisable": "关闭此规则的自动拒绝", |
  | `console/src/pages/Settings/Security/components/RuleTable.tsx` | +27/-0 | 前端页面 | 修改文件；新增配置/字段：onToggleAutoDeny: (ruleId: string, currentlyAutoDeny: boolean) => void;；title: (；key: "autoDeny",；width: 100, |
  | `console/src/pages/Settings/Security/components/ToolGuardTab.tsx` | +3/-0 | 前端页面 | 修改文件 |
  | `console/src/pages/Settings/Security/index.tsx` | +2/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Settings/Security/useSecurityPage.ts` | +3/-0 | 前端页面 | 修改文件 |
  | `console/src/pages/Settings/Security/useToolGuard.ts` | +36/-1 | 前端页面 | 修改文件；新增/修改符号：const toggleAutoDeny = useCallback(；const next = new Set(prev);；const next = new Set(prev);；新增配置/字段：autoDeny: boolean;；autoDeny: autoDenyRules.has(r.id),；autoDeny: autoDenyRules.has(r.id),；auto_denied_rules: Array.from(autoDenyRules), |
  | `src/qwenpaw/agents/tool_guard_mixin.py` | +26/-1 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/config/config.py` | +1/-0 | 配置/常量 | 修改文件 |
  | `src/qwenpaw/security/tool_guard/engine.py` | +25/-2 | 其他 | 修改文件；新增/修改符号：def auto_denied_rules(self) -> set[str]:；def should_auto_deny_result(self, result: ToolGuardResult \| None) -> bool: |
  | `src/qwenpaw/security/tool_guard/utils.py` | +30/-0 | 其他 | 修改文件；新增/修改符号：def resolve_auto_denied_rules(；新增配置/字段：user_defined: set[str] \| list[str] \| tuple[str, ...] \| None = None,；Priority: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [44] `411603e` feat(cron): add channel-based session isolation for session and share option for cron jobs (#4117)

- **完整 SHA**：`411603eb4afcd51f171e0cf61e414c8954e50846`
- **日期/作者**：`2026-05-08` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`17 文件`，`+145/-44`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响记忆管理、自动记忆或长期记忆配置
  - 影响定时任务、收件箱、消息推送或 session 隔离
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/locales/en.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："runtimeShareSession": "Share Session",；"shareSessionTooltip": "When enabled, shares session with target user. When disabled, each run creates isolated context |
  | `console/src/locales/ja.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："runtimeShareSession": "セッション共有",；"shareSessionTooltip": "有効にすると、対象ユーザーとセッションを共有します。無効にすると、実行ごとに一意のIDで独立したコンテキストを作成します。履歴を必要としない独立したタスクに適しています。デフォルト: 有効", |
  | `console/src/locales/ru.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："runtimeShareSession": "Общая сессия",；"shareSessionTooltip": "При включении используется общая сессия с целевым пользователем. При отключении каждый запуск со |
  | `console/src/locales/zh.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："runtimeShareSession": "共用会话",；"shareSessionTooltip": "开启时，与目标用户共用会话。关闭时，每次运行创建独立的会话上下文，互不影响。适用于不需要记忆历史的独立任务。默认：开启", |
  | `console/src/pages/Control/CronJobs/components/JobDrawer.tsx` | +9/-16 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Control/CronJobs/components/columns.tsx` | +0/-12 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Control/CronJobs/components/constants.ts` | +1/-0 | 前端页面 | 修改文件 |
  | `src/qwenpaw/agents/memory/proactive/proactive_trigger.py` | +2/-0 | 记忆系统 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/memory/proactive/proactive_utils.py` | +6/-0 | 记忆系统 | 修改文件；新增配置/字段：channel: str = "",；"channel": channel, |
  | `src/qwenpaw/app/crons/executor.py` | +18/-5 | 其他 | 修改文件 |
  | `src/qwenpaw/app/crons/models.py` | +7/-0 | 其他 | 修改文件 |
  | `src/qwenpaw/app/runner/api.py` | +1/-0 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/command_dispatch.py` | +4/-0 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/runner.py` | +4/-0 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/session.py` | +72/-9 | Agent 核心/执行 | 修改文件；新增/修改符号：def _get_save_path(；新增配置/字段：session_id: str,；user_id: str,；channel: str = "",；Args: |
  | `src/qwenpaw/cli/cron_cmd.py` | +12/-2 | 其他 | 修改文件；新增配置/字段：share_session: bool = True,；"share_session": share_session,；share_session: bool, |
  | `tests/unit/agents/test_session.py` | +1/-0 | 测试/CI | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [45] `45afb7c` feat: add agent status endpoint with task tracking (#4107)

- **完整 SHA**：`45afb7c89aa0c2c299b1dbad6adfba78a050af8d`
- **日期/作者**：`2026-05-08` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+144/-505`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
  - 删除代码/资源，需确认我方没有依赖
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/routers/agent.py` | +0/-504 | 后端 API 路由 | 删除文件；移除符号：class MdFileInfo(BaseModel):；class MdFileContent(BaseModel):；async def list_working_files( |
  | `src/qwenpaw/app/routers/agent_scoped.py` | +3/-0 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/agent_status.py` | +93/-0 | 后端 API 路由 | 新增文件；新增/修改符号：class AgentStatus(BaseModel):；async def get_agent_status(；新增配置/字段：status: Literal["idle", "running", "disabled"] = Field(；running_task_count: int = Field(；last_run_at: Optional[datetime] = Field(；last_finish_at: Optional[datetime] = Field( |
  | `src/qwenpaw/app/runner/task_tracker.py` | +48/-1 | Agent 核心/执行 | 修改文件；新增/修改符号：async def get_global_status(self) -> dict:；新增配置/字段：start_time: Optional[datetime] = None；finish_time: Optional[datetime] = None；Returns:；"status": status, |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [46] `c832082` perf(console,chat): chat performance optimization (#4110)

- **完整 SHA**：`c83208281597438a279fae43f8bfbd2519a33b91`
- **日期/作者**：`2026-05-08` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P1`
- **总体规模**：`3 文件`，`+98/-150`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Chat/components/ChatActionGroup/index.tsx` | +8/-19 | 前端页面 | 修改文件；新增/修改符号：interface ChatActionGroupProps {；const ChatActionGroup: React.FC<ChatActionGroupProps> = ({ |
  | `console/src/pages/Chat/index.tsx` | +58/-118 | 前端页面 | 修改文件；新增/修改符号：const updateCapsIfChanged = useCallback(；const noCaps = {；const prevApprovalKeyRef = useRef("");；const approvalKey = sessionApprovals；新增配置/字段：supportsMultimodal: boolean;；supportsImage: boolean;；supportsVideo: boolean;；supportsMultimodal: false, |
  | `console/src/pages/Chat/sessionApi/index.ts` | +32/-13 | 前端页面 | 修改文件；新增/修改符号：const resolvers = this.realIdResolvers.get(sessionId);；const session = this.sessionList.find((x) => x.id === sessionId) as；const existing = this.realIdResolvers.get(sessionId) \|\| []; |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [47] `b2f9417` fix: use RotatingFileHandler for log rotation on all platforms (#4076)

- **完整 SHA**：`b2f9417982f63dca25c6576fb2b44e3e2379011f`
- **日期/作者**：`2026-05-08` / `MarkWu`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+31/-17`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/utils/logging.py` | +31/-17 | 其他 | 修改文件；新增/修改符号：class _SafeRotatingFileHandler(logging.handlers.RotatingFileHandler):；def doRollover(self): |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [48] `ccea67d` test(console): setup Vitest and add Chat/utils/api unit tests (#3559)

- **完整 SHA**：`ccea67d57c5c6de541a44a5859274761e2425efa`
- **日期/作者**：`2026-05-08` / `Remy he`
- **标签/优先级**：`🟠 待人工` / `P2`
- **总体规模**：`31 文件`，`+4145/-424`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `.github/workflows/frontend-tests.yml` | +49/-0 | 测试/CI | 新增文件；新增配置/字段：name: Frontend Tests；on:；push:；branches: [main, master, dev, develop] |
  | `console/.gitignore` | +3/-0 | 其他 | 新增文件；逻辑 hunk 调整 |
  | `console/.npmrc` | +1/-0 | 其他 | 新增文件；逻辑 hunk 调整 |
  | `console/package-lock.json` | +1263/-421 | 其他 | 修改文件；新增配置/字段："jsdom": "^29.0.2",；"vite": "^6.3.5",；"vitest": "^4.1.4"；"version": "4.4.4", |
  | `console/package.json` | +10/-2 | 其他 | 修改文件；新增配置/字段："test": "vitest",；"jsdom": "^29.0.2",；"vite": "^6.3.5",；"vitest": "^4.1.4" |
  | `console/src/api/config.test.ts` | +76/-0 | 前端 API/types | 新增文件；新增/修改符号：const setViteBase = (v: string) => {；const setToken = (v: string) => { |
  | `console/src/api/modules/auth.test.ts` | +149/-0 | 前端 API/types | 新增文件；新增/修改符号：function mockFetch(status: number, body: unknown) {；const result = await authApi.login("alice", "pass");；const body = JSON.parse((fetch as any).mock.calls[0][1].body);；const result = await authApi.register("bob", "pass123");；新增配置/字段：getApiUrl: (path: string) => `/api${path}`,；ok: status >= 200 && status < 300,；statusText: status === 200 ? "OK" : "Bad Request",；json: () => Promise.resolve(body), |
  | `console/src/api/modules/chat.test.ts` | +205/-0 | 前端 API/types | 新增文件；新增/修改符号：const result = chatApi.filePreviewUrl("img.png");；const result = chatApi.filePreviewUrl("/img.png");；const result = chatApi.filePreviewUrl("img.png");；const result = chatApi.filePreviewUrl("img.png");；新增配置/字段：getApiUrl: (path: string) => `/api${path}`,；getApiToken: vi.fn(() => ""),；buildAuthHeaders: vi.fn(() => ({})),；ok: true, |
  | `console/src/api/modules/provider.test.ts` | +85/-0 | 前端 API/types | 新增文件；新增/修改符号：const body = {；新增配置/字段：request: vi.fn(),；scope: "effective",；agent_id: "agent-1",；provider_id: "openai", |
  | `console/src/api/request.test.ts` | +157/-0 | 前端 API/types | 新增文件；新增/修改符号：function mockFetch(；const responseBody =；const headers: Headers = (fetch as any).mock.calls[0][1].headers;；const headers: Headers = (fetch as any).mock.calls[0][1].headers;；新增配置/字段：getApiUrl: (path: string) => `/api${path}`,；getApiToken: vi.fn(() => ""),；clearAuthToken: vi.fn(),；buildAuthHeaders: vi.fn(() => ({})), |
  | `console/src/components/AgentSelector/AgentSelector.test.tsx` | +80/-0 | 前端组件 | 新增文件；新增/修改符号：const actual = await importOriginal<typeof import("react-router-dom")>();；const mockAgentsData = {；const sortedAgents = mockSetAgents.mock.calls[0][0];；新增配置/字段：mockSetSelectedAgent: vi.fn(),；mockSetAgents: vi.fn(),；mockListAgents: vi.fn(),；mockNavigate: vi.fn(), |
  | `console/src/components/LanguageSwitcher/LanguageSwitcher.test.tsx` | +86/-0 | 前端组件 | 新增文件；新增/修改符号：const user = userEvent.setup();；const user = userEvent.setup();；const user = userEvent.setup();；新增配置/字段：mockChangeLanguage: vi.fn(),；mockUpdateLanguage: vi.fn().mockResolvedValue(undefined),；useTranslation: () => ({；i18n: { |
  | `console/src/components/PageHeader/PageHeader.test.tsx` | +61/-0 | 前端组件 | 新增文件；逻辑 hunk 调整 |
  | `console/src/components/SkillVisual/SkillVisual.test.tsx` | +49/-0 | 前端组件 | 新增文件；新增/修改符号：const cases: [string, string][] = [ |
  | `console/src/components/ThemeToggleButton/ThemeToggleButton.test.tsx` | +51/-0 | 前端组件 | 新增文件；新增/修改符号：function renderWithTheme(mode: "light" \| "dark" \| "system" = "light") { |
  | `console/src/pages/Chat/ChatPage.test.tsx` | +364/-0 | 前端页面 | 新增文件；新增/修改符号：const actual = await importOriginal<typeof import("antd")>();；const mockActiveModel = {；const mockProviders = [；const response = await capturedOptions.api.fetch({；新增配置/字段：mockListProviders: vi.fn(),；mockGetActiveModels: vi.fn(),；mockUploadFile: vi.fn(),；mockFilePreviewUrl: vi.fn((f: string) => `/preview/${f}`), |
  | `console/src/pages/Chat/ModelSelector/ModelSelector.test.tsx` | +197/-0 | 前端页面 | 新增文件；新增/修改符号：const mockProvider = {；const mockActiveModels = {；function setupDefaultMocks() {；const user = userEvent.setup();；新增配置/字段：providerApi: {；listProviders: vi.fn(),；getActiveModels: vi.fn(),；setActiveLlm: vi.fn(), |
  | `console/src/pages/Chat/components/ChatActionGroup/ChatActionGroup.test.tsx` | +27/-0 | 前端页面 | 新增文件；逻辑 hunk 调整 |
  | ... |  |  | 另有 13 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [49] `9a03dd1` test(console): frontend test (#4121)

- **完整 SHA**：`9a03dd16baef3678091afafe124ff7185a706f1f`
- **日期/作者**：`2026-05-08` / `zhaozhuang521`
- **标签/优先级**：`⚪ 跳过-无关` / `P3`
- **总体规模**：`1 文件`，`+8/-2`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/utils/utils.test.ts` | +8/-2 | 其他 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [50] `97d2f3a` feat(doctor): add Windows environment diagnostics (#4032)

- **完整 SHA**：`97d2f3a512a4131aa1bb625ab8ab1c9f4fbb69c3`
- **日期/作者**：`2026-05-08` / `Wei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+104/-0`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/cli/doctor_checks.py` | +97/-0 | 其他 | 修改文件；新增/修改符号：def _windows_long_paths_enabled() -> tuple[bool \| None, str \| None]:；def _powershell_language_mode(；def windows_environment_lines() -> list[str]:；新增配置/字段：try:；try:；executable: str,；try: |
  | `src/qwenpaw/cli/doctor_cmd.py` | +7/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

# 逐 commit 代码影响分析（第 5 批）

> 范围：第 101 - 125 条。此文档基于 diff 提取，重点回答“commit 了什么、影响哪里”。

## [101] `7e82329` feat(plugins): add Qwen-Image and Wan 2.7 plugins (#4248)

- **完整 SHA**：`7e823295ca40c7d2212246628913c5c5616b48af`
- **日期/作者**：`2026-05-12` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`20 文件`，`+3206/-874`
- **实际影响范围**：
  - 影响插件安装、注册、工具插件或云部署插件
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
  - 删除代码/资源，需确认我方没有依赖
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Agent/Tools/index.tsx` | +95/-76 | 前端页面 | 修改文件；新增/修改符号：const renderInput = () => {；新增配置/字段：default:；required: field.required,；message: `${field.label} is required`, |
  | `console/src/pages/Agent/Tools/useTools.ts` | +9/-8 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `plugins/tool/gpt-image2/gpt_image2.py` | +63/-0 | 插件 | 新增文件；新增/修改符号：def _load_tool_module():；class GPTImage2ToolPlugin:；def register(self, api: PluginApi):；新增配置/字段：Args:；api: PluginApi instance. |
  | `plugins/tool/gpt-image2/gpt_image2_tool.py` | +574/-0 | 插件 | 新增文件；新增/修改符号：async def generate_image_gpt(；async def edit_image_gpt(  # pylint: disable=too-many-statements；def _process_image_url(image_path: str) -> dict:；新增配置/字段：prompt: str,；size: str = "1024x1024",；quality: str = "auto",；Args: |
  | `plugins/tool/gpt-image2/plugin.json` | +2/-2 | 插件 | 修改文件；新增配置/字段："version": "1.1.1",；"backend": "gpt_image2.py" |
  | `plugins/tool/gpt-image2/plugin.py` | +0/-159 | 插件 | 删除文件；移除符号：class GPTImage2ToolPlugin:；def register(self, api: PluginApi):；def _register_tool(self): |
  | `plugins/tool/gpt-image2/tool.py` | +0/-611 | 插件 | 删除文件；移除符号：async def generate_image_gpt(；async def edit_image_gpt(  # pylint: disable=too-many-statements；def _process_image_url(image_path: str) -> dict: |
  | `plugins/tool/qwen-image/README.md` | +89/-0 | 插件 | 新增文件；文档或提示词文本调整 |
  | `plugins/tool/qwen-image/plugin.json` | +128/-0 | 插件 | 新增文件；新增配置/字段："id": "qwen-image-tool",；"name": "Qwen-Image Tool",；"version": "1.0.0",；"description": "Generate and edit images using Alibaba Qwen-Image models", |
  | `plugins/tool/qwen-image/qwen_image.py` | +62/-0 | 插件 | 新增文件；新增/修改符号：def _load_tool_module():；class QwenImageToolPlugin:；def register(self, api: PluginApi):；新增配置/字段：Args:；api: PluginApi instance. |
  | `plugins/tool/qwen-image/qwen_image_tool.py` | +734/-0 | 插件 | 新增文件；新增/修改符号：def _resolve_image_url(path_or_url: str) -> str:；def _extract_config(；async def _download_image(；def _call_multimodal_conversation(；新增配置/字段：".png": "image/png",；".jpg": "image/jpeg",；".jpeg": "image/jpeg",；".webp": "image/webp", |
  | `plugins/tool/qwen-image/requirements.txt` | +2/-0 | 插件 | 新增文件；逻辑 hunk 调整 |
  | `plugins/tool/wan27/README.md` | +90/-0 | 插件 | 新增文件；文档或提示词文本调整 |
  | `plugins/tool/wan27/plugin.json` | +121/-0 | 插件 | 新增文件；新增配置/字段："id": "wan27-tool",；"name": "Wan 2.7 Video Generation Tool",；"version": "1.0.0",；"description": "Generate videos using Alibaba Wan 2.7 models (text-to-video, image-to-video, reference-to-video)", |
  | `plugins/tool/wan27/requirements.txt` | +2/-0 | 插件 | 新增文件；逻辑 hunk 调整 |
  | `plugins/tool/wan27/wan27.py` | +69/-0 | 插件 | 新增文件；新增/修改符号：def _load_tool_module():；class Wan27ToolPlugin:；def register(self, api: PluginApi):；新增配置/字段：Args:；api: PluginApi instance. |
  | `plugins/tool/wan27/wan27_tool.py` | +944/-0 | 插件 | 新增文件；新增/修改符号：def _resolve_image_url(path_or_url: str) -> str:；def _extract_config(；async def _download_video(；def _call_video_synthesis(；新增配置/字段：".png": "image/png",；".jpg": "image/jpeg",；".jpeg": "image/jpeg",；".webp": "image/webp", |
  | `src/qwenpaw/app/routers/tools.py` | +66/-16 | 后端 API 路由 | 修改文件；新增/修改符号：def _build_tool_info(tool_config: Any, tool_name: str) -> ToolInfo:；新增配置/字段：Args:；tool_config: BuiltinToolConfig instance；tool_name: Tool function name；Returns: |
  | ... |  |  | 另有 2 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [102] `a82ce8d` feat(plugins): enable register FastAPI APIRouter instances through plugin (#4255)

- **完整 SHA**：`a82ce8dca9ac62c7c2e48e3ab7ea1a74f17fcb02`
- **日期/作者**：`2026-05-13` / `Osier-Yi`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`5 文件`，`+565/-4`
- **实际影响范围**：
  - 影响插件安装、注册、工具插件或云部署插件
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/_app.py` | +6/-2 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/plugins/api.py` | +32/-1 | 插件 | 修改文件；新增/修改符号：def register_http_router(；新增配置/字段：router: Any,；prefix: str,；tags: Optional[List[str]] = None,；Args: |
  | `src/qwenpaw/plugins/registry.py` | +177/-1 | 插件 | 修改文件；新增/修改符号：def _find_console_spa_route_index(app: Any) -> Optional[int]:；def _mount_plugin_http_on_app(；class HttpRouterRegistration:；class PluginRegistry:  # pylint:disable=too-many-public-methods；新增配置/字段：app: Any,；router: APIRouter,；full_path_prefix: str,；tags: Optional[List[Any]], |
  | `website/public/docs/plugins.en.md` | +179/-0 | 文档/发布 | 修改文件；新增/修改符号：class Pet(BaseModel):；class PetCreate(BaseModel):；def build_router() -> APIRouter:；def list_pets() -> List[Pet]:；新增配置/字段："id": "pet-api-plugin",；"name": "Pet API Plugin",；"version": "1.0.0",；"description": "Expose a small REST API under /api/pets", |
  | `website/public/docs/plugins.zh.md` | +171/-0 | 文档/发布 | 修改文件；新增/修改符号：class Pet(BaseModel):；class PetCreate(BaseModel):；def build_router() -> APIRouter:；def list_pets() -> List[Pet]:；新增配置/字段："id": "pet-api-plugin",；"name": "Pet API Plugin",；"version": "1.0.0",；"description": "Expose a small REST API under /api/pets", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [103] `5bc599a` feat: add timeout for keyring (#4263)

- **完整 SHA**：`5bc599a7d6aa16883f531dc4232002ba2a041498`
- **日期/作者**：`2026-05-13` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+89/-9`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/security/secret_store.py` | +89/-9 | 其他 | 修改文件；新增/修改符号：def _call_with_timeout(fn, timeout):；def _worker():；def _get():；def _set():；新增配置/字段：Note:；try:；finally: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [104] `cb8a8d7` feat(console): support crosses year in TokenUsage (#4268)

- **完整 SHA**：`cb8a8d7f267adec00a2a54ae4f8ca01521233465`
- **日期/作者**：`2026-05-13` / `zhaozhuang521`
- **标签/优先级**：`✅ 直接合入` / `P1`
- **总体规模**：`3 文件`，`+32/-13`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Settings/AgentStats/index.tsx` | +28/-11 | 前端页面 | 修改文件；新增/修改符号：function formatDateLabel(dateStr: string, crossesYear: boolean): string {；const date = dayjs(dateStr);；const crossesYear = useMemo(；新增配置/字段：crossesYear: boolean,；date: d.date,；axis: {；x: { |
  | `console/src/pages/Settings/TokenUsage/hooks/useModelTrendConfig.ts` | +2/-1 | 前端页面 | 修改文件；新增/修改符号：const crossesYear = startDate.year() !== endDate.year(); |
  | `console/src/pages/Settings/TokenUsage/hooks/useTokenTypeConfig.ts` | +2/-1 | 前端页面 | 修改文件；新增/修改符号：const crossesYear = startDate.year() !== endDate.year(); |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [105] `5dfe1ca` refactor(console): console/PluginManager (#4266)

- **完整 SHA**：`5dfe1caf7437b23dafa1f790d9567f57e1f8698b`
- **日期/作者**：`2026-05-13` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P2`
- **总体规模**：`7 文件`，`+486/-433`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Settings/PluginManager/components/InstallPluginModal.tsx` | +149/-0 | 前端页面 | 新增文件；新增/修改符号：type InstallModalProps = ReturnType<typeof useInstallModal>;；export function InstallPluginModal({ |
  | `console/src/pages/Settings/PluginManager/components/PluginTypeTag.tsx` | +59/-0 | 前端页面 | 新增文件；新增/修改符号：const PLUGIN_TYPE_CONFIG: Record<；export function PluginTypeTag({ type }: { type: PluginType }) {；const cfg = PLUGIN_TYPE_CONFIG[type] ?? PLUGIN_TYPE_CONFIG.general;；新增配置/字段：tool: {；label: "Tool",；color: "blue",；icon: <Wrench size={11} />, |
  | `console/src/pages/Settings/PluginManager/hooks/useInstallModal.ts` | +173/-0 | 前端页面 | 新增文件；新增/修改符号：export function useInstallModal(onSuccess: () => void) {；const fileInputRef = useRef<HTMLInputElement>(null);；const cancel = () => setDragOver(false);；const openModal = useCallback(() => setInstallOpen(true), []); |
  | `console/src/pages/Settings/PluginManager/hooks/usePluginManager.ts` | +58/-0 | 前端页面 | 新增文件；新增/修改符号：export function usePluginManager() {；const handleUninstall = useCallback(；const msg =；新增配置/字段：data: plugins,；onError: () => message.error(t("pluginManager.loadFailed")),；title: t("pluginManager.confirmTitle"),；content: t("pluginManager.uninstallConfirm", { name: plugin.name }), |
  | `console/src/pages/Settings/PluginManager/index.module.less` | +0/-1 | 前端页面 | 修改文件；样式/布局调整 |
  | `console/src/pages/Settings/PluginManager/index.tsx` | +11/-432 | 前端页面 | 修改文件；新增/修改符号：const installModal = useInstallModal(refresh); |
  | `console/src/pages/Settings/PluginManager/utils.ts` | +36/-0 | 前端页面 | 新增文件；新增/修改符号：const result: Array<{ path: string; file: File }> = [];；const reader = entry.createReader();；const readBatch = (): Promise<FileSystemEntry[]> =>；const file = await new Promise<File>((resolve, reject) =>；新增配置/字段：entry: FileSystemDirectoryEntry,；kind: "folder";；name: string;；entries: Array<{ path: string; file: File }>; |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [106] `475fe26` feat(mcp): add OAuth 2.1 PKCE support for remote MCP servers (#4256)

- **完整 SHA**：`475fe269be52bc605624ad9de8a5e2ad85f5ff75`
- **日期/作者**：`2026-05-13` / `Weirui Kuang`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`20 文件`，`+2120/-107`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响 MCP 工具连接生命周期、超时、OAuth 或清理逻辑
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/modules/mcp.ts` | +33/-0 | 前端 API/types | 修改文件；新增配置/字段：startOAuth: (clientKey: string, body: MCPOAuthStartRequest) =>；method: "POST",；body: JSON.stringify(body),；getOAuthStatus: (clientKey: string) => |
  | `console/src/api/types/mcp.ts` | +39/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface MCPClientOAuthStatus {；export interface MCPOAuthStartRequest {；export interface MCPOAuthStartResponse {；export interface MCPOAuthStatusResponse {；新增配置/字段：authorized: boolean;；expires_at: number;；scope: string;；client_id: string; |
  | `console/src/locales/en.json` | +50/-1 | 前端国际化 | 修改文件；新增文案 key："toolSchema": "Input Schema",；"tab": {；"json": "JSON Import",；"form": "Form Mode"；"form": { |
  | `console/src/locales/id.json` | +28/-1 | 前端国际化 | 修改文件；新增文案 key："toolSchema": "Skema Input",；"oauth": {；"enableOAuth": "Gunakan Otorisasi OAuth",；"manage": "OAuth",；"authorized": "Telah Diotorisasi", |
  | `console/src/locales/ja.json` | +28/-1 | 前端国际化 | 修改文件；新增文案 key："toolSchema": "入力スキーマ",；"oauth": {；"enableOAuth": "OAuth 認証を使用する",；"manage": "OAuth",；"authorized": "認証済み", |
  | `console/src/locales/pt-BR.json` | +28/-1 | 前端国际化 | 修改文件；新增文案 key："toolSchema": "Input Schema",；"oauth": {；"enableOAuth": "Usar autorização OAuth",；"manage": "OAuth",；"authorized": "Autorizado", |
  | `console/src/locales/ru.json` | +28/-1 | 前端国际化 | 修改文件；新增文案 key："toolSchema": "Схема ввода",；"oauth": {；"enableOAuth": "Использовать OAuth авторизацию",；"manage": "OAuth",；"authorized": "Авторизован", |
  | `console/src/locales/zh.json` | +50/-1 | 前端国际化 | 修改文件；新增文案 key："toolSchema": "输入参数",；"tab": {；"json": "JSON 导入",；"form": "表单模式"；"form": { |
  | `console/src/pages/Agent/MCP/components/MCPClientCard.tsx` | +148/-13 | 前端页面 | 修改文件；新增/修改符号：const oauthStatus = client.oauth_status;；const now = Date.now() / 1000;；const isOauthAuthorized =；const isOauthExpired =；新增配置/字段：display: "flex",；alignItems: "center",；gap: 6,；minWidth: 0, |
  | `console/src/pages/Agent/MCP/components/MCPOAuthSection.tsx` | +501/-0 | 前端页面 | 新增文件；新增/修改符号：interface MCPOAuthSectionProps {；type OAuthPhase =；const OAUTH_MESSAGE_TYPE = "mcp-oauth";；export const MCPOAuthSection: React.FC<MCPOAuthSectionProps> = ({；新增配置/字段：url: string;；client_id: clientId,；auth_endpoint: authEndpoint,；token_endpoint: tokenEndpoint, |
  | `console/src/pages/Agent/MCP/components/index.ts` | +1/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Agent/MCP/index.module.less` | +18/-9 | 前端页面 | 修改文件；新增配置/字段：gap: 8px;；padding: 6px 10px;；overflow: hidden;；padding: 6px 10px; |
  | `console/src/pages/Agent/MCP/index.tsx` | +339/-73 | 前端页面 | 修改文件；新增/修改符号：function normalizeClientData(key: string, rawData: Record<string, unknown>) {；const defaultForm = {；const setField = useCallback(；const resetModal = useCallback(() => {；新增配置/字段：name: (rawData.name as string) \|\| key,；description: (rawData.description as string) \|\| "",；enabled:；url: (rawData.url \|\| rawData.baseUrl \|\| "") as string, |
  | `console/src/pages/Agent/MCP/useMCP.ts` | +1/-0 | 前端页面 | 修改文件 |
  | `src/qwenpaw/app/mcp/manager.py` | +35/-3 | MCP | 修改文件；新增/修改符号：def _inject_oauth_token(；新增配置/字段：headers: dict,；client_config: "MCPClientConfig",；headers: dict = dict(client_config.headers or {}) |
  | `src/qwenpaw/app/mcp/stateful_client.py` | +33/-1 | MCP | 修改文件；新增/修改符号：def _is_401_error(exc: BaseException) -> bool:；async def _run_lifecycle(self) -> None:  # noqa: C901 |
  | `src/qwenpaw/app/routers/__init__.py` | +2/-0 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/mcp.py` | +37/-2 | 后端 API 路由 | 修改文件；新增/修改符号：class MCPClientOAuthStatus(BaseModel):；def _build_oauth_status(；新增配置/字段：authorized: bool = False；expires_at: float = 0.0；scope: str = ""；client_id: str = "" |
  | ... |  |  | 另有 2 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [107] `207c278` fix(console): replace window.open calls with openExternalLink utility in ACPDrawer and ChannelDrawer components (#4270)

- **完整 SHA**：`207c278569c1fa2d57c321069e50e2e50eea8b07`
- **日期/作者**：`2026-05-13` / `zhijianma`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`3 文件`，`+29/-11`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Agent/ACP/components/ACPDrawer.tsx` | +2/-7 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +3/-4 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/utils/openExternalLink.ts` | +24/-0 | 其他 | 新增文件；新增/修改符号：export function openExternalLink(；const pywebview = (window as any).pywebview;；新增配置/字段：url: string,；target: string = "_blank",；features: string = "noopener,noreferrer", |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [108] `af50cf7` style: sidebar (#4273)

- **完整 SHA**：`af50cf7ae62dbd759ede81d60b6063ed47c3738a`
- **日期/作者**：`2026-05-13` / `zhaozhuang521`
- **标签/优先级**：`⚪ 跳过-无关` / `P3`
- **总体规模**：`1 文件`，`+1/-0`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/layouts/index.module.less` | +1/-0 | 前端布局 | 修改文件；样式/布局调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [109] `dc2ce24` feat(channel): add streaming output hooks to BaseChannel with WeCom support (#4271)

- **完整 SHA**：`dc2ce2423b67eef9315e6c02d8986dcedeab3d6e`
- **日期/作者**：`2026-05-13` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`10 文件`，`+436/-15`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 影响多语言文案，需要校验中文“数字员工”等术语
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/channel.ts` | +1/-0 | 前端 API/types | 修改文件；逻辑 hunk 调整 |
  | `console/src/locales/en.json` | +1/-0 | 前端国际化 | 修改文件；新增文案 key："streamingEnabled": "Streaming Output", |
  | `console/src/locales/ja.json` | +1/-0 | 前端国际化 | 修改文件；新增文案 key："streamingEnabled": "ストリーミング出力", |
  | `console/src/locales/pt-BR.json` | +1/-0 | 前端国际化 | 修改文件；新增文案 key："streamingEnabled": "Saída em Streaming", |
  | `console/src/locales/ru.json` | +1/-0 | 前端国际化 | 修改文件；新增文案 key："streamingEnabled": "Потоковый вывод", |
  | `console/src/locales/zh.json` | +1/-0 | 前端国际化 | 修改文件；新增文案 key："streamingEnabled": "流式输出", |
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +10/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/base.py` | +245/-15 | 后端渠道实现 | 修改文件；新增/修改符号：def _resolve_stream_type(self, event: Any) -> str:；async def _dispatch_streaming_event(；async def _on_stream_msg_start(；async def _on_stream_content_delta(；新增配置/字段：streaming_enabled: bool = False；streaming_enabled: bool = False,；request: "AgentRequest",；to_handle: str, |
  | `src/qwenpaw/app/channels/wecom/channel.py` | +174/-0 | 后端渠道实现 | 修改文件；新增/修改符号：class _SdkLoggerAdapter:；def __init__(self, std_logger: logging.Logger) -> None:；def debug(self, message: str, *args: object) -> None:；def info(self, message: str, *args: object) -> None:；新增配置/字段：streaming_enabled: bool = False,；send_meta: Dict[str, Any],；try:；send_meta: Dict[str, Any], |
  | `src/qwenpaw/config/config.py` | +1/-0 | 配置/常量 | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [110] `b1770de` Fix(tool): read_file_safe allocation size (#4272)

- **完整 SHA**：`b1770de60115dfb330b10cdb0d6b96b8cf5af64d`
- **日期/作者**：`2026-05-13` / `suntp`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+86/-2`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/utils.py` | +6/-2 | 工具实现 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/agents/tools/test_utils.py` | +80/-0 | 工具实现 | 新增文件；新增/修改符号：class _FakeAsyncFile:；def __init__(self, reads: list[int], content: str = "ok"):；async def __aenter__(self):；async def __aexit__(self, exc_type, exc, tb):；新增配置/字段：reads: list[int] = []；reads: list[int] = [] |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [111] `503390d` perf(tools): reduce maximum file read size to 200MB (#4276)

- **完整 SHA**：`503390d7462a2c7705b387f39ed7a21ed736c13c`
- **日期/作者**：`2026-05-13` / `jinliyl`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+2/-82`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
  - 删除代码/资源，需确认我方没有依赖
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/utils.py` | +2/-2 | 工具实现 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/agents/tools/test_utils.py` | +0/-80 | 工具实现 | 删除文件；移除符号：class _FakeAsyncFile:；def __init__(self, reads: list[int], content: str = "ok"):；async def __aenter__(self): |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [112] `af65842` fix(QA agent): package website/public/docs into wheel and sdist (#4275)

- **完整 SHA**：`af658424d38ef4c91bdcfbe1257777cb41708055`
- **日期/作者**：`2026-05-13` / `lalaliat`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
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

## [113] `67cb469` Feat(tool): Add action="file_download" for browser use (#4261)

- **完整 SHA**：`67cb46997ef2d9e4452d6b0307d6bbd575c02391`
- **日期/作者**：`2026-05-13` / `x1n95c`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+525/-16`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/browser_control.py` | +525/-16 | 工具实现 | 修改文件；新增/修改符号：def _safe_download_filename(filename: Any, default: str = "download") -> str:；class DirectUrlDownloadRejectedError(ValueError):；def __init__(；def _browser_output_dir(state: dict, name: str) -> Path:；新增配置/字段：reason: str,；content_length: int \| None = None,；status: int \| None = None,；try: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [114] `9f49c91` feat(cron & inbox): add inbox and optimize the cron job (#4210)

- **完整 SHA**：`9f49c911afedcdf4f0fbfbd7a0e7d622344aa1e3`
- **日期/作者**：`2026-05-13` / `lalaliat`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`74 文件`，`+8438/-328`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
  - 影响技能导入、加载、路径规范化或技能池存储
  - 影响定时任务、收件箱、消息推送或 session 隔离
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/index.ts` | +4/-0 | 前端 API/types | 修改文件；逻辑 hunk 调整 |
  | `console/src/api/modules/console.ts` | +69/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface InboxEvent {；export interface InboxTrace {；const query = new URLSearchParams();；const suffix = query.toString() ? `?${query.toString()}` : "";；新增配置/字段：id: string;；agent_id: string;；source_type: string;；source_id: string; |
  | `console/src/api/modules/cronjob.ts` | +20/-0 | 前端 API/types | 修改文件；新增/修改符号：const searchParams = new URLSearchParams();；const query = searchParams.toString();；新增配置/字段：getCronJobHistory: (jobId: string) =>；listCronDispatchTargets: (params?: { |
  | `console/src/api/modules/heartbeat.ts` | +5/-0 | 前端 API/types | 修改文件；新增配置/字段：runHeartbeatNow: () =>；method: "POST", |
  | `console/src/api/types/cronjob.ts` | +32/-1 | 前端 API/types | 修改文件；新增/修改符号：export interface CronJobScheduleCron {；export interface CronJobScheduleOnce {；export type CronJobSchedule = CronJobScheduleCron \| CronJobScheduleOnce;；export interface CronJobExecutionRecord {；新增配置/字段：type: "once";；run_at: string;；run_at: string;；status: "success" \| "error" \| "running" \| "skipped" \| "cancelled"; |
  | `console/src/components/ApprovalCard/ApprovalCard.module.less` | +22/-0 | 前端组件 | 修改文件；新增配置/字段：padding: 1px 8px;；border: none;；color: #cf1322;；color: #ff7875; |
  | `console/src/components/ApprovalCard/ApprovalCard.tsx` | +116/-32 | 前端组件 | 修改文件；新增/修改符号：const agents = useAgentStore((state) => state.agents);；const agentsById = useMemo(；const isTimedOut = showInboxAgentContext && remaining <= 0;；const executionAgentDisplayName = useMemo(() => { |
  | `console/src/layouts/MainLayout/index.tsx` | +3/-0 | 前端布局 | 修改文件；新增/修改符号：const InboxPage = lazyImportWithRetry("../../pages/Inbox"); |
  | `console/src/layouts/Sidebar.tsx` | +49/-0 | 前端布局 | 修改文件；新增/修改符号：const INBOX_BADGE_POLLING_MS = 6000;；const loadUnreadState = async () => {；const hasUnreadEvents = (inboxRes?.events?.length \|\| 0) > 0;；const hasPendingApprovals =；新增配置/字段：unread_only: true,；limit: 1,；key: "inbox",；icon: inboxIcon(18), |
  | `console/src/layouts/constants.ts` | +2/-0 | 前端布局 | 修改文件；新增配置/字段：inbox: "/inbox",；inbox: "nav.inbox", |
  | `console/src/layouts/index.module.less` | +0/-4 | 前端布局 | 修改文件；样式/布局调整 |
  | `console/src/locales/en.json` | +181/-3 | 前端国际化 | 修改文件；新增文案 key："inbox": "Inbox",；"inbox": {；"title": "Inbox",；"tabApprovals": "Approvals",；"tabPushMessages": "Push Messages", |
  | `console/src/locales/ja.json` | +174/-2 | 前端国际化 | 修改文件；新增文案 key："saveFailed": "ハートビート設定の保存に失敗しました",；"targetInbox": "受信トレイに送信",；"runNow": "今すぐ実行",；"runNowSuccess": "ハートビートを実行しました。受信トレイまたは送信先チャンネルを確認してください。",；"runNowFailed": "ハートビートの実行に失敗しました" |
  | `console/src/locales/pt-BR.json` | +271/-97 | 前端国际化 | 修改文件；新增文案 key："cronJobs": "Tarefas Cron",；"title": "Batimento",；"description": "Execute HEARTBEAT.md em intervalo fixo para autoverificações. Por padrão roda em silêncio sem afetar con；"every": "Intervalo",；"everyRequired": "Obrigatório", |
  | `console/src/locales/ru.json` | +175/-3 | 前端国际化 | 修改文件；新增文案 key："saveFailed": "Не удалось сохранить конфигурацию пульса",；"targetInbox": "Отправлять во входящие",；"runNow": "Запустить сейчас",；"runNowSuccess": "Пульс запущен. Через несколько секунд проверьте входящие или целевой канал.",；"runNowFailed": "Не удалось запустить выполнение пульса" |
  | `console/src/locales/zh.json` | +181/-3 | 前端国际化 | 修改文件；新增文案 key："inbox": "收件箱",；"inbox": {；"title": "收件箱",；"tabApprovals": "审批",；"tabPushMessages": "推送消息", |
  | `console/src/pages/Chat/index.tsx` | +29/-7 | 前端页面 | 修改文件；新增/修改符号：const sessionId = |
  | `console/src/pages/Control/CronJobs/components/JobDrawer.tsx` | +359/-43 | 前端页面 | 修改文件；新增/修改符号：type SelectOption = { value: string; label: string };；const selectedChannel = Form.useWatch(["dispatch", "channel"], form);；const selectedTargetUserId = Form.useWatch(；const mergeOptions = (；新增配置/字段：targetItems: CronDispatchTargetItem[];；targetChannels: string[];；targetsLoading: boolean;；onReloadTargets: () => Promise<void>; |
  | ... |  |  | 另有 56 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [115] `f684c13` bumping version to 1.1.7b2 (#4283)

- **完整 SHA**：`f684c1382499b4000e856c4518d5a41a47542cb6`
- **日期/作者**：`2026-05-13` / `Yuexiang XIE`
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

## [116] `c937ffb` refactor(console): Inbox (#4305)

- **完整 SHA**：`c937ffb558d5ab6ffe5f8756c4d2a9c13216dc92`
- **日期/作者**：`2026-05-14` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P2`
- **总体规模**：`4 文件`，`+563/-437`
- **实际影响范围**：
  - 影响定时任务、收件箱、消息推送或 session 隔离
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Inbox/hooks/useInboxData.ts` | +35/-4 | 前端页面 | 修改文件；新增/修改符号：const startPolling = () => {；const stopPolling = () => {；const handleVisibilityChange = () => { |
  | `console/src/pages/Inbox/hooks/useTraceViewer.ts` | +153/-0 | 前端页面 | 新增文件；新增/修改符号：type TraceDisplayItem,；interface TraceData {；export interface TraceViewerState {；export function useTraceViewer(；新增配置/字段：events: Array<{ at: number; event: Record<string, unknown> }>;；detailOpen: boolean;；selectedMessage: PushMessage \| null;；traceLoading: boolean; |
  | `console/src/pages/Inbox/index.tsx` | +33/-433 | 前端页面 | 修改文件；新增/修改符号：const foldIcon = kind |
  | `console/src/pages/Inbox/utils/traceUtils.ts` | +342/-0 | 前端页面 | 新增文件；新增/修改符号：export type TraceDisplayItem = {；export const buildContentFallbackTrace = (messageItem: PushMessage) => ({；export const getPrimaryTraceBlock = (；const content = event.content;；新增配置/字段：at: number;；eventType: string;；eventRecord: Record<string, unknown>;；traceText: string; |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [117] `7a0b62f` Fix(Provider): Fix anthropic provider max token handling (#4317)

- **完整 SHA**：`7a0b62f427eb35057eb32a0f90093fe7410c6f3b`
- **日期/作者**：`2026-05-14` / `Xuchen Pan`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+37/-7`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/providers/anthropic_provider.py` | +5/-7 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/providers/test_anthropic_provider.py` | +32/-0 | 模型 Provider | 修改文件；新增/修改符号：def test_get_chat_model_instance_does_not_mutate_generate_kwargs(；class FakeAnthropicChatModel:；def __init__(self, **kwargs) -> None:；新增配置/字段：captured: list[dict[str, object]] = []；"max_tokens": 32768,；"temperature": 0.2,；"max_tokens": 32768, |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [118] `fc6be99` feat(WeCom): support tool_guard interactive card in streaming path (#4307)

- **完整 SHA**：`fc6be9962665e1f8cf7d00257e3571fe5268d262`
- **日期/作者**：`2026-05-14` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+21/-1`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wecom/cards/dispatcher.py` | +11/-0 | 后端渠道实现 | 修改文件；新增配置/字段：skip_stream_detail: bool = False,；Args:；skip_stream_detail: When *True*, injects a transient flag |
  | `src/qwenpaw/app/channels/wecom/cards/tool_guard.py` | +3/-1 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/wecom/channel.py` | +7/-0 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [119] `8e2a835` chore(version): add release note for v1.1.7 (#4319)

- **完整 SHA**：`8e2a8351ec78c6b06004859d2955b604538fc1ac`
- **日期/作者**：`2026-05-14` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`8 文件`，`+162/-29`
- **实际影响范围**：
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `README.md` | +8/-7 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_ja.md` | +8/-7 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_ru.md` | +8/-7 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_zh.md` | +8/-7 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/__version__.py` | +1/-1 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
  | `website/public/release-notes/v1.1.7.md` | +64/-0 | 文档/发布 | 新增文件；文档或提示词文本调整 |
  | `website/public/release-notes/v1.1.7.zh.md` | +64/-0 | 文档/发布 | 新增文件；文档或提示词文本调整 |
  | `website/src/pages/ReleaseNotes.tsx` | +1/-0 | 文档/发布 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需排除包名、项目名、发布说明等品牌化内容

---

## [120] `f2e8b7f` chore(version): bumping version to 1.1.8b1 (#4346)

- **完整 SHA**：`f2e8b7fc07272b785c955f14e600b9e4932e675b`
- **日期/作者**：`2026-05-14` / `Yuexiang XIE`
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

## [121] `8e189a6` feat(plan mode): Strengthen plan reaffirm from the user message (#4198)

- **完整 SHA**：`8e189a6425e0252888383611fc688f733a73c133`
- **日期/作者**：`2026-05-14` / `yuanxs21`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+144/-16`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/react_agent.py` | +60/-2 | Agent 核心/执行 | 修改文件；新增/修改符号：def _filter_plan_tools(msg: Msg, nb: Any) -> Msg: |
  | `src/qwenpaw/app/runner/runner.py` | +26/-0 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/plan/__init__.py` | +2/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/plan/hints.py` | +56/-14 | 其他 | 修改文件；新增/修改符号：def clear_plan_awaiting_user_confirm(  # pylint: disable=protected-access；def check_plan_tool_gate( |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [122] `a49dc9e` fix(tool): browser implement activity tracking, crash monitoring, and lifecycle management (#4306)

- **完整 SHA**：`a49dc9e5764d1b87e4244f56e3376073cf5bf0d3`
- **日期/作者**：`2026-05-14` / `weixizi`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+72/-8`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/browser_control.py` | +64/-8 | 工具实现 | 修改文件；新增/修改符号：def on_crash(_p):；async def stop_all_browsers() -> None:；新增配置/字段：try:；else:；else:；try: |
  | `src/qwenpaw/app/_app.py` | +8/-0 | 其他 | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [123] `251e700` feat(agent): add Indonesian language option (#4287)

- **完整 SHA**：`251e7007cd380a1eb4afe660862eaf2a9b39dbbc`
- **日期/作者**：`2026-05-14` / `Aqil Aziz`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`10 文件`，`+242/-6`
- **实际影响范围**：
  - 影响记忆管理、自动记忆或长期记忆配置
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/constants/timezone.ts` | +1/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Agent/Config/components/ReactAgentCard.tsx` | +1/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/md_files/id/AGENTS.md` | +80/-0 | 其他 | 新增文件；新增配置/字段：summary: "Template workspace untuk AGENTS.md"；read_when:；Tujuannya: membantu tanpa mengganggu. Sesekali periksa hal penting, lakukan pekerjaan latar yang berguna, tetapi hormati |
  | `src/qwenpaw/agents/md_files/id/BOOTSTRAP.md` | +47/-0 | 其他 | 新增文件；新增配置/字段：summary: "Ritual pertama untuk agent baru"；read_when: |
  | `src/qwenpaw/agents/md_files/id/HEARTBEAT.md` | +11/-0 | 其他 | 新增文件；新增配置/字段：summary: "Template workspace untuk HEARTBEAT.md"；read_when: |
  | `src/qwenpaw/agents/md_files/id/MEMORY.md` | +26/-0 | 其他 | 新增文件；新增配置/字段：summary: "Memori jangka panjang agent — setup tool dan pelajaran yang dipelajari"；read_when:；Contohnya: |
  | `src/qwenpaw/agents/md_files/id/PROFILE.md` | +29/-0 | 其他 | 新增文件；新增配置/字段：summary: "Identitas agent dan profil pengguna"；read_when: |
  | `src/qwenpaw/agents/md_files/id/SOUL.md` | +40/-0 | 其他 | 新增文件；新增配置/字段：summary: "Template workspace untuk SOUL.md"；read_when: |
  | `src/qwenpaw/agents/utils/setup_utils.py` | +4/-3 | 其他 | 修改文件；新增配置/字段：language: Supported agent language code.；language: Supported agent language code. |
  | `src/qwenpaw/app/routers/workspace.py` | +3/-3 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [124] `83828a8` feat(telegram): add streaming output via editMessageText (#4318)

- **完整 SHA**：`83828a81f7831c9f24363dd74e854652ce8c4753`
- **日期/作者**：`2026-05-14` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`4 文件`，`+249/-1`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/channel.ts` | +1/-0 | 前端 API/types | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +1/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/telegram/channel.py` | +246/-0 | 后端渠道实现 | 修改文件；新增/修改符号：def _get_stream_state(self, send_meta: Dict[str, Any]) -> Dict[str, Any]:；async def _send_placeholder(；async def _edit_stream_message(；async def _delete_message(self, chat_id: str, message_id: int) -> None:；新增配置/字段：streaming_enabled: bool = False,；"message_ids": {},；"last_edit_ts": {},；chat_id: str, |
  | `src/qwenpaw/config/config.py` | +1/-0 | 配置/常量 | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [125] `d8ac7f6` fix(skill): fix skill hub import: fix www, add skill_hub retry (#4359)

- **完整 SHA**：`d8ac7f6a62594e5fcd61d7a282f1dd1de1594317`
- **日期/作者**：`2026-05-14` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+49/-5`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Agent/Skills/components/ImportHubModal.tsx` | +21/-4 | 前端页面 | 修改文件；新增/修改符号：function normalizeHost(host: string): string {；const inputHost = normalizeHost(parsedInput.host);；const inputPath = parsedInput.pathname.toLowerCase();；const source = skillMarkets.find((m) => { |
  | `src/qwenpaw/agents/skill_system/hub.py` | +28/-1 | 技能系统 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

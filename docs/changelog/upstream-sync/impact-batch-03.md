# 逐 commit 代码影响分析（第 3 批）

> 范围：第 51 - 75 条。此文档基于 diff 提取，重点回答“commit 了什么、影响哪里”。

## [51] `01750d9` fix(reload): route AgentConfigWatcher through reload_agent for graceful task draining (#4064)

- **完整 SHA**：`01750d9e37ff4ea33b337ad81a64476c8475e08b`
- **日期/作者**：`2026-05-08` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+130/-205`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/agent_config_watcher.py` | +107/-203 | Agent 核心/执行 | 修改文件；新增/修改符号：def _channels_hash(channels: Any) -> Optional[int]:；def _heartbeat_hash(hb: Optional["HeartbeatConfig"]) -> int:；def _read_mtime(self) -> float:；def _snapshot(self) -> None:；新增配置/字段：workspace: "Workspace",；agent_id: Agent ID to monitor.；workspace_dir: Path to agent's workspace directory.；workspace: Owning ``Workspace`` instance. The manager is |
  | `src/qwenpaw/app/multi_agent_manager.py` | +16/-0 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/app/workspace/service_factories.py` | +7/-2 | 其他 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [52] `8a6d2dc` feat(provider): add aliyun token plan as a built-in provider (#4122)

- **完整 SHA**：`8a6d2dc569b3bd1e9cf3788983bcf04ec2f91fcf`
- **日期/作者**：`2026-05-08` / `yuanxs21`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`6 文件`，`+140/-0`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Settings/Models/components/providerIcon.ts` | +1/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
  | `console/src/pages/Settings/Models/components/providerLetterIcon.tsx` | +1/-0 | 前端页面 | 修改文件 |
  | `src/qwenpaw/providers/anthropic_provider.py` | +15/-0 | 模型 Provider | 修改文件；新增配置/字段："X-DashScope-Cdpl": json.dumps(；"agentType": "QwenPaw",；"deployType": "UnKnown",；"moduleCode": "model", |
  | `src/qwenpaw/providers/capability_baseline.py` | +57/-0 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/providers/openai_provider.py` | +15/-0 | 模型 Provider | 修改文件；新增配置/字段："X-DashScope-Cdpl": json.dumps(；"agentType": "QwenPaw",；"deployType": "UnKnown",；"moduleCode": "model", |
  | `src/qwenpaw/providers/provider_manager.py` | +51/-0 | 模型 Provider | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [53] `9c9deab` fix(runner): rename channel variable to channel_name in command dispatch (#4134)

- **完整 SHA**：`9c9deabb79184e951ebbadb770b4c1dcb90d1a7b`
- **日期/作者**：`2026-05-09` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+4/-4`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/runner/command_dispatch.py` | +4/-4 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [54] `804cb82` perf(console): skip chat history lookup for non-arrow keys (#4130)

- **完整 SHA**：`804cb8284eb9b995920e0b24fa4a9967a9ddf969`
- **日期/作者**：`2026-05-09` / `YingchaoX`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+1/-0`
- **实际影响范围**：
  - 影响聊天页输入、会话、附件、模型选择或历史导航
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Chat/index.tsx` | +1/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [55] `ec8aad8` fix(tool_schema): add sanitize tool function schemas (#4126)

- **完整 SHA**：`ec8aad804d5e43288ab0c8a50eb314807addeecd`
- **日期/作者**：`2026-05-09` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+97/-0`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/providers/openai_chat_model_compat.py` | +97/-0 | 模型 Provider | 修改文件；新增/修改符号：def _sanitize_boolean_schemas(schema: Any) -> Any:；def _sanitize_tool_schemas(；def _format_tools_json_schemas(；新增配置/字段：result: dict[str, Any] = {}；else:；tools: list[dict[str, Any]],；schemas: list[dict[str, Any]], |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [56] `d4ebc9f` fix(cli): bypass proxies for loopback API checks (#4092)

- **完整 SHA**：`d4ebc9f36e6f59da4db85b7ec0d08771feb16cee`
- **日期/作者**：`2026-05-09` / `Jinglin Peng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`7 文件`，`+183/-6`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/agent_management.py` | +4/-1 | 工具实现 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/cli/doctor_cmd.py` | +10/-4 | 其他 | 修改文件；新增/修改符号：def _http_get(url: str, **kwargs) -> httpx.Response: |
  | `src/qwenpaw/cli/http.py` | +7/-1 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/utils/http.py` | +23/-0 | 其他 | 新增文件；新增/修改符号：def is_loopback_url(url: str) -> bool:；def trust_env_for_url(url: str) -> bool: |
  | `tests/unit/cli/test_cli_doctor_proxy.py` | +53/-0 | 测试/CI | 新增文件；新增/修改符号：class _Response:；def __init__(；def json(self) -> dict[str, Any]:；def test_doctor_http_get_bypasses_env_for_loopback(monkeypatch) -> None:；新增配置/字段：status_code: int = 200,；json_data: dict[str, Any] \| None = None,；text: str = "",；content_type: str = "application/json", |
  | `tests/unit/cli/test_cli_http_proxy.py` | +50/-0 | 测试/CI | 新增文件；新增/修改符号：def test_cli_http_client_bypasses_env_for_loopback(monkeypatch) -> None:；def _fake_client(**kwargs):；def test_cli_http_client_keeps_env_for_remote_base_url(monkeypatch) -> None:；def _fake_client(**kwargs):；新增配置/字段：captured: dict[str, object] = {}；captured: dict[str, object] = {}；captured: dict[str, object] = {} |
  | `tests/unit/utils/test_http.py` | +36/-0 | 测试/CI | 新增文件；新增/修改符号：def test_is_loopback_url_recognizes_loopback_targets(url: str) -> None:；def test_is_loopback_url_keeps_non_loopback_targets(url: str) -> None: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [57] `5c1cd03` fix(agent): replace hardcoded agent name with config-driven value (#4140)

- **完整 SHA**：`5c1cd03edc320d2cb23b64dd344dc997be0122c5`
- **日期/作者**：`2026-05-09` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`6 文件`，`+36/-14`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/react_agent.py` | +1/-1 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/app/_app.py` | +1/-1 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/command_dispatch.py` | +10/-7 | Agent 核心/执行 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/runner/daemon_commands.py` | +3/-2 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/app/runner/mission_dispatch.py` | +2/-1 | Agent 核心/执行 | 修改文件 |
  | `src/qwenpaw/app/runner/runner.py` | +19/-2 | Agent 核心/执行 | 修改文件；新增/修改符号：def agent_name(self) -> str:；def invalidate_agent_name_cache(self) -> None: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [58] `90a145d` fix(channels): keep markdown tables renderable across split_text chunks (#4119)

- **完整 SHA**：`90a145d9c20c4dbd9d50e44b9cc4261845058799`
- **日期/作者**：`2026-05-09` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+168/-48`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/utils.py` | +168/-48 | 后端渠道实现 | 修改文件；新增/修改符号：def _is_table_separator(line: str) -> bool:；def _split_table_block(；def _collect_table_lines(；class _SplitBuffer:；新增配置/字段：table_lines: List[str],；max_len: int,；current_rows: List[str] = []；lines: List[str], |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [59] `171030f` fix(agent): emoji example in AGENTS.md (#4142)

- **完整 SHA**：`171030fd590d70456dcd0fa7bfbc24ec60ea56c7`
- **日期/作者**：`2026-05-09` / `Keillion-Dynamsoft`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`3 文件`，`+6/-6`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/md_files/en/AGENTS.md` | +2/-2 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/md_files/ru/AGENTS.md` | +2/-2 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/md_files/zh/AGENTS.md` | +2/-2 | 其他 | 修改文件；文档或提示词文本调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [60] `3b884f4` fix(backup): restore secrets on Docker volume mount points (#3916)

- **完整 SHA**：`3b884f4e813b803d0d0f01c5c830e3a0abfddd47`
- **日期/作者**：`2026-05-09` / `Jinglin Peng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`7 文件`，`+860/-9`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/_app.py` | +13/-2 | 其他 | 修改文件 |
  | `src/qwenpaw/backup/_ops/restore.py` | +6/-0 | 其他 | 修改文件；新增/修改符号：def _restore_sync_locked(backup_id: str, req: RestoreBackupRequest) -> None: |
  | `src/qwenpaw/backup/_utils/_mount_swap.py` | +330/-0 | 其他 | 新增文件；新增/修改符号：class SwapPreparation(Enum):；def is_mount_point(path: Path) -> bool:；def is_rename_blocked(exc: OSError) -> bool:；def should_skip_restore_internal_path(rel_path: str) -> bool:；新增配置/字段：try:；dst: Path,；tmp_dst: Path,；old_dst: Path, |
  | `src/qwenpaw/backup/_utils/safe_swap.py` | +164/-6 | 其他 | 修改文件；新增/修改符号：def restore_process_lock() -> Iterator[None]:；def _acquire_file_lock(handle: BinaryIO, lock_path: Path) -> None:；def _raise_restore_lock_timeout(lock_path: Path) -> None:；def _restore_lock_timeout_seconds() -> float:；新增配置/字段：try:；finally:；try:；else: |
  | `src/qwenpaw/envs/store.py` | +8/-1 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/backup/__init__.py` | +0/-0 | 测试/CI | 新增文件；逻辑 hunk 调整 |
  | `tests/unit/backup/test_safe_swap.py` | +339/-0 | 测试/CI | 新增文件；新增/修改符号：def _make_zip(entries: dict[str, str]) -> zipfile.ZipFile:；def _snapshot(root: Path) -> dict[str, str]:；def _tmp_dir(dst: Path) -> Path:；def _secrets_dir(tmp_path: Path) -> Path:；新增配置/字段："new.txt": "new",；secrets_dir: Path,；secrets_dir: Path,；secrets_dir: Path, |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [61] `26a9344` feat(settings): add pt-BR language support (#4143)

- **完整 SHA**：`26a9344eb978aec6a934e2838fdeda27839ba028`
- **日期/作者**：`2026-05-09` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+2/-2`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/routers/settings.py` | +1/-1 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/routers/test_settings.py` | +1/-1 | 测试/CI | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [62] `2b9564d` feat(console): support mermaid graph (#4146)

- **完整 SHA**：`2b9564d1de3316b73877bba34dd7a9359f238ef3`
- **日期/作者**：`2026-05-09` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P1`
- **总体规模**：`8 文件`，`+214/-0`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/package-lock.json` | +1/-0 | 其他 | 修改文件 |
  | `console/package.json` | +1/-0 | 其他 | 修改文件 |
  | `console/src/components/MarkdownCopy/MarkdownCopy.tsx` | +2/-0 | 前端组件 | 修改文件；逻辑 hunk 调整 |
  | `console/src/components/MermaidCodeBlock/MermaidCodeBlock.tsx` | +95/-0 | 前端组件 | 新增文件；新增/修改符号：function ensureMermaidInit() {；interface MermaidCodeBlockProps {；export function MermaidCodeBlock({ chart }: MermaidCodeBlockProps) {；const trimmedChart = chart.trim();；新增配置/字段：startOnLoad: false,；theme: "neutral",；securityLevel: "loose",；chart: string; |
  | `console/src/components/MermaidCodeBlock/index.module.less` | +50/-0 | 前端组件 | 新增文件；新增配置/字段：position: relative;；width: 100%;；overflow: auto;；background: #fafafa; |
  | `console/src/components/MermaidCodeBlock/index.ts` | +2/-0 | 前端组件 | 新增文件；逻辑 hunk 调整 |
  | `console/src/components/MermaidCodeBlock/mermaidComponents.tsx` | +61/-0 | 前端组件 | 新增文件；新增/修改符号：function extractText(children: ReactNode): string {；function CodeWithMermaid({；const chartSource = extractText(children);；export const mermaidComponents: Record<；新增配置/字段：domNode: _domNode,；streamStatus: _streamStatus,；code: CodeWithMermaid, |
  | `console/src/pages/Agent/Workspace/components/FileEditor.tsx` | +2/-0 | 前端页面 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [63] `8b8ddba` feat(WeCom): tool-guard interactive approval card (#4112)

- **完整 SHA**：`8b8ddbafc719ae098cc92623245de54b3484f081`
- **日期/作者**：`2026-05-09` / `hongxicheng`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`5 文件`，`+813/-0`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wecom/cards/__init__.py` | +21/-0 | 后端渠道实现 | 新增文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/channels/wecom/cards/context.py` | +124/-0 | 后端渠道实现 | 新增文件；新增/修改符号：def extract_meta(event: Any) -> Optional[Dict[str, Any]]:；def extract_body_text(content: Any) -> str:；def build_session_ctx(；async def send_stream_detail(；新增配置/字段：to_handle: str,；send_meta: Dict[str, Any],；"session_id": session_id,；"sender_id": str(send_meta.get("wecom_sender_id") or ""), |
  | `src/qwenpaw/app/channels/wecom/cards/dispatcher.py` | +199/-0 | 后端渠道实现 | 新增文件；新增/修改符号：class CardKind:；class WecomCardHandler:；def __init__(self, channel: "WecomChannel") -> None:；def register(self, kind: CardKind) -> None:；新增配置/字段：name: str  # human-readable tag for logs；message_type: str  # matches ``metadata.message_type`` (outbound)；task_id_prefix: str  # matches ``task_id`` prefix (inbound)；render: RenderFn |
  | `src/qwenpaw/app/channels/wecom/cards/tool_guard.py` | +436/-0 | 后端渠道实现 | 新增文件；新增/修改符号：def _truncate(text: str, limit: int) -> str:；def _build_button_key(；def build_approval_card(；def build_resolved_card(；新增配置/字段：Refs: https://developer.work.weixin.qq.com/document/path/101032；https://developer.work.weixin.qq.com/document/path/101027；action: str,；request_id: str, |
  | `src/qwenpaw/app/channels/wecom/channel.py` | +33/-0 | 后端渠道实现 | 修改文件；新增/修改符号：async def on_event_message_completed(；新增配置/字段：request: "AgentRequest",；to_handle: str,；event: Any,；send_meta: Dict[str, Any], |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [64] `c6019fb` feat(provider): allow Dashscope base URL selection in Console UI (#4074)

- **完整 SHA**：`c6019fb80891580b552f1386e3e5fd79f62384f3`
- **日期/作者**：`2026-05-09` / `Eric Zhu`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`11 文件`，`+97/-13`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/api/types/provider.ts` | +8/-0 | 前端 API/types | 修改文件；新增/修改符号：export interface BaseUrlOption {；新增配置/字段：label: string;；value: string; |
  | `console/src/locales/en.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："selectBaseURL": "Select a base URL",；"selectBaseURLHint": "Select the regional endpoint for this provider", |
  | `console/src/locales/ja.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："selectBaseURL": "ベースURLを選択してください",；"selectBaseURLHint": "このプロバイダーのリージョンエンドポイントを選択", |
  | `console/src/locales/pt-BR.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："selectBaseURL": "Selecione uma URL base",；"selectBaseURLHint": "Selecione o endpoint regional deste provedor", |
  | `console/src/locales/ru.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："selectBaseURL": "Выберите базовый URL",；"selectBaseURLHint": "Выберите региональную конечную точку этого провайдера", |
  | `console/src/locales/zh.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："selectBaseURL": "请选择基础 URL",；"selectBaseURLHint": "选择该服务商的区域接入点", |
  | `console/src/pages/Settings/Models/components/modals/ProviderConfigModal.tsx` | +48/-3 | 前端页面 | 修改文件；新增/修改符号：const baseUrlOptions = useMemo<BaseUrlOption[]>(() => {；const raw = provider.meta?.base_url_options;；const useBaseUrlSelect = canEditBaseUrl && baseUrlOptions.length > 0;；新增配置/字段：label: `${option.label} — ${option.value}`,；value: option.value, |
  | `src/qwenpaw/constant.py` | +0/-5 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/providers/anthropic_provider.py` | +6/-2 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/providers/openai_provider.py` | +6/-2 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/providers/provider_manager.py` | +19/-1 | 模型 Provider | 修改文件；新增配置/字段："base_url_options": [；"label": "China (Beijing)",；"value": "https://dashscope.aliyuncs.com/"；"label": "International (Singapore)", |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [65] `c46996b` fix(agent-tools): add safe default timeout for delegate_external_agent (#3928)

- **完整 SHA**：`c46996bb781b079db31a2a47be6fe8c49adad4f8`
- **日期/作者**：`2026-05-09` / `Nova Dev Team`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+17/-11`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/delegate_external_agent.py` | +17/-11 | 工具实现 | 修改文件 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [66] `cf18e6c` fix(console): Immediately stop polling and clear the status after closing the drawer. (#4148)

- **完整 SHA**：`cf18e6cc987a13f807ef05258d6302a7210f9d90`
- **日期/作者**：`2026-05-09` / `zhaozhuang521`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+11/-1`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +11/-1 | 前端页面 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [67] `c3b56c0` fix(agent-config): preserve complete config on save to prevent nested config loss (#4157)

- **完整 SHA**：`c3b56c01cee167cf7c7f85f794ac1089ea86413a`
- **日期/作者**：`2026-05-09` / `zhijianma`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`1 文件`，`+12/-3`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Agent/Config/useAgentConfig.tsx` | +12/-3 | 前端页面 | 修改文件；新增/修改符号：const originalConfigRef = useRef<AgentsRunningConfig \| null>(null); |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [68] `6a7b39d` refactor(console): extract QrcodeAuthBlock component and fix polling leak on drawer close (#4153)

- **完整 SHA**：`6a7b39d817b37b14b380aae5f8f6d59546213e9f`
- **日期/作者**：`2026-05-09` / `zhaozhuang521`
- **标签/优先级**：`🟠 待人工` / `P2`
- **总体规模**：`3 文件`，`+132/-208`
- **实际影响范围**：
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/pages/Control/Channels/components/ChannelDrawer.tsx` | +67/-200 | 前端页面 | 修改文件；移除符号：const wechatQrcode = useChannelQrcode({；const dingtalkQrcode = useChannelQrcode({；const wecomQrcode = useChannelQrcode({；新增配置/字段：client_id: credentials.client_id,；client_secret: credentials.client_secret,；bot_id: credentials.bot_id,；secret: credentials.secret, |
  | `console/src/pages/Control/Channels/components/QrcodeAuthBlock.tsx` | +62/-0 | 前端页面 | 新增文件；新增/修改符号：interface QrcodeAuthBlockProps extends ChannelQrcodeConfig {；export function QrcodeAuthBlock({；const qrcode = useChannelQrcode(qrcodeConfig);；新增配置/字段：label: string;；buttonText: string;；imageAlt: string;；hintText: string; |
  | `console/src/pages/Control/Channels/components/useChannelQrcode.ts` | +3/-8 | 前端页面 | 修改文件；新增/修改符号：export interface ChannelQrcodeConfig {；export interface ChannelQrcodeState { |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [69] `0dc50af` fix lifecycle-task leak in stateful clients and refactor shared logic into mixin (#4152)

- **完整 SHA**：`0dc50afddb4a529431222a11bf5e0304d3015cb3`
- **日期/作者**：`2026-05-09` / `qbc`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+394/-376`
- **实际影响范围**：
  - 影响 MCP 工具连接生命周期、超时、OAuth 或清理逻辑
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/mcp/manager.py` | +26/-38 | MCP | 修改文件；新增配置/字段：Flow: connect new (outside lock) → atomic swap (inside lock) →；try: |
  | `src/qwenpaw/app/mcp/stateful_client.py` | +368/-338 | MCP | 修改文件；新增/修改符号：def _is_transport_error(exc: BaseException) -> bool:；class _MCPClientMixin:；async def _setup_transport(；async def close(self, ignore_errors: bool = True) -> None:；新增配置/字段：try:；_ANYIO_TRANSPORT_ERRORS: tuple[type[BaseException], ...] = (；_TRANSPORT_ERRORS: tuple[type[BaseException], ...] = (；name: str |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [70] `047afe5` chore(version): bumping version to 1.1.6b2 (#4161)

- **完整 SHA**：`047afe5f89ca4a54ecbb3c5f6e1e51c80969fff5`
- **日期/作者**：`2026-05-09` / `Yuexiang XIE`
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

## [71] `8cc10d2` chore(release): update release note of v1.1.6 (#4163)

- **完整 SHA**：`8cc10d2c86673320a6f728b0994170f18a007eb1`
- **日期/作者**：`2026-05-09` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P3`
- **总体规模**：`8 文件`，`+218/-61`
- **实际影响范围**：
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `README.md` | +7/-15 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_ja.md` | +7/-15 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_ru.md` | +7/-15 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `README_zh.md` | +7/-15 | 文档/发布 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/__version__.py` | +1/-1 | 配置/常量 | 修改文件；逻辑 hunk 调整 |
  | `website/public/release-notes/v1.1.6.md` | +94/-0 | 文档/发布 | 新增文件；文档或提示词文本调整 |
  | `website/public/release-notes/v1.1.6.zh.md` | +94/-0 | 文档/发布 | 新增文件；文档或提示词文本调整 |
  | `website/src/pages/ReleaseNotes.tsx` | +1/-0 | 文档/发布 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需排除包名、项目名、发布说明等品牌化内容

---

## [72] `53cd8b1` Fix(provider): fix models in VOLCENGINE Provider (#4169)

- **完整 SHA**：`53cd8b164fa12301bbcfb3b9c439977579bdf635`
- **日期/作者**：`2026-05-11` / `Lingrui Gu`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+68/-71`
- **实际影响范围**：
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/providers/provider_manager.py` | +62/-67 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
  | `tests/unit/providers/test_volcengine_provider.py` | +6/-4 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

## [73] `95908ac` chore(version): bumping version to 1.1.7b1 (#4196)

- **完整 SHA**：`95908ac535f7c76be6fdb9bcfd85088495361bfb`
- **日期/作者**：`2026-05-11` / `Yuexiang XIE`
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

## [74] `cc57579` fix(console): improve text contrast in Plan Panel dark mode (#4190)

- **完整 SHA**：`cc575796016c695de27e0da0cd5b0b24b4f21f24`
- **日期/作者**：`2026-05-11` / `ltzu`
- **标签/优先级**：`✅ 直接合入` / `P0`
- **总体规模**：`2 文件`，`+56/-2`
- **实际影响范围**：
  - 局部代码行为调整，影响范围主要限于列出的文件
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/components/PlanPanel/index.module.less` | +54/-0 | 前端组件 | 修改文件；新增配置/字段：color: var(--colorText, rgba(0, 0, 0, 0.88));；color: rgba(255, 255, 255, 0.85) !important;；color: rgba(255, 255, 255, 0.65) !important;；color: #73d13d !important; |
  | `console/src/components/PlanPanel/index.tsx` | +2/-2 | 前端组件 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 主要按文件冲突和测试结果判断

---

## [75] `eb01c83` fix(provider,wecom): preserve provider meta field and update tool_guard docstring in wecom (#4200)

- **完整 SHA**：`eb01c838dc5d2238a90d33b4d3baf49d9658b737`
- **日期/作者**：`2026-05-11` / `zhijianma`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`2 文件`，`+3/-1`
- **实际影响范围**：
  - 影响消息渠道收发、连接状态、审批卡片或流式输出行为
  - 影响模型供应商请求参数、模型列表或兼容性
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/app/channels/wecom/cards/tool_guard.py` | +2/-1 | 后端渠道实现 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/providers/provider.py` | +1/-0 | 模型 Provider | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

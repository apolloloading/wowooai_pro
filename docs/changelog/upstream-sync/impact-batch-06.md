# 逐 commit 代码影响分析（第 6 批）

> 范围：第 126 - 130 条。此文档基于 diff 提取，重点回答“commit 了什么、影响哪里”。

## [126] `f18a3c2` style(console): inbox page (#4358)

- **完整 SHA**：`f18a3c2f3a819b8e95cf6c047640ca21b8e13b46`
- **日期/作者**：`2026-05-14` / `zhaozhuang521`
- **标签/优先级**：`🟡 裁剪合入` / `P2`
- **总体规模**：`11 文件`，`+203/-154`
- **实际影响范围**：
  - 影响多语言文案，需要校验中文“数字员工”等术语
  - 影响定时任务、收件箱、消息推送或 session 隔离
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `console/src/layouts/Sidebar.tsx` | +20/-7 | 前端布局 | 修改文件；移除符号：const inboxIcon = (size: number) => (；新增配置/字段：icon: (；position: "absolute",；top: -1,；right: -3, |
  | `console/src/layouts/index.module.less` | +9/-2 | 前端布局 | 修改文件；新增配置/字段：overflow: visible !important;；overflow: visible !important; |
  | `console/src/locales/en.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："batchOperation": "Batch",；"exitBatch": "Exit Batch", |
  | `console/src/locales/ja.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："batchOperation": "一括操作",；"exitBatch": "一括終了", |
  | `console/src/locales/pt-BR.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："batchOperation": "Operação em lote",；"exitBatch": "Sair do lote", |
  | `console/src/locales/ru.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："batchOperation": "Массовые действия",；"exitBatch": "Выйти", |
  | `console/src/locales/zh.json` | +2/-0 | 前端国际化 | 修改文件；新增文案 key："batchOperation": "批量操作",；"exitBatch": "退出批量", |
  | `console/src/pages/Inbox/components/PushMessageCard.module.less` | +18/-5 | 前端页面 | 修改文件；新增配置/字段：height: 142px !important;；display: flex;；display: -webkit-box;；overflow: hidden; |
  | `console/src/pages/Inbox/components/PushMessageCard.tsx` | +8/-31 | 前端页面 | 修改文件；新增/修改符号：export function PushMessageCard(props: PushMessageCardProps) { |
  | `console/src/pages/Inbox/index.module.less` | +23/-18 | 前端页面 | 修改文件；新增配置/字段：height: 100%;；display: flex;；overflow: hidden;；background: #fff; |
  | `console/src/pages/Inbox/index.tsx` | +115/-91 | 前端页面 | 修改文件；新增配置/字段：key: "messages",；label: (；children: (；count: selectedMessageIds.length, |
- **合入检查点**：
  - 需人工核对中文/英文/俄文文案与品牌术语

---

## [127] `11f2136` fix(skill): fix skill path, use safer path normalizer and refactor for function naming (#4335)

- **完整 SHA**：`11f213637da4ff4a935eaac7aee281024506bdf7`
- **日期/作者**：`2026-05-14` / `Runlin Lei`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`7 文件`，`+519/-353`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/skill_system/pool_service.py` | +126/-91 | 技能系统 | 修改文件；新增配置/字段：try:；try:；try:；try: |
  | `src/qwenpaw/agents/skill_system/registry.py` | +94/-53 | 技能系统 | 修改文件；新增/修改符号：def get_packaged_builtin_versions() -> dict[str, str]: |
  | `src/qwenpaw/agents/skill_system/store.py` | +147/-93 | 技能系统 | 修改文件；新增/修改符号：def read_frontmatter_safe_from_path(；def _read_frontmatter(skill_dir: Path) -> Any:；def _read_frontmatter_safe(；def get_skill_mtime(skill_dir: Path) -> str:；新增配置/字段：skill_md_path: Path,；skill_name: str = "",；try:；skill_dir: Path, |
  | `src/qwenpaw/agents/skill_system/workspace_service.py` | +119/-83 | 技能系统 | 修改文件；新增配置/字段：try:；try:；"success": False,；"updated_workspaces": [], |
  | `src/qwenpaw/app/migration.py` | +6/-6 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/app/routers/skills.py` | +25/-25 | 后端 API 路由 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/cli/skills_cmd.py` | +2/-2 | 技能系统 | 修改文件；逻辑 hunk 调整 |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [128] `799017e` feat(plugin): add CloudPaw plugin bundle for Alibaba Cloud deployment (#4362)

- **完整 SHA**：`799017e65ef481f0bf31ab8772b6d608a7096449`
- **日期/作者**：`2026-05-14` / `Xuanrui Lin`
- **标签/优先级**：`🟠 待人工` / `P1`
- **总体规模**：`101 文件`，`+22511/-0`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
  - 影响插件安装、注册、工具插件或云部署插件
  - 新增模块/页面/插件文件，合入时需确认入口注册是否完整
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `plugins/bundle/cloudpaw/README.md` | +160/-0 | 插件 | 新增文件；文档或提示词文本调整 |
  | `plugins/bundle/cloudpaw/README_zh.md` | +160/-0 | 插件 | 新增文件；文档或提示词文本调整 |
  | `plugins/bundle/cloudpaw/__init__.py` | +2/-0 | 插件 | 新增文件；逻辑 hunk 调整 |
  | `plugins/bundle/cloudpaw/agents/executor/en/PROFILE.md` | +36/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/executor/en/SOUL.md` | +9/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/executor/zh/PROFILE.md` | +36/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/executor/zh/SOUL.md` | +9/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/orchestration/en/PROFILE.md` | +11/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/orchestration/en/SOUL.md` | +7/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/orchestration/zh/PROFILE.md` | +11/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/orchestration/zh/SOUL.md` | +7/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/verifier/en/PROFILE.md` | +307/-0 | 插件 | 新增文件；新增/修改符号：def http_get(url,timeout=10):；def check_http_reachable():；def check_visual_style():；def run():；新增配置/字段：summary: "Verifier Agent identity"；Script: story_US-001_verify.py  Config: config_US-001.yaml  Result: (result_US-001.json specific content)；Script: story_US-002_verify.py  Config: config_US-002.yaml  Result: (result_US-002.json specific content)；OVERALL: FAIL |
  | `plugins/bundle/cloudpaw/agents/verifier/en/SOUL.md` | +10/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents/verifier/zh/PROFILE.md` | +307/-0 | 插件 | 新增文件；新增/修改符号：def http_get(url,timeout=10):；def check_http_reachable():；def check_visual_style():；def run():；新增配置/字段：summary: "验证 Agent 身份"；OVERALL: FAIL；"verification_status": "passed\|failed\|partial",；"checks": [{"category": "file_check\|html_structure\|cloud_resource\|accessibility\|security_group\|security","item": "验收条件简短 |
  | `plugins/bundle/cloudpaw/agents/verifier/zh/SOUL.md` | +10/-0 | 插件 | 新增文件 |
  | `plugins/bundle/cloudpaw/agents_setup.py` | +404/-0 | 插件 | 新增文件；新增/修改符号：def register_extra_tools(agent_id: str, extra_tools: dict[str, dict]) -> None:；def _build_acp_config(spec: dict[str, Any]) -> Any:；def _inject_llm_env(env: dict[str, str]) -> None:；def ensure_builtin_agents() -> None:；新增配置/字段：try:；try:；try:；try: |
  | `plugins/bundle/cloudpaw/constants.py` | +137/-0 | 插件 | 新增文件；新增配置/字段：_DISABLED_AGENT_TOOLS: dict[str, dict[str, Any]] = {；"chat_with_agent": {；"name": "chat_with_agent",；"enabled": False, |
  | `plugins/bundle/cloudpaw/docs/cloudpaw.png` | +bin/-bin | 插件 | 新增文件；逻辑 hunk 调整 |
  | ... |  |  | 另有 83 个文件，通常为同一功能的资源/文案/测试扩展；完整列表见 `commits-batch-*` |
- **合入检查点**：
  - 需确认不破坏 onboarding-guide 与我方技能目录

---

## [129] `fc5e6af` fix(QA agent): bundle docs as package_data (#4280)

- **完整 SHA**：`fc5e6afd0927bc395a5fbd12d6ff6b506622f685`
- **日期/作者**：`2026-05-14` / `Yuexiang XIE`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`16 文件`，`+131/-37`
- **实际影响范围**：
  - 影响技能导入、加载、路径规范化或技能池存储
  - 影响打包元数据、发布说明或文档，不一定是运行时代码
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `.dockerignore` | +4/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `.github/workflows/publish-pypi.yml` | +6/-0 | 测试/CI | 修改文件 |
  | `.gitignore` | +3/-0 | 其他 | 修改文件；逻辑 hunk 调整 |
  | `deploy/Dockerfile` | +1/-0 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
  | `pyproject.toml` | +1/-1 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
  | `scripts/install.sh` | +29/-1 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
  | `scripts/wheel_build.ps1` | +7/-0 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
  | `scripts/wheel_build.sh` | +7/-0 | 脚本/部署 | 修改文件；逻辑 hunk 调整 |
  | `src/qwenpaw/agents/md_files/qa/en/AGENTS.md` | +1/-1 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/md_files/qa/ru/AGENTS.md` | +1/-1 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/md_files/qa/zh/AGENTS.md` | +1/-1 | 其他 | 修改文件；文档或提示词文本调整 |
  | `src/qwenpaw/agents/skills/QA_source_index-en/SKILL.md` | +5/-4 | 其他 | 修改文件 |
  | `src/qwenpaw/agents/skills/QA_source_index-zh/SKILL.md` | +5/-4 | 其他 | 修改文件 |
  | `src/qwenpaw/agents/skills/guidance-en/SKILL.md` | +22/-12 | 其他 | 修改文件 |
  | `src/qwenpaw/agents/skills/guidance-zh/SKILL.md` | +22/-12 | 其他 | 修改文件 |
  | `src/qwenpaw/constant.py` | +16/-0 | 配置/常量 | 修改文件；新增/修改符号：def _resolve_docs_dir() -> Path \| None: |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合
  - 需确认不破坏 onboarding-guide 与我方技能目录
  - 需排除包名、项目名、发布说明等品牌化内容

---

## [130] `00ede85` fix(tool): add _CDP_CONNECT_TIMEOUT_SECONDS = 30 for connect cdp (#4350)

- **完整 SHA**：`00ede853fac401296c58a49ec782b907e2e1d882`
- **日期/作者**：`2026-05-14` / `x1n95c`
- **标签/优先级**：`🔴 跳过-冲突` / `P1`
- **总体规模**：`1 文件`，`+34/-1`
- **实际影响范围**：
  - 影响内置工具调用能力、浏览器控制、文件读取或代理委托
- **逐文件影响**：
  | 文件 | +/- | 类型 | 影响说明 |
  |---|---:|---|---|
  | `src/qwenpaw/agents/tools/browser_control.py` | +34/-1 | 工具实现 | 修改文件；新增/修改符号：async def _stop_playwright_instance(pw: Any) -> None:；新增配置/字段：try:；"ok": False,；"error": ( |
- **合入检查点**：
  - 需要映射到 `src/wowooai/` 对应文件，不能直接按路径合

---

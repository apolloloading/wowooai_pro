# 前端改造说明

> 本文记录本轮已落地的前端改动。完整目标源码以 [source-bundle/console/](source-bundle/console/) 为准；蓝色品牌资产在 [brand/](brand/)。
>
> 前端依赖后端：先按 [backend.md](backend.md) §1 完成包重命名（`qwenpaw` / `copaw` → `wowooai`，大小写不敏感）。

---

## 目录

### 一、品牌与基础（§1–§4）
- [§1 品牌资产](#1-品牌资产)
- [§3 主题与语言锁定](#3-主题与语言锁定)
- [§4 蓝色品牌资产替换与旧引用修正](#4-蓝色品牌资产替换与旧引用修正)

### 二、本地开发与校验（§5–§6）
- [§5 本地开发联调（dev server + 后端 CORS）](#5-本地开发联调dev-server--后端-cors)
- [§6 复刻整体校验清单](#6-复刻整体校验清单)

### 三、菜单导航裁剪与页面收敛（§7–§14）
- [§7 菜单与导航裁剪 / 默认智能体锁定 / 面包屑移除](#7-菜单与导航裁剪--默认智能体锁定--面包屑移除)
- [§8 工具执行安全独立页](#8-工具执行安全独立页)
- [§9 安全防护（/agent-config）改为复用 AgentConfigPage（仅前端）](#9-安全防护agent-config改为复用-agentconfigpage仅前端)
- [§10 侧边栏扁平化（仅前端）](#10-侧边栏扁平化仅前端)
- [§11 外部渠道：移除「全部 / 内置 / 自定义」筛选](#11-外部渠道移除全部--内置--自定义筛选仅前端)
- [§12 我的技能：移除三个操作按钮](#12-我的技能移除三个操作按钮仅前端)
- [§13 全局橙色 → 品牌蓝](#13-全局橙色--品牌蓝仅前端)
- [§14 后续修订（§9–§13）的资产与快照位置](#14-后续修订9-13的资产与快照位置)

### 四、2026-04-30 落地复刻顺序与二次/三次收敛（§15–§17）
- [§15 2026-04-30 实际落地复刻顺序（前端）](#15-2026-04-30-实际落地复刻顺序前端)
- [§16 2026-04-30 二次前端收敛：Chat / 模型供应商 / 外部渠道 / 配色](#16-2026-04-30-二次前端收敛chat--模型供应商--外部渠道--配色)
- [§17 2026-04-30 第三轮前端微调：Chat 文案 / Workspace attribution 隐藏](#17-2026-04-30-第三轮前端微调chat-文案--workspace-attribution-隐藏)

### 五、Cron 与 API base URL（§18–§19、§21）
- [§18 2026-04-30 增量：Cron 默认执行超时 120s → 1200s](#18-2026-04-30-增量cron-默认执行超时-120s--1200s)
- [§19 2026-04-30 增量：前端 API base URL 修复（接口打到正确后端）](#19-2026-04-30-增量前端-api-base-url-修复接口打到正确后端)
- [§21 2026-05-04 增量：前端 API base URL 改为同源相对路径](#21-2026-05-04-增量前端-api-base-url-改为同源相对路径)

### 六、桌面打包与文件下载（§20、§22）
- [§20 2026-05-04 增量：桌面打包前端静态资源校验](#20-2026-05-04-增量桌面打包前端静态资源校验)
- [§22 2026-05-04 修复：桌面端 send_file_to_user 文件点击下载无响应](#22-2026-05-04-修复桌面端-send_file_to_user-文件点击下载无响应window-open--pywebview-save_file)

### 七、2026-05-06 UI 精简（§23–§24）
- [§23 2026-05-06 前端 UI 精简与文案调整](#23-2026-05-06-前端-ui-精简与文案调整仅前端)
- [§24 2026-05-06 修复：定时任务列表 hidden 列未真正隐藏，操作列布局异常](#24-2026-05-06-修复定时任务列表-hidden-列未真正隐藏操作列布局异常)

### 八、2026-05-12 桌面控制能力（§25）
- [§25 2026-05-12 说明：桌面控制能力无前端改动（对应 backend §33）](#25-2026-05-12-说明桌面控制能力无前端改动对应-backend-33)

### 九、2026-05-14 浏览器默认有头模式（§27）
- [§27 2026-05-14 说明：浏览器默认有头模式无前端改动（对应 backend §35）](#27-2026-05-14-说明浏览器默认有头模式无前端改动对应-backend-35)

### 十、2026-05-14 用户消息空白保留（§28）
- [§28 2026-05-14 修复：用户消息保留换行/空格/缩进（CSS 单行修复）](#28-2026-05-14-修复用户消息保留换行空格缩进css-单行修复)

### 十一、2026-05-14 数字员工管理 UX 收敛（§31）
- [§31 2026-05-14 数字员工管理 UX 收敛：菜单收纳 / 选择器重设计 / 列表瘦身 / 创建表单精简 / 技能中文名](#31-2026-05-14-数字员工管理-ux-收敛菜单收纳--选择器重设计--列表瘦身--创建表单精简--技能中文名)

### 十二、2026-05-14 OpenCode 供应商前端隐藏（§32）
- [§32 2026-05-14 OpenCode 供应商前端隐藏（在 API 层过滤）](#32-2026-05-14-opencode-供应商前端隐藏在-api-层过滤)

### 十三、2026-05-14 Chat 页 UX 收敛（§33–§34）
- [§33 2026-05-14 Chat 页 UX 收敛：ModelSelector 移入发送区 / 去掉搜索入口 / 欢迎语动态化](#33-2026-05-14-chat-页-ux-收敛modelselector-移入发送区--去掉搜索入口--欢迎语动态化)
- [§34 2026-05-14 §33 落地后的修正：欢迎语回退到真实 name / 描述留空 / ModelSelector 槽位 + 弹出方向 / 后端 future-annotations 崩溃](#34-2026-05-14-33-落地后的修正欢迎语回退到真实-name--描述留空--modelselector-槽位--弹出方向--后端-future-annotations-崩溃)

### 十四、2026-05-14 侧边栏个人中心（§35、§37）
- [§35 2026-05-14 侧边栏新增「个人中心」置底入口，收纳 4 个二级菜单](#35-2026-05-14-侧边栏新增个人中心置底入口收纳-4-个二级菜单)
- [§37 2026-05-14 §35 后续收敛：个人中心真正置底 / 模型配置页样式收紧 / 安全防护页去掉面包屑与标题](#37-2026-05-14-35-后续收敛个人中心真正置底--模型配置页样式收紧--安全防护页去掉面包屑与标题)

### 十五、2026-05-14 入职小助手内置技能识别（§36）
- [§36 2026-05-14 内置 QA Agent → 入职小助手：前端内置技能识别名单追加 `onboarding-guide`](#36-2026-05-14-内置-qa-agent--入职小助手前端内置技能识别名单追加-onboarding-guide)

### 十六、2026-05-14 二轮 UX 收敛（§38）
- [§38 2026-05-14 二轮 UX 收敛：模型卡瘦身 / 我的记忆顶栏移除 / 安全防护精简 / 渠道卡精简 / 技能页筛选与文案](#38-2026-05-14-二轮-ux-收敛模型卡瘦身--我的记忆顶栏移除--安全防护精简--渠道卡精简--技能页筛选与文案)

### 十七、2026-05-15 紧凑卡片重设计（§39）
- [§39 2026-05-15 紧凑卡片重设计：渠道 / 模型供应商 / 默认 LLM 顶部条](#39-2026-05-15-紧凑卡片重设计渠道--模型供应商--默认-llm-顶部条)

### 十八、2026-05-15 二轮顶栏微调（§40）
- [§40 2026-05-15 员工记忆移出个人中心 / 技能页工具条重设计 / 折叠态图标对齐 / 个人中心置底 / md 编辑切换](#40-2026-05-15-员工记忆移出个人中心--技能页工具条重设计--折叠态图标对齐--个人中心置底--md-编辑切换)

> **编号说明**：§2 在原始记录中未使用；§19 / §20 在历史中曾出现编号冲突，已通过本次重排（→§24）解决，原始内容完整保留。§29 / §30 为后端章节占位，前端无改动直接在正文呈现，未在目录列出。

---

## §1 品牌资产

**文件**：
- `console/index.html`
- `console/package.json`
- `console/public/`（logo / favicon / 背景图）

**`console/index.html` 关键点**：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>WowooAI Console</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**`console/package.json`**：包名 `wowooai-console`、脚本 `dev` / `build` / `preview` 走 vite。

**复刻校验**：

```bash
grep -E '"name"|"version"' console/package.json
grep -E "<title>|favicon" console/index.html
ls console/public/
# 期望：favicon.svg / logo-dark.svg / logo-light.svg / wowooai-logo.svg / wowooai.png / wowooaiBack.png
```

> **左上角 Header logo 必须可读**：`console/src/layouts/index.module.less` 中 `.logoImg` 设为 `height: 32px; width: auto;`。

---

## §3 主题与语言锁定

**文件**：
- `console/src/contexts/ThemeContext.tsx`
- `console/src/i18n.ts`
- `console/src/App.tsx`

**主题**：默认 `light`，不读取 `localStorage`，应用内不暴露主题切换按钮。

```tsx
// ThemeContext.tsx
const DEFAULT_THEME: ThemeMode = "light";
```

**语言**：默认 `zh-CN`，启动时强制对齐。

```ts
// i18n.ts
i18n.use(initReactI18next).init({
  resources: { zh, en, ja, ru },
  lng: "zh",
  fallbackLng: "zh",
  interpolation: { escapeValue: false },
});
```

```tsx
// App.tsx
useEffect(() => {
  if (i18n.language !== "zh") i18n.changeLanguage("zh");
}, []);
```

**复刻校验**：

```bash
grep -n 'lng:' console/src/i18n.ts                 # 期望 lng: "zh"
grep -n 'DEFAULT_THEME' console/src/contexts/ThemeContext.tsx
```

---

## §4 蓝色品牌资产替换与旧引用修正

> 本节记录已落地的蓝色 `#2563EB` 品牌资产替换，以及旧 logo / 远程头像引用修正。

### 4.1 公共资产替换为蓝色版本

**新 logo 源文件位置（仓库内权威来源，蓝色 `#2563EB`）**：

| 文件 | 源路径（绝对） | 仓库相对路径 | 用途 |
|---|---|---|---|
| `favicon.svg` | `/Users/rlw/AI项目/wowooai/docs/changelog/brand/favicon.svg` | [docs/changelog/brand/favicon.svg](docs/changelog/brand/favicon.svg) | 浏览器 tab 图标 + Chat 欢迎页头像 |
| `logo-light.svg` | `/Users/rlw/AI项目/wowooai/docs/changelog/brand/logo-light.svg` | [docs/changelog/brand/logo-light.svg](docs/changelog/brand/logo-light.svg) | 浅色主题左上角 Header logo + Login 页 logo |
| `logo-dark.svg` | `/Users/rlw/AI项目/wowooai/docs/changelog/brand/logo-dark.svg` | [docs/changelog/brand/logo-dark.svg](docs/changelog/brand/logo-dark.svg) | 深色主题 logo 资产 |
| `wowooai-logo.svg` | `/Users/rlw/AI项目/wowooai/docs/changelog/brand/wowooai-logo.svg` | [docs/changelog/brand/wowooai-logo.svg](docs/changelog/brand/wowooai-logo.svg) | 含文字主 logo |

**落地位置（前端 public 目录，构建后会被 Vite 复制到根路径 `/`）**：

| 文件 | 落地路径（绝对） | 仓库相对路径 | 运行时 URL |
|---|---|---|---|
| `favicon.svg` | `/Users/rlw/AI项目/wowooai/console/public/favicon.svg` | [console/public/favicon.svg](console/public/favicon.svg) | `${BASE_URL}favicon.svg` |
| `logo-light.svg` | `/Users/rlw/AI项目/wowooai/console/public/logo-light.svg` | [console/public/logo-light.svg](console/public/logo-light.svg) | `${BASE_URL}logo-light.svg` |
| `logo-dark.svg` | `/Users/rlw/AI项目/wowooai/console/public/logo-dark.svg` | [console/public/logo-dark.svg](console/public/logo-dark.svg) | `${BASE_URL}logo-dark.svg` |
| `wowooai-logo.svg` | `/Users/rlw/AI项目/wowooai/console/public/wowooai-logo.svg` | [console/public/wowooai-logo.svg](console/public/wowooai-logo.svg) | `${BASE_URL}wowooai-logo.svg` |
| `wowooai.png` | `/Users/rlw/AI项目/wowooai/console/public/wowooai.png` | [console/public/wowooai.png](console/public/wowooai.png) | `${BASE_URL}wowooai.png`（背景图） |
| `wowooaiBack.png` | `/Users/rlw/AI项目/wowooai/console/public/wowooaiBack.png` | [console/public/wowooaiBack.png](console/public/wowooaiBack.png) | `${BASE_URL}wowooaiBack.png`（背景图） |

**复制命令（在仓库根目录执行）**：

```bash
cp docs/changelog/brand/favicon.svg      console/public/favicon.svg
cp docs/changelog/brand/logo-light.svg   console/public/logo-light.svg
cp docs/changelog/brand/logo-dark.svg    console/public/logo-dark.svg
cp docs/changelog/brand/wowooai-logo.svg console/public/wowooai-logo.svg
```

> ⚠️ **不要把 logo 放到 `console/src/assets/` 或其它目录**：所有引用都走 `${import.meta.env.BASE_URL}<file>`，文件必须落在 `console/public/` 顶层。

### 4.2 Header / Login logo 路径修正

source-bundle 中的 `Header.tsx` 与 `Login/index.tsx` 引用了不存在的 `dark-logo.png` / `logo.png`，需改为 `logo-dark.svg` / `logo-light.svg`：

```tsx
// console/src/layouts/Header.tsx
src={
  isDark
    ? `${import.meta.env.BASE_URL}logo-dark.svg`
    : `${import.meta.env.BASE_URL}logo-light.svg`
}
```

```tsx
// console/src/pages/Login/index.tsx
src={`${import.meta.env.BASE_URL}${
  isDark ? "logo-dark.svg" : "logo-light.svg"
}`}
```

校验：

```bash
grep -RnE 'dark-logo\.png|(^|/)logo\.png' console/src   # 期望无输出
```

### 4.3 Chat 欢迎页头像收敛到本地 favicon

source-bundle 的 `Chat/index.tsx` 与 `Chat/OptionsPanel/defaultConfig.ts` 把欢迎页头像写成了远程 alicdn 图（`https://gw.alicdn.com/imgextra/i2/O1CN01pyXzjQ1EL1PuZMlSd_!!6000000000334-2-tps-288-288.png`）。统一改为本地蓝色 favicon：

```ts
// console/src/pages/Chat/OptionsPanel/defaultConfig.ts
avatar: `${import.meta.env.BASE_URL}favicon.svg`,
```

```tsx
// console/src/pages/Chat/index.tsx — options.welcome
welcome: {
  ...i18nConfig.welcome,
  nick: "WowooAI",
  avatar: `${import.meta.env.BASE_URL}favicon.svg`,
},
```

校验：

```bash
grep -RnE 'alicdn|gw\.alicdn|wowooai-symbol\.svg' console/src   # 期望无输出
grep -Rn 'favicon.svg' console/src/pages/Chat                   # 期望两处命中
```

### 4.4 Header logo 高度

复刻时 `console/src/layouts/index.module.less` 必须保留 `.logoImg { height: 32px; width: auto; }`，详见 §1。

---

## §5 本地开发联调（dev server + 后端 CORS）

> source-bundle 的 `console/vite.config.ts` 没有内置 `server.proxy`，所以 5174 端口的 dev 直接 fetch 同源 `/api/*` 会 404；同时直连 8088 又会被 CORS 拦。两边都要补环境变量。

### 5.1 前端启动指向后端

```bash
cd console
VITE_API_BASE_URL=http://127.0.0.1:8088 pnpm dev --host --port 5174
```

`vite.config.ts` 内的 `apiBaseUrl = env.VITE_API_BASE_URL ?? ""` 在不传入时会走同源，开发环境必须显式赋值。

### 5.2 后端开放 dev 源 CORS

后端读取 `WOWOOAI_CORS_ORIGINS`（逗号分隔），仅在非空时挂载 `CORSMiddleware`：

```bash
WOWOOAI_CORS_ORIGINS="http://127.0.0.1:5174,http://localhost:5174" \
  .venv/bin/python -m wowooai app --host 127.0.0.1 --port 8088
```

校验（应返回带 `access-control-allow-origin` 的 204/200）：

```bash
curl -I -X OPTIONS http://127.0.0.1:8088/api/auth/status \
  -H 'Origin: http://127.0.0.1:5174' \
  -H 'Access-Control-Request-Method: GET'
```

### 5.3 8088 直接访问的提示语

8088 是后端 API；直接打开 `http://127.0.0.1:8088/` 会返回：

```
WowooAI Web Console is not available. If you installed WowooAI from source code,
please run `npm ci && npm run build` in WowooAI's `console/` directory, and restart
WowooAI to enable the web console.
```

这是预期行为：源码安装下，后端只在 `console/dist/` 存在时才托管 Web Console；开发期请用 5174 dev server。生产构建：

```bash
cd console && pnpm install && pnpm build
```

---

## §6 复刻整体校验清单

按本轮所有修改一次性扫一遍：

```bash
# 品牌色
grep -RnE '#FF7A3D|#FF7F16' console/public console/src   # 期望无输出（除非有意保留）

# 旧资产路径
grep -RnE 'dark-logo\.png|(^|/)logo\.png|alicdn|wowooai-symbol\.svg' console
# 期望无输出

# 残留旧品牌名
grep -RniE 'qwenpaw|copaw' console/src console/index.html console/package.json
# 期望无输出

# 主题/语言锁定
grep -n 'DEFAULT_THEME' console/src/contexts/ThemeContext.tsx
grep -n 'lng:' console/src/i18n.ts
grep -n 'changeLanguage' console/src/App.tsx
```

---

## §7 菜单与导航裁剪 / 默认智能体锁定 / 面包屑移除

> 仅前端入口裁剪，**不动后端任何服务**。被隐藏的功能在后端依然存在，路由与组件文件保留以便后续恢复，仅去掉菜单注册与路由挂载。

### §7.1 左侧菜单（Sidebar）

按用户列出的 23 项处置（保留 / 隐藏 / 改名）：

| # | 菜单 | 处置 | 备注 |
|---|---|---|---|
| 1 | 当前智能体选择器（AgentSelector） | 隐藏 | 默认锁定为 `default` |
| 2 | 聊天 chat | 保留 | |
| 3 | 频道 channels | 保留 | |
| 4 | 会话 sessions | 隐藏 | |
| 5 | 定时任务 cron-jobs | 保留 | |
| 6 | 心跳 heartbeat | 隐藏 | |
| 7 | 文件 workspace | 保留 + **改名为"记忆"** | |
| 8 | 技能 skills | 保留 | |
| 9 | 工具 tools | 隐藏 | |
| 10 | MCP | 保留 | |
| 11 | ACP / agents 入口 | 隐藏 | |
| 12 | 运行配置 agent-config | 保留，**子页面只保留"工具执行安全"** | 见 §7.2 |
| 13 | 智能体统计 | 隐藏 | |
| 14 | 智能体管理 agents | 隐藏 | |
| 15 | 模型 models | 保留 | |
| 16 | 技能池 skill-pool | 隐藏 | |
| 17 | 环境变量 environments | 隐藏 | |
| 18 | 安全 security | 隐藏（功能合并到运行配置）| |
| 19 | Token 消耗 token-usage | 保留 | |
| 20 | 备份 | 隐藏 | |
| 21 | 语音转写 voice-transcription | 隐藏 | |
| 22 | 调试 | 隐藏 | |
| 23 | 所有子页面 | **去掉面包屑导航** | 见 §7.5 |

代码改动 — `console/src/layouts/Sidebar.tsx`：

- 删除未再使用的 icon imports：`SparkUserGroupLine`、`SparkVoiceChat01Line`、`SparkInternetLine`、`SparkBrowseLine`、`SparkToolLine`、`SparkMicLine`、`SparkAgentLine`、`SparkOtherLine`。
- 删除 `import AgentSelector from "../components/AgentSelector";` 及 JSX 中 `<AgentSelector collapsed={collapsed} />` 挂载。
- `collapsedNavItems` 收敛为：`chat, channels, cron-jobs, workspace, skills, mcp, agent-config, models, token-usage`。
- `menuItems` 分组收敛为：
  - 顶层：`chat`
  - control-group：`channels, cron-jobs`（移除 sessions、heartbeat）
  - agent-group：`workspace, skills, mcp, agent-config`（移除 tools）
  - settings-group：`models, token-usage`（移除 agents、skill-pool、environments、security、voice-transcription）

### §7.2 路由与常量裁剪

`console/src/layouts/constants.ts`：

- `KEY_TO_PATH` 收敛为：`chat, channels, cron-jobs, skills, mcp, workspace, models, agent-config, token-usage`。
- `KEY_TO_LABEL` 同步裁剪。

`console/src/layouts/MainLayout/index.tsx`：

- 删除以下 page imports：`SessionsPage, HeartbeatPage, AgentConfigPage, SkillPoolPage, ToolsPage, EnvironmentsPage, VoiceTranscriptionPage, AgentsPage`。
- 同步收敛 `pathToKey` 映射。
- `<Routes>` 中删除：`/sessions、/heartbeat、/skill-pool、/tools、/agents、/environments、/security、/voice-transcription`。
- **关键路由替换**：`/agent-config` 渲染独立的"工具执行安全"页（原"运行配置→工具执行安全"tab）：

  ```tsx
  import ToolExecutionSecurityPage from "../../pages/Settings/ToolExecutionSecurity";
  // ...
  <Route path="/agent-config" element={<ToolExecutionSecurityPage />} />
  ```

  `ToolExecutionSecurityPage` 是新增的独立页（见 §8）。原 `Agent/Config` 在 source-bundle 是包含 6 个 tab 的复合页面（ReAct 智能体 / LLM 自动重试 / LLM 并发限流 / 上下文管理 / 长期记忆 / 工具执行安全）；当前只挂载工具执行安全页。

### §7.3 默认智能体锁定

`console/src/App.tsx` 在 `AppInner` 中新增首屏 effect，强制把 zustand 持久化的 `selectedAgent` 重置为 `"default"`，避免 sessionStorage 里残留的旧 agentId 选中已被隐藏的入口：

```tsx
import { useAgentStore } from "./stores/agentStore";

useEffect(() => {
  const { selectedAgent, setSelectedAgent } = useAgentStore.getState();
  if (selectedAgent !== "default") {
    setSelectedAgent("default");
  }
}, []);
```

### §7.4 顶部导航栏（Header）

按用户列出的 6 项处置：

| # | 项 | 处置 |
|---|---|---|
| 1 | 更新日志 changelog | 隐藏 |
| 2 | 文档 docs | 隐藏 |
| 3 | 常见问题 faq | 隐藏 |
| 4 | GitHub | 隐藏 |
| 5 | 语言切换 LanguageSwitcher | 隐藏 |
| 6 | 主题切换（皮肤）ThemeToggleButton | 隐藏 |

代码改动 — `console/src/layouts/Header.tsx`：

- 删除 imports：`LanguageSwitcher`、`ThemeToggleButton`、`Tooltip`、`GITHUB_URL`、`getDocsUrl`、`getFaqUrl`。
- 右侧动作区整块替换为占位空白：

  ```tsx
  <Space size="middle" />
  ```

- 仅保留版本徽标、新版本提示 Modal（Modal 内"查看 Releases"按钮仍调用 `getReleaseNotesUrl` — 这是"发现新版本"流程的内部跳转，不属于顶栏菜单项）。

### §7.5 移除面包屑（PageHeader）

`console/src/components/PageHeader/index.tsx` 重写：保留 `PageHeaderProps` 类型签名（`items / parent / current` 字段保留为可选），新实现忽略这些面包屑相关字段，只渲染 `afterBreadcrumb / subRow / center / extra`。这样 ~15 处调用方无须改动即可生效。

```tsx
export function PageHeader({
  center,
  extra,
  afterBreadcrumb,
  subRow,
  className,
}: PageHeaderProps) {
  const hasLeading = afterBreadcrumb != null || subRow != null;
  return (
    <div className={`${styles.pageHeader} ${className ?? ""}`.trim()}>
      {hasLeading ? (
        <div className={styles.leading}>
          {afterBreadcrumb ? (
            <div className={styles.leadingTop}>{afterBreadcrumb}</div>
          ) : null}
          {subRow}
        </div>
      ) : null}
      {center ? <div className={styles.center}>{center}</div> : null}
      {extra ? <div className={styles.extra}>{extra}</div> : null}
    </div>
  );
}
```

同步删除 `Fragment` import 与 `buildItemsFromParentCurrent` 辅助函数。

### §7.6 文案改名

`console/src/locales/zh.json`：

```diff
   "nav": {
     "chat": "聊天",
     ...
-    "workspace": "文件",
+    "workspace": "记忆",
```

（en/ja/ru 本轮维持原文，按用户偏好保留中文优先。）

### §7.7 构建校验

```bash
cd /Users/rlw/AI项目/wowooai/console && npm run build
```

期望：`tsc -b && vite build` 双步均通过。

### §7.8 验证清单

```bash
# 路由集合不再包含被隐藏页
grep -nE "path=\"/(sessions|heartbeat|skill-pool|tools|agents|environments|security|voice-transcription)\"" \
  console/src/layouts/MainLayout/index.tsx
# 期望无输出

# /agent-config 指向独立工具执行安全页
grep -n 'ToolExecutionSecurityPage' console/src/layouts/MainLayout/index.tsx
# 期望 import 与 element={<ToolExecutionSecurityPage />} 均命中

# AgentSelector 不再挂载
grep -n 'AgentSelector' console/src/layouts/Sidebar.tsx
# 期望无输出

# 顶栏外链按钮已清理
grep -nE 'LanguageSwitcher|ThemeToggleButton|GITHUB_URL|getDocsUrl|getFaqUrl' \
  console/src/layouts/Header.tsx
# 期望无输出

# nav.workspace 改名为"我的记忆"
grep -n '"workspace"' console/src/locales/zh.json
# 期望命中 "我的记忆"

# 默认 agent 锁定
grep -n 'setSelectedAgent("default")' console/src/App.tsx
# 期望命中

# 面包屑相关 helper 已删除
grep -n 'buildItemsFromParentCurrent' console/src/components/PageHeader/index.tsx
# 期望无输出
```

---

## §8 工具执行安全独立页

> 把原"运行配置"6 个子页面之一的 **工具执行安全** tab 抽成独立页面，只展示审批级别配置。

### §8.1 新增 UI 组件：`ToolExecutionLevelCard`

**文件**：`console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx`

该组件来自 [source-bundle/console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx](source-bundle/console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx)，提供四档审批级别：

| 值 | 中文名 | 行为含义 |
|---|---|---|
| `STRICT` | 严格模式 | 所有工具调用都需要审批 |
| `SMART` | 智能模式 | 低风险自动放行，中高风险需要审批 |
| `AUTO` | 自动模式 | 仅被明确标记为需要审批的工具才要求审批，默认值 |
| `OFF` | 关闭模式 | 关闭工具审批，工具自动执行 |

新增图标依赖来自 `lucide-react`，不需要额外品牌资产文件：

```tsx
import { Shield, CheckCircle, AlertTriangle, Ban } from "lucide-react";
```

`console/src/pages/Agent/Config/components/index.ts` 同步导出：

```ts
export { ToolExecutionLevelCard } from "./ToolExecutionLevelCard";
export type { ToolExecutionLevel } from "./ToolExecutionLevelCard";
```

### §8.2 新增独立页面：`ToolExecutionSecurityPage`

**文件**：`console/src/pages/Settings/ToolExecutionSecurity/index.tsx`

该页面源码已同步到 [source-bundle/console/src/pages/Settings/ToolExecutionSecurity/index.tsx](source-bundle/console/src/pages/Settings/ToolExecutionSecurity/index.tsx)。页面逻辑：

- 读取当前 `selectedAgent`。
- 调用 `agentsApi.getAgent(selectedAgent)` 获取 agent profile。
- 从 `profile.approval_level` 读取审批级别，缺省为 `AUTO`。
- 保存时把完整 profile 展开后更新 `approval_level`：

```tsx
const next = { ...profileRef.current, approval_level: level };
await agentsApi.updateAgent(selectedAgent, next);
```

页面只渲染一个 `ToolExecutionLevelCard` 与 Reset / Save 两个按钮，不展示原运行配置其它 5 个 tab。

### §8.3 类型与文案

`console/src/api/types/agents.ts`：

```ts
export interface AgentProfileConfig {
  // ...existing fields
  approval_level?: string;
}
```

`console/src/locales/zh.json` 在 `agentConfig` 下新增：

```json
"toolExecutionLevelTitle": "工具执行安全",
"toolExecutionLevel": {
  "title": "工具执行安全",
  "alertMessage": "配置工具调用的审批策略，控制数字员工执行工具时的安全级别",
  "strict": "严格模式",
  "strictDesc": "所有工具调用都需要审批，最高安全级别",
  "smart": "智能模式",
  "smartDesc": "低风险工具自动放行，中高风险工具需要审批",
  "auto": "自动模式",
  "autoDesc": "仅被明确标记为需要审批的工具才会要求审批（默认）",
  "off": "关闭模式",
  "offDesc": "关闭所有工具审批，所有工具自动执行"
},
"saveLevelSuccess": "工具执行安全级别已保存",
"saveLevelFailed": "保存工具执行安全级别失败"
```

同时菜单中文按最新用户术语统一：

```json
"skills": "我的技能",
"workspace": "我的记忆",
"channels": "外部渠道",
"agentConfig": "安全防护",
"models": "模型配置"
```

### §8.4 路由绑定

`console/src/layouts/MainLayout/index.tsx`：

```tsx
import ToolExecutionSecurityPage from "../../pages/Settings/ToolExecutionSecurity";

<Route path="/agent-config" element={<ToolExecutionSecurityPage />} />
```

### §8.5 校验

```bash
grep -n 'ToolExecutionSecurityPage' console/src/layouts/MainLayout/index.tsx
grep -n 'approval_level' console/src/api/types/agents.ts \
  console/src/pages/Settings/ToolExecutionSecurity/index.tsx
grep -n 'lucide-react' console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx
grep -n 'saveLevelSuccess' console/src/locales/zh.json
cd console && npm run build
```

期望：`tsc -b && vite build` 通过。

---

## §9 安全防护（/agent-config）改为复用 AgentConfigPage（仅前端）

> 2026-04-30 后续修订：跳过 §8.2 的独立 `ToolExecutionSecurityPage`，改为直接复用 `console/src/pages/Agent/Config/index.tsx`，在其内只渲染原"运行配置"6 个 tab 中的「工具执行安全」一个。后端无需任何改动。

### §9.1 路由保持不变

`console/src/layouts/MainLayout/index.tsx`：`/agent-config` 仍渲染 `AgentConfigPage`，**不再** import 也不再使用 `ToolExecutionSecurityPage`。

### §9.2 `Agent/Config/index.tsx` 裁剪到只剩工具执行安全 tab

- `dynamicTabs` 仅保留 `key: "toolExecutionLevel"` 的项；其它 5 个 tab（ReAct / LLM Retry / LLM Concurrency / Context / Memory）整块删除。
- `defaultActiveTab` 设为 `"toolExecutionLevel"`。
- 移除 `Form` import 与 `<Form form={...}>` 包裹；`useAgentConfig()` 不再返回 / 接受 `form`。
- `PageHeader` 用 `parent={t("nav.agent")} current={t("agentConfig.title")}`（"安全防护"）。
- 底部按钮：「重置」(`fetchConfig`) / 「保存」(`handleSave`)。

### §9.3 `Agent/Config/useAgentConfig.tsx` 数据源（关键）

**严禁使用 `api.getAgentRunningConfig()`** —— 该接口在 `/api/workspace/running-config`，未挂到 agent-scoped 路径，会返回 `Not Found - {"detail":"Not Found"}`，页面白屏。

正确实现与原"运行配置"第 6 个 tab 一致，使用 `agentsApi`：

```tsx
import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslation } from "react-i18next";
import { agentsApi } from "../../../api/modules/agents";
import type { AgentProfileConfig } from "../../../api/types/agents";
import { useAppMessage } from "../../../hooks/useAppMessage";
import { useAgentStore } from "../../../stores/agentStore";
import type { ToolExecutionLevel } from "./components/ToolExecutionLevelCard";

export function useAgentConfig() {
  const { t } = useTranslation();
  const { message } = useAppMessage();
  const { selectedAgent } = useAgentStore();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [approvalLevel, setApprovalLevel] =
    useState<ToolExecutionLevel>("AUTO");
  const initialApprovalLevelRef = useRef<ToolExecutionLevel>("AUTO");
  const agentProfileRef = useRef<AgentProfileConfig | null>(null);

  const fetchConfig = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const agentProfile = await agentsApi.getAgent(selectedAgent);
      agentProfileRef.current = agentProfile;
      const loadedLevel = (
        agentProfile.approval_level || "AUTO"
      ).toUpperCase() as ToolExecutionLevel;
      setApprovalLevel(loadedLevel);
      initialApprovalLevelRef.current = loadedLevel;
    } catch (err) {
      const errMsg =
        err instanceof Error ? err.message : t("agentConfig.loadFailed");
      setError(errMsg);
    } finally {
      setLoading(false);
    }
  }, [t, selectedAgent]);

  useEffect(() => {
    fetchConfig();
  }, [fetchConfig]);

  const handleSave = useCallback(async () => {
    if (!agentProfileRef.current) return;
    setSaving(true);
    try {
      const updatedProfile: AgentProfileConfig = {
        ...agentProfileRef.current,
        approval_level: approvalLevel,
      };
      await agentsApi.updateAgent(selectedAgent, updatedProfile);
      agentProfileRef.current = updatedProfile;
      initialApprovalLevelRef.current = approvalLevel;
      message.success(t("agentConfig.saveSuccess"));
    } catch (err) {
      const errMsg =
        err instanceof Error ? err.message : t("agentConfig.saveFailed");
      message.error(errMsg);
    } finally {
      setSaving(false);
    }
  }, [t, selectedAgent, approvalLevel, message]);

  return {
    loading,
    saving,
    error,
    approvalLevel,
    setApprovalLevel,
    fetchConfig,
    handleSave,
  };
}
```

要点：

- 数据源：`agentsApi.getAgent(selectedAgent)` 读取 `approval_level`；`agentsApi.updateAgent(selectedAgent, profile)` 写回。
- 用 `agentProfileRef` 缓存完整 `AgentProfileConfig`，避免保存时丢失其它字段。
- 不依赖 antd `Form`、不引入 `Promise.all` 多接口聚合，简化为单一接口流。

### §9.4 范围确认（仅前端）

- 后端 `agentsApi` 路由 `GET/PUT /api/agents/{id}` 与 `approval_level` 字段已在上游提供，无需后端改动。
- 涉及文件全部位于 `console/src/`，与 §8 共用 `ToolExecutionLevelCard` 组件、`approval_level` 类型、`agentConfig.toolExecutionLevel*` 文案。

### §9.5 校验

```bash
# /agent-config 仍由 AgentConfigPage 渲染，不再使用 ToolExecutionSecurityPage
grep -n 'ToolExecutionSecurityPage' console/src/layouts/MainLayout/index.tsx
# 期望无输出

# useAgentConfig 必须用 agentsApi，禁用 getAgentRunningConfig
grep -n 'agentsApi\|getAgentRunningConfig' console/src/pages/Agent/Config/useAgentConfig.tsx
# 期望命中 agentsApi、不命中 getAgentRunningConfig

# 后端接口连通性
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/api/agents/default
# 期望 200

cd console && npm run build
```

---

## §10 侧边栏扁平化（仅前端）

> 2026-04-30 后续修订：去掉「控制 / 工作区 / 设置」分组标题，改为按用户给定顺序的扁平菜单；样式统一品牌蓝。

### §10.1 顺序与图标

`console/src/layouts/Sidebar.tsx` 重写为纯 `<nav>` + `<button>` 渲染（移除 antd `Menu` 与 `KEY_TO_PATH`）。9 项顺序固定：

| key | i18n label | path | icon (`@agentscope-ai/icons`) |
|---|---|---|---|
| chat | nav.chat | /chat | SparkChatTabFill |
| cron-jobs | nav.cronJobs | /cron-jobs | SparkDateLine |
| skills | nav.skills | /skills | SparkMagicWandLine |
| workspace | nav.workspace | /workspace | SparkLocalFileLine |
| mcp | nav.mcp | /mcp | SparkMcpMcpLine |
| channels | nav.channels | /channels | SparkWifiLine |
| agent-config | nav.agentConfig | /agent-config | SparkModifyLine |
| models | nav.models | /models | SparkModePlazaLine |
| token-usage | nav.tokenUsage | /token-usage | SparkDataLine |

折叠态用 `Tooltip` 显示 label。完整代码见 [source-bundle/console/src/layouts/Sidebar.tsx](source-bundle/console/src/layouts/Sidebar.tsx)。

### §10.2 样式：logo 放大 + 菜单/弹窗品牌色

`console/src/layouts/index.module.less` 关键变更（完整文件见 [source-bundle/console/src/layouts/index.module.less](source-bundle/console/src/layouts/index.module.less)）：

- `.logoImg { height: 32px; }`（原本更小）
- `.sidebarNavItem`：`font-family: "PingFang SC", -apple-system, ...; font-size: 14px; font-weight: 500; color: #475569;`
- hover：`background: rgba(37, 99, 235, 0.06); color: #1e40af;`
- `.sidebarNavItemActive`：`background: rgba(37, 99, 235, 0.1) !important; color: #2563eb !important; font-weight: 600;`
- `.collapsedNavItem(Active)` 同色系
- 升级 Modal `.updateModalBannerTitle / .updateModalVersionTag / .updateModalTitle / .updateViewReleasesBtn / .updateModalPrimaryBtn` 全部改用 `#2563eb / #1d4ed8`
- 删除旧 `.siderDark` 暗色覆盖（主题已锁 light）

---

## §11 外部渠道：移除「全部 / 内置 / 自定义」筛选（仅前端）

`console/src/pages/Control/Channels/index.tsx`：

- 移除 `FilterType` / `filter` 状态 / `FILTER_TABS` / 顶部 PageHeader 的 `center` 三选一按钮
- `cards` `useMemo` 简化为：启用项排前、未启用排后，不再过滤
- 仍从 `useChannels()` 取 `isBuiltin`，因为 `<ChannelDrawer isBuiltin={...} />` 还需要它

完整文件见 [source-bundle/console/src/pages/Control/Channels/index.tsx](source-bundle/console/src/pages/Control/Channels/index.tsx)。

---

## §12 我的技能：移除三个操作按钮（仅前端）

`console/src/pages/Agent/Skills/components/HeaderActions.tsx`：

- 移除 `PlusOutlined`、`SwapOutlined` 图标 import
- 删除按钮：
  - 「同步到技能池」(upload to pool，批量与非批量分支都删)
  - 「批量操作」(toggle batch mode 进入按钮，不影响批量模式内已有按钮)
  - 「创建技能」(create skill)
- 保留：刷新 / 从池下载 / 上传 zip / 从 Hub 导入；批量模式下保留 选中计数 / 全选 / 清除 / 删除 / 退出
- 接口 `HeaderActionsProps` 字段未删（`onUploadToPool / onOpenUploadPool / onCreate / onToggleBatchMode`），保持父组件无需改动

完整文件见 [source-bundle/console/src/pages/Agent/Skills/components/HeaderActions.tsx](source-bundle/console/src/pages/Agent/Skills/components/HeaderActions.tsx)。

---

## §13 全局橙色 → 品牌蓝（仅前端）

把页面里残留的橙色变量统一替换为品牌蓝 `#2563EB`，覆盖按钮、进度条、状态色、provider 图标等。

```bash
cd console
find src -type f \( -name '*.less' -o -name '*.css' -o -name '*.tsx' -o -name '*.ts' \) \
  -not -path '*/node_modules/*' \
  -exec grep -lEi '#ff7f16|#ff9d4d' {} \; \
  | xargs sed -i '' -E 's/#[fF][fF]7[fF]16/#2563EB/g; s/#[fF][fF]9[dD]4[dD]/#2563EB/g'

# 校验：应输出 0
grep -RniE '#ff7f16|#ff9d4d|#ff7a3d' src public | wc -l
```

涉及目录（替换后会写到这些文件）：`src/styles/layout.css`、`src/components/ThemeToggleButton/index.module.less`、`src/pages/Settings/{Security,Environments,Models,Agents,SkillPool,VoiceTranscription,Backups,AgentStats}/...`、`src/pages/Chat/{index.module.less,components/ChatSessionDrawer/index.module.less,components/ChatSessionItem/index.module.less,ModelSelector/index.tsx}`、`src/pages/Agent/{Tools,Workspace}/index.module.less`、`src/pages/Settings/Models/components/{providerLetterIcon.tsx,modals/local-models/LocalRuntimePanel.tsx,modals/LocalModelManageModal.tsx}`。

---

## §14 后续修订（§9–§13）的资产与快照位置

- 源码快照：[source-bundle/console/src/](source-bundle/console/src/) 下对应路径已被 §10–§12 的最新文件覆盖，复刻时直接拷贝即可
- 品牌资产：[brand/](brand/) 已包含 `favicon.svg / logo-light.svg / logo-dark.svg / wowooai-logo.svg`；`wowooai.png / wowooaiBack.png` 仍位于 [source-bundle/console/public/](source-bundle/console/public/)
- 复刻顺序：先按 §1–§8 完成基础本地化，再依序应用 §9–§13；最后 `cd console && npm run build` 做最终校验

---

## §15 2026-04-30 实际落地复刻顺序（前端）

> 本节把 `applied-2026-04-30.md` 的前端实际落地内容合并到 frontend changelog。以后从干净上游前端复刻时，按 §1–§15 执行即可，不需要再看 applied 文件。

### §15.1 品牌与包元数据

```bash
cd /Users/rlw/AI项目/wowooai

# 静态资产：svg 权威来源放在 brand；png 保留在 source-bundle/console/public
cp docs/changelog/brand/favicon.svg      console/public/favicon.svg
cp docs/changelog/brand/logo-light.svg   console/public/logo-light.svg
cp docs/changelog/brand/logo-dark.svg    console/public/logo-dark.svg
cp docs/changelog/brand/wowooai-logo.svg console/public/wowooai-logo.svg
cp docs/changelog/source-bundle/console/public/wowooai.png     console/public/wowooai.png
cp docs/changelog/source-bundle/console/public/wowooaiBack.png console/public/wowooaiBack.png
```

`console/index.html`：

```html
<html lang="zh-CN">
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<title>WowooAI Console</title>
```

`console/package.json`：

```json
{
  "name": "wowooai-console"
}
```

如果项目已有 `console/package-lock.json`，也必须同步顶层 `name` 与 `packages[""].name`，否则 `npm ci` / 锁文件比对会继续显示旧品牌：

```bash
python - <<'PY'
from pathlib import Path
import json
path = Path('console/package-lock.json')
if path.exists():
    data = json.loads(path.read_text())
    data['name'] = 'wowooai-console'
    if '' in data.get('packages', {}):
        data['packages']['']['name'] = 'wowooai-console'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
PY
```

### §15.2 主题 / 语言锁定

直接以 source-bundle 的目标文件为准：

```bash
cp docs/changelog/source-bundle/console/src/contexts/ThemeContext.tsx console/src/contexts/ThemeContext.tsx
cp docs/changelog/source-bundle/console/src/i18n.ts                  console/src/i18n.ts
cp docs/changelog/source-bundle/console/src/App.tsx                  console/src/App.tsx
```

必须满足：

- `ThemeContext.tsx`：`DEFAULT_THEME = "light"`，去掉 localStorage 读写，`setThemeMode` / `toggleTheme` no-op
- `i18n.ts`：`lng: "zh"`、`fallbackLng: "zh"`，不再从 localStorage 读语言
- `App.tsx`：首屏 `useEffect` 强制 `i18n.changeLanguage("zh")`，并 `setSelectedAgent("default")`

### §15.3 Chat 欢迎页头像与昵称

```bash
cp docs/changelog/source-bundle/console/src/pages/Chat/OptionsPanel/defaultConfig.ts \
   console/src/pages/Chat/OptionsPanel/defaultConfig.ts
cp docs/changelog/source-bundle/console/src/pages/Chat/index.tsx \
   console/src/pages/Chat/index.tsx
```

必须满足：

```tsx
colorPrimary: "#2563EB"
avatar: `${import.meta.env.BASE_URL}favicon.svg`
```

Chat welcome 中：

```tsx
nick: "WowooAI"
avatar: `${import.meta.env.BASE_URL}favicon.svg`
```

### §15.4 菜单 / 路由 / Header / PageHeader

直接覆盖目标文件：

```bash
cp docs/changelog/source-bundle/console/src/layouts/Sidebar.tsx        console/src/layouts/Sidebar.tsx
cp docs/changelog/source-bundle/console/src/layouts/constants.ts       console/src/layouts/constants.ts
cp docs/changelog/source-bundle/console/src/layouts/MainLayout/index.tsx console/src/layouts/MainLayout/index.tsx
cp docs/changelog/source-bundle/console/src/layouts/Header.tsx         console/src/layouts/Header.tsx
cp docs/changelog/source-bundle/console/src/components/PageHeader/index.tsx console/src/components/PageHeader/index.tsx
```

覆盖后应满足：

- 左侧菜单仅 9 项：聊天 / 定时任务 / 我的技能 / 我的记忆 / MCP / 外部渠道 / 安全防护 / 模型配置 / token消耗
- 删除隐藏页路由：sessions / heartbeat / skill-pool / tools / agents / environments / security / voice-transcription / agent-stats / debug / backups
- Header 删除语言切换、主题切换、changelog/docs/faq/github 外链；右侧动作区为空 `<Space size="middle" />`
- PageHeader 保留 props 类型签名但不渲染面包屑

### §15.5 zh.json 菜单文案

```bash
cp docs/changelog/source-bundle/console/src/locales/zh.json console/src/locales/zh.json
```

关键值：

```json
{
  "nav": {
    "workspace": "我的记忆",
    "skills": "我的技能",
    "channels": "外部渠道",
    "agentConfig": "安全防护",
    "models": "模型配置"
  },
  "agentConfig": {
    "title": "安全防护",
    "toolExecutionLevelTitle": "工具执行安全"
  }
}
```

### §15.6 安全防护页：复用 AgentConfigPage，只保留工具执行安全

```bash
cp docs/changelog/source-bundle/console/src/pages/Agent/Config/index.tsx \
   console/src/pages/Agent/Config/index.tsx
cp docs/changelog/source-bundle/console/src/pages/Agent/Config/useAgentConfig.tsx \
   console/src/pages/Agent/Config/useAgentConfig.tsx
cp docs/changelog/source-bundle/console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx \
   console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx
cp docs/changelog/source-bundle/console/src/pages/Agent/Config/components/index.ts \
   console/src/pages/Agent/Config/components/index.ts
```

关键点：

- `/agent-config` 渲染 `AgentConfigPage`，不是独立 `ToolExecutionSecurityPage`
- `AgentConfigPage` 只保留 `toolExecutionLevel` tab
- `useAgentConfig.tsx` 必须使用 `agentsApi.getAgent(selectedAgent)` / `agentsApi.updateAgent(selectedAgent, profile)` 读写 `approval_level`
- 严禁使用 `api.getAgentRunningConfig()`，否则会出现 `Not Found - {"detail":"Not Found"}`

### §15.7 外部渠道 / 我的技能 / 全局配色

```bash
cp docs/changelog/source-bundle/console/src/pages/Control/Channels/index.tsx \
   console/src/pages/Control/Channels/index.tsx
cp docs/changelog/source-bundle/console/src/pages/Agent/Skills/components/HeaderActions.tsx \
   console/src/pages/Agent/Skills/components/HeaderActions.tsx
```

然后执行全局橙色替换：

```bash
cd console
find src -type f \( -name '*.less' -o -name '*.css' -o -name '*.tsx' -o -name '*.ts' \) \
  -not -path '*/node_modules/*' \
  -exec grep -lEi '#ff7f16|#ff9d4d' {} \; \
  | xargs sed -i '' -E 's/#[fF][fF]7[fF]16/#2563EB/g; s/#[fF][fF]9[dD]4[dD]/#2563EB/g'
```

### §15.8 前端完整校验

```bash
cd /Users/rlw/AI项目/wowooai/console

npm run build
# 期望：tsc -b && vite build 通过；允许 chunk-size warning

grep -RniE 'qwenpaw|copaw' src ../console/index.html package.json package-lock.json 2>/dev/null
# 期望：无输出

grep -RniE '#ff7f16|#ff9d4d|#ff7a3d' src public
# 期望：无输出

grep -n 'setSelectedAgent("default")' src/App.tsx
# 期望：命中

grep -n 'getAgentRunningConfig' src/pages/Agent/Config/useAgentConfig.tsx
# 期望：无输出

grep -n 'agentsApi' src/pages/Agent/Config/useAgentConfig.tsx
# 期望：命中
```

运行联调：

```bash
cd /Users/rlw/AI项目/wowooai/console
VITE_API_BASE_URL=http://127.0.0.1:8088 pnpm dev --host --port 5174
```

浏览器检查：

- `/agent-config`：只显示「工具执行安全」一个 tab，可保存四档审批级别
- `/channels`：无「全部 / 内置 / 自定义」筛选
- `/skills`：无「同步到技能池 / 批量操作 / 创建技能」按钮
- 左侧菜单顺序与 §15.4 一致，logo 为 32px 高，整体蓝色风格

---

## §16 2026-04-30 二次前端收敛：Chat / 模型供应商 / 外部渠道 / 配色

> 本节记录 §15 之后的前端追加收敛项。以后从干净上游前端复刻时，先执行 §15，再执行本节。

### §16.1 Chat 输入框文案与语音入口隐藏

`console/src/locales/zh.json`：

```diff
-    "inputPlaceholder": "\"↑↓\" 浏览消息 · \"/\" 快捷指令（审批时 \"/approve\" 或 \"/deny\"）",
+    "inputPlaceholder": "发消息",
```

`console/src/pages/Chat/index.tsx`：

```diff
-        allowSpeech: true,
+        allowSpeech: false,
```

效果：聊天页输入框默认提示只显示「发消息」，右侧话筒 / 语音输入入口隐藏。

校验：

```bash
grep -n '"inputPlaceholder": "发消息"' console/src/locales/zh.json
grep -n 'allowSpeech: false' console/src/pages/Chat/index.tsx
```

### §16.2 模型配置页供应商白名单

`console/src/pages/Settings/Models/index.tsx` 在 `useMemo` 内过滤 provider，只保留以下模型供应商：

| 显示名 | provider id |
|---|---|
| DashScope | `dashscope` |
| OpenAI | `openai` |
| Anthropic | `anthropic` |
| Google Gemini | `gemini` |
| DeepSeek | `deepseek` |
| Kimi (China) | `kimi-cn` |
| Zhipu (Z.AI) | `zhipu-intl` |

目标代码片段：

```tsx
  const { regularProviders, localProviders } = useMemo(() => {
    const ALLOWED_PROVIDER_IDS = new Set([
      "dashscope",
      "openai",
      "anthropic",
      "gemini",
      "deepseek",
      "kimi-cn",
      "zhipu-intl",
    ]);
    const regular: ProviderInfo[] = [];
    const local: ProviderInfo[] = [];
    for (const p of providers) {
      if (p.is_local) continue;
      if (!p.is_custom && !ALLOWED_PROVIDER_IDS.has(p.id)) {
        continue;
      }
      regular.push(p);
    }
```

说明：`is_custom` 走原逻辑兼容（用户自建供应商始终保留），白名单仅作用于内置远程供应商。所有 `is_local=true` 的供应商一律跳过，不出现在页面上。

#### 2026-05-14 修订：彻底隐藏 wowooai Local / Ollama / LM Studio

**症状**：§16.2 初次落地后，打包客户端的「模型配置」页仍能看到 wowooai Local、Ollama、LM Studio 三个本地供应商入口。

**根因**：初版过滤条件为：

```tsx
if (!p.is_custom && !ALLOWED_PROVIDER_IDS.has(p.id) && !p.is_local) {
  continue;
}
if (p.is_local) local.push(p);
else regular.push(p);
```

逻辑写成「`!is_custom && !inWhitelist && !is_local` 才跳过」——一旦 `is_local=true`，`!is_local` 为 false，整个 `&&` 短路为 false，`continue` 不触发，于是本地供应商绕过白名单进入 `local[]` 列表。后端 `provider_manager.py` 中 `wowooai-local` / `ollama` / `lmstudio` 三个都注册为 `is_local=True`（[src/wowooai/providers/provider_manager.py:583,684,702](../../src/wowooai/providers/provider_manager.py)），所以三个全部漏过。

**修复**：把 `is_local` 提升为第一道过滤条件，无条件跳过；删除 `local.push(p)` 分支（`localProviders` 永远为空数组，模板里 `localProviders.length > 0 && ...` 守卫自动不渲染）。

```tsx
for (const p of providers) {
  if (p.is_local) continue;                                  // 新增：本地供应商一律隐藏
  if (!p.is_custom && !ALLOWED_PROVIDER_IDS.has(p.id)) {
    continue;
  }
  regular.push(p);
}
```

**未改动**：`localProviders` 变量仍然解构出来并保留 `{localProviders.length > 0 && ...}` 渲染块——保持代码结构稳定，未来如需重新启用本地供应商，只要把 `if (p.is_local) continue;` 这一行改成 `if (p.is_local) { local.push(p); continue; }` 即可恢复。

**校验**：

```bash
grep -n 'if (p.is_local) continue;' console/src/pages/Settings/Models/index.tsx
# 期望命中 1 处

grep -n 'local.push' console/src/pages/Settings/Models/index.tsx
# 期望无输出（local 数组不再有写入）
```

打开「模型配置」页，不应再看到 wowooai Local / Ollama / LM Studio 任一入口。

校验：

```bash
grep -n 'ALLOWED_PROVIDER_IDS' console/src/pages/Settings/Models/index.tsx
grep -n 'zhipu-intl\|kimi-cn\|dashscope' console/src/pages/Settings/Models/index.tsx
```

### §16.3 外部渠道页渠道白名单

`console/src/pages/Control/Channels/useChannels.ts`：

只保留：控制台、钉钉、飞书、iMessage、QQ、微信、企业微信。

目标代码片段：

```tsx
  const builtinOrder = useMemo(
    () => [
      "console",
      "dingtalk",
      "feishu",
      "imessage",
      "qq",
      "weixin",
      "wecom",
    ],
    [],
  );

  const orderedKeys = useMemo(
    () => builtinOrder.filter((k) => channelTypes.includes(k)),
    [builtinOrder, channelTypes],
  );
```

关键点：不再追加 `channelTypes.filter((k) => !builtinOrder.includes(k))`，否则 API 返回的 Discord / Telegram / SIP 等仍会出现在页面中。

校验：

```bash
grep -n '"weixin"\|"wecom"' console/src/pages/Control/Channels/useChannels.ts
grep -n 'channelTypes.filter((k) => !builtinOrder.includes(k))' \
  console/src/pages/Control/Channels/useChannels.ts
# 期望无输出
```

### §16.4 蓝色按钮文字统一为白色

`console/src/styles/layout.css` 末尾追加全局 primary button 规则：

```css
/* ─── Brand-blue primary buttons must use white text ───────────────────────── */
.ant-btn-primary:not(:disabled):not([disabled]):not(.ant-btn-disabled),
.wowooai-btn-primary:not(:disabled):not([disabled]):not(.wowooai-btn-disabled) {
  color: #ffffff !important;
}
.ant-btn-primary:not(:disabled):not([disabled]) > span,
.ant-btn-primary:not(:disabled):not([disabled]) .anticon,
.wowooai-btn-primary:not(:disabled):not([disabled]) > span,
.wowooai-btn-primary:not(:disabled):not([disabled]) .anticon {
  color: #ffffff !important;
}
```

效果：蓝色主按钮不再出现黑色文字；禁用态仍沿用前文 disabled button 规则。

校验：

```bash
grep -n 'Brand-blue primary buttons must use white text' console/src/styles/layout.css
```

### §16.5 全局背景色从米白改为冷灰白

全局把旧背景色 `#F9F8F4` / `#f9f8f4` 改为冷灰白 `#F8FAFC`：

```bash
cd /Users/rlw/AI项目/wowooai/console
find src -type f \( -name '*.less' -o -name '*.css' -o -name '*.tsx' -o -name '*.ts' \) \
  -exec grep -lEi 'f9f8f4' {} \; \
  | xargs sed -i '' -E 's/#[fF]9[fF]8[fF]4/#F8FAFC/g'
```

校验：

```bash
grep -RniE 'f9f8f4' console/src
# 期望无输出

grep -RniE '#F8FAFC|#f8fafc' console/src/styles console/src/pages | head
# 期望能看到 layout.css 与相关页面样式命中
```

### §16.6 完整校验

```bash
cd /Users/rlw/AI项目/wowooai/console
npm run build
# 期望：tsc -b && vite build 通过；允许 chunk-size warning

# Chat
 grep -n '"inputPlaceholder": "发消息"' src/locales/zh.json
 grep -n 'allowSpeech: false' src/pages/Chat/index.tsx

# 模型供应商
 grep -n 'ALLOWED_PROVIDER_IDS' src/pages/Settings/Models/index.tsx
 grep -n 'dashscope\|openai\|anthropic\|gemini\|deepseek\|kimi-cn\|zhipu-intl' \
   src/pages/Settings/Models/index.tsx

# 外部渠道
 grep -n '"console"\|"dingtalk"\|"feishu"\|"imessage"\|"qq"\|"weixin"\|"wecom"' \
   src/pages/Control/Channels/useChannels.ts
 grep -n 'channelTypes.filter((k) => !builtinOrder.includes(k))' \
   src/pages/Control/Channels/useChannels.ts
 # 期望无输出

# 配色
 grep -RniE 'f9f8f4' src
 # 期望无输出
 grep -n 'Brand-blue primary buttons must use white text' src/styles/layout.css
```

---

## §17 2026-04-30 第三轮前端微调：Chat 文案 / Workspace attribution 隐藏

### §17.1 Chat 输入框与底部免责语

`console/src/locales/zh.json`：

```diff
-    "disclaimer": "懂你所需，伴你左右",
+    "disclaimer": "",
...
-    "inputPlaceholder": "发消息",
+    "inputPlaceholder": "发消息～",
```

`disclaimer` 置空后，Chat 底部"懂你所需，伴你左右"行不再渲染（消息组件按空文案隐藏整行）。`inputPlaceholder` 在 §16.1 基础上再加波浪号，最终显示「发消息～」。

校验：

```bash
grep -n '"disclaimer": ""' console/src/locales/zh.json
grep -n '"inputPlaceholder": "发消息～"' console/src/locales/zh.json
```

### §17.2 我的记忆页隐藏 OpenClaw attribution

`console/src/pages/Agent/Workspace/components/FileEditor.tsx` 删除底部段落：

```diff
-        <p className={styles.attribution}>{t("workspace.attribution")}</p>
```

`workspace.attribution` 文案保留在各 locale，只是不再渲染，便于以后需要时一键恢复。

校验：

```bash
grep -n 'workspace.attribution' console/src/pages/Agent/Workspace/components/FileEditor.tsx
# 期望无输出

cd console && npm run build
```

---

## §18 2026-04-30 增量：Cron 默认执行超时 120s → 1200s

> 配套后端 [backend.md §11](backend.md#11-2026-04-30-增量cron-默认执行超时-120s--1200s)。本节只记录前端默认表单值。

**文件**：`console/src/pages/Control/CronJobs/components/constants.ts`

新建 cron 任务时使用的默认表单值中 `runtime.timeout_seconds` 由 `120` 改为 `1200`：

```ts
import dayjs from "dayjs";

export const DEFAULT_FORM_VALUES = {
  enabled: false,
  schedule: {
    type: "cron" as const,
    cron: "0 9 * * *",
    timezone: "UTC",
  },
  cronType: "daily",
  cronTime: dayjs().hour(9).minute(0),
  task_type: "agent" as const,
  request: {
    input: "",
    session_id: "",
    user_id: "",
  },
  text: "",
  dispatch: {
    type: "channel" as const,
    channel: "console",
    target: {
      user_id: "",
      session_id: "",
    },
    mode: "final" as const,
  },
  runtime: {
    max_concurrency: 1,
    timeout_seconds: 1200,
    misfire_grace_seconds: 60,
  },
};
```

校验：

```bash
grep -n 'timeout_seconds: 1200' \
  console/src/pages/Control/CronJobs/components/constants.ts
```

---

## §19 2026-04-30 增量：前端 API base URL 修复（接口打到正确后端）

> **症状**：联调时浏览器 `/api/*` 请求或者发不出去，或者打到错误的相对路径，前端"我的记忆"等页面接口全错。
>
> **根因**：前端代码用 `declare const VITE_API_BASE_URL: string;` + 裸标识符引用环境变量，依赖 `console/vite.config.ts` 里的 `define: { VITE_API_BASE_URL: JSON.stringify(apiBaseUrl) }` 在编译期做字符串替换。Vite 6 在 dev server 下对裸标识符的 `define` 替换不稳定（实际下发到浏览器的 JS 仍是裸符号 `VITE_API_BASE_URL`，运行时 `ReferenceError`）。修复方式：统一改成 Vite 标准的 `import.meta.env.VITE_API_BASE_URL`，并新增 `.env.local` 把值固定到 `http://127.0.0.1:8088`。

### §19.1 新增 `console/.env.local`

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8088
```

> 该文件已被 Vite 默认 `.gitignore` 排除，不要提交到仓库。`.env.local` 的优先级高于命令行 `VITE_API_BASE_URL=...` 之外的所有 `.env*`，确保不论用户在哪个 shell 里启动前端，都打到本机后端。

### §19.2 `console/src/api/config.ts`

**改动 1**：删除文件顶部的 `declare const VITE_API_BASE_URL: string;`，只保留 `declare const TOKEN: string;`（Vite `vite/client` 类型已包含 `import.meta.env`）。

**改动 2**：`getApiUrl()` 中 `const base = VITE_API_BASE_URL || "";` 改为：

```ts
const base = (import.meta.env.VITE_API_BASE_URL as string | undefined) || "";
```

落地后该文件相关片段：

```ts
declare const TOKEN: string;

const AUTH_TOKEN_KEY = "wowooai_auth_token";

export function getApiUrl(path: string): string {
  const base = (import.meta.env.VITE_API_BASE_URL as string | undefined) || "";
  const apiPrefix = "/api";
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${base}${apiPrefix}${normalizedPath}`;
}
```

### §19.3 `console/src/api/modules/skill.ts`

**改动 1**：删除文件顶部的：

```ts
// Declare VITE_API_BASE_URL as global (injected by Vite)
declare const VITE_API_BASE_URL: string;
```

**改动 2**：`getStreamApiUrl()` 中 `const base = typeof VITE_API_BASE_URL === "string" ? VITE_API_BASE_URL : "";` 改为：

```ts
function getStreamApiUrl(): string {
  const base = (import.meta.env.VITE_API_BASE_URL as string | undefined) || "";
  return `${base}/api`;
}
```

### §19.4 `console/src/plugins/hostExternals.ts`

**改动**：`installHostExternals()` 中 `const apiBaseUrl = typeof VITE_API_BASE_URL !== "undefined" ? VITE_API_BASE_URL : "";` 改为：

```ts
export function installHostExternals(): void {
  const apiBaseUrl =
    (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "";
  // ...
}
```

> 该文件靠近顶部仍保留 `declare const VITE_API_BASE_URL: string;`（与全文统一删除时一并保留也可），但**实际取值必须从 `import.meta.env` 读**，不要再回退到裸标识符。

### §19.5 不需要改的地方

- `console/vite.config.ts` 中 `define: { VITE_API_BASE_URL: JSON.stringify(apiBaseUrl) }` 可保留也可删除，因为代码不再读取裸标识符；保留不会有副作用。
- 仓库内 `console/.env` / `console/.env.development` 没有也不需要新建。
- `pnpm dev` 启动命令本身不需要再带 `VITE_API_BASE_URL=http://127.0.0.1:8088`，`.env.local` 已经覆盖。

### §19.6 复刻校验

启动前端：

```bash
cd /Users/rlw/AI项目/wowooai/console
pnpm dev --host --port 5174
```

校验注入是否生效（dev server 编译产物里应该出现 `import.meta.env.VITE_API_BASE_URL` 而不是裸 `VITE_API_BASE_URL`）：

```bash
curl -s 'http://127.0.0.1:5174/src/api/config.ts?t=verify' | \
  grep -E 'import.meta.env|VITE_API_BASE_URL'
# 期望含：
#   import.meta.env = {... "VITE_API_BASE_URL": "http://127.0.0.1:8088"};
#   const base = import.meta.env.VITE_API_BASE_URL || "";

curl -s 'http://127.0.0.1:5174/src/api/modules/skill.ts?t=verify' | \
  grep -E 'import.meta.env|VITE_API_BASE_URL'
# 期望同上

# 后端联通性
curl -s http://127.0.0.1:8088/api/version
# 期望：{"version":"0.0.1"}
```

浏览器打开 `http://127.0.0.1:5174/`，"我的记忆"页面 `/api/workspace/files`、`/api/workspace/system-prompt-files` 应返回 200，不再 404。

---

## §20 2026-05-04 增量：桌面打包前端静态资源校验

> 配套后端 / 打包脚本变更见 [backend.md](backend.md) §24，打包执行步骤见 [packaging-macos.md](packaging-macos.md) / [packaging-windows.md](packaging-windows.md)。本节只记录前端构建产物要求；不修改 `console/src` 页面业务代码。

### §20.1 构建要求

桌面生产包禁止启动 Vite dev server，前端必须在 wheel 构建阶段完成：

```bash
bash scripts/wheel_build.sh
```

该脚本会执行：

```bash
(cd console && npm ci)
(cd console && npm run build)
cp -R console/dist/* src/wowooai/console/
python3 -m build --outdir dist .
```

最终 wheel 必须包含：

```text
wowooai/console/index.html
```

否则 `.app` 会启动成功但页面白屏或静态资源 404。

### §20.2 打包脚本兜底

`scripts/pack/build_macos.sh` 在复用已有 wheel 前会检查 wheel 内是否包含 `wowooai/console/index.html`。如果缺失，会删除旧 wheel 并重新执行 `scripts/wheel_build.sh`。

### §20.3 复刻校验

```bash
bash scripts/wheel_build.sh
python3 - <<'PY'
import glob, zipfile
whl = sorted(glob.glob('dist/wowooai-*.whl'))[-1]
with zipfile.ZipFile(whl) as z:
    assert any('wowooai/console/index.html' in n for n in z.namelist())
print(whl)
PY
```


---

## §21 2026-05-04 增量：前端 API base URL 改为同源相对路径

> 配套打包脚本兜底见 [packaging-macos.md](packaging-macos.md) §9；本节记录前端侧变更。

### §21.1 问题背景

桌面包启动时，后端由 `desktop_cmd.py` 随机分配空闲端口，例如：

```text
http://127.0.0.1:60494
```

但此前 `console/.env.local` 中存在：

```bash
VITE_API_BASE_URL=http://127.0.0.1:8088
```

Vite 构建会把这个值写死进 `console/dist/assets/*.js`，导致打包后的客户端页面能打开，但所有 API 都请求 `127.0.0.1:8088`，而真正后端在随机端口，接口全部 `ERR_CONNECTION_REFUSED`。

### §21.2 已落地改动

#### 删除仓库内 `console/.env.local`

仓库不再保留 `console/.env.local`。`console/src/api/config.ts` 已有逻辑：

```ts
const base = (import.meta.env.VITE_API_BASE_URL as string | undefined) || "";
return `${base}/api${normalizedPath}`;
```

当 `VITE_API_BASE_URL` 为空时，API URL 变成：

```text
/api/agents
/api/console/chat
/api/skills
```

浏览器会自动按当前页面 origin 补全，因此桌面包随机端口、命令行默认 8088、自定义端口都能正常工作。

#### `console/vite.config.ts` 增加 dev proxy

为了替代开发阶段依赖 `.env.local` 的做法，Vite dev server 增加代理：

```ts
server: {
  host: "0.0.0.0",
  port: 5173,
  proxy: (() => {
    const target = env.WOWOOAI_DEV_BACKEND || "http://127.0.0.1:8088";
    return {
      "/api": { target, changeOrigin: true },
      "/console": { target, changeOrigin: true },
    };
  })(),
},
```

开发模式使用：

```bash
# 终端 1：启动后端
wowooai app --host 127.0.0.1 --port 8088

# 终端 2：启动前端
cd console
npm run dev
```

如后端不是 8088，可临时指定：

```bash
WOWOOAI_DEV_BACKEND=http://127.0.0.1:9999 npm run dev
```

### §21.3 复刻校验

```bash
# 仓库中不应保留 .env.local
ls console/.env.local
# 期望：No such file or directory

# 构建后的前端 API 应为相对路径，不应写死 127.0.0.1:8088
cd console
VITE_API_BASE_URL="" npm run build
! grep -R "127.0.0.1:8088/api" dist/assets/*.js
```

---

## §22 2026-05-04 修复：桌面端 `send_file_to_user` 文件点击下载无响应（window.open → pywebview.save_file）

### 现象

桌面客户端中 bot 通过 `send_file_to_user` 发送的文件，对话气泡里已经显示了下载图标（§27 已修复），但**点击下载图标后没有任何反应**：

- 没有弹出系统保存对话框
- 没有新窗口打开
- `~/.wowooai/desktop.log` 无相关记录

### 根因

§27 修复了 `FileBlock` 的 URL 和字段补全，让 `@agentscope-ai/chat` 的 `DefaultCards/Files` 组件能正常渲染下载图标。但该组件的默认点击行为是 `window.open(fileInfo.url, '_blank')`：

```js
// @agentscope-ai-chat/lib/DefaultCards/Files/index.js
onClick: function onClick() {
  window.open(fileInfo.url, '_blank');
}
```

在浏览器中这会打开新标签页并触发下载。但在 pywebview WebView（macOS WKWebView / Windows WebView2）中，`window.open('_blank')` 被静默忽略——这是 WebView 安全模型的常见限制。

### 修复方案

在 `console/src/pages/Chat/index.tsx` 的 `ChatPage` 组件中，用 `useEffect` 拦截 `window.open`：

```typescript
useEffect(() => {
  const originalOpen = window.open;
  window.open = function (url, target, features) {
    const urlStr = typeof url === "string" ? url : url.toString();
    if (
      urlStr.includes("/api/files/preview/") &&
      (window as any).pywebview?.api?.save_file
    ) {
      const filename = decodeURIComponent(urlStr.split("/").pop() || "file");
      const fullUrl = urlStr.startsWith("http")
        ? urlStr
        : `${window.location.origin}${urlStr}`;
      (window as any).pywebview.api.save_file(fullUrl, filename);
      return null;
    }
    return originalOpen.call(window, url, target, features);
  };
  return () => { window.open = originalOpen; };
}, []);
```

逻辑与 `console/src/api/modules/backup.ts:exportBackup` 中已有的桌面端保存逻辑完全一致：

1. 判断 URL 是否为 `/api/files/preview/` 路径
2. 判断是否存在 `window.pywebview?.api?.save_file`
3. 存在则调用 `save_file(fullUrl, filename)` 弹出 OS 原生保存对话框
4. 不存在则回退到 `window.open`（浏览器 / Docker 模式）

### 跨平台兼容性

| 平台 | 效果 |
|---|---|
| macOS 桌面包（WKWebView） | ✅ 弹原生 Save As 对话框 |
| Windows 桌面包（WebView2） | ✅ 弹原生 Save As 对话框（`WebViewAPI.save_file` 是同一份代码） |
| 浏览器模式（`wowooai app`） | ✅ `pywebview.api` 不存在，回退 `window.open` |
| Docker / 反代 | ✅ 同浏览器模式 |

### 风险与回归

| 场景 | 影响 |
|---|---|
| 仅拦截 `/api/files/preview/` 路径，不影响其他 `window.open` 调用 | ✅ 无副作用 |
| 组件卸载时恢复原始 `window.open` | ✅ 无内存泄漏 |
| 中文文件名 | ✅ `decodeURIComponent` 正确解码 |
| Windows 非法字符 | ✅ `WebViewAPI.save_file` 内部已有 `re.sub(r'[<>:"/\\|?*]', '_', filename)` 处理 |
| 历史消息中 `file://` URL | ⚠️ 不匹配 `/api/files/preview/`，仍无效（与 §27 存量问题一致） |

---

## §23 2026-05-06 前端 UI 精简与文案调整（仅前端）

> 本节记录 4 项前端 UI 精简与文案变更：定时任务列表列精简、定时任务创建弹窗高级字段隐藏、MCP 页面创建按钮改名、外部渠道页文档链接隐藏。

### §23.1 定时任务列表 — 列精简（只隐藏不删除）

**文件**：`console/src/pages/Control/CronJobs/components/columns.tsx`

`createColumns` 返回的列中，给以下 16 列添加 `hidden: true`（Ant Design v5.29 Table 原生支持列隐藏）：

| 列 key | 列名 | hidden |
|---|---|---|
| `id` | ID | ✅ |
| `schedule_type` | ScheduleType | ✅ |
| `timezone` | Timezone | ✅ |
| `task_type` | TaskType | ✅ |
| `text` | 消息内容（单独列） | ✅ |
| `request_input` | 请求内容（单独列） | ✅ |
| `session_id` | RequestSessionID | ✅ |
| `user_id` | RequestUserID | ✅ |
| `dispatch_type` | DispatchType | ✅ |
| `channel` | DispatchChannel | ✅ |
| `target_user_id` | DispatchTargetUserID | ✅ |
| `target_session_id` | DispatchTargetSessionID | ✅ |
| `mode` | DispatchMode | ✅ |
| `max_concurrency` | RuntimeMaxConcurrency | ✅ |
| `timeout_seconds` | RuntimeTimeoutSeconds | ✅ |
| `misfire_grace_seconds` | RuntimeMisfireGraceSeconds | ✅ |

**保留可见的列**（5 列）：

| 列 key | 列名 | 说明 |
|---|---|---|
| `name` | 任务名称 | ✅ 可见 |
| `enabled` | 启用状态 | ✅ 可见 |
| `cron` | 执行时间（含 cron 解析） | ✅ 可见 |
| `task_content` | 消息内容 + 请求内容（合并渲染） | ✅ 可见 |
| `action` | 操作 | ✅ 可见 |

> **注意**：`hidden: true` 仅为显示层隐藏，列定义和数据字段完整保留，随时可通过删除 `hidden` 一行恢复。

落地代码示例（以 `id` 列为例）：

```tsx
{
  title: handlers.t("cronJobs.id"),
  dataIndex: "id",
  key: "id",
  width: 250,
  fixed: "left",
  hidden: true,
},
```

校验：

```bash
grep -c 'hidden: true' console/src/pages/Control/CronJobs/components/columns.tsx
# 期望：16（恰好 16 个列被隐藏）
```

### §23.2 定时任务创建弹窗 — 高级字段隐藏（只隐藏不删除）

**文件**：`console/src/pages/Control/CronJobs/components/JobDrawer.tsx`

创建/编辑定时任务时，弹窗内以下 9 个 `Form.Item` 添加 `hidden` 属性，隐藏后使用 `constants.ts` 中的默认值提交：

| 字段路径 | 当前 label | hidden | 默认值来源 |
|---|---|---|---|
| `request.session_id` | RequestSessionID | ✅ | `constants.ts: "default"` |
| `request.user_id` | RequestUserID | ✅ | `constants.ts: ""` |
| `dispatch.channel` | 发送渠道 | ✅ | `constants.ts: "console"` |
| `dispatch.target.user_id` | 目标用户ID | ✅ | `constants.ts: ""` |
| `dispatch.target.session_id` | 目标会话ID | ✅ | `constants.ts: ""` |
| `dispatch.mode` | 分发模式 | ✅ | `constants.ts: "final"` |
| `runtime.max_concurrency` | 最大并发 | ✅ | `constants.ts: 1` |
| `runtime.timeout_seconds` | 超时时间 | ✅ | `constants.ts: 1200` |
| `runtime.misfire_grace_seconds` | 错过执行宽限期 | ✅ | `constants.ts: 60` |

落地方式：在对应 `<Form.Item>` 标签上追加 `hidden` 属性，保持 `name` / `rules` / `tooltip` 完整不变：

```tsx
<Form.Item
  name={["request", "session_id"]}
  label={t("cronJobs.requestSessionId")}
  tooltip={t("cronJobs.requestSessionIdTooltip")}
  hidden
>
  <Input placeholder="default" />
</Form.Item>
```

**不需要改动的文件**：`constants.ts` — 所有隐藏字段已有默认值，无需补充。

校验：

```bash
grep -c 'hidden$' console/src/pages/Control/CronJobs/components/JobDrawer.tsx
# 期望：9（恰好 9 个 Form.Item 被隐藏）

# 确认仍保留所有 name 字段（hidden 只影响渲染，不影响表单数据）
grep -n 'session_id\|user_id\|dispatch.*channel\|dispatch.*mode\|max_concurrency\|timeout_seconds\|misfire_grace' \
  console/src/pages/Control/CronJobs/components/JobDrawer.tsx
# 期望所有字段均命中
```

### §23.3 MCP 页面 — 创建按钮改名

**文件**：
- `console/src/pages/Agent/MCP/index.tsx`
- `console/src/locales/zh.json`
- `console/src/locales/en.json`

**改动**：

| 位置 | 原 key | 原文案（zh） | 新 key | 新文案（zh） | 新文案（en） |
|---|---|---|---|---|---|
| 页面顶部按钮 | `mcp.create` | 创建客户端 | `mcp.addMcp` | 新增MCP | Add MCP |
| 弹窗标题 | `mcp.create` | 创建客户端 | 未变 | 创建客户端 | Create Client |
| 弹窗确认按钮 | `common.create` | 创建 | 未变 | 创建 | Create |

**具体代码变更**：

1. `console/src/locales/zh.json` — `mcp` 下新增 key：

```diff
   "mcp": {
     "title": "MCP 客户端",
     "create": "创建客户端",
+    "addMcp": "新增MCP",
```

2. `console/src/locales/en.json` — `mcp` 下新增 key：

```diff
   "mcp": {
     "title": "MCP Clients",
     "create": "Create Client",
+    "addMcp": "Add MCP",
```

3. `console/src/pages/Agent/MCP/index.tsx` — 顶部按钮文案替换：

```diff
-  {t("mcp.create")}
+  {t("mcp.addMcp")}
```

> **说明**：仅改了页面顶部按钮显示的文字。弹窗标题仍为 `t("mcp.create")` = "创建客户端"，弹窗确认按钮仍为 `t("common.create")` = "创建"。整个 MCP 创建流程（JSON 格式导入、`createClient` API 调用、三种格式支持）完全不变。

校验：

```bash
grep -n 'mcp.addMcp' console/src/pages/Agent/MCP/index.tsx
# 期望：1 处命中

grep -n '"addMcp"' console/src/locales/zh.json console/src/locales/en.json
# 期望：2 处命中（zh + en）
```

### §23.4 外部渠道页 — 隐藏文档链接（只隐藏不删除）

**文件**：`console/src/pages/Control/Channels/components/ChannelDrawer.tsx`

渠道设置弹窗标题右侧的文档链接按钮（如"钉钉 Doc"、"飞书 Doc"等）以及 Voice 渠道的 Twilio 链接按钮，通过添加 `display: "none"` 样式隐藏：

| 按钮 | 原代码 | 隐藏方式 |
|---|---|---|
| 渠道文档链接 | `style={{ color: "#2563EB" }}` | 改为 `style={{ color: "#2563EB", display: "none" }}` |
| Voice Twilio 链接 | `style={{ color: "#2563EB" }}` | 改为 `style={{ color: "#2563EB", display: "none" }}` |

具体改动位置：`drawerTitle` 变量内两个 `<Button>` 的 `style` 属性。

> **说明**：使用 `display: "none"` 而非删除，按钮代码完整保留，只需去掉 `display: "none"` 即可恢复。相关常量 `CHANNEL_DOC_EN_URLS`、`CHANNEL_DOC_ZH_URLS`、`TWILIO_CONSOLE_URL`、`LinkOutlined` import 均保留不变。

校验：

```bash
grep -n 'display: "none"' console/src/pages/Control/Channels/components/ChannelDrawer.tsx
# 期望：2 处命中（文档链接 + Twilio 链接各 1 处）

# 确认 LinkOutlined import 和 URL 常量仍存在（未被删除）
grep -n 'LinkOutlined\|CHANNEL_DOC_EN_URLS\|TWILIO_CONSOLE_URL' \
  console/src/pages/Control/Channels/components/ChannelDrawer.tsx
# 期望均有命中
```

### §23.5 完整校验

```bash
cd /Users/rlw/AI项目/wowooai/console
npm run build
# 期望：tsc -b && vite build 通过

# columns.tsx — 16 列 hidden
grep -c 'hidden: true' src/pages/Control/CronJobs/components/columns.tsx
# 期望：16

# JobDrawer.tsx — 9 个 Form.Item hidden
grep -c 'hidden$' src/pages/Control/CronJobs/components/JobDrawer.tsx
# 期望：9

# MCP 页面 — 按钮文案
grep -n 'mcp.addMcp' src/pages/Agent/MCP/index.tsx
# 期望：1

# MCP 国际化 — zh + en
grep -n 'addMcp' src/locales/zh.json src/locales/en.json
# 期望：2

# ChannelDrawer — 文档链接隐藏
grep -c 'display: "none"' src/pages/Control/Channels/components/ChannelDrawer.tsx
# 期望：2
```

---

## §24 2026-05-06 修复：定时任务列表 hidden 列未真正隐藏，操作列布局异常

### 现象

定时任务页面表格异常：任务名称后面有大段空白，然后才是操作栏。看起来操作栏直接跟在名称后面。

### 根因

`columns.tsx` 中 16 个列设置了 `hidden: true`，但 `hidden` 不是 antd v5 `Table` 的标准 `ColumnType` 字段（antd 5.13+ 才正式支持），传入后被忽略。所有"隐藏"列实际都被渲染了，每列都有 `width`，合计约 2400px。`index.tsx` 的 `scroll={{ x: 2840 }}` 又按所有列宽度总和设置，导致表格横向滚动区域极大，hidden 列内容是空白 / `-`，使可见列之间隔着大段空白。

### 修复

**文件 1**：`console/src/pages/Control/CronJobs/components/columns.tsx`

`createColumns` 返回前用 `.filter()` 过滤掉 `hidden` 列：

```tsx
const all: Array<ColumnsType<CronJob>[number] & { hidden?: boolean }> = [
    // 所有列定义不变
];

return all.filter((c) => !c.hidden);
```

**文件 2**：`console/src/pages/Control/CronJobs/index.tsx`

横向滚动宽度从硬编码 2840 改为自适应：

```tsx
// 旧：scroll={{ x: 2840 }}
// 新：
scroll={{ x: "max-content" }}
```

### 效果

- 表格只渲染 4 列：名称（250）→ 启用状态（100）→ cron 表达式（180）→ 操作（160，右固定）
- 操作列 `fixed: "right"` 始终在最右侧，宽度收紧到 160px，按钮内边距 4px、间距 2px、`nowrap`，不会再撑开布局
- hidden 列定义保留在 columns.tsx 中，未来想显示某列只需去掉 `hidden: true`

### 操作列宽度收紧（同日补充）

- `columns.tsx` 操作列 `width: 240` → `160`
- `index.module.less` `.actionColumn` 加 `gap: 2px`、`justify-content: flex-start`（与表头"操作"对齐）、`flex-wrap: nowrap`、`white-space: nowrap`，并把内部 `ant-btn-link / ant-btn-text` 的 `padding-inline` 收为 `4px`

### 复刻校验

```bash
grep -n 'filter.*hidden' \
  console/src/pages/Control/CronJobs/components/columns.tsx
# 期望：1 行命中

grep -n 'max-content' \
  console/src/pages/Control/CronJobs/index.tsx
# 期望：1 行命中

grep -n '2840' console/src/pages/Control/CronJobs/index.tsx
# 期望：无输出
```

---

## §25 2026-05-12 说明：桌面控制能力无前端改动（对应 backend §33）

> 本节为占位说明。2026-05-12 新增的桌面应用控制能力（`desktop_input` / `desktop_app` 工具 + `desktop_control` 内置 skill）**完全在后端落地**，详见 [backend.md §33](backend.md#33-2026-05-12-增量新增-desktop_input--desktop_app-工具与-desktop_control-内置-skill)。

### §25.1 为什么没有前端改动

新增的两个工具与既有 `browser_use` / `desktop_screenshot` 走的是同一条工具调用链路：

- 工具元数据由 `BuiltinToolConfig` 在后端 `_default_builtin_tools()` 注册，前端「工具」列表自动展示 emoji（🖱️ / 🪟）、name、description，无需为新工具添加专属 UI。
- 工具调用与回包走 chat 现有的 `tool_call` / `tool_result` block，前端 `Chat` 组件原样渲染 JSON 文本结果。
- `desktop_control` skill 是纯 Markdown（SKILL.md），由后端 skill 池统一加载，前端「我的技能」列表通过既有接口自动出现该卡片。

### §25.2 不需要改的地方

| 模块 | 状态 |
|---|---|
| 工具列表页 | ✅ 通过 `BuiltinToolConfig` 自动渲染，无需改动 |
| 技能列表页 | ✅ 通过 skill manifest 自动渲染，无需改动 |
| Chat 工具调用气泡 | ✅ 复用现有 `tool_call` / `tool_result` 渲染 |
| 安全防护页 | ✅ 已经支持任意工具名（按 `approval_level` 全局生效�� |

### §25.3 复刻校验

```bash
# 后端启动后，前端工具列表应自动包含新工具
curl -sS http://127.0.0.1:8088/api/tools | \
  python3 -c "import json,sys; tools=json.load(sys.stdin); print([t['name'] for t in tools if t['name'].startswith('desktop_')])"
# 期望：['desktop_app', 'desktop_input', 'desktop_screenshot']

# 默认 agent 工作区应自动安装 desktop_control skill
ls ~/.wowooai/workspaces/default/skills/desktop_control-zh/SKILL.md
# 期望：文件存在
```

---

## §26 2026-05-14 撤销隐藏：恢复"数字员工选择 + 数字员工管理"入口，统一术语为"数字员工"

> 本节撤销 §7.1（隐藏数字员工选择器、数字员工管理菜单 / 路由）与 §7.3（强制锁定 `selectedAgent="default"`）的部分行为。**仅前端改动**，后端 `agentsApi` 全程未动。

### §26.1 改动总览

| 区域 | 改动 |
|---|---|
| 左侧栏顶部 | 恢复挂载 `<AgentSelector collapsed={collapsed} />`，显示"当前数字员工"下拉选择器 |
| 左侧栏菜单 | 在 `mcp` 下方新增菜单项 `agents`（数字员工管理），图标 `SparkAgentLine` |
| 路由 | 新增 `/agents` 路由，挂载 `AgentsPage`（懒加载） |
| App.tsx | 删除首屏强制 `setSelectedAgent("default")`，让 zustand persist 保留用户上次选中的数字员工 |
| 文案术语 | `zh.json` 内全部"智能体" → "数字员工"（88 处） |

### §26.2 [console/src/App.tsx](console/src/App.tsx) — 拆掉强制锁定

```diff
-import { useAgentStore } from "./stores/agentStore";
-
   useEffect(() => {
     if (i18n.language !== "zh") i18n.changeLanguage("zh");
-    const { selectedAgent, setSelectedAgent } = useAgentStore.getState();
-    if (selectedAgent !== "default") {
-      setSelectedAgent("default");
-    }
   }, [i18n]);
```

**Why**：§7.3 加的这段 effect 每次首屏都把 `selectedAgent` 重置为 `"default"`。一旦把选择器放回来，用户切换的结果立即被这段 effect 打回 default，��于白选。删除后由 zustand persist（sessionStorage）保留用户上次选中的数字员工；首次安装/清缓存的用户回退到 [agentStore.ts](console/src/stores/agentStore.ts) 的 initial state `"default"`。

### §26.3 [console/src/layouts/Sidebar.tsx](console/src/layouts/Sidebar.tsx)

**1) 新增 import**：

```tsx
import { SparkAgentLine } from "@agentscope-ai/icons";
import AgentSelector from "../components/AgentSelector";
```

**2) `navItems` 在 `mcp` 与 `channels` 之间插入 `agents`**：

```tsx
{
  key: "agents",
  icon: <SparkAgentLine size={18} />,
  path: "/agents",
  label: t("nav.agents"),
},
```

最终菜单顺序：`chat / cron-jobs / skills / workspace / mcp / agents / channels / agent-config / models / token-usage`（10 项）。

**3) `<Sider>` 内部顶部挂 AgentSelector**：

```tsx
<Sider ...>
  <AgentSelector collapsed={collapsed} />
  {renderNav()}
  ...
```

折叠态下 `AgentSelector` 自动收缩为单个 Bot 图标（组件内 `collapsed` 分支）。

### §26.4 [console/src/layouts/MainLayout/index.tsx](console/src/layouts/MainLayout/index.tsx)

```diff
+const AgentsPage = lazyImportWithRetry("../../pages/Settings/Agents");

 const pathToKey: Record<string, string> = {
   ...
   "/mcp": "mcp",
+  "/agents": "agents",
   "/workspace": "workspace",
   ...
 };

 <Routes>
   ...
   <Route path="/mcp" element={<MCPPage />} />
+  <Route path="/agents" element={<AgentsPage />} />
   <Route path="/workspace" element={<WorkspacePage />} />
   ...
 </Routes>
```

`AgentsPage` 文件本来就一直保留在 [console/src/pages/Settings/Agents/](console/src/pages/Settings/Agents/)（216 行 + `AgentTable / AgentModal / SortableAgentRow` 子组件），§7.2 只是 unmount 路由没有删文件。`useAgents.ts` + `reorder.ts` 全部沿用原逻辑，跑 `agentsApi.listAgents / createAgent / updateAgent / deleteAgent / reorderAgents / toggleAgent`。

### §26.5 [console/src/layouts/constants.ts](console/src/layouts/constants.ts) — 同步映射表

`KEY_TO_PATH` 与 `KEY_TO_LABEL` 各加 `agents` 一项。当前代码全文未引用这两个常量，仅为保持一致性。

### §26.6 [console/src/locales/zh.json](console/src/locales/zh.json) — 术语统一替换

按 auto-memory `[[feedback_terminology]]` 偏好，把所有面向用户的中文「智能体」与中文上下文里裸露的英文「Agent」统一改为「数字员工」。

**Step 1：批量替换中文「智能体」**

```bash
sed -i '' 's/智能体/数字员工/g' console/src/locales/zh.json
```

共 88 处命中，覆盖 `nav.agents / nav.agentStats / agent.* / cronJobs.* / xiaoyiSetupGuide / environments.description / agentStats.* / agentConfig.* / backups.*` 等所有面向用户的中文文案。

**Step 2：复查并手动修正中文文案中残留的英文「Agent」**

`sed` 只匹配中文，`zh.json` 中嵌在中文 tooltip / description 里的英文 `Agent` 仍会泄漏。手工逐项核对，将以下 10 处面向用户的英文 `Agent` 改为「数字员工」（保留 `ACP Agent` / `Agent Key` / `Agent ID` / 任务类型字段值 `'agent'` 等技术名）：

| 行号 | i18n key | 原文片段 | 改后片段 |
|---|---|---|---|
| L107 | `workspace.memoryFileWarning` | 一般是由 agent 主动调用 | 一般是由数字员工主动调用 |
| L592 | `channels.ackMessageTooltip` | 在 Agent 处理之前 | 在数字员工处理之前 |
| L678 | `channels.livekitRoomNameTooltip` | Agent 连入并等待 SIP 来电 | 数字员工连入并等待 SIP 来电 |
| L831 | `models.llmDescription` | 为具体 Agent 单独选择 | 为具体数字员工单独选择 |
| L1120 | `agentConfig.llmMaxConcurrentTooltip` | 所有 Agent 共享 | 所有数字员工共享 |
| L1209 | `agentConfig.timezoneTooltip` | Agent 上下文 | 数字员工上下文 |
| L1571 | `security.fileGuard.description` | 防止被 Agent 工具访问 | 防止被数字员工工具访问 |
| L1823 | `backup.agents` / `allAgents` | `{{count}} 个 Agent` / `全部 Agent` | `{{count}} 个数字员工` / `全部数字员工` |
| L1832 | `backup.progressAgent` | 第 N 个 Agent | 第 N 个数字员工 |
| L1846 | `approval.subSession` | 子 Agent | 子数字员工 |

**未改动的地方**（保留英文技术术语，符合 `[[feedback_terminology]]` 的例外条款）：
- en.json 镜像的 `Agent / Agents`
- `ACP Agent`、`Agent Key`、`Agent ID` 等技术接口/字段名
- 代码标识符 `agentsApi / AgentSummary / AgentProfileConfig / agentStore` 等
- `acp.create: "新增 Custom Agent"` / `acp.createTitle: "新增 ACP Agent"` — ACP 协议 Agent 是专有概念
- `agent.idPlaceholder: "例如：my-agent"` — 是 ID 字段格式示例字面量，不是数字员工称呼
- `cronJobs.taskTypeTooltip` / `requestInputTooltip` 中带引号的 `'agent'` — 是 `task_type` 字段的合法取值，不是文案
- `agentConfig.exemptToolNamesPlaceholder: "chat_with_agent, list_agents"` — 工具名字面量

### §26.7 校验

```bash
cd console

# 1) 路由
grep -n '"/agents"' src/layouts/MainLayout/index.tsx
# 期望：pathToKey 1 处 + <Route> 1 处

# 2) AgentSelector 挂载 + agents 菜单项
grep -n 'AgentSelector\|"agents"' src/layouts/Sidebar.tsx
# 期望：import + navItems + <AgentSelector> 至少 3 处

# 3) App.tsx 拆锁
grep -n 'setSelectedAgent("default")' src/App.tsx
# 期望：无输出

# 4) 术语
grep -c '智能体' src/locales/zh.json
# 期望：0
grep -c '数字员工' src/locales/zh.json
# 期望：99（88 处 sed 替换 + 11 处英文 Agent 手工替换；其中 backup.agents/allAgents 各贡献 1 处）

# 5) 残留英文 Agent 复核（应只剩白名单条目）
grep -nE '\bAgent[s]?\b' src/locales/zh.json
# 期望命中条目仅限：
#   - i18n key 名（"agents", "agentConfig", "agentStats", "agentKey" 等）
#   - "ACP Agent" / "Agent Key" / "Agent ID" 等技术名
#   - task_type 字段值 'agent'
#   - 工具名 chat_with_agent, list_agents
#   - ID 示例 "my-agent"

# 6) 编译
npx tsc -b --noEmit
# 期望：无错误
npm run build
# 期望：tsc -b && vite build 通过
```

### §26.8 复刻顺序

如果从干净上游 + §1–§25 复刻后想恢复本节效果：

1. 改 4 个文件：`App.tsx`、`Sidebar.tsx`、`MainLayout/index.tsx`、`constants.ts`（按 §26.2–§26.5 的 diff 应用即可）
2. 跑一次 `sed -i '' 's/智能体/数字员工/g' console/src/locales/zh.json`
3. 按 §26.6 Step 2 表格手工修正 10 处中文文案中残留的英文 `Agent`
4. `npm run build` 确认通过

---


## §27 2026-05-14 说明：浏览器默认有头模式无前端改动（对应 backend §35）

> 本节为占位说明。2026-05-14 的浏览器默认有头模式 + 登录隐私安全变更**完全在后端 / SKILL.md 层落地**，详见 [backend.md §35](backend.md#35-2026-05-14-增量browser_use--renliwo_browser-默认有头模式--登录交给用户)。

### §27.1 为什么没有前端改动

`headed` / `headless` 参数由后端工具函数控制，前端 Chat 组件只展示工具调用结果（JSON），无需为此新增 UI。登录交给用户规则是模型行为约束，通过工具 docstring 和 SKILL.md 传达，不涉及前端组件。

---

## §28 2026-05-14 修复：用户消息保留换行/空格/缩进（CSS 单行修复）

### §28.1 现象

用户在 Chat 输入框输入带换行、缩进或多空格的内容（例如粘贴一段格式化的代码片段或多行文本），点击发送后，气泡里展示成一坨连续的纯文本，所有空白字符都被折叠成单个空格。助手回复消息的换行 / 列表 / 代码块等格式正常。

### §28.2 根因

问题在依赖库 `@agentscope-ai/chat` 内部，**不在 wowooai 自身代码**。链路如下：

| 位置 | 行为 |
|---|---|
| `node_modules/@agentscope-ai/chat/lib/AgentScopeRuntimeWebUI/core/AgentScopeRuntime/Request/Card.js:8-15` | 用户消息的 TEXT 内容被打包时硬编码 `{ content: c.text, raw: true }` |
| `node_modules/@agentscope-ai/chat/lib/DefaultCards/Text/index.js:11-15` | Text 卡片把 `raw: true` 透传给 `<Markdown>` |
| `node_modules/@agentscope-ai/chat/lib/Markdown/Markdown.js:59,141` | 检测到 `raw === true` 直接短路返回 `<Raw>` 回退，跳过 Markdown 解析 |
| `node_modules/@agentscope-ai/chat/lib/Markdown/core/components/Raw.js:3-12` | 仅渲染 `<div className="...-markdown">{content}</div>`，**没有 `white-space: pre-wrap`** |

HTML 默认折叠所有空白字符，导致换行 / 缩进 / 多空格全部丢失。助手消息的 TEXT 不带 `raw` 标记（见 `Response/Message.js:26-30`），走完整 `MarkdownX` 解析，因此���受影响。

### §28.3 修复

在 [console/src/styles/layout.css](console/src/styles/layout.css) 末尾追加 4 行 CSS，仅对**用户气泡**内的 Raw 容器保留空白字符：

```css
/* ─── User message: preserve whitespace (newlines, spaces, indentation) ──── */
.wowooai-spark-bubble-end .wowooai-spark-markdown {
  white-space: pre-wrap;
}
```

**选择器解释**：

- `.wowooai-spark-bubble-end` — `<Bubble role="user">` 渲染时 `placement = "end"`，外层容器 class 由 `Bubble.js:39` 拼出 `"<prefix>-bubble-end"`。`<ConfigProvider prefix="wowooai">` 在 [console/src/App.tsx:159](console/src/App.tsx#L159) 设置，于是完整 class 是 `wowooai-spark-bubble-end`
- `.wowooai-spark-markdown` — Raw 组件用 `getPrefixCls('markdown')` 生成的容器 class，完整为 `wowooai-spark-markdown`
- 两者组合后只命中"用户气泡内的 Raw 容器"，**不影响**助手消息的正常 Markdown 渲染（助手消息走的是 `MarkdownX` 组件树，DOM 结构里没有这个 Raw `<div>`）

### §28.4 修复效果与局限

| 项目 | 修复前 | 修复后 |
|---|---|---|
| 换行符 `\n` | 折叠为空格 | ✅ 保留 |
| 多个连续空格 | 折叠为 1 个 | ✅ 保留 |
| 行首缩进 | 丢失 | ✅ 保留 |
| Markdown 标题 / 列表 / 加粗 | 原样显示标记符 | ⚠️ 仍原样显示（不是本次修复目标） |
| 代码块 ``` ``` ``` | 原样显示反引号 | ⚠️ 仍原样显示 |

如未来需要让用户消息也支持 Markdown 渲染，需要 patch 上游库 `Request/Card.js`（去掉 `raw: true`），需评估 XSS 风险，本次不做。

### §28.5 跨平台兼容性

`white-space: pre-wrap` 是 CSS 2.1 标准属性，全平台 WebView 与浏览器原生支持，无 polyfill 需求：

| 平台 | 渲染引擎 | 验证 |
|---|---|---|
| macOS（M 芯片）桌面包 | WKWebView (Safari) | ✅ |
| macOS（Intel 芯片）桌面包 | WKWebView (Safari) | ✅ |
| Windows 桌面包 | WebView2 (Chromium) | ✅ |
| 浏览器模式（`wowooai app`） | Chrome / Safari / Firefox | ✅ |

### §28.6 校验

```bash
grep -n 'wowooai-spark-bubble-end .wowooai-spark-markdown' \
  console/src/styles/layout.css
# 期望：1 处命中

cd console && npm run build
# 期望：tsc -b && vite build 通过
```

浏览器实测：在输入框粘贴一段多行带缩进的文本（例如代码片段），发送后用户气泡应保留原始换行与缩进，不再被压成一坨。

---

## §29 agent-browser 高级浏览器能力（无前端改动）

**日期**：2026-05-14
**作用域**：纯后端 + 打包；前端无改动。

### §29.1 背景

后端新增 `agent_browser` skill（封装 `npx agent-browser@0.27.0`）作为浏览器三层能力中的"高级层"，并把 `browser_cdp` 与 `agent_browser` 默认装入 default 数字员工。详见 [backend.md §37](changelog/backend.md)。

### §29.2 为何前端无改动

- 三类浏览器工具的执行结果（截图、文本、错误）都走既有 ToolBlock / TextBlock 渲染管线。
- skill 列表在前端读自后端 `/skills` 接口，新增条目自动出现在"技能"抽屉中，无需 UI 适配。
- 用户可见名称（"高级浏览（agent-browser）"）已在 SKILL.md frontmatter 配置，前端原样显示。

### §29.3 校验

```bash
cd console && npm run build
# 期望：tsc -b && vite build 通过（无前端代码改动 → 无新增 lint/类型错误）
```

启动桌面包后在 default 数字员工的"技能"面板中应能看到三个浏览器条目（基础浏览 / CDP 浏览 / 高级浏览）共存。

---

## §30 tool_result 截断阈值放宽（无前端改动）

**日期**：2026-05-14
**作用域**：纯后端配置默认值 + 用户工作区 SKILL.md；前端无改动。

### §30.1 背景

后端调整了 `ToolResultPruningConfig` 默认阈值（`pruning_old_msg_max_bytes` 3000 → 8000、`pruning_recent_n` 2 → 4），缓解中文多步工具链被反复压扁的问题。详见 [backend.md §38](changelog/backend.md)。

### §30.2 为何前端无改动

- 该配置是后端 LightContextManager 内部的"对话历史压缩"参数，不暴露到前端 API。
- 用户体感（"模型不再重复调同一工具"）来自后端行为变化，前端展示链路（消息气泡 / tool_call 块 / tool_result 块）完全不变。
- 现有 [Settings 面板](console/src/pages/Settings/) 暂未提供该参数的 UI 入口，本次也不新增——配置仍只能通过编辑 `~/.wowooai/workspaces/<id>/agent.json` 调整。

### §30.3 校验

```bash
cd console && npm run build
# 期望：tsc -b && vite build 通过（无前端代码改动 → 无新增 lint/类型错误）
```

---

## §31 2026-05-14 数字员工管理 UX 收敛：菜单收纳 / 选择器重设计 / 列表瘦身 / 创建表单精简 / 技能中文名

> 本节是 §26 之后的二次收敛。§26 把「数字员工管理」恢复为左侧菜单一级入口；本节把它**重新收纳**到顶部 `AgentSelector` 的下拉抽屉里，并配套优化选择器视觉、管理表单和列表布局。所有改动仅在前端，未触及任何后端接口。

### §31.1 改动总览

| 区域 | 改动 |
|---|---|
| 左侧菜单 | 移除 `agents` 一级菜单项（§26.3 加的那一项） |
| AgentSelector 顶部 | 用自绘 SVG 徽章替换 `favicon.svg`（避免与品牌 logo 同形） |
| AgentSelector 下拉 | 单行卡片：名称 + 当前选中 √；底部固定「数字员工管理 ›」入口跳转 `/agents` |
| AgentsPage 表格 | 名称列 300 → 200、操作列右侧固定 + `width:160` + `align:"center"`、`scroll={{ x: "max-content" }}` |
| AgentsPage 表格隐藏列 | id / workspace_dir / active_model 三列改为 `hidden: true` 并在 render 前 `filter` 掉 |
| AgentModal — 创建态 | 只渲染 3 个字段：名称 / 描述 / 初始技能；id / model / workspace_dir 仅在编辑态出现 |
| 技能选择卡片 | 卡片名从英文 skill key 翻为中文（新增 `skillNames.*` i18n 字典，未命中 fallback 到原名） |

### §31.2 [console/src/layouts/Sidebar.tsx](console/src/layouts/Sidebar.tsx) — 移除 agents 菜单项

- 删除 `import { SparkAgentLine } from "@agentscope-ai/icons";`
- 从 `navItems` 数组中删除 `{ key: "agents", icon: <SparkAgentLine size={18} />, path: "/agents", label: t("nav.agents") }` 这一项

`/agents` 路由本身保留（[MainLayout/index.tsx](console/src/layouts/MainLayout/index.tsx) 不动），由 §31.3 的下拉入口跳转进入。

### §31.3 [console/src/components/AgentSelector/index.tsx](console/src/components/AgentSelector/index.tsx) — 自绘徽章 + 下拉重构

**1) 自绘 `AgentBadge` SVG**（替换 `favicon.svg`，避免与左上角 logo 同形）：

```tsx
function AgentBadge({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="agentBadgeGrad" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#3b82f6" />
          <stop offset="100%" stopColor="#1d4ed8" />
        </linearGradient>
      </defs>
      <rect x="1.5" y="1.5" width="21" height="21" rx="6" fill="url(#agentBadgeGrad)" />
      <circle cx="12" cy="9.5" r="2.6" fill="#ffffff" />
      <path d="M6.4 17.8c1-2.4 3.1-3.6 5.6-3.6s4.6 1.2 5.6 3.6" stroke="#ffffff" strokeWidth="1.8" strokeLinecap="round" fill="none" />
      <circle cx="18.4" cy="6.2" r="1.6" fill="#ffffff" opacity="0.95" />
      <circle cx="18.4" cy="6.2" r="0.7" fill="#1d4ed8" />
    </svg>
  );
}
```

视觉：品牌蓝渐变圆角方块 + 白色人像剪影 + 右上角白底蓝心 spark 小圆点。**与 `favicon.svg` 完全不同形态**。

**2) 下拉单行 + 底部「数字员工管理」入口**：

```tsx
dropdownRender={(menu) => (
  <>
    {menu}
    <div className={styles.dropdownFooter}>
      <button className={styles.managementLink} onClick={() => { setDropdownOpen(false); navigate("/agents"); }}>
        {t("agent.management")}
        <ChevronRight size={12} strokeWidth={2.5} />
      </button>
    </div>
  </>
)}
```

每个 Option 的 `label` 与展开后的 `.agentOption` 都引用 `<AgentBadge size={16} />`，不再依赖 `BRAND_ICON_SRC = ${import.meta.env.BASE_URL}favicon.svg`。

折叠态：`.agentSelectorCollapsed` 内只渲染 `<AgentBadge size={20} />`，外加 `Tooltip` 显示当前数字员工名。

### §31.4 [console/src/components/AgentSelector/index.module.less](console/src/components/AgentSelector/index.module.less) — 配套样式

LESS 变量：

```less
@brand: #2563eb;
@brand-hover: #1d4ed8;
@brand-tint-06: rgba(37, 99, 235, 0.06);
@brand-tint-10: rgba(37, 99, 235, 0.10);
```

要点：
- `.agentSelectorCollapsed`：40×40 品牌淡蓝底，hover 加深
- `.agentSelector :global .ant-select-selector`：去边框、去阴影、纯净底，高度 32px
- `.agentOption`：单行 flex，名称 ellipsis，右侧渲染当前选中的 CheckCircle
- `.dropdownFooter`：顶部 1px 分隔线，右对齐的 `.managementLink` 文本按钮
- 完整 `.dark-mode` 覆盖（深色背景 + 调亮的品牌蓝 `#6b8df0 / #93b0ff`）

### §31.5 [AgentTable.tsx](console/src/pages/Settings/Agents/components/AgentTable.tsx) — 列表瘦身

```tsx
const columns: (ColumnsType<AgentSummary>[number] & { hidden?: boolean })[] = [
  { /* sort */ width: 56, align: "center", ... },
  { /* name */ width: 200, ellipsis: true, ... },
  { /* id */ hidden: true, ... },
  { /* description */ ellipsis: true },
  { /* workspace_dir */ hidden: true },
  { /* active_model */ hidden: true },
  { /* actions */ width: 160, fixed: "right", align: "center", ... },
];

<Table
  columns={columns.filter((c) => !c.hidden) as ColumnsType<AgentSummary>}
  scroll={{ x: "max-content" }}
  ...
/>
```

要点：
- `hidden` 是自定义字段（不属于 antd `ColumnType`），通过 `.filter()` 在 render 前丢弃
- 操作列必须配 `scroll={{ x: "max-content" }}`，否则 `fixed: "right"` 无横向滚动容器时不会触发 sticky 定位
- 拖拽列（key `sort`）保留 56px 宽度，DragHandle 居中

### §31.6 [AgentModal.tsx](console/src/pages/Settings/Agents/components/AgentModal.tsx) — 创建表单只保留 3 个字段

把 id / model 选择器 / workspace_dir 三块用 `{editingAgent && (...)}` 包裹，仅在编辑态出现：

```tsx
<Form form={form} layout="vertical" autoComplete="off">
  <Form.Item name="active_model_provider" hidden><Input /></Form.Item>
  <Form.Item name="active_model_model" hidden><Input /></Form.Item>

  {editingAgent && (
    <Form.Item name="id" label={t("agent.id")}><Input disabled /></Form.Item>
  )}
  <Form.Item name="name" label={t("agent.name")} rules={[{ required: true, ... }]}>
    <Input placeholder={t("agent.namePlaceholder")} />
  </Form.Item>
  <Form.Item name="description" label={t("agent.description")}>
    <Input.TextArea rows={3} ... />
  </Form.Item>
  {editingAgent && (
    <>
      <Form.Item label={t("agent.model")}>...</Form.Item>
      <Form.Item name="workspace_dir" label={t("agent.workspace")}>
        <Input disabled />
      </Form.Item>
    </>
  )}
</Form>
```

后端 `agentsApi.createAgent` 在缺省 id / workspace_dir / active_model 时会按当前用户的全局默认补齐，因此创建态只收 name + description + skill_names 即可。技能选择区段（下方 `pickerGrid`）不变，但分组顶部文案在创建态走 `t("agent.initialSkills")`（"初始技能"），编辑态走 `t("agent.addSkillsToAgent")`。

### §31.7 [zh.json](console/src/locales/zh.json) — 新增 `skillNames` 字典

在 `acp` 与 `skills` 之间插入：

```json
"skillNames": {
  "QA_source_index": "问答来源索引",
  "agent_browser": "高级浏览器",
  "browser_cdp": "浏览器 CDP 连接",
  "browser_visible": "可视化浏览器",
  "channel_message": "渠道消息推送",
  "chat_with_agent": "数字员工协作",
  "cron": "定时任务",
  "desktop_control": "桌面控制",
  "dingtalk_channel": "钉钉渠道接入",
  "docx": "Word 文档处理",
  "file_reader": "文件阅读",
  "guidance": "使用引导",
  "himalaya": "邮件收发",
  "make_plan": "任务规划",
  "multi_agent_collaboration": "多员工协作",
  "news": "新闻资讯",
  "onboarding-guide": "新手引导",
  "pdf": "PDF 文档处理",
  "pptx": "PPT 文档处理",
  "xlsx": "Excel 表格处理"
}
```

涵盖当前后端 builtin skill 池里所有 20 个 skill。`AgentModal` 卡片标题改为：

```tsx
<div className={styles.pickerCardTitle}>
  {t(`skillNames.${skill.name}`, skill.name)}
</div>
```

> i18next 的 `t(key, defaultValue)` 在 key 缺失时返回 `defaultValue`，所以用户自行上传的 pool skill 没有翻译条目时会原样回退到英文 skill key，不会出现 `skillNames.foo` 这种裸路径。

### §31.8 与既有章节的关系

| 章节 | 当时行为 | §31 行为 |
|---|---|---|
| §7.1 | 隐藏 AgentSelector + 隐藏数字员工管理菜单 | — |
| §7.3 | 强制 `setSelectedAgent("default")` 首屏锁定 | — |
| §26.2 | 拆掉 §7.3 的锁定 | 保持 |
| §26.3 | 把 `agents` 菜单加回侧边栏 | **撤销**（移回 AgentSelector 下拉底部） |
| §26.4 | 路由 `/agents` 挂回 MainLayout | 保持 |
| §26.6 | 智能体 → 数字员工 文案统一 | 保持 |

复刻顺序：先按 §1–§30 完成，再按 §31 应用本节 5 个文件改动。

### §31.9 校验

```bash
cd console

# 菜单不再包含 agents
grep -n '"agents"' src/layouts/Sidebar.tsx
# 期望：无输出

# AgentSelector 不再引用 favicon.svg
grep -n 'BRAND_ICON_SRC\|favicon.svg' src/components/AgentSelector/index.tsx
# 期望：无输出

# AgentSelector 自绘徽章
grep -n 'AgentBadge\|agentBadgeGrad' src/components/AgentSelector/index.tsx
# 期望：命中

# 表格操作列固定右侧
grep -n 'fixed: "right"\|max-content' src/pages/Settings/Agents/components/AgentTable.tsx
# 期望：两处命中

# 创建态字段
grep -n 'editingAgent && (' src/pages/Settings/Agents/components/AgentModal.tsx
# 期望：至少 2 处（id 包裹 + model/workspace 包裹）

# 技能中文名字典
grep -n '"skillNames"' src/locales/zh.json
# 期望：1 处命中
grep -n 'skillNames\.' src/pages/Settings/Agents/components/AgentModal.tsx
# 期望：1 处命中

# 编译
npm run build
# 期望：tsc -b && vite build 通过
```

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

浏览器实测：
- 左侧 9 项菜单（不再有"数字员工管理"）
- 顶部 AgentSelector 显示自绘蓝色徽章；点击下拉，每行只显示数字员工名，当前选中右侧带勾，下拉底部有「数字员工管理 ›」入口
- `/agents` 列表：4 列（拖拽 / 名称 / 描述 / 操作），操作列贴右侧；新建弹窗只有 名称 / 描述 / 初始技能 三块
- 技能卡片全部中文显示（如"文件阅读"、"Word 文档处理"、"高级浏览器"）

---

## §32 2026-05-14 OpenCode 供应商前端隐藏（在 API 层过滤）

> 后端 `PROVIDER_OPENCODE`（[src/wowooai/providers/provider_manager.py:598](src/wowooai/providers/provider_manager.py)）是免 API key 的内置供应商，`require_api_key=False` + 固定 `base_url`，会绕过前端各处「已配置」过滤器，出现在 Chat ModelSelector / AgentModal 的模型选择下拉里。Models 配置页因为有白名单（§16.2）所以本来就看不见，但其他选择器视而不见。

### §32.1 为何不删后端

`opencode` 字符串还被 [delegate_external_agent.py:468](src/wowooai/agents/tools/delegate_external_agent.py#L468) 作为 ACP 外部 runner 名称引用（与本节这个内置 LLM provider **同名但不同概念**：后者是个 OpenAI-兼容 LLM，前者是 ACP 协议外部 agent）。直接从 `_register_builtins` 删 `_add_builtin(PROVIDER_OPENCODE)` 不会破坏 ACP，但会让 [capability_baseline.py:617-633](src/wowooai/providers/capability_baseline.py) 的能力基线条目悬空。隐藏 ≠ 删除，保留扩展性的同时收敛 UI。

### §32.2 前端在 API 层一次性过滤

[console/src/api/modules/provider.ts](console/src/api/modules/provider.ts) 把 `listProviders()` 返回结果在缓存层就剪掉 OpenCode：

```ts
const HIDDEN_PROVIDER_IDS = new Set(["opencode"]);

export const providerApi = {
  listProviders: () => {
    if (listProvidersPromise) return listProvidersPromise;
    listProvidersPromise = request<ProviderInfo[]>("/models")
      .then((providers) =>
        providers.filter((p) => !HIDDEN_PROVIDER_IDS.has(p.id)),
      )
      .finally(() => {
        listProvidersPromise = null;
      });
    return listProvidersPromise;
  },
  // ...
};
```

要点：
- 过滤发生在 **API 客户端缓存层**，所有调用方（Models 页 / Chat ModelSelector / AgentModal / Chat 多模态能力探测 / 任何未来新增的消费者）一次到位
- 用 `Set` 而不是数组，便于以后追加屏蔽其它内置供应商（例如某天想隐藏 Azure OpenAI 也只需加一个 id）
- 保留 `Promise.then(...).finally(...)` 的链路，单飞缓存语义不变

### §32.3 与 §16.2 的关系

| 章节 | 范围 | 机制 |
|---|---|---|
| §16.2 | 仅 Models 设置页 | 页面内 `ALLOWED_PROVIDER_IDS` 白名单 |
| §32 | 全前端所有消费者 | API 层 `HIDDEN_PROVIDER_IDS` 黑名单 |

两者互补：白名单负责"只让特定 7 个供应商出现在配置页"；黑名单负责"不论哪个页面问后端要 provider 列表都不返回 opencode"。§16.2 的白名单逻辑保持不动，本节不会改变 Models 页行为。

### §32.4 校验

```bash
grep -n 'HIDDEN_PROVIDER_IDS' console/src/api/modules/provider.ts
# 期望：2 处命中（声明 + filter 调用）

cd console && npm run build
# 期望：tsc -b && vite build 通过
```

浏览器实测：
- Models 配置页 — 与之前一致（OpenCode 本来就被白名单挡掉）
- Chat 顶部模型选择下拉 — 不再出现 OpenCode
- 数字员工编辑弹窗的「模型」下拉 — 不再出现 OpenCode
- 如果上次选择记录是 OpenCode 的某模型，Chat ModelSelector 会按既有"未配置"逻辑回退到 placeholder，不会崩溃（`eligibleProviders` 找不到时 `activeProviderId` 直接是 undefined）

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

---

## §33 2026-05-14 Chat 页 UX 收敛：ModelSelector 移入发送区 / 去掉搜索入口 / 欢迎语动态化

> 本节是 §32 之后对 Chat 页的体验收敛，目标是向主流 AI 对话产品（Claude / ChatGPT）的视觉对齐，并让欢迎语随当前数字员工自适应。仅前端改动，未触及任何后端接口。

### §33.1 改动总览

| 区域 | 改动 |
|---|---|
| Chat 顶部右侧 | 移除 `<ModelSelector />`；只保留 `ChatHeaderTitle + ChatActionGroup` |
| Sender 发送区 | `sender.prefix` 槽位挂载 `<ModelSelector />`，渲染为药丸（pill）形态，与左下角附件按钮并排 |
| Sender 字符计数 | 删除 `sender.maxLength`（原值 10000），不再渲染 `0/10000` |
| ChatActionGroup | 去掉「搜索聊天」按钮（`SparkSearchLine` + `ChatSearchPanel`）；保留新建聊天 + 聊天历史 |
| 欢迎卡片 greeting | 动态注入当前数字员工的 `name`：`嗨，我是 {{name}}`；agents 列表未加载或不存在时回退到 `"WowooAI"` |
| 欢迎卡片描述 | 留空（描述文字过长，与 greeting 重复，去掉后视觉更干净） |
| 默认 prompt | 从 2 条改为 4 条平台级（非领域）能力入口 |

> **关于 ModelSelector 槽位选择**：`@agentscope-ai/chat` 的内层 `Chat/Input` 包装器（[node_modules/@agentscope-ai/chat/lib/AgentScopeRuntimeWebUI/core/Chat/Input/index.js:34-48](console/node_modules/@agentscope-ai/chat/lib/AgentScopeRuntimeWebUI/core/Chat/Input/index.js)）只把 `placeholder / disclaimer / maxLength / beforeSubmit / beforeUI / afterUI / attachments / prefix / allowSpeech / suggestions` 透传给底层 `ChatInput`，**`footer` 字段在这一层被丢弃**——所以最初挂在 `sender.footer` 的 ModelSelector 不会渲染。最终采用 `sender.prefix`（左下角，与附件按钮并排），与 Claude / ChatGPT 的标准 pattern 一致。如未来需要让它出现在右下角（原"0/10000"位置）需要 patch 上游库。

> **关于默认数字员工名**：[agentDisplayName.ts](console/src/utils/agentDisplayName.ts) 把 `id === "default"` ��� agent 名硬翻译为 `t("agent.defaultDisplayName")` = "默认数字员工"——这是仓库初始就有的逻辑（用于 §31 等列表场景的统一显示）。但 Chat 欢迎语希望显示员工**真实 name**（如默认 agent 的 `name = "wowooai"`），因此本节直接用 `currentAgentInfo?.name`，**绕过** `getAgentDisplayName`，回退值是字面量 `"WowooAI"` 而非 i18n key。

### §33.2 [ChatActionGroup/index.tsx](console/src/pages/Chat/components/ChatActionGroup/index.tsx) — 去搜索

- 删除 `SparkSearchLine` import 与 `ChatSearchPanel` import
- 删除 `searchOpen` state 与对应 `<Tooltip><IconButton/></Tooltip>` + `<ChatSearchPanel/>` 块
- `ChatSearchPanel` 组件文件保留在仓库中（未来如恢复搜索入口可直接重新挂载）

### §33.3 [ModelSelector/index.module.less](console/src/pages/Chat/ModelSelector/index.module.less) — 药丸样式

`.trigger` 从矩形按钮改为药丸：

```less
.trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  background: rgba(37, 99, 235, 0.06);
  border: 1px solid rgba(37, 99, 235, 0.12);
  max-width: 240px;

  &:hover,
  &.triggerActive {
    background: rgba(37, 99, 235, 0.12);
    border-color: rgba(37, 99, 235, 0.3);
    color: #1d4ed8;
  }
}
```

`.dark-mode .trigger` 同步改为深色药丸（背景 `rgba(37, 99, 235, 0.12)`，hover 加深到 `0.2`，文字色 `#93b0ff`）。

### §33.4 [Chat/index.tsx](console/src/pages/Chat/index.tsx) — 槽位迁移 + 动态欢迎

新增 `currentAgentInfo` 派生值（不再需要 `getAgentDisplayName`，直接用 agent 真实 name）：

```tsx
const { selectedAgent } = useAgentStore();
const agents = useAgentStore((s) => s.agents);
const currentAgentInfo = useMemo(
  () => agents.find((a) => a.id === selectedAgent),
  [agents, selectedAgent],
);
```

`options` useMemo 内：

```tsx
rightHeader: (
  <>
    <ChatSessionInitializer />
    <RuntimeLoadingBridge bridgeRef={runtimeLoadingBridgeRef} />
    <ChatHeaderTitle />
    <span style={{ flex: 1 }} />
    <ChatActionGroup />
  </>
),
welcome: {
  ...i18nConfig.welcome,
  nick: "WowooAI",
  avatar: `${import.meta.env.BASE_URL}favicon.svg`,
  greeting: t("chat.greeting", {
    name: currentAgentInfo?.name?.trim() || "WowooAI",
  }),
  description: "",
},
sender: {
  ...(i18nConfig as any)?.sender,
  beforeSubmit: handleBeforeSubmit,
  allowSpeech: false,
  prefix: <ModelSelector />,
  // ...
},
```

`useMemo` 依赖数组追加 `currentAgentInfo`，确保切换数字员工后欢迎语重新计算。

### §33.5 [OptionsPanel/defaultConfig.ts](console/src/pages/Chat/OptionsPanel/defaultConfig.ts) — 4 条 prompt + 删除 maxLength

`getPrompts` 改为返回 4 条；同时**删除** `sender.maxLength: 10000`，原本会在右下角渲染 `0/10000` 字符计数，删除后该计数消失（为 ModelSelector 让位的视觉考量也促成此调整，但本身意义独立——10000 字限制对自然对话无意义）：

```ts
const defaultConfig = {
  // ...
  sender: {
    attachments: true,
    disclaimer: "Works for you, grows with you",
    // maxLength: 10000  // 删除
  },
  // ...
};

getPrompts(t: TFunction): Array<{ value: string }> {
  return [
    { value: t("chat.prompt1") },
    { value: t("chat.prompt2") },
    { value: t("chat.prompt3") },
    { value: t("chat.prompt4") },
  ];
}
```

### §33.6 [zh.json](console/src/locales/zh.json) — 文案

```diff
-    "greeting": "你好，我今天能帮你做什么？",
-    "description": "我是一个智能助手，可以帮助你解答问题。",
-    "prompt1": "让我们开启一段新的旅程吧！",
-    "prompt2": "能告诉我你有哪些技能吗？",
+    "greeting": "嗨，我是 {{name}}",
+    "description": "告诉我你想做什么，我来执行。",
+    "prompt1": "📋 看看我能帮你做什么",
+    "prompt2": "🧰 列出可用技能",
+    "prompt3": "📝 帮我整理一份文档",
+    "prompt4": "⏰ 安排一个定时任务",
```

**Why 通用化**：未来会有 HR / IT / 销售等多个数字员工，欢迎卡片由平台层统一渲染，不应硬编码任一员工的领域文案。4 条 prompt 都映射到平台级能力（技能列表 / 文档处理 / 定时任务 / 自我介绍），任何 builtin skill 集都能响应。员工身份信息从 `agent.name` + `agent.description` 动态注入。

### §33.7 校验

```bash
cd /Users/rlw/AI项目/wowooai/console

# Search 入口已删除
grep -n 'SparkSearchLine\|ChatSearchPanel' src/pages/Chat/components/ChatActionGroup/index.tsx
# 期望：无输出

# ModelSelector 不在 rightHeader、改挂 sender.prefix
grep -n 'ModelSelector' src/pages/Chat/index.tsx
# 期望：仅 import + prefix: <ModelSelector />（2 处）

# 字符计数删除
grep -n 'maxLength' src/pages/Chat/OptionsPanel/defaultConfig.ts
# 期望：无输出

# 4 条 prompt
grep -nE '"prompt[1-4]"' src/locales/zh.json
# 期望：4 处命中

# 动态 greeting
grep -n '"greeting": "嗨，我是 {{name}}"' src/locales/zh.json
# 期望：1 处命中

# 编译
npm run build
# 期望：tsc -b && vite build 通过
```

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

浏览器实测：
- Chat 顶部右侧只剩标题与「新建聊天 / 聊天历史」按钮，**无**搜索图标、**无**模型选择器
- 发送框**左下角**（附件按钮旁边）出现蓝色药丸样式的模型选择器
- 发送框右下角不再显示 `0/10000` 字符计数
- 欢迎卡片：default 员工显示「嗨，我是 wowooai」（其 `name` 字段值），描述行留空；切换到 qa 显示「嗨，我是 入职小助手」+ 描述行留空
- 4 条快捷 prompt 居中排列在欢迎卡片下方

---

## §34 2026-05-14 §33 落地后的修正：欢迎语回退到真实 name / 描述留空 / ModelSelector 槽位 + 弹出方向 / 后端 future-annotations 崩溃

> 本节是 §33 上线后实际使用中发现的修正，集中记录以保持复刻性。前 3 条仅前端，第 4 条是配套的后端修复（不写到 backend.md，因为它是 §33 链路上"chat 一发消息就 422"的直接根因，放这里读者更好定位）。

### §34.1 欢迎语：用 agent 真实 `name`，不要走 `getAgentDisplayName`

§33.4 最初用 `getAgentDisplayName(currentAgentInfo, t)` 注入 `{{name}}`。该 helper（[console/src/utils/agentDisplayName.ts](console/src/utils/agentDisplayName.ts)）对 `id === "default"` 的 agent **强制返回** `t("agent.defaultDisplayName")` = "默认数字员工"——这是 §31 列表场景的统一显示规则，但 Chat 欢迎语希望显示员工真实身份（默认 agent 的 `name = "wowooai"`）。

修法：直接读 `currentAgentInfo?.name`，绕过 i18n 翻译；agents 列表未加载时回退到字面量 `"WowooAI"`。

```tsx
greeting: t("chat.greeting", {
  name: currentAgentInfo?.name?.trim() || "WowooAI",
}),
```

同时移除 `import { getAgentDisplayName } from "../../utils/agentDisplayName";`（在 Chat/index.tsx 内不再用到）。

### §34.2 欢迎卡片：描述留空

§33 最初让 `description` 优先取 `currentAgentInfo?.description`，回退到 `t("chat.description")`。实际渲染下 description 文字过长，与 greeting 重复，视觉拥挤。直接置空：

```tsx
description: "",
```

`chat.description` i18n key 保留在 zh.json，便于以后想再渲染时一行恢复。

### §34.3 ModelSelector 槽位：`sender.footer` → `sender.prefix`

§33.4 最初挂 `sender.footer`，**实际从未渲染**。

**根因**：`@agentscope-ai/chat` 的内层 `Chat/Input` 包装器（[node_modules/@agentscope-ai/chat/lib/AgentScopeRuntimeWebUI/core/Chat/Input/index.js:34-48](console/node_modules/@agentscope-ai/chat/lib/AgentScopeRuntimeWebUI/core/Chat/Input/index.js)）只解构透传以下字段给底层 `ChatInput`：

```js
placeholder, disclaimer, maxLength, beforeSubmit,
beforeUI, afterUI, attachments, prefix, allowSpeech, suggestions
```

`footer`、`header` 都被丢弃。底层 `ChatInput` 自身虽然接受 `footer`，但永远收不到。

**修法**：改挂 `sender.prefix`，渲染在输入框内的左前缀位置（与附件按钮并排，左下角，最接近 Claude/ChatGPT 的标准 pattern）。

```tsx
sender: {
  ...,
  prefix: <ModelSelector />,
}
```

如果未来想放到原"0/10000"位置（输入框右下角，提交按钮旁），需要 patch node_modules 或包一层 wrapper —— 当前以左下角为准。

### §34.4 ModelSelector 弹窗向上展开 + 二级菜单也向上

#### §34.4.1 一级面板：`placement="bottomLeft"` → `"topLeft"`

ModelSelector 现在挂在输入框最底下（`sender.prefix`），原 `placement="bottomLeft"` 让 antd Dropdown 向下展开，弹出内容会被 viewport 底边裁掉，且没有 fallback 滚动。

[console/src/pages/Chat/ModelSelector/index.tsx:252](console/src/pages/Chat/ModelSelector/index.tsx#L252)：

```diff
-  placement="bottomLeft"
+  placement="topLeft"
```

#### §34.4.2 二级（Provider → 模型列表）子菜单：`top: -1px` → `bottom: -1px`

一级面板向上展开后，悬停"阿里云 / DashScope" 等 provider 时弹出的二级模型子菜单仍按"对齐 providerItem 顶部、向下生长"渲染，结果模型多时（如 DashScope 有 10+ 个）超出 viewport 底边。

修复：把 `.submenu` 的锚点从 `top: -1px` 改成 `bottom: -1px`，让它"对齐 providerItem 底部、向上生长"，与一级面板方向保持一致。`max-height: 360px` + `overflow-y: auto` 一直就有，超过 360px 会出滚动条。

[console/src/pages/Chat/ModelSelector/index.module.less:125-140](console/src/pages/Chat/ModelSelector/index.module.less#L125-L140)：

```diff
 .submenu {
   display: none;
   position: absolute;
-  top: -1px;
+  bottom: -1px;
   right: 100%;
   margin-right: 2px;
   min-width: 200px;
   max-height: 360px;     // 已存在，超出会出滚动条
   overflow-y: auto;       // 已存在
   ...
 }
```

> 同方向还有 hover bridge `&::after`（覆盖 providerItem 整个高度）以及 dark-mode 覆盖，均不需要改 —— 它们都不依赖锚点是 `top` 还是 `bottom`。

### §34.5 后端：`MODEL_EXECUTION_FAILED` —— 从新 desktop 工具的 `from __future__ import annotations` 删除

> ⚠️ 这是后端修复，但属于 §33 + §34 的事故链：§25 / backend §33 引入了 `desktop_app.py` 与 `desktop_input.py` 两个新工具，文件顶部带 `from __future__ import annotations` (PEP 563)。前端聊天发出消息后，后端构造 `wowooaiAgent` 时崩溃：

```
File "src/wowooai/agents/react_agent.py", line 299, in _create_toolkit
    toolkit.register_tool_function(tool_func, ...)
File "agentscope/_utils/_common.py", line 439, in _parse_tool_function
    params_json_schema = base_model.model_json_schema()
File "pydantic/main.py", line 591, in model_json_schema
    return model_json_schema(...)
pydantic.errors.PydanticUserError: `_StructuredOutputDynamicClass` is not fully defined;
you should define `Optional`, then call `_StructuredOutputDynamicClass.model_rebuild()`.
```

**根因**：开启 PEP 563 后，`Optional[str]` 等注解变成裸字符串 `"Optional[str]"`。`agentscope._parse_tool_function` 用 `pydantic.create_model(...)` 动态建一个名叫 `_StructuredOutputDynamicClass` 的 model，再调 `model_json_schema()` —— Pydantic 在解析字符串注解时找不到 `Optional`、`List` 等符号的命名空间（`create_model` 内部没把工具模块的 globals 传过去），抛 `is not fully defined`。仓库内其它 tool 文件没有用这个 future import，所以**不要在 `src/wowooai/agents/tools/*.py` 写 `from __future__ import annotations`**。

**修法**：在两个新文件顶部去掉这一行即可，`Optional / List` 已正常 import。

```diff
 # -*- coding: utf-8 -*-
 """Desktop application lifecycle / window-focus tool."""

-from __future__ import annotations
-
 import json
 ...
 from typing import Any, List, Optional
```

[src/wowooai/agents/tools/desktop_app.py](src/wowooai/agents/tools/desktop_app.py) + [src/wowooai/agents/tools/desktop_input.py](src/wowooai/agents/tools/desktop_input.py) 同步修复。修复后必须**重启后端进程**才生效（已加载的旧 module 还在内存里）。

### §34.6 复刻校验

```bash
cd /Users/rlw/AI项目/wowooai/console

# 欢迎语用真实 name
grep -n 'currentAgentInfo?.name?.trim() || "WowooAI"' src/pages/Chat/index.tsx
# 期望：1 处命中

grep -n 'getAgentDisplayName' src/pages/Chat/index.tsx
# 期望：无输出（已不再用）

# 描述留空
grep -nE 'description: ""' src/pages/Chat/index.tsx
# 期望：1 处命中

# ModelSelector 在 prefix
grep -n 'prefix: <ModelSelector' src/pages/Chat/index.tsx
# 期望：1 处命中

# Dropdown 向上
grep -n 'placement="topLeft"' src/pages/Chat/ModelSelector/index.tsx
# 期望：1 处命中

# 二级子菜单向上
grep -n 'bottom: -1px' src/pages/Chat/ModelSelector/index.module.less
# 期望：1 处命中

# 后端工具不要用 future annotations
grep -nl 'from __future__ import annotations' \
  ../src/wowooai/agents/tools/desktop_app.py \
  ../src/wowooai/agents/tools/desktop_input.py
# 期望：无输出

# 编译
npm run build
# 期望：tsc -b && vite build 通过
```

打包同步与重启后端：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/

# 重启后端（如果之前在跑）
pkill -f "wowooai app" || true
nohup python -m wowooai app --host 127.0.0.1 --port 8088 > /tmp/wowooai-backend.log 2>&1 &
```

浏览器实测：
- 发消息不再出现 `MODEL_EXECUTION_FAILED`
- 欢迎卡片显示"嗨，我是 wowooai"（默认 agent），描述行为空
- ModelSelector 点开后：一级面板向上弹出；hover provider 后二级模型列表也向上弹出；模型超过 360px 时出现滚动条

---

## §35 2026-05-14 侧边栏新增「个人中心」置底入口，收纳 4 个二级菜单

> 把原一级菜单中的 4 个偏「设置/账户」类入口（模型配置 / 我的记忆 / 安全防护 / token 消耗）收纳到底部新增的「个人中心」折叠区。仅前端改动。

### §35.1 改动总览

| 区域 | 改动 |
|---|---|
| 一级菜单（`navItems`） | 由 9 项缩减为 5 项：`chat / cron-jobs / skills / mcp / channels` |
| 个人中心（新增，置底） | 折叠按钮 + 4 个子项，按用户给定顺序：`models / workspace / agent-config / token-usage` |
| 折叠态（72px Sider） | 个人中心渲染为单图标，点击弹出 antd `Dropdown` 菜单（`placement="topRight"`），4 个子项作为菜单项 |
| 当前路由命中其中 4 个之一时 | 个人中心按钮显示 active 态、自动展开子菜单 |
| i18n | 新增 `nav.personalCenter` = "个人中心" |

### §35.2 [console/src/layouts/Sidebar.tsx](console/src/layouts/Sidebar.tsx)

**1) 新增 import**：

```tsx
import { Layout, Button, Modal, Input, Form, Tooltip, Dropdown } from "antd";
import { useState, useEffect, useMemo } from "react";
import { SparkAccountManagementLine } from "@agentscope-ai/icons";
import { ChevronDown } from "lucide-react";
```

**2) `navItems` 缩减为 5 项**：删除 `workspace / agent-config / models / token-usage` 四项。

**3) 新增 `personalCenterItems`**（顺序固定）：

```tsx
const personalCenterItems = [
  { key: "models",       icon: <SparkModePlazaLine size={18} />, path: "/models",       label: t("nav.models") },
  { key: "workspace",    icon: <SparkLocalFileLine size={18} />, path: "/workspace",    label: t("nav.workspace") },
  { key: "agent-config", icon: <SparkModifyLine size={18} />,    path: "/agent-config", label: t("nav.agentConfig") },
  { key: "token-usage",  icon: <SparkDataLine size={18} />,      path: "/token-usage",  label: t("nav.tokenUsage") },
];

const personalCenterActive = useMemo(
  () => personalCenterItems.some((it) => it.key === selectedKey),
  [personalCenterItems, selectedKey],
);

const [personalCenterOpen, setPersonalCenterOpen] = useState(personalCenterActive);

useEffect(() => {
  if (personalCenterActive) setPersonalCenterOpen(true);
}, [personalCenterActive]);
```

**Why active 即展开**：直接通过 URL 落到 `/models` 等子页面时，sidebar 应自动展开个人中心，不能让子项处于"被折叠隐藏但又是当前页"的矛盾态。

**4) JSX：放在 `renderNav()` 之后、`authActions` 之前**（依赖 `.sidebarNav { flex: 1 }` 把后续节点压到底部）：

- 展开态：自绘 `<button>` 触发器（与 `.sidebarNavItem` 同款样式），右侧带 `<ChevronDown>` 旋转指示；展开时下方渲染缩进的子项列表
- 折叠态：单图标 + antd `Dropdown`（`placement="topRight"` 向上向右弹出，与 §34 ModelSelector 的"向上弹"思路保持一致）。Dropdown 里 4 个子项点击后调 `navigate(it.path)`

折叠态使用 antd `Dropdown` 而非自绘子菜单的原因：72px 宽度下没有渲染纵向子项的横向空间，原生 Popover 的 `placement="topRight"` 能直接把子菜单弹到 Sider 外侧，并自动处理点外关闭。

### §35.3 [console/src/layouts/index.module.less](console/src/layouts/index.module.less)

新增样式（追加在 `.authActions` 之后）：

```less
.personalCenter {
  flex-shrink: 0;
  padding: 4px 0 8px;
  border-top: 1px solid rgba(15, 23, 42, 0.06);
}

.personalCenterTrigger {
  margin-top: 4px;
  width: 100%;
}

.personalCenterChevron {
  flex-shrink: 0;
  color: #94a3b8;
  transition: transform 0.18s ease;
}

.personalCenterChevronOpen {
  transform: rotate(180deg);
  color: #2563eb;
}

.personalCenterSubmenu {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 2px;
  padding-left: 12px;
}

.personalCenterSubItem {
  height: 36px;
  font-size: 13px;
  font-weight: 400;
}
```

要点：
- `.personalCenter` 顶部 1px 分隔线，与 `.authActions` 的分隔线视觉一致
- 子项 `padding-left: 12px` + 高度 36px、字号 13px，与一级项区分缩进层级
- 不需要 `margin-top: auto` —— 上方 `.sidebarNav { flex: 1 }` 已经把 personalCenter / authActions / collapseToggleContainer 三块全部压到底部

### §35.4 [console/src/locales/zh.json](console/src/locales/zh.json)

`nav` 块末尾追加：

```diff
     "backups": "备份",
+    "personalCenter": "个人中心"
   },
```

未改 en/ja/ru —— 项目当前锁定中文（§3 `lng: "zh"` + `App.tsx` 强制 `changeLanguage("zh")`）。

### §35.5 与既有章节的关系

| 章节 | 当时行为 | §35 行为 |
|---|---|---|
| §7.1 | 隐藏部分菜单（sessions / heartbeat / tools 等） | 保持 |
| §10 | 9 项扁平化菜单 | **改写**：一级 9 项 → 5 项；4 项移入个人中心 |
| §15.4 | 9 项菜单顺序 | **改写**：仅保留前 5 项作为一级；后 4 项收纳 |
| §26.3 | 曾把 `agents` 加入一级菜单 | 与本节无冲突 — `agents` 不在个人中心 4 项内（§31 已撤销 agents 一级菜单） |
| §31.2 | 移除 `agents` 一级菜单 | 保持 — 一级菜单仍只有 5 项 |

### §35.6 校验

```bash
cd /Users/rlw/AI项目/wowooai/console

# 一级菜单只剩 5 项
grep -c '^    {$' src/layouts/Sidebar.tsx
# 视改动情况，但 navItems 数组中应只剩 chat/cron-jobs/skills/mcp/channels 5 项

grep -nE 'key: "(workspace|agent-config|models|token-usage)"' src/layouts/Sidebar.tsx
# 期望：4 处命中，全部位于 personalCenterItems 数组中（不再出现在 navItems）

# 个人中心顺序
grep -nE '"models"|"workspace"|"agent-config"|"token-usage"' src/layouts/Sidebar.tsx | head -10
# 期望：personalCenterItems 中 models 在前、token-usage 在最后

# i18n
grep -n '"personalCenter"' src/locales/zh.json
# 期望：1 处命中

grep -nE 't\("nav\.personalCenter"\)' src/layouts/Sidebar.tsx
# 期望：至少 2 处（折叠态 Tooltip + 展开态文字）

# 编译
npm run build
# 期望：tsc -b && vite build 通过
```

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

### §35.7 浏览器实测

- 展开态（240px）：左侧菜单顶部依次为「聊天 / 定时任务 / 我的技能 / MCP / 外部渠道」5 项；底部紧贴 authActions 上方出现「个人中心 ⌄」按钮，点击后向下展开 4 个缩进子项（模型配置 / 我的记忆 / 安全防护 / token消耗），雪佛龙图标旋转 180°，蓝色高亮
- 折叠态（72px）：4 个一级菜单图标 + 底部一个个人中心图标；点击图标向右上弹出 antd Dropdown 菜单，列出 4 项，hover 当前路由项加蓝色描边
- 直接访问 `/models` 等 URL：刷新后 sidebar 自动展开个人中心、子项 active 态点亮
- 切换到 `/chat` 等一级路由：个人中心按钮回到非 active 态（仍可点击展开/收起，状态保留）

## §36 2026-05-14 内置 QA Agent → 入职小助手：前端内置技能识别名单追加 `onboarding-guide`

**联动**：后端 [§39](backend.md#39-2026-05-14-内置-qa-agent-改造为入职小助手人力窝公司入职指引数字员工) 把内置 QA Agent 改造为「入职小助手」，默认技能从 `("guidance", "QA_source_index")` 改为 `("onboarding-guide",)`。

### §36.1 改动

| 文件 | 位置 | 改动 |
|---|---|---|
| [console/src/components/SkillVisual/index.tsx](../../console/src/components/SkillVisual/index.tsx#L22-L30) | `textSkillIcons` 集合 | 追加 `"onboarding-guide"` |
| [console/src/pages/Agent/Skills/components/SkillCard.tsx](../../console/src/pages/Agent/Skills/components/SkillCard.tsx#L41-L49) | `textSkillIcons` 集合 | 追加 `"onboarding-guide"` |

**保留 `"guidance"`**：避免已有用户的 wowooai QA workspace 升级后失去内置图标识别。

### §36.2 Why

前端两处 `textSkillIcons` 集合用于判定一个 skill 是否为"已知内置技能"，命中即渲染文字 emoji 图标、并在管理页标记为不可删除。新内置技能 `onboarding-guide` 不加入此集合会被误判为用户自定义技能。

### §36.3 校验

- 创建新的入职小助手 workspace 后，技能列表里 `onboarding-guide` 应显示为内置技能样式（与 `guidance` 等其他内置项一致）
- 已有 wowooai QA workspace 的 `guidance` 仍正常显示，未受影响



---

## §37 2026-05-14 §35 后续收敛：个人中心真正置底 / 模型配置页样式收紧 / 安全防护页去掉面包屑与标题

> §35 把「个人中心」加到 sidebar，但 JSX 位置错放在 `authActions` 之前，导致它实际跟在「外部渠道」一级菜单下方而非视觉最底部；同时用户反馈模型配置页样式过于"散"，以及 `/agent-config` 仍有面包屑与"安全防护"标题占位。本节修复 3 处，仅前端改动。

### §37.1 [console/src/layouts/Sidebar.tsx](console/src/layouts/Sidebar.tsx) + [index.module.less](console/src/layouts/index.module.less) — 个人中心置底

#### §37.1.1 JSX 顺序

把 `{collapsed ? (...) : (...)}` 整段个人中心 JSX 从 `renderNav()` 之后 / `authActions` 之前的位置**整体移到**所有元素之后（紧邻 `<Modal>` 之前，位于 `collapseToggleContainer` 之后），让它成为 `<Sider>` 内最后一个可视节点。

#### §37.1.2 Flex 容器修正（关键）

**症状**：仅做 §37.1.1 后浏览器端实测发现个人中心仍未贴底——它紧跟在 5 项主菜单下方，rlw 账号 / 退出登录 / 折叠按钮反而在它下面。

**根因**：`.sider { display: flex; flex-direction: column }` 应用在 antd `<Sider>` 渲染出的外层 `<aside>` 上，但 antd 把所有 children 包在内层 `<div class="ant-layout-sider-children">` 里——这才是 children 的真正父节点。外层 flex column 不会把内层 children 当作 flex item，于是 `.sidebarNav { flex: 1 }` 自始至终是 no-op，所有兄弟节点按文档流自然顺序从顶向下堆叠。

**修复**：把 flex column 与 padding/overflow 规则下沉到 `:global(.ant-layout-sider-children)`：

```less
.sider {
  background: #f7f9fc !important;
  height: calc(100vh - 64px);
  border-right: 1px solid rgba(15, 23, 42, 0.06);

  :global(.ant-layout-sider-children) {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 16px 12px 0;
    overflow: auto;
    &::-webkit-scrollbar { display: none; }
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  &.siderCollapsed {
    :global(.ant-layout-sider-children) { padding: 16px 8px 0; }
    .collapseToggleContainer { /* ... */ }
  }
}
```

修复后 `.sidebarNav { flex: 1 }` 真正生效，把 `authActions / collapseToggleContainer / personalCenter` 三块整体压到 Sider 底部；它们之间按 JSX 顺序排列（账号操作 → 折叠按钮 → 个人中心），个人中心成为视觉绝对底部节点。

**Why**：`.sidebarNav { flex: 1 }` 把后续兄弟节点压到底部；只要个人中心是最后一个兄弟节点，配合 [index.module.less](console/src/layouts/index.module.less) 中 `.personalCenter { flex-shrink: 0 }` 与顶部 1px 分隔线，就会贴在 Sider 绝对底部。

**校验**：

```bash
# personalCenter JSX 应位于 collapseToggleContainer 之后
awk '/personalCenter/{print NR}; /collapseToggleContainer/{print NR}' \
  console/src/layouts/Sidebar.tsx
# 期望 collapseToggleContainer 行号 < personalCenter 行号
```

### §37.2 模型配置页样式收紧

**改动**：

| 文件 | 改动 |
|---|---|
| [console/src/pages/Settings/Models/index.tsx](console/src/pages/Settings/Models/index.tsx) | 删除两个 `PageHeader`（顶层"LLM"+ 内层"Providers"），删除 `PageHeader` import；providers 区域改���单行 `<h3 className={styles.providersTitle}>` + 搜索框/刷新/新增按钮的横排 `.providersHeader`；移除冗余的 `.sectionHeaderRow / .searchRow / .providerGroup` 包装层 |
| [console/src/pages/Settings/Models/index.module.less](console/src/pages/Settings/Models/index.module.less) | `.content { padding: 24px }` 统一外边距；`.slotSection` 卡片去边框/去阴影/去 hover/`margin: 20px → 0`/`padding: 24px → 16px`；删除 `.providerGroup { padding: 0 16px }`、`.providersPageHeader`、`.searchRow`、`.searchBtn`、`.addProviderBtn { margin-right: 20px }`；新增 `.providersHeader`/`.providersTitle` 单行布局规则 |

**Why**：删除前页面有 4 处独立 padding/margin 来源（外层 `.content` 无 padding → `.slotSection` 自己撑 `margin: 20px` → `.providersBlock` 加 `margin-top: 32px` → 内层 `.providerGroup` 又加 `padding: 0 16px`，并叠加另一个 `PageHeader` 的 `padding: 20px`），视觉上像 4 个不相干的方块。统一到 `.content { padding: 24px }` + `.providersBlock { margin-top: 24px }` + slotSection 无外边距，整页只有一个统一边距系统。

**校验**：

```bash
grep -n 'PageHeader' console/src/pages/Settings/Models/index.tsx
# 期望：无输出（已不再用）

grep -nE '\.slotSection|\.providersBlock|\.providersHeader|\.providersTitle' \
  console/src/pages/Settings/Models/index.module.less
# 期望命中：slotSection (新轻量) / providersBlock margin-top: 24px / providersHeader / providersTitle
```

### §37.3 [console/src/pages/Agent/Config/index.tsx](console/src/pages/Agent/Config/index.tsx) — 安全防护页去掉面包屑与标题

**Why**：§7.5 把 PageHeader 神器化（只渲染 afterBreadcrumb / subRow / center / extra，忽略 parent/current）后，单纯调 `<PageHeader parent={t("nav.agent")} current={t("agentConfig.title")} />` 已经不渲染面包屑文字，但页面仍渲染一个 24px padding + 1px 底边的空白 `.pageHeader` 容器（来自 [index.module.less](console/src/pages/Agent/Config/index.module.less) 中 `.pageHeader { padding: 20px; border-bottom: 1px solid #eae9e7 }`）。同时 `<Tabs items={[{label, key: "toolExecutionLevel"}]}>` 渲染一个只有 1 项 tab 的导航条，视觉上和"标题"等价但只有一个 tab 没有意义。

**改动**（完整重写 [index.tsx](console/src/pages/Agent/Config/index.tsx)）：

- 删除 `PageHeader` import 与调用
- 删除 `Tabs` import 与单 tab 包装
- 删除内部 `useState`/`useMemo`/`useEffect` 用于 tab 切换的逻辑
- 直接渲染 `<ToolExecutionLevelCard>` 到 `<div className={styles.tabContent}>`
- 底部 `.footerActions` 按钮组保留（重置 / 保存）

[index.module.less](console/src/pages/Agent/Config/index.module.less) 把 `.tabContent { padding: 24px 16px 0 }` 顶部留 24px，补回原来由 PageHeader 提供的视觉间距。

**校验**：

```bash
grep -n 'PageHeader\|<Tabs' console/src/pages/Agent/Config/index.tsx
# 期望：无输出
```

### §37.4 完整校验

```bash
cd /Users/rlw/AI项目/wowooai/console
npm run build
# 期望：tsc -b && vite build 通过
```

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

浏览器实测：

- 左侧 sidebar 折叠态/展开态：「个人中心」按钮**贴在 Sider 绝对底部**（其下方只剩 `Modal`，不可见），账号/登出按钮位于其上方
- 模型配置页：进入后只有"默认 LLM"白色面板（无 hover 阴影/边框/外边距），其下方紧跟"Providers"单行标题 + 搜索框 + 刷新 + 新增按钮，整页边距统一为 24px
- `/agent-config` 安全防护页：进入后没有面包屑、没有"安全防护"标题、没有 tab 条，直接显示工具执行安全四档卡片


---

## §38 2026-05-14 二轮 UX 收敛：模型卡瘦身 / 我的记忆顶栏移除 / 安全防护精简 / 渠道卡精简 / 技能页筛选与文案

> §37 之后的二次收敛。涵盖 6 处页面级精简，仅前端改动。

### §38.1 模型配置页 — 默认 LLM 卡片瘦身 + 去说明文案

| 文件 | 改动 |
|---|---|
| [components/sections/ModelsSection.tsx](console/src/pages/Settings/Models/components/sections/ModelsSection.tsx) | 删除底部 `<p className={styles.slotDescription}>{t("models.llmDescription")}</p>` 段落 |
| [index.module.less](console/src/pages/Settings/Models/index.module.less) | `.slotSection` 内追加 `:global(.ant-card-head)` / `:global(.wowooai-card-head)` 高度收紧（min-height 36px、padding `0 16px`、去 border-bottom），head-title padding `8px 0` + 字号 14px，body padding `8px 16px 16px`；外层 padding 从 16 改 0 |

**Why**：原默认 LLM 卡片用 antd Card 默认 chrome（head 57px + body 24px padding），加上一行长说明文案，视觉上比下方所有 provider 卡都高得多。说明文案在 Chat 页面可以直接选模型，已经是"再说一遍"。

`models.llmDescription` 翻译保留在 [zh.json](console/src/locales/zh.json)，未来想再渲染只需把 `<p>` 段加回去。

### §38.2 我的记忆页 — 移除顶部 PageHeader（路径 + 上传/下载）

[Workspace/index.tsx](console/src/pages/Agent/Workspace/index.tsx)：

- 整个 `<PageHeader>` 块删除（含 `afterBreadcrumb`/`<p className={styles.workspacePath}>` 与 `extra`/上传下载按钮）
- 同步删除未再用的 imports：`UploadOutlined / DownloadOutlined / Button / Tooltip / workspaceApi / useRef / PageHeader / useAppMessage / useTranslation`
- 删除 `handleDownload / handleFileUpload / handleUploadClick` 三个 handler 与 `fileInputRef` / `message` 局部变量

**Why**：用户不希望在 UI 中暴露后端工作区绝对路径，也不需要前端导出/导入工作区的入口。底层 `workspaceApi.uploadFile / downloadWorkspace` 后端 API **保留**，未来想恢复入口直接重写组件即可。

### §38.3 安全防护页 — `ToolExecutionLevelCard` 去 Card 标题 + 顶部 Alert

[components/ToolExecutionLevelCard.tsx](console/src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx)：

- 去掉外层 `<Card title={<Space><Shield/>...title</Space>}>` 包装，改为纯 `<div className={styles.formCard}>`
- 去掉顶部蓝色 `<Alert type="info" message={...alertMessage} />`
- 4 个级别选项改用纯 `<div>` + 内联 border / radius / padding 样式（保留 selected 边框高亮 + hoverable 行为）
- imports 同步去掉 `Card / Alert`

`agentConfig.toolExecutionLevel.title` / `alertMessage` 文案保留在 i18n。

**Why**：§37 已经把外层页面的标题和 tab 去掉，但 `ToolExecutionLevelCard` 自身仍然有 Card 标题"工具执行安全"+ 长 Alert 提示，整页又出现了"标题感"。本次进一步把整张内层 Card 也降级为四张选项卡片直接平铺。

### §38.4 外部渠道页 — 渠道卡片去内置标签 + 去机器人前缀

[ChannelCard.tsx](console/src/pages/Control/Channels/components/ChannelCard.tsx)：

- 删除 `Middle section` 中 `{isBuiltin ? <span builtinTag>{channels.builtin}</span> : <span customTag>{channels.custom}</span>}`
- 删除整个 `Bottom section`：`<div className={styles.cardDescription}>{channels.botPrefix}: {botPrefix || channels.notSet}</div>`
- 删除局部变量 `isBuiltin / botPrefix / getConfigString`

**Why**："内置/自定义"标签和"机器人前缀: 未设置"对最终用户毫无意义；首屏只需要图标 + 名称 + 启用状态。`channels.builtin/custom/botPrefix/notSet` 文案保留。

### §38.5 我的技能页 — 移除"按标签筛选"

| 文件 | 改动 |
|---|---|
| [components/SkillsToolbar.tsx](console/src/pages/Agent/Skills/components/SkillsToolbar.tsx) | 整段 `<Select mode="multiple"... dropdownRender={SkillFilterDropdown}/>` 与对应 props（`searchTags / onTagsChange / allTags / filterOpen / onFilterOpenChange`）全部删除；`SkillFilterDropdown` import 删除 |
| [index.tsx](console/src/pages/Agent/Skills/index.tsx) | 调用处 `<SkillsToolbar>` props 同步精简；从 `useSkillsPage()` 解构中移除未再使用的 `filterOpen / setFilterOpen / searchTags / setSearchTags`（`tsconfig` 开启了 `noUnusedLocals`） |

[SkillFilterDropdown.tsx](console/src/pages/Agent/Skills/components/SkillFilterDropdown.tsx) 文件**保留**未删除——仍由 `useSkillsPage` 暴露 `allTags`，hook 与 `SkillDrawer.availableTags` 使用，必要时可一键重新挂载到 toolbar。

### §38.6 我的技能页 — "从技能池载入" → "从默认技能安装"

[zh.json](console/src/locales/zh.json)：

```diff
-    "downloadFromPoolHint": "将选中的技能池技能下载到当前工作区",
-    "downloadFromPool": "从技能池载入",
+    "downloadFromPoolHint": "从默认技能池中安装技能到当前工作区",
+    "downloadFromPool": "从默认技能安装",
```

按钮文案与 hover Tooltip 同步换。i18n key 保持不变（`skills.downloadFromPool`），所有调用方零改动。

### §38.7 PoolTransferModal — 中文显示 + 仅保留全选/清除

[PoolTransferModal.tsx](console/src/pages/Agent/Skills/components/PoolTransferModal.tsx)：

- 头部 `bulkActions` 区只保留两个按钮：「全选」(`skills.selectAll`) + 「清除」(`skills.clearSelection`)。删除中间「内置」按钮（原 `agent.selectBuiltin` + `builtinNames` 计算）
- 删除 `import { isSkillBuiltin } from "@/utils/skill"` 与 `builtinNames` 局部变量
- 卡片标题渲染从 `skill.name` 改为 `t(\`skillNames.${skill.name}\`, skill.name)`，复用 §31.7 的 `skillNames.*` 中文字典；缺翻译时 i18next 第二参 `defaultValue` 回退到原英文 key（典型场景：用户自传 pool skill）
- Tooltip 仍显示原英文 `skill.name`，方便用户识别底层 ID

**Why**：用户要求弹窗"技能名称要显示为中文"+"选项只保留圈选和清除"。

### §38.8 完整校验

```bash
cd /Users/rlw/AI项目/wowooai/console
npm run build
# 期望：tsc -b && vite build 通过

# Models card 已无 description
grep -n 'llmDescription' src/pages/Settings/Models/components/sections/ModelsSection.tsx
# 期望：无输出

# Workspace 顶栏已删
grep -n 'PageHeader\|workspaceApi' src/pages/Agent/Workspace/index.tsx
# 期望：无输出

# ToolExecutionLevelCard 不再用 Card / Alert
grep -nE '\b(Card|Alert)\b' src/pages/Agent/Config/components/ToolExecutionLevelCard.tsx
# 期望：仅 import 注释或类型;运行时 JSX 中应无 <Card> <Alert>

# Channel 卡片不再渲染 builtin / botPrefix
grep -nE 'channels.builtin|channels.botPrefix' src/pages/Control/Channels/components/ChannelCard.tsx
# 期望：无输出

# SkillsToolbar 不再有 Select / 标签筛选
grep -nE 'Select|SkillFilterDropdown|searchTags' src/pages/Agent/Skills/components/SkillsToolbar.tsx
# 期望：无输出

# 按钮文案
grep -n '"downloadFromPool"' src/locales/zh.json
# 期望命中"从默认技能安装"

# PoolTransferModal 用 skillNames.*
grep -n 'skillNames\.' src/pages/Agent/Skills/components/PoolTransferModal.tsx
# 期望：1 处命中
grep -n 'agent.selectBuiltin\|isSkillBuiltin' src/pages/Agent/Skills/components/PoolTransferModal.tsx
# 期望：无输出
```

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

### §38.9 浏览器实测

- 模型配置 → 默认 LLM 卡：高度明显减半，无说明文字行
- 我的记忆：进入直接是文件列表 + 编辑器双栏，无顶部路径行/上传下载按钮
- 安全防护：进入直接是 4 张选项卡片平铺，无标题与蓝色提示条
- 外部渠道：每张卡片只剩 图标 / 启用状态 / 渠道名 三层
- 我的技能 toolbar：搜索框旁不再有"按标签筛选"下拉
- 我的技能"从默认技能安装"按钮 → 弹窗：技能卡显示中文名（如"文件阅读"、"PDF 文档处理"）；按钮区只有「全选」和「清除」

---

## §39 2026-05-15 紧凑卡片重设计：渠道 / 模型供应商 / 默认 LLM 顶部条

> §38 在内容层做了精简（去掉无意义文案/标签），本节继续做布局层的密度优化——把外部渠道卡、Provider 卡、默认 LLM 顶部条三处统一改为「紧凑卡 + 状态徽章」风格。仅前端改动。

### §39.1 外部渠道卡片 — 单行 64px

[ChannelCard.tsx](console/src/pages/Control/Channels/components/ChannelCard.tsx)：把"图标行 / 名称行"两段式拆解为单行：

```tsx
<div className={styles.cardRow}>
  <div className={styles.channelIcon}>{getChannelIcon()}</div>
  <div className={styles.cardTitle}>{label}</div>
  <div className={styles.statusIndicator}>
    <div className={`${styles.statusDot} ...`} />
    <span className={`${styles.statusText} ...`}>{enabled ? "已启用" : "未启用"}</span>
  </div>
</div>
```

[index.module.less](console/src/pages/Control/Channels/index.module.less)：

- `.channelsGrid` 列宽 `346px → 240px`，gap `16 → 12`
- `.channelCard` `min-height 150px → 64px`，wowooai-card-body padding 0 → 12，图标 40×40 → 28×28（圆角 10 → 6）
- `.cardTitle` 单行 + ellipsis（去掉 `margin: 12px 0`），title 与状态徽章并列右侧

`.cardTopSection / .cardMiddleSection` 保留为 `display: none` 兜底，避免老的 build 缓存渲染崩坏。

### §39.2 模型供应商卡片 — 两行紧凑（隐藏 Base URL / API Key）

[RemoteProviderCard.tsx](console/src/pages/Settings/Models/components/cards/RemoteProviderCard.tsx) 重构 JSX：

- 第一行：`<ProviderIcon size=28> 名称  [内置/自定义] · · · [状态点+状态文字]`
- 第二行：`N 个模型 · · · [模型] [设置] [删除?]`
- 删除 `cardInfo / infoRow * 3` 三行（Base URL / API Key / Model 数）

[index.module.less](console/src/pages/Settings/Models/index.module.less)：

- `.providerCards` 从 `flex + min-width: 432px` 改为 `grid auto-fill minmax(320px, 1fr)`，gap `16 → 12`
- `.providerCard` 去掉 `padding-bottom: 64px`（绝对定位 actions 不再需要），padding `16 → 12`，shadow `0 4px 12px → none`（hover 才加 shadow）
- `.cardName` 字号 `16 → 14`，并入 header row 同一行
- 新增 `.cardFooterRow` / `.cardModelCount`，把模型数+按钮排在第二行
- 老规则（`.cardTitleRow / .cardInfo / .infoRow / .infoLabel / .infoValue / .infoEmpty`）置 `display: none` 兜底

### §39.3 默认 LLM 顶部条 — 单行 inline（去掉 Card 外壳）

[ModelsSection.tsx](console/src/pages/Settings/Models/components/sections/ModelsSection.tsx)：

- 删除 `<Card title>` 外壳与三个 `.slotField` 包装块
- 删除每个 Select 上方的 label（"供应商" / "模型"），直接用 placeholder
- 改为一行 flex：`"默认 LLM"  [供应商 ▾]  [模型 ▾]  [保存]`
- Save 按钮改 `size="small"`，去掉 `block`

[index.module.less](console/src/pages/Settings/Models/index.module.less)：

- 新增 `.slotInlineBar` / `.slotInlineLabel` / `.slotInlineSelect`：高度约 40px，padding `6px 12px`，单行 flex gap 8
- 老规则 `.slotForm / .slotField / .slotLabel / .visuallyHiddenLabel / .slotActionField` 保留未删（无引用即生效不渲染）；`.slotSection` 也保留为简单空壳

### §39.4 校验

```bash
cd /Users/rlw/AI项目/wowooai/console
npm run build
# 期望：tsc -b && vite build 通过

# 渠道卡单行布局
grep -n 'cardRow' src/pages/Control/Channels/components/ChannelCard.tsx
# 期望：1 处命中

# Provider 卡 Base URL / API Key 已去
grep -nE 'Base URL|API Key' src/pages/Settings/Models/components/cards/RemoteProviderCard.tsx
# 期望：无输出

# Provider 卡 footer row
grep -n 'cardFooterRow\|cardModelCount' src/pages/Settings/Models/components/cards/RemoteProviderCard.tsx
# 期望：各 1 处

# LLM 改为 inline bar
grep -n 'slotInlineBar' src/pages/Settings/Models/components/sections/ModelsSection.tsx
# 期望：1 处
grep -n '<Card ' src/pages/Settings/Models/components/sections/ModelsSection.tsx
# 期望：无输出
```

### §39.5 浏览器实测

- 外部渠道：每行容纳 4–5 张卡片（视屏宽），每张 64px 高，单行排布"图标 飞书 ●已启用"
- 模型配置 - 默认 LLM：顶部一条 40px 高的横条，"默认 LLM  [DashScope ▾]  [qwen-max ▾]  [保存]"
- 模型配置 - Providers：每张卡 ~80px 高，标题行 + 模型数/按钮行；Base URL / API Key 不再露出



---

## §40 2026-05-15 员工记忆移出个人中心 / 技能页工具条重设计 / 折叠态图标对齐 / 个人中心置底 / md 编辑切换

> §35 把 4 个"设置类"页面收纳到底部「个人中心」折叠区，但「我的记忆」其实是日常使用频率很高的内容入口，不该藏在"个人中心"里。本节把它移回一级菜单，并配套做 4 处收敛：技能页工具条样式与品牌统一、折叠态侧边栏图标真正对齐到一条竖线、个人中心真正置底、md 文件预览开关改为"编辑"切换。仅前端。

### §40.1 我的记忆 → 员工记忆，移回一级菜单（外部渠道下方）

**改动**：

| 文件 | 改动 |
|---|---|
| [console/src/layouts/Sidebar.tsx](console/src/layouts/Sidebar.tsx) | `navItems` 在 `channels` 之后追加 `workspace`（6 项）；`personalCenterItems` 移除 `workspace`（3 项） |
| [console/src/locales/zh.json](console/src/locales/zh.json) L49 | `"workspace": "我的记忆"` → `"workspace": "员工记忆"` |

一级菜单最终顺序（6 项）：`chat / cron-jobs / skills / mcp / channels / workspace`。
个人中心子项（3 项）：`models / agent-config / token-usage`。

**Why**：员工记忆是日常对话上下文（system prompt、长期记忆文件）的入口，使用频率高于模型配置/安全防护。藏在个人中心折叠区里增加 2 次点击成本。

### §40.2 md 文件编辑器：「预览」开关改为「编辑」开关（语义反转）

**文件**：[console/src/pages/Agent/Workspace/components/FileEditor.tsx](console/src/pages/Agent/Workspace/components/FileEditor.tsx)

```diff
 <div className={styles.markdownToggle}>
   <span className={styles.toggleLabel}>
-    {t("common.preview")}
+    {t("common.edit")}
   </span>
   <Switch
-    checked={showMarkdown}
-    onChange={setShowMarkdown}
+    checked={!showMarkdown}
+    onChange={(v) => setShowMarkdown(!v)}
     size="small"
   />
 </div>
```

`showMarkdown` 仍默认为 `true`（打开文件先看渲染后的 md），开关标签从「预览」变为「编辑」——开关关闭时是预览/渲染态，开启时进入纯文本编辑态。i18n key `common.edit` 已经在 zh.json 中存在（`"edit": "编辑"`），无需新增。

**Why**：原标签"预览"会让用户以为"打开开关 = 进入预览"，但实际默认就是预览态，开关其实控制"是否退出预览进入编辑"。把标签改为"编辑"后语义直观。

### §40.3 技能页顶部工具条重设计

**文件**：
- [console/src/pages/Agent/Skills/components/HeaderActions.tsx](console/src/pages/Agent/Skills/components/HeaderActions.tsx)
- [console/src/pages/Agent/Skills/index.module.less](console/src/pages/Agent/Skills/index.module.less)

**改动**：

- 删除原来 `.headerActionsLeft` / `.headerActionsRight` 双分组结构，改为单一 `.toolbarActions` 平铺容器
- 刷新按钮：`type="default"` → `type="text"`，32×32 方形 ghost 图标（hover 蓝色背景）
- 从默认技能安装：`type="default"` → `type="primary"` 品牌蓝主按钮（推荐操作）
- 通过 zip 上传 / 导入 hub：保留 `type="default"`，但用新 `.toolbarGhostBtn` 样式（白底蓝描边 hover）

新增 LESS 类：

```less
.toolbarActions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.toolbarIconBtn {
  width: 32px; height: 32px;
  border-radius: 8px;
  color: #475569;
  background: transparent;
  &:hover:not(:disabled) {
    background: rgba(37, 99, 235, 0.08);
    color: #2563eb;
  }
}

.toolbarPrimaryBtn {
  height: 32px; padding: 0 14px;
  border-radius: 8px;
  font-size: 13px; font-weight: 500;
  background: #2563eb; border-color: #2563eb;
  box-shadow: 0 1px 2px rgba(37, 99, 235, 0.18);
  &:hover, &:focus {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
  }
}

.toolbarGhostBtn {
  height: 32px; padding: 0 12px;
  border-radius: 8px;
  font-size: 13px; font-weight: 500;
  color: #334155;
  background: #ffffff;
  border-color: rgba(15, 23, 42, 0.12);
  &:hover, &:focus {
    color: #1d4ed8 !important;
    border-color: rgba(37, 99, 235, 0.45) !important;
    background: rgba(37, 99, 235, 0.04) !important;
  }
}
```

旧类 `.primaryTransferButton` / `.creationActionButton` 保留（无引用即不渲染），便于回滚。

**Why**：原工具条 3 个按钮都是 `type="default"` + `min-width: 108px`，视觉权重均等且块状感强，与 §39 紧凑卡片风格脱节。改后:
1. 主操作"从默认技能安装"用品牌蓝凸显
2. 次操作（zip 上传 / hub 导入）用白底蓝描边的 ghost 样式
3. 刷新按钮纯图标 32×32 与图标按钮约定一致

### §40.4 折叠态侧边栏图标真正对齐到一条竖线

**症状**：折叠态（72px Sider）下，从上到下渲染：

```
[AgentSelector 40×40]   ← 偏左 2px
[chat 44×44]
[cron-jobs 44×44]
...
[channels 44×44]
[workspace 44×44]
[authActions ?]
[collapseToggle ?]
[personalCenter 44×44]  ← 偏左
```

`.agentSelectorCollapsed` 是 40×40 的盒子，而 `.collapsedNavItem`（5 项主菜单 + 个人中心触发器）是 44×44，两者左右各偏移 2px。`.personalCenter` 在折叠态也没有显式居中其内部 Dropdown 触发器。

**修复**：

- [console/src/components/AgentSelector/index.module.less](console/src/components/AgentSelector/index.module.less) — `.agentSelectorCollapsed` 改为 `width: 44px; height: 44px; border-radius: 10px; margin: 0 auto 12px`（与 `.collapsedNavItem` 等宽 + 容器内水平居中）
- [console/src/layouts/index.module.less](console/src/layouts/index.module.less) — `.sider.siderCollapsed` 内新增：
  ```less
  .personalCenter {
    align-items: center;
  }
  .authActions {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 0;
  }
  ```

修复后折叠态从顶到底所有图标盒子都是 44×44 且水平居中，整列对齐到一条竖线。

### §40.5 个人中心真正置底（margin-top: auto）

**症状**：§35 之后，个人中心已经位于 sidebar JSX 的最后一个位置，且依赖 `.sidebarNav { flex: 1 }` 把它压到底部。但实际渲染顺序是「主菜单 → 一段空白 → 账户/登出 → 折叠按钮 → 个人中心」，个人中心其实贴在折叠按钮下方而非"绝对底部"，账户登出和折叠按钮挤在 sidebar 中部偏下。

**根因**：`.sidebarNav { flex: 1 }` 一旦展开撑满，后续 4 个兄弟节点（`authActions / collapseToggleContainer / personalCenter / Modal`）按文档流自上而下排，挤在 sidebar 底部 80–120px 区间。但用户希望个人中心**贴底**，账户/登出 / 折叠按钮在它之上。

**修复**：[console/src/layouts/index.module.less](console/src/layouts/index.module.less) 给 `.personalCenter` 加 `margin-top: auto`：

```diff
 .personalCenter {
   flex-shrink: 0;
+  margin-top: auto;
   padding: 4px 0 8px;
   border-top: 1px solid rgba(15, 23, 42, 0.06);
+  display: flex;
+  flex-direction: column;
+  align-items: stretch;
 }
```

`margin-top: auto` 让 personalCenter 吃掉所有剩余垂直空间，把自己推到 flex 容器的底端。配合 sidebarNav 已有的 `flex: 1`，结果是：

```
[AgentSelector]
[主菜单 6 项]
... (sidebarNav 撑开)
[authActions]
[collapseToggleContainer]
———— margin-top: auto 把 personalCenter 推到这里 ————
[personalCenter]  ← 绝对底部
```

> **Note**：`flex: 1` + `margin-top: auto` 共存时，flex item 优先吃 `flex: 1`，剩余空间再被 `margin-top: auto` 兄弟吸收；因为 `.sidebarNav` 内容本身就把 1fr 撑满，所以视觉上 sidebarNav 压不动，personalCenter 通过 `margin-top: auto` 把自己推到容器末尾，把 authActions/collapseToggle 顺势上推。

### §40.6 校验

```bash
cd /Users/rlw/AI项目/wowooai/console

# 1) workspace 在 navItems
grep -n 'key: "workspace"' src/layouts/Sidebar.tsx
# 期望命中 1 处（在 navItems 数组内）

# 2) 文案
grep -n '"workspace": "员工记忆"' src/locales/zh.json
# 期望命中

# 3) FileEditor 切换为 common.edit
grep -n 'common\.edit' src/pages/Agent/Workspace/components/FileEditor.tsx
# 期望命中

# 4) Skills 新工具条类
grep -n 'toolbarPrimaryBtn\|toolbarGhostBtn\|toolbarIconBtn' src/pages/Agent/Skills/components/HeaderActions.tsx
# 期望命中 3 个

# 5) 折叠态 AgentSelector 44×44
grep -nE 'width: 44px;' src/components/AgentSelector/index.module.less
# 期望命中（.agentSelectorCollapsed）

# 6) Personal Center margin-top auto
grep -n 'margin-top: auto' src/layouts/index.module.less
# 期望命中 1 处（在 .personalCenter 内）

npm run build
# 期望：tsc -b && vite build 通过
```

打包同步：

```bash
cd /Users/rlw/AI项目/wowooai
rsync -a --delete console/dist/ src/wowooai/console/
```

### §40.7 浏览器实测

- 展开态（240px）：左侧主菜单 6 项（含底部新加的「员工记忆」）；底部依次：账户/登出 → 折叠按钮 → 个人中心置底，三块紧贴下边缘
- 折叠态（72px）：从上到下 9 个 44×44 图标（数字员工徽章 + 5 项主菜单 + 员工记忆 + 个人中心入口），全部在同一垂直中线上，账户/登出按钮也水平居中
- 我的技能页：顶部三个按钮（从默认技能安装 / zip 上传 / hub 导入）均为白底蓝描边 ghost 风格（见 §40.8），刷新为透明 ghost 图标
- 员工记忆页：打开任一 .md 文件，编辑器右上角开关标签为「编辑」，默认关闭显示渲染后的 md，打开开关进入 TextArea 编辑

### §40.8 我的技能页工具条：三按钮统一为 ghost 风格

§40.3 把「从默认技能安装」设为 `type="primary"` 蓝色实心，「通过 zip 上传 / 导入 hub」设为 ghost 白底蓝描边。视觉上单独一个蓝色实心按钮在顶部工具条里像"提交/保存"按钮，语义错位 —— 三者本质都是"添加技能到当前工作区"的等价入口，没有真正的主次。

**修改**：[HeaderActions.tsx](console/src/pages/Agent/Skills/components/HeaderActions.tsx) 把「从默认技能安装」从 `type="primary" + toolbarPrimaryBtn` 改为 `type="default" + toolbarGhostBtn`，与另外两个按钮完全一致。

```diff
 <Tooltip title={t("skills.downloadFromPoolHint")}>
   <Button
-    type="primary"
-    className={styles.toolbarPrimaryBtn}
+    type="default"
+    className={styles.toolbarGhostBtn}
     onClick={onOpenDownloadPool}
     icon={<DownloadOutlined />}
   >
     {t("skills.downloadFromPool")}
   </Button>
 </Tooltip>
```

`.toolbarPrimaryBtn` LESS 类保留在 [index.module.less](console/src/pages/Agent/Skills/index.module.less)，未来若需要重新区分主次操作可直接复用。

**校验**：

```bash
grep -c 'toolbarPrimaryBtn' console/src/pages/Agent/Skills/components/HeaderActions.tsx
# 期望：0（不再使用）

grep -c 'toolbarGhostBtn' console/src/pages/Agent/Skills/components/HeaderActions.tsx
# 期望：3（从默认技能安装 + zip 上传 + 导入 hub）
```

浏览器实测：我的技能页顶部三个按钮（刷新除外）视觉风格完全一致 —— 白底、灰色边框、hover 时蓝色描边 + 浅蓝背景。

### §40.9 数字员工选择器顶部留白 + 默认员工显示名改为 wowooai

**症状 1**：左侧 sidebar 第一行的「数字员工选择器」紧贴 Sider 顶部边缘，与下方主菜单的呼吸感不一致 —— 主菜单项之间是 2–4px 的细间隙，但选择器距 Sider 顶部仅有 16px 父容器 padding，没有任何额外缓冲。

**症状 2**：`id === "default"` 的内置数字员工在 UI 上显示为「默认数字员工」（来自 [agentDisplayName.ts](console/src/utils/agentDisplayName.ts) 强制走 i18n key `agent.defaultDisplayName`），不符合品牌一致性 —— 这个员工本身就是 wowooai 的主员工。

**修改**：

1. [zh.json](console/src/locales/zh.json) L138：`"defaultDisplayName": "默认数字员工"` → `"defaultDisplayName": "wowooai"`。`getAgentDisplayName` 逻辑不动，所有调用方（AgentSelector / AgentTable / Chat 等）自动跟随。
2. [AgentSelector/index.tsx](console/src/components/AgentSelector/index.tsx) 撤销上一轮新增的 `<div className={styles.agentSelectorLabel}>当前数字员工</div>` 小标签头。
3. [AgentSelector/index.module.less](console/src/components/AgentSelector/index.module.less)：`.agentSelectorWrapper` 顶部边距从 4px 增加到 20px；`.agentSelectorCollapsed` 同步从 `margin: 4px auto 16px` 调到 `margin: 20px auto 16px`。
4. 同步删除 `.agentSelectorLabel` 样式定义（不再被引用）。

调整后选择器距 Sider 顶部 ≈ 36px（父容器 16px padding + 20px wrapper margin），与下方 16px 间距形成 36:16 的"卡片头部强调"节奏，明显区分于主菜单项之间的紧凑间距。

**校验**：

```bash
grep -n '"defaultDisplayName"' console/src/locales/zh.json
# 期望：1 处命中 "wowooai"

grep -n 'agentSelectorLabel\|agent.currentWorkspace' console/src/components/AgentSelector/index.tsx
# 期望：无输出（标签头已删）

grep -n 'margin-top: 20px' console/src/components/AgentSelector/index.module.less
# 期望：1 处命中（.agentSelectorWrapper）

grep -n 'margin: 20px auto 16px' console/src/components/AgentSelector/index.module.less
# 期望：1 处命中（.agentSelectorCollapsed）
```

浏览器实测：默认员工在所有列表与下拉中显示为「wowooai」；左上角数字员工选择器距 Sider 顶部 ≈ 36px 留白，下方主菜单 16px 后开始排列；折叠态徽章也同步下移。

### §40.10 个人中心真正贴底（sticky bottom 修复）

**症状**：§40.5 用 `margin-top: auto` 把个人中心推到底部，但实际并未贴 Sider 视口底部 —— 还是跟在折叠按钮下方一段距离。

**根因**：`.ant-layout-sider-children` 的 flex column 内有 `overflow: auto`。当 AgentSelector + 6 项主菜单 + authActions + collapseToggle 的总高度接近或超过 Sider 视口高度时：
1. `.sidebarNav { flex: 1 }` 被压缩到极小甚至 0，`margin-top: auto` 没有剩余空间可吸收 → 失效
2. 即便有空间，整个内容流可滚动，个人中心会被推到"内容流末尾"而非"视口底部"，用户滚动时看不到它

**修复**：[layouts/index.module.less](console/src/layouts/index.module.less) 给 `.personalCenter` 加 `position: sticky; bottom: 0` + 不透明背景 + z-index：

```diff
 .personalCenter {
   flex-shrink: 0;
+  position: sticky;
+  bottom: 0;
   margin-top: auto;
   padding: 4px 0 8px;
   border-top: 1px solid rgba(15, 23, 42, 0.06);
+  background: #f7f9fc;
+  z-index: 5;
   display: flex;
   flex-direction: column;
   align-items: stretch;
 }
```

`position: sticky` 在滚动容器里被钉到 `bottom: 0`，不论内容是否溢出都贴视口底部；`background: #f7f9fc`（与 `.sider` 同色）让滚动时上方内容不会"穿透"露出；`z-index: 5` 保证上方内容滚过时不会覆盖个人中心。`margin-top: auto` 保留——内容不溢出时仍由 flex 推到底部，视觉效果一致。

**校验**：

```bash
grep -n 'position: sticky' console/src/layouts/index.module.less
# 期望：1 处命中（.personalCenter）
```

浏览器实测：无论 sidebar 内容是否需要滚动，个人中心都贴在 Sider 视口底部；滚动时上方主菜单从其下方滑过，不会与之重叠。


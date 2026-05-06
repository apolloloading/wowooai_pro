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

### 七、2026-05-06 UI 精简与性能优化（§23–§25）
- [§23 2026-05-06 前端 UI 精简与文案调整](#23-2026-05-06-前端-ui-精简与文案调整仅前端)
- [§24 2026-05-06 修复：定时任务列表 hidden 列未真正隐藏，操作列布局异常](#24-2026-05-06-修复定时任务列表-hidden-列未真正隐藏操作列布局异常)
- [§25 2026-05-06 优化：vite manualChunks 拆分 7.8MB ui-vendor](#25-2026-05-06-优化vite-manualchunks-拆分-78mb-ui-vendor)

> **编号说明**：§2 在原始记录中未使用；§19 / §20 在历史中曾出现编号冲突，已通过本次重排（→§24 / §25）解决，原始内容完整保留。

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
      if (!p.is_custom && !ALLOWED_PROVIDER_IDS.has(p.id) && !p.is_local) {
        continue;
      }
      if (p.is_local) local.push(p);
      else regular.push(p);
    }
```

说明：`is_custom` 与 `is_local` 保持原逻辑兼容，白名单只隐藏内置远程供应商中的其它项。

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

> 配套后端 / 打包脚本变更见 [backend.md](backend.md) §24，打包执行步骤见 [packaging.md](packaging.md)。本节只记录前端构建产物要求；不修改 `console/src` 页面业务代码。

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

> 配套打包脚本兜底见 [packaging.md](packaging.md) §9；本节记录前端侧变更。

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

## §25 2026-05-06 优化：vite manualChunks 拆分 7.8MB ui-vendor

> 配套后端优化见 [backend.md](backend.md) §28。两个改动叠加，目标把首次冷启动从 ~70s 降到 ~30–35s。

### 现象

构建产物中单个 `ui-vendor-*.js` 达 7.8MB，WebKit（macOS pywebview）解析速率约 1–1.5 MB/s，前端 JS 解析 + 水合需 ~39s。

### 根因

`vite.config.ts` 的 `manualChunks` 把 `antd/`、`antd-style/`、`@ant-design/*`、`@agentscope-ai/*` 全部合并到一个 `ui-vendor` chunk。其中 `@ant-design/graphs`（含 cytoscape）、`mermaid`、`react-syntax-highlighter` 等只在特定页面 / 特定渲染场景使用，首屏完全不需要。

### 修复

**文件**：`console/vite.config.ts`

原 `ui-vendor` 单一规则拆为 8 个独立 chunk（匹配顺序关键：先具体子包，最后兜底 `antd-core`）：

```ts
// mermaid: only loaded when rendering diagrams
if (id.includes("node_modules/mermaid/")) {
  return "mermaid-vendor";
}
// Code highlighting: only used inside chat code blocks
if (
  id.includes("node_modules/react-syntax-highlighter/") ||
  id.includes("node_modules/refractor/") ||
  id.includes("node_modules/prismjs/") ||
  id.includes("node_modules/highlight.js/")
) {
  return "syntax-highlighter";
}
// @ant-design/graphs: large, only used on graph pages
if (id.includes("node_modules/@ant-design/graphs")) {
  return "antd-graphs";
}
// cytoscape: indirectly pulled by @ant-design/graphs
if (id.includes("node_modules/cytoscape")) {
  return "cytoscape-vendor";
}
// @ant-design/x: chat UI kit
if (id.includes("node_modules/@ant-design/x")) {
  return "antd-x";
}
// @agentscope-ai/chat: chat page main component
if (id.includes("node_modules/@agentscope-ai/chat")) {
  return "agentscope-chat";
}
// @agentscope-ai/design + icons shared design system
if (id.includes("node_modules/@agentscope-ai/")) {
  return "agentscope-design";
}
// antd core + antd-style + remaining @ant-design/* (icons etc.)
if (
  id.includes("node_modules/antd/") ||
  id.includes("node_modules/antd-style/") ||
  id.includes("node_modules/@ant-design/")
) {
  return "antd-core";
}
```

### 预期产物变化

| chunk | 预估大小 | 首屏是否需要 |
|---|---|---|
| `antd-core` | 2.0–2.5 MB | 是 |
| `agentscope-chat` | 1.5–2.0 MB | 是（Chat 页） |
| `antd-x` | 0.8–1.2 MB | 是（Chat 页） |
| `agentscope-design` | 0.3–0.5 MB | 是 |
| `antd-graphs` + `cytoscape-vendor` | 0.8–1.0 MB | 否（仅图谱页） |
| `mermaid-vendor` | ~0.5 MB | 否（仅渲染时） |
| `syntax-highlighter` | ~0.3 MB | 否（仅代码块出现时） |

首屏减少 ~2.0–2.5 MB JS 解析，WebKit 解析速率下节省 ~12–15s。

### 风险

| 项 | 说明 |
|---|---|
| antd cssinjs 跨 chunk | antd / antd-style 共享 cssinjs context；同一 React tree 加载顺序正常，context 不受影响 |
| @ant-design/x 与 antd ConfigProvider | 拆分后仍在同一 React tree，ConfigProvider context 正常传递 |
| HTTP/2 多路复用 | 本地 webview 走 127.0.0.1，多 chunk 并行加载无瓶颈 |

### 复刻校验

```bash
cd console && pnpm build
ls -lhS dist/assets/*.js | head -20
# 期望：不再有单一 7.8MB chunk；antd-core / agentscope-chat / antd-x 各自 < 2.5MB

grep -n 'antd-core\|antd-x\|antd-graphs\|agentscope-chat\|agentscope-design\|mermaid-vendor\|syntax-highlighter\|cytoscape-vendor' \
  console/vite.config.ts
# 期望：8 行命中

grep -n 'ui-vendor' console/vite.config.ts
# 期望：无输出
```

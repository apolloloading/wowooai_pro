---
name: agent_browser
description: "当用户需要浏览器高级能力（语义元素查找 find role / text / label、网络请求拦截/mock、HAR 录制、视觉/快照 diff、annotated screenshot、状态 save/load、Chrome profile 复用、React DevTools 调试、Web Vitals 测量）时，使用本 skill。本 skill 通过 execute_shell_command 调用打包好的 npx + agent-browser@0.27.0；优先与 browser_use 共享同一个 Chrome 实例（先用 browser_use 启动并暴露 cdp_port，再让 agent-browser connect）。renliwo 内部平台仍优先用 renliwo_browser；一般浏览/截图/简单交互优先用 browser_use；只有遇到 browser_use 解决不了的高级场景才升级到 agent-browser。"
metadata:
  builtin_skill_version: "1.0"
  wowooai:
    emoji: "🛰️"
    requires:
      bins: ["npx"]
---

# agent-browser 浏览器高级能力

`agent-browser` 是 Vercel Labs 开源的 AI agent 浏览器 CLI（纯 Rust + CDP），
锁定版本 `0.27.0`。本 skill 让 wowooai 通过 `execute_shell_command` 调它，
与内置 `browser_use` / `renliwo_browser` 协同工作。

---

## 一、三浏览器工具分工（硬规则）

按"renliwo → 常规 → 高级"逐级上升：

| 场景 | 选用 |
|---|---|
| renliwo 内部平台（人力窝、QD 外包等）URL | **`renliwo_browser`** |
| 一般浏览 / 截图 / 简单点击 / 表单填写 | **`browser_use`**（in-process，无 CLI 开销） |
| 语义 `find role/text/label` / 网络拦截 / HAR / state save/load / Chrome profile 复用 / 视觉 diff / annotated screenshot / React 调试 / Web Vitals | **`agent-browser`** |

遇到问题逐级上升：browser_use 搞不定的 → 切到 agent-browser；
agent-browser 也搞不定的 → 向用户报告并请求人工接管。

---

## 二、共享 Chrome 流程（避免重复打开浏览器）

**关键原则**：先让 `browser_use` 启动 Chrome 并暴露 CDP 端口，
再让 `agent-browser`（和 `renliwo_browser`，如果需要）通过 CDP 接管。
登录一次，三方共享 cookies / localStorage / 已打开的 tab。

### 标准步骤

1. **browser_use 启动并暴露端口**

   ```json
   {"action": "start", "cdp_port": 9222}
   ```

   从返回值取 `cdp_url`（通常是 `http://localhost:9222`）。
   暴露 cdp_port 时 idle watchdog 会自动关闭，浏览器不会因为闲置被回收。

2. **agent-browser 连接同一个 Chrome**

   ```bash
   npx agent-browser@0.27.0 connect 9222 --session $WOWOOAI_WORKSPACE_ID
   ```

   `--session` 用当前 workspace id 命名，确保多 workspace 互不干扰。

3. **如需 renliwo_browser 也加入共享**（少数场景）

   ```json
   {"action": "connect_cdp", "cdp_url": "http://127.0.0.1:9222"}
   ```

   renliwo_browser stop 时只断开连接、不杀进程，不影响其它工具。

### 反例（不要这么做）

- ❌ 直接 `npx agent-browser@0.27.0 start --headed`——会另起一个 Chrome 实例，
  与 browser_use 的浏览器并存，登录态不共享
- ❌ 用 `--auto-connect` 跨多 workspace 自动发现端口——可能连错 workspace 的浏览器

---

## 三、常用命令清单（通过 execute_shell_command 调用）

所有命令前缀统一是 `npx agent-browser@0.27.0`。

### 语义元素查找（比 browser_use 的 ref 流程少一次 snapshot）

```bash
npx agent-browser@0.27.0 find role button --name "Submit" --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 find text "登录" --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 click @e1 --session $WOWOOAI_WORKSPACE_ID
```

### 网络拦截 / mock / HAR

```bash
# 阻断某 URL
npx agent-browser@0.27.0 network route "https://example.com/track" --abort --session $WOWOOAI_WORKSPACE_ID

# Mock 响应体
npx agent-browser@0.27.0 network route "**/api/user" --body '{"id":1,"name":"test"}' --session $WOWOOAI_WORKSPACE_ID

# 录 HAR
npx agent-browser@0.27.0 network har start --session $WOWOOAI_WORKSPACE_ID
# ...操作页面...
npx agent-browser@0.27.0 network har stop --session $WOWOOAI_WORKSPACE_ID
```

### 等待

```bash
# 等 URL 跳转
npx agent-browser@0.27.0 wait --url "**/dash" --session $WOWOOAI_WORKSPACE_ID
# 等 networkidle
npx agent-browser@0.27.0 wait --load networkidle --session $WOWOOAI_WORKSPACE_ID
# 等 JS 表达式为真
npx agent-browser@0.27.0 wait --fn "window.ready === true" --session $WOWOOAI_WORKSPACE_ID
```

### 状态 save / load（跳过下次登录）

```bash
npx agent-browser@0.27.0 state save my-login --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 state load my-login --session $WOWOOAI_WORKSPACE_ID
```

### 视觉 / annotated screenshot

```bash
npx agent-browser@0.27.0 screenshot --annotate --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 diff snapshot --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 diff screenshot --baseline before.png -t 0.2 --session $WOWOOAI_WORKSPACE_ID
```

### React / Web Vitals

```bash
npx agent-browser@0.27.0 react tree --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 vitals --session $WOWOOAI_WORKSPACE_ID
```

完整命令参考 https://github.com/vercel-labs/agent-browser

---

## 四、登录 / 账号密码 / 验证码（与 browser_use / renliwo_browser 一致）

⚠️ **禁止用 agent-browser 自动填写账号 / 密码 / 验证码 / 短信 OTP / 滑动验证**。
这些必须由用户在可见的浏览器窗口里手动完成。

正确做法：
1. 用 browser_use action='start' headed=true cdp_port=9222 启动可见 Chrome
2. browser_use action='open' 导航到登录页
3. 告诉用户"请在浏览器窗口完成登录，登录完成后告诉我"
4. 用户登录完成后，agent-browser 通过 connect 接管，登录态已经存在 cookies 里

---

## 五、首跑下载提示

第一次调用 `npx agent-browser@0.27.0 ...` 时：
- agent-browser CLI 已在打包时预装到 bundled Node.js，无需联网下载
- 但首次执行 **浏览器相关命令**前，agent-browser 可能会下载 Chrome for Testing（~200-300MB）
- 下载位置：`~/.cache/agent-browser/`（macOS/Linux）或 `%LOCALAPPDATA%\agent-browser\`（Windows）
- 如果用户已经在用 browser_use 的 Chrome（推荐的共享流程），通常不需要再下载 Chrome for Testing

向用户说明：首次使用 agent-browser 高级能力可能需要几分钟下载浏览器，之后会缓存。

---

## 六、session 隔离约定

- 每次调用都带 `--session $WOWOOAI_WORKSPACE_ID`
- 多 workspace 并行时各自独立 session，不会互串
- 如果用户明确要求"用 agent-browser 自己的 admin / user session"，可以用 `--session admin`

---

## 七、失败兜底

| 故障 | 处置 |
|---|---|
| `command not found: npx` | 报告用户：bundled Node.js 未正确注入 PATH，回退到 browser_use |
| `agent-browser connect` 失败 | 检查 browser_use 是否还在运行；如已 stop，重新 start 带 cdp_port 后再 connect |
| 命令报错（CLI 语法不识别） | 锁版本 `@0.27.0` 已避免；如仍出现，向用户报告并切回 browser_use |
| 连续 2 次同类命令失败 | 停止并向用户报告，不要无脑重试 |

---

## 八、安全提示

- bundled npx 默认只用来跑 `agent-browser@0.27.0`，**不要**通过 npx 安装/执行其它 npm 包
- agent-browser 是 Vercel Labs 出品；Chrome for Testing 来自 Google
- 涉及敏感数据时，避免用 `state save` 把登录态写到磁盘；如必须，提醒用户清理

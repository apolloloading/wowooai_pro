---
name: browser_visible
description: "当用户需要控制 browser_use 的浏览器启动方式时，使用本 skill。当前 browser_use 默认以有头（可见窗口）模式启动本地 Chrome/Chromium（managed CDP）；仅当用户明确要求无头/后台时才传 `headed=false`。`private_mode` 控制是否禁用 CDP、改走 Playwright，`browser_args` 传入额外的 Chromium 启动参数，`executable_path` 指定自定义浏览器可执行文件路径。涉及登录/账号密码/验证码的页面，必须交给用户在可见窗口里手动完成。"
metadata:
  builtin_skill_version: "1.4"
  wowooai:
    emoji: "🖥️"
    requires: {}
---

# 浏览器启动模式

`browser_use.start` 只有两种启动方式：

- 默认：managed CDP（**有头模式，可见窗口**）
- `private_mode=true`：Playwright 直接管理

参数含义：

- `headed`：是否显示浏览器窗口（**默认 true，可见窗口**）。仅当用户明确要求"无头/后台/headless"时才传 `headed=false`。
- `private_mode`：是否禁用 CDP，改走 Playwright
- `browser_args`：额外的 Chromium 启动参数（字符串），多个参数用空格分隔。适用于所有启动路径（headless、headed、managed CDP）。例如 `"--incognito"` 启用隐身模式，`"--proxy-server=http://127.0.0.1:7890"` 设置代理。默认空字符串（无额外参数）。
- `executable_path`：自定义浏览器可执行文件路径（字符串）。设置后覆盖系统默认浏览器检测，可指定任意基于 Chromium 的浏览器。例如 `"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"`。仅允许包含已知浏览器关键词（chrome、chromium、edge、firefox、brave 等）的可执行文件，且文件必须存在。默认空字符串（使用系统默认）。

以上参数互不影响，可自由组合。

## 常见用法

默认启动（有头模式，可见窗口）：
```json
{"action": "start"}
```

无头模式（仅在用户明确要求时使用）：
```json
{"action": "start", "headed": false}
```

不走 CDP：
```json
{"action": "start", "private_mode": true}
```

无头 + 不走 CDP：
```json
{"action": "start", "headed": false, "private_mode": true}
```

隐身模式：
```json
{"action": "start", "browser_args": "--incognito"}
```

指定浏览器路径 + 设置代理：
```json
{"action": "start", "browser_args": "--proxy-server=http://127.0.0.1:7890", "executable_path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"}
```

## 什么时候用 `private_mode`

只有当用户明确要求以下之一时，再设置 `private_mode=true`：

- 不想通过 CDP 管理浏览器
- 想改走 Playwright
- 想减少被其他本地工具通过 CDP 连接的可能性

否则只按需设置 `headed=false` 即可（极少见）。

## 登录 / 账号密码 / 验证码处理

**绝对禁止**使用 `action=type` 自动填写账号、密码、验证码、短信 OTP。

当页面出现登录表单或需要输入敏感凭据时：
1. 确保浏览器运行在有头模式（默认即是）
2. 告知用户在可见窗口里手动完成登录
3. 等待用户确认"已登录"后再继续自动化操作

这条规则没有例外——即使配置或环境变量中存在账号密码，也不要自动填充。

## 什么时候用 `browser_args`

当用户需要传入 Chromium 原生启动参数时使用，常见场景：

- 隐身/无痕模式（`--incognito`、`--inprivate`）
- 设置代理（`--proxy-server`）
- 指定窗口大小（`--window-size=1920,1080`）
- 禁用 GPU（`--disable-gpu`）
- 加载扩展（`--load-extension=/path/to/ext`）

参数使用 shell 风格的空格分隔，在 Windows 上会自动处理路径中的反斜杠。

## 什么时候用 `executable_path`

当用户需要使用非系统默认的浏览器时使用，常见场景：

- 系统默认是 Chrome，但用户想用 Edge
- 安装了多个浏览器，想指定某一个
- 使用便携版浏览器

注意：`executable_path` 只接受包含已知浏览器关键词（chrome、chromium、edge、firefox、brave、vivaldi、opera、360se、yandex、tor）的可执行文件，且路径必须指向一个真实存在的文件。

## 注意

- 默认就是 managed CDP，**有头模式（可见窗口）**
- 启动方式完全由调用参数决定
- managed CDP 依赖本机存在 Chrome / Chromium / Edge
- `private_mode=true` 不等于绝对不可检测，只是改为 Playwright 管理
- 用户手动操作可见浏览器时，不一定会刷新 idle 计时
- `private_mode`、`browser_args`、`executable_path` 都是每次 `start` 的显式参数，不会持久保存
- 若当前已有浏览器在运行，需要先 `stop` 再重新 `start`，才能切换启动方式、窗口可见性或启动参数
- 无头模式可能在服务器/无图形环境中更合适，但默认有头模式是为了保证用户能手动完成登录
- **登录/账号密码/验证码必须由用户手动输入，禁止自动填充**

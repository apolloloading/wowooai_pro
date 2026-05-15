# 10 — 桌面打包（macOS / Windows）

> 版本：0.0.1
> 对应代码：[scripts/pack/](../../scripts/pack/) · [docs/changelog/packaging-macos.md](../changelog/packaging-macos.md) · [docs/changelog/packaging-windows.md](../changelog/packaging-windows.md)

## 1. 总体目标

**即开即用（zero-dep）**：用户下载安装包后无需安装 Python / Node / Conda / Chrome / Pandoc 等任何依赖；双击即可运行。

| 维度 | 取值 |
|---|---|
| 打包方案 | conda-pack + pywebview（**不**用 Tauri / Electron） |
| 后端 runtime | bundled Python 3.11 conda env（含全部依赖 wheel） |
| 前端 runtime | `console/dist`（pnpm build 静态产物，由 FastAPI 同源托管） |
| UI 容器 | pywebview（macOS 原生 WebKit / Windows WebView2） |
| 包体预算 | macOS `.app` ≤ 2.5 GB，Windows installer ≤ 1.5 GB（解压后 ≤ 3 GB） |

## 2. 打包技术栈

| 组件 | 用途 | 备注 |
|---|---|---|
| `conda-pack` | 把开发用 conda env 打包成可重定位 tarball | 生成 `bundled-venv/` |
| `pywebview` | 把 FastAPI 包装成桌面窗口 | macOS / Windows 都用 |
| `pyinstaller` 仅 launcher | 仅打 launcher 二进制（启动 venv + 起 FastAPI + 起 webview） | 主体不走 PyInstaller |
| Playwright Chromium | 浏览器自动化（`browser_use` / `agent-browser`） | 随 conda env 带 ~525 MB |
| Node.js 22 LTS | 运行 `agent-browser` / `claude-agent-acp` 等 CLI | 单独 bundle |
| pypandoc-binary | 文档转换（HTML → docx / pdf） | 通过 PATH 注入 |

## 3. macOS 打包

### 3.1 入口脚本

[scripts/pack/build_macos.sh](../../scripts/pack/build_macos.sh)

### 3.2 PACKBOT_BASE_ENV 快速路径

支持 `PACKBOT_BASE_ENV=/path/to/conda-env` 环境变量复用已有 env，避免每次重建。失败自动回退到 slow-build（重新 `conda env create`）。

参考 commit：[c7c39ebe — pack(win): add PACKBOT_BASE_ENV fast-path with slow-build fallback](../../docs/changelog/packaging-macos.md)。

### 3.3 产物结构

```
WowooAI.app/
  Contents/
    MacOS/
      WowooAI                    # launcher binary
    Resources/
      bundled-venv/              # conda-pack 解压后 Python env
      console-dist/              # 前端静态文件
      node/                      # Node.js runtime
      node_modules/              # agent-browser 等
      pandoc                     # pypandoc-binary 提供
      Info.plist
      icon.icns
```

### 3.4 Chromium bundle

- Playwright 安装时把 Chromium 放在 conda env 内 `~/Library/Caches/ms-playwright`。
- 打包脚本把它复制进 `Resources/bundled-venv/lib/python3.11/site-packages/playwright/driver/...`。
- 启动时通过 `PLAYWRIGHT_BROWSERS_PATH` 指向 bundle 路径。

### 3.5 pandoc

参考 commit：[e2ad58ca — pack(desktop): bundle pandoc via pypandoc-binary with PATH injection](../changelog/packaging-macos.md)。
launcher 启动前把 `bundled-venv/bin` prepend 到 `PATH`，让 `pypandoc.get_pandoc_path()` 找到。

### 3.6 分发

- `.app` → `.dmg`（用 `create-dmg` 或 `hdiutil`）。
- **不做 codesign / notarization**：自签名分发，首次打开需用户右键 → 打开。

## 4. Windows 打包

### 4.1 入口脚本

[scripts/pack/build_win.ps1](../../scripts/pack/build_win.ps1) + [scripts/pack/desktop.nsi](../../scripts/pack/desktop.nsi)

### 4.2 产物结构

```
WowooAI/
  WowooAI.exe                    # launcher
  bundled-venv\
  console-dist\
  node\
  node_modules\
  pandoc.exe
  icon.ico
```

NSIS 打包成 `WowooAI-Setup-0.0.1.exe` 安装器（自带卸载器）。

### 4.3 图标修复

参考 commit：[bd549647 — Windows icon fix](../changelog/packaging-windows.md)。

### 4.4 Unicode 编码

`save_file` 在 Windows 上需要 UTF-8 BOM 处理中文文件名。

### 4.5 fetch_node.ps1 / fetch_node.sh

打包前从 nodejs.org 下载对应平台的 Node.js 22 LTS，解压进 `node/`。

## 5. 包体预算

| 平台 | 主要体积来源 | 预算 |
|---|---|---|
| macOS | bundled-venv ~1.4 GB + Chromium ~525 MB + Node ~80 MB + 前端 ~30 MB | `.app` ≤ 2.5 GB |
| Windows | bundled-venv ~900 MB + Chromium ~280 MB + Node ~60 MB | installer ≤ 1.5 GB / 解压 ≤ 3 GB |

桌面控制工具（`desktop_input` / `desktop_app`）相关依赖（pyautogui / pyobjc-quartz / pywin32）增量预算 < 30 MB。

## 6. 启动顺序（launcher）

详见 [11-startup-runtime.md](11-startup-runtime.md)。

## 7. 凭据隐私

打包过程严禁把以下内容写入安装包：

- 任何 API key / token（包括"测试 key"）。
- 任何账号密码 / 渠道凭据。
- 任何用户的 `~/.wowooai/` 内容。

所有用户配置在用户机器首次运行时由 launcher 创建空模板。

## 8. 0.0.1 不做

- 不做 macOS codesign / notarization（自签名）。
- 不做 Windows 数字签名 / SmartScreen 白名单。
- 不做自动更新（Sparkle / Squirrel）。
- 不做 Linux 桌面包（仅源码可跑）。
- 不做精简版（CPU-only / 不带 Chromium）—— 全功能单一安装包。
- 不做应用商店分发（Mac App Store / Microsoft Store）。

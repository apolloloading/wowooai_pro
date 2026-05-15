# WowooAI 打包执行说明

> 本文只说明如何从当前源码构建 WowooAI wheel 与 macOS 桌面包，供交付给打包执行人使用。代码改造记录请看 [backend.md](backend.md) / [frontend.md](frontend.md)，本文不记录代码调整逻辑。

---

## §0 产物清单

| 产物 | 构建命令 | 输出路径 |
|---|---|---|
| Python wheel | `bash scripts/wheel_build.sh` | `dist/wowooai-<version>-py3-none-any.whl` |
| macOS `.app` | `bash scripts/pack/build_macos.sh` | `dist/WowooAI.app` |
| macOS DMG | `bash scripts/pack/build_macos.sh` | `dist/WowooAI-<version>-macOS.dmg` |
| DMG SHA-256 | 自动生成 | `dist/WowooAI-<version>-macOS.dmg.sha256` |

---

## §1 前置环境

在一台干净 macOS 打包机上执行，建议不要复用开发虚拟环境。

必需：

- macOS 14 或更新版本
- Python 3.10+，仓库本地 `.venv` 存在时脚本会优先使用 `.venv/bin/python`
- Node.js 与 npm（`scripts/wheel_build.sh` 会在 `console/` 下执行 `npm ci && npm run build`）
- conda / miniconda（`scripts/pack/build_common.py` 会创建临时 conda 环境并 conda-pack）
- macOS 自带 `hdiutil` / `ditto`

可选但推荐：

- 预先执行 `playwright install chromium`，或设置 `PLAYWRIGHT_BROWSERS_DIR` 指向已有 Playwright Chromium 缓存；这样 DMG 会内置 Chromium，浏览器自动化能力首次运行不需要下载。
- 准备 `scripts/pack/assets/icon.icns` 与 `scripts/pack/assets/icon_statusbar.png`，用于 `.app` 图标与状态栏图标。

---

## §2 构建 wheel

在项目根目录执行：

```bash
cd /Users/rlw/AI项目/wowooai
bash scripts/wheel_build.sh
```

验证 wheel 存在且包含前端静态资源：

```bash
ls dist/wowooai-*.whl
python3 - <<'PY'
import glob, zipfile
whl = sorted(glob.glob('dist/wowooai-*.whl'))[-1]
with zipfile.ZipFile(whl) as z:
    assert any('wowooai/console/index.html' in n for n in z.namelist())
print(whl)
PY
```

---

## §3 验证桌面依赖 extras

桌面包默认安装 `desktop` extras。可先用干净 venv 验证 Office/PDF 依赖可导入：

```bash
python3 -m venv /tmp/wowooai-desktop-check
/tmp/wowooai-desktop-check/bin/pip install 'dist/wowooai-*.whl[desktop]'
/tmp/wowooai-desktop-check/bin/python -c 'import openpyxl, docx, pptx, pdfplumber; print("ok")'
rm -rf /tmp/wowooai-desktop-check
```

---

## §4 构建 macOS 桌面包

默认构建 `.app` 与 DMG：

```bash
cd /Users/rlw/AI项目/wowooai
bash scripts/pack/build_macos.sh
```

输出：

```bash
ls dist/WowooAI.app
ls dist/WowooAI-*-macOS.dmg
```

如需跳过 DMG，只生成 `.app`：

```bash
CREATE_DMG=0 bash scripts/pack/build_macos.sh
```

如需把本地推理 / whisper 依赖也装入桌面包：

```bash
EXTRAS=full bash scripts/pack/build_macos.sh
```

---

## §5 生产包运行约束

生产包运行时只应由桌面 launcher 拉起 `wowooai app` 后端进程。

禁止在生产包里启动：

- `pnpm dev`
- `npm run dev`
- `vite --host --port 5174`
- `esbuild` dev 进程树

前端必须在构建阶段通过 `scripts/wheel_build.sh` 构建完成，并作为 `wowooai/console/**` 静态资源打入 wheel，再由后端 FastAPI 托管。

---

## §6 桌面包人工验收

安装/打开 DMG 后，把 `WowooAI.app` 拖到 Applications，再双击启动。

### 6.1 进程检查

启动后检查：

```bash
ps -ef | grep 'wowooai app' | grep -v grep
```

期望：有 1 个后端进程。

确认生产包没有 dev server：

```bash
ps -ef | grep -E 'pnpm|npm run dev|vite|esbuild' | grep -i wowooai | grep -v grep
```

期望：无输出。

### 6.2 正常关闭

关闭窗口或从 Dock 退出后等待 3 秒：

```bash
sleep 3
ps -ef | grep 'wowooai app' | grep -v grep
```

期望：无输出，后端进程已退出。

### 6.3 Force Quit 兜底

重新启动 `.app`，找到 launcher PID 后强制退出 launcher，再检查后端：

```bash
ps -ef | grep -i 'WowooAI' | grep -v grep
# Force Quit launcher 后：
sleep 3
ps -ef | grep 'wowooai app' | grep -v grep
```

期望：无输出，后端子进程会随 launcher 消失而退出。

### 6.4 首次启动业务检查

全新工作区首次启动后检查：

- `default` 数字员工名称为 `wowooai`
- `default` 已预装精选技能：`make_plan`、`file_reader`、`pdf`、`docx`、`xlsx`、`pptx`、`cron`、`browser_visible`
- QA 数字员工存在，技能包含 `guidance` 与 `QA_source_index`
- 可以打开主页面，不是白屏
- 能正常打开“我的记忆”“我的技能”“安全防护”等页面
- Office/PDF 相关能力不会因缺少 `openpyxl`、`python-docx`、`python-pptx`、`pdfplumber` 报 `ModuleNotFoundError`

---

## §7 常见问题定位

### 7.1 `.app` 打开后白屏

优先确认 wheel 内是否包含前端静态资源：

```bash
python3 - <<'PY'
import glob, zipfile
whl = sorted(glob.glob('dist/wowooai-*.whl'))[-1]
with zipfile.ZipFile(whl) as z:
    print(any('wowooai/console/index.html' in n for n in z.namelist()))
PY
```

期望输出 `True`。

### 7.2 `.app` 启动失败

查看桌面日志：

```bash
tail -200 ~/.wowooai/desktop.log
```

### 7.3 macOS 提示无法打开

如果未签名/未公证，测试机可右键打开。必要时清理隔离标记：

```bash
xattr -cr /Applications/WowooAI.app
```

正式分发给外部用户前，建议另行补齐签名与 notarization 流程。

---

## §8 已知打包陷阱与防范（2026-05-04 实测记录）

> 以下问题均在真实打包→安装→启动中发现并定位。**在另一台新电脑上打包前必须逐条检查**，否则打出的 DMG 在其他 Mac 上安装后闪退。

### 8.1 `~/.local/lib/pythonX.Y/site-packages` 泄漏（致命）

**现象**：打包出的 `.app` 在打包机上能运行，拖到其他 Mac 闪退。日志报 `ModuleNotFoundError: No module named 'typing_extensions'` 或其他包缺失。

**根因**：

1. 打包机上 `~/.local/lib/python3.10/site-packages/` 存在用户级 pip 安装的包（如 `typing_extensions`、`playwright`、`selenium` 等）。
2. `build_common.py` 执行 `conda run -n env python -m pip install wowooai[desktop]` 时，pip 发现这些包在 `~/.local` 已满足版本要求，输出 `Requirement already satisfied`，**跳过安装**，不会把它们装到 conda 环境的 `site-packages/` 里。
3. `conda-pack` 只打包 conda 前缀目录内的文件，`~/.local` 不在其中，所以这些包完全缺失于产物。
4. 打包机上直接运行 `dist/WowooAI.app` 时 Python 仍能从 `~/.local` 读到这些包，看起来一切正常——**假象**。
5. 安装到 `/Applications/` 后 launcher 设置 `PYTHONNOUSERSITE=1` 隔离用户目录，缺失暴露，启动崩溃。

**2026-05-04 实测缺失清单**（打包机 `~/.local` 中有以下包，全部未进入 conda-pack 产物）：

| 缺失包 | 被谁需要 | 影响 |
|---|---|---|
| `typing_extensions` | pydantic, pydantic_core, fastapi 等 30+ 个包 | 启动即崩 |
| `playwright` | wowooai 主依赖 | 浏览器自动化全部失效 |
| `selenium` | wowooai[desktop] | 浏览器自动化全部失效 |
| `pyee` | playwright, wecom-aibot-python-sdk | playwright 无法导入 |
| `greenlet` | playwright | playwright 无法导入 |
| `trio` | selenium | selenium 无法导入 |
| `trio_websocket` | selenium | selenium 无法导入 |
| `outcome` | trio | trio 无法导入 |
| `sortedcontainers` | trio | trio 无法导入 |
| `PySocks` | selenium 代理支持 | 代理功能失效 |
| `webdriver_manager` | selenium 驱动管理 | webdriver 定位失败 |

**防范**：

`build_common.py` 中 pip install 命令必须加 `--no-user` 强制安装到 conda 环境内，或者在 `conda run` 之前设置 `PYTHONNOUSERSITE=1` 环境变量，使 pip 完全忽略 `~/.local`。

打包前检查当前机器是否有泄漏风险：

```bash
ls ~/.local/lib/python3.10/site-packages/*.dist-info 2>/dev/null | \
  sed 's|.*/||;s|\.dist-info||' | sort
```

如输出非空，说明存在泄漏风险，必须确保 `build_common.py` 的 pip 调用带 `--no-user`。

**打包后验证**（必做）：

```bash
# 检查产物内是否缺关键包
PYTHONNOUSERSITE=1 dist/WowooAI.app/Contents/Resources/env/bin/python -m pip check
```

期望输出 `No broken requirements found.`。如果报 `xxx requires yyy, which is not installed`，说明泄漏问题仍存在。

更严格的验证：

```bash
# 模拟其他 Mac 的隔离环境，批量验证导入
PYTHONNOUSERSITE=1 \
PYTHONHOME=dist/WowooAI.app/Contents/Resources/env \
dist/WowooAI.app/Contents/Resources/env/bin/python -c "
import importlib
for name in [
    'typing_extensions', 'pydantic', 'playwright', 'selenium',
    'pyee', 'greenlet', 'trio', 'webview', 'fastapi',
    'uvicorn', 'httpx', 'certifi',
]:
    try:
        importlib.import_module(name)
    except ImportError as e:
        print(f'MISSING: {name} -- {e}')
        raise SystemExit(1)
print('All critical imports OK')
"
```

### 8.2 App 未签名 — Gatekeeper 拦截

**现象**：其他 Mac 从网络下载 DMG 安装后，双击提示「"WowooAI"已损坏，无法打开」或「无法验证开发者」。

**根因**：当前打包流程不包含 `codesign` 和 Apple notarization。macOS Gatekeeper 对未签名应用施加隔离标记（`com.apple.quarantine`）。

**临时解决（仅限测试/内部分发）**：

```bash
# 方法 1：右键 → 打开（只需一次）
# 方法 2：命令行清除隔离标记
xattr -cr /Applications/WowooAI.app
```

**正式分发解决方案**：

1. 获取 Apple Developer ID Application 证书
2. 打包后执行 `codesign --deep --force --sign "Developer ID Application: <Team>" dist/WowooAI.app`
3. 将 DMG 提交 `xcrun notarytool submit` 公证
4. 公证通过后 `xcrun stapler staple` 装订票据到 DMG

### 8.3 仅支持 Apple Silicon（arm64）

**现象**：Intel Mac 双击后直接报错或闪退。

**根因**：conda 创建的 Python 3.10 环境在 Apple Silicon 打包机上生成的是 arm64 二进制。部分 `.so` 扩展虽是 universal（arm64+x86_64），但 Python 解释器本身是 arm64-only。

**确认方法**：

```bash
file dist/WowooAI.app/Contents/Resources/env/bin/python3.10
# 期望看到: Mach-O 64-bit executable arm64
```

**如需支持 Intel Mac**：需在 Intel Mac 上或使用 x86_64 conda 环境单独构建一份包，或使用 `CONDA_SUBDIR=osx-64` 创建 x86_64 conda 环境。两个架构需要分别打包分别分发。

### 8.4 `LSMinimumSystemVersion` 与实际兼容性

`Info.plist` 中 `LSMinimumSystemVersion` 设为 `14.0`（macOS Sonoma）。macOS 12/13 用户会被系统直接拒绝打开，即使二进制实际支持 macOS 12.1+。

如需放宽，在 `scripts/pack/build_macos.sh` 中修改 `LSMinimumSystemVersion` 值。但需实测目标 macOS 版本上 pywebview 和系统框架是否正常工作后再调整。

### 8.5 品牌 logo 必须在打包前完成替换

前端 SVG logo（`favicon.svg`、`logo-light.svg`、`logo-dark.svg`、`wowooai-logo.svg`）的权威来源是 `docs/changelog/brand/`。打包前需确认 `console/public/` 下的文件已从 brand 目录同步：

```bash
for f in favicon.svg logo-light.svg logo-dark.svg wowooai-logo.svg; do
  diff -q "docs/changelog/brand/$f" "console/public/$f" || echo "NOT SYNCED: $f"
done
```

macOS `.app` 的 Dock 图标来自 `scripts/pack/assets/icon.icns`，与前端 SVG 是独立的两套文件。如果更换了品牌色，`icon.icns` 也需要重新从 SVG 生成：

```bash
# 从 favicon.svg 生成 icon.icns（需要 Python + Pillow + macOS iconutil）
# 步骤：SVG → 多尺寸 PNG (16~1024) → .iconset → iconutil --convert icns
```

### 8.6 打包前完整检查清单

在新电脑上打包前，按顺序执行：

```bash
# 1. 确认 ~/.local 泄漏风险
ls ~/.local/lib/python3.10/site-packages/*.dist-info 2>/dev/null | wc -l
# 如果 > 0，确保 build_common.py 中 pip 带 --no-user

# 2. 确认 conda 可用
conda --version

# 3. 确认 node/npm 可用
node --version && npm --version

# 4. 确认品牌 logo 已同步
for f in favicon.svg logo-light.svg logo-dark.svg wowooai-logo.svg; do
  diff -q "docs/changelog/brand/$f" "console/public/$f"
done

# 5. 确认 icon.icns 是蓝色品牌版（检查主色不是橙色 #FF9D4D）
python3 -c "
from PIL import Image
import collections, subprocess, tempfile, os
td = tempfile.mkdtemp()
subprocess.run(['iconutil', '--convert', 'iconset', 'scripts/pack/assets/icon.icns', '--output', f'{td}/i.iconset'], check=True)
img = Image.open(f'{td}/i.iconset/icon_256x256.png').convert('RGBA')
c = collections.Counter()
for r,g,b,a in img.getdata():
    if a > 128 and not (r>240 and g>240 and b>240):
        c[(r,g,b)] += 1
top = c.most_common(1)[0][0]
print(f'主色: #{top[0]:02X}{top[1]:02X}{top[2]:02X}')
assert top == (37,99,235), f'icon.icns 主色不是品牌蓝 #2563EB，当前: #{top[0]:02X}{top[1]:02X}{top[2]:02X}'
print('icon.icns 品牌色正确')
"

# 6. 确认 Playwright Chromium 已缓存（可选）
ls ~/Library/Caches/ms-playwright/chromium-* 2>/dev/null | head -1

# 7. 执行打包
bash scripts/pack/build_macos.sh

# 8. 打包后验证（必做）
PYTHONNOUSERSITE=1 dist/WowooAI.app/Contents/Resources/env/bin/python -m pip check
```

---

## §9 前端 API base URL 必须走相对路径（致命，2026-05-04 实测记录）

### 9.1 现象

打包后的 DMG 安装到任意 Mac，双击打开后**前端能加载、后端进程也在跑**，但所有业务请求全部失败：

- WebView/浏览器 DevTools 中可见大量请求 `http://127.0.0.1:8088/api/...` 全部 `ERR_CONNECTION_REFUSED`
- `lsof -nP -iTCP:8088` 没有任何监听
- 但 `lsof` 显示 backend 实际在 `127.0.0.1:60494`（每次启动随机端口）

### 9.2 根因（多处共同导致）

1. **`console/.env.local` 把 `VITE_API_BASE_URL` 写死成 `http://127.0.0.1:8088`**。Vite 构建时会把 `import.meta.env.VITE_API_BASE_URL` 替换成该值并打入 bundle，所以所有 `getApiUrl()` 都返回绝对 URL。
2. **`scripts/wheel_build.sh` 没清理 `.env.local`**：执行 `npm run build` 时直接读到 `.env.local`，把 8088 永久打进 wheel 内的前端 JS。
3. **桌面包模式下后端是随机端口**：`src/wowooai/cli/desktop_cmd.py` 中 `port = _find_free_port(host)` 由 OS 分配空闲端口，不会复用 8088。
4. **`wowooai app` 命令行模式默认端口刚好是 8088**：开发模式下 8088 一直能命中，问题永远不会暴露——是个误导性的巧合。

### 9.3 修复方案（已落地，2026-05-04）

采用「前端走同源相对路径 + 打包脚本兜底」组合方案。

#### 9.3.1 前端：删除 `console/.env.local`

仓库不再保留 `console/.env.local`。前端 `getApiUrl(path)` 在 `VITE_API_BASE_URL` 为空时返回 `/api/<path>`，浏览器自动补全为 `当前页面 origin/api/<path>`，恰好就是后端地址（前后端是同一个 FastAPI 进程，前端是后端托管的静态文件）。

> `.gitignore` 已经 ignore 了 `.env.*`，开发者本地可以再造一份，不会被提交。

#### 9.3.2 前端：`vite.config.ts` 加 dev proxy

为了让 `npm run dev`（5173）模式仍能跨端口连后端 8088，在 vite 配置里加 proxy，覆盖 `/api`、`/console`：

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

开发者无需 `.env.local`，dev 与 prod 行为一致：前端永远走同源相对路径。

#### 9.3.3 打包：`scripts/wheel_build.sh` 强制清空 `VITE_API_BASE_URL`

即使开发者本地不慎留了 `.env.local`，打包时也要保证不被打入 bundle：

```bash
# 临时移走 .env.local，构建结束自动还原
ENV_LOCAL="$CONSOLE_DIR/.env.local"
if [[ -f "$ENV_LOCAL" ]]; then
  mv "$ENV_LOCAL" "$ENV_LOCAL.wheelbuild.bak"
fi
trap 'if [[ -f "$ENV_LOCAL.wheelbuild.bak" ]]; then mv "$ENV_LOCAL.wheelbuild.bak" "$ENV_LOCAL"; fi' EXIT

# 强制 VITE_API_BASE_URL 为空，防止 shell 环境里残留覆盖
(cd "$CONSOLE_DIR" && VITE_API_BASE_URL="" npm run build)
```

### 9.4 打包后验证（必做）

```bash
# 检查打包出的前端 JS 中不再硬编码 8088
grep -c "127.0.0.1:8088" dist/WowooAI.app/Contents/Resources/env/lib/python3.10/site-packages/wowooai/console/assets/*.js
# 期望：每个 JS 文件都返回 0；docker 文档字符串里残留的 8088 不算（应只在 .css/.html 之外的非 JS）
```

更直接的功能性验证：

```bash
# 启动 .app 后查看实际监听端口
lsof -nP -iTCP -sTCP:LISTEN | grep -i wowooai

# 浏览器 DevTools → Network 中所有 /api/ 请求都应返回 200，没有 ERR_CONNECTION_REFUSED
```

### 9.5 风险与回归

| 场景 | A+B 之后是否有回归 |
|---|---|
| 桌面包随机端口 | ✅ 修复，走相对路径自动适配 |
| `wowooai app` 默认 8088 | ✅ 不受影响，相对路径同源 |
| `wowooai app --port 9999` 自定义端口 | ✅ 不受影响 |
| Docker 同端口 | ✅ 不受影响 |
| 开发模式 `npm run dev` | ✅ 已加 proxy，无需 `.env.local` |
| 开发者保留旧 `.env.local` | ✅ 打包脚本会兜底移走再还原 |
---

## §10 桌面包必须内置 Node.js / npx（Tavily MCP 依赖，2026-05-04 实测记录）

### 10.1 现象

桌面包安装后，默认 MCP 工具 `tavily_search` 已配置 `TAVILY_API_KEY`，但页面一直提示：

```text
MCP 服务器正在连接中，请稍后重试
```

后端日志 `~/.wowooai/wowooai.log` 持续出现：

```text
Error in MCP client lifecycle for tavily_mcp: [Errno 2] No such file or directory
Timeout waiting for MCP client 'tavily_mcp' to connect
Failed to initialize MCP client 'tavily_search'
```

### 10.2 根因

默认 agent 配置中 Tavily MCP 是 stdio 子进程模式：

```json
{
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "tavily-mcp@latest"],
  "env": {
    "TAVILY_API_KEY": "..."
  }
}
```

而 macOS 用户双击 `.app` 时，进程从 `launchd` 启动，不会加载用户 shell 的 `.zshrc` / `.bashrc`，所以 `PATH` 通常只有：

```text
/Applications/WowooAI.app/Contents/Resources/env/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

用户机器上的 Node / npx 可能在：

```text
/opt/homebrew/bin/npx
/usr/local/bin/npx
~/.nvm/versions/node/*/bin/npx
~/claude/node/bin/npx
```

这些路径不会自动进入 GUI app 的环境。MCP SDK 执行：

```python
anyio.open_process(["npx", "-y", "tavily-mcp@latest"], env=...)
```

因为 `PATH` 中找不到 `npx`，直接抛 `OSError: [Errno 2] No such file or directory`，Tavily MCP 永远无法连接。钉钉 MCP 使用 `streamable_http`，不依赖本地 `npx`，所以不会受影响。

### 10.3 修复方案（已落地）

在 conda-pack 环境内直接安装 `nodejs`，让桌面包自带 `node`、`npm`、`npx`：

```bash
conda install -n <temp-env> -y nodejs
```

对应代码位置：

```text
scripts/pack/build_common.py
```

在创建临时 conda env 后、执行 pip 安装 Python 依赖前，新增：

```python
_run([
    conda,
    "install",
    "-n",
    env_name,
    "nodejs",
    "-y",
])
```

这样最终 `.app` 中会存在：

```text
dist/WowooAI.app/Contents/Resources/env/bin/node
dist/WowooAI.app/Contents/Resources/env/bin/npm
dist/WowooAI.app/Contents/Resources/env/bin/npx
```

launcher 已经设置：

```bash
export PATH="$ENV_DIR/bin:$PATH"
```

所以 MCP stdio 子进程执行 `npx -y tavily-mcp@latest` 时，会优先命中 bundle 内置的 `npx`，不再依赖用户机器是否安装 Node.js。

### 10.4 代价

- DMG / `.app` 体积会上涨，预估约 `+80MB` 左右（取决于 conda nodejs 包版本与压缩率）。
- 首次运行 Tavily MCP 时，`npx -y tavily-mcp@latest` 仍可能需要访问 npm registry 下载该 MCP 包；如需完全离线，还需要进一步把 `tavily-mcp` npm 包缓存或改为本地固定路径，这不在本次修复范围内。

### 10.5 打包后验证（必做）

```bash
# 1. 确认 node / npm / npx 已进入 conda-pack 产物
ls -la dist/WowooAI.app/Contents/Resources/env/bin/node
ls -la dist/WowooAI.app/Contents/Resources/env/bin/npm
ls -la dist/WowooAI.app/Contents/Resources/env/bin/npx

# 2. 确认版本可执行
PYTHONNOUSERSITE=1 \
PATH="$(pwd)/dist/WowooAI.app/Contents/Resources/env/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
dist/WowooAI.app/Contents/Resources/env/bin/npx --version

# 3. 模拟 GUI app 的最小 PATH，确认能解析到 bundle 内 npx
PATH="$(pwd)/dist/WowooAI.app/Contents/Resources/env/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
command -v npx
# 期望输出：.../dist/WowooAI.app/Contents/Resources/env/bin/npx
```

### 10.6 风险与回归

| 场景 | 影响 |
|---|---|
| 用户机器没有 Node.js | ✅ Tavily MCP 仍可启动，因为 bundle 内置 npx |
| 用户机器有 Homebrew / nvm Node.js | ✅ bundle 内置 npx 优先，不受用户环境影响 |
| 钉钉 HTTP MCP | ✅ 不受影响 |
| Python 依赖打包 | ✅ 不受影响，仍由 pip 安装并由 `pip check` 验证 |
| DMG 体积 | ⚠️ 增大约 80MB |

---

## §11 Playwright Chromium / headless shell 必须同时打入桌面包（2026-05-04 实测记录）

### 11.1 现象

桌面包安装到全新 Mac，第一次让 bot 调用浏览器自动化（`renliwo_browser`、`browser_use`）失败，`~/.wowooai/wowooai.log` 报：

```text
Browser start failed: BrowserType.launch: Executable doesn't exist at
  .../playwright-browsers/chromium_headless_shell-1217/chrome-headless-shell-mac-arm64/chrome-headless-shell

Looks like Playwright was just installed or updated.
Please run the following command to download new browsers:
    playwright install
```

随后日志出现 `Downloading Chrome Headless Shell ... downloaded to .../chromium_headless_shell-1217`，~150MB 网络流量。**离线 Mac 直接无法使用浏览器技能**。

### 11.2 根因

打包脚本 `scripts/pack/build_macos.sh` 旧版只复制 `chromium-*`：

```bash
for dir in "$PW_BROWSERS_SRC"/chromium-*; do
  cp -R "$dir" "$PW_BROWSERS_DST/"
done
```

而 Playwright >= 1.49 在 `headless=True`（`browser_control.py` 默认值）下并不使用完整 Chromium，而是用更小的独立 `chrome-headless-shell` 二进制，路径在 `chromium_headless_shell-<rev>/`。glob `chromium-*` **不匹配** `chromium_headless_shell-*`（中间多一个 `_headless_shell` 段），导致：

1. 打包阶段：headless shell 没进 DMG。
2. 运行阶段：第一次启动 `pw.chromium.launch(headless=True)` 在 `PLAYWRIGHT_BROWSERS_PATH` 下找不到二进制。
3. 联网用户：Playwright 默默下载补齐 → 打包机自验时不会暴露问题。
4. 离线用户：直接 `Executable doesn't exist`，浏览器技能全部失效。

附加问题：同一台打包机的 `~/Library/Caches/ms-playwright/` 会随 Playwright 升级累计多版本 chromium（如 `chromium-1208` + `chromium-1217`），旧版 glob 把全部版本都打进去，每多一份占 ~330MB。

### 11.3 修复（已落地）

`scripts/pack/build_macos.sh` 改为：

1. 读取 conda-pack 产物里的 `playwright/driver/package/browsers.json`，拿到 **当前打包用的 Playwright 版本要求的精确 revision**（chromium 与 chromium-headless-shell 一一对应）。
2. 按这两个版本号精确复制 `chromium-<rev>` + `chromium_headless_shell-<rev>` 两个目录，跳过其他历史版本/firefox/webkit/ffmpeg。
3. 复制后做完整性校验：两个目录必须都存在且非空，否则脚本 `exit 1` 而不是 warning，避免再次出现"打了个不完整的包"。
4. 找不到 cache 或缺关键目录时直接报错并退出，提示打包者先 `playwright install chromium`。

核心代码片段（详见仓库当前脚本）：

```bash
PW_BROWSERS_JSON=".../site-packages/playwright/driver/package/browsers.json"
PW_DIRS_TO_COPY="$("${PYTHON}" - "$PW_BROWSERS_JSON" << 'PYEOF'
import json, sys
data = json.loads(open(sys.argv[1]).read())
wanted = {"chromium": None, "chromium-headless-shell": None}
for b in data.get("browsers", []):
    if b.get("name") in wanted:
        wanted[b["name"]] = b.get("revision")
print(f"chromium-{wanted['chromium']} "
      f"chromium_headless_shell-{wanted['chromium-headless-shell']}")
PYEOF
)"

for d in $PW_DIRS_TO_COPY; do
  [[ -d "$PW_BROWSERS_SRC/$d" ]] || { echo "missing $d"; exit 1; }
  cp -R "$PW_BROWSERS_SRC/$d" "$PW_BROWSERS_DST/"
done
```

### 11.4 为什么只保留 `chromium-1217`，不保留 `chromium-1208`

- 当前 `dist/WowooAI.app/.../playwright/driver/package/browsers.json` 中 chromium 与 chromium-headless-shell 的 `revision` 都是 **1217**。
- Playwright Python 包升级时只认 `browsers.json` 里固定的那一个 revision；老 revision 留在 cache 里完全不会被运行时使用。
- 所以保留 1217、丢弃 1208 是安全的，且每个 .app 减小 ~330MB。

打包完成后可执行：

```bash
ls dist/WowooAI.app/Contents/Resources/playwright-browsers/
# 期望仅看到：
#   chromium-1217
#   chromium_headless_shell-1217
#   <若干 *.json 标记文件>
```

### 11.5 打包后验证（必做）

```bash
# 1. 必需的两个目录都存在
test -d dist/WowooAI.app/Contents/Resources/playwright-browsers/chromium-1217
test -d dist/WowooAI.app/Contents/Resources/playwright-browsers/chromium_headless_shell-1217

# 2. headless shell 可执行
ls -la dist/WowooAI.app/Contents/Resources/playwright-browsers/chromium_headless_shell-*/chrome-headless-shell-*-arm64/chrome-headless-shell

# 3. 模拟离线启动验证
PLAYWRIGHT_BROWSERS_PATH="$(pwd)/dist/WowooAI.app/Contents/Resources/playwright-browsers" \
PYTHONNOUSERSITE=1 \
dist/WowooAI.app/Contents/Resources/env/bin/python - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    page = b.new_page()
    page.set_content("<h1>ok</h1>")
    print("title:", page.title())
    b.close()
PY
# 期望输出 "title: " 且无 BrowserType.launch ... Executable doesn't exist 报错
```

### 11.6 风险与回归

| 场景 | 影响 |
|---|---|
| 离线 Mac 首次使用 renliwo_browser / browser_use | ✅ 修复后可用，无需联网下载 |
| 联网 Mac 首次使用 | ✅ 不再产生 ~150MB 后台下载 |
| Playwright 后续升级到新 revision | ✅ 自动跟随：脚本读 `browsers.json`，下次打包自动选新版本（前提是打包机本地 cache 已有该新版本） |
| 打包机 cache 缺新版本 | ✅ 脚本会 `exit 1` 并提示先跑 `playwright install chromium` |
| 打包机 cache 同时有旧版本（如 chromium-1208） | ✅ 不再被错误打入；DMG 体积稳定 |
| browser_visible 技能（headed 模式） | ✅ 仍然命中完整 chromium-* 目录，可正常显示窗口 |
| DMG 体积 | ⚠️ 净增/减取决于历史：相比"只 chromium 不含 headless"会 +约 150MB；相比"chromium-1208+1217 全打"会 −约 330MB |


---

## §12 2026-05-06 增量：DMG 卷图标自定义（Finder 挂载后显示品牌图标）

### 现象

在 §0 / §4 流程跑出来的 `WowooAI-<version>-macOS.dmg`,用户双击挂载后,Finder 侧边栏 / 桌面图标是通用磁盘图标(灰白色 HD 形状),而不是品牌蓝色 W。`.app` 自身图标已正确(继承 `Contents/Resources/icon.icns`),但卷图标是另一个独立资源。

### 根因

DMG 卷图标由根目录下隐藏文件 `.VolumeIcon.icns` 提供,且需要 HFS+ FinderInfo 中的 "has custom icon" attribute bit(`SetFile -a C` 或对应 `xattr` 字节标记)。`hdiutil create` 默认不会做这个,需要在 mount 后、detach 前主动写入。

### 修复

**文件**:`scripts/pack/build_macos.sh`

DMG 创建段中,`ditto` 拷贝 `.app` + `ln -s /Applications` 之后、`hdiutil detach` 之前,新增卷图标设置:

```bash
ditto "${APP_DIR}" "${_MOUNT_PT}/${APP_NAME}.app"
ln -s /Applications "${_MOUNT_PT}/Applications"

# Custom DMG volume icon: Finder shows this in the sidebar / desktop when
# the DMG is mounted. Copy icon.icns as .VolumeIcon.icns and toggle the
# "has custom icon" attribute (chflags hasicon -> attribute bit C).
if [[ -f "${PACK_DIR}/assets/icon.icns" ]]; then
  cp "${PACK_DIR}/assets/icon.icns" "${_MOUNT_PT}/.VolumeIcon.icns"
  if command -v SetFile >/dev/null 2>&1; then
    SetFile -a C "${_MOUNT_PT}"
  else
    # SetFile is part of Xcode CLT; fall back to xattr for the same effect.
    # The "com.apple.FinderInfo" 32-byte blob with byte 8 = 0x04 sets the
    # "has custom icon" flag.
    xattr -wx com.apple.FinderInfo \
      "0000000000000000040000000000000000000000000000000000000000000000" \
      "${_MOUNT_PT}" 2>/dev/null || true
  fi
fi

hdiutil detach "${_MOUNT_PT}"
```

要点:

- `${PACK_DIR}/assets/icon.icns` 是 `build_macos.sh` 已使用的同一个图标源(参见 §4 / 脚本顶部 `PACK_DIR`),与 `.app` 内 `Resources/icon.icns` 完全一致
- `SetFile -a C`(Xcode Command Line Tools 自带)是首选;CI/未装 Xcode CLT 的环境走 `xattr` 兜底
- xattr 32 字节 FinderInfo blob 中,**第 9 个字节**(下标 8)的 `0x04` 位即 "has custom icon" flag(macOS Finder File Manager 资料中的 `kHasCustomIcon` 常量)
- 失败 `|| true`:DMG 创建是主流程,卷图标是 cosmetic;失败仅打 stderr,不让整个打包脚本退出

### 边界

| 场景 | 行为 |
|---|---|
| Xcode CLT 已装 | ✅ `SetFile -a C` 成功,Finder 立即识别 |
| 仅 macOS base(无 Xcode CLT) | ✅ `xattr` 兜底设置 FinderInfo |
| `icon.icns` 缺失 | ✅ 整段 if 跳过,DMG 仍生成,只是卷图标是默认 |
| 用户已挂载的旧 DMG | ❌ 需要重新构建/挂载才会显示新卷图标(Finder 缓存可用 `killall Finder` 强制刷新) |

### 校验

```bash
bash scripts/pack/build_macos.sh
# 挂载新 DMG
hdiutil attach "dist/WowooAI-$(sed -n 's/^__version__[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' src/wowooai/__version__.py)-macOS.dmg" -nobrowse -plist | \
  python3 -c "import sys,plistlib; pl=plistlib.loads(sys.stdin.buffer.read()); print(next(e['mount-point'] for e in pl['system-entities'] if 'mount-point' in e))"
# 期望输出 /Volumes/WowooAI <version>

# 然后 Finder 中查看挂载卷的图标应为蓝色 W
ls -la@ "/Volumes/WowooAI 0.0.1/.VolumeIcon.icns"
# 期望存在
xattr -px com.apple.FinderInfo "/Volumes/WowooAI 0.0.1"
# 期望第 9 字节为 04
```



## §13 2026-05-06 同步：`desktop_cmd.py` Win 修复对 macOS 的影响（无影响 / 附带受益）

`src/wowooai/cli/desktop_cmd.py` 因 Windows 打包反馈修了两件事(详见 `docs/changelog/backend.md` §29 / §30):

1. 新增 `_apply_win_icon(window, icon_path)`,通过 `WM_SETICON` 强制覆盖 Windows 标题栏 / 任务栏图标。
2. `WebViewAPI.save_file` 在 `urlopen` 前对 URL 做百分号编码,修中文文件名下载 `UnicodeEncodeError`。

### macOS 影响评估

| 改动点 | macOS 行为 |
|---|---|
| `_apply_win_icon` 函数体引用 `ctypes.windll` | ✅ 函数仅在 `if sys.platform == "win32":` 下被调用,macOS 永不进入函数体,`ctypes.windll` 永不被触达。模块顶层不 import 任何 Windows 专属符号(`ctypes` / `wintypes` 都是函数局部 import) |
| `webview.start(icon=icon_path)` 新增 icon kwarg | ✅ 候选只查 `icon.ico`(`<env_root>/icon.ico` + `scripts/pack/assets/icon.ico`)。macOS bundle 用 `icon.icns` 且不在这两处,`os.path.exists` 均 False,`icon_path = None`。pywebview Cocoa 后端接受 `icon=None`,no-op;窗口 icon 继续走 `Info.plist` 的 `CFBundleIconFile=icon.icns` |
| 删除旧 `_resolve_window_icon()` | ✅ 该函数原仅在 `if is_windows:` 分支调用,macOS 从未走过这条路径,删除后无影响 |
| `save_file` 百分号编码 | ✅ 平台无关。macOS 桌面包同样修复了上传文件名含中文时 `urlopen` 抛 `UnicodeEncodeError` 的 bug — 属附带收益 |
| `build_macos.sh` / `Info.plist` / DMG 链路 | ✅ 完全未变,继续走 `CFBundleIconFile=icon.icns` + `.VolumeIcon.icns` |

### 校验(在 macOS 上)

```bash
.venv/bin/python -m py_compile src/wowooai/cli/desktop_cmd.py && echo OK

# 函数仅在 win32 守卫下被调用
grep -n 'sys.platform == "win32"' src/wowooai/cli/desktop_cmd.py
# 期望:命中 _apply_win_icon 调用前

# macOS 候选路径都不存在,icon_path 为 None
ls scripts/pack/assets/icon.ico 2>/dev/null || echo "missing on macOS bundle: OK"

# 行为校验:正常 build → open dist/WowooAI.app
# 期望:Dock / 标题栏继续显示 icon.icns,无报错
```

### 回退

如需完全剥离这两个改动以回到 §11 之前的实现:
- 把 `WebViewAPI.save_file` 中 `encoded_url` 构造删除,`urlopen(encoded_url)` 改回 `urlopen(url)`。
- 删除 `_apply_win_icon` 函数及其调用。
- `webview.start(private_mode=False, icon=icon_path)` 改回 `webview.start(private_mode=False)`。

macOS 打包链路本身不受这些回退影响。

---

## §14 2026-05-14 修复：macOS Dock 图标错误显示为通用 "exec" 图标

### §14.1 现象

打包后的 `WowooAI.app` 在 macOS Dock / 程序坞 / Cmd-Tab 切换器中显示一个通用的 "exec" 图标，而不是品牌蓝 W logo。Finder 中 `.app` 自身的 Get Info 图标可能正确，但启动后 Dock 立刻被替换成错误图标。

### §14.2 根因

两条独立路径都没生效，导致 macOS 兜底用了 Python 解释器进程的默认图标：

**路径 1 — Info.plist 的 `CFBundleIconFile` 没被 LaunchServices 采纳**

[scripts/pack/build_macos.sh:401-417](../../scripts/pack/build_macos.sh#L401-L417) 生成的 Info.plist 缺少：

```xml
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
```

没有 `CFBundlePackageType=APPL`，macOS LaunchServices 不会把它当成标准 GUI 应用注册，`CFBundleIconFile=icon.icns` 在某些场景下被忽略。

**路径 2 — 运行时 pywebview 没调用 `setApplicationIconImage_`**

[src/wowooai/cli/desktop_cmd.py:367-378](../../src/wowooai/cli/desktop_cmd.py#L367-L378) 在创建 webview 窗口前定位图标，**只查找 `icon.ico`（Windows 格式），从来不查 `icon.icns`**：

```python
icon_path = None
for cand in (
    os.path.join(os.path.dirname(sys.executable), "icon.ico"),
    os.path.join(..., "scripts", "pack", "assets", "icon.ico"),
):
    if os.path.exists(cand):
        icon_path = cand
        break
```

macOS .app 里两个候选路径都不存在 → `icon_path = None` → 调用 `webview.start(icon=None)`。

而 [pywebview cocoa.py:628-630](https://github.com/r0x0r/pywebview) 只在 icon 非空时设置应用图标：

```python
if _state['icon'] and os.path.isfile(_state['icon']):
    ns_image = AppKit.NSImage.alloc().initByReferencingFile_(_state['icon'])
    BrowserView.app.setApplicationIconImage_(ns_image)
```

所以运行时 `NSApplication.setApplicationIconImage_` 永远不会被调用。

**为什么 Info.plist 不能独立救场**

[scripts/pack/build_macos.sh:309-369](../../scripts/pack/build_macos.sh#L309-L369) 的 bash launcher 在 `Contents/MacOS/WowooAI` 立刻 `exec` 到 `env/bin/WowooAI`（指向 `python3.10` 的硬链接）。bash 被 exec 替换为 python 进程后，macOS 把 python 视为 CFBundleExecutable，但 Info.plist 的图标继承在「非 Mach-O 启动器 + 硬链接二进制」组合下不稳定 —— 一旦 NSApplication 没有显式 `setApplicationIconImage_`，Dock 就会回退到运行中可执行二进制的默认图标。

### §14.3 修复（C 方案：组合拳）

**改动 1 — Info.plist 补齐两个 key**

[scripts/pack/build_macos.sh:407-408](../../scripts/pack/build_macos.sh#L407-L408)：

```diff
 <plist version="1.0">
 <dict>
+  <key>CFBundlePackageType</key><string>APPL</string>
+  <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
   <key>CFBundleExecutable</key><string>${APP_NAME}</string>
```

让 LaunchServices 把 .app 当成标准 GUI 应用注册，启动闪屏阶段就能直接显示正确图标。

**改动 2 — `desktop_cmd.py` 按平台选择图标格式**

[src/wowooai/cli/desktop_cmd.py:363-401](../../src/wowooai/cli/desktop_cmd.py#L363-L401)：把原先只查 `icon.ico` 的逻辑改为按平台分流：

```python
if sys.platform == "darwin":
    icon_name = "icon.icns"
    candidates = (
        os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(sys.executable))),
            icon_name,
        ),
        os.path.join(repo_assets, icon_name),
    )
else:
    icon_name = "icon.ico"
    candidates = (
        os.path.join(os.path.dirname(sys.executable), icon_name),
        os.path.join(repo_assets, icon_name),
    )
```

macOS 路径推算说明：`sys.executable` = `<bundle>/Contents/Resources/env/bin/WowooAI`（hardlink to python3.10），往上跳 3 层得到 `<bundle>/Contents/Resources`，icon.icns 真实落在那里（由 build_macos.sh 拷贝）。

pywebview 启动后会读取 `webview.start(icon=icon_path)`，命中 cocoa.py 的 `setApplicationIconImage_` 分支，运行时覆盖 Dock 图标。

### §14.4 为什么是 C 方案而不是单方案

| 方案 | 改动文件 | 启动闪屏阶段 | 修真正根因 |
|---|---|---|---|
| A. 只改 desktop_cmd.py | 1 个 | ❌（启动 1-3 秒内仍是错图标） | ❌ |
| B. 只改 build_macos.sh | 1 个 | ✅ | ✅ |
| **C. 两个都改（已采用）** | 2 个 | ✅ | ✅（双保险） |

C 方案双保险：Info.plist 修通启动阶段，`setApplicationIconImage_` 兜底运行时；任一路径失败另一路径仍能保证图标正确。

### §14.5 Windows 影响评估

| 检查项 | 结论 |
|---|---|
| `icon.ico` 候选路径 | ✅ 不变 — `os.path.dirname(sys.executable) + "icon.ico"` 与 `scripts/pack/assets/icon.ico` 都保留 |
| `_apply_win_icon` 调用 | ✅ 仍在 `sys.platform == "win32"` 守卫下调用，路径未动 |
| `webview.start(icon=icon_path)` | ✅ Windows 上 `icon_path` 仍是 `.ico`，行为一致 |

### §14.6 校验

下次重新打包后执行：

```bash
# 1. Info.plist 包含两个新 key
plutil -p /Applications/WowooAI.app/Contents/Info.plist | grep -E 'CFBundlePackageType|CFBundleInfoDictionaryVersion'
# 期望：CFBundlePackageType => "APPL"; CFBundleInfoDictionaryVersion => "6.0"

# 2. desktop_cmd.py 平台分流逻辑
grep -n 'sys.platform == "darwin"' src/wowooai/cli/desktop_cmd.py
# 期望：命中 icon 选择分支

# 3. 清缓存后实测（macOS 自身图标缓存与代码无关）
sudo rm -rf /Library/Caches/com.apple.iconservices.store
killall Dock Finder
open /Applications/WowooAI.app
# 期望：Dock 图标 = 蓝色 W logo（启动瞬间 + 窗口出现后均正确）
```

### §14.7 回退

如需回到 §13 行为：
- 删除 Info.plist 中新增的两个 key
- `desktop_cmd.py` 的图标查找逻辑改回只查 `icon.ico`

---

## §15 2026-05-15 增量：打包产物 SHA-256 完整性哈希

### §15.1 背景

发布 DMG / NSIS 安装包时，需要在下载页或管理后台旁附一个 SHA-256 校验值，让客户验证下载完整性。此前需要人工 `shasum -a 256` 再手动粘贴，容易遗漏。

### §15.2 改动

| 文件 | 改动 |
|---|---|
| `scripts/pack/build_macos.sh` | 末尾追加 9 行：DMG 构建完成后 `shasum -a 256` 计算哈希，输出到终端并写入 `<DMG>.sha256` 边车文件 |
| `scripts/pack/build_win.ps1` | 末尾追加 8 行：NSIS 安装包构建完成后 `Get-FileHash -Algorithm SHA256` 计算哈希，输出到终端并写入 `<installer>.sha256` 边车文件 |

**macOS 关键片段**（`build_macos.sh`）：

```bash
if command -v shasum >/dev/null 2>&1; then
  DMG_SHA256="$(shasum -a 256 "${DMG_NAME}" | awk '{print $1}')"
  echo "== SHA-256: ${DMG_SHA256}  ${DMG_NAME} =="
  printf '%s  %s\n' "${DMG_SHA256}" "$(basename "${DMG_NAME}")" \
    > "${DMG_NAME}.sha256"
fi
```

**Windows 关键片段**（`build_win.ps1`）：

```powershell
$InstallerSha = (Get-FileHash -Algorithm SHA256 -Path $OutInstaller).Hash.ToLower()
$InstallerName = Split-Path -Leaf $OutInstaller
Write-Host "== SHA-256: $InstallerSha  $OutInstaller =="
Set-Content -Path ($OutInstaller + ".sha256") `
  -Value ("{0}  {1}" -f $InstallerSha, $InstallerName) -NoNewline
```

### §15.3 产物

| 平台 | 安装包 | 边车文件 |
|---|---|---|
| macOS | `dist/WowooAI-<ver>-macOS.dmg` | `dist/WowooAI-<ver>-macOS.dmg.sha256` |
| Windows | `dist/WowooAI-<ver>-Setup.exe` | `dist/WowooAI-<ver>-Setup.exe.sha256` |

`.sha256` 文件格式兼容 `shasum -c` / `sha256sum -c`：

```
<64位小写hex>  <文件名>
```

### §15.4 校验

```bash
# macOS
cat dist/WowooAI-*-macOS.dmg.sha256
shasum -a 256 -c dist/WowooAI-*-macOS.dmg.sha256
# 期望：OK

# Windows (PowerShell)
Get-Content dist\WowooAI-*-Setup.exe.sha256
# 手动比对 Get-FileHash 输出
```

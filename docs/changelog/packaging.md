# WowooAI 打包执行说明

> 本文只说明如何从当前源码构建 WowooAI wheel 与 macOS 桌面包，供交付给打包执行人使用。代码改造记录请看 [backend.md](backend.md) / [frontend.md](frontend.md)，本文不记录代码调整逻辑。

---

## §0 产物清单

| 产物 | 构建命令 | 输出路径 |
|---|---|---|
| Python wheel | `bash scripts/wheel_build.sh` | `dist/wowooai-<version>-py3-none-any.whl` |
| macOS `.app` | `bash scripts/pack/build_macos.sh` | `dist/WowooAI.app` |
| macOS DMG | `bash scripts/pack/build_macos.sh` | `dist/WowooAI-<version>-macOS.dmg` |

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
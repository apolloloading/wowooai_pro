# Windows 打包说明

> 本文是 Windows 平台的桌面包打包操作说明。macOS 打包流程见 [packaging-macos.md](packaging-macos.md)。
>
> 本文只描述「**怎么打包**」与「**已知踩坑**」，不承载源码改造逻辑。代码层面的变更记录在 [backend.md](backend.md) / [frontend.md](frontend.md)。

---

## 目录

- [§0 产物清单](#0-产物清单)
- [§1 前置环境](#1-前置环境)
- [§2 一键构建](#2-一键构建)
- [§3 build_win.ps1 流程概览](#3-build_winps1-流程概览)
- [§4 已知踩坑（Windows 特有）](#4-已知踩坑windows-特有)
  - [§4.1 conda-pack issue #154：`conda-unpack` 损坏字符串转义](#41-conda-pack-issue-154conda-unpack-损坏字符串转义)
  - [§4.2 PYTHONNOUSERSITE：隔离用户 site-packages](#42-pythonnousersite隔离用户-site-packages)
  - [§4.3 SSL 证书路径：`for /f` 阻塞与临时文件兜底](#43-ssl-证书路径for-f-阻塞与临时文件兜底)
  - [§4.4 双启动器：`.vbs` + `.bat` + `(Debug).bat`](#44-双启动器vbs--bat--debugbat)
  - [§4.5 预编译 `.pyc`：缩短首次冷启动](#45-预编译-pyc缩短首次冷启动)
- [§5 NSIS 安装器](#5-nsis-安装器)
- [§6 人工验收](#6-人工验收)
- [§7 2026-05-06 增量：python.exe PE 图标嵌入 + Add/Remove Programs DisplayIcon](#7-2026-05-06-增量pythonexe-pe-图标嵌入--addremove-programs-displayicon)
- [§8 2026-05-06 修复：Windows 主窗口 OS 标题栏 / 任务栏图标 + 中文文件名下载](#8-2026-05-06-修复windows-主窗口-os-标题栏--任务栏图标--中文文件名下载)
- [§9 2026-05-15 增量：NSIS 安装包 SHA-256 完整性哈希](#9-2026-05-15-增量nsis-安装包-sha-256-完整性哈希)

---

## §0 产物清单

| 产物 | 路径（相对仓库根） | 说明 |
|---|---|---|
| Wheel | `dist\wowooai-<version>-*.whl` | Python wheel，含 `console/dist/` 静态资源 |
| 解包后 conda 环境 | `dist\win-unpacked\` | `python.exe` + `Scripts\` + `Lib\site-packages\` 等，可直接运行 |
| 压缩 conda 环境 | `dist\wowooai-env.zip` | 由 conda-pack 产生；解压后即 `win-unpacked\` |
| NSIS 安装器 | `dist\wowooai-Setup-<version>.exe` | 最终交付给用户的一键安装包 |
| 安装器 SHA-256 | `dist\wowooai-Setup-<version>.exe.sha256` | 自动生成,内容格式 `<hash>  <文件名>` |

`win-unpacked\` 关键文件：

```
win-unpacked\
├── python.exe                       # 主 Python 解释器（不要替换符号链接）
├── wowooai.cmd                      # 入口 shim（绕开 Scripts\wowooai.exe 的失效路径）
├── wowooai Desktop.bat              # 主启动器（被 .vbs 包装为无控制台）
├── wowooai Desktop.vbs              # 双击入口（无窗口闪烁）
├── wowooai Desktop (Debug).bat      # 调试启动器（保留控制台 + pause）
├── icon.ico                         # NSIS / 快捷方式图标
├── Scripts\
│   └── conda-unpack.exe             # 仅构建期使用，安装后无意义
└── Lib\site-packages\
    ├── wowooai\console\index.html   # 前端静态资源
    ├── huggingface_hub\             # ⚠ 见 §4.1
    └── discord\                     # ⚠ 见 §4.1
```

---

## §1 前置环境

| 工具 | 版本要求 | 备注 |
|---|---|---|
| Windows | 10 / 11（x64） | Windows Server 2019+ 也可 |
| PowerShell | 5.1 或 7+ | 脚本以 `pwsh` / `powershell` 调用 |
| Conda（Miniconda / Anaconda） | 任意现代版本 | 必须能在 PowerShell 中 `conda --version` |
| Python | 3.10 | 与 wheel `requires-python` 对齐 |
| Node.js | 18+ | 含 `npm`（构建前端） |
| NSIS | 3.x | 必须把 `makensis.exe` 放进 `PATH` |
| 7-zip / Expand-Archive | 系统自带即可 | `Expand-Archive` 用于解压 conda-pack zip |

可用空间至少 10 GB（wheel 缓存、conda 环境解包、Playwright Chromium、NSIS 中间产物加在一起会超过 5 GB）。

---

## §2 一键构建

仓库根目录下：

```powershell
# 可选：强制重建 wheel（默认会复用 dist/ 中已有同版本 wheel）
Remove-Item -Force dist\wowooai-*.whl -ErrorAction SilentlyContinue

# 一键脚本：wheel → conda-pack → unpack → 修复 #154 → 预编译 .pyc → NSIS
powershell -ExecutionPolicy Bypass -File scripts\pack\build_win.ps1
```

完成后检查：

```powershell
Test-Path dist\win-unpacked\python.exe                # True
Test-Path dist\win-unpacked\Lib\site-packages\wowooai\console\index.html  # True
Test-Path dist\wowooai-Setup-*.exe                    # True
```

可选环境变量：

| 变量 | 默认 | 说明 |
|---|---|---|
| `DIST` | `dist` | 输出目录（脚本会拼成绝对路径） |

---

## §3 build_win.ps1 流程概览

[scripts/pack/build_win.ps1](../../scripts/pack/build_win.ps1) 的执行顺序：

1. 计算 `RepoRoot` / `Dist` / `Archive` / `Unpacked`，建立产物目录
2. **构建 wheel**：若 `dist\` 已有当前版本的 wheel 则跳过；否则调用 [scripts/wheel_build.ps1](../../scripts/wheel_build.ps1)（内部会先 `npm ci && npm run build` 再 `python -m build`），保证 wheel 内含 `wowooai/console/index.html`
3. **conda-pack**：调用 [scripts/pack/build_common.py](../../scripts/pack/build_common.py)，输出 `wowooai-env.zip`，并把构建期的 wheel 缓存到 `.cache\conda_unpack_wheels\`（供下一步修复使用）
4. **解包**：`Expand-Archive` 解到 `dist\win-unpacked\`
5. **conda-unpack**：执行 `Scripts\conda-unpack.exe` 改写 prefix；**紧接着修复 #154**（见 §4.1）
6. **预编译 `.pyc`**：`python -m compileall -q -j 0 <env>`（见 §4.5）
7. **写启动器**：`wowooai Desktop.bat` / `wowooai Desktop.vbs` / `wowooai Desktop (Debug).bat` / `wowooai.cmd`（见 §4.4）
8. **复制图标**：`scripts\pack\assets\icon.ico` → `<env>\icon.ico`
9. **NSIS 编译**：`makensis /Dwowooai_VERSION=<v> /DOUTPUT_EXE=... /DUNPACKED=... scripts\pack\desktop.nsi`

---

## §4 已知踩坑（Windows 特有）

> 这五项是 macOS 打包不会遇到、Windows 打包必须显式处理的「隐性陷阱」。`build_win.ps1` 里都已自动化，但任何修改这条流程的人必须理解为什么这样写。

### §4.1 conda-pack issue #154：`conda-unpack` 损坏字符串转义

**症状**：用户安装后双击启动器，进程秒退；`Lib\site-packages\huggingface_hub\file_download.py` / `discord\http.py` 等文件出现 `SyntaxError: unexpected character after line continuation character`。

**根因**：[conda/conda-pack#154](https://github.com/conda/conda-pack/issues/154) — `conda-unpack` 在重写路径前缀时会破坏 Windows 扩展长度路径前缀 `\\\\?\\` 的转义，把 `"\\\\?\\"`（合法）改成 `"\\"`（非法），命中下列包的源码：

| 受影响的包 | 命中字符串 |
|---|---|
| `huggingface_hub` | 文件下载里使用 `\\?\` 扩展长度路径前缀 |
| `discord.py` | `ARG_NAME_SUBREGEX` 包含 `\\?\*` |

**修复策略**：构建期把 wheel 缓存到 `.cache\conda_unpack_wheels\`（由 `build_common.py --cache-wheels` 写入）；`conda-unpack` 后立即用缓存里的原始 wheel 强制重装受影响的包：

```powershell
foreach ($pkg in $CondaUnpackAffectedPackages) {
  & $pythonExe -m pip install --force-reinstall --no-deps `
    --find-links $WheelsCache --no-index $pkg
}
# 紧跟着 import 校验，命中 SyntaxError 就 throw，不让损坏的包流到 NSIS
& $pythonExe -c "from huggingface_hub import file_download; print('ok')"
& $pythonExe -c "import discord; print('ok')"
```

**新增受害者怎么办**：如果新依赖也使用了 Windows 扩展长度路径或包含 `\\?\` 的字面量，把包名加进 `build_win.ps1` 顶部的 `$CondaUnpackAffectedPackages` 数组，重新构建即可。

---

### §4.2 `PYTHONNOUSERSITE`：隔离用户 site-packages

**症状**：用户机器上有同名包的全局安装（例如自己装过 `httpx` / `pydantic`），桌面包启动后导入了用户 `%APPDATA%\Python\Python310\site-packages\` 里的旧版本，类型签名不兼容，500 错或启动失败。

**根因**：`python.exe` 默认会把用户 site-packages 加到 `sys.path`。conda-pack 的 env 没有显式禁用 user site，安装后用户的 `%APPDATA%\Python\Python310\` 仍会被搜索到。

**修复策略**：所有启动器 `.bat` 顶部都设置：

```bat
set "PYTHONNOUSERSITE=1"
set "PATH=%~dp0;%~dp0Scripts;%PATH%"
```

`PYTHONNOUSERSITE=1` 让 `site.py` 跳过 user site；同时把 env 根目录前缀到 `PATH`，确保 `python` / `wowooai` 命令优先解析到包内 binary 而不是用户全局 Python。

校验（用户安装包后跑）：

```powershell
$env = "$env:LOCALAPPDATA\wowooai"
& "$env\python.exe" -c "import site; print(site.ENABLE_USER_SITE)"
# 期望：False
```

---

### §4.3 SSL 证书路径：`for /f` 阻塞与临时文件兜底

**症状**：在某些 AV/EDR 环境下，`.bat` 里 `for /f "tokens=*" %%i in ('python -c "..."') do set CERT_FILE=%%i` 会被阻塞或挂起，启动器卡在初始化阶段。

**根因**：`for /f` 调用子进程时部分安全软件对管道进行扫描；同时 `for /f` 对包含特殊字符的输出处理脆弱（中文路径、空格）。

**修复策略**：用临时文件中转，避免管道：

```bat
set "CERT_TMP=%TEMP%\wowooai_cert_%RANDOM%.txt"
"%~dp0python.exe" -u -c "import certifi; print(certifi.where())" > "%CERT_TMP%" 2>nul
set /p CERT_FILE=<"%CERT_TMP%"
del "%CERT_TMP%" 2>nul
if defined CERT_FILE (
  if exist "%CERT_FILE%" (
    set "SSL_CERT_FILE=%CERT_FILE%"
    set "REQUESTS_CA_BUNDLE=%CERT_FILE%"
    set "CURL_CA_BUNDLE=%CERT_FILE%"
  )
)
```

`%RANDOM%` 防止并发启动撞名；`set /p` 一次读首行，对 ASCII 路径稳定。

三个变量都需要：`SSL_CERT_FILE`（OpenSSL）、`REQUESTS_CA_BUNDLE`（requests / httpx 用 requests 后端时）、`CURL_CA_BUNDLE`（curl / pycurl）。

---

### §4.4 双启动器：`.vbs` + `.bat` + `(Debug).bat`

**症状（不修复时）**：直接把 `.bat` 设为 NSIS 快捷方式目标，用户双击会闪一下黑色控制台再出主窗口；命令行输出会被 antd 主窗口隐藏，但「黑屏一闪」体验差，且部分 IT 安全策略会把闪现的 cmd.exe 标记为可疑进程。

**修复策略**：写三个文件，分工明确：

| 文件 | 角色 | 控制台 | 谁调用 |
|---|---|---|---|
| `wowooai Desktop.bat` | 主启动逻辑（设置 `PYTHONNOUSERSITE` / `PATH` / SSL / 调 `wowooai desktop`） | 隐藏 | 被 `.vbs` 调用 |
| `wowooai Desktop.vbs` | 无窗口包装：`WshShell.Run "...bat", 0, False` | 无 | NSIS 主快捷方式 |
| `wowooai Desktop (Debug).bat` | 同主 .bat，但保留 `echo` 与末尾 `pause`，把 log-level 默认改为 `debug` | 显示 | 用户从开始菜单 / 桌面 Debug 快捷方式启动 |

`.vbs` 实现：

```vbs
Set WshShell = CreateObject("WScript.Shell")
batPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\wowooai Desktop.bat"
WshShell.Run Chr(34) & batPath & Chr(34), 0, False
```

第二个参数 `0` 即 `SW_HIDE`，第三个 `False` 表示不等待，`Chr(34)` 包裹路径处理空格。

NSIS 主快捷方式指向 `.vbs`、Debug 快捷方式指向 `(Debug).bat`，详见 [scripts/pack/desktop.nsi](../../scripts/pack/desktop.nsi)。

> 另外还写了一个 `wowooai.cmd` shim 在 env 根目录：`@"%~dp0python.exe" -u -m wowooai %*`。它绕开了 `Scripts\wowooai.exe`（conda-pack 后这个 entry point 内嵌的 Python 路径会指向旧 prefix，命令行调用 `wowooai cron ...` 会找不到解释器）。

---

### §4.5 预编译 `.pyc`：缩短首次冷启动

**症状（不修复时）**：用户首次启动桌面包，所有 `.py` 都要在第一次 import 时编译成 `.pyc`，conda 环境包含约 5 万个 Python 文件，机械硬盘上能多花 8–15 秒。

**修复策略**：构建期一次性把整棵 env 编译成 `.pyc`：

```powershell
& $pythonExe -m compileall -q -j 0 $EnvRoot
```

参数说明：

- `-q`：安静模式，只输出错误（构建日志整洁）
- `-j 0`：用所有 CPU 核并行编译（构建机上能从 ~2 分钟降到 ~20 秒）

编译产物 `*.pyc` 会落在每个包的 `__pycache__\` 目录，NSIS 打包时会一并带进安装器。安装到用户机器后，import 直接读 `.pyc`，跳过 source-to-bytecode 步骤。

如果某些 `.py` 在打包机器上语法不兼容（罕见），`compileall` 会返回非零，脚本不会 throw，只打 WARN，原因是这些包在用户机器上仍然能在 import 时 fallback 到运行时编译。

---

## §5 NSIS 安装器

NSIS 脚本在 [scripts/pack/desktop.nsi](../../scripts/pack/desktop.nsi)，关键设定：

- 默认安装到 `$LOCALAPPDATA\wowooai`（用户级，不需要管理员权限）
- MUI2 + SimpChinese 语言包
- 主快捷方式 → `wowooai Desktop.vbs`（无控制台）
- Debug 快捷方式 → `wowooai Desktop (Debug).bat`
- 卸载器清理：开始菜单项、桌面快捷方式、安装目录、注册表 `HKCU\Software\wowooai`

`build_win.ps1` 通过 `/D` 注入三个变量：

```
/Dwowooai_VERSION=<x.y.z>
/DOUTPUT_EXE=<absolute path to dist\wowooai-Setup-x.y.z.exe>
/DUNPACKED=<absolute path to dist\win-unpacked>
```

`makensis` 必须能在当前 PowerShell 的 `PATH` 里找到，否则脚本会显式 throw。

---

## §6 人工验收

打包完成后，把 `dist\wowooai-Setup-<version>.exe` 拷到一台**干净的 Windows 10/11** 机器（最好没有装过 Python / Conda），按以下顺序验收：

1. **安装与启动**

   ```powershell
   # 双击 .exe 或命令行：
   .\wowooai-Setup-<version>.exe /S        # 静默安装到 $LOCALAPPDATA\wowooai
   ```

   开始菜单点击「wowooai Desktop」→ 主窗口应在 5–15 秒内出现，无黑色 cmd.exe 闪现。

2. **检查没有泄漏的用户 site-packages**

   ```powershell
   $env = "$env:LOCALAPPDATA\wowooai"
   & "$env\python.exe" -c "import site; print(site.ENABLE_USER_SITE)"
   # 期望：False
   ```

3. **检查 #154 修复**

   ```powershell
   & "$env\python.exe" -c "from huggingface_hub import file_download; print('ok')"
   & "$env\python.exe" -c "import discord; print('ok')"
   # 都期望 ok
   ```

4. **桌面 / Office / PDF 依赖可 import**

   ```powershell
   & "$env\python.exe" -c "import openpyxl, docx, pptx, pdfplumber, playwright; print('ok')"
   ```

5. **MCP / npx 可解析**（如果安装包内含 nodejs）

   ```powershell
   & "$env\nodejs\npx.cmd" --version
   ```

6. **关闭与端口释放**

   - 关闭主窗口 → 任务管理器中 `python.exe`（或 `WowooAI.exe`，若已重命名）应在 1–3 秒内消失
   - `netstat -ano | findstr :8088`（或桌面包的随机端口）应无残留
   - 若使用 Debug 启动器，控制台会显示「[Exit] wowooai Desktop closed」并 `pause`

7. **卸载干净**

   ```powershell
   & "$env\Uninstall.exe" /S
   Test-Path "$env"                                    # False
   Test-Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\wowooai"  # False
   ```

   `~\.wowooai\`（用户工作区）默认保留，避免删除用户数据。

任何一步失败都属于打包回归，必须先 fix 再交付。


---

## §7 2026-05-06 增量：python.exe PE 图标嵌入 + Add/Remove Programs DisplayIcon

### 背景

§5 的 NSIS `MUI_ICON` 和 `CreateShortcut "..." "$INSTDIR\icon.ico"` 只解决了**安装向导**和**快捷方式 .lnk**的图标问题。但下列场景仍会暴露 conda 默认蛇图标:

1. **任务管理器进程列表** — 显示 `python.exe` 内嵌图标(conda 蛇)
2. **直接双击 `python.exe` 或被外部脚本 invoke** — Windows 资源管理器读 PE 资源
3. **Alt-Tab / Win+Tab 缩略图**(直启场景下)
4. **「打开文件位置」跳转后看到的 EXE** — 资源管理器
5. **设置 → 应用 / 控制面板程序和功能列表** — 没有 `DisplayIcon` 注册项时显示空白/默认占位

§5 的快捷方式覆盖只在用户**通过快捷方式**启动时生效,以上场景都直接读 PE 资源或注册表 `DisplayIcon`,所以即使 `icon.ico` 已经在 env 根目录,这些位置也不会显示品牌图标。

### 修复 1:rcedit 改写 python.exe / pythonw.exe PE 资源

**文件**:`scripts/pack/build_win.ps1`

在原本的 `Copy-Item $IconSrc -Destination $EnvRoot -Force` 后,新增 rcedit 自动下载 + `--set-icon` 步骤:

```powershell
# Embed icon.ico into python.exe / pythonw.exe PE resource so the brand icon
# shows in Task Manager, Alt-Tab thumbnails, "Open File Location" jumps, and
# direct-launch scenarios — not just .lnk shortcuts.
#
# Uses rcedit-x64 (https://github.com/electron/rcedit). Auto-downloaded into
# .cache/ on first run. Failure is non-fatal: shortcuts already have the right
# icon, so the .exe-resource patch is a "nice to have" cosmetic fix.
$IconAtEnvRoot = Join-Path $EnvRoot "icon.ico"
if (Test-Path $IconAtEnvRoot) {
  $RceditCache = Join-Path $RepoRoot ".cache\rcedit"
  $Rcedit = Join-Path $RceditCache "rcedit-x64.exe"
  if (-not (Test-Path $Rcedit)) {
    Write-Host "[build_win] Downloading rcedit-x64.exe..."
    New-Item -ItemType Directory -Force -Path $RceditCache | Out-Null
    try {
      $RceditUrl = "https://github.com/electron/rcedit/releases/download/v2.0.0/rcedit-x64.exe"
      Invoke-WebRequest -Uri $RceditUrl -OutFile $Rcedit -UseBasicParsing
    } catch {
      Write-Host "[build_win] WARN: rcedit download failed: $_" -ForegroundColor Yellow
      $Rcedit = $null
    }
  }
  if ($Rcedit -and (Test-Path $Rcedit)) {
    foreach ($exeName in @("python.exe", "pythonw.exe")) {
      $TargetExe = Join-Path $EnvRoot $exeName
      if (Test-Path $TargetExe) {
        Write-Host "[build_win] Embedding icon into $exeName ..."
        & $Rcedit $TargetExe --set-icon $IconAtEnvRoot
        if ($LASTEXITCODE -ne 0) {
          Write-Host "[build_win] WARN: rcedit failed for $exeName (exit $LASTEXITCODE)" -ForegroundColor Yellow
        }
      }
    }
  } else {
    Write-Host "[build_win] WARN: skipping python.exe icon embed (rcedit unavailable)" -ForegroundColor Yellow
  }
}
```

要点:

- **rcedit**:Electron 项目维护的 PE 资源编辑工具,~1.8 MB 单文件,无运行时依赖
- **缓存到 `.cache/rcedit/`**:首次构建联网下载,后续命中本地缓存
- **同时改 `python.exe` 和 `pythonw.exe`**:`pythonw.exe` 是不带控制台的 GUI 子集,部分 webview 场景会用;两者 PE 资源都得改
- **失败非致命**:rcedit 下载或写入失败仅 WARN,不让 `$ErrorActionPreference = "Stop"` 中断主流程;快捷方式 .lnk 仍能保持品牌图标
- **执行顺序**:必须放在 `Copy-Item $IconSrc` 之后(因为读取 `$IconAtEnvRoot`),且建议放在 `compileall` 步骤之后(避免 rcedit 写入引发缓存不一致;不过 rcedit 仅改 PE 资源段,不影响代码段,实际两种顺序都可)

### 修复 2:NSIS 写入 Add/Remove Programs `DisplayIcon`

**文件**:`scripts/pack/desktop.nsi`

在 `Section "wowooai Desktop"` 末尾追加注册表写入,卸载时同步清理。完整 diff:

```nsis
!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\wowooai"

Section "wowooai Desktop" SEC01
  SetOutPath "$INSTDIR"
  File /r "${UNPACKED}\*.*"
  WriteRegStr HKCU "Software\wowooai" "InstallPath" "$INSTDIR"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Main shortcut - uses VBS to hide console window
  CreateShortcut "$SMPROGRAMS\wowooai Desktop.lnk" "$INSTDIR\wowooai Desktop.vbs" "" "$INSTDIR\icon.ico" 0
  CreateShortcut "$DESKTOP\wowooai Desktop.lnk" "$INSTDIR\wowooai Desktop.vbs" "" "$INSTDIR\icon.ico" 0

  ; Debug shortcut - shows console window for troubleshooting
  CreateShortcut "$SMPROGRAMS\wowooai Desktop (Debug).lnk" "$INSTDIR\wowooai Desktop (Debug).bat" "" "$INSTDIR\icon.ico" 0

  ; Add/Remove Programs entry — DisplayIcon makes Settings/Control Panel
  ; show the brand icon instead of a blank/default placeholder.
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayName" "wowooai Desktop"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayVersion" "${wowooai_VERSION}"
  WriteRegStr HKCU "${UNINST_KEY}" "Publisher" "wowooai"
  WriteRegStr HKCU "${UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayIcon" "$INSTDIR\icon.ico,0"
  WriteRegStr HKCU "${UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\wowooai Desktop.lnk"
  Delete "$SMPROGRAMS\wowooai Desktop (Debug).lnk"
  Delete "$DESKTOP\wowooai Desktop.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\wowooai"
  DeleteRegKey HKCU "${UNINST_KEY}"
SectionEnd
```

要点:

- **`HKCU` 写法**:与 §5 `RequestExecutionLevel user` 一致,无需管理员权限。如果改为系统级安装,得改 `HKLM` 并重新评估权限
- **`DisplayIcon "$INSTDIR\icon.ico,0"`**:`,0` = 资源 index 0,标准写法,Windows Settings 与控制面板都按这个 key 找图标
- **`DisplayName`/`DisplayVersion`/`Publisher`**:同时写入这几个 key,让卸载列表条目同时正确显示文本与图标
- **`NoModify=1, NoRepair=1`**:隐藏「修改」「修复」按钮(因为没实现这两条路径)
- **卸载时 `DeleteRegKey HKCU "${UNINST_KEY}"`**:必须显式清理,否则卸载完成后控制面板里仍残留死条目

### 修复后图标覆盖矩阵

| 场景 | 改动前 | 改动后 |
|---|---|---|
| 开始菜单 / 桌面快捷方式 | ✅ 品牌图标 | ✅(不变) |
| 任务管理器进程列表 | ❌ conda 蛇 | ✅ 品牌图标(rcedit) |
| Alt-Tab / Win+Tab 缩略图(快捷方式启动) | ⚠️ 取决于实际窗口 owner | ✅ 品牌图标 |
| 直接双击 `python.exe` | ❌ conda 蛇 | ✅ 品牌图标(rcedit) |
| pywebview 标题栏 / 任务栏(无 icon kwarg) | ❌ pywebview 默认 | ✅ 品牌图标(由 [backend.md §29](backend.md) 在 `desktop_cmd.py` 注入 `icon=...` 解决) |
| Settings → 应用 / 控制面板程序列表 | ❌ 空白/占位 | ✅ 品牌图标 + 名称 + 版本 |
| NSIS 安装向导 | ✅(MUI_ICON) | ✅(不变) |

### 校验

构建后(在 Windows 主机):

```powershell
# 1) python.exe / pythonw.exe PE 资源已嵌入图标
$env = "$env:LOCALAPPDATA\wowooai"
# 资源管理器查看 python.exe 属性 → 应显示蓝色 W
explorer.exe /select,"$env\python.exe"

# 2) Add/Remove Programs 注册表写入完整
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\wowooai"
# 期望输出:DisplayName / DisplayVersion / Publisher / DisplayIcon / UninstallString / NoModify / NoRepair

# 3) 设置 → 应用 中应能看到 wowooai Desktop 条目带蓝色 W 图标

# 4) rcedit 缓存
Test-Path "$RepoRoot\.cache\rcedit\rcedit-x64.exe"   # True (首次构建后)
```

构建脚本静态校验(任意平台):

```bash
grep -n 'rcedit-x64.exe --set-icon' scripts/pack/build_win.ps1
# 期望:命中 1 处(在 foreach 内)

grep -n 'DisplayIcon' scripts/pack/desktop.nsi
# 期望:命中 1 处

grep -n 'DeleteRegKey HKCU "\${UNINST_KEY}"' scripts/pack/desktop.nsi
# 期望:命中 1 处
```

### 风险与回退

| 风险 | 评估 |
|---|---|
| rcedit 下载失败(打包机离线 / GitHub 不可达) | 自动 fallback 到 WARN,主流程不中断;快捷方式仍带正确图标 |
| rcedit 改 PE 后破坏 `python.exe` 签名 | conda 发行的 `python.exe` 本身不签名,无影响。如果未来切到签名 Python,需要重新签��� |
| `compileall` 在 rcedit 之前 vs 之后 | 当前顺序是 compileall → 拷贝 icon → rcedit。rcedit 只改 PE 资源段,不影响 `__pycache__` |
| 写入 `HKCU\...\Uninstall\wowooai` 与现有应用冲突 | key 名 `wowooai` 唯一,无第三方占用 |

回退:把上述 PowerShell foreach 块和 NSIS 新增的 7 行 `WriteRegStr/DWORD` 全部删除,即可恢复改动前行为。卸载时残留的 `Uninstall\wowooai` 注册项可手动 `reg delete` 清理。



## §8 2026-05-06 修复：Windows 主窗口 OS 标题栏 / 任务栏图标 + 中文文件名下载

打包后 Windows 桌面包反馈两个问题,均落点在 `src/wowooai/cli/desktop_cmd.py`,详见 `docs/changelog/backend.md` §29、§30。本节只记录与 Windows 打包链路相关的部分。

### 1. 标题栏 / 任务栏图标仍是 python.exe

仅靠 `webview.start(icon=...)` 不够 — Win11 按宿主进程对窗口分组并读取标题栏 icon。修复路径:

- `desktop_cmd.py` 新增 `_apply_win_icon(window, icon_path)`,内部 `SetCurrentProcessExplicitAppUserModelID("AgentScope.WowooAI.Desktop.1")` + 后台线程 `FindWindowW("WowooAI Desktop")` + `SendMessageW(hwnd, WM_SETICON, ...)` 注入 `icon.ico`。
- 仅在 `sys.platform == "win32"` 调用,macOS 永不进入。
- `icon.ico` 路径:打包时由 `scripts/pack/build_win.ps1` 拷贝到 `<env_root>/icon.ico`(与 `python.exe` 同目录),`desktop_cmd.py` 优先从 `os.path.dirname(sys.executable)` 取。

打包侧无需新增步骤 — `build_win.ps1` 现有"拷贝 icon.ico 到 EnvRoot"块即可满足查找路径,与 §7 中 rcedit 嵌入 PE icon 双管齐下:
- rcedit 解决 Task Manager / Alt-Tab / 直接启动 `python.exe` 时显示的 PE icon。
- WM_SETICON 解决主窗口运行期标题栏 + 任务栏 icon。
- AppUserModelID 解决 Win11 把 WowooAI 与其他 python 窗口分组的问题。

### 2. 中文 / 非 ASCII 文件名下载静默失败

`WebViewAPI.save_file(url, filename)` 对 URL 做百分号编码后再 `urlopen`,避免 `UnicodeEncodeError`。纯 Python 改动,打包链路无变化,仅说明 Windows 打包包受影响最重(用户上传的合同 / 报销单文件名常含中文)。

### 校验

```bash
grep -n '_apply_win_icon\|WM_SETICON' src/wowooai/cli/desktop_cmd.py
grep -n 'encoded_url' src/wowooai/cli/desktop_cmd.py
grep -n 'icon.ico' scripts/pack/build_win.ps1
# 期望:build_win.ps1 仍把 icon.ico 拷贝到 EnvRoot
```

### 回退

仅删除 `desktop_cmd.py` 中:
- `_apply_win_icon` 函数。
- `desktop_cmd()` 内对 `_apply_win_icon(window, icon_path)` 的调用。
- `save_file` 中 `encoded_url` 构造及两处 `urlopen(encoded_url)` 改回 `urlopen(url)`。

打包脚本(`build_win.ps1` / `desktop.nsi`)无须改动。

---

## §9 2026-05-15 增量：NSIS 安装包 SHA-256 完整性哈希

### 背景

发布 NSIS 安装包到管理后台 / 下载页时,需要附 SHA-256 校验值供客户验证下载完整性。此前需人工 `Get-FileHash` 后手动粘贴,容易遗漏或贴错。

### 改动

`scripts/pack/build_win.ps1` 末尾追加 8 行:NSIS 编译完成、`Test-Path $OutInstaller` 验证存在后,立即计算 SHA-256 并写边车文件:

```powershell
$InstallerSha = (Get-FileHash -Algorithm SHA256 -Path $OutInstaller).Hash.ToLower()
$InstallerName = Split-Path -Leaf $OutInstaller
Write-Host "== SHA-256: $InstallerSha  $OutInstaller =="
Set-Content -Path ($OutInstaller + ".sha256") `
  -Value ("{0}  {1}" -f $InstallerSha, $InstallerName) -NoNewline
```

### 产物

| 文件 | 说明 |
|---|---|
| `dist\wowooai-Setup-<version>.exe` | NSIS 安装包(原有) |
| `dist\wowooai-Setup-<version>.exe.sha256` | 边车哈希文件,格式 `<64位小写hex>  <文件名>`,兼容 `sha256sum -c` / `shasum -c` 校验 |

### 校验

```powershell
# 查看哈希
Get-Content dist\wowooai-Setup-*.exe.sha256

# 重新计算并比对
Get-FileHash -Algorithm SHA256 -Path dist\wowooai-Setup-*.exe
```

macOS / Linux 下校验 Windows 安装包:

```bash
shasum -a 256 -c dist/wowooai-Setup-*.exe.sha256
# 期望:OK
```

### 平行改动

macOS 侧 `scripts/pack/build_macos.sh` 同步追加 `shasum -a 256` 输出 + 边车文件,详见 [packaging-macos.md §15](packaging-macos.md#15-2026-05-15-增量打包产物-sha-256-完整性哈希)。

### 回退

删除 `scripts/pack/build_win.ps1` 末尾�� 5 行(从 `$InstallerSha = ...` 到 `Set-Content ...`)即可。删除后已发布的 `.sha256` 边车文件不会被自动清理,需手动删除。

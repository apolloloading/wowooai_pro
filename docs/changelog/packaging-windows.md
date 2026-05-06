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

---

## §0 产物清单

| 产物 | 路径（相对仓库根） | 说明 |
|---|---|---|
| Wheel | `dist\wowooai-<version>-*.whl` | Python wheel，含 `console/dist/` 静态资源 |
| 解包后 conda 环境 | `dist\win-unpacked\` | `python.exe` + `Scripts\` + `Lib\site-packages\` 等，可直接运行 |
| 压缩 conda 环境 | `dist\wowooai-env.zip` | 由 conda-pack 产生；解压后即 `win-unpacked\` |
| NSIS 安装器 | `dist\wowooai-Setup-<version>.exe` | 最终交付给用户的一键安装包 |

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

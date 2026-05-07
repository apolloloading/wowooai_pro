# One-click build: console -> conda-pack -> NSIS .exe. Run from repo root.
# Requires: conda, node/npm (for console), NSIS (makensis) on PATH.

$ErrorActionPreference = "Stop"
$RepoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location $RepoRoot
Write-Host "[build_win] REPO_ROOT=$RepoRoot"
$PackDir = $PSScriptRoot
$Dist = if ($env:DIST) { $env:DIST } else { "dist" }
$Archive = Join-Path $Dist "wowooai-env.zip"
$Unpacked = Join-Path $Dist "win-unpacked"
$NsiPath = Join-Path $PackDir "desktop.nsi"

# Packages affected by conda-unpack bug on Windows (conda-pack Issue #154)
# conda-unpack corrupts Python string escaping when replacing path prefixes.
# Example: "\\\\?\\" (correct) -> "\\" (SyntaxError)
# Solution: Reinstall these packages after conda-unpack to restore correct files.
# See: issue.md, scripts/pack/WINDOWS_FIX.md
$CondaUnpackAffectedPackages = @(
  "huggingface_hub"  # Uses Windows extended-length path prefix (\\?\)
  "discord.py"       # ARG_NAME_SUBREGEX contains \\?\* which gets corrupted
)

New-Item -ItemType Directory -Force -Path $Dist | Out-Null

# ============================================================
# packbot fast-path: skip the slow conda env create + pip install
# pipeline if a healthy base env is available via $PACKBOT_BASE_ENV.
# packbot has already replaced scripts/pack/build_common.py with the
# fast-pack shim before invoking this script.
# ============================================================
$SkipSlowBuild = $false
if ($env:PACKBOT_BASE_ENV -and (Test-Path "$env:PACKBOT_BASE_ENV\python.exe")) {
    Write-Host "[build_win] PACKBOT fast-path: PACKBOT_BASE_ENV=$env:PACKBOT_BASE_ENV"

    # Ensure wheel is built first (shim needs it in dist/)
    $VersionFile = Join-Path $RepoRoot "src\wowooai\__version__.py"
    $CurrentVersion = ""
    if (Test-Path $VersionFile) {
        $m = (Get-Content $VersionFile -Raw) -match '__version__\s*=\s*"([^"]+)"'
        if ($m) { $CurrentVersion = $Matches[1] }
    }
    $needWheel = $true
    if ($CurrentVersion) {
        $existingWheels = Get-ChildItem -Path (Join-Path $Dist "wowooai-$CurrentVersion-*.whl") -ErrorAction SilentlyContinue
        if ($existingWheels.Count -gt 0) { $needWheel = $false }
    }
    if ($needWheel) {
        $WheelBuildScript = Join-Path $RepoRoot "scripts\wheel_build.ps1"
        & $WheelBuildScript
        if ($LASTEXITCODE -ne 0) { throw "wheel_build.ps1 failed: $LASTEXITCODE" }
    }

    # Invoke shim with the BASE ENV's python (so the shim can import conda_pack etc.)
    Write-Host "[build_win] Invoking fast-pack shim..."
    & "$env:PACKBOT_BASE_ENV\python.exe" "$PackDir\build_common.py" `
        --output $Archive --format zip --cache-wheels
    if ($LASTEXITCODE -eq 0 -and (Test-Path $Archive)) {
        Write-Host "[build_win] fast-path SUCCESS, skipping slow build"
        $SkipSlowBuild = $true
    } else {
        Write-Host "[build_win] fast-path FAILED (rc=$LASTEXITCODE), falling back"
    }
}

if (-not $SkipSlowBuild) {

Write-Host "== Building wheel (includes console frontend) =="
# Skip wheel_build if dist already has a wheel for current version
$VersionFile = Join-Path $RepoRoot "src\wowooai\__version__.py"
$CurrentVersion = ""
if (Test-Path $VersionFile) {
  $m = (Get-Content $VersionFile -Raw) -match '__version__\s*=\s*"([^"]+)"'
  if ($m) { $CurrentVersion = $Matches[1] }
}
$RunWheelBuild = $true
if ($CurrentVersion) {
  $wheelGlob = Join-Path $Dist "wowooai-$CurrentVersion-*.whl"
  $existingWheels = Get-ChildItem -Path $wheelGlob -ErrorAction SilentlyContinue
  if ($existingWheels.Count -gt 0) {
    Write-Host "dist/ already has wheel for version $CurrentVersion, skipping."
    $RunWheelBuild = $false
  } else {
    # Clean up old wheels to avoid confusion
    $oldWheels = Get-ChildItem -Path (Join-Path $Dist "wowooai-*.whl") -ErrorAction SilentlyContinue
    if ($oldWheels.Count -gt 0) {
      Write-Host "Removing old wheel files: $($oldWheels | ForEach-Object { $_.Name })"
      $oldWheels | Remove-Item -Force
    }
  }
}
if ($RunWheelBuild) {
  $WheelBuildScript = Join-Path $RepoRoot "scripts\wheel_build.ps1"
  if (-not (Test-Path $WheelBuildScript)) {
    throw "wheel_build.ps1 not found: $WheelBuildScript"
  }
  & $WheelBuildScript
  if ($LASTEXITCODE -ne 0) { throw "wheel_build.ps1 failed with exit code $LASTEXITCODE" }
}

Write-Host "== Building conda-packed env =="
& python $PackDir\build_common.py --output $Archive --format zip --cache-wheels
if ($LASTEXITCODE -ne 0) {
  throw "build_common.py failed with exit code $LASTEXITCODE"
}
if (-not (Test-Path $Archive)) {
  throw "Archive not created: $Archive"
}

}  # end of if (-not $SkipSlowBuild)

Write-Host "== Unpacking env =="
if (Test-Path $Unpacked) { Remove-Item -Recurse -Force $Unpacked }
Expand-Archive -Path $Archive -DestinationPath $Unpacked -Force
$unpackedRoot = Get-ChildItem -Path $Unpacked -ErrorAction SilentlyContinue | Measure-Object
Write-Host "[build_win] Unpacked entries in $Unpacked : $($unpackedRoot.Count)"

# Resolve env root: conda-pack usually puts python.exe at archive root; allow one nested dir.
$EnvRoot = $Unpacked
if (-not (Test-Path (Join-Path $EnvRoot "python.exe"))) {
  $found = Get-ChildItem -Path $Unpacked -Directory -ErrorAction SilentlyContinue |
    Where-Object { Test-Path (Join-Path $_.FullName "python.exe") } |
    Select-Object -First 1
  if ($found) { $EnvRoot = $found.FullName; Write-Host "[build_win] Env root: $EnvRoot" }
}
if (-not (Test-Path (Join-Path $EnvRoot "python.exe"))) {
  throw "python.exe not found in unpacked env (checked $Unpacked and one level down)."
}
if (-not [System.IO.Path]::IsPathRooted($EnvRoot)) {
  $EnvRoot = Join-Path $RepoRoot $EnvRoot
}
Write-Host "[build_win] python.exe found at env root: $EnvRoot"

# Rewrite prefix in packed env so paths point to current location (required after move).
$CondaUnpack = Join-Path $EnvRoot "Scripts\conda-unpack.exe"
if (Test-Path $CondaUnpack) {
  Write-Host "[build_win] Running conda-unpack..."
  & $CondaUnpack
  if ($LASTEXITCODE -ne 0) { throw "conda-unpack failed with exit code $LASTEXITCODE" }
  
  # Fix conda-unpack bug: it corrupts Python string escaping on Windows
  # See: issue.md and https://github.com/conda/conda-pack/issues/154
  # Solution: Reinstall affected packages using cached wheels
  Write-Host "[build_win] Fixing conda-unpack corruption by reinstalling affected packages..."
  $WheelsCache = Join-Path $RepoRoot ".cache\conda_unpack_wheels"
  if (Test-Path $WheelsCache) {
    $pythonExe = Join-Path $EnvRoot "python.exe"
    
    foreach ($pkg in $CondaUnpackAffectedPackages) {
      Write-Host "  Reinstalling $pkg..."
      & $pythonExe -m pip install --force-reinstall --no-deps `
        --find-links $WheelsCache --no-index $pkg
      if ($LASTEXITCODE -ne 0) {
        Write-Host "  WARN: Failed to reinstall $pkg (exit code: $LASTEXITCODE)" -ForegroundColor Yellow
      }
    }
    
    # Verify the fix worked
    Write-Host "[build_win] Verifying fix..."
    & $pythonExe -c "from huggingface_hub import file_download; print('✓ huggingface_hub import OK')"
    if ($LASTEXITCODE -ne 0) {
      throw "CRITICAL: huggingface_hub still has import errors after reinstall. See issue.md"
    }
    & $pythonExe -c "import discord; print('✓ discord.py import OK')"
    if ($LASTEXITCODE -ne 0) {
      throw "CRITICAL: discord.py still has import errors after reinstall."
    }
    Write-Host "[build_win] ✓ conda-unpack corruption fixed successfully."
  } else {
    Write-Host "[build_win] WARN: wheels_cache not found at $WheelsCache" -ForegroundColor Yellow
    Write-Host "[build_win] WARN: Cannot fix conda-unpack corruption. App may fail to start." -ForegroundColor Yellow
  }
} else {
  Write-Host "[build_win] WARN: conda-unpack.exe not found at $CondaUnpack, skipping."
}

Write-Host "== Pre-compiling Python bytecode for faster startup =="
$pythonExe = Join-Path $EnvRoot "python.exe"
if (Test-Path $pythonExe) {
  Write-Host "[build_win] Compiling all .py files to .pyc..."
  $compileStart = Get-Date
  
  # Compile all Python files to bytecode
  # -q: quiet mode (only show errors)
  # -j 0: use all CPU cores for parallel compilation
  & $pythonExe -m compileall -q -j 0 $EnvRoot
  
  if ($LASTEXITCODE -eq 0) {
    $compileEnd = Get-Date
    $compileTime = ($compileEnd - $compileStart).TotalSeconds
    Write-Host "[build_win] ✓ Bytecode compilation completed in $($compileTime.ToString('F1')) seconds"
    
    # Count compiled files for reporting
    $pycCount = (Get-ChildItem -Path $EnvRoot -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "[build_win] Generated $pycCount .pyc files (these will be included in installer)"
  } else {
    Write-Host "[build_win] WARN: Bytecode compilation had some errors (exit code: $LASTEXITCODE)" -ForegroundColor Yellow
    Write-Host "[build_win] This is usually not critical - app will compile on first run" -ForegroundColor Yellow
  }
} else {
  Write-Host "[build_win] WARN: python.exe not found at $pythonExe, skipping bytecode compilation" -ForegroundColor Yellow
}

# Main launcher .bat (will be hidden by VBS)
$LauncherBat = Join-Path $EnvRoot "wowooai Desktop.bat"
@"
@echo off
cd /d "%~dp0"

REM Isolate packaged Python from user site-packages to prevent conflicts
set "PYTHONNOUSERSITE=1"

REM Preserve system PATH for accessing system commands
REM Prepend packaged env to PATH so packaged Python takes precedence
set "PATH=%~dp0;%~dp0Scripts;%PATH%"

REM Log level: env var wowooai_LOG_LEVEL or default to "info"
if not defined wowooai_LOG_LEVEL set "wowooai_LOG_LEVEL=info"

REM Set SSL certificate paths for packaged environment
REM Use temp file to avoid for /f blocking issue in bat scripts
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

if not exist "%USERPROFILE%\.wowooai\config.json" (
  "%~dp0python.exe" -u -m wowooai init --defaults --accept-security
)
"%~dp0python.exe" -u -m wowooai desktop --log-level %wowooai_LOG_LEVEL%
"@ | Set-Content -Path $LauncherBat -Encoding ASCII

# Debug launcher .bat (shows console)
$DebugBat = Join-Path $EnvRoot "wowooai Desktop (Debug).bat"
@"
@echo off
cd /d "%~dp0"

REM Isolate packaged Python from user site-packages to prevent conflicts
set "PYTHONNOUSERSITE=1"

REM Preserve system PATH for accessing system commands
REM Prepend packaged env to PATH so packaged Python takes precedence
set "PATH=%~dp0;%~dp0Scripts;%PATH%"

REM Debug mode: use debug log level by default (can override with wowooai_LOG_LEVEL)
if not defined wowooai_LOG_LEVEL set "wowooai_LOG_LEVEL=debug"

REM Set SSL certificate paths for packaged environment
REM Use temp file to avoid for /f blocking issue in bat scripts
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

echo ====================================
echo wowooai Desktop - Debug Mode
echo ====================================
echo Working Directory: %cd%
echo Python: "%~dp0python.exe"
echo PATH: %PATH%
echo PYTHONNOUSERSITE: %PYTHONNOUSERSITE%
echo Log Level: %wowooai_LOG_LEVEL%
echo SSL_CERT_FILE: %SSL_CERT_FILE%
echo REQUESTS_CA_BUNDLE: %REQUESTS_CA_BUNDLE%
echo CURL_CA_BUNDLE: %CURL_CA_BUNDLE%
echo.
if not exist "%USERPROFILE%\.wowooai\config.json" (
  echo [Init] Creating config...
  "%~dp0python.exe" -u -m wowooai init --defaults --accept-security
)
echo [Launch] Starting wowooai Desktop with log-level=%wowooai_LOG_LEVEL%...
echo Press Ctrl+C to stop
echo.
"%~dp0python.exe" -u -m wowooai desktop --log-level %wowooai_LOG_LEVEL%
echo.
echo [Exit] wowooai Desktop closed
pause
"@ | Set-Content -Path $DebugBat -Encoding ASCII

# VBScript launcher (no console window)
$LauncherVbs = Join-Path $EnvRoot "wowooai Desktop.vbs"
@"
Set WshShell = CreateObject("WScript.Shell")
batPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\wowooai Desktop.bat"
WshShell.Run Chr(34) & batPath & Chr(34), 0, False
Set WshShell = Nothing
"@ | Set-Content -Path $LauncherVbs -Encoding ASCII

# Create wowooai.cmd wrapper in env root so "wowooai" resolves to this
# instead of Scripts\wowooai.exe whose embedded Python path may be stale
# after conda-pack/unpack.
$wowooaiCmd = Join-Path $EnvRoot "wowooai.cmd"
@"
@"%~dp0python.exe" -u -m wowooai %*
"@ | Set-Content -Path $wowooaiCmd -Encoding ASCII

# Copy icon.ico to env root so NSIS can find it
$IconSrc = Join-Path $PackDir "assets\icon.ico"
if (Test-Path $IconSrc) {
  Copy-Item $IconSrc -Destination $EnvRoot -Force
  Write-Host "[build_win] Copied icon.ico to env root"
} else {
  Write-Host "[build_win] WARN: icon.ico not found at $IconSrc"
}

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

Write-Host "== Building NSIS installer =="

# Debug: Print EnvRoot directory contents
Write-Host "=== EnvRoot=$EnvRoot ==="
Write-Host "=== EnvRoot top files ==="
Get-ChildItem -LiteralPath $EnvRoot -Force | Select-Object -First 50 | ForEach-Object { Write-Host $_.FullName }

# Prioritize version from __version__.py to ensure accuracy
$Version = $CurrentVersion
if (-not $Version) {
  # Fallback: try to get version from packed env metadata
  try {
    $Version = (& (Join-Path $EnvRoot "python.exe") -c "from importlib.metadata import version; print(version('wowooai'))" 2>&1) -replace '\s+$', ''
    Write-Host "[build_win] Using version from packed env metadata: $Version"
  } catch {
    Write-Host "[build_win] version from packed env failed: $_"
  }
}
if (-not $Version) { $Version = "0.0.0"; Write-Host "[build_win] WARN: Using fallback version 0.0.0" }
Write-Host "[build_win] Version determined: $Version"
Write-Host "[build_win] wowooai_VERSION=$Version OUTPUT_EXE will be under $Dist"
$OutInstaller = Join-Path (Join-Path $RepoRoot $Dist) "wowooai-Setup-$Version.exe"
# Pass absolute paths to NSIS (keep backslashes).
$UnpackedFull = (Resolve-Path $EnvRoot).Path
$OutputExeNsi = [System.IO.Path]::GetFullPath($OutInstaller)
$nsiArgs = @(
  "/Dwowooai_VERSION=$Version",
  "/DOUTPUT_EXE=$OutputExeNsi",
  "/DUNPACKED=$UnpackedFull",
  $NsiPath
)

# Debug: Check if makensis is available
Write-Host "=== Checking makensis availability ==="
try {
  $makensisPath = (Get-Command makensis -ErrorAction Stop).Source
  Write-Host "[build_win] makensis found at: $makensisPath"
} catch {
  throw "makensis not found in PATH. Please install NSIS and ensure makensis.exe is in PATH."
}

Write-Host "[build_win] Running: makensis $($nsiArgs -join ' ')"
Write-Host "=== NSIS will compile from: $NsiPath ==="
Write-Host "=== NSIS unpacked source: $UnpackedFull ==="
Write-Host "=== NSIS output installer: $OutputExeNsi ==="
$nsisOutput = & makensis @nsiArgs 2>&1 | Out-String
Write-Host "=== NSIS Output Begin ==="
Write-Host $nsisOutput
Write-Host "=== NSIS Output End ==="
$makensisExit = $LASTEXITCODE
Write-Host "[build_win] makensis exit code: $makensisExit"
if ($makensisExit -ne 0) {
  Write-Host "ERROR: makensis compilation failed!"
  Write-Host "Check the NSIS output above for specific errors."
  throw "makensis failed with exit code $makensisExit"
}
if (-not (Test-Path $OutInstaller)) {
  throw "NSIS did not create installer: $OutInstaller"
}
Write-Host "== Built $OutInstaller =="

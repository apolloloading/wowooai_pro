#!/usr/bin/env bash
# One-click build: console -> conda-pack -> WowooAI.app -> DMG. Run from repo root.
# Requires: conda, node/npm (for console). Optional: icon.icns in assets/.
#
# Environment variables:
#   DIST            Output directory (default: dist)
#   EXTRAS          pip extras to install (default: desktop)
#                   Use 'full' to include local-inference packages.
#   CREATE_DMG      Set to 0 to skip DMG creation (default: 1)

set -e
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"
PACK_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST="${DIST:-dist}"
EXTRAS="${EXTRAS:-desktop}"
ARCHIVE="${DIST}/wowooai-env.tar.gz"
# DMG creation is enabled by default; set CREATE_DMG=0 to disable.
CREATE_DMG="${CREATE_DMG:-1}"
APP_NAME="WowooAI"
APP_DIR="${DIST}/${APP_NAME}.app"
if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  PYTHON="${REPO_ROOT}/.venv/bin/python"
elif [[ -n "${PYTHON_BIN}" && -x "${PYTHON_BIN}" ]]; then
  PYTHON="${PYTHON_BIN}"
else
  PYTHON="python3"
fi
echo "== Using Python: ${PYTHON} ($(${PYTHON} --version 2>&1)) =="

echo "== Building wheel (includes console frontend) =="
# Skip wheel_build if dist already has a wheel for current version
VERSION_FILE="${REPO_ROOT}/src/wowooai/__version__.py"
CURRENT_VERSION=""
if [[ -f "${VERSION_FILE}" ]]; then
  CURRENT_VERSION="$(
    sed -n 's/^__version__[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' \
      "${VERSION_FILE}" 2>/dev/null
  )"
fi
if [[ -n "${CURRENT_VERSION}" ]]; then
  shopt -s nullglob
  whls=("${REPO_ROOT}/dist/wowooai-${CURRENT_VERSION}-"*.whl)
  # A valid wheel MUST contain the compiled frontend (console/dist/index.html).
  # If that file is absent it means the wheel was built without running
  # wheel_build.sh (e.g. via plain `python -m build`) and the bundle will show
  # a white screen.  In that case we delete the stale wheel and rebuild.
  wheel_ok=0
  if [[ ${#whls[@]} -gt 0 ]]; then
    whl_path="${whls[0]}"
    if "${PYTHON}" -c "
import zipfile, sys
whl = sys.argv[1]
with zipfile.ZipFile(whl) as z:
    names = z.namelist()
has_frontend = any('wowooai/console/index.html' in n for n in names)
sys.exit(0 if has_frontend else 1)
" "$whl_path" 2>/dev/null; then
      echo "dist/ already has valid wheel for version ${CURRENT_VERSION} (frontend included), skipping."
      wheel_ok=1
    else
      echo "WARNING: existing wheel ${whl_path} is missing wowooai/console/index.html — deleting and rebuilding."
      rm -f "$whl_path"
    fi
  fi
  if [[ $wheel_ok -eq 0 ]]; then
    # Clean up any remaining old wheels to avoid confusion
    old_whls=("${REPO_ROOT}/dist/wowooai-"*.whl)
    if [[ ${#old_whls[@]} -gt 0 ]]; then
      echo "Removing old wheel files: ${old_whls[*]}"
      rm -f "${old_whls[@]}"
    fi
    bash scripts/wheel_build.sh
  fi
else
  bash scripts/wheel_build.sh
fi

echo "== Building conda-packed env =="
"${PYTHON}" "${PACK_DIR}/build_common.py" --output "$ARCHIVE" --format tar.gz \
  --extras "${EXTRAS}"

echo "== Building .app bundle =="
rm -rf "$APP_DIR"
mkdir -p "${APP_DIR}/Contents/MacOS"
mkdir -p "${APP_DIR}/Contents/Resources"

# Unpack conda env into Resources/env
mkdir -p "${APP_DIR}/Contents/Resources/env"
tar -xzf "$ARCHIVE" -C "${APP_DIR}/Contents/Resources/env" --strip-components=0

# Fix paths for portability (required or app will crash on launch)
if [[ -x "${APP_DIR}/Contents/Resources/env/bin/conda-unpack" ]]; then
  # Use absolute path to avoid issues with relative paths in subshells.
  # Use python3.10 directly (bin/python is a symlink; resolve it explicitly
  # to avoid "No such file or directory" on some macOS environments).
  ENV_PYTHON="$(cd "${APP_DIR}/Contents/Resources/env" && pwd)/bin/python3.10"
  (cd "${APP_DIR}/Contents/Resources/env" && "$ENV_PYTHON" ./bin/conda-unpack)
fi

# Hardlink the python3.10 binary as "WowooAI" so that when the launcher
# exec's it, macOS shows the Dock tooltip / process name as "WowooAI"
# instead of "python3.10". CPython resolves stdlib via PYTHONHOME (set in
# the launcher), so the binary name does not affect interpreter behaviour.
ENV_BIN_DIR="${APP_DIR}/Contents/Resources/env/bin"
if [[ -f "${ENV_BIN_DIR}/python3.10" && ! -e "${ENV_BIN_DIR}/${APP_NAME}" ]]; then
  ln "${ENV_BIN_DIR}/python3.10" "${ENV_BIN_DIR}/${APP_NAME}"
  echo "== Hardlinked ${ENV_BIN_DIR}/${APP_NAME} -> python3.10 =="
fi

# Patch agentscope _common.py: add model_rebuild() with typing namespace before
# model_json_schema() to fix PydanticUserError "not fully defined" on Python 3.10.
# This is a dependency-level fix that must be applied after every conda-pack.
COMMON_PY="${APP_DIR}/Contents/Resources/env/lib/python3.10/site-packages/agentscope/_utils/_common.py"
if [[ -f "$COMMON_PY" ]]; then
  "${PYTHON}" - "$COMMON_PY" << 'PATCHPY'
import sys, re
path = sys.argv[1]
src = open(path).read()
old = (
    '    base_model = create_model(\n'
    '        "_StructuredOutputDynamicClass",\n'
    '        __config__=ConfigDict(arbitrary_types_allowed=True),\n'
    '        **fields,\n'
    '    )\n'
    '    params_json_schema = base_model.model_json_schema()'
)
new = (
    '    base_model = create_model(\n'
    '        "_StructuredOutputDynamicClass",\n'
    '        __config__=ConfigDict(arbitrary_types_allowed=True),\n'
    '        **fields,\n'
    '    )\n'
    '    import typing as _typing\n'
    '    base_model.model_rebuild(\n'
    '        _types_namespace={\n'
    '            "Optional": _typing.Optional,\n'
    '            "Union": _typing.Union,\n'
    '            "List": _typing.List,\n'
    '            "Dict": _typing.Dict,\n'
    '            "Any": _typing.Any,\n'
    '            "Tuple": _typing.Tuple,\n'
    '            "Set": _typing.Set,\n'
    '        }\n'
    '    )\n'
    '    params_json_schema = base_model.model_json_schema()'
)
if old in src:
    open(path, 'w').write(src.replace(old, new))
    print("Patched agentscope _common.py successfully")
    # Remove stale pyc
    import os, glob
    for pyc in glob.glob(path.replace('.py', '.cpython-*.pyc').replace('_common', '__pycache__/_common')):
        os.remove(pyc)
else:
    print("WARNING: agentscope _common.py patch target not found - may already be patched or changed upstream")
PATCHPY
else
  echo "Warning: agentscope _common.py not found at $COMMON_PY"
fi

# -------------------------------------------------------------------
# Bundle Playwright browsers (Chromium + Chromium Headless Shell) so
# renliwo_browser / browser_use can run out-of-the-box without asking
# the user to `playwright install`.
#
# Source:
#   $PLAYWRIGHT_BROWSERS_DIR (set by the CI workflow after running
#   `playwright install chromium`). Typically points at
#   ~/Library/Caches/ms-playwright on macOS.
#
# Destination:
#   ${APP_DIR}/Contents/Resources/playwright-browsers/
#
# Why both chromium AND chromium_headless_shell:
#   Playwright >=1.49 default `headless=True` launches the standalone
#   `chrome-headless-shell` binary, which lives in
#   `chromium_headless_shell-<rev>/`, NOT in `chromium-<rev>/`. If only
#   `chromium-*` is bundled, the user-facing app must still download
#   ~150 MB on first browser-tool invocation and FAILS on offline Macs
#   with `BrowserType.launch: Executable doesn't exist`.
#   See packaging.md §11.
#
# Why we read browsers.json:
#   The host cache (~/Library/Caches/ms-playwright) accumulates old
#   revisions over time (e.g. chromium-1208 + chromium-1217). Bundling
#   all of them wastes ~330 MB per duplicate. The Python `playwright`
#   package pinned in this build has ONE required revision per browser;
#   we read it from the unpacked env's bundled `browsers.json` and copy
#   only that revision.
#
# Runtime:
#   The launcher exports PLAYWRIGHT_BROWSERS_PATH to this directory so
#   Playwright picks up the bundled binaries instead of downloading.
# -------------------------------------------------------------------
PW_BROWSERS_SRC="${PLAYWRIGHT_BROWSERS_DIR:-$HOME/Library/Caches/ms-playwright}"
PW_BROWSERS_DST="${APP_DIR}/Contents/Resources/playwright-browsers"
PW_BROWSERS_JSON="${APP_DIR}/Contents/Resources/env/lib/python3.10/site-packages/playwright/driver/package/browsers.json"

if [[ ! -f "$PW_BROWSERS_JSON" ]]; then
  echo "ERROR: cannot resolve required Playwright revisions:"
  echo "  $PW_BROWSERS_JSON not found."
  echo "  Was conda-pack of playwright skipped?"
  exit 1
fi

# Resolve the exact required revisions for chromium + chromium-headless-shell
# from the bundled playwright package. Output two whitespace-separated dirs:
#   chromium-<rev> chromium_headless_shell-<rev>
PW_DIRS_TO_COPY="$("${PYTHON}" - "$PW_BROWSERS_JSON" << 'PYEOF'
import json, sys
data = json.loads(open(sys.argv[1]).read())
wanted = {"chromium": None, "chromium-headless-shell": None}
for b in data.get("browsers", []):
    name = b.get("name")
    if name in wanted:
        wanted[name] = b.get("revision")
missing = [k for k, v in wanted.items() if not v]
if missing:
    sys.stderr.write(f"ERROR: revisions not found in browsers.json: {missing}\n")
    sys.exit(1)
# Disk dirs use underscore in cache: chromium-headless-shell -> chromium_headless_shell
print(f"chromium-{wanted['chromium']} "
      f"chromium_headless_shell-{wanted['chromium-headless-shell']}")
PYEOF
)" || exit 1

echo "== Required Playwright dirs: ${PW_DIRS_TO_COPY} =="

if [[ -d "$PW_BROWSERS_SRC" ]]; then
  echo "== Bundling Playwright browsers from ${PW_BROWSERS_SRC} =="
  mkdir -p "$PW_BROWSERS_DST"
  copied_any=0
  missing_dirs=()
  for d in $PW_DIRS_TO_COPY; do
    if [[ -d "$PW_BROWSERS_SRC/$d" ]]; then
      echo "  -> copying $d"
      cp -R "$PW_BROWSERS_SRC/$d" "$PW_BROWSERS_DST/"
      copied_any=1
    else
      missing_dirs+=("$d")
    fi
  done

  # Copy per-browser install markers (*.json) so playwright validates the cache.
  find "$PW_BROWSERS_SRC" -maxdepth 1 -name '*.json' -exec \
    cp {} "$PW_BROWSERS_DST/" \; 2>/dev/null || true

  if [[ ${#missing_dirs[@]} -gt 0 ]]; then
    echo "ERROR: required Playwright dirs missing in cache ${PW_BROWSERS_SRC}:"
    for d in "${missing_dirs[@]}"; do echo "    $d"; done
    echo "  Run \`playwright install chromium\` on this build host first,"
    echo "  or set PLAYWRIGHT_BROWSERS_DIR to a cache that contains them."
    echo "  Without these binaries the bundled .app will fail offline AND"
    echo "  silently download ~150 MB on first run online."
    exit 1
  fi

  # Final integrity check: each required dir must exist in the bundle and
  # contain a non-empty subtree.
  for d in $PW_DIRS_TO_COPY; do
    if [[ ! -d "$PW_BROWSERS_DST/$d" ]] || \
       [[ -z "$(ls -A "$PW_BROWSERS_DST/$d" 2>/dev/null)" ]]; then
      echo "ERROR: $PW_BROWSERS_DST/$d is missing or empty after copy."
      exit 1
    fi
  done

  PW_SIZE="$(du -sh "$PW_BROWSERS_DST" | cut -f1)"
  echo "== Bundled Playwright browsers: ${PW_SIZE} =="
else
  echo "ERROR: Playwright cache dir not found: ${PW_BROWSERS_SRC}"
  echo "  Run 'playwright install chromium' before this script,"
  echo "  or set PLAYWRIGHT_BROWSERS_DIR to an existing cache location."
  exit 1
fi

# Launcher: uses exec so Python *replaces* the shell process and becomes the
# CFBundleExecutable from macOS's perspective.
#
# WHY exec IS REQUIRED:
#   macOS sets activationPolicy=prohibited on any process that is NOT the
#   registered CFBundleExecutable.  A Python launched as a bash child process
#   gets policy=prohibited and can never show a window — the Dock icon bounces
#   then disappears.  With "exec", bash is replaced by Python before any GUI
#   code runs, so macOS gives it policy=regular and the window appears.
#
# WHY THIS IS NOW SAFE (unlike before):
#   Previously we relied on sys.executable to find bundle Resources/icon.icns.
#   That code has been fixed in desktop_cmd.py to use __file__ (the .py module
#   path) instead — so the path calculation is correct regardless of where
#   sys.executable is.
cat > "${APP_DIR}/Contents/MacOS/${APP_NAME}" << 'LAUNCHER'
#!/usr/bin/env bash
ENV_DIR="$(cd "$(dirname "$0")/../Resources/env" && pwd)"
PYTHON="$ENV_DIR/bin/python"
LOG="$HOME/.wowooai/desktop.log"

unset PYTHONPATH
export PYTHONHOME="$ENV_DIR"
export PYTHONNOUSERSITE=1
export WOWOOAI_DESKTOP_APP=1
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
export PATH="$ENV_DIR/bin:$PATH"

# Point Playwright at the bundled Chromium (if present) so renliwo_browser /
# browser_use work offline without triggering a runtime download.
PW_BUNDLED="$(cd "$(dirname "$0")/../Resources/playwright-browsers" 2>/dev/null && pwd)"
if [ -n "$PW_BUNDLED" ] && [ -d "$PW_BUNDLED" ]; then
  export PLAYWRIGHT_BROWSERS_PATH="$PW_BUNDLED"
fi

if [ -x "$PYTHON" ]; then
  CERT_FILE=$("$PYTHON" -c "import certifi; print(certifi.where())" 2>/dev/null)
  if [ -n "$CERT_FILE" ] && [ -f "$CERT_FILE" ]; then
    export SSL_CERT_FILE="$CERT_FILE"
    export REQUESTS_CA_BUNDLE="$CERT_FILE"
    export CURL_CA_BUNDLE="$CERT_FILE"
  fi
fi

cd "$HOME" || true
LOG_LEVEL="${WOWOOAI_LOG_LEVEL:-info}"
mkdir -p "$HOME/.wowooai"

if [ ! -x "$PYTHON" ]; then
  echo "ERROR: python not executable at $PYTHON" >> "$LOG"
  exit 1
fi

if [ ! -f "$HOME/.wowooai/config.json" ]; then
  "$PYTHON" -u -m wowooai init --defaults --accept-security >> "$LOG" 2>&1
fi

{ echo "=== $(date) WowooAI starting ==="
  echo "Python: $PYTHON"
  echo "LOG_LEVEL=$LOG_LEVEL"
  echo "SSL_CERT_FILE=${SSL_CERT_FILE:-not set}"
} >> "$LOG"

# exec replaces this shell with the interpreter so macOS sees it as the
# CFBundleExecutable — required for activationPolicy=regular (GUI windows).
# We exec a hardlink named "WowooAI" (same inode as python3.10) so the
# Dock tooltip / process name shows "WowooAI" instead of "python3.10".
# Falls back to $PYTHON if the hardlink is missing for any reason.
APP_BIN="$ENV_DIR/bin/WowooAI"
if [ -x "$APP_BIN" ]; then
  exec "$APP_BIN" -u -m wowooai desktop --log-level "$LOG_LEVEL" >> "$LOG" 2>&1
else
  exec "$PYTHON" -u -m wowooai desktop --log-level "$LOG_LEVEL" >> "$LOG" 2>&1
fi
LAUNCHER
chmod +x "${APP_DIR}/Contents/MacOS/${APP_NAME}"

# Icon: use pre-generated icon.icns
if [[ -f "${PACK_DIR}/assets/icon.icns" ]]; then
  echo "== Using pre-generated icon.icns =="
else
  echo "Warning: icon.icns not found at ${PACK_DIR}/assets/icon.icns"
  echo "Generate it first: bash scripts/pack/generate_icons.sh"
fi

# Info.plist (include icon key if icon.icns exists)
# Prioritize version from __version__.py to ensure accuracy
VERSION="${CURRENT_VERSION}"
if [[ -z "${VERSION}" ]]; then
  # Fallback: try to get version from packed env metadata
  VERSION="$("${APP_DIR}/Contents/Resources/env/bin/python" -c \
    "from importlib.metadata import version; print(version('wowooai'))" 2>/dev/null \
    || echo "0.0.0")"
  echo "Using version from packed env metadata: ${VERSION}"
else
  echo "Version determined from __version__.py: ${VERSION}"
fi
ICON_PLIST=""
if [[ -f "${PACK_DIR}/assets/icon.icns" ]]; then
  cp "${PACK_DIR}/assets/icon.icns" "${APP_DIR}/Contents/Resources/"
  ICON_PLIST="<key>CFBundleIconFile</key><string>icon.icns</string>
  "
fi
# Status bar (menu bar) icon — 36×36 px template image
if [[ -f "${PACK_DIR}/assets/icon_statusbar.png" ]]; then
  cp "${PACK_DIR}/assets/icon_statusbar.png" "${APP_DIR}/Contents/Resources/"
fi
cat > "${APP_DIR}/Contents/Info.plist" << INFOPLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" \
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key><string>${APP_NAME}</string>
  <key>CFBundleIdentifier</key><string>com.wowooai.desktop</string>
  <key>CFBundleName</key><string>${APP_NAME}</string>
  <key>CFBundleVersion</key><string>${VERSION}</string>
  <key>CFBundleShortVersionString</key><string>${VERSION}</string>
  ${ICON_PLIST}<key>NSHighResolutionCapable</key><true/>
  <key>LSMinimumSystemVersion</key><string>14.0</string>
  <key>NSDesktopFolderUsageDescription</key><string>WowooAI may access files in your Desktop folder if you use file-related features. You can choose Don'\''t Allow; the app will still run with limited file access.</string>
</dict>
</plist>
INFOPLIST

echo "== Built ${APP_DIR} =="

APP_SIZE="$(du -sh "${APP_DIR}" | cut -f1)"
echo "== App size: ${APP_SIZE} =="

# Create compressed DMG for distribution
if [[ "${CREATE_DMG}" != "0" ]]; then
  DMG_NAME="${DIST}/WowooAI-${VERSION}-macOS.dmg"
  DMG_TMP="${DIST}/WowooAI-${VERSION}-macOS-tmp.dmg"
  echo "== Creating compressed DMG: ${DMG_NAME} =="
  rm -f "${DMG_NAME}" "${DMG_TMP}"

  # Build a standard macOS installer-style DMG:
  #   WowooAI.app  +  Applications -> /Applications symlink
  # so Finder shows a drag-to-Applications window.
  #
  # Strategy: create a blank writable UDIF, mount it, copy app + symlink
  # inside, detach, then convert to compressed UDZO.
  # (Using -srcfolder with a symlink to /Applications is unreliable on
  # some macOS versions and can fail with "Operation not permitted".)
  #
  # Size: 2x app size + 256MB buffer. Playwright Chromium bundles
  # "Google Chrome for Testing.app" (deeply nested); hdiutil underestimates
  # HFS+ volume overhead for this tree — the 2x buffer prevents
  # "No space left on device" during ditto.
  APP_SIZE_MB="$(du -sm "${APP_DIR}" | awk '{print $1}')"
  DMG_SIZE_MB="$(( APP_SIZE_MB * 2 + 256 ))"
  echo "== DMG temp volume: ${DMG_SIZE_MB}MB (app: ${APP_SIZE_MB}MB) =="
  hdiutil create \
    -size "${DMG_SIZE_MB}m" \
    -fs HFS+ \
    -volname "WowooAI ${VERSION}" \
    -type UDIF \
    "${DMG_TMP}"

  # Mount and extract mount point via plist output (robust across locales)
  _ATTACH_PLIST=$(hdiutil attach "${DMG_TMP}" -nobrowse -plist 2>/dev/null)
  _MOUNT_PT=$(echo "$_ATTACH_PLIST" | python3 -c "
import sys, plistlib
pl = plistlib.loads(sys.stdin.buffer.read())
for e in pl.get('system-entities', []):
    if 'mount-point' in e:
        print(e['mount-point'])
        break
")
  echo "== Mounted at: ${_MOUNT_PT} =="

  ditto "${APP_DIR}" "${_MOUNT_PT}/${APP_NAME}.app"
  ln -s /Applications "${_MOUNT_PT}/Applications"

  hdiutil detach "${_MOUNT_PT}"
  hdiutil convert "${DMG_TMP}" \
    -format UDZO \
    -imagekey zlib-level=9 \
    -o "${DMG_NAME}"
  rm -f "${DMG_TMP}"
  DMG_SIZE="$(du -sh "${DMG_NAME}" | cut -f1)"
  echo "== Created ${DMG_NAME} (${DMG_SIZE}) =="
fi

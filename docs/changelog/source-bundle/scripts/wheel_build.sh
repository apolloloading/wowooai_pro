#!/usr/bin/env bash
# Build a full wheel package including the latest console frontend.
# Run from repo root: bash scripts/wheel_build.sh
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

CONSOLE_DIR="$REPO_ROOT/console"
CONSOLE_DEST="$REPO_ROOT/src/wowooai/console"

# Always use the project's own virtualenv first. This prevents a parent shell
# PATH from accidentally selecting another project's python3 during packaging.
if [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
  PYTHON="$REPO_ROOT/.venv/bin/python"
elif [[ -n "${PYTHON_BIN:-}" && -x "$PYTHON_BIN" ]]; then
  PYTHON="$PYTHON_BIN"
else
  PYTHON="python3"
fi

echo "[wheel_build] Using Python: $PYTHON ($($PYTHON --version 2>&1))"

echo "[wheel_build] Building console frontend..."
(cd "$CONSOLE_DIR" && npm ci)

# Backend port is dynamically allocated in desktop mode (cli/desktop_cmd.py
# uses _find_free_port). The frontend MUST use same-origin relative URLs
# (empty VITE_API_BASE_URL) so requests reach whatever port the backend
# actually bound to. Any leftover .env.local with VITE_API_BASE_URL=...
# would bake an absolute hard-coded URL into the bundle and break the
# packaged desktop app. See docs/changelog/packaging-macos.md §9.
ENV_LOCAL="$CONSOLE_DIR/.env.local"
ENV_LOCAL_BAK=""
if [[ -f "$ENV_LOCAL" ]]; then
  ENV_LOCAL_BAK="$ENV_LOCAL.wheelbuild.bak"
  echo "[wheel_build] Temporarily moving .env.local aside (avoids baking VITE_API_BASE_URL into bundle)..."
  mv "$ENV_LOCAL" "$ENV_LOCAL_BAK"
fi

# Restore .env.local even if the build fails.
restore_env_local() {
  if [[ -n "$ENV_LOCAL_BAK" && -f "$ENV_LOCAL_BAK" ]]; then
    mv "$ENV_LOCAL_BAK" "$ENV_LOCAL"
    echo "[wheel_build] Restored .env.local."
  fi
}
trap restore_env_local EXIT

# Force VITE_API_BASE_URL empty so the bundle uses same-origin relative URLs.
(cd "$CONSOLE_DIR" && VITE_API_BASE_URL="" npm run build)

echo "[wheel_build] Copying console/dist/* -> src/wowooai/console/..."
rm -rf "$CONSOLE_DEST"/*

mkdir -p "$CONSOLE_DEST"
cp -R "$CONSOLE_DIR/dist/"* "$CONSOLE_DEST/"

echo "[wheel_build] Building wheel + sdist..."
"$PYTHON" -m pip install --quiet build
rm -rf dist/*
"$PYTHON" -m build --outdir dist .

echo "[wheel_build] Done. Wheel(s) in: $REPO_ROOT/dist/"

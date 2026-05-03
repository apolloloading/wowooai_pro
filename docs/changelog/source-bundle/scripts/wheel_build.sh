#!/usr/bin/env bash
# Build a full wheel package including the latest console frontend.
# Run from repo root: bash scripts/wheel_build.sh
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

CONSOLE_DIR="$REPO_ROOT/console"
CONSOLE_DEST="$REPO_ROOT/src/wowooai/console"

# Prefer project .venv python (avoids picking up shell-activated envs that may
# lack pip, e.g. Hermes agent venv). Fall back to PYTHON_BIN env var, then python3.
if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  PYTHON="${REPO_ROOT}/.venv/bin/python"
elif [[ -n "${PYTHON_BIN}" && -x "${PYTHON_BIN}" ]]; then
  PYTHON="${PYTHON_BIN}"
else
  PYTHON="python3"
fi
echo "[wheel_build] Using Python: ${PYTHON} ($(${PYTHON} --version 2>&1))"

echo "[wheel_build] Building console frontend..."
(cd "$CONSOLE_DIR" && npm ci)
(cd "$CONSOLE_DIR" && npm run build)

echo "[wheel_build] Copying console/dist/* -> src/wowooai/console/..."
rm -rf "$CONSOLE_DEST"/*

mkdir -p "$CONSOLE_DEST"
cp -R "$CONSOLE_DIR/dist/"* "$CONSOLE_DEST/"

echo "[wheel_build] Building wheel + sdist..."
"${PYTHON}" -m pip install --quiet build
rm -rf dist/*
"${PYTHON}" -m build --outdir dist .

echo "[wheel_build] Done. Wheel(s) in: $REPO_ROOT/dist/"

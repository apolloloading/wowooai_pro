#!/usr/bin/env bash
# Fetch Node.js LTS + pre-install agent-browser into a portable directory.
#
# Usage:
#   bash scripts/pack/fetch_node.sh <dest_dir> [arch]
#
# Arguments:
#   dest_dir  Target directory; will contain ./bin/node, ./bin/npm, ./bin/npx,
#             plus a pre-installed `agent-browser@<pinned>` reachable via npx.
#   arch      Optional: arm64 (default on Apple Silicon) or x64.
#
# Pinned versions:
#   Node.js   22.14.0 (current LTS as of 2026-05)
#   agent-browser 0.27.0 (matches src/wowooai/agents/skills/agent_browser-zh/SKILL.md)
#
# Why bundle Node.js:
#   `agent_browser` skill calls `npx agent-browser@0.27.0 ...` via
#   execute_shell_command. Desktop users (especially Windows) typically don't
#   have Node.js on PATH, and we don't want first-run to require an internet
#   download for the CLI. Chrome for Testing (~250 MB) is downloaded on
#   demand by agent-browser itself and is NOT bundled here.

set -euo pipefail

DEST="${1:-}"
if [[ -z "$DEST" ]]; then
  echo "ERROR: dest_dir required"
  echo "Usage: $0 <dest_dir> [arch]"
  exit 1
fi

NODE_VERSION="22.14.0"
AGENT_BROWSER_VERSION="0.27.0"

ARCH="${2:-}"
if [[ -z "$ARCH" ]]; then
  case "$(uname -m)" in
    arm64|aarch64) ARCH="arm64" ;;
    x86_64) ARCH="x64" ;;
    *) echo "ERROR: unknown arch $(uname -m)"; exit 1 ;;
  esac
fi

case "$(uname -s)" in
  Darwin) PLATFORM="darwin" ;;
  Linux) PLATFORM="linux" ;;
  *) echo "ERROR: unsupported OS $(uname -s)"; exit 1 ;;
esac

TARBALL="node-v${NODE_VERSION}-${PLATFORM}-${ARCH}.tar.gz"
URL="https://nodejs.org/dist/v${NODE_VERSION}/${TARBALL}"

mkdir -p "$DEST"
TMP="$(mktemp -d)"
trap "rm -rf '$TMP'" EXIT

echo "== Fetching ${TARBALL} =="
curl -fL "$URL" -o "${TMP}/${TARBALL}"

echo "== Extracting to ${DEST} =="
tar -xzf "${TMP}/${TARBALL}" -C "${TMP}"
SRC_DIR="${TMP}/node-v${NODE_VERSION}-${PLATFORM}-${ARCH}"
# Copy contents into DEST (so DEST/bin/node exists, not DEST/node-v.../bin/node).
cp -R "${SRC_DIR}/." "${DEST}/"

# Pre-warm npx cache with agent-browser so first run does not hit the network.
# We install globally into the bundled Node prefix so `npx agent-browser@...`
# resolves locally.
echo "== Pre-installing agent-browser@${AGENT_BROWSER_VERSION} =="
"${DEST}/bin/npm" install -g \
  --prefix "${DEST}" \
  "agent-browser@${AGENT_BROWSER_VERSION}" \
  >/dev/null 2>&1 || {
    echo "WARNING: pre-install agent-browser failed; first run will hit network"
  }

echo "== Bundled Node.js v${NODE_VERSION} (${PLATFORM}-${ARCH}) at ${DEST} =="
ls -la "${DEST}/bin/" | head -20

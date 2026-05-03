# -*- coding: utf-8 -*-
"""#1 【基本盘】点击每一个菜单 — API smoke.

Tier 1: no LLM required. Verifies every backend route the console UI hits
returns 2xx and the SPA shell loads.
"""
from __future__ import annotations

import httpx
import pytest

# All paths the console UI calls on initial menu navigation.
# Each entry: (path, expected status set, optional content check)
SMOKE_GETS = [
    ("/api/version", {200}),
    ("/api/models/", {200}),
    ("/api/skills", {200}),
    ("/api/cron/jobs", {200}),
    ("/api/agents", {200}),
    ("/api/tools", {200}),
    ("/api/mcp/", {200}),
    ("/api/chats", {200}),
    ("/api/config/channels", {200}),
    ("/api/config/security/tool-guard", {200}),
    ("/api/config/security/file-guard", {200}),
    ("/api/workspace/files", {200}),
    ("/api/workspace/memory", {200}),
    ("/api/settings/language", {200}),
    ("/api/plugins", {200}),
    ("/api/token-usage", {200, 422}),  # may need query params; 422 still proves route is wired
    ("/api/agent-stats", {200, 422}),
]


@pytest.mark.e2e
@pytest.mark.parametrize("path,allowed", SMOKE_GETS)
def test_api_get_returns_ok(sync_client: httpx.Client, path: str, allowed: set[int]) -> None:
    """Every menu's primary GET endpoint is reachable and returns expected status."""
    r = sync_client.get(path)
    assert r.status_code in allowed, (
        f"GET {path} -> {r.status_code}, body: {r.text[:300]}"
    )


@pytest.mark.e2e
def test_console_html_loads(sync_client: httpx.Client) -> None:
    """Console SPA shell renders (not blank, not 5xx)."""
    r = sync_client.get("/console/")
    assert r.status_code == 200
    assert "text/html" in r.headers.get("content-type", "").lower()
    body = r.text.lower()
    assert "<!doctype html>" in body or "<html" in body


@pytest.mark.e2e
def test_logs_have_no_traceback(server_log_lines: list[str]) -> None:
    """No Python tracebacks accumulated during smoke probes.

    Note: when running against an external server (WOWOOAI_E2E_BASE_URL), the
    log buffer is empty and this test trivially passes.
    """
    if not server_log_lines:
        pytest.skip("No subprocess log buffer (external server mode)")
    joined = "".join(server_log_lines)
    # Filter known benign noise here if needed:
    benign = ("Nacos SDK is not available",)
    bad_lines: list[str] = []
    for line in joined.splitlines():
        if "Traceback" in line or " ERROR " in line or " CRITICAL " in line:
            if any(b in line for b in benign):
                continue
            bad_lines.append(line)
    assert not bad_lines, "Unexpected errors in server log:\n" + "\n".join(bad_lines[:30])

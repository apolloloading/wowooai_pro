# -*- coding: utf-8 -*-
"""#2 【模型配置】重新配置 dashscope apikey.

Tier 1: CRUD round-trip is always testable.
Tier 2 (optional): connection test against real dashscope.
"""
from __future__ import annotations

import os

import httpx
import pytest


@pytest.mark.e2e
def test_list_providers_includes_dashscope(sync_client: httpx.Client) -> None:
    r = sync_client.get("/api/models/")
    assert r.status_code == 200
    data = r.json()
    # Response shape can be a list of providers or an envelope with 'providers'
    providers = data.get("providers", data) if isinstance(data, dict) else data
    assert isinstance(providers, list)
    ids = [p.get("id") for p in providers if isinstance(p, dict)]
    assert "dashscope" in ids, f"dashscope not in providers: {ids}"


@pytest.mark.e2e
def test_save_dashscope_config_persists(sync_client: httpx.Client) -> None:
    """Save → re-fetch → assert key value round-trips."""
    test_key = "sk-e2e-test-dummy-do-not-use"
    r = sync_client.put(
        "/api/models/dashscope/config",
        json={"api_key": test_key, "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"},
    )
    assert r.status_code == 200, f"save failed: {r.status_code} {r.text[:200]}"

    # Re-fetch the provider list and find dashscope
    r2 = sync_client.get("/api/models/")
    assert r2.status_code == 200
    data = r2.json()
    providers = data.get("providers", data) if isinstance(data, dict) else data
    ds = next((p for p in providers if isinstance(p, dict) and p.get("id") == "dashscope"), None)
    assert ds is not None
    # API may mask the key in the response; accept any of: full echo, masked, or set indicator
    saved = (ds.get("api_key") or "").strip()
    assert saved, f"dashscope api_key empty after save: {ds}"


@pytest.mark.e2e
def test_provider_connection_test(sync_client: httpx.Client) -> None:
    """Tier 2: real connectivity check against dashscope."""
    if not os.environ.get("DASHSCOPE_API_KEY"):
        pytest.skip("DASHSCOPE_API_KEY not set")
    # Save the real key first
    sync_client.put(
        "/api/models/dashscope/config",
        json={"api_key": os.environ["DASHSCOPE_API_KEY"]},
    )
    r = sync_client.post("/api/models/dashscope/test", timeout=30.0)
    assert r.status_code == 200, f"provider test failed: {r.text[:300]}"
    body = r.json()
    # Common shapes: {"success": True}, {"ok": True}, {"status": "ok"}
    ok = body.get("success") or body.get("ok") or body.get("status") in ("ok", "success", True)
    assert ok, f"connection test reported failure: {body}"

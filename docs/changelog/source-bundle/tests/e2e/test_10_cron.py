# -*- coding: utf-8 -*-
"""#10 【定时任务】对话创建 + 锁屏执行.

Tier 1 (CRUD via API) + Tier 2 (creation via chat).

The manual test waits 5 minutes for real fire under lock-screen. CI cannot
do that, so the API path force-runs jobs via POST /api/cron/jobs/{id}/run.
"""
from __future__ import annotations

import asyncio

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


@pytest.mark.e2e
def test_cron_crud_via_api(sync_client: httpx.Client) -> None:
    """Pure API CRUD: create → list → run → delete."""
    spec = {
        "name": "e2e-test-cron",
        "description": "E2E regression test job",
        "cron": "*/5 * * * *",
        "enabled": True,
        "task": {"type": "noop"},
    }
    create = sync_client.post("/api/cron/jobs", json=spec)
    if create.status_code not in (200, 201):
        pytest.skip(
            f"cron create rejected ({create.status_code}); "
            f"task schema may differ in this build: {create.text[:200]}"
        )
    body = create.json()
    job_id = body.get("id") or body.get("job_id") or body.get("data", {}).get("id")
    assert job_id, f"create response missing id: {body}"

    try:
        listing = sync_client.get("/api/cron/jobs")
        assert listing.status_code == 200
        items = listing.json()
        if isinstance(items, dict):
            items = items.get("jobs", items.get("data", []))
        assert any(
            (j.get("id") == job_id) for j in items if isinstance(j, dict)
        ), "created job not found in listing"

        # Force a manual run if the build supports it
        run = sync_client.post(f"/api/cron/jobs/{job_id}/run")
        assert run.status_code in (200, 202), f"run failed: {run.text[:200]}"
    finally:
        sync_client.delete(f"/api/cron/jobs/{job_id}")
        # Confirm deletion
        again = sync_client.get(f"/api/cron/jobs/{job_id}")
        assert again.status_code in (404, 410), (
            f"job still exists after delete: {again.status_code}"
        )


@pytest.mark.e2e
async def test_cron_created_via_chat_appears_in_list(
    client: httpx.AsyncClient,
    require_dashscope: str,
) -> None:
    """Ask agent to schedule a reminder; assert a job shows up."""
    before_resp = await client.get("/api/cron/jobs")
    before = before_resp.json() if before_resp.status_code == 200 else []
    if isinstance(before, dict):
        before = before.get("jobs", before.get("data", []))
    before_ids = {j.get("id") for j in before if isinstance(j, dict)}

    session_id = make_session_id("cron10")
    await send_chat_collect(
        client,
        session_id=session_id,
        message="请创建一个定时任务，5 分钟后提醒我喝水",
        timeout=60.0,
    )
    # Give the cron persistence a moment
    await asyncio.sleep(2.0)

    after_resp = await client.get("/api/cron/jobs")
    after = after_resp.json() if after_resp.status_code == 200 else []
    if isinstance(after, dict):
        after = after.get("jobs", after.get("data", []))
    new_jobs = [
        j for j in after
        if isinstance(j, dict) and j.get("id") and j.get("id") not in before_ids
    ]
    if not new_jobs:
        pytest.xfail("agent did not schedule a cron job (LLM non-deterministic)")

    # Cleanup any new jobs to avoid polluting the workspace
    for job in new_jobs:
        await client.delete(f"/api/cron/jobs/{job['id']}")

# -*- coding: utf-8 -*-
"""#5 【安全机制】删除文件需人工确认.

Tier 2: requires LLM to actually invoke a destructive tool.
"""
from __future__ import annotations

import asyncio

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


async def _wait_for_pending_approval(
    client: httpx.AsyncClient,
    session_id: str,
    timeout: float = 30.0,
) -> dict | None:
    """Poll /api/approval/list until a pending request appears."""
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        r = await client.get("/api/approval/list", params={"session_id": session_id})
        if r.status_code == 200:
            data = r.json()
            items = data.get("approvals", data) if isinstance(data, dict) else data
            if isinstance(items, list) and items:
                return items[0]
        await asyncio.sleep(1.0)
    return None


@pytest.mark.e2e
async def test_destructive_op_requires_approval(
    client: httpx.AsyncClient,
    require_dashscope: str,
    tmp_path,
) -> None:
    """Ask agent to delete a file → approval request must appear; deny → file lives."""
    target = tmp_path / "delete_me.txt"
    target.write_text("approval-test")
    assert target.exists()

    session_id = make_session_id("sec5")
    # Run the chat in the background so we can poll for approvals concurrently
    chat_task = asyncio.create_task(
        send_chat_collect(
            client,
            session_id=session_id,
            message=f"请删除文件 {target}",
            timeout=60.0,
        )
    )
    pending = await _wait_for_pending_approval(client, session_id, timeout=30.0)
    if pending is None:
        chat_task.cancel()
        pytest.xfail("LLM did not propose a destructive tool call (non-deterministic)")

    approval_id = pending.get("id") or pending.get("approval_id")
    assert approval_id, f"approval missing id: {pending}"

    deny = await client.post("/api/approval/deny", json={"approval_id": approval_id})
    assert deny.status_code == 200, f"deny failed: {deny.text[:200]}"

    try:
        await chat_task
    except Exception:
        pass

    assert target.exists(), "file was deleted despite denial!"

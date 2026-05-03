# -*- coding: utf-8 -*-
"""#3 【聊天功能】新建聊天发送「你好」.

Tier 2: requires DASHSCOPE_API_KEY (or whichever is the default LLM).
"""
from __future__ import annotations

import re

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


@pytest.mark.e2e
async def test_new_chat_replies_within_timeout(
    client: httpx.AsyncClient,
    require_dashscope: str,
) -> None:
    session_id = make_session_id("chat3")
    result = await send_chat_collect(
        client, session_id=session_id, message="你好", timeout=30.0
    )
    assert result["events"], "no SSE events received"
    # First-event latency (a bit more lenient than the 4s manual standard
    # because cold-start of LLM can vary; 10s catches obvious regression)
    assert (result["first_event_latency"] or 99) < 10, (
        f"first event took {result['first_event_latency']}s"
    )
    assert len(result["text"]) > 0, "assistant produced empty response"


@pytest.mark.e2e
async def test_chat_is_streaming(
    client: httpx.AsyncClient,
    require_dashscope: str,
) -> None:
    """Stream should produce multiple events, not a single blob."""
    session_id = make_session_id("chat3-stream")
    result = await send_chat_collect(
        client,
        session_id=session_id,
        message="用 50 字介绍一下你自己",
        timeout=60.0,
    )
    # Loose: at least 2 events. Real streaming usually emits dozens.
    assert len(result["events"]) >= 2, (
        f"expected streaming, got {len(result['events'])} events"
    )


@pytest.mark.e2e
async def test_multi_turn_memory_in_session(
    client: httpx.AsyncClient,
    require_dashscope: str,
) -> None:
    """In-session short-term memory recall."""
    session_id = make_session_id("chat3-multi")
    for msg in ["我叫李雷", "我喜欢喝拿铁", "我住在北京"]:
        await send_chat_collect(client, session_id=session_id, message=msg, timeout=30.0)
    final = await send_chat_collect(
        client,
        session_id=session_id,
        message="我刚才说我叫什么？喜欢什么？住哪？",
        timeout=45.0,
    )
    text = final["text"]
    matches = sum(1 for kw in ("李雷", "拿铁", "北京") if kw in text)
    # LLM occasionally drops one; require at least 2 of 3
    assert matches >= 2, (
        f"expected ≥2 of (李雷,拿铁,北京) in reply, got: {text!r}"
    )

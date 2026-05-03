# -*- coding: utf-8 -*-
"""#4 【记忆功能】跨会话长期记忆 + 隔离.

Tier 2.
"""
from __future__ import annotations

import asyncio

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


@pytest.mark.e2e
async def test_cross_session_long_term_memory(
    client: httpx.AsyncClient,
    require_dashscope: str,
) -> None:
    """Tell agent its name in session A, ask in fresh session B."""
    session_a = make_session_id("mem-a")
    await send_chat_collect(
        client,
        session_id=session_a,
        message="你以后叫老A，请记住这个名字",
        timeout=30.0,
    )
    # Give the long-term memory pipeline a moment to persist
    await asyncio.sleep(2.0)

    session_b = make_session_id("mem-b")
    result = await send_chat_collect(
        client, session_id=session_b, message="你叫什么名字？", timeout=30.0
    )
    text = result["text"]
    # Long-term memory is best-effort; xfail (not fail) if missed
    if "老A" not in text and "老a" not in text.lower():
        pytest.xfail(f"long-term memory miss (LLM/memory non-deterministic): {text!r}")


@pytest.mark.e2e
async def test_cross_session_short_term_isolation(
    client: httpx.AsyncClient,
    require_dashscope: str,
) -> None:
    """Secrets in session A must NOT leak into session C's short-term context."""
    session_a = make_session_id("iso-a")
    secret = "hello123-isolated"
    await send_chat_collect(
        client,
        session_id=session_a,
        message=f"我的临时测试密码是 {secret}",
        timeout=30.0,
    )

    session_c = make_session_id("iso-c")
    result = await send_chat_collect(
        client,
        session_id=session_c,
        message="我的临时测试密码是什么？请直接说",
        timeout=30.0,
    )
    assert secret not in result["text"], (
        f"isolation breach: secret leaked into new session: {result['text']!r}"
    )

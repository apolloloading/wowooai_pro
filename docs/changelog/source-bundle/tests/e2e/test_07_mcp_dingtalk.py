# -*- coding: utf-8 -*-
"""#7 【MCP】钉钉创建会议.

Tier 3: requires DingTalk MCP server configured + LLM.
Verifies the API/tool path; actual DingTalk side effect is human-verified
(see manual checklist).
"""
from __future__ import annotations

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


@pytest.mark.e2e
async def test_dingtalk_meeting_via_mcp(
    client: httpx.AsyncClient,
    require_dashscope: str,
    require_tier3: None,
) -> None:
    """Ask agent to create a meeting; assert MCP tool call is reported."""
    # Sanity: MCP route is reachable
    r = await client.get("/api/mcp/")
    assert r.status_code == 200

    session_id = make_session_id("mcp7")
    result = await send_chat_collect(
        client,
        session_id=session_id,
        message=(
            "帮我预定一个今天晚上 22:00 到 23:00 的会议，"
            "邀请测试员甲、测试员乙参加，最好预定一个测试会议室，"
            "会议名称叫『回归测试』"
        ),
        timeout=120.0,
    )
    text = result["text"]
    # The agent's text typically reflects the action (success or failure msg)
    assert "回归测试" in text or "会议" in text, (
        f"agent did not address meeting request: {text[:300]!r}"
    )

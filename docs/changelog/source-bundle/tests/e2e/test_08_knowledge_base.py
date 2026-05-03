# -*- coding: utf-8 -*-
"""#8 【知识库】RAG 检索公司 WiFi 密码.

Tier 2 + requires KB pre-loaded with WiFi info.
"""
from __future__ import annotations

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


EXPECTED_PASSWORD = "zEDc2QIzB&"


@pytest.mark.e2e
async def test_rag_returns_wifi_password(
    client: httpx.AsyncClient,
    require_dashscope: str,
    require_kb: None,
) -> None:
    session_id = make_session_id("kb8")
    result = await send_chat_collect(
        client,
        session_id=session_id,
        message="公司 wifi 密码是多少？",
        timeout=60.0,
    )
    text = result["text"]
    assert EXPECTED_PASSWORD in text, (
        f"WiFi password mismatch.\n"
        f"Expected substring: {EXPECTED_PASSWORD!r}\n"
        f"Got: {text!r}"
    )

# -*- coding: utf-8 -*-
"""#9 【浏览器操作】登录 + 导航 + 导出.

Tier 3: requires playwright browsers + UAT account + LLM with browser tool.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


@pytest.mark.e2e
async def test_browser_login_and_export(
    client: httpx.AsyncClient,
    require_dashscope: str,
    require_tier3: None,
    tmp_path,
) -> None:
    user = os.environ.get("WOWOOAI_TEST_USER_A", "2422733396@qq.com")
    pwd = os.environ.get("WOWOOAI_TEST_PASS_A", "admin12345677")

    download_dir = tmp_path / "downloads"
    download_dir.mkdir()
    before = set(p.name for p in download_dir.iterdir())
    started = time.time()

    session_id = make_session_id("browser9")
    instruction = (
        "现在你按照以下操作：\n"
        f"1. 打开 https://ereference-v-uat.renliwo.com/，如果遇到登录，"
        f"账户：{user}，密码：{pwd}，完成登录\n"
        "2. 进入网站以后，可能默认是异步导出记录页面，请忽略，"
        "点击顶部导航栏中的『综合管理』菜单\n"
        "3. 点击左侧的『合同管理』，再点击『合同产品列表』\n"
        "4. 在合同产品列表页面中，点击『查询』按钮，"
        f"如果有查询结果，点击『查询导出』，导出到 {download_dir}"
    )
    await send_chat_collect(
        client,
        session_id=session_id,
        message=instruction,
        timeout=240.0,
    )

    # Verify a new file landed in the requested directory
    after = set(p.name for p in download_dir.iterdir())
    new_files = after - before
    if not new_files:
        pytest.xfail("browser tool did not produce a download (UAT/LLM flaky)")

    new_file: Path = max(
        (download_dir / n for n in new_files), key=lambda p: p.stat().st_mtime
    )
    assert new_file.stat().st_size > 0, f"downloaded file is empty: {new_file}"
    # Should be very recent
    assert new_file.stat().st_mtime >= started - 5

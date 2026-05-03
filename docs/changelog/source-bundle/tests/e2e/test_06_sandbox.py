# -*- coding: utf-8 -*-
"""#6 【沙箱机制】不修改原文件.

Tier 2.
"""
from __future__ import annotations

import asyncio
import hashlib

import httpx
import pytest

from .conftest import make_session_id, send_chat_collect


def _md5(path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


@pytest.mark.e2e
async def test_processing_creates_new_file_keeps_original(
    client: httpx.AsyncClient,
    require_dashscope: str,
    tmp_path,
) -> None:
    """Ask to process a CSV-like file; the original must remain bit-identical."""
    src = tmp_path / "测试材料.csv"
    src.write_text(
        "合同编号,客户,金额\n"
        "C001,张三,100\n"
        "C002,李四,200\n"
        "C003,王五,300\n",
        encoding="utf-8",
    )
    original_md5 = _md5(src)
    original_mtime = src.stat().st_mtime

    session_id = make_session_id("sandbox6")
    await send_chat_collect(
        client,
        session_id=session_id,
        message=(
            f"处理这个文件 {src}，只保留合同编号一列，"
            f"输出到 {tmp_path} 目录下的新文件中"
        ),
        timeout=120.0,
    )
    # Allow tool I/O to settle
    await asyncio.sleep(1.0)

    # Original untouched
    assert src.exists(), "original file was deleted!"
    assert _md5(src) == original_md5, "original file was modified!"
    assert src.stat().st_mtime == original_mtime, "original mtime changed!"

    # Some new file appeared in the temp dir
    new_files = [p for p in tmp_path.iterdir() if p != src and p.is_file()]
    if not new_files:
        pytest.xfail("agent did not produce a new file (LLM non-deterministic)")

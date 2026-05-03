# -*- coding: utf-8 -*-
"""E2E test fixtures and helpers.

Boots a real `wowooai app` subprocess once per session in an isolated HOME,
provides HTTP clients, SSE chat helpers, and skip fixtures for tier 2/3 tests.

Set WOWOOAI_E2E_BASE_URL=http://127.0.0.1:8088 to point at an already-running
server instead of booting one (much faster during local development).
"""
# pylint:disable=consider-using-with
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Generator, Iterator
from pathlib import Path
from typing import Any

import httpx
import pytest


# =============================================================================
# Subprocess helpers
# =============================================================================


def _find_free_port(host: str = "127.0.0.1") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def _tee_stream(stream, buffer: list[str]) -> None:
    try:
        for line in iter(stream.readline, ""):
            buffer.append(line)
            print(line, end="", flush=True)
    finally:
        stream.close()


# =============================================================================
# Server fixture (session scope)
# =============================================================================


@pytest.fixture(scope="session")
def wowooai_server() -> Generator[str, None, None]:
    """Start (or reuse) a wowooai server, yield base URL like http://127.0.0.1:1234.

    If WOWOOAI_E2E_BASE_URL is set, skip the subprocess and use that URL.
    Otherwise spawn `python -m wowooai app` in an isolated HOME and tear it
    down at the end of the session.
    """
    external = os.environ.get("WOWOOAI_E2E_BASE_URL")
    if external:
        # Verify it's actually up before yielding
        with httpx.Client(timeout=5.0, trust_env=False) as c:
            try:
                r = c.get(f"{external.rstrip('/')}/api/version")
                if r.status_code != 200:
                    pytest.skip(f"WOWOOAI_E2E_BASE_URL not reachable: {external}")
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                pytest.skip(f"WOWOOAI_E2E_BASE_URL not reachable: {external}: {exc}")
        yield external.rstrip("/")
        return

    host = "127.0.0.1"
    port = _find_free_port(host)
    home_dir = tempfile.mkdtemp(prefix="wowooai_e2e_home_")

    env = os.environ.copy()
    env["HOME"] = home_dir
    env["WOWOOAI_HOME"] = str(Path(home_dir) / ".wowooai")
    Path(env["WOWOOAI_HOME"]).mkdir(parents=True, exist_ok=True)
    # Don't carry sensitive keys we don't want unless explicitly preserved
    env.setdefault("WOWOOAI_LOG_LEVEL", "info")

    log_lines: list[str] = []
    process = subprocess.Popen(
        [
            sys.executable, "-m", "wowooai", "app",
            "--host", host, "--port", str(port),
            "--log-level", "info",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )
    assert process.stdout is not None
    log_thread = threading.Thread(
        target=_tee_stream,
        args=(process.stdout, log_lines),
        daemon=True,
    )
    log_thread.start()

    base_url = f"http://{host}:{port}"
    try:
        max_wait = 90
        start = time.time()
        ready = False
        last_error = None
        with httpx.Client(timeout=5.0, trust_env=False) as c:
            while time.time() - start < max_wait:
                if process.poll() is not None:
                    raise AssertionError(
                        f"wowooai exited early code={process.returncode}.\n"
                        f"Logs:\n{''.join(log_lines)[-4000:]}"
                    )
                try:
                    r = c.get(f"{base_url}/api/version")
                    if r.status_code == 200:
                        ready = True
                        break
                except (httpx.ConnectError, httpx.TimeoutException) as e:
                    last_error = str(e)
                    time.sleep(1.0)
        if not ready:
            raise AssertionError(
                f"wowooai did not become ready in {max_wait}s. "
                f"Last error: {last_error}\n"
                f"Logs:\n{''.join(log_lines)[-4000:]}"
            )

        # Stash the log buffer on the fixture for tests that want it
        wowooai_server.log_lines = log_lines  # type: ignore[attr-defined]
        yield base_url
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        log_thread.join(timeout=2)
        shutil.rmtree(home_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def server_log_lines(wowooai_server) -> list[str]:
    """Return the live tail of subprocess output (empty when external URL)."""
    return getattr(wowooai_server.__class__, "log_lines", []) or getattr(
        # The real attribute lives on the fixture function object
        sys.modules[__name__].wowooai_server, "log_lines", []
    )


# =============================================================================
# HTTP client fixtures
# =============================================================================


@pytest.fixture(scope="session")
def base_url(wowooai_server: str) -> str:
    return wowooai_server


@pytest.fixture(scope="session")
def sync_client(base_url: str) -> Iterator[httpx.Client]:
    with httpx.Client(base_url=base_url, timeout=30.0, trust_env=False) as c:
        yield c


@pytest.fixture()
async def client(base_url: str) -> Any:
    async with httpx.AsyncClient(
        base_url=base_url,
        timeout=60.0,
        trust_env=False,
    ) as c:
        yield c


# =============================================================================
# Tier skip fixtures
# =============================================================================


@pytest.fixture(scope="session")
def require_dashscope() -> str:
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        pytest.skip("DASHSCOPE_API_KEY not set; skipping Tier 2 LLM test")
    return key


@pytest.fixture(scope="session")
def require_tier3() -> None:
    if not os.environ.get("WOWOOAI_E2E_TIER3"):
        pytest.skip("WOWOOAI_E2E_TIER3 not set; skipping Tier 3 external test")


@pytest.fixture(scope="session")
def require_kb() -> None:
    if not os.environ.get("WOWOOAI_E2E_KB"):
        pytest.skip("WOWOOAI_E2E_KB not set; skipping knowledge base test")


# =============================================================================
# Chat helpers
# =============================================================================


def make_session_id(prefix: str = "e2e") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


async def send_chat_collect(
    client: httpx.AsyncClient,
    *,
    session_id: str,
    message: str,
    user_id: str = "e2e-user",
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Send a chat message and collect the full SSE event stream.

    Returns dict:
      - text: concatenated assistant text (best-effort across event shapes)
      - events: list of parsed JSON event payloads
      - first_event_latency: seconds until first event arrived
      - total_duration: seconds for the whole stream
    """
    payload = {
        "channel": "console",
        "user_id": user_id,
        "session_id": session_id,
        "input": [
            {"content": [{"type": "text", "text": message}]},
        ],
    }
    events: list[dict[str, Any]] = []
    text_parts: list[str] = []
    started = time.time()
    first_event_latency: float | None = None

    async with client.stream(
        "POST",
        "/api/console/chat",
        json=payload,
        timeout=timeout,
    ) as response:
        response.raise_for_status()
        async for raw_line in response.aiter_lines():
            if not raw_line:
                continue
            if raw_line.startswith(":"):  # SSE comment
                continue
            if not raw_line.startswith("data:"):
                continue
            data_str = raw_line[len("data:"):].strip()
            if not data_str or data_str == "[DONE]":
                continue
            try:
                event = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            if first_event_latency is None:
                first_event_latency = time.time() - started
            events.append(event)
            text_parts.append(_extract_text(event))

    return {
        "text": "".join(text_parts),
        "events": events,
        "first_event_latency": first_event_latency,
        "total_duration": time.time() - started,
    }


def _extract_text(event: dict[str, Any]) -> str:
    """Best-effort extraction of assistant-visible text from an event."""
    # agentscope_runtime emits events with various shapes. Cover common ones.
    if not isinstance(event, dict):
        return ""
    # Direct delta
    delta = event.get("delta")
    if isinstance(delta, str):
        return delta
    if isinstance(delta, dict):
        for k in ("text", "content"):
            v = delta.get(k)
            if isinstance(v, str):
                return v
    # message.content[].text style
    msg = event.get("message") or event.get("response") or event
    if isinstance(msg, dict):
        content = msg.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            out: list[str] = []
            for part in content:
                if isinstance(part, dict):
                    t = part.get("text")
                    if isinstance(t, str):
                        out.append(t)
            if out:
                return "".join(out)
        # Plain text field
        for k in ("text", "output_text"):
            v = msg.get(k)
            if isinstance(v, str):
                return v
    return ""

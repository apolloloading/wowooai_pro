# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import os
import threading
import time

import click
import uvicorn

from ..constant import LOG_LEVEL_ENV
from ..config.utils import write_last_api
from ..utils.logging import setup_logger, SuppressPathAccessLogFilter


def _start_parent_watchdog() -> None:
    raw = os.environ.get("WOWOOAI_PARENT_PID")
    if not raw:
        return
    try:
        expected_ppid = int(raw)
    except ValueError:
        return
    if expected_ppid <= 1:
        return

    log = logging.getLogger(__name__)

    def _watch() -> None:
        while True:
            time.sleep(1.0)
            try:
                current_ppid = os.getppid()
            except OSError:
                current_ppid = 1
            if current_ppid != expected_ppid:
                log.warning(
                    "Parent process (pid=%d) is gone (current ppid=%d); "
                    "exiting to avoid becoming an orphan.",
                    expected_ppid,
                    current_ppid,
                )
                os._exit(0)

    threading.Thread(
        target=_watch,
        name="parent-watchdog",
        daemon=True,
    ).start()


@click.command("app")
@click.option(
    "--host",
    default="127.0.0.1",
    show_default=True,
    help="Bind host",
)
@click.option(
    "--port",
    default=8088,
    type=int,
    show_default=True,
    help="Bind port",
)
@click.option("--reload", is_flag=True, help="Enable auto-reload (dev only)")
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(
        ["critical", "error", "warning", "info", "debug", "trace"],
        case_sensitive=False,
    ),
    show_default=True,
    help="Log level",
)
@click.option(
    "--hide-access-paths",
    multiple=True,
    default=("/console/push-messages",),
    show_default=True,
    help="Path substrings to hide from uvicorn access log (repeatable).",
)
@click.option(
    "--workers",
    type=int,
    default=None,
    help="[DEPRECATED] Number of worker processes. "
    "This option is deprecated and will be removed in a future version. "
    "wowooai always uses 1 worker.",
)
def app_cmd(
    host: str,
    port: int,
    reload: bool,
    workers: int,  # pylint: disable=unused-argument
    log_level: str,
    hide_access_paths: tuple[str, ...],
) -> None:
    """Run wowooai FastAPI app."""
    # Handle deprecated --workers parameter
    if workers is not None:
        click.echo(
            "⚠️  WARNING: --workers option is deprecated and will be removed "
            "in a future version.",
            err=True,
        )
        click.echo(
            "   wowooai always uses 1 worker for stability. "
            "Your specified value will be ignored.",
            err=True,
        )
        click.echo(err=True)

    # Persist last used host/port for other terminals
    if host == "0.0.0.0":
        write_last_api("127.0.0.1", port)
    else:
        write_last_api(host, port)
    os.environ[LOG_LEVEL_ENV] = log_level

    # Signal reload mode to browser_control.py for Windows
    # compatibility: use sync Playwright + ThreadPool only when reload=True
    if reload:
        os.environ["wowooai_RELOAD_MODE"] = "1"
    else:
        os.environ.pop("wowooai_RELOAD_MODE", None)

    setup_logger(log_level)
    _start_parent_watchdog()

    try:
        import pypandoc
        pandoc_dir = os.path.dirname(pypandoc.get_pandoc_path())
        os.environ["PATH"] = pandoc_dir + os.pathsep + os.environ.get("PATH", "")
    except Exception:
        pass
    if log_level in ("debug", "trace"):
        from .main import log_init_timings

        log_init_timings()

    paths = [p for p in hide_access_paths if p]
    if paths:
        logging.getLogger("uvicorn.access").addFilter(
            SuppressPathAccessLogFilter(paths),
        )

    uvicorn.run(
        "wowooai.app._app:app",
        host=host,
        port=port,
        reload=reload,
        workers=1,
        log_level=log_level,
    )

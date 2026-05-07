# -*- coding: utf-8 -*-
"""CLI command: run WowooAI app on a free port in a native webview window."""
# pylint:disable=too-many-branches,too-many-statements,consider-using-with
from __future__ import annotations

import logging
import os
import socket
import subprocess
import sys
import threading
import time
import traceback
import webbrowser

import click

from ..constant import LOG_LEVEL_ENV
from ..utils.logging import setup_logger

try:
    import webview
except ImportError:
    webview = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


class WebViewAPI:
    """API exposed to the webview for external links and file downloads."""

    def open_external_link(self, url: str) -> None:
        """Open URL in system's default browser."""
        if not url.startswith(("http://", "https://")):
            return
        webbrowser.open(url)

    def save_file(self, url: str, filename: str) -> bool:
        """Download a file from *url* and save it via a native save dialog.

        Shows the OS "Save As" dialog so the user can pick a destination,
        then downloads the file and writes it there.  This is the desktop
        equivalent of the browser's ``<a download>`` click pattern which
        pywebview/WebView2 does not support.

        Args:
            url: Full HTTP(S) URL of the file to download.
            filename: Default filename shown in the save dialog.

        Returns:
            True if the file was saved successfully, False if the user
            cancelled the dialog or an error occurred.
        """
        import re
        import shutil
        import urllib.request

        if not url.startswith(("http://", "https://")):
            return False

        # ``urllib.request.urlopen`` writes the HTTP request line as ASCII
        # and raises ``UnicodeEncodeError`` if the URL contains raw non-ASCII
        # characters (common in user-uploaded filenames like
        # "有效合同_副本.xlsx"). Percent-encode the path/query/fragment up
        # front so every later urlopen() call works.
        from urllib.parse import quote, urlsplit, urlunsplit

        parts = urlsplit(url)
        safe_chars = "/-_.~!$&'()*+,;=:@%"
        encoded_url = urlunsplit((
            parts.scheme,
            parts.netloc,
            quote(parts.path, safe=safe_chars),
            quote(parts.query, safe=safe_chars + "=&"),
            quote(parts.fragment, safe=safe_chars),
        ))

        # Sanitize filename: remove characters illegal on Windows
        # (< > : " / \ | ? *) and trim leading/trailing whitespace/dots.
        # Colons are common in backup names like "Backup 2026-04-22 17:36".
        safe_name = re.sub(r'[<>:"/\\|?*]', "_", filename).strip(" .")

        # Ensure the filename has a file extension.
        # In some edge cases the caller may pass a name without an extension;
        # Windows create_file_dialog will not auto-append one.
        if "." not in safe_name:
            import mimetypes
            # Try extracting extension from URL path segment
            url_path = url.split("?")[0]
            url_name = url_path.split("/")[-1]
            if "." in url_name:
                ext = url_name.rsplit(".", 1)[-1]
                if ext and 1 <= len(ext) <= 10:
                    safe_name = f"{safe_name}.{ext}"
            # Fallback: infer from Content-Type header
            if "." not in safe_name:
                try:
                    with urllib.request.urlopen(encoded_url) as resp:
                        ct = resp.headers.get("Content-Type", "")
                        ext = mimetypes.guess_extension(ct)
                        if ext:
                            safe_name = f"{safe_name}{ext}"
                except Exception:
                    pass

        try:
            # Show native OS save dialog via pywebview
            result = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=safe_name,
            )
            if not result:
                return False  # user cancelled

            dest_path = result if isinstance(result, str) else result[0]

            # Percent-encoded URL is computed once at the top of save_file
            # so urlopen does not blow up on non-ASCII filenames.
            with urllib.request.urlopen(encoded_url) as response:
                with open(dest_path, "wb") as f:
                    shutil.copyfileobj(response, f)

            return True
        except Exception:
            logger.exception("save_file failed")
            return False


def _find_free_port(host: str = "127.0.0.1") -> int:
    """Bind to port 0 and return the OS-assigned free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        sock.listen(1)
        return sock.getsockname()[1]


def _wait_for_http(host: str, port: int, timeout_sec: float = 300.0) -> bool:
    """Return True when something accepts TCP on host:port."""
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((host, port))
                return True
        except (OSError, socket.error):
            time.sleep(1)
    return False


def _stream_reader(in_stream, out_stream) -> None:
    """Read from in_stream line by line and write to out_stream.

    Used on Windows to prevent subprocess buffer blocking. Runs in a
    background thread to continuously drain the subprocess output.
    """
    try:
        for line in iter(in_stream.readline, ""):
            if not line:
                break
            out_stream.write(line)
            out_stream.flush()
    except Exception:
        pass
    finally:
        try:
            in_stream.close()
        except Exception:
            pass


def _apply_win_icon(window, icon_path: str) -> None:
    """Force the Windows title-bar AND taskbar icon to *icon_path*.

    On Windows, ``webview.start(icon=...)`` only updates EdgeChromium's
    drawn title bar. The actual OS title-bar icon (top-left corner) and the
    taskbar icon are read from the host process; without intervention Win11
    groups the window under ``python.exe`` and shows that icon.

    This function:
    1. Sets the AppUserModelID so Win11 stops grouping us under python.exe.
    2. After the webview window opens, locates its HWND and sends two
       ``WM_SETICON`` messages (small + big) loaded from ``icon_path``.

    Both steps are best-effort; failures are logged at warning level.
    """
    import ctypes
    from ctypes import wintypes

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "AgentScope.WowooAI.Desktop.1",
        )
    except Exception as e:
        logger.warning(f"SetCurrentProcessExplicitAppUserModelID failed: {e}")

    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    LR_DEFAULTSIZE = 0x00000040

    user32 = ctypes.windll.user32
    user32.LoadImageW.restype = wintypes.HANDLE
    user32.LoadImageW.argtypes = [
        wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
        ctypes.c_int, ctypes.c_int, wintypes.UINT,
    ]
    user32.SendMessageW.restype = ctypes.c_long
    user32.SendMessageW.argtypes = [
        wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
    ]
    user32.FindWindowW.restype = wintypes.HWND
    user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]

    def _set_icons() -> None:
        # Wait for the webview window to materialise. pywebview emits a
        # 'shown' / 'loaded' event but not always reliably across backends,
        # so poll FindWindow by title for up to 10 s.
        hwnd = 0
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            hwnd = user32.FindWindowW(None, "WowooAI Desktop")
            if hwnd:
                break
            time.sleep(0.2)
        if not hwnd:
            logger.warning("Window HWND not found; icon not applied.")
            return

        small = user32.LoadImageW(
            None, icon_path, IMAGE_ICON, 16, 16,
            LR_LOADFROMFILE,
        )
        big = user32.LoadImageW(
            None, icon_path, IMAGE_ICON, 32, 32,
            LR_LOADFROMFILE | LR_DEFAULTSIZE,
        )
        if small:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, small)
        if big:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, big)
        logger.info(
            f"WM_SETICON applied (small={bool(small)}, big={bool(big)})",
        )

    threading.Thread(target=_set_icons, daemon=True).start()


@click.command("desktop")
@click.option(
    "--host",
    default="127.0.0.1",
    show_default=True,
    help="Bind host for the app server.",
)
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(
        ["critical", "error", "warning", "info", "debug", "trace"],
        case_sensitive=False,
    ),
    show_default=True,
    help="Log level for the app process.",
)
def desktop_cmd(
    host: str,
    log_level: str,
) -> None:
    """Run WowooAI app on an auto-selected free port in a webview window.

    Starts the FastAPI app in a subprocess on a free port, then opens a
    native webview window loading that URL. Use for a dedicated desktop
    window without conflicting with an existing WowooAI app instance.
    """
    # Setup logger for desktop command (separate from backend subprocess)
    setup_logger(log_level)

    port = _find_free_port(host)
    url = f"http://{host}:{port}"
    click.echo(f"Starting WowooAI app on {url} (port {port})")
    logger.info("Server subprocess starting...")

    env = os.environ.copy()
    env[LOG_LEVEL_ENV] = log_level
    env["WOWOOAI_PARENT_PID"] = str(os.getpid())

    try:
        import pypandoc
        pandoc_dir = os.path.dirname(pypandoc.get_pandoc_path())
        env["PATH"] = pandoc_dir + os.pathsep + env.get("PATH", "")
    except Exception:
        pass

    if "SSL_CERT_FILE" in env:
        cert_file = env["SSL_CERT_FILE"]
        if os.path.exists(cert_file):
            logger.info(f"SSL certificate: {cert_file}")
        else:
            logger.warning(
                f"SSL_CERT_FILE set but not found: {cert_file}",
            )
    else:
        logger.warning("SSL_CERT_FILE not set on environment")

    is_windows = sys.platform == "win32"
    proc = None
    manually_terminated = (
        False  # Track if we intentionally terminated the process
    )
    try:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "wowooai",
                "app",
                "--host",
                host,
                "--port",
                str(port),
                "--log-level",
                log_level,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE if is_windows else sys.stdout,
            stderr=subprocess.PIPE if is_windows else sys.stderr,
            env=env,
            bufsize=1,
            universal_newlines=True,
        )
        try:
            if is_windows:
                stdout_thread = threading.Thread(
                    target=_stream_reader,
                    args=(proc.stdout, sys.stdout),
                    daemon=True,
                )
                stderr_thread = threading.Thread(
                    target=_stream_reader,
                    args=(proc.stderr, sys.stderr),
                    daemon=True,
                )
                stdout_thread.start()
                stderr_thread.start()
            logger.info("Waiting for HTTP ready...")
            if _wait_for_http(host, port):
                logger.info("HTTP ready, creating webview window...")
                api = WebViewAPI()
                window = webview.create_window(
                    "WowooAI Desktop",
                    url,
                    width=1280,
                    height=800,
                    text_select=True,
                    js_api=api,
                )
                logger.info(
                    "Calling webview.start() (blocks until closed)...",
                )
                # Locate icon.ico for the window title-bar / taskbar.
                # In a packaged install (build_win.ps1) icon.ico is copied
                # to the env root, which is the directory of python.exe.
                # In dev / source runs, it sits in scripts/pack/assets/.
                icon_path = None
                for cand in (
                    os.path.join(os.path.dirname(sys.executable), "icon.ico"),
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__))))),
                        "scripts", "pack", "assets", "icon.ico",
                    ),
                ):
                    if os.path.exists(cand):
                        icon_path = cand
                        break
                if icon_path:
                    logger.info(f"Window icon: {icon_path}")
                    if sys.platform == "win32":
                        _apply_win_icon(window, icon_path)
                webview.start(
                    private_mode=False,
                    icon=icon_path,
                )  # blocks until user closes the window
                logger.info("webview.start() returned (window closed).")
            else:
                logger.error("Server did not become ready in time.")
                click.echo(
                    "Server did not become ready in time; open manually: "
                    + url,
                    err=True,
                )
                try:
                    proc.wait()
                except KeyboardInterrupt:
                    pass  # will be handled in finally
        finally:
            # Ensure backend process is always cleaned up
            # Wrap all cleanup operations to handle race conditions:
            # - Process may exit between poll() and terminate()
            # - terminate()/kill() may raise ProcessLookupError/OSError
            # - We must not let cleanup exceptions mask the original error
            if proc and proc.poll() is None:  # process still running
                logger.info("Terminating backend server...")
                manually_terminated = (
                    True  # Mark that we're intentionally terminating
                )
                try:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5.0)
                        logger.info("Backend server terminated cleanly.")
                    except subprocess.TimeoutExpired:
                        logger.warning(
                            "Backend did not exit in 5s, force killing...",
                        )
                        try:
                            proc.kill()
                            proc.wait()
                            logger.info("Backend server force killed.")
                        except (ProcessLookupError, OSError) as e:
                            # Process already exited, which is fine
                            logger.debug(
                                f"kill() raised {e.__class__.__name__} "
                                f"(process already exited)",
                            )
                except (ProcessLookupError, OSError) as e:
                    # Process already exited between poll() and terminate()
                    logger.debug(
                        f"terminate() raised {e.__class__.__name__} "
                        f"(process already exited)",
                    )
            elif proc:
                logger.info(
                    f"Backend already exited with code {proc.returncode}",
                )

        # Only report errors if process exited unexpectedly
        # (not manually terminated)
        # On Windows, terminate() doesn't use signals so exit codes vary
        # (1, 259, etc.)
        # On Unix/Linux/macOS, terminate() sends SIGTERM (exit code -15)
        # Using a flag is more reliable than checking specific exit codes
        if proc and proc.returncode != 0 and not manually_terminated:
            logger.error(
                f"Backend process exited unexpectedly with code "
                f"{proc.returncode}",
            )
            # Follow POSIX convention for exit codes:
            # - Negative (signal): 128 + signal_number
            # - Positive (normal): use as-is
            # Example: -15 (SIGTERM) -> 143 (128+15), -11 (SIGSEGV) ->
            # 139 (128+11)
            if proc.returncode < 0:
                sys.exit(128 + abs(proc.returncode))
            else:
                sys.exit(proc.returncode or 1)
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt in main, cleaning up...")
        raise
    except Exception as e:
        logger.error(f"Exception: {e!r}")
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        raise

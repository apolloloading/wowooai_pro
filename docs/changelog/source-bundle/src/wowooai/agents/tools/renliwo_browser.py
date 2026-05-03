# -*- coding: utf-8 -*-
# flake8: noqa: E501
"""Renliwo browser automation tool — Playwright action-based engine.

Dedicated tool for operating on renliwo (internal HR platform) URLs.
Built on the same Playwright infrastructure as browser_use, but optimised
for Ant Design Pro (React) single-page apps on a known internal site:

- Per-workspace persistent browser session; login is only needed once.
- Action-per-call model: each call does one atomic operation, returns
  page state so the AI can observe then decide the next step.
- ARIA snapshot (action='snapshot') for reliable element targeting.
- renliwo-specific actions: login, ant_select, nav_menu, nav_submenu, guide.
- All actions return current page state (url, title, alerts, pagination)
  so the AI always knows where it is without an extra call.
- Page guide data is bundled with this tool and can be queried with
  action='guide'; leaf navigation and exports attach compact guide snippets.

⚠️  ONLY use this tool for renliwo URLs.
⚠️  After login, NEVER use action='navigate' to go to business pages —
    that will redirect you back to the login page. Use nav_menu / nav_submenu
    / click to navigate via menu items only.
"""

import asyncio
import atexit
from concurrent import futures
import json
import logging
from pathlib import Path
import sys
import time
from typing import Any, Optional

from agentscope.message import TextBlock
from agentscope.tool import ToolResponse

from ...config import (
    get_playwright_chromium_executable_path,
    get_system_default_browser,
    is_running_in_container,
)
from ...config.context import get_current_workspace_dir
from ...constant import WORKING_DIR, EnvVarLoader

from .browser_snapshot import build_role_snapshot_from_aria

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Page guide index — loaded once at import time from the bundled JSON
# ---------------------------------------------------------------------------

_GUIDE_INDEX: dict[str, Any] = {}
_GUIDE_INDEX_VERSION: str = ""
_GUIDE_DOC_PATH: str = ""   # path to full doc inside the tool data dir


def _load_guide_index() -> None:
    """Load renliwo_guide_index.json from the bundled tool data directory."""
    global _GUIDE_INDEX, _GUIDE_INDEX_VERSION, _GUIDE_DOC_PATH
    if _GUIDE_INDEX:
        return

    candidates = [
        Path(__file__).parent / "renliwo_browser_data" / "renliwo_guide_index.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                _GUIDE_INDEX = data
                _GUIDE_INDEX_VERSION = data.get("version", "")
                _GUIDE_DOC_PATH = str(
                    path.parent / "Renliwo页面结构文档_完整版.md",
                )
                logger.debug(
                    "Loaded renliwo guide index v%s from %s",
                    _GUIDE_INDEX_VERSION,
                    path,
                )
            except Exception as e:
                logger.warning("Failed to load renliwo guide index: %s", e)
            return


# Eagerly load at import
_load_guide_index()


def _guide_for_route(route_hash: str) -> dict[str, Any] | None:
    """Return the guide entry for the given URL hash (e.g. '#/contractManage/list').

    Returns a compact dict with the most useful fields for AI decision-making,
    or None if the route is not in the index.
    """
    if not _GUIDE_INDEX:
        return None
    page = _GUIDE_INDEX.get("route_index", {}).get(route_hash)
    if not page:
        return None
    return {
        "module": page.get("module", ""),
        "page_name": page.get("page_name", ""),
        "route": route_hash,
        "tabs": page.get("tabs", []),
        "export_mode": page.get("export_mode", "none"),
        "export_buttons": page.get("export_buttons", []),
        "all_buttons": page.get("all_buttons", []),
        "select_fields": page.get("select_fields", {}),
        "filter_count": page.get("filter_count", 0),
        "notes": _build_notes(page),
        "doc_ref": _GUIDE_DOC_PATH or "",
        "guide_version": _GUIDE_INDEX_VERSION,
    }


def _guide_for_url(url: str) -> dict[str, Any] | None:
    """Extract hash from a full URL and look up the guide."""
    if "#/" not in url:
        return None
    route_hash = "#/" + url.split("#/", 1)[1]
    # Strip query params from hash
    route_hash = route_hash.split("?")[0]
    return _guide_for_route(route_hash)


def _guide_routes_summary(max_routes: int = 80) -> dict[str, Any]:
    """Return a compact summary of available route guides."""
    route_index = _GUIDE_INDEX.get("route_index", {}) if _GUIDE_INDEX else {}
    routes = []
    for route, page in list(route_index.items())[:max_routes]:
        routes.append(
            {
                "route": route,
                "module": page.get("module", ""),
                "page_name": page.get("page_name", ""),
                "export_mode": page.get("export_mode", "none"),
            },
        )
    return {
        "guide_version": _GUIDE_INDEX_VERSION,
        "doc_ref": _GUIDE_DOC_PATH or "",
        "route_count": len(route_index),
        "routes": routes,
        "truncated": len(route_index) > max_routes,
    }


def _guide_for_doc_ref() -> dict[str, Any]:
    """Return guide metadata without reading the full markdown document."""
    return {
        "guide_version": _GUIDE_INDEX_VERSION,
        "doc_ref": _GUIDE_DOC_PATH or "",
        "note": (
            "Use route/current page guide first. Read the full markdown only "
            "when the compact guide is insufficient."
        ),
    }


def _guide_for_current_page(state: dict, page_id: str, url: str = "") -> ToolResponse:
    """Return the compact guide for a specified URL/route or current page."""
    lookup_url = (url or "").strip()
    page_state = {"url": lookup_url, "title": ""}

    if lookup_url.startswith("#/"):
        guide = _guide_for_route(lookup_url.split("?")[0])
    elif lookup_url:
        guide = _guide_for_url(lookup_url)
    else:
        page = _get_page(state, page_id)
        if page:
            page_state = _page_state_sync_snapshot(page)
            guide = _guide_for_url(page_state.get("url", ""))
        else:
            guide = None

    payload = {"ok": True, "page": page_state}
    if guide:
        payload["guide"] = guide
    else:
        payload["ok"] = False if not lookup_url and not _get_page(state, page_id) else True
        payload["message"] = (
            "No guide matched current page URL; returning route summary."
        )
        payload["guide"] = _guide_routes_summary(max_routes=20)
    payload["full_doc"] = _guide_for_doc_ref()
    return _tool_response(json.dumps(payload, ensure_ascii=False, indent=2))


def _page_state_sync_snapshot(page: Any) -> dict[str, Any]:
    """Return a minimal sync-safe page state for guide lookup."""
    return {"url": getattr(page, "url", ""), "title": ""}


def _build_notes(page: dict) -> list[str]:
    """Build contextual notes / warnings for this page."""
    notes = []
    btns = page.get("all_buttons", [])
    # Full-width space warning
    fw_btns = [b for b in btns if "\u3000" in b or (" " in b and len(b) <= 6)]
    if fw_btns:
        notes.append(
            f"按钮含全角空格，优先用 has-text 模糊匹配: {fw_btns}"
        )
    # Export notes
    em = page.get("export_mode", "none")
    if em == "async_export_center":
        notes.append(
            "导出为异步模式：点击导出按钮后，须到「综合管理→导出中心→异步导出记录」等待文件生成再下载。"
        )
    elif em == "direct_download":
        notes.append(
            "导出为直接下载：使用 action='export' 自动拦截，文件默认保存到桌面。"
        )
    return notes

# ---------------------------------------------------------------------------
# Sync / async mode (Windows + reload mode needs sync)
# ---------------------------------------------------------------------------

_USE_SYNC_PLAYWRIGHT = sys.platform == "win32" and EnvVarLoader.get_bool(
    "WOWOOHR_RELOAD_MODE",
)

if _USE_SYNC_PLAYWRIGHT:
    _executor: Optional[futures.ThreadPoolExecutor] = None

    def _get_executor() -> futures.ThreadPoolExecutor:
        global _executor
        if _executor is None:
            _executor = futures.ThreadPoolExecutor(
                max_workers=1,
                thread_name_prefix="rw_playwright",
            )
        return _executor

    async def _run_sync(func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _get_executor(),
            lambda: func(*args, **kwargs),
        )
else:
    async def _run_sync(func, *args, **kwargs):
        return await func(*args, **kwargs)


# ---------------------------------------------------------------------------
# Per-workspace state
# ---------------------------------------------------------------------------

_rw_workspace_states: dict[str, dict[str, Any]] = {}


def _make_fresh_state(workspace_id: str, workspace_dir: str) -> dict[str, Any]:
    # Store cookies under renliwo_browser/ so it doesn't clash with browser_use
    user_data_dir = (
        str(Path(workspace_dir) / "renliwo_browser" / "user_data")
        if workspace_dir
        else ""
    )
    return {
        "playwright": None,
        "browser": None,
        "context": None,
        "_sync_playwright": None,
        "_sync_browser": None,
        "_sync_context": None,
        "pages": {},
        "refs": {},
        "refs_frame": {},
        "console_logs": {},
        "pending_dialogs": {},
        "pending_file_choosers": {},
        "headless": True,
        "current_page_id": None,
        "page_counter": 0,
        "last_activity_time": 0.0,
        "_last_browser_error": None,
        "workspace_id": workspace_id,
        "user_data_dir": user_data_dir,
        "launch_mode": None,
    }


def _get_workspace_state(workspace_id: str, workspace_dir: str = "") -> dict[str, Any]:
    if workspace_id not in _rw_workspace_states:
        _rw_workspace_states[workspace_id] = _make_fresh_state(workspace_id, workspace_dir)
    return _rw_workspace_states[workspace_id]


def _touch_activity(state: dict) -> None:
    state["last_activity_time"] = time.monotonic()


def _is_browser_running(state: dict) -> bool:
    if _USE_SYNC_PLAYWRIGHT:
        return state.get("_sync_context") is not None or state.get("_sync_browser") is not None
    return state.get("browser") is not None or state.get("context") is not None


def _reset_browser_state(state: dict) -> None:
    state["playwright"] = None
    state["browser"] = None
    state["context"] = None
    state["_sync_playwright"] = None
    state["_sync_browser"] = None
    state["_sync_context"] = None
    state["pages"].clear()
    state["refs"].clear()
    state["refs_frame"].clear()
    state["console_logs"].clear()
    state["pending_dialogs"].clear()
    state["pending_file_choosers"].clear()
    state["current_page_id"] = None
    state["page_counter"] = 0
    state["last_activity_time"] = 0.0
    state["headless"] = True
    state["launch_mode"] = None


# ---------------------------------------------------------------------------
# atexit cleanup
# ---------------------------------------------------------------------------

def _atexit_cleanup() -> None:
    if not _rw_workspace_states:
        return
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running() or loop.is_closed():
            return
        for ws_state in list(_rw_workspace_states.values()):
            if _is_browser_running(ws_state):
                try:
                    loop.run_until_complete(_action_stop(ws_state))
                except Exception:
                    pass
    except Exception:
        pass


atexit.register(_atexit_cleanup)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tool_response(text: str) -> ToolResponse:
    return ToolResponse(content=[TextBlock(type="text", text=text)])


def _ok(**kwargs) -> ToolResponse:
    return _tool_response(json.dumps({"ok": True, **kwargs}, ensure_ascii=False, indent=2))


def _err(error: str, **kwargs) -> ToolResponse:
    return _tool_response(json.dumps({"ok": False, "error": error, **kwargs}, ensure_ascii=False, indent=2))


def _chromium_launch_args() -> list[str]:
    args = []
    if is_running_in_container() or sys.platform == "win32":
        args.extend(["--no-sandbox"])
    if is_running_in_container():
        args.extend(["--disable-dev-shm-usage"])
    if sys.platform == "win32":
        args.extend(["--disable-gpu"])
    return args


def _resolve_launch_target() -> tuple[Optional[str], Optional[str]]:
    use_default = not is_running_in_container() and EnvVarLoader.get_bool(
        "WOWOOHR_BROWSER_USE_DEFAULT", True,
    )
    default_kind, default_path = get_system_default_browser() if use_default else (None, None)
    if default_kind == "chromium" and default_path:
        return default_kind, default_path
    if default_kind == "webkit":
        return default_kind, None
    return default_kind, get_playwright_chromium_executable_path()


def _parse_json_param(value: str, default: Any = None):
    if not value or not isinstance(value, str):
        return default
    value = value.strip()
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        if "," in value:
            return [x.strip() for x in value.split(",")]
        return default


def _get_page(state: dict, page_id: str):
    return state["pages"].get(page_id)


def _get_context(state: dict):
    return state["context"] or state.get("_sync_context")


def _get_refs(state: dict, page_id: str) -> dict[str, dict]:
    return state["refs"].setdefault(page_id, {})


def _get_root(page, frame_selector: str = ""):
    if not (frame_selector and frame_selector.strip()):
        return page
    return page.frame_locator(frame_selector.strip())


def _get_locator_by_ref(state: dict, page, page_id: str, ref: str, frame_selector: str = ""):
    refs = _get_refs(state, page_id)
    info = refs.get(ref)
    if not info:
        return None
    role = info.get("role", "generic")
    name = info.get("name")
    nth = info.get("nth")
    root = _get_root(page, frame_selector)
    locator = root.get_by_role(role, name=name or None)
    if nth is not None:
        locator = locator.nth(nth)
    return locator


def _next_page_id(state: dict) -> str:
    state["page_counter"] = state.get("page_counter", 0) + 1
    return f"page_{state['page_counter']}"


def _attach_page_listeners(state: dict, page, page_id: str) -> None:
    logs = state["console_logs"].setdefault(page_id, [])

    def on_console(msg):
        logs.append({"level": msg.type, "text": msg.text})

    page.on("console", on_console)
    dialogs = state["pending_dialogs"].setdefault(page_id, [])

    def on_dialog(dialog):
        dialogs.append(dialog)

    page.on("dialog", on_dialog)
    choosers = state["pending_file_choosers"].setdefault(page_id, [])

    def on_filechooser(chooser):
        choosers.append(chooser)

    page.on("filechooser", on_filechooser)


def _register_page(state: dict, page, page_id: str) -> None:
    state["refs"][page_id] = {}
    state["console_logs"][page_id] = []
    state["pending_dialogs"][page_id] = []
    state["pending_file_choosers"][page_id] = []
    _attach_page_listeners(state, page, page_id)
    state["pages"][page_id] = page


def _attach_context_listeners(state: dict, context) -> None:
    def on_page(page):
        new_id = _next_page_id(state)
        _register_page(state, page, new_id)
        state["current_page_id"] = new_id
        logger.debug("New tab opened, registered as page_id=%s", new_id)

    context.on("page", on_page)


# ---------------------------------------------------------------------------
# Page state snapshot (lightweight — returned with every action response)
# ---------------------------------------------------------------------------

async def _page_state(state: dict, page_id: str) -> dict:
    """Return lightweight page state: url, title, active_nav, active_tab,
    headings, table_headers, alerts, pagination."""
    page = _get_page(state, page_id)
    if page is None:
        return {"url": "", "title": ""}
    try:
        info = await page.evaluate("""() => {
            const url = location.href;
            const title = document.title;
            const activeNav = [];
            document.querySelectorAll('.ant-menu-horizontal .ant-menu-item-selected').forEach(el => {
                const t = (el.innerText || '').trim(); if (t) activeNav.push(t);
            });
            const activeTab = [];
            document.querySelectorAll('.ant-tabs-tab-active').forEach(el => {
                const t = (el.innerText || '').trim(); if (t) activeTab.push(t);
            });
            const headings = [];
            document.querySelectorAll('h1, h2, .ant-breadcrumb, .ant-page-header-heading-title').forEach(el => {
                const t = (el.innerText || '').trim().substring(0, 60);
                if (t && el.children.length <= 2) headings.push(t);
            });
            const tableHeaders = [];
            document.querySelectorAll('.ant-table-thead th').forEach(el => {
                if (tableHeaders.length >= 10) return;
                const t = (el.innerText || '').trim(); if (t) tableHeaders.push(t);
            });
            const alerts = [];
            document.querySelectorAll(
                '.ant-message-notice-content, .ant-alert-message, ' +
                '.ant-notification-notice-message, .ant-form-item-explain-error'
            ).forEach(el => {
                const t = (el.innerText || '').trim().substring(0, 100); if (t) alerts.push(t);
            });
            const pagination = [];
            document.querySelectorAll('.ant-pagination-total-text, .ant-table-pagination').forEach(el => {
                const t = (el.innerText || '').trim().substring(0, 60); if (t) pagination.push(t);
            });
            return {url, title, activeNav, activeTab, headings, tableHeaders, alerts, pagination};
        }""")
        return {
            "url": info.get("url", ""),
            "title": info.get("title", ""),
            "active_nav": info.get("activeNav", []),
            "active_tab": info.get("activeTab", []),
            "headings": info.get("headings", []),
            "table_headers": info.get("tableHeaders", []),
            "alerts": info.get("alerts", []),
            "pagination": info.get("pagination", []),
        }
    except Exception as e:
        return {"url": getattr(page, "url", ""), "title": "", "error": str(e)}


def _with_page_state(resp_dict: dict, ps: dict, with_guide: bool = False) -> ToolResponse:
    """Merge page_state (and optionally a guide entry) into a response dict."""
    resp_dict["page"] = ps
    if with_guide:
        guide = _guide_for_url(ps.get("url", ""))
        if guide:
            resp_dict["guide"] = guide
    return _tool_response(json.dumps(resp_dict, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Browser lifecycle
# ---------------------------------------------------------------------------

async def _ensure_browser(state: dict) -> bool:
    """Start browser if not running. Returns True when ready."""
    if _USE_SYNC_PLAYWRIGHT:
        if state["_sync_context"] is not None:
            _touch_activity(state)
            return True
    else:
        if state["context"] is not None:
            _touch_activity(state)
            return True

    try:
        await _action_start(state, headed=False)
        state["_last_browser_error"] = None
        _touch_activity(state)
        return True
    except Exception as e:
        state["_last_browser_error"] = str(e)
        return False


async def _action_start(state: dict, headed: bool = False) -> ToolResponse:
    if _USE_SYNC_PLAYWRIGHT:
        already = state["_sync_browser"] is not None or state["_sync_context"] is not None
    else:
        already = state["browser"] is not None or state["context"] is not None

    if already:
        if headed and state["headless"]:
            # Restart as headed
            try:
                await _action_stop(state)
            except Exception:
                pass
        else:
            return _ok(message="Browser already running", headless=state["headless"])

    # Renliwo is an internal SPA — always use Chromium (not WebKit);
    # force headless=True even if headed=True is passed, for stability.
    state["headless"] = True

    try:
        if _USE_SYNC_PLAYWRIGHT:
            from playwright.sync_api import sync_playwright
            loop = asyncio.get_event_loop()

            def _launch():
                pw = sync_playwright().start()
                default_kind, exe = _resolve_launch_target()
                extra_args = list(_chromium_launch_args())
                if exe and default_kind == "chromium":
                    udd = state["user_data_dir"]
                    if udd:
                        Path(udd).mkdir(parents=True, exist_ok=True)
                        ctx = pw.chromium.launch_persistent_context(
                            user_data_dir=udd, headless=True,
                            executable_path=exe,
                            args=["--no-first-run", "--no-default-browser-check",
                                  "--disable-sync", *extra_args],
                        )
                        _attach_context_listeners(state, ctx)
                        return pw, None, ctx
                    browser = pw.chromium.launch(headless=True, executable_path=exe,
                                                  args=extra_args or [])
                else:
                    browser = pw.chromium.launch(headless=True,
                                                  args=["--no-first-run", *extra_args])
                ctx = browser.new_context()
                _attach_context_listeners(state, ctx)
                return pw, browser, ctx

            pw, browser, ctx = await loop.run_in_executor(_get_executor(), _launch)
            state["_sync_playwright"] = pw
            state["_sync_browser"] = browser
            state["_sync_context"] = ctx
            state["launch_mode"] = "playwright_sync"
        else:
            from playwright.async_api import async_playwright
            pw = await async_playwright().start()
            default_kind, exe = _resolve_launch_target()
            extra_args = list(_chromium_launch_args())

            if exe and default_kind == "chromium":
                udd = state["user_data_dir"]
                if udd:
                    Path(udd).mkdir(parents=True, exist_ok=True)
                    ctx = await pw.chromium.launch_persistent_context(
                        user_data_dir=udd, headless=True,
                        executable_path=exe,
                        args=["--no-first-run", "--no-default-browser-check",
                              "--disable-sync", *extra_args],
                    )
                    _attach_context_listeners(state, ctx)
                    state["playwright"] = pw
                    state["browser"] = None
                    state["context"] = ctx
                else:
                    pw_browser = await pw.chromium.launch(headless=True,
                                                           executable_path=exe,
                                                           args=extra_args or [])
                    ctx = await pw_browser.new_context()
                    _attach_context_listeners(state, ctx)
                    state["playwright"] = pw
                    state["browser"] = pw_browser
                    state["context"] = ctx
            else:
                # No system chromium: fall back to playwright's bundled chromium
                pw_browser = await pw.chromium.launch(
                    headless=True,
                    args=["--no-first-run", "--no-default-browser-check",
                          "--disable-sync", *extra_args],
                )
                ctx = await pw_browser.new_context()
                _attach_context_listeners(state, ctx)
                state["playwright"] = pw
                state["browser"] = pw_browser
                state["context"] = ctx

            state["launch_mode"] = "playwright_async"

        _touch_activity(state)
        return _ok(message="Browser started (headless)", headless=True,
                   launch_mode=state["launch_mode"])
    except Exception as e:
        _reset_browser_state(state)
        return _err(f"Browser start failed: {e}")


async def _action_stop(state: dict) -> ToolResponse:
    if not _is_browser_running(state):
        return _ok(message="Browser not running")

    if _USE_SYNC_PLAYWRIGHT:
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(_get_executor(), lambda: (
                state["_sync_browser"].close() if state["_sync_browser"] else
                (state["_sync_context"].close() if state["_sync_context"] else None)
            ))
            await loop.run_in_executor(_get_executor(), lambda: (
                state["_sync_playwright"].stop() if state["_sync_playwright"] else None
            ))
        except Exception:
            pass
        finally:
            _reset_browser_state(state)
    else:
        try:
            if state["context"] is not None:
                try:
                    await state["context"].close()
                except Exception:
                    pass
            if state["browser"] is not None:
                try:
                    await state["browser"].close()
                except Exception:
                    pass
            if state["playwright"] is not None:
                try:
                    await state["playwright"].stop()
                except Exception:
                    pass
        finally:
            _reset_browser_state(state)

    return _ok(message="Browser stopped")


# ---------------------------------------------------------------------------
# Ensure a live page exists, return page_id
# ---------------------------------------------------------------------------

async def _ensure_page(state: dict) -> Optional[str]:
    """Return current page_id, creating a new page if needed. None on failure."""
    if not await _ensure_browser(state):
        return None
    current = state.get("current_page_id")
    ctx = _get_context(state)
    if current and current in state["pages"]:
        page = state["pages"][current]
        try:
            if _USE_SYNC_PLAYWRIGHT:
                closed = page.is_closed()
            else:
                closed = page.is_closed()
            if not closed:
                return current
        except Exception:
            pass
    # Create a new page
    try:
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            page = await loop.run_in_executor(_get_executor(), lambda: ctx.new_page())
        else:
            page = await ctx.new_page()
        page_id = _next_page_id(state)
        _register_page(state, page, page_id)
        state["current_page_id"] = page_id
        return page_id
    except Exception:
        return None


# ---------------------------------------------------------------------------
# login action
# ---------------------------------------------------------------------------

async def _action_login(state: dict, page_id: str) -> ToolResponse:
    """Login to renliwo using credentials from config.json > plugins.renliwo.
    Skipped if already logged in (URL does not contain #/login)."""
    page = _get_page(state, page_id)
    if page is None:
        return _err(f"Page '{page_id}' not found")

    # Check if already logged in
    try:
        current_url = page.url
    except Exception:
        current_url = ""

    if current_url and "about:blank" not in current_url and "#/login" not in current_url:
        ps = await _page_state(state, page_id)
        return _with_page_state({"ok": True, "message": "Already logged in", "skipped": True}, ps)

    try:
        from ...config.utils import load_config
        cfg = load_config().plugins.get("renliwo", {})
        username = cfg.get("username", "")
        password = cfg.get("password", "")
    except Exception:
        username = ""
        password = ""

    if not username or not password:
        return _err(
            "No renliwo credentials found. Add username/password to "
            "config.json > plugins > renliwo."
        )

    try:
        login_url = "https://ereference-v-uat.renliwo.com/#/login"
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(_get_executor(), lambda: page.goto(login_url))
            await asyncio.sleep(1.5)
            await loop.run_in_executor(_get_executor(), lambda: page.fill("#username", username))
            await loop.run_in_executor(_get_executor(), lambda: page.fill("#password", password))
            await loop.run_in_executor(_get_executor(), lambda: page.click("button.ant-btn-primary"))
            await asyncio.sleep(2.5)
        else:
            await page.goto(login_url)
            await page.wait_for_load_state("networkidle", timeout=15000)
            await page.fill("#username", username)
            await page.fill("#password", password)
            await page.click("button.ant-btn-primary")
            await page.wait_for_load_state("networkidle", timeout=15000)
            await asyncio.sleep(2)

        final_url = page.url
        if "#/login" in final_url:
            ps = await _page_state(state, page_id)
            return _with_page_state(
                {"ok": False, "error": "Login failed — still on login page. Check credentials."},
                ps,
            )

        ps = await _page_state(state, page_id)
        # After login, attach guide for the landing page so AI immediately
        # knows what page it landed on and what actions are available.
        return _with_page_state({"ok": True, "message": "Login successful"}, ps, with_guide=True)
    except Exception as e:
        return _err(f"Login failed: {e}")


# ---------------------------------------------------------------------------
# open (first navigation to login page only)
# ---------------------------------------------------------------------------

async def _action_open(state: dict, url: str, page_id: str) -> ToolResponse:
    """Open renliwo login page. After login, navigate ONLY via menu clicks."""
    url = (url or "https://ereference-v-uat.renliwo.com/#/login").strip()
    if not await _ensure_browser(state):
        return _err(state.get("_last_browser_error") or "Browser not started")
    try:
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            page = await loop.run_in_executor(
                _get_executor(), lambda: _get_context(state).new_page()
            )
        else:
            page = await state["context"].new_page()
        _register_page(state, page, page_id)
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(_get_executor(), lambda: page.goto(url))
        else:
            await page.goto(url)
        state["current_page_id"] = page_id
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state({"ok": True, "message": f"Opened {url}", "page_id": page_id}, ps)
    except Exception as e:
        return _err(f"Open failed: {e}")


# ---------------------------------------------------------------------------
# snapshot (ARIA snapshot — primary way to discover elements)
# ---------------------------------------------------------------------------

async def _action_snapshot(state: dict, page_id: str, filename: str = "") -> ToolResponse:
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            raw = await loop.run_in_executor(
                _get_executor(),
                lambda: page.locator(":root").aria_snapshot(),
            )
        else:
            raw = await page.locator(":root").aria_snapshot()

        raw_str = str(raw) if raw is not None else ""
        snapshot, refs = build_role_snapshot_from_aria(raw_str, interactive=False, compact=False)
        state["refs"][page_id] = refs
        state["refs_frame"][page_id] = ""
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        out: dict[str, Any] = {
            "ok": True,
            "snapshot": snapshot,
            "refs": list(refs.keys()),
        }
        if filename and filename.strip():
            from ...config.context import get_current_workspace_dir as _gcwd
            base = (_gcwd() or WORKING_DIR) / "browser"
            base.mkdir(parents=True, exist_ok=True)
            resolved = str(base / filename.strip())
            with open(resolved, "w", encoding="utf-8") as f:
                f.write(snapshot)
            out["filename"] = resolved
        out["page"] = ps
        return _tool_response(json.dumps(out, ensure_ascii=False, indent=2))
    except Exception as e:
        return _err(f"Snapshot failed: {e}")


# ---------------------------------------------------------------------------
# click
# ---------------------------------------------------------------------------

async def _action_click(
    state: dict,
    page_id: str,
    selector: str = "",
    ref: str = "",
    wait_after: float = 0.0,
    double_click: bool = False,
    frame_selector: str = "",
) -> ToolResponse:
    ref = (ref or "").strip()
    selector = (selector or "").strip()
    if not ref and not selector:
        return _err("selector or ref required for click")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            if ref:
                locator = _get_locator_by_ref(state, page, page_id, ref, frame_selector)
                if locator is None:
                    return _err(f"Unknown ref: {ref}")
                fn = locator.dblclick if double_click else locator.click
                await loop.run_in_executor(_get_executor(), fn)
            else:
                root = _get_root(page, frame_selector)
                locator = root.locator(selector).first
                fn = locator.dblclick if double_click else locator.click
                await loop.run_in_executor(_get_executor(), fn)
        else:
            if ref:
                locator = _get_locator_by_ref(state, page, page_id, ref, frame_selector)
                if locator is None:
                    return _err(f"Unknown ref: {ref}")
                if double_click:
                    await locator.dblclick()
                else:
                    await locator.click()
            else:
                root = _get_root(page, frame_selector)
                locator = root.locator(selector).first
                if double_click:
                    await locator.dblclick()
                else:
                    await locator.click()

        if wait_after > 0:
            await asyncio.sleep(wait_after)
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state({"ok": True, "message": f"Clicked {ref or selector}"}, ps)
    except Exception as e:
        return _err(f"Click failed: {e}")


# ---------------------------------------------------------------------------
# type
# ---------------------------------------------------------------------------

async def _action_type(
    state: dict,
    page_id: str,
    selector: str = "",
    ref: str = "",
    text: str = "",
    submit: bool = False,
    slowly: bool = False,
    frame_selector: str = "",
) -> ToolResponse:
    ref = (ref or "").strip()
    selector = (selector or "").strip()
    if not ref and not selector:
        return _err("selector or ref required for type")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            if ref:
                locator = _get_locator_by_ref(state, page, page_id, ref, frame_selector)
                if locator is None:
                    return _err(f"Unknown ref: {ref}")
                if slowly:
                    await loop.run_in_executor(_get_executor(), lambda: locator.press_sequentially(text or ""))
                else:
                    await loop.run_in_executor(_get_executor(), lambda: locator.fill(text or ""))
                if submit:
                    await loop.run_in_executor(_get_executor(), lambda: locator.press("Enter"))
            else:
                root = _get_root(page, frame_selector)
                loc = root.locator(selector).first
                if slowly:
                    await loop.run_in_executor(_get_executor(), lambda: loc.press_sequentially(text or ""))
                else:
                    await loop.run_in_executor(_get_executor(), lambda: loc.fill(text or ""))
                if submit:
                    await loop.run_in_executor(_get_executor(), lambda: loc.press("Enter"))
        else:
            if ref:
                locator = _get_locator_by_ref(state, page, page_id, ref, frame_selector)
                if locator is None:
                    return _err(f"Unknown ref: {ref}")
                if slowly:
                    await locator.press_sequentially(text or "")
                else:
                    await locator.fill(text or "")
                if submit:
                    await locator.press("Enter")
            else:
                root = _get_root(page, frame_selector)
                loc = root.locator(selector).first
                if slowly:
                    await loc.press_sequentially(text or "")
                else:
                    await loc.fill(text or "")
                if submit:
                    await loc.press("Enter")

        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state({"ok": True, "message": f"Typed into {ref or selector}"}, ps)
    except Exception as e:
        return _err(f"Type failed: {e}")


# ---------------------------------------------------------------------------
# wait_for
# ---------------------------------------------------------------------------

async def _action_wait_for(
    state: dict,
    page_id: str,
    wait_time: float = 0,
    text: str = "",
    text_gone: str = "",
    timeout: float = 15.0,
) -> ToolResponse:
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if wait_time and wait_time > 0:
            await asyncio.sleep(wait_time)
        text = (text or "").strip()
        text_gone = (text_gone or "").strip()
        ms = int(timeout * 1000)
        if text:
            locator = page.get_by_text(text)
            if _USE_SYNC_PLAYWRIGHT:
                await _run_sync(locator.wait_for, state="visible", timeout=ms)
            else:
                await locator.wait_for(state="visible", timeout=ms)
        if text_gone:
            locator = page.get_by_text(text_gone)
            if _USE_SYNC_PLAYWRIGHT:
                await _run_sync(locator.wait_for, state="hidden", timeout=ms)
            else:
                await locator.wait_for(state="hidden", timeout=ms)
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state({"ok": True, "message": "Wait completed"}, ps)
    except Exception as e:
        return _err(f"Wait failed: {e}")


# ---------------------------------------------------------------------------
# evaluate (JS)
# ---------------------------------------------------------------------------

async def _action_evaluate(
    state: dict,
    page_id: str,
    code: str,
    ref: str = "",
    frame_selector: str = "",
) -> ToolResponse:
    code = (code or "").strip()
    if not code:
        return _err("code required for evaluate")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if ref and ref.strip():
            locator = _get_locator_by_ref(state, page, page_id, ref.strip(), frame_selector)
            if locator is None:
                return _err(f"Unknown ref: {ref}")
            if _USE_SYNC_PLAYWRIGHT:
                result = await _run_sync(locator.evaluate, code)
            else:
                result = await locator.evaluate(code)
        else:
            expr = code if (code.startswith("(") or code.startswith("function")) else f"() => {{ return ({code}); }}"
            if _USE_SYNC_PLAYWRIGHT:
                result = await _run_sync(page.evaluate, expr)
            else:
                result = await page.evaluate(expr)
        _touch_activity(state)
        try:
            return _tool_response(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))
        except TypeError:
            return _tool_response(json.dumps({"ok": True, "result": str(result)}, ensure_ascii=False, indent=2))
    except Exception as e:
        return _err(f"Evaluate failed: {e}")


# ---------------------------------------------------------------------------
# screenshot
# ---------------------------------------------------------------------------

async def _action_screenshot(
    state: dict,
    page_id: str,
    path: str = "",
    full_page: bool = False,
) -> ToolResponse:
    import base64
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if path:
            from ...config.context import get_current_workspace_dir as _gcwd
            base = (_gcwd() or WORKING_DIR) / "browser"
            base.mkdir(parents=True, exist_ok=True)
            resolved = str(base / path) if not Path(path).is_absolute() else path
            if _USE_SYNC_PLAYWRIGHT:
                await _run_sync(page.screenshot, path=resolved, full_page=full_page, type="jpeg", quality=80)
            else:
                await page.screenshot(path=resolved, full_page=full_page, type="jpeg", quality=80)
            _touch_activity(state)
            return _ok(message=f"Screenshot saved to {resolved}", path=resolved)
        else:
            if _USE_SYNC_PLAYWRIGHT:
                buf = await _run_sync(page.screenshot, type="jpeg", quality=75, full_page=full_page)
            else:
                buf = await page.screenshot(type="jpeg", quality=75, full_page=full_page)
            b64 = base64.b64encode(buf).decode("utf-8")
            _touch_activity(state)
            return _ok(screenshot=b64, current_url=page.url)
    except Exception as e:
        return _err(f"Screenshot failed: {e}")


# ---------------------------------------------------------------------------
# press_key
# ---------------------------------------------------------------------------

async def _action_press_key(state: dict, page_id: str, key: str) -> ToolResponse:
    key = (key or "").strip()
    if not key:
        return _err("key required for press_key")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if _USE_SYNC_PLAYWRIGHT:
            await _run_sync(page.keyboard.press, key)
        else:
            await page.keyboard.press(key)
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state({"ok": True, "message": f"Pressed {key}"}, ps)
    except Exception as e:
        return _err(f"Press key failed: {e}")


# ---------------------------------------------------------------------------
# file_upload
# ---------------------------------------------------------------------------

async def _action_file_upload(state: dict, page_id: str, paths_json: str) -> ToolResponse:
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    paths = _parse_json_param(paths_json, [])
    if not isinstance(paths, list):
        paths = []
    choosers = state["pending_file_choosers"].get(page_id, [])
    if not choosers:
        return _err("No pending file chooser. Click the upload button first, then call file_upload.")
    try:
        chooser = choosers.pop(0)
        if _USE_SYNC_PLAYWRIGHT:
            await _run_sync(chooser.set_files, paths)
        else:
            await chooser.set_files(paths)
        _touch_activity(state)
        return _ok(message=f"Uploaded {len(paths)} file(s)")
    except Exception as e:
        return _err(f"File upload failed: {e}")


# ---------------------------------------------------------------------------
# handle_dialog
# ---------------------------------------------------------------------------

async def _action_handle_dialog(
    state: dict, page_id: str, accept: bool = True, prompt_text: str = ""
) -> ToolResponse:
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    dialogs = state["pending_dialogs"].get(page_id, [])
    if not dialogs:
        return _err("No pending dialog")
    try:
        dialog = dialogs.pop(0)
        if accept:
            if prompt_text:
                if _USE_SYNC_PLAYWRIGHT:
                    await _run_sync(dialog.accept, prompt_text)
                else:
                    await dialog.accept(prompt_text)
            else:
                if _USE_SYNC_PLAYWRIGHT:
                    await _run_sync(dialog.accept)
                else:
                    await dialog.accept()
        else:
            if _USE_SYNC_PLAYWRIGHT:
                await _run_sync(dialog.dismiss)
            else:
                await dialog.dismiss()
        return _ok(message="Dialog handled")
    except Exception as e:
        return _err(f"Handle dialog failed: {e}")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

async def _action_status(state: dict) -> ToolResponse:
    if not _is_browser_running(state):
        return _ok(running=False)
    page_ids = list(state["pages"].keys())
    pages_info = []
    for pid in page_ids:
        page = state["pages"][pid]
        try:
            title = await page.title() if not _USE_SYNC_PLAYWRIGHT else ""
        except Exception:
            title = ""
        pages_info.append({"page_id": pid, "url": getattr(page, "url", ""), "title": title})
    return _ok(
        running=True,
        headless=state.get("headless", True),
        current_page_id=state.get("current_page_id"),
        pages=pages_info,
    )


# ---------------------------------------------------------------------------
# cookies_clear (reset session — force re-login)
# ---------------------------------------------------------------------------

async def _action_cookies_clear(state: dict) -> ToolResponse:
    ctx = _get_context(state)
    if not ctx:
        return _err("Browser not running")
    try:
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(_get_executor(), ctx.clear_cookies)
        else:
            await ctx.clear_cookies()
        return _ok(message="Cookies cleared — next login will be fresh")
    except Exception as e:
        return _err(f"Cookies clear failed: {e}")


# ---------------------------------------------------------------------------
# renliwo-specific: nav_menu (top navigation)
# ---------------------------------------------------------------------------

async def _action_nav_menu(
    state: dict,
    page_id: str,
    menu_text: str,
    wait_after: float = 1.5,
) -> ToolResponse:
    """Click a top-level navigation menu item (综合管理, 专项职能外包, etc.)
    and wait for the page to settle."""
    menu_text = (menu_text or "").strip()
    if not menu_text:
        return _err("menu_text required for nav_menu")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        selector = f'.ant-menu-horizontal li:has-text("{menu_text}")'
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(_get_executor(), lambda: page.click(selector))
        else:
            await page.click(selector)
            await page.wait_for_load_state("networkidle", timeout=10000)
        await asyncio.sleep(wait_after)
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state(
            {"ok": True, "message": f"Clicked top-nav '{menu_text}'"}, ps
        )
    except Exception as e:
        return _err(f"nav_menu failed: {e}")


# ---------------------------------------------------------------------------
# renliwo-specific: nav_submenu (expand sidebar submenu or click leaf item)
# ---------------------------------------------------------------------------

async def _action_nav_submenu(
    state: dict,
    page_id: str,
    item_text: str,
    is_leaf: bool = False,
    wait_after: float = 0.8,
) -> ToolResponse:
    """Expand a sidebar submenu group (is_leaf=False) or click a leaf page
    item (is_leaf=True).

    For submenu groups, clicks .ant-menu-submenu-title containing item_text.
    For leaf items, clicks .ant-menu-item containing item_text.
    """
    item_text = (item_text or "").strip()
    if not item_text:
        return _err("item_text required for nav_submenu")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        if is_leaf:
            selector = f'.ant-menu-item:has-text("{item_text}")'
            if _USE_SYNC_PLAYWRIGHT:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(_get_executor(), lambda: page.locator(selector).first.click())
            else:
                await page.locator(selector).first.click()
                await page.wait_for_load_state("networkidle", timeout=10000)
            await asyncio.sleep(max(wait_after, 1.0))
        else:
            selector = f'.ant-menu-submenu-title:has-text("{item_text}")'
            if _USE_SYNC_PLAYWRIGHT:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(_get_executor(), lambda: page.locator(selector).first.click())
            else:
                await page.locator(selector).first.click()
            await asyncio.sleep(wait_after)
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state(
            {"ok": True, "message": f"{'Navigated to' if is_leaf else 'Expanded'} '{item_text}'"},
            ps,
            # Attach guide only when landing on a leaf page (actual content page)
            with_guide=is_leaf,
        )
    except Exception as e:
        return _err(f"nav_submenu failed: {e}")


# ---------------------------------------------------------------------------
# renliwo-specific: ant_select (Ant Design dropdown)
# ---------------------------------------------------------------------------

async def _action_ant_select(
    state: dict,
    page_id: str,
    label: str,
    value: str,
) -> ToolResponse:
    """Select a value from an Ant Design Select dropdown identified by its
    form-item label text.

    Steps:
    1. Click the .ant-select-selector inside the .ant-form-item matching label.
    2. Wait 400 ms for dropdown animation.
    3. Click the option with matching text in the visible dropdown.
    """
    label = (label or "").strip()
    value = (value or "").strip()
    if not label or not value:
        return _err("label and value are both required for ant_select")
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")
    try:
        selector_trigger = f'.ant-form-item:has-text("{label}") .ant-select-selector'
        option_selector = (
            f'.ant-select-dropdown:not(.ant-select-dropdown-hidden) '
            f'.ant-select-item-option:has-text("{value}")'
        )
        if _USE_SYNC_PLAYWRIGHT:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _get_executor(), lambda: page.locator(selector_trigger).first.click()
            )
            await asyncio.sleep(0.5)
            await loop.run_in_executor(
                _get_executor(), lambda: page.click(option_selector)
            )
        else:
            await page.locator(selector_trigger).first.click()
            await asyncio.sleep(0.4)
            await page.click(option_selector)
        _touch_activity(state)
        ps = await _page_state(state, page_id)
        return _with_page_state(
            {"ok": True, "message": f"Selected '{value}' in '{label}'"}, ps
        )
    except Exception as e:
        return _err(f"ant_select failed: {e}. "
                    "If the label is ambiguous, use action='snapshot' to find the correct "
                    "selector and use action='click' + action='click' manually.")


# ---------------------------------------------------------------------------
# export (封装导出 + 自动保存，绕过 OS Save-As 弹窗)
# ---------------------------------------------------------------------------

async def _action_export(
    state: dict,
    page_id: str,
    btn_text: str = "",
    selector: str = "",
    save_to: str = "",
    timeout: float = 30.0,
) -> ToolResponse:
    """Click an export/download button and intercept the file download via
    Playwright's expect_download() so the OS "Save As" dialog never appears.

    Works for buttons like:
      查询导出 / 批量导出 / 常规查询导出 / 查询导出（统计版）/ 导出 …

    For pages that use async export (aysnExport API), the button click still
    succeeds but no download event fires — in that case the function returns
    ok=True with async_export=True and instructs the caller to check
    导出中心 → 异步导出记录.

    Args:
        btn_text: Button text to click (e.g. "查询导出"). Either btn_text or
                  selector must be provided.
        selector: CSS selector for the export button (alternative to btn_text).
        save_to:  Directory or full path to save the file.  Defaults to the
                  workspace browser/ directory.
        timeout:  Max seconds to wait for the download to start (default 30).
    """
    page = _get_page(state, page_id)
    if not page:
        return _err(f"Page '{page_id}' not found")

    btn_text = (btn_text or "").strip()
    selector = (selector or "").strip()
    if not btn_text and not selector:
        return _err("btn_text or selector required for export")

    # Resolve save directory — default to ~/Desktop so downloaded files are
    # immediately visible to the user on any macOS machine.
    import os as _os
    if save_to and save_to.strip():
        save_dir = _os.path.expanduser(save_to.strip())
    else:
        save_dir = _os.path.expanduser("~/Desktop")
    from pathlib import Path as _Path
    _Path(save_dir).mkdir(parents=True, exist_ok=True)

    try:
        ms = int(timeout * 1000)

        if _USE_SYNC_PLAYWRIGHT:
            # Sync path: use page.expect_download() context manager in executor
            loop = asyncio.get_event_loop()

            def _do_sync():
                with page.expect_download(timeout=ms) as dl_info:
                    if btn_text:
                        # JS click to bypass invisible modal overlays
                        page.evaluate(
                            f"Array.from(document.querySelectorAll('button'))"
                            f".find(b=>b.innerText.trim()==='{btn_text}')?.click()"
                        )
                    else:
                        page.locator(selector).first.click()
                download = dl_info.value
                fname = download.suggested_filename or "export_file"
                dest = str(_Path(save_dir) / fname)
                download.save_as(dest)
                return dest, fname

            try:
                dest, fname = await loop.run_in_executor(_get_executor(), _do_sync)
            except Exception as e:
                if "Timeout" in type(e).__name__ or "timeout" in str(e).lower():
                    ps = await _page_state(state, page_id)
                    return _with_page_state({
                        "ok": True,
                        "async_export": True,
                        "message": (
                            "No download event — this page uses async export. "
                            "Navigate to 综合管理 → 导出中心 → 异步导出记录 "
                            "and wait for status 文件已生成, then click 下载."
                        ),
                    }, ps)
                raise

        else:
            # Async path
            try:
                async with page.expect_download(timeout=ms) as dl_info:
                    if btn_text:
                        await page.evaluate(
                            f"Array.from(document.querySelectorAll('button'))"
                            f".find(b=>b.innerText.trim()==='{btn_text}')?.click()"
                        )
                    else:
                        await page.locator(selector).first.click()
                download = await dl_info.value
                fname = download.suggested_filename or "export_file"
                dest = str(_Path(save_dir) / fname)
                await download.save_as(dest)
            except Exception as e:
                if "Timeout" in type(e).__name__ or "timeout" in str(e).lower():
                    ps = await _page_state(state, page_id)
                    return _with_page_state({
                        "ok": True,
                        "async_export": True,
                        "message": (
                            "No download event — this page uses async export. "
                            "Navigate to 综合管理 → 导出中心 → 异步导出记录 "
                            "and wait for status 文件已生成, then click 下载."
                        ),
                    }, ps)
                raise

        _touch_activity(state)
        ps = await _page_state(state, page_id)
        import os as _os
        size = _os.path.getsize(dest) if _os.path.exists(dest) else 0
        size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.2f} MB"
        return _with_page_state({
            "ok": True,
            "async_export": False,
            "file": dest,
            "filename": fname,
            "size": size_str,
            "message": f"Downloaded '{fname}' ({size_str}) → {dest}",
        }, ps, with_guide=True)

    except Exception as e:
        return _err(f"export failed: {e}")


# ---------------------------------------------------------------------------
# tabs (list / new / close / select)
# ---------------------------------------------------------------------------

async def _action_tabs(
    state: dict,
    page_id: str,
    tab_action: str,
    index: int = -1,
) -> ToolResponse:
    tab_action = (tab_action or "").strip().lower()
    pages = state["pages"]
    page_ids = list(pages.keys())
    if tab_action == "list":
        return _ok(tabs=page_ids, count=len(page_ids),
                   current=state.get("current_page_id"))
    if tab_action == "new":
        ctx = _get_context(state)
        if not ctx:
            ok = await _ensure_browser(state)
            if not ok:
                return _err(state.get("_last_browser_error") or "Browser not started")
        try:
            if _USE_SYNC_PLAYWRIGHT:
                page = await _run_sync(_get_context(state).new_page)
            else:
                page = await _get_context(state).new_page()
            new_id = _next_page_id(state)
            _register_page(state, page, new_id)
            state["current_page_id"] = new_id
            return _ok(page_id=new_id, tabs=list(state["pages"].keys()))
        except Exception as e:
            return _err(f"New tab failed: {e}")
    if tab_action == "close":
        target = page_ids[index] if 0 <= index < len(page_ids) else page_id
        p = _get_page(state, target)
        if p:
            try:
                if _USE_SYNC_PLAYWRIGHT:
                    await _run_sync(p.close)
                else:
                    await p.close()
            except Exception:
                pass
            del state["pages"][target]
            for key in ("refs", "refs_frame", "console_logs", "pending_dialogs", "pending_file_choosers"):
                state[key].pop(target, None)
            if state.get("current_page_id") == target:
                remaining = list(state["pages"].keys())
                state["current_page_id"] = remaining[0] if remaining else None
        return _ok(message=f"Closed tab '{target}'")
    if tab_action == "select":
        target = page_ids[index] if 0 <= index < len(page_ids) else page_id
        state["current_page_id"] = target
        return _ok(message=f"Active page set to '{target}'", page_id=target)
    return _err(f"Unknown tab_action: {tab_action}. Valid: list, new, close, select")


# ---------------------------------------------------------------------------
# Public tool function
# ---------------------------------------------------------------------------

async def renliwo_browser(
    action: str,
    url: str = "",
    page_id: str = "default",
    selector: str = "",
    ref: str = "",
    text: str = "",
    code: str = "",
    path: str = "",
    filename: str = "",
    key: str = "",
    paths_json: str = "",
    menu_text: str = "",
    item_text: str = "",
    label: str = "",
    value: str = "",
    btn_text: str = "",
    save_to: str = "",
    submit: bool = False,
    slowly: bool = False,
    double_click: bool = False,
    full_page: bool = False,
    accept: bool = True,
    prompt_text: str = "",
    is_leaf: bool = False,
    wait_after: float = 0.0,
    wait_time: float = 0.0,
    text_gone: str = "",
    timeout: float = 15.0,
    tab_action: str = "",
    index: int = -1,
    frame_selector: str = "",
    headed: bool = False,
) -> ToolResponse:
    """Playwright browser automation tool exclusively for renliwo internal HR platform.

    ⚠️  Only use this tool for renliwo URLs (ereference-v-uat.renliwo.com).
    ⚠️  After login, NEVER navigate with action='navigate' (will go back to login).
        Use nav_menu → nav_submenu → nav_submenu(is_leaf=True) to reach pages.

    ── 典型操作节奏 ─────────────────────────────────────────────────────────
    1. action='start'                  — 启动浏览器（已启动则跳过）
    2. action='open'                   — 打开登录页（url 留空即可）
    3. action='login'                  — 自动登录（已登录则跳过）
    4. action='snapshot'               — 查看当前页结构 + 获取 refs
    5. action='nav_menu', menu_text=X  — 点顶部模块，观察 page.active_nav
    6. action='nav_submenu', item_text=X              — 展开侧边 submenu 组
    7. action='nav_submenu', item_text=X, is_leaf=True — 点叶子页面
    8. action='snapshot'               — 确认表格列名、筛选字段 ref
    9. action='ant_select' / 'type' / 'click' — 设置筛选条件
   10. action='click', selector='button:has-text("查")' — 点查询
   11. action='wait_for', text_gone='加载中' — 等结果
   12. action='export', btn_text='查询导出'  — 导出并自动保存文件（推荐）

    如当前页面结构不清楚，调用 action='guide' 可按当前 URL 或传入 url/route
    获取 Renliwo 页面结构精简手册；工具会在进入叶子页面和导出后自动附带 guide。

    ── 导出操作（重要）────────────────────────────────────────────────────────
    ⚠️  导出必须使用 action='export'，禁止用 action='click' 点导出按钮！
    原因：直接 click 会触发 macOS/OS 原生 Save As 弹窗卡住流程；
    action='export' 在网络层提前拦截下载流，弹窗永远不会出现。

    两种导出行为（系统自动处理，AI 无需区分）：
    • 直接下载（大多数页面）：文件立即保存到 save_to 目录，返回 file 路径。
    • 异步导出（少数页面）：返回 async_export=True，提示去导出中心下载。
      已知异步导出页面：到款认款表、专职渠道费账单、专职费用结算财务。

    用法示例：
      action='export', btn_text='查询导出'               # 保存到默认工作目录
      action='export', btn_text='批量导出', save_to='~/Desktop'
      action='export', btn_text='查询导出（统计版）'

    ── 每次 action 返回值 ────────────────────────────────────────────────────
    成功时返回 page 快照：
      page.url           — 当前 URL
      page.active_nav    — 顶部激活模块
      page.active_tab    — 当前激活 Tab
      page.headings      — 页面标题/面包屑
      page.table_headers — 表格列名
      page.alerts        — toast / 错误提示
      page.pagination    — 分页信息（如「共 123 条」）

    ── 登录 SOP ─────────────────────────────────────────────────────────────
    凭证从 config.json > plugins > renliwo 读取，无需手写。
    action='login' 会自动判断是否已登录，已登录则跳过。

    ── Ant Design Select ────────────────────────────────────────────────────
    action='ant_select', label='字段标签文字', value='选项文字'
    例：action='ant_select', label='实名认证验证状态', value='成功'

    Args:
        action: Required. One of:
            start       — 启动浏览器（headless）
            stop        — 关闭浏览器
            open        — 打开页面（url 默认登录页）
            login       — 自动登录（已登录跳过）
            snapshot    — ARIA 快照，获取 refs 用于 click/type
            click       — 点击元素（ref 或 selector）
            type        — 输入文字（ref 或 selector）
            wait_for    — 等待文字出现/消失，或等待指定秒数
            evaluate    — 执行 JS 返回结果
            screenshot  — 截图（path 为空则返回 base64）
            press_key   — 按键（如 Enter, Escape）
            file_upload — 上传文件（先 click 触发文件选择器）
            handle_dialog — 处理弹窗（accept/dismiss）
            nav_menu    — 点击顶部导航模块（menu_text）
            nav_submenu — 展开侧边菜单组 or 点叶子页面（item_text, is_leaf）
            ant_select  — Ant Design 下拉框选值（label + value）
            export      — ⭐ 点击导出按钮并自动保存文件（btn_text + save_to）
            guide       — 获取当前页面或指定 url/route 的 Renliwo 页面结构手册摘要
            tabs        — 多标签管理（tab_action: list/new/close/select）
            status      — 查看浏览器状态
            cookies_clear — 清除 cookies（强制重新登录）
        url: 目标 URL，action=open 时使用（默认登录页）；action=guide 时也可传完整 URL 或 #/route。
        page_id: 页面标识符，默认 "default"。多标签时指定。
        selector: CSS 选择器，用于 click/type/export。
        ref: ARIA snapshot 返回的 ref，优先于 selector。
        text: 输入文字，action=type 必填；action=wait_for 时等待该文字出现。
        code: JavaScript，action=evaluate 必填。
        path: 截图保存路径，action=screenshot 时使用。
        filename: snapshot 保存文件名。
        key: 按键名称，action=press_key 必填（如 "Enter"）。
        paths_json: JSON 数组，文件路径，action=file_upload 必填。
        menu_text: 顶部导航模块名，action=nav_menu 必填。
        item_text: 侧边菜单项名，action=nav_submenu 必填。
        label: 表单字段标签，action=ant_select 必填。
        value: 选项文字，action=ant_select 必填。
        btn_text: 导出按钮文字，action=export 必填（如 "查询导出"/"批量导出"）。
        save_to: 文件保存目录，action=export 可选（默认工作目录/browser/）。
        submit: type 后是否按 Enter 提交，默认 False。
        slowly: 是否逐字符输入（处理有输入监听的字段），默认 False。
        double_click: 是否双击，action=click 时使用。
        full_page: 是否全页截图，默认 False。
        accept: handle_dialog 时是否接受，默认 True。
        prompt_text: handle_dialog 的输入文字。
        is_leaf: nav_submenu 时是否为叶子页面（True=点击跳转，False=展开组）。
        wait_after: click / nav_menu / nav_submenu 后额外等待秒数。
        wait_time: action=wait_for 时固定等待秒数。
        text_gone: action=wait_for 时等待该文字消失。
        timeout: wait_for / export 最大等待秒数，默认 15。
        tab_action: tabs 子操作：list / new / close / select。
        index: tabs 操作的标签序号（0-based）。
        frame_selector: iframe 选择器（在 iframe 内操作时指定）。
        headed: action=start 时是否显示浏览器窗口（默认 False，强制 headless）。
    """
    from ...config.context import get_current_workspace_dir as _get_cwd

    _cwd = _get_cwd()
    _ws_id = _cwd.name if _cwd else "default"
    _ws_dir = str(_cwd) if _cwd else ""
    state = _get_workspace_state(_ws_id, _ws_dir)

    action = (action or "").strip().lower()
    if not action:
        return _err("action required")

    # Resolve page_id
    page_id = (page_id or "default").strip() or "default"
    current = state.get("current_page_id")
    pages = state.get("pages") or {}
    if page_id == "default" and current and current in pages:
        page_id = current

    _touch_activity(state)

    try:
        if action == "start":
            return await _action_start(state, headed=headed)

        if action == "stop":
            return await _action_stop(state)

        if action == "status":
            return await _action_status(state)

        if action == "cookies_clear":
            return await _action_cookies_clear(state)

        if action == "guide":
            return _guide_for_current_page(state, page_id, url)

        if action == "open":
            return await _action_open(state, url, page_id)

        if action == "login":
            # Auto-ensure browser + page exist
            pid = await _ensure_page(state)
            if pid is None:
                return _err(state.get("_last_browser_error") or "Browser not started")
            if page_id == "default" or page_id not in state["pages"]:
                page_id = pid
            return await _action_login(state, page_id)

        if action == "snapshot":
            if not _is_browser_running(state):
                return _err("Browser not running. Call action='start' first.")
            if page_id not in state["pages"]:
                return _err(f"Page '{page_id}' not found. Call action='open' first.")
            return await _action_snapshot(state, page_id, filename or path)

        if action == "click":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_click(
                state, page_id, selector, ref, wait_after, double_click, frame_selector
            )

        if action == "type":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_type(
                state, page_id, selector, ref, text, submit, slowly, frame_selector
            )

        if action == "wait_for":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_wait_for(state, page_id, wait_time, text, text_gone, timeout)

        if action == "evaluate":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_evaluate(state, page_id, code, ref, frame_selector)

        if action == "screenshot":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_screenshot(state, page_id, path or filename, full_page)

        if action == "press_key":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_press_key(state, page_id, key)

        if action == "file_upload":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_file_upload(state, page_id, paths_json)

        if action == "handle_dialog":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_handle_dialog(state, page_id, accept, prompt_text)

        if action == "nav_menu":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_nav_menu(state, page_id, menu_text, wait_after or 1.5)

        if action == "nav_submenu":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_nav_submenu(
                state, page_id, item_text, is_leaf, wait_after or (1.0 if is_leaf else 0.8)
            )

        if action == "ant_select":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_ant_select(state, page_id, label, value)

        if action == "export":
            if not _is_browser_running(state):
                return _err("Browser not running.")
            return await _action_export(
                state, page_id,
                btn_text=btn_text or text,
                selector=selector,
                save_to=save_to or path,
                timeout=timeout if timeout != 15.0 else 30.0,
            )

        if action == "tabs":
            return await _action_tabs(state, page_id, tab_action, index)

        return _err(
            f"Unknown action: '{action}'. "
            "Valid: start, stop, open, login, snapshot, click, type, wait_for, "
            "evaluate, screenshot, press_key, file_upload, handle_dialog, "
            "nav_menu, nav_submenu, ant_select, export, guide, tabs, status, cookies_clear"
        )
    except Exception as e:
        logger.error("renliwo_browser error: %s", e, exc_info=True)
        return _err(str(e))

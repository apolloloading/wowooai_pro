# -*- coding: utf-8 -*-
"""Desktop application lifecycle / window-focus tool."""

import json
import shlex
import subprocess
import sys
from typing import Any, List, Optional

from agentscope.message import TextBlock
from agentscope.tool import ToolResponse


_SUPPORTED_ACTIONS = (
    "launch",
    "activate",
    "list_windows",
    "focus_window",
    "quit",
)


def _tool_error(msg: str, **extra: Any) -> ToolResponse:
    payload = {"ok": False, "error": msg}
    payload.update(extra)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=json.dumps(payload, ensure_ascii=False, indent=2),
            ),
        ],
    )


def _tool_ok(action: str, **fields: Any) -> ToolResponse:
    payload: dict[str, Any] = {"ok": True, "action": action}
    payload.update(fields)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=json.dumps(payload, ensure_ascii=False, indent=2),
            ),
        ],
    )


def _run(cmd: List[str], timeout: float = 15.0) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _osa_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _launch_mac(target: str) -> ToolResponse:
    cmd = ["open", "-a", target] if not target.endswith(".app") and "/" not in target else ["open", target]
    r = _run(cmd)
    if r.returncode != 0:
        return _tool_error(
            f"open failed: {(r.stderr or '').strip() or r.stdout.strip()}",
        )
    return _tool_ok("launch", target=target)


def _launch_win(target: str) -> ToolResponse:
    ps = f'Start-Process -FilePath {shlex.quote(target)}'
    r = _run(["powershell", "-NoProfile", "-Command", ps])
    if r.returncode != 0:
        return _tool_error(
            f"Start-Process failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("launch", target=target)


def _activate_mac(name: str) -> ToolResponse:
    script = f'tell application "{_osa_escape(name)}" to activate'
    r = _run(["osascript", "-e", script])
    if r.returncode != 0:
        return _tool_error(
            f"osascript activate failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("activate", target=name)


def _activate_win(name: str) -> ToolResponse:
    vb = (
        "Add-Type -AssemblyName Microsoft.VisualBasic; "
        f"[Microsoft.VisualBasic.Interaction]::AppActivate({shlex.quote(name)})"
    )
    r = _run(["powershell", "-NoProfile", "-Command", vb])
    if r.returncode != 0:
        return _tool_error(
            f"AppActivate failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("activate", target=name)


def _list_windows_mac() -> ToolResponse:
    script = (
        'set output to ""\n'
        'tell application "System Events"\n'
        '  repeat with p in (every process whose visible is true)\n'
        '    try\n'
        '      set wcount to count of windows of p\n'
        '    on error\n'
        '      set wcount to 0\n'
        '    end try\n'
        '    if wcount > 0 then\n'
        '      set pname to name of p\n'
        '      repeat with w in (every window of p)\n'
        '        try\n'
        '          set wname to name of w\n'
        '        on error\n'
        '          set wname to ""\n'
        '        end try\n'
        '        set output to output & pname & "\\t" & wname & "\\n"\n'
        '      end repeat\n'
        '    end if\n'
        '  end repeat\n'
        'end tell\n'
        'return output'
    )
    r = _run(["osascript", "-e", script])
    if r.returncode != 0:
        return _tool_error(
            f"osascript list_windows failed: "
            f"{(r.stderr or '').strip()}",
        )
    raw = (r.stdout or "").strip()
    windows = []
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        proc, _, title = line.partition("\t")
        windows.append({"app": proc.strip(), "title": title.strip()})
    return _tool_ok("list_windows", windows=windows)


def _list_windows_win() -> ToolResponse:
    ps = (
        "Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | "
        "Select-Object -Property ProcessName, MainWindowTitle | "
        "ConvertTo-Json -Compress"
    )
    r = _run(["powershell", "-NoProfile", "-Command", ps])
    if r.returncode != 0:
        return _tool_error(
            f"Get-Process failed: {(r.stderr or '').strip()}",
        )
    raw = (r.stdout or "").strip() or "[]"
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            parsed = [parsed]
    except json.JSONDecodeError:
        parsed = []
    return _tool_ok("list_windows", windows=parsed)


def _focus_window_mac(title_substring: str) -> ToolResponse:
    script = (
        'tell application "System Events"\n'
        '  set matchedProc to ""\n'
        '  repeat with p in (every process whose visible is true)\n'
        '    repeat with w in (every window of p)\n'
        f'      if name of w contains "{_osa_escape(title_substring)}" then\n'
        '        set frontmost of p to true\n'
        '        perform action "AXRaise" of w\n'
        '        set matchedProc to name of p\n'
        '        exit repeat\n'
        '      end if\n'
        '    end repeat\n'
        '    if matchedProc is not "" then exit repeat\n'
        '  end repeat\n'
        '  return matchedProc\n'
        'end tell'
    )
    r = _run(["osascript", "-e", script])
    if r.returncode != 0:
        return _tool_error(
            f"focus_window failed: {(r.stderr or '').strip()}",
        )
    matched = (r.stdout or "").strip()
    if not matched:
        return _tool_error(
            f"no visible window title contains '{title_substring}'",
        )
    return _tool_ok("focus_window", matched_app=matched)


def _focus_window_win(title_substring: str) -> ToolResponse:
    vb = (
        "Add-Type -AssemblyName Microsoft.VisualBasic; "
        f"[Microsoft.VisualBasic.Interaction]::AppActivate("
        f"{shlex.quote(title_substring)})"
    )
    r = _run(["powershell", "-NoProfile", "-Command", vb])
    if r.returncode != 0:
        return _tool_error(
            f"AppActivate failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("focus_window", matched_app=title_substring)


def _quit_mac(name: str) -> ToolResponse:
    script = f'tell application "{_osa_escape(name)}" to quit'
    r = _run(["osascript", "-e", script])
    if r.returncode != 0:
        return _tool_error(
            f"osascript quit failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("quit", target=name)


def _quit_win(name: str) -> ToolResponse:
    proc = name
    if proc.lower().endswith(".exe"):
        proc = proc[:-4]
    ps = (
        f"Get-Process -Name {shlex.quote(proc)} -ErrorAction SilentlyContinue "
        "| ForEach-Object { $_.CloseMainWindow() | Out-Null }"
    )
    r = _run(["powershell", "-NoProfile", "-Command", ps])
    if r.returncode != 0:
        return _tool_error(
            f"CloseMainWindow failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("quit", target=name)


async def desktop_app(
    action: str,
    name_or_path: Optional[str] = None,
    name: Optional[str] = None,
    title_substring: Optional[str] = None,
) -> ToolResponse:
    """Manage native desktop application lifecycle and window focus.

    Use this tool to start an application, bring it to the foreground,
    list visible windows, or quit an application. After ``launch`` or
    ``activate`` always follow up with ``desktop_screenshot`` to confirm
    the expected UI is on screen before issuing ``desktop_input`` actions.

    Action reference (one per call):

    - ``launch``: start an app. On macOS pass the app name (``"Calculator"``,
      ``"Numbers"``) or a ``.app`` path; uses ``open -a``. On Windows pass
      the executable name (``"notepad"``, ``"calc.exe"``) or full path; uses
      ``Start-Process``.
    - ``activate``: bring an already-running app to the foreground by name.
      macOS uses AppleScript ``tell application ... to activate``; Windows
      uses ``AppActivate``.
    - ``list_windows``: enumerate visible windows. macOS returns the raw
      AppleScript output. Windows returns a JSON list of
      ``{ProcessName, MainWindowTitle}``.
    - ``focus_window``: focus the first visible window whose title contains
      ``title_substring`` (case-sensitive on macOS).
    - ``quit``: ask the app to quit gracefully (macOS AppleScript quit /
      Windows ``CloseMainWindow``).

    Args:
        action (`str`):
            One of ``launch``, ``activate``, ``list_windows``,
            ``focus_window``, ``quit``.
        name_or_path (`Optional[str]`):
            App name or path for ``launch``.
        name (`Optional[str]`):
            App name for ``activate`` / ``quit``.
        title_substring (`Optional[str]`):
            Substring to match in window titles for ``focus_window``.

    Returns:
        `ToolResponse`:
            JSON with ``ok``, ``action``, and action-specific fields,
            or ``error``.
    """
    act = (action or "").strip()
    if act not in _SUPPORTED_ACTIONS:
        return _tool_error(
            f"unsupported action '{act}'. "
            f"Supported: {', '.join(_SUPPORTED_ACTIONS)}",
        )

    is_mac = sys.platform == "darwin"
    is_win = sys.platform == "win32"
    if not (is_mac or is_win):
        return _tool_error(
            f"desktop_app currently supports macOS and Windows only "
            f"(sys.platform={sys.platform})",
        )

    try:
        if act == "launch":
            target = (name_or_path or "").strip()
            if not target:
                return _tool_error("launch requires 'name_or_path'")
            return _launch_mac(target) if is_mac else _launch_win(target)

        if act == "activate":
            target = (name or "").strip()
            if not target:
                return _tool_error("activate requires 'name'")
            return _activate_mac(target) if is_mac else _activate_win(target)

        if act == "list_windows":
            return _list_windows_mac() if is_mac else _list_windows_win()

        if act == "focus_window":
            sub = (title_substring or "").strip()
            if not sub:
                return _tool_error(
                    "focus_window requires 'title_substring'",
                )
            return (
                _focus_window_mac(sub) if is_mac else _focus_window_win(sub)
            )

        if act == "quit":
            target = (name or "").strip()
            if not target:
                return _tool_error("quit requires 'name'")
            return _quit_mac(target) if is_mac else _quit_win(target)
    except subprocess.TimeoutExpired as e:
        return _tool_error(f"desktop_app '{act}' timed out: {e!s}")
    except Exception as e:
        return _tool_error(f"desktop_app '{act}' failed: {e!s}")

    return _tool_error(f"unhandled action '{act}'")

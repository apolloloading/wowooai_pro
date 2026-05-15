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
    "ensure_frontmost",
    "zoom_window",
    "quit",
)

_TRAY_KEEP_WIN = {
    "DingTalk",
    "WeChat",
    "WeChatAppEx",
    "Feishu",
    "Lark",
    "wxwork",
    "WXWork",
    "Outlook",
    "Teams",
    "ms-teams",
    "Slack",
}


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
        '    set pname to name of p\n'
        '    if wcount > 0 then\n'
        '      repeat with w in (every window of p)\n'
        '        try\n'
        '          set wname to name of w\n'
        '        on error\n'
        '          set wname to ""\n'
        '        end try\n'
        '        set output to output & pname & "\\t" & wname & "\\t0\\n"\n'
        '      end repeat\n'
        '    else\n'
        '      set output to output & pname & "\\t\\t1\\n"\n'
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
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        proc, title, tray = parts[0], parts[1], parts[2]
        windows.append({
            "app": proc.strip(),
            "title": title.strip(),
            "tray": tray.strip() == "1",
        })
    return _tool_ok("list_windows", windows=windows)


def _list_windows_win() -> ToolResponse:
    ps = (
        "Get-Process | Where-Object { $_.Id -ne $PID } | "
        "Select-Object -Property ProcessName, "
        "@{N='MainWindowTitle';E={ $_.MainWindowTitle }}, "
        "@{N='Tray';E={ [string]::IsNullOrEmpty($_.MainWindowTitle) }} | "
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
    windows = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        name = (item.get("ProcessName") or "").strip()
        title = (item.get("MainWindowTitle") or "").strip()
        tray = bool(item.get("Tray"))
        if tray and name not in _TRAY_KEEP_WIN:
            continue
        windows.append({
            "app": name,
            "title": title,
            "tray": tray,
        })
    return _tool_ok("list_windows", windows=windows)


def _focus_window_mac(title_substring: str) -> ToolResponse:
    needle = _osa_escape(title_substring)
    script = (
        'tell application "System Events"\n'
        '  set matchedProc to ""\n'
        '  set matchedTitle to ""\n'
        '  repeat with p in (every process whose visible is true)\n'
        '    try\n'
        '      set wlist to every window of p\n'
        '    on error\n'
        '      set wlist to {}\n'
        '    end try\n'
        '    repeat with w in wlist\n'
        '      try\n'
        '        set wname to name of w\n'
        '      on error\n'
        '        set wname to ""\n'
        '      end try\n'
        '      if wname is not "" then\n'
        '        set hit to false\n'
        '        ignoring case\n'
        f'          if wname contains "{needle}" then set hit to true\n'
        '        end ignoring\n'
        '        if hit then\n'
        '          try\n'
        '            if value of attribute "AXMinimized" of w is true then '
        'set value of attribute "AXMinimized" of w to false\n'
        '          end try\n'
        '          set frontmost of p to true\n'
        '          try\n'
        '            perform action "AXRaise" of w\n'
        '          end try\n'
        '          set matchedProc to name of p\n'
        '          set matchedTitle to wname\n'
        '          exit repeat\n'
        '        end if\n'
        '      end if\n'
        '    end repeat\n'
        '    if matchedProc is not "" then exit repeat\n'
        '  end repeat\n'
        '  return matchedProc & "\\t" & matchedTitle\n'
        'end tell'
    )
    r = _run(["osascript", "-e", script])
    if r.returncode != 0:
        return _tool_error(
            f"focus_window failed: {(r.stderr or '').strip()}",
        )
    raw = (r.stdout or "").strip()
    proc, _, title = raw.partition("\t")
    proc = proc.strip()
    title = title.strip()
    if not proc:
        return _tool_error(
            f"no visible window title matches '{title_substring}' "
            f"(case-insensitive). For apps with untitled windows, use "
            f"'ensure_frontmost' with name=<AppName>.",
        )
    return _tool_ok(
        "focus_window",
        matched_app=proc,
        matched_title=title,
    )


_PS_FOCUS_WINDOW = r'''
param([Parameter(Mandatory=$true)][string]$Needle)
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class WowooWin {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr h, int n);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Auto)]
  public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
}
"@
$script:hits = New-Object System.Collections.ArrayList
$cb = [WowooWin+EnumProc]{
  param($h, $l)
  if ([WowooWin]::IsWindowVisible($h)) {
    $sb = New-Object System.Text.StringBuilder 512
    [WowooWin]::GetWindowText($h, $sb, 512) | Out-Null
    $t = $sb.ToString()
    if ($t -and $t.ToLower().Contains($Needle.ToLower())) {
      [void]$script:hits.Add(@{H=$h; T=$t})
    }
  }
  return $true
}
[WowooWin]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
if ($script:hits.Count -eq 0) { Write-Output "NOMATCH"; exit 0 }
$h = $script:hits[0].H
$t = $script:hits[0].T
if ([WowooWin]::IsIconic($h)) { [WowooWin]::ShowWindowAsync($h, 9) | Out-Null }
[WowooWin]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 200
$fg = [WowooWin]::GetForegroundWindow()
if ($fg -eq $h) { Write-Output ("OK`t" + $t) } else { Write-Output ("RACE`t" + $t) }
'''


def _focus_window_win(title_substring: str) -> ToolResponse:
    r = _run([
        "powershell", "-NoProfile", "-Command", _PS_FOCUS_WINDOW,
        "-Needle", title_substring,
    ])
    if r.returncode != 0:
        return _tool_error(
            f"focus_window failed: {(r.stderr or '').strip()}",
        )
    raw = (r.stdout or "").strip()
    if not raw:
        return _tool_error(
            f"focus_window returned no output for '{title_substring}'",
        )
    out = raw.splitlines()[-1].strip()
    if out == "NOMATCH":
        return _tool_error(
            f"no visible window title contains '{title_substring}'",
        )
    status, _, title = out.partition("\t")
    title = title.strip()
    if status == "RACE":
        return _tool_error(
            "Windows blocked SetForegroundWindow "
            "(LockSetForegroundWindow). Try ensure_frontmost which "
            "auto-retries.",
            matched_title=title,
        )
    if status != "OK":
        return _tool_error(f"focus_window unexpected output: {out}")
    return _tool_ok("focus_window", matched_title=title)


def _ensure_frontmost_mac(
    name: Optional[str],
    title_substring: Optional[str],
    timeout_ms: int,
) -> ToolResponse:
    import time as _t

    if name:
        _run([
            "osascript", "-e",
            f'tell application "{_osa_escape(name)}" to activate',
        ])

    deadline = _t.monotonic() + max(0.2, timeout_ms / 1000.0)
    last_err = ""
    while _t.monotonic() < deadline:
        if title_substring:
            res = _focus_window_mac(title_substring)
            payload = json.loads(res.content[0]["text"])
            if payload.get("ok"):
                _t.sleep(0.15)
                check = _run([
                    "osascript", "-e",
                    'tell application "System Events" to '
                    'return name of first process whose frontmost is true',
                ])
                front = (check.stdout or "").strip()
                if front and front == payload.get("matched_app"):
                    return _tool_ok(
                        "ensure_frontmost",
                        matched_app=front,
                        matched_title=payload.get("matched_title"),
                    )
                last_err = (
                    f"raised window of {payload.get('matched_app')} "
                    f"but frontmost is now '{front}'"
                )
            else:
                last_err = payload.get("error", "")
        else:
            check = _run([
                "osascript", "-e",
                'tell application "System Events" to '
                'return name of first process whose frontmost is true',
            ])
            front = (check.stdout or "").strip()
            if front and front.lower() == (name or "").lower():
                return _tool_ok("ensure_frontmost", matched_app=front)
            last_err = f"frontmost is '{front}', expected '{name}'"
        _t.sleep(0.1)

    return _tool_error(
        f"ensure_frontmost timed out after {timeout_ms}ms: {last_err}",
    )


def _ensure_frontmost_win(
    name: Optional[str],
    title_substring: Optional[str],
    timeout_ms: int,
) -> ToolResponse:
    import time as _t

    needle = title_substring or name or ""
    if not needle:
        return _tool_error(
            "ensure_frontmost requires name or title_substring",
        )

    deadline = _t.monotonic() + max(0.3, timeout_ms / 1000.0)
    last = None
    attempt = 0
    while _t.monotonic() < deadline:
        attempt += 1
        last = _focus_window_win(needle)
        payload = json.loads(last.content[0]["text"])
        if payload.get("ok"):
            return _tool_ok(
                "ensure_frontmost",
                matched_title=payload.get("matched_title"),
                attempts=attempt,
            )
        _t.sleep(0.2)

    err_msg = ""
    if last is not None:
        err_msg = json.loads(last.content[0]["text"]).get("error", "")
    return _tool_error(
        f"ensure_frontmost timed out: {err_msg or 'no attempts'}",
    )


def _zoom_window_mac(
    name: Optional[str],
    title_substring: Optional[str],
) -> ToolResponse:
    if title_substring:
        cond = (
            'first window whose name contains '
            f'"{_osa_escape(title_substring)}"'
        )
    else:
        cond = "front window"
    if name:
        app_clause = f'process "{_osa_escape(name)}"'
    else:
        app_clause = "(first process whose frontmost is true)"
    script = (
        f'tell application "System Events"\n'
        f'  tell {app_clause}\n'
        f'    set _w to {cond}\n'
        f'    try\n'
        f'      if value of attribute "AXMinimized" of _w is true then '
        f'set value of attribute "AXMinimized" of _w to false\n'
        f'    end try\n'
        f'    try\n'
        f'      if value of attribute "AXFullScreen" of _w is true then '
        f'set value of attribute "AXFullScreen" of _w to false\n'
        f'    end try\n'
        f'    set _btns to (every button of _w whose subrole is "AXZoomButton")\n'
        f'    if (count of _btns) is 0 then error "AXZoomButton not found"\n'
        f'    click item 1 of _btns\n'
        f'  end tell\n'
        f'end tell'
    )
    r = _run(["osascript", "-e", script])
    if r.returncode != 0:
        return _tool_error(
            f"zoom_window failed: {(r.stderr or '').strip()}",
        )
    return _tool_ok("zoom_window")


_PS_MAXIMIZE_WINDOW = r'''
param([Parameter(Mandatory=$true)][string]$Needle)
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class WowooWinMax {
  [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr h, int n);
  [DllImport("user32.dll", CharSet=CharSet.Auto)]
  public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
}
"@
$script:found = $false
$cb = [WowooWinMax+EnumProc]{
  param($h, $l)
  if ([WowooWinMax]::IsWindowVisible($h)) {
    $sb = New-Object System.Text.StringBuilder 512
    [WowooWinMax]::GetWindowText($h, $sb, 512) | Out-Null
    $t = $sb.ToString()
    if ($t -and $t.ToLower().Contains($Needle.ToLower())) {
      [WowooWinMax]::ShowWindowAsync($h, 3) | Out-Null
      $script:found = $true
      return $false
    }
  }
  return $true
}
[WowooWinMax]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
if ($script:found) { Write-Output "OK" } else { Write-Output "NOMATCH" }
'''


def _maximize_window_win(
    name: Optional[str],
    title_substring: Optional[str],
) -> ToolResponse:
    needle = title_substring or name or ""
    if not needle:
        return _tool_error(
            "zoom_window requires name or title_substring",
        )
    r = _run([
        "powershell", "-NoProfile", "-Command", _PS_MAXIMIZE_WINDOW,
        "-Needle", needle,
    ])
    if r.returncode != 0:
        return _tool_error(
            f"maximize_window failed: {(r.stderr or '').strip()}",
        )
    out = (r.stdout or "").strip().splitlines()[-1] if (r.stdout or "").strip() else ""
    if out != "OK":
        return _tool_error(
            f"no visible window title contains '{needle}'",
        )
    return _tool_ok("zoom_window")


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
    timeout_ms: int = 1500,
) -> ToolResponse:
    """Manage native desktop application lifecycle and window focus.

    Use this tool to start an application, bring it to the foreground,
    list visible windows, or quit an application. Before any
    ``desktop_input`` action prefer ``ensure_frontmost`` over bare
    ``focus_window`` — it auto-deminimizes, retries on Windows
    foreground races, and verifies the target is actually on top.
    After bringing a window forward, always follow up with
    ``desktop_screenshot`` to confirm the expected UI is visible.

    Action reference (one per call):

    - ``launch``: start an app. On macOS pass the app name
      (``"Calculator"``, ``"Numbers"``) or a ``.app`` path; uses
      ``open -a``. On Windows pass the executable name (``"notepad"``,
      ``"calc.exe"``) or full path; uses ``Start-Process``.
    - ``activate``: bring an already-running app to the foreground by
      name. macOS uses AppleScript ``tell application ... to
      activate``; Windows uses ``AppActivate``. Note: only switches
      processes, does **not** auto-restore minimized windows — use
      ``ensure_frontmost`` for that.
    - ``list_windows``: enumerate visible processes / windows. Each
      entry is ``{app, title, tray}``. ``tray=true`` means the app is
      running but has no visible window (e.g. DingTalk/WeChat
      minimized to system tray); call ``ensure_frontmost`` to surface
      a window.
    - ``focus_window``: focus the first visible window whose title
      contains ``title_substring``. macOS match is case-insensitive
      and auto-restores minimized windows. Windows verifies the
      foreground really switched and returns an error if
      ``LockSetForegroundWindow`` blocked the request.
    - ``ensure_frontmost``: composite atomic operation — activate the
      app (if ``name`` given), focus the matching window (if
      ``title_substring`` given), auto-deminimize, wait for animation,
      and verify the result. Retries on Windows foreground races up
      to ``timeout_ms`` (default 1500). Recommended over plain
      ``focus_window`` whenever the next step is a click/keystroke.
    - ``zoom_window``: **opt-in** maximize. macOS uses ``zoomed``
      (green-button equivalent) and explicitly stays out of fullscreen
      Space; Windows uses ``SW_MAXIMIZE``. Calling this **invalidates
      any previously estimated coordinates** — you must take a fresh
      ``desktop_screenshot`` before any subsequent ``desktop_input``.
      Use only when the current window is too small to see the target
      control.
    - ``quit``: ask the app to quit gracefully (macOS AppleScript quit
      / Windows ``CloseMainWindow``).

    Args:
        action (`str`):
            One of ``launch``, ``activate``, ``list_windows``,
            ``focus_window``, ``ensure_frontmost``, ``zoom_window``,
            ``quit``.
        name_or_path (`Optional[str]`):
            App name or path for ``launch``.
        name (`Optional[str]`):
            App name for ``activate`` / ``ensure_frontmost`` /
            ``zoom_window`` / ``quit``.
        title_substring (`Optional[str]`):
            Substring to match in window titles for ``focus_window``
            / ``ensure_frontmost`` / ``zoom_window``.
        timeout_ms (`int`):
            Max wait for ``ensure_frontmost`` (default 1500ms).

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

        if act == "ensure_frontmost":
            nm = (name or "").strip() or None
            sub = (title_substring or "").strip() or None
            if not (nm or sub):
                return _tool_error(
                    "ensure_frontmost requires 'name' and/or "
                    "'title_substring'",
                )
            return (
                _ensure_frontmost_mac(nm, sub, int(timeout_ms))
                if is_mac
                else _ensure_frontmost_win(nm, sub, int(timeout_ms))
            )

        if act == "zoom_window":
            nm = (name or "").strip() or None
            sub = (title_substring or "").strip() or None
            if not (nm or sub):
                return _tool_error(
                    "zoom_window requires 'name' and/or "
                    "'title_substring'",
                )
            return (
                _zoom_window_mac(nm, sub)
                if is_mac
                else _maximize_window_win(nm, sub)
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

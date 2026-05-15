---
name: desktop_control
description: "Use this skill when the user needs to operate native desktop apps (Excel, DingTalk, internal ERP, IM clients, etc.) with clicks, keystrokes and screenshot verification. Combine desktop_app (launch/focus/list/quit), desktop_screenshot (see), and desktop_input (mouse/keyboard) into a 'screenshot → locate → act → screenshot' loop. For web tasks always use browser_use, not this skill."
metadata:
  builtin_skill_version: "1.0"
  wowooai:
    emoji: "🖥️"
    requires: {}
---

# Desktop App Control

Lets the Agent operate native macOS / Windows apps the way a human does.

## When to use

- User asks to open a local file (e.g. `~/Desktop/foo.xlsx`) in its GUI app
- User asks to operate Excel, Numbers, Word, Pages, DingTalk, Feishu, WeCom, internal ERP / SAP / OA clients
- A web flow downloads a file and the next step must happen in a native app

## When NOT to use

- Anything doable on the web → use `browser_use`, not this skill
- Plain file read/write of Office/PDF → use the dedicated `xlsx` / `docx` / `pptx` / `pdf` skills; don't click the GUI
- Do not use for unsupervised macros / recording / bulk automation

## The three tools

- `desktop_app`: app lifecycle and window focus
  - `launch`, `activate`, `list_windows` (visible/tray), `focus_window`, `ensure_frontmost` **(composite, recommended)**, `zoom_window` (opt-in maximize), `quit`
- `desktop_screenshot`: existing capture tool
  - Whole screen by default; on macOS `capture_window=true` lets the user pick a window
- `desktop_input`: single mouse or keyboard action per call
  - `move_to` / `click` / `double_click` / `right_click` / `drag` / `type_text` / `press_keys` / `scroll` / `screen_size`

## Mandatory loop

Before any click or keystroke you **must** first bring the target window to a stable foreground state and screenshot; after any action you **must** screenshot again to verify:

1. `desktop_app(action="ensure_frontmost", name="<AppName>", title_substring="<title fragment>")` — auto-deminimizes, raises to front, retries on Windows foreground races, verifies
2. `desktop_screenshot` → see the current UI
3. Locate the target visually; call `desktop_input(action="screen_size")` to know real pixel dimensions
4. `desktop_input(action="click", x=..., y=...)` — one action per call
5. `desktop_screenshot` → confirm the result
6. Failure handling: stop after 2 consecutive failed attempts; report to the user

## Coordinates and DPI

`desktop_input` uses **screen pixels** with origin `(0, 0)` at the top-left of the primary monitor.

- On macOS Retina displays, the screenshot's pixel size is usually 2× the actual screen coordinates. Call `desktop_input(action="screen_size")` to get the real screen size (e.g. `1920x1080`); if the screenshot is `3840x2160`, divide by 2 before passing coordinates.
- Out-of-bounds coordinates are rejected (not clamped).

## Cross-platform keyboard

`press_keys` takes an ordered array of key names:

```json
{"action": "press_keys", "keys": ["cmd", "c"]}
```

- On Windows, `cmd` / `command` / `meta` are auto-mapped to `win`
- On Linux, they are mapped to `super`
- `option` is auto-mapped to `alt`
- You may always write macOS-style keys; the tool normalizes them

## Typical examples

> User: "Open `~/Desktop/associated_data.xlsx` and show me the first 10 rows."

1. Launch the app:
   ```json
   {"tool": "desktop_app", "action": "launch", "name_or_path": "Microsoft Excel"}
   ```
   Or let macOS pick the default app:
   ```json
   {"tool": "execute_shell_command", "command": "open ~/Desktop/associated_data.xlsx"}
   ```
2. Wait a moment, then screenshot:
   ```json
   {"tool": "desktop_screenshot"}
   ```
3. Use `view_image` on the screenshot and describe the first 10 rows in your reply.

> User: "Put the cursor in A1 and paste."

1. `desktop_app(action="ensure_frontmost", name="Microsoft Excel")` — bring Excel forward and verify
2. Screenshot to locate A1
3. `desktop_input(action="click", x=..., y=...)`
4. `desktop_input(action="press_keys", keys=["cmd", "v"])`
5. Screenshot to verify

## Recovery

- Click had no effect: `desktop_app(action="ensure_frontmost", name="<AppName>", title_substring="...")` — it auto-deminimizes, retries, and verifies; then re-screenshot and retry once
- Control drifted (window moved, DPI changed): re-screenshot; never reuse stale coordinates
- Window minimized to Dock / taskbar: `ensure_frontmost` automatically restores and brings it forward
- `list_windows` entry with `tray: true`: app is running but has no visible window (e.g. DingTalk/WeChat collapsed to tray) — call `ensure_frontmost` to surface a window
- Windows `focus_window` returns `LockSetForegroundWindow`-blocked error: `ensure_frontmost` will auto-retry until timeout (default 1500ms)
- After 2 consecutive failures: stop, tell the user what you see and where it's stuck; let the user decide
- Never silently dismiss system dialogs or close unsaved windows

## When to use `zoom_window`

**Do not** maximize windows by default. Only call `zoom_window` when:

- The current window is so small that key controls are clipped or cramped and the screenshot is unreadable
- A side panel is collapsed and you can't see the target chat / tab
- The user explicitly says to enlarge the window

After calling, **all previously estimated coordinates are invalid** — you must immediately take a fresh `desktop_screenshot` and re-locate. macOS uses the green-button (zoom) action and stays out of fullscreen Space; Windows uses `SW_MAXIMIZE`.

```json
{"action": "zoom_window", "name": "DingTalk", "title_substring": "Alice"}
```

## Notes

- One action per call; split batches into multiple calls
- Do not screenshot or read the clipboard via `desktop_input`; use `desktop_screenshot` and `read_file`
- First use on macOS may prompt Accessibility / Screen Recording permissions; if denied, the tool returns an error
- On Windows, key combos act on the foreground window — `activate` or `focus_window` first

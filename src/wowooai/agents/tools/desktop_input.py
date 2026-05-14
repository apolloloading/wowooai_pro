# -*- coding: utf-8 -*-
"""Desktop input injection tool (mouse / keyboard)."""

import json
import sys
from typing import Any, List, Optional

from agentscope.message import TextBlock
from agentscope.tool import ToolResponse


_SUPPORTED_ACTIONS = (
    "screen_size",
    "move_to",
    "click",
    "double_click",
    "right_click",
    "drag",
    "type_text",
    "press_keys",
    "scroll",
    "query",
)

_KEY_ALIAS_WIN = {
    "cmd": "win",
    "command": "win",
    "meta": "win",
    "option": "alt",
    "return": "enter",
}

_KEY_ALIAS_MAC = {
    "meta": "cmd",
    "command": "cmd",
    "win": "cmd",
    "option": "alt",
    "return": "enter",
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


def _load_pyautogui():
    try:
        import pyautogui  # type: ignore
    except ImportError as e:
        return None, (
            "desktop_input requires the 'pyautogui' package. "
            f"Install with: pip install pyautogui. Original error: {e!s}"
        )
    pyautogui.FAILSAFE = False
    return pyautogui, None


def _normalize_key(key: str) -> str:
    k = (key or "").strip().lower()
    if not k:
        return k
    if sys.platform == "win32":
        return _KEY_ALIAS_WIN.get(k, k)
    if sys.platform == "darwin":
        return _KEY_ALIAS_MAC.get(k, k)
    # linux: leave as-is, treat cmd/meta as super
    return {"cmd": "super", "command": "super", "meta": "super"}.get(k, k)


def _in_bounds(pyautogui, x: int, y: int) -> bool:
    w, h = pyautogui.size()
    return 0 <= x < w and 0 <= y < h


async def desktop_input(
    action: str,
    x: Optional[int] = None,
    y: Optional[int] = None,
    x2: Optional[int] = None,
    y2: Optional[int] = None,
    text: Optional[str] = None,
    keys: Optional[List[str]] = None,
    button: str = "left",
    clicks: int = 1,
    duration: float = 0.3,
    dy: int = 0,
) -> ToolResponse:
    """Inject a single mouse or keyboard action on the local desktop.

    Use this tool together with ``desktop_screenshot`` to operate native
    apps: first take a screenshot, decide where to click or what to type
    from the image, call this tool to perform exactly one action, then
    take another screenshot to verify the result. Coordinates are in
    screen pixels with origin at the top-left of the primary monitor.

    Action reference (one per call):

    - ``screen_size``: return primary-monitor width/height in pixels.
      No other args.
    - ``move_to``: move the mouse cursor to (x, y).
    - ``click``: click at (x, y). ``button`` is ``"left"`` / ``"right"`` /
      ``"middle"``. ``clicks`` defaults to 1.
    - ``double_click``: double-click at (x, y).
    - ``right_click``: right-click at (x, y).
    - ``drag``: press at (x, y), drag to (x2, y2) over ``duration`` seconds.
    - ``type_text``: type the literal characters in ``text``.
    - ``press_keys``: press a key combination, e.g. ``["cmd", "c"]``.
      ``cmd`` / ``command`` / ``meta`` is auto-mapped to ``win`` on Windows
      and ``super`` on Linux. ``option`` is auto-mapped to ``alt``.
    - ``scroll``: scroll by ``dy`` clicks (positive=up) at (x, y). If x/y
      omitted, scrolls at current cursor position.
    - ``query``: reserved for phase-2 structured element lookup
      (returns ``not_implemented`` today).

    Coordinates that fall outside the screen return an error rather
    than being clamped, so the caller is forced to re-evaluate.

    Args:
        action (`str`):
            One of ``screen_size``, ``move_to``, ``click``,
            ``double_click``, ``right_click``, ``drag``, ``type_text``,
            ``press_keys``, ``scroll``, ``query``.
        x (`Optional[int]`):
            X coordinate (pixels). Required for pointer actions.
        y (`Optional[int]`):
            Y coordinate (pixels). Required for pointer actions.
        x2 (`Optional[int]`):
            Destination X for ``drag``.
        y2 (`Optional[int]`):
            Destination Y for ``drag``.
        text (`Optional[str]`):
            Literal text to type for ``type_text``.
        keys (`Optional[List[str]]`):
            Ordered list of keys for ``press_keys``.
        button (`str`):
            ``left`` / ``right`` / ``middle`` for ``click``.
        clicks (`int`):
            Number of clicks for ``click``.
        duration (`float`):
            Drag duration in seconds.
        dy (`int`):
            Scroll amount (positive=up) for ``scroll``.

    Returns:
        `ToolResponse`:
            JSON with ``ok``, ``action``, and action-specific fields
            (``screen_size``, ``mouse_pos_after``, etc.) or ``error``.
    """
    act = (action or "").strip()
    if act not in _SUPPORTED_ACTIONS:
        return _tool_error(
            f"unsupported action '{act}'. "
            f"Supported: {', '.join(_SUPPORTED_ACTIONS)}",
        )

    if act == "query":
        return _tool_error(
            "not_implemented: structured element lookup is reserved "
            "for phase 2. Use screenshot + coordinates for now.",
        )

    pyautogui, err = _load_pyautogui()
    if err:
        return _tool_error(err)

    try:
        screen_w, screen_h = pyautogui.size()
    except Exception as e:
        return _tool_error(f"failed to read screen size: {e!s}")

    def _need_xy() -> Optional[ToolResponse]:
        if x is None or y is None:
            return _tool_error(f"action '{act}' requires x and y")
        if not _in_bounds(pyautogui, int(x), int(y)):
            return _tool_error(
                f"coordinate ({x}, {y}) is outside screen "
                f"({screen_w}x{screen_h})",
                screen_size={"width": screen_w, "height": screen_h},
            )
        return None

    def _done(**extra: Any) -> ToolResponse:
        try:
            cx, cy = pyautogui.position()
        except Exception:
            cx, cy = (None, None)
        return _tool_ok(
            act,
            screen_size={"width": screen_w, "height": screen_h},
            mouse_pos_after={"x": cx, "y": cy},
            **extra,
        )

    try:
        if act == "screen_size":
            return _tool_ok(
                act,
                screen_size={"width": screen_w, "height": screen_h},
            )

        if act == "move_to":
            err = _need_xy()
            if err:
                return err
            pyautogui.moveTo(int(x), int(y), duration=0.0)
            return _done()

        if act == "click":
            err = _need_xy()
            if err:
                return err
            pyautogui.click(
                x=int(x),
                y=int(y),
                clicks=max(1, int(clicks)),
                button=button,
            )
            return _done(button=button, clicks=int(clicks))

        if act == "double_click":
            err = _need_xy()
            if err:
                return err
            pyautogui.doubleClick(x=int(x), y=int(y))
            return _done()

        if act == "right_click":
            err = _need_xy()
            if err:
                return err
            pyautogui.rightClick(x=int(x), y=int(y))
            return _done()

        if act == "drag":
            err = _need_xy()
            if err:
                return err
            if x2 is None or y2 is None:
                return _tool_error("drag requires x2 and y2")
            if not _in_bounds(pyautogui, int(x2), int(y2)):
                return _tool_error(
                    f"destination ({x2}, {y2}) is outside screen "
                    f"({screen_w}x{screen_h})",
                )
            pyautogui.moveTo(int(x), int(y), duration=0.0)
            pyautogui.dragTo(
                int(x2),
                int(y2),
                duration=max(0.0, float(duration)),
                button="left",
            )
            return _done(to={"x": int(x2), "y": int(y2)})

        if act == "type_text":
            if text is None:
                return _tool_error("type_text requires 'text'")
            pyautogui.typewrite(str(text), interval=0.0)
            return _done(typed_len=len(text))

        if act == "press_keys":
            if not keys:
                return _tool_error("press_keys requires non-empty 'keys'")
            normalized = [_normalize_key(k) for k in keys if k]
            if not normalized:
                return _tool_error("press_keys: all keys were empty")
            pyautogui.hotkey(*normalized)
            return _done(keys_pressed=normalized)

        if act == "scroll":
            if x is not None and y is not None:
                if not _in_bounds(pyautogui, int(x), int(y)):
                    return _tool_error(
                        f"coordinate ({x}, {y}) is outside screen "
                        f"({screen_w}x{screen_h})",
                    )
                pyautogui.moveTo(int(x), int(y), duration=0.0)
            pyautogui.scroll(int(dy))
            return _done(dy=int(dy))

    except Exception as e:
        return _tool_error(f"desktop_input '{act}' failed: {e!s}")

    return _tool_error(f"unhandled action '{act}'")

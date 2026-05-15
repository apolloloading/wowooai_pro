---
name: browser_visible
description: "Use this skill when the user needs to control the browser launch mode for browser_use. By default, browser_use launches the local Chrome/Chromium in headed mode (visible window) using managed CDP; pass `headed=false` only when the user explicitly asks for headless/background. `private_mode` controls whether CDP is disabled in favor of Playwright. Any login / account / password / verification code input must be handed off to the user in the visible window."
metadata:
  builtin_skill_version: "1.3"
  wowooai:
    emoji: "🖥️"
    requires: {}
---

# Browser Launch Modes

`browser_use.start` has only two launch modes:

- Default: managed CDP (**headed mode, visible window**)
- `private_mode=true`: Playwright-managed

Parameter meanings:

- `headed`: whether to display the browser window (**default true, visible window**). Pass `headed=false` only when the user explicitly asks for headless/background mode.
- `private_mode`: whether to disable CDP and use Playwright instead

The two parameters are independent and can be freely combined.

## Common Usage

Default launch (headed, visible window):
```json
{"action": "start"}
```

Headless mode (only when user explicitly requests it):
```json
{"action": "start", "headed": false}
```

Without CDP:
```json
{"action": "start", "private_mode": true}
```

Headless + without CDP:
```json
{"action": "start", "headed": false, "private_mode": true}
```

## When to Use `private_mode`

Only set `private_mode=true` when the user explicitly requests one of the following:

- Does not want the browser managed via CDP
- Wants to use Playwright instead
- Wants to reduce the possibility of other local tools connecting via CDP

Otherwise, just set `headed=false` as needed (rare).

## Login / Credentials Handoff

**Never** use `action=type` to auto-fill account, password, verification code, or SMS OTP.

When a page shows a login form or requires sensitive credentials:
1. Ensure the browser is running in headed mode (the default)
2. Tell the user to complete the login manually in the visible window
3. Wait for the user to confirm "logged in" before continuing automation

This rule has no exceptions — even if credentials exist in config or environment variables, do not auto-fill them.

## Notes

- The default is managed CDP, **headed mode (visible window)**
- The launch mode is entirely determined by the call parameters
- Managed CDP requires Chrome / Chromium / Edge to be installed locally
- `private_mode=true` does not mean absolutely undetectable — it simply switches to Playwright management
- When the user manually operates the visible browser, the idle timer may not be refreshed
- `private_mode` is an explicit parameter for each `start` call and is not persisted
- If a browser is already running, you must `stop` it and then `start` again to switch launch modes or window visibility
- Headless mode may be more suitable for servers or headless environments, but headed mode is the default to ensure users can complete login manually
- **Login / account / password / verification code must be entered manually by the user — never auto-fill**

---
name: agent_browser
description: "Use this skill when the user needs advanced browser capabilities (semantic find by role/text/label, network request route/mock, HAR recording, visual / snapshot diff, annotated screenshot, state save/load, Chrome profile reuse, React DevTools, Web Vitals). The skill calls the bundled `npx agent-browser@0.27.0` via execute_shell_command. It prefers to share Chrome with browser_use (start browser_use first with cdp_port exposed, then have agent-browser connect over CDP). For renliwo internal platforms still prefer renliwo_browser; for general browse/screenshot/simple interactions prefer browser_use; only escalate to agent-browser for advanced scenarios browser_use cannot handle."
metadata:
  builtin_skill_version: "1.0"
  wowooai:
    emoji: "🛰️"
    requires:
      bins: ["npx"]
---

# agent-browser advanced browser capabilities

`agent-browser` is Vercel Labs' open-source AI-agent browser CLI (Rust + CDP),
pinned to version `0.27.0`. This skill lets wowooai invoke it via
`execute_shell_command`, cooperating with the built-in `browser_use` and
`renliwo_browser` tools.

---

## 1. Three-tool layering rule (hard rule)

Escalate **renliwo → general → advanced**:

| Scenario | Tool |
|---|---|
| renliwo internal platforms (人力窝, QD outsourcing etc.) URLs | **`renliwo_browser`** |
| General browsing / screenshots / clicks / form fills | **`browser_use`** (in-process, no CLI overhead) |
| Semantic `find role/text/label` / network route / HAR / state save/load / Chrome profile reuse / visual diff / annotated screenshot / React debugging / Web Vitals | **`agent-browser`** |

Escalate on failure: browser_use can't do it → switch to agent-browser;
agent-browser also fails → report to user and ask for manual takeover.

---

## 2. Shared Chrome flow (avoid opening multiple browsers)

**Key principle**: have `browser_use` start Chrome and expose its CDP port,
then have `agent-browser` (and `renliwo_browser` if needed) attach via CDP.
One login is shared by all three: cookies / localStorage / open tabs.

### Standard steps

1. **browser_use starts and exposes the port**

   ```json
   {"action": "start", "cdp_port": 9222}
   ```

   Take `cdp_url` from the response (typically `http://localhost:9222`).
   Exposing `cdp_port` automatically disables the idle watchdog so the
   browser is not garbage-collected while idle.

2. **agent-browser connects to the same Chrome**

   ```bash
   npx agent-browser@0.27.0 connect 9222 --session $WOWOOAI_WORKSPACE_ID
   ```

   `--session` is named after the current workspace id so multiple
   workspaces don't bleed into each other.

3. **(Optional) renliwo_browser also joins the shared Chrome**

   ```json
   {"action": "connect_cdp", "cdp_url": "http://127.0.0.1:9222"}
   ```

   On `stop`, renliwo_browser only disconnects — it does not kill the
   process, so the other tools keep working.

### Anti-patterns

- ❌ `npx agent-browser@0.27.0 start --headed` — starts a *second* Chrome
  process unconnected to browser_use's browser; logins are not shared.
- ❌ `--auto-connect` across workspaces — may attach to the wrong workspace's
  browser.

---

## 3. Common commands (called via execute_shell_command)

All commands are prefixed with `npx agent-browser@0.27.0`.

### Semantic element finding (one fewer snapshot than browser_use's ref flow)

```bash
npx agent-browser@0.27.0 find role button --name "Submit" --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 find text "Login" --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 click @e1 --session $WOWOOAI_WORKSPACE_ID
```

### Network route / mock / HAR

```bash
# Block a URL
npx agent-browser@0.27.0 network route "https://example.com/track" --abort --session $WOWOOAI_WORKSPACE_ID

# Mock a response body
npx agent-browser@0.27.0 network route "**/api/user" --body '{"id":1,"name":"test"}' --session $WOWOOAI_WORKSPACE_ID

# HAR recording
npx agent-browser@0.27.0 network har start --session $WOWOOAI_WORKSPACE_ID
# ...interact with page...
npx agent-browser@0.27.0 network har stop --session $WOWOOAI_WORKSPACE_ID
```

### Waiting

```bash
# Wait for URL navigation
npx agent-browser@0.27.0 wait --url "**/dash" --session $WOWOOAI_WORKSPACE_ID
# Wait for networkidle
npx agent-browser@0.27.0 wait --load networkidle --session $WOWOOAI_WORKSPACE_ID
# Wait for a JS expression to be true
npx agent-browser@0.27.0 wait --fn "window.ready === true" --session $WOWOOAI_WORKSPACE_ID
```

### State save / load (skip next login)

```bash
npx agent-browser@0.27.0 state save my-login --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 state load my-login --session $WOWOOAI_WORKSPACE_ID
```

### Visual / annotated screenshot

```bash
npx agent-browser@0.27.0 screenshot --annotate --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 diff snapshot --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 diff screenshot --baseline before.png -t 0.2 --session $WOWOOAI_WORKSPACE_ID
```

### React / Web Vitals

```bash
npx agent-browser@0.27.0 react tree --session $WOWOOAI_WORKSPACE_ID
npx agent-browser@0.27.0 vitals --session $WOWOOAI_WORKSPACE_ID
```

Full command reference: https://github.com/vercel-labs/agent-browser

---

## 4. Login / credentials / OTP (matches browser_use / renliwo_browser)

⚠️ **Never use agent-browser to auto-fill usernames / passwords / OTPs /
SMS codes / sliding captchas.** These must be completed by the user in the
visible browser window.

Correct flow:
1. `browser_use action='start' headed=true cdp_port=9222` — opens visible Chrome
2. `browser_use action='open'` — navigate to login page
3. Tell the user "please complete login in the browser window, then tell me"
4. After login, agent-browser attaches via `connect`; the session is already
   in the cookies.

---

## 5. First-run download notes

The first time you call `npx agent-browser@0.27.0 ...`:
- The agent-browser CLI is pre-installed into the bundled Node.js at
  packaging time, so no internet download is required for the CLI itself.
- However, the first **browser-related** command may download
  Chrome for Testing (~200–300 MB).
- Cache location: `~/.cache/agent-browser/` (macOS/Linux) or
  `%LOCALAPPDATA%\agent-browser\` (Windows).
- If the user is already using browser_use's Chrome (the recommended
  shared flow), Chrome for Testing usually does **not** need to be
  downloaded at all.

Tell the user the first invocation may take a few minutes to download the
browser; subsequent calls are cached.

---

## 6. Session isolation convention

- Always pass `--session $WOWOOAI_WORKSPACE_ID` on every call.
- Parallel workspaces use independent sessions — they don't cross-contaminate.
- If the user explicitly requests "use agent-browser's own admin / user
  session", you may use names like `--session admin`.

---

## 7. Failure handling

| Failure | Response |
|---|---|
| `command not found: npx` | Report: bundled Node.js wasn't injected into PATH; fall back to browser_use. |
| `agent-browser connect` fails | Check whether browser_use is still running; if it was stopped, restart with `cdp_port` and re-connect. |
| Command syntax error | The pinned `@0.27.0` should prevent this; if it still happens, report to user and switch back to browser_use. |
| Two consecutive failures of the same command | Stop and report to the user — do not blindly retry. |

---

## 8. Security notes

- The bundled npx is intended **only** to run `agent-browser@0.27.0` —
  do not use it to install/execute arbitrary npm packages.
- agent-browser is by Vercel Labs; Chrome for Testing is by Google.
- For sensitive data, avoid `state save` (it persists logins to disk);
  if you must, remind the user to clean up afterwards.

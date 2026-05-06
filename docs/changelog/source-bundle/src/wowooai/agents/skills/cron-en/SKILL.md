---
name: cron
description: Use this skill only when future scheduled or periodic execution is needed. Manage tasks via wowooai cron list/create/get/state/pause/resume/delete/run, and always pass --agent-id explicitly.
metadata:
  builtin_skill_version: "2.1"
  wowooai:
    emoji: "⏰"
---

# Scheduled Task Management

## When to Use

Only use this skill when you need **automatic execution at a future time** or **periodic repeated execution**.

### Should Use
- User asks for "every day / every week / every hour" to do something
- User asks for "tomorrow at 9 AM / next Monday / some time" to auto-remind or execute
- Long-term periodic notifications, checks, reports, data exports

### Should NOT Use
- Just need to **execute once right now**
- Just a normal reply in the current session
- User has not specified execution time or schedule
- Target channel / user / session is not yet clear

---

## Decision Rules

1. **Only use cron for future scheduled or periodic execution**
2. **If it's a one-time immediate execution, usually don't create a cron**
3. **Before creating, confirm: execution time/schedule, target channel, target-user, target-session**
4. **All cron commands MUST explicitly pass `--agent-id`**
5. **Never rely on default agent, or the task may end up in the default workspace**

---

## Key: How to Choose `--type`

This is the most error-prone part. Choose the type based on **the nature of the user's request**:

### `--type text`: Send a fixed message only

**Use case**: Only need to send a **plain text message** at the target time, no computation, query, or operation needed.

**Behavior after trigger**: The system directly sends the `--text` content to the target channel, **without involving the agent**, **no tool calls are executed**.

### `--type agent`: Trigger agent to execute a full task

**Use case**: Need the agent to **execute a task** at the target time, including but not limited to:
- Browser operations (login to website, export data, fill forms)
- Data processing (read files, merge tables, generate reports)
- Shell commands (run scripts, check system status)
- MCP tool calls (query APIs, operate external systems)
- Comprehensive workflows (query data first, process, then send results)

**Execution chain after trigger**:
1. The system wraps the `--text` content into an agent request (equivalent to the user sending this message in a conversation)
2. The agent receives this message and **executes normally like handling any user message**:
   - Calls appropriate tools based on task description (browser, shell, file I/O, MCP, etc.)
   - Generates a reply
3. The reply is sent to the target session via the channel

### Decision Method

> Ask yourself: **"When the time arrives, should this text be 'read out' or 'executed'?"**
> - Read out → `--type text`
> - Execute → `--type agent`

---

## Parameter Reference

### Default Values

Use these defaults if the user doesn't specify otherwise:

| Parameter | Default | Description |
|---|---|---|
| `--channel` | `console` | Default: send to current console |
| `--target-user` | `default` | Default: send to current user |
| `--target-session` | Current session ID | Default: send to current session (from system prompt) |

### Meaning of `--text` Parameter

The meaning of `--text` differs by `--type`:

| Type | Meaning of `--text` | Content Requirements | Example |
|---|---|---|---|
| **text** | The final message sent to the user | Can be beautified/polished for a friendlier tone | User says "remind me to drink water" → `--text`: "Time to drink water! Stay hydrated" |
| **agent** | Task instruction, equivalent to a user message in conversation | Should include all info the agent needs: operation path, credentials, processing rules, output requirements. **Use the user's original description as much as possible, do not rewrite or simplify** | "Please open https://xxx.com, login with account xxx, navigate to contract management, export report and send to me" |

### Handling Long `--text`

If the task description is very long (over 500 characters), consider generating a JSON file first and using `wowooai cron create --agent-id <agent_id> -f job_spec.json`.

---

## Notes for Creating Agent Tasks

Agent tasks are **executed independently** at trigger time — they do NOT inherit the current session's context. Therefore `--text` MUST include:

- All information needed for execution (URLs, accounts, passwords, file paths, etc.)
- Expected output format and delivery method
- Any context the agent needs at execution time

**If the user's description is unclear, MUST ask for clarification before creating**:
- User says "check the server every day" → Ask: check what? CPU? Memory? Service response? How?
- User says "export report every day" → Ask: which website? Login credentials? How to handle after export?
- User says "remind me of a meeting" → This is a plain message, use `--type text`

**Preserve user's original description**: If the user's description is already clear (includes operation path, accounts, output requirements), use it directly as `--text`. Only ask for clarification when the description is vague.

---

## Hard Rules

### Must Explicitly Specify `--agent-id`

All `wowooai cron` commands **MUST** pass:

```bash
--agent-id <your_agent_id>
```

Your agent_id is in the Agent Identity section of the system prompt (Your agent id is ...).
Never omit, or the task may be created in the wrong agent's workspace.

---

## Common Commands

```bash
# List jobs
wowooai cron list --agent-id <agent_id>

# Get job details
wowooai cron get <job_id> --agent-id <agent_id>

# Get job runtime state
wowooai cron state <job_id> --agent-id <agent_id>

# Create a job
wowooai cron create --agent-id <agent_id> ...

# Delete a job
wowooai cron delete <job_id> --agent-id <agent_id>

# Pause / resume a job
wowooai cron pause <job_id> --agent-id <agent_id>
wowooai cron resume <job_id> --agent-id <agent_id>

# Trigger a one-off run immediately
wowooai cron run <job_id> --agent-id <agent_id>
```

> **Note**: CLI has no `update` command. To modify an existing task, you must: get details → delete → recreate.

---

## Creating Tasks

### Minimum Confirmation Before Creating
- `--type` (text or agent? see decision guide above)
- `--name`
- `--cron`
- `--channel`
- `--target-user`
- `--target-session`
- `--text`
- `--agent-id`

If any of these are missing, ask the user before creating.

### `--type text` Example

```bash
wowooai cron create \
  --agent-id <agent_id> \
  --type text \
  --name "Water Reminder" \
  --cron "0 9 * * *" \
  --channel console \
  --target-user default \
  --target-session "1777892768390" \
  --text "Time to drink water! Stay hydrated"
```

> `--text` is the reminder message the user will see. Can be beautified/polished.

### `--type agent` Example (Simple Q&A)

```bash
wowooai cron create \
  --agent-id <agent_id> \
  --type agent \
  --name "Check TODOs" \
  --cron "0 */2 * * *" \
  --channel console \
  --target-user default \
  --target-session "1777892768390" \
  --text "What are my pending TODO items?"
```

### `--type agent` Example (Complex Workflow)

```bash
wowooai cron create \
  --agent-id <agent_id> \
  --type agent \
  --name "Daily Contract Report Export" \
  --cron "0 8 * * *" \
  --channel console \
  --target-user default \
  --target-session "1777892768390" \
  --text "Please perform the following:
1. Open https://example.com/ and login with account xxx, password yyy
2. Navigate to Contract Management → Contract Product List
3. Click the Query button
4. Click Query Export, save to desktop as table1
5. Read table2 from desktop: related_data.xlsx
6. Merge the two tables and split results, then send to me"
```

> **Note**: `--type agent`'s `--text` is a **complete task description** containing all info the agent needs. Use the user's original description as much as possible.

### Create from JSON

```bash
wowooai cron create --agent-id <agent_id> -f job_spec.json
```

---

## Modifying Existing Tasks

CLI has no `update` command. To modify a task (change time, content, name, etc.):

```bash
# 1. Get task details
wowooai cron get <job_id> --agent-id <agent_id>

# 2. Delete old task
wowooai cron delete <job_id> --agent-id <agent_id>

# 3. Recreate with new parameters
wowooai cron create --agent-id <agent_id> ...
```

---

## Minimal Workflow

```
1. Determine if it's really "future scheduled" or "periodic execution"
2. Confirm execution time / schedule
3. Confirm channel, target-user, target-session (defaults: console / default / current session)
4. [Key] Determine task nature: plain message → text; needs execution → agent
5. If user description is unclear, ask for clarification; if clear, agent tasks use user's original text, text tasks can be polished
6. Explicitly pass --agent-id
7. wowooai cron create to create the task
8. Manage with list / state / pause / resume / delete afterwards
```

---

## Cron Expression Examples

```
0 9 * * *      Every day at 9:00
0 */2 * * *    Every 2 hours
30 8 * * 1-5   Weekdays at 8:30
0 0 * * 0      Every Sunday at midnight
*/15 * * * *   Every 15 minutes
```

---

## Common Errors

### Error 1: Treating one-time immediate execution as cron

If it's just execute once right now, usually don't create a cron.

### Error 2: Not passing `--agent-id`

This causes the task to end up in the wrong agent / workspace. All cron commands must explicitly pass `--agent-id`.

### Error 3: Creating without confirming all info

If user hasn't specified time, schedule, target channel, or target session, ask first.

**For agent tasks**, also confirm that `--text` contains all execution info (URLs, accounts, file paths, etc.). If the user's description is vague, must ask for clarification.

### Error 4: Operating on existing tasks without checking first

Before pausing, resuming, or deleting, first use:

```bash
wowooai cron list --agent-id <agent_id>
```

to find the correct `job_id`.

### Error 5: Choosing `--type text` when agent execution is needed

If the user requests a scheduled operation (e.g., "auto-export report at 8 AM daily", "check server status every hour") but you chose `--type text` during creation, the **system will only send this text out, without executing any operation**.

The correct approach is to use `--type agent`, so the agent actually executes the task at trigger time.

**Decision method**:
- `text` after trigger = text is printed as-is
- `agent` after trigger = agent receives message → calls tools → executes task → sends result

---

## Usage Tips

- When parameters are missing, ask the user before creating
- For text tasks, `--text` can be beautified/polished for a friendlier tone
- For agent tasks, `--text` should use the user's original description unless it's unclear
- Agent task `--text` must include full context (agent has no current session memory at trigger time)
- To modify a task: `get` details → `delete` → `create`
- Before modifying/pausing/deleting, first `wowooai cron list --agent-id <agent_id>`
- For troubleshooting, use `wowooai cron state <job_id> --agent-id <agent_id>`
- When showing commands to users, provide complete, directly copyable versions

---

## Help Information

```bash
wowooai cron -h
wowooai cron list -h
wowooai cron create -h
wowooai cron get -h
wowooai cron state -h
wowooai cron pause -h
wowooai cron resume -h
wowooai cron delete -h
wowooai cron run -h
```

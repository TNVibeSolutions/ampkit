---
name: worker
description: Execute beads autonomously within a track. Handles bead-to-bead context persistence via Agent Mail, uses preferred tools from AGENTS.md, and reports progress to orchestrator.
---

# Worker Skill: Autonomous Bead Execution

Executes beads within an assigned track, maintaining context via Agent Mail.

> **Agent Mail CLI**: All `am` commands use JSON args, NOT flags:
> `am <cmd> '{"key": "value"}'` (correct) | `am <cmd> --key value` (wrong)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACK LOOP (repeat for each bead in track)                                 │
│                                                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                     │
│  │ START BEAD   │ → │ WORK ON BEAD │ → │ COMPLETE     │ ───┐                │
│  │              │   │              │   │ BEAD         │    │                │
│  │ • Read ctx   │   │ • Implement  │   │ • Report     │    │                │
│  │ • Reserve    │   │ • Use tools  │   │ • Save ctx   │    │                │
│  │ • Claim      │   │ • Check mail │   │ • Release    │    │                │
│  └──────────────┘   └──────────────┘   └──────────────┘    │                │
│         ▲                                                  │                │
│         └──────────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Initial Setup (Once Per Track)

### 1. Register Agent Identity

**Tool**: `am register_agent`

| Parameter          | Required | Value                     |
| ------------------ | -------- | ------------------------- |
| `project_key`      | Yes      | `<absolute-project-path>` |
| `program`          | Yes      | `amp`                     |
| `model`            | Yes      | `<your-model>`            |
| `task_description` | Yes      | `Track N: <description>`  |
| `name`             | No       | Auto-generated if omitted |

### 2. Understand Your Assignment

From orchestrator: **Track number**, **Beads (in order)**, **File scope**, **Epic thread** (`<epic-id>`), **Track thread** (`track:<AgentName>:<epic-id>`)

---

## Bead Execution Loop

### Step 1: Start Bead

#### 1.1 Read Context from Previous Bead

**Tool**: `am summarize_thread`

| Parameter          | Value                         |
| ------------------ | ----------------------------- |
| `project_key`      | `<path>`                      |
| `thread_id`        | `track:<AgentName>:<epic-id>` |
| `include_examples` | `true`                        |

#### 1.2 Check Inbox

**Tool**: `am fetch_inbox`

| Parameter        | Value         |
| ---------------- | ------------- |
| `project_key`    | `<path>`      |
| `agent_name`     | `<AgentName>` |
| `include_bodies` | `true`        |

#### 1.3 Reserve Files

**Tool**: `am file_reservation_paths`

| Parameter     | Value                      |
| ------------- | -------------------------- |
| `project_key` | `<path>`                   |
| `agent_name`  | `<AgentName>`              |
| `paths`       | `["<your-file-scope>/**"]` |
| `ttl_seconds` | `7200`                     |
| `exclusive`   | `true`                     |
| `reason`      | `<bead-id>`                |

If conflict → report blocker (see `reference/message-templates.md`)

#### 1.4 Claim Bead

```bash
bd update <bead-id> --status in_progress
bd show <bead-id>
```

---

### Step 2: Work on Bead

#### 2.1 Explore Codebase

**Tool**: `finder`

| Parameter | Value                                                                 |
| --------- | --------------------------------------------------------------------- |
| `query`   | Natural language query describing what to find (e.g., "JWT auth flow") |

Use `finder` for semantic/conceptual searches. Use `Grep` for exact text matches.

#### 2.2 Make Changes

**Tool**: `edit_file`

| Parameter | Value                                      |
| --------- | ------------------------------------------ |
| `path`    | Absolute path to file                      |
| `old_str` | Exact text to replace (must match exactly) |
| `new_str` | New text to replace with                   |

After edits: `get_diagnostics("<edited-file>")`

#### 2.3 For UI Work

Load `frontend-design` skill first, then follow this workflow:

##### 2.3.1 Search for Components

**Tool**: `mcp__shadcn__search_items_in_registries`

| Parameter    | Value         |
| ------------ | ------------- |
| `registries` | `["@shadcn"]` |
| `query`      | `<component>` |

##### 2.3.2 View Component Details

**Tool**: `mcp__shadcn__view_items_in_registries`

| Parameter | Value                     |
| --------- | ------------------------- |
| `items`   | `["@shadcn/<component>"]` |

##### 2.3.3 Get Usage Examples

**Tool**: `mcp__shadcn__get_item_examples_from_registries`

| Parameter    | Value              |
| ------------ | ------------------ |
| `registries` | `["@shadcn"]`      |
| `query`      | `<component>-demo` |

##### 2.3.4 Install Component

**Tool**: `mcp__shadcn__get_add_command_for_items`

| Parameter | Value                     |
| --------- | ------------------------- |
| `items`   | `["@shadcn/<component>"]` |

Then run the returned command (e.g., `npx shadcn@latest add button`).

##### 2.3.5 Verify Installation

**Tool**: `mcp__shadcn__get_audit_checklist`

| Parameter | Value                             |
| --------- | --------------------------------- |
| `reason`  | `Verify <component> installation` |

#### 2.4 Check Inbox Periodically

Use `am fetch_inbox` with `since_ts` parameter.

#### 2.5 If Blocker or Interface Change

See `reference/message-templates.md` for message formats.

---

### Step 3: Complete Bead

#### 3.1 Verify & Check

```bash
get_diagnostics("<project-path>")
bun run check-types
bun run build
```

#### 3.2 Close Bead

```bash
bd close <bead-id> --reason "<concise summary>"
```

#### 3.3 Report to Orchestrator

**Tool**: `am send_message`

| Parameter     | Value                                |
| ------------- | ------------------------------------ |
| `project_key` | `<path>`                             |
| `sender_name` | `<AgentName>`                        |
| `to`          | `["<OrchestratorName>"]`             |
| `thread_id`   | `<epic-id>`                          |
| `subject`     | `[<bead-id>] COMPLETE`               |
| `body_md`     | See `reference/message-templates.md` |

#### 3.4 Save Context for Next Bead

Self-addressed message to track thread. See `reference/message-templates.md`.

#### 3.5 Release Reservations

**Tool**: `am release_file_reservations`

| Parameter     | Value         |
| ------------- | ------------- |
| `project_key` | `<path>`      |
| `agent_name`  | `<AgentName>` |

---

### Step 4: Continue to Next Bead

Loop back to Step 1. Context from Step 3.4 available via track thread.

---

## Track Completion

When all beads done, send track complete message (see `reference/message-templates.md`), then return:

```
Track N (<AgentName>) Complete:
- Completed beads: a, b, c
- Summary: <what was built>
- All acceptance criteria met
```

---

## Quick Reference

### Bead Lifecycle Checklist

```
START: summarize_thread → fetch_inbox → file_reservation_paths → bd update
WORK:  finder → edit_file → get_diagnostics → check inbox
DONE:  verify → bd close → send_message (orchestrator) → send_message (self) → release
NEXT:  loop to START
```

### Thread Reference

| Thread                        | Purpose                                 |
| ----------------------------- | --------------------------------------- |
| `<epic-id>`                   | Cross-agent, orchestrator communication |
| `track:<AgentName>:<epic-id>` | Your personal context persistence       |

### Tool Reference

| Task              | Tool                                             |
| ----------------- | ------------------------------------------------ |
| Find code         | `finder`                                         |
| Search components | `mcp__shadcn__search_items_in_registries`        |
| View components   | `mcp__shadcn__view_items_in_registries`          |
| Get examples      | `mcp__shadcn__get_item_examples_from_registries` |
| Install component | `mcp__shadcn__get_add_command_for_items`         |
| Verify install    | `mcp__shadcn__get_audit_checklist`               |

---

## Additional Resources

- **Message Templates**: `reference/message-templates.md` for all Agent Mail message formats

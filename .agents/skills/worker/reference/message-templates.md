# Worker Message Templates

Templates for Agent Mail messages sent during bead execution.

## Report to Orchestrator (Bead Complete)

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter     | Value                     |
| ------------- | ------------------------- |
| `project_key` | `<absolute-project-path>` |
| `sender_name` | `<AgentName>`             |
| `to`          | `["<OrchestratorName>"]`  |
| `thread_id`   | `<epic-id>`               |
| `subject`     | `[<bead-id>] COMPLETE`    |
| `body_md`     | See template below        |

```markdown
## Completed: <bead-id>

### What Was Done

- <bullet points>

### Files Modified

- <file list>

### Next Bead

- <next-bead-id>: <brief plan>

### Track Progress

- Completed: X/Y beads
```

---

## Save Context (Self-Addressed)

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter     | Value                                   |
| ------------- | --------------------------------------- |
| `project_key` | `<absolute-project-path>`               |
| `sender_name` | `<AgentName>`                           |
| `to`          | `["<AgentName>"]` (self-addressed!)     |
| `thread_id`   | `track:<AgentName>:<epic-id>`           |
| `subject`     | `<bead-id> Complete - Context for Next` |
| `body_md`     | See template below                      |

```markdown
## Bead Complete: <bead-id>

### Key Changes

- <what was implemented>

### Learnings

- <patterns discovered>
- <things that work well>

### Gotchas

- <things to watch out for>

### For Next Bead (<next-bead-id>)

- <recommendations>
- <relevant context>

### Files to Reference

- <key files for next bead>
```

---

## Report Blocker

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter      | Value                                              |
| -------------- | -------------------------------------------------- |
| `project_key`  | `<absolute-project-path>`                          |
| `sender_name`  | `<AgentName>`                                      |
| `to`           | `["<OrchestratorName>"]`                           |
| `thread_id`    | `<epic-id>`                                        |
| `subject`      | `[<bead-id>] BLOCKED: <reason>`                    |
| `body_md`      | `Blocked by: <explanation>. Need: <what you need>` |
| `importance`   | `high`                                             |
| `ack_required` | `true`                                             |

---

## Interface Change Notification

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter     | Value                                                |
| ------------- | ---------------------------------------------------- |
| `project_key` | `<absolute-project-path>`                            |
| `sender_name` | `<AgentName>`                                        |
| `to`          | `["<OtherWorker1>", "<OtherWorker2>"]`               |
| `thread_id`   | `<epic-id>`                                          |
| `subject`     | `[<bead-id>] Interface Change: <what>`               |
| `body_md`     | `Changed <interface> from X to Y. Update your code.` |
| `importance`  | `high`                                               |

---

## Track Complete

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter     | Value                     |
| ------------- | ------------------------- |
| `project_key` | `<absolute-project-path>` |
| `sender_name` | `<AgentName>`             |
| `to`          | `["<OrchestratorName>"]`  |
| `thread_id`   | `<epic-id>`               |
| `subject`     | `[Track N] COMPLETE`      |
| `body_md`     | See template below        |

```markdown
## Track N Complete

### Beads Completed

- <bead-1>: <summary>
- <bead-2>: <summary>
- <bead-3>: <summary>

### Track Summary

- <overall what was accomplished>

### Key Learnings

- <insights for future work>

### Files Modified

- <comprehensive list>
```

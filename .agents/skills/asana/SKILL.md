---
name: asana
description: Integrate with Asana for task management. Use when user references Asana task IDs, asks to read/update/create Asana tasks, sync task status, fetch task details, search tasks, list projects, manage subtasks, or create tasks with standardized templates. Supports full CRUD operations on tasks and projects.
version: 1.2.0
---

# Asana Integration

Interact with Asana API for complete task management.

## Setup

1. Get Personal Access Token from https://app.asana.com/0/developer-console
2. Create `.env` file in this skill folder: `ASANA_PAT=your_token`

## Commands

### Basic Task Operations
```bash
python3 scripts/asana_api.py get-task <task_id>
python3 scripts/asana_api.py complete-task <task_id>
python3 scripts/asana_api.py incomplete-task <task_id>
python3 scripts/asana_api.py update-task <task_id> name "New name"
python3 scripts/asana_api.py update-task <task_id> notes "Description"
python3 scripts/asana_api.py update-task <task_id> due_on 2025-01-20
python3 scripts/asana_api.py assign-task <task_id> <user_gid>
python3 scripts/asana_api.py unassign-task <task_id>
python3 scripts/asana_api.py add-comment <task_id> "Comment text"
python3 scripts/asana_api.py create-task <project_id> "Task name"
```

### Subtasks
```bash
python3 scripts/asana_api.py get-subtasks <task_id>
python3 scripts/asana_api.py create-subtask <parent_task_id> "Subtask name"
```

### Projects & Search
```bash
python3 scripts/asana_api.py list-tasks <project_id>
python3 scripts/asana_api.py list-projects [workspace_id]
python3 scripts/asana_api.py search <workspace_id> "query"
```

### Users
```bash
python3 scripts/asana_api.py me
python3 scripts/asana_api.py list-users [workspace_id]
```

---

## Create Tasks with Template

Create well-formatted tasks with standardized title format: `[{Project}][{Platform}] {Title}`

**Platform options:** `BE`, `FE`, `DevOps`, `QA`, `Mobile`, `Design`, `Docs`

### Create Single Task
```bash
python3 scripts/create_task.py \
  --project-id "PROJECT_ID" \
  --project-name "MyProject" \
  --platform "BE" \
  --title "User Authentication API" \
  --details "Implement JWT auth|Add refresh token|Rate limiting" \
  --tests "Verify token generation|Verify refresh flow" \
  --files "src/auth/handler.py|src/auth/jwt.py" \
  --estimate "8h"
```

### Create Subtask with Template
```bash
python3 scripts/create_task.py \
  --parent-id "PARENT_TASK_ID" \
  --project-name "MyProject" \
  --platform "FE" \
  --title "Login Form Component" \
  --details "Create login form|Add validation|Connect to API" \
  --tests "Verify form validation|Verify API integration" \
  --estimate "4h"
```

### Batch Create from JSON
```bash
python3 scripts/batch_create_tasks.py \
  --input tasks.json \
  --parent-id "PARENT_TASK_ID"
```

**tasks.json format:**
```json
{
  "project_name": "MyProject",
  "subtasks": [
    {
      "platform": "BE",
      "title": "Task Title",
      "details": ["Detail 1", "Detail 2"],
      "tests": ["Test case 1", "Test case 2"],
      "files": ["path/to/file.py"],
      "estimate": "4h"
    }
  ]
}
```

### Dry Run (Preview)
```bash
python3 scripts/batch_create_tasks.py --input tasks.json --parent-id "123" --dry-run
```

See [templates/example_tasks.json](templates/example_tasks.json) for a complete example.

---

## Task Description Template

Tasks created with template will have this format:

```markdown
**Implementation Detail:**

- Detail point 1
- Detail point 2

**Testing Checklist:**

- [ ] Test case 1
- [ ] Test case 2

**Files:**
- `path/to/file1.py`
- `path/to/file2.py`

**Dependencies:**
- Dependency task

**Estimate:** 4h
```

---

## Task ID Format

Extract from URL: `https://app.asana.com/0/PROJECT_ID/TASK_ID`
Or branch names: `feat/1212812747582922`

## References

- [API Reference](references/api_reference.md)

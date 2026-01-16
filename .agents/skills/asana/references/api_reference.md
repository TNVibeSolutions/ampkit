# Asana API Reference

## Authentication

All requests use Bearer token:
```
Authorization: Bearer <ASANA_PAT>
```

## Common Endpoints

### Tasks

```
GET /tasks/{task_id}
  - Get task details including name, notes, completed, due_on, assignee

PUT /tasks/{task_id}
  - Update task (completed, name, notes, due_on, assignee)
  - Body: {"data": {"completed": true}}

POST /tasks/{task_id}/stories
  - Add comment
  - Body: {"data": {"text": "comment"}}
```

### Projects

```
GET /projects/{project_id}/tasks
  - List tasks in project
  - Params: opt_fields=name,completed,due_on,assignee.name
```

### Users

```
GET /users/me
  - Current user info and workspaces
```

## Task Fields

| Field | Type | Description |
|-------|------|-------------|
| gid | string | Task ID |
| name | string | Task title |
| notes | string | Task description (HTML) |
| completed | boolean | Completion status |
| due_on | string | Due date (YYYY-MM-DD) |
| assignee | object | {gid, name} |
| projects | array | Parent projects |
| custom_fields | array | Custom field values |

## Error Handling

```json
{
  "errors": [{
    "message": "Error description",
    "help": "Suggestion"
  }]
}
```

Common errors:
- 401: Invalid/expired token
- 403: No permission
- 404: Task/project not found

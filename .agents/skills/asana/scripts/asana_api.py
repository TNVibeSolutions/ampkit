#!/usr/bin/env python3
"""
Asana API client for task management.
Usage: python3 asana_api.py <command> [args]
"""

import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

ASANA_API_BASE = "https://app.asana.com/api/1.0"


def load_env():
    """Load .env file following priority order."""
    env_paths = [
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env",
        Path.home() / ".claude" / "skills" / ".env",
        Path.home() / ".claude" / ".env",
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key.strip() not in os.environ:
                            os.environ[key.strip()] = value.strip().strip('"').strip("'")


def get_token():
    """Get Asana Personal Access Token."""
    load_env()
    token = os.environ.get("ASANA_PAT") or os.environ.get("ASANA_TOKEN")
    if not token:
        print("ERROR: ASANA_PAT not set. Create .env file with:")
        print("  ASANA_PAT=your_personal_access_token")
        sys.exit(1)
    return token


def api_request(endpoint, method="GET", data=None):
    """Make Asana API request."""
    url = f"{ASANA_API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }
    
    body = json.dumps({"data": data}).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)
    
    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"API Error {e.code}: {error_body}")
        sys.exit(1)


# ============== TASK OPERATIONS ==============

def get_task(task_id):
    """Get task details."""
    result = api_request(f"/tasks/{task_id}")
    task = result.get("data", {})
    
    print(f"Task: {task.get('name')}")
    print(f"GID: {task.get('gid')}")
    print(f"Status: {'Completed' if task.get('completed') else 'Open'}")
    print(f"Due: {task.get('due_on') or 'Not set'}")
    assignee = task.get('assignee')
    print(f"Assignee: {assignee.get('name') if assignee else 'Unassigned'}")
    projects = task.get('projects', [])
    print(f"Projects: {', '.join([p.get('name', '') for p in projects]) or 'None'}")
    print(f"Notes:\n{(task.get('notes') or '')[:500]}")
    
    return task


def complete_task(task_id):
    """Mark task as complete."""
    api_request(f"/tasks/{task_id}", method="PUT", data={"completed": True})
    print(f"Task {task_id} marked as complete")


def incomplete_task(task_id):
    """Mark task as incomplete."""
    api_request(f"/tasks/{task_id}", method="PUT", data={"completed": False})
    print(f"Task {task_id} marked as incomplete")


def update_task(task_id, **kwargs):
    """Update task fields (name, notes, due_on)."""
    data = {}
    if "name" in kwargs:
        data["name"] = kwargs["name"]
    if "notes" in kwargs:
        data["notes"] = kwargs["notes"]
    if "due_on" in kwargs:
        data["due_on"] = kwargs["due_on"]  # Format: YYYY-MM-DD
    if "assignee" in kwargs:
        data["assignee"] = kwargs["assignee"]  # User GID
    
    if not data:
        print("No fields to update")
        return
    
    result = api_request(f"/tasks/{task_id}", method="PUT", data=data)
    print(f"Task {task_id} updated successfully")
    return result.get("data", {})


def create_task(project_id, name, **kwargs):
    """Create a new task in project."""
    data = {
        "name": name,
        "projects": [project_id],
    }
    if "notes" in kwargs:
        data["notes"] = kwargs["notes"]
    if "due_on" in kwargs:
        data["due_on"] = kwargs["due_on"]
    if "assignee" in kwargs:
        data["assignee"] = kwargs["assignee"]
    
    result = api_request("/tasks", method="POST", data=data)
    task = result.get("data", {})
    print(f"Created task: {task.get('name')} (GID: {task.get('gid')})")
    return task


def assign_task(task_id, user_gid):
    """Assign task to user."""
    api_request(f"/tasks/{task_id}", method="PUT", data={"assignee": user_gid})
    print(f"Task {task_id} assigned to user {user_gid}")


def unassign_task(task_id):
    """Unassign task."""
    api_request(f"/tasks/{task_id}", method="PUT", data={"assignee": None})
    print(f"Task {task_id} unassigned")


def add_comment(task_id, text):
    """Add comment to task."""
    api_request(f"/tasks/{task_id}/stories", method="POST", data={"text": text})
    print(f"Comment added to task {task_id}")


def get_stories(task_id):
    """Get comments/stories of a task."""
    result = api_request(f"/tasks/{task_id}/stories?opt_fields=created_at,created_by.name,text,type,resource_subtype")
    stories = result.get("data", [])
    
    print(f"Stories for task {task_id}:")
    for story in stories:
        if story.get("resource_subtype") == "comment_added":
            created_by = story.get("created_by", {}).get("name", "Unknown")
            created_at = story.get("created_at", "")[:10]
            text = story.get("text", "")
            print(f"\n[{created_at}] {created_by}:")
            print(f"  {text}")
    
    return stories


def get_subtasks(task_id):
    """Get subtasks of a task."""
    result = api_request(f"/tasks/{task_id}/subtasks?opt_fields=name,completed,due_on,assignee.name")
    subtasks = result.get("data", [])
    
    print(f"Subtasks of {task_id}:")
    for task in subtasks:
        status = "✓" if task.get("completed") else "○"
        assignee = task.get("assignee")
        assignee_name = assignee.get("name") if assignee else ""
        print(f"  {status} [{task['gid']}] {task['name']} ({assignee_name})")
    
    return subtasks


def create_subtask(parent_task_id, name, **kwargs):
    """Create subtask under parent task."""
    data = {"name": name}
    if "notes" in kwargs:
        data["notes"] = kwargs["notes"]
    if "due_on" in kwargs:
        data["due_on"] = kwargs["due_on"]
    if "assignee" in kwargs:
        data["assignee"] = kwargs["assignee"]
    
    result = api_request(f"/tasks/{parent_task_id}/subtasks", method="POST", data=data)
    task = result.get("data", {})
    print(f"Created subtask: {task.get('name')} (GID: {task.get('gid')})")
    return task


# ============== PROJECT OPERATIONS ==============

def list_tasks(project_id, limit=50):
    """List tasks in project."""
    result = api_request(f"/projects/{project_id}/tasks?opt_fields=name,completed,due_on,assignee.name&limit={limit}")
    tasks = result.get("data", [])
    
    print(f"Tasks in project {project_id}:")
    for task in tasks:
        status = "✓" if task.get("completed") else "○"
        assignee = task.get("assignee")
        assignee_name = assignee.get("name") if assignee else ""
        due = task.get("due_on") or ""
        print(f"  {status} [{task['gid']}] {task['name']} | {assignee_name} | {due}")
    
    return tasks


def list_projects(workspace_id=None):
    """List projects in workspace."""
    if not workspace_id:
        # Get first workspace from user
        me = api_request("/users/me")
        workspaces = me.get("data", {}).get("workspaces", [])
        if not workspaces:
            print("No workspaces found")
            return []
        workspace_id = workspaces[0]["gid"]
    
    result = api_request(f"/workspaces/{workspace_id}/projects?opt_fields=name,archived&limit=100")
    projects = result.get("data", [])
    
    print(f"Projects in workspace {workspace_id}:")
    for project in projects:
        if not project.get("archived"):
            print(f"  [{project['gid']}] {project['name']}")
    
    return projects


# ============== SEARCH ==============

def search_tasks(workspace_id, query, limit=20):
    """Search tasks in workspace."""
    params = urlencode({
        "text": query,
        "opt_fields": "name,completed,due_on,assignee.name,projects.name",
        "limit": limit
    })
    result = api_request(f"/workspaces/{workspace_id}/tasks/search?{params}")
    tasks = result.get("data", [])
    
    print(f"Search results for '{query}':")
    for task in tasks:
        status = "✓" if task.get("completed") else "○"
        assignee = task.get("assignee")
        assignee_name = assignee.get("name") if assignee else ""
        projects = task.get("projects", [])
        project_name = projects[0].get("name") if projects else ""
        print(f"  {status} [{task['gid']}] {task['name']} | {project_name} | {assignee_name}")
    
    return tasks


# ============== USER OPERATIONS ==============

def get_me():
    """Get current user info."""
    result = api_request("/users/me")
    user = result.get("data", {})
    print(f"User: {user.get('name')}")
    print(f"GID: {user.get('gid')}")
    print(f"Email: {user.get('email')}")
    print(f"Workspaces:")
    for ws in user.get("workspaces", []):
        print(f"  [{ws['gid']}] {ws['name']}")
    return user


def list_users(workspace_id=None):
    """List users in workspace."""
    if not workspace_id:
        me = api_request("/users/me")
        workspaces = me.get("data", {}).get("workspaces", [])
        if not workspaces:
            print("No workspaces found")
            return []
        workspace_id = workspaces[0]["gid"]
    
    result = api_request(f"/workspaces/{workspace_id}/users?opt_fields=name,email")
    users = result.get("data", [])
    
    print(f"Users in workspace {workspace_id}:")
    for user in users:
        print(f"  [{user['gid']}] {user.get('name')} ({user.get('email', '')})")
    
    return users


# ============== MAIN ==============

def print_help():
    """Print help message."""
    help_text = """
Asana API Client

Usage: asana_api.py <command> [args]

TASK COMMANDS:
  get-task <task_id>                    Get task details
  complete-task <task_id>               Mark task complete
  incomplete-task <task_id>             Mark task incomplete
  update-task <task_id> <field> <value> Update task (name|notes|due_on)
  assign-task <task_id> <user_gid>      Assign task to user
  unassign-task <task_id>               Unassign task
  add-comment <task_id> <text>          Add comment to task
  create-task <project_id> <name>       Create new task
  get-subtasks <task_id>                List subtasks
  create-subtask <task_id> <name>       Create subtask

PROJECT COMMANDS:
  list-tasks <project_id>               List tasks in project
  list-projects [workspace_id]          List projects

SEARCH:
  search <workspace_id> <query>         Search tasks

USER COMMANDS:
  me                                    Get current user info
  list-users [workspace_id]             List users in workspace
"""
    print(help_text)


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    # Task commands
    if cmd == "get-task" and len(args) >= 1:
        get_task(args[0])
    elif cmd == "complete-task" and len(args) >= 1:
        complete_task(args[0])
    elif cmd == "incomplete-task" and len(args) >= 1:
        incomplete_task(args[0])
    elif cmd == "update-task" and len(args) >= 3:
        update_task(args[0], **{args[1]: " ".join(args[2:])})
    elif cmd == "assign-task" and len(args) >= 2:
        assign_task(args[0], args[1])
    elif cmd == "unassign-task" and len(args) >= 1:
        unassign_task(args[0])
    elif cmd == "add-comment" and len(args) >= 2:
        add_comment(args[0], " ".join(args[1:]))
    elif cmd == "get-stories" and len(args) >= 1:
        get_stories(args[0])
    elif cmd == "create-task" and len(args) >= 2:
        create_task(args[0], " ".join(args[1:]))
    elif cmd == "get-subtasks" and len(args) >= 1:
        get_subtasks(args[0])
    elif cmd == "create-subtask" and len(args) >= 2:
        create_subtask(args[0], " ".join(args[1:]))
    
    # Project commands
    elif cmd == "list-tasks" and len(args) >= 1:
        limit = int(args[1]) if len(args) > 1 else 50
        list_tasks(args[0], limit)
    elif cmd == "list-projects":
        workspace_id = args[0] if args else None
        list_projects(workspace_id)
    
    # Search
    elif cmd == "search" and len(args) >= 2:
        search_tasks(args[0], " ".join(args[1:]))
    
    # User commands
    elif cmd == "me":
        get_me()
    elif cmd == "list-users":
        workspace_id = args[0] if args else None
        list_users(workspace_id)
    
    elif cmd == "help" or cmd == "--help" or cmd == "-h":
        print_help()
    
    else:
        print(f"Unknown command or missing args: {cmd}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

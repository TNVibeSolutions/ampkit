#!/usr/bin/env python3
"""
Create Asana tasks with standardized format for any project.
Uses html_notes for rich text formatting and sets Dev Hours custom field.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ASANA_API_BASE = "https://app.asana.com/api/1.0"

# Platform mapping
PLATFORMS = ["BE", "FE", "DevOps", "QA", "Mobile", "Design", "Docs"]


def load_env():
    """Load .env file from asana skill directory."""
    env_paths = [
        Path(__file__).parent.parent / ".env",
        Path(__file__).parent / ".env",
        Path.home() / ".claude" / "skills" / "asana" / ".env",
        Path.home() / ".claude" / "skills" / ".env",
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
        print("ERROR: ASANA_PAT not set.")
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


def get_dev_hours_field_gid(task_id: str) -> str:
    """Get the Dev Hours custom field GID for a task."""
    result = api_request(f"/tasks/{task_id}?opt_fields=custom_fields.name,custom_fields.gid,custom_fields.type")
    custom_fields = result.get("data", {}).get("custom_fields", [])
    
    for field in custom_fields:
        if field.get("name") == "Dev Hours" and field.get("type") == "number":
            return field.get("gid")
    
    return None


def format_task_title(project_name: str, platform: str, title: str) -> str:
    """Format task title with project prefix."""
    return f"[{project_name}][{platform}] {title}"


def parse_hours(estimate: str) -> float:
    """Parse hours from estimate string like '4h' or '4'."""
    if not estimate:
        return None
    try:
        return float(estimate.lower().replace("h", "").strip())
    except ValueError:
        return None


def format_html_notes(
    details: list,
    tests: list = None,
    files: list = None,
    dependencies: list = None,
    estimate: str = None
) -> str:
    """Format task description as HTML for Asana rich text."""
    parts = []
    
    # Implementation Details
    if details:
        parts.append("<strong>Implementation Detail:</strong>")
        parts.append("<ul>")
        for detail in details:
            parts.append(f"<li>{detail}</li>")
        parts.append("</ul>")
    
    # Testing Checklist
    if tests:
        parts.append("<strong>Testing Checklist:</strong>")
        parts.append("<ul>")
        for test in tests:
            parts.append(f"<li>[ ] {test}</li>")
        parts.append("</ul>")
    
    # Files (optional)
    if files:
        parts.append("<strong>Files:</strong>")
        parts.append("<ul>")
        for f in files:
            parts.append(f"<li><code>{f}</code></li>")
        parts.append("</ul>")
    
    # Dependencies (optional)
    if dependencies:
        parts.append("<strong>Dependencies:</strong>")
        parts.append("<ul>")
        for dep in dependencies:
            parts.append(f"<li>{dep}</li>")
        parts.append("</ul>")
    
    # Note: Estimate goes to custom field, not description
    
    return "<body>" + "\n".join(parts) + "</body>"


def create_task(project_id: str, name: str, html_notes: str, hours: float = None) -> dict:
    """Create a new task in project."""
    data = {
        "name": name,
        "html_notes": html_notes,
        "projects": [project_id],
    }
    
    result = api_request("/tasks", method="POST", data=data)
    task = result.get("data", {})
    task_gid = task.get("gid")
    
    # Set Dev Hours if provided
    if hours and task_gid:
        set_dev_hours(task_gid, hours)
    
    print(f"✓ Created task: {task.get('name')} (GID: {task_gid})")
    return task


def create_subtask(parent_task_id: str, name: str, html_notes: str, hours: float = None) -> dict:
    """Create a subtask under parent task."""
    data = {
        "name": name,
        "html_notes": html_notes,
    }
    
    result = api_request(f"/tasks/{parent_task_id}/subtasks", method="POST", data=data)
    task = result.get("data", {})
    task_gid = task.get("gid")
    
    # Set Dev Hours if provided
    if hours and task_gid:
        set_dev_hours(task_gid, hours)
    
    print(f"✓ Created subtask: {task.get('name')} (GID: {task_gid})")
    return task


def set_dev_hours(task_id: str, hours: float) -> bool:
    """Set the Dev Hours custom field for a task."""
    field_gid = get_dev_hours_field_gid(task_id)
    
    if not field_gid:
        print(f"  ⚠ Dev Hours field not found for task {task_id}")
        return False
    
    data = {
        "custom_fields": {
            field_gid: hours
        }
    }
    
    api_request(f"/tasks/{task_id}", method="PUT", data=data)
    print(f"  ✓ Set Dev Hours: {hours}h")
    return True


def update_task(task_id: str, name: str = None, html_notes: str = None, hours: float = None) -> dict:
    """Update an existing task."""
    data = {}
    if name:
        data["name"] = name
    if html_notes:
        data["html_notes"] = html_notes
    
    result = api_request(f"/tasks/{task_id}", method="PUT", data=data)
    task = result.get("data", {})
    
    # Set Dev Hours if provided
    if hours:
        set_dev_hours(task_id, hours)
    
    print(f"✓ Updated task: {task.get('name')} (GID: {task.get('gid')})")
    return task


def main():
    parser = argparse.ArgumentParser(description="Create Asana task with standardized format")
    parser.add_argument("--project-id", help="Project ID to create task in")
    parser.add_argument("--parent-id", help="Parent task ID for subtask")
    parser.add_argument("--task-id", help="Task ID to update (for updates)")
    parser.add_argument("--project-name", required=True, help="Project name for title prefix")
    parser.add_argument("--platform", required=True, choices=PLATFORMS, help="Platform type")
    parser.add_argument("--title", required=True, help="Task title (without prefix)")
    parser.add_argument("--details", required=True, help="Implementation details, pipe-separated")
    parser.add_argument("--tests", help="Test cases, pipe-separated")
    parser.add_argument("--files", help="Related files, pipe-separated")
    parser.add_argument("--dependencies", help="Dependencies, pipe-separated")
    parser.add_argument("--estimate", help="Time estimate (e.g., 4h) - sets Dev Hours field")
    
    args = parser.parse_args()
    
    if not args.project_id and not args.parent_id and not args.task_id:
        print("ERROR: Either --project-id, --parent-id, or --task-id is required")
        sys.exit(1)
    
    # Parse pipe-separated values
    details = [d.strip() for d in args.details.split("|")]
    tests = [t.strip() for t in args.tests.split("|")] if args.tests else None
    files = [f.strip() for f in args.files.split("|")] if args.files else None
    dependencies = [d.strip() for d in args.dependencies.split("|")] if args.dependencies else None
    hours = parse_hours(args.estimate)
    
    # Format task
    task_name = format_task_title(args.project_name, args.platform, args.title)
    html_notes = format_html_notes(details, tests, files, dependencies)
    
    # Create or update task
    if args.task_id:
        update_task(args.task_id, task_name, html_notes, hours)
    elif args.parent_id:
        create_subtask(args.parent_id, task_name, html_notes, hours)
    else:
        create_task(args.project_id, task_name, html_notes, hours)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Batch create Asana tasks from JSON file with standardized format.
Usage: python3 batch_create_tasks.py --input tasks.json --parent-id 1212613149794163
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ASANA_API_BASE = "https://app.asana.com/api/1.0"


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
        return None


def format_task_title(project_name: str, platform: str, title: str) -> str:
    """Format task title with project prefix."""
    return f"[{project_name}][{platform}] {title}"


def format_task_description(task: dict) -> str:
    """Format task description with standard template."""
    lines = []
    
    # Implementation Details
    details = task.get("details", [])
    if details:
        lines.append("**Implementation Detail:**\n")
        for detail in details:
            lines.append(f"- {detail}")
        lines.append("")
    
    # Testing Checklist
    tests = task.get("tests", [])
    if tests:
        lines.append("**Testing Checklist:**\n")
        for test in tests:
            lines.append(f"- [ ] {test}")
        lines.append("")
    
    # Files (optional)
    files = task.get("files", [])
    if files:
        lines.append("**Files:**")
        for f in files:
            lines.append(f"- `{f}`")
        lines.append("")
    
    # Dependencies (optional)
    dependencies = task.get("dependencies", [])
    if dependencies:
        lines.append("**Dependencies:**")
        for dep in dependencies:
            lines.append(f"- {dep}")
        lines.append("")
    
    # Estimate (optional)
    estimate = task.get("estimate")
    if estimate:
        lines.append(f"**Estimate:** {estimate}")
    
    return "\n".join(lines)


def create_subtask(parent_task_id: str, name: str, notes: str) -> dict:
    """Create a subtask under parent task."""
    data = {
        "name": name,
        "notes": notes,
    }
    
    result = api_request(f"/tasks/{parent_task_id}/subtasks", method="POST", data=data)
    if result:
        task = result.get("data", {})
        print(f"✓ Created: {task.get('name')} (GID: {task.get('gid')})")
        return task
    return None


def create_task(project_id: str, name: str, notes: str) -> dict:
    """Create a new task in project."""
    data = {
        "name": name,
        "notes": notes,
        "projects": [project_id],
    }
    
    result = api_request("/tasks", method="POST", data=data)
    if result:
        task = result.get("data", {})
        print(f"✓ Created: {task.get('name')} (GID: {task.get('gid')})")
        return task
    return None


def main():
    parser = argparse.ArgumentParser(description="Batch create Asana tasks from JSON")
    parser.add_argument("--input", required=True, help="JSON file with tasks")
    parser.add_argument("--parent-id", help="Parent task ID for subtasks")
    parser.add_argument("--project-id", help="Project ID for top-level tasks")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    
    args = parser.parse_args()
    
    if not args.parent_id and not args.project_id:
        print("ERROR: Either --parent-id or --project-id is required")
        sys.exit(1)
    
    # Load JSON file
    with open(args.input, "r") as f:
        data = json.load(f)
    
    project_name = data.get("project_name", "Project")
    subtasks = data.get("subtasks", [])
    
    print(f"Project: {project_name}")
    print(f"Found {len(subtasks)} tasks to create")
    print("-" * 50)
    
    created_count = 0
    total_hours = 0
    
    for task in subtasks:
        platform = task.get("platform", "API")
        title = task.get("title", "Untitled")
        estimate = task.get("estimate", "")
        
        # Parse hours from estimate
        if estimate:
            try:
                hours = float(estimate.replace("h", "").strip())
                total_hours += hours
            except ValueError:
                pass
        
        task_name = format_task_title(project_name, platform, title)
        task_notes = format_task_description(task)
        
        if args.dry_run:
            print(f"\n[DRY RUN] {task_name}")
            print(f"  Estimate: {estimate}")
        else:
            if args.parent_id:
                result = create_subtask(args.parent_id, task_name, task_notes)
            else:
                result = create_task(args.project_id, task_name, task_notes)
            
            if result:
                created_count += 1
    
    print("-" * 50)
    print(f"Total estimated hours: {total_hours}h")
    
    if args.dry_run:
        print(f"Dry run complete. {len(subtasks)} tasks would be created.")
    else:
        print(f"Created {created_count}/{len(subtasks)} tasks.")


if __name__ == "__main__":
    main()

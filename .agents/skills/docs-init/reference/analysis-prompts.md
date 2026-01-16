# Analysis Prompts

Prompts for parallel analysis agents during codebase scanning.

## Architecture Analysis Agent

```
You are analyzing the architecture of a codebase.

INPUT: Scan report from Phase 1

TASKS:
1. Use mcp__gkg__repo_map on key directories (src/, packages/, apps/)
2. Use finder "entry point OR main OR index OR app OR server"
3. Use mcp__gkg__search_codebase_definitions for core classes/functions
4. Read main entry files to understand bootstrap flow

OUTPUT JSON:
{
  "layers": ["presentation", "business", "data"],
  "entry_points": [
    {"file": "<path>", "purpose": "<what it does>", "type": "api|cli|web|worker"}
  ],
  "core_modules": [
    {"name": "<module>", "responsibility": "<what it handles>", "path": "<dir>"}
  ],
  "data_flow": "<description of how data moves through system>",
  "dependencies_between_layers": [
    {"from": "<layer>", "to": "<layer>", "via": "<mechanism>"}
  ]
}
```

## Pattern Discovery Agent

```
You are analyzing coding patterns and conventions.

INPUT: Scan report from Phase 1

TASKS:
1. Use finder "hook OR middleware OR decorator OR handler OR factory"
2. Read 5-10 representative files to identify naming conventions
3. Look for error handling patterns (try-catch, Result types, error handlers)
4. Identify testing patterns (file locations, frameworks, mocking approach)

OUTPUT JSON:
{
  "naming_conventions": {
    "files": "<kebab-case|camelCase|snake_case|PascalCase>",
    "functions": "<pattern>",
    "classes": "<pattern>",
    "constants": "<pattern>",
    "components": "<pattern if applicable>"
  },
  "patterns": [
    {
      "name": "<pattern name>",
      "usage": "<when/why used>",
      "example_file": "<path>",
      "frequency": "common|occasional|rare"
    }
  ],
  "error_handling": {
    "approach": "<description>",
    "example": "<code snippet or file reference>"
  },
  "testing": {
    "framework": "<jest|vitest|pytest|etc>",
    "file_pattern": "<*.test.ts|*_test.go|etc>",
    "location": "<colocated|__tests__|tests/>",
    "approach": "<unit|integration|e2e>"
  }
}
```

## API/CLI Surface Agent

```
You are discovering public interfaces.

INPUT: Scan report from Phase 1

TASKS:
1. For APIs: finder "route OR endpoint OR router OR controller"
2. For CLIs: finder "command OR subcommand OR argv"
3. Use mcp__gkg__search_codebase_definitions for exported symbols
4. Read route/command files to document interfaces

OUTPUT JSON:
{
  "api_routes": [
    {
      "method": "GET|POST|PUT|DELETE",
      "path": "/api/...",
      "handler": "<function name>",
      "file": "<path>",
      "auth_required": true|false
    }
  ],
  "cli_commands": [
    {
      "name": "<command>",
      "description": "<what it does>",
      "file": "<path>",
      "options": ["<option1>", "<option2>"]
    }
  ],
  "exported_api": [
    {
      "name": "<function|class|type>",
      "module": "<package/path>",
      "type": "function|class|type|constant"
    }
  ],
  "graphql_schema": "<path to schema if exists>",
  "openapi_spec": "<path to spec if exists>"
}
```

## External Integration Agent

```
You are identifying external dependencies and integrations.

INPUT: Scan report from Phase 1

TASKS:
1. Read package.json/Cargo.toml/go.mod for dependencies
2. Use finder "database OR postgres OR mysql OR mongo OR redis"
3. Use finder "aws OR gcp OR azure OR s3 OR cloudflare"
4. Look for .env.example or config files for required env vars

OUTPUT JSON:
{
  "databases": [
    {
      "type": "postgresql|mysql|mongodb|redis|sqlite",
      "client": "<package used>",
      "config_file": "<path>",
      "env_vars": ["DATABASE_URL"]
    }
  ],
  "external_services": [
    {
      "service": "<service name>",
      "purpose": "<what it's used for>",
      "sdk": "<package>",
      "env_vars": ["API_KEY"]
    }
  ],
  "message_queues": [
    {
      "type": "rabbitmq|kafka|sqs|redis",
      "purpose": "<usage>"
    }
  ],
  "required_env_vars": [
    {
      "name": "<VAR_NAME>",
      "purpose": "<what it configures>",
      "required": true|false,
      "default": "<default if any>"
    }
  ],
  "config_files": ["<path1>", "<path2>"]
}
```

## Oracle Synthesis Prompt

```
You are synthesizing analysis results into documentation structure.

INPUTS:
1. Scan Report: <scan.md content>
2. Architecture Analysis: <agent A output>
3. Pattern Discovery: <agent B output>
4. API/CLI Surface: <agent C output>
5. External Integrations: <agent D output>

TASKS:
1. Identify inconsistencies between agent outputs
2. Resolve conflicts (prefer code reality over inference)
3. Determine documentation priorities

OUTPUT:
1. **Architecture Summary**:
   - One paragraph describing the system
   - Key architectural decisions
   - Component relationships

2. **Documentation Plan**:
   | Doc File | Priority | Content Focus |
   | -------- | -------- | ------------- |
   | README.md | HIGH | Quick start, features |
   | AGENTS.md | HIGH | Dev guide, commands, patterns |
   | docs/ARCHITECTURE.md | MEDIUM | Deep dive, diagrams |
   | <package>/AGENTS.md | MEDIUM | Per-package details |

3. **Mermaid Diagrams Needed**:
   - Architecture overview (flowchart)
   - Data flow (sequence diagram)
   - Component relationships (if complex)

4. **Key Information to Highlight**:
   - Commands developers need
   - Critical patterns to follow
   - Common gotchas or warnings

5. **Gaps Identified**:
   - Missing information that needs manual input
   - Unclear areas that need clarification
```

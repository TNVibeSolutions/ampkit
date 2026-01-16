---
name: docs-init
description: Initialize documentation for a new codebase by scanning code structure, analyzing architecture, and generating initial docs following doc-mapping conventions. Use when onboarding a new project, bootstrapping docs for existing codebase, or creating initial AGENTS.md.
---

# Docs Init Pipeline

Bootstrap documentation from codebase analysis. One-time setup for new/undocumented projects.

## Pipeline Overview

```
REQUEST → SCAN → ANALYZE → GENERATE → REVIEW → APPLY
```

| Phase       | Action                            | Tools                                       |
| ----------- | --------------------------------- | ------------------------------------------- |
| 1. Scan     | Discover codebase structure       | `finder`                                    |
| 2. Analyze  | Understand architecture, patterns | `finder`                                    |
| 3. Generate | Create doc drafts                 | `Task` (parallel per doc type)              |
| 4. Review   | Validate against code             | `Oracle`                                    |
| 5. Apply    | Write docs with diagrams          | `create_file`, `edit_file`, `mermaid`       |

## Phase 1: Scan Codebase

### 1.1 Get Project Structure

```bash
# Use finder to understand structure
finder "project structure and key directories"
finder "existing documentation files"
finder "package.json or Cargo.toml or go.mod or pyproject.toml"
```

### 1.2 Identify Project Type

| Indicator            | Project Type       |
| -------------------- | ------------------ |
| `package.json`       | Node.js/TypeScript |
| `Cargo.toml`         | Rust               |
| `go.mod`             | Go                 |
| `pyproject.toml`     | Python             |
| `docker-compose.yml` | Multi-service      |
| `packages/` or `apps/` | Monorepo         |

### 1.3 Scan Report Template

Save to `history/docs-init/scan.md`:

```markdown
# Codebase Scan Report

## Project Type
<type> (monorepo / single-package / multi-service)

## Structure
<tree output from finder>

## Key Directories
| Directory | Purpose |
| --------- | ------- |
| src/      | ...     |
| packages/ | ...     |

## Existing Docs
- README.md: <exists/missing>
- AGENTS.md: <exists/missing>
- docs/: <exists/missing>

## Entry Points
- <main files, CLI entry, API routes>

## Dependencies
- <major deps from package.json/Cargo.toml/etc>
```

## Phase 2: Analyze Architecture

### 2.1 Parallel Analysis via Task

Spawn parallel sub-agents:

```
Task() → Agent A: Architecture analysis (entry points, data flow)
Task() → Agent B: Pattern discovery (common patterns, conventions)
Task() → Agent C: API/CLI surface (public interfaces)
Task() → Agent D: External integrations (DBs, APIs, services)
```

### 2.2 Analysis Prompts

**Architecture Agent:**
```
Understand the scan report and explore the codebase:
1. finder to understand key directories structure
2. finder "entry point OR main OR app OR server"
3. finder for core classes/functions

Return:
{
  "layers": ["presentation", "business", "data"],
  "entry_points": [{"file": "...", "purpose": "..."}],
  "core_modules": [{"name": "...", "responsibility": "..."}],
  "data_flow": "description of how data moves"
}
```

**Pattern Agent:**
```
Analyze coding patterns in the codebase:
1. finder "hook OR middleware OR decorator OR handler"
2. Look for consistent naming conventions
3. Identify error handling patterns

Return:
{
  "naming_conventions": {"files": "...", "functions": "...", "classes": "..."},
  "patterns": [{"name": "...", "usage": "...", "example_file": "..."}],
  "error_handling": "description",
  "testing_approach": "description"
}
```

**API/CLI Agent:**
```
Discover public interfaces:
1. finder "route OR endpoint OR command OR export"
2. finder for exported symbols
3. Understand API route files or CLI command files

Return:
{
  "api_routes": [{"method": "...", "path": "...", "handler": "..."}],
  "cli_commands": [{"name": "...", "description": "..."}],
  "exported_functions": [{"name": "...", "module": "..."}]
}
```

### 2.3 Oracle Synthesis

```
oracle(
  task: "Synthesize analysis into architecture overview",
  context: """
    Scan report: <scan.md>
    Architecture: <agent A output>
    Patterns: <agent B output>
    Interfaces: <agent C output>
    Integrations: <agent D output>
    
    Output:
    1. High-level architecture description
    2. Component relationships
    3. Key patterns and conventions
    4. Recommended doc structure
  """,
  files: ["history/docs-init/scan.md"]
)
```

Save to `history/docs-init/analysis.md`.

## Phase 3: Generate Docs

Based on analysis, determine which docs to create using doc-mapping conventions.

### 3.1 Doc Target Mapping

| Topic Type      | Target Files                              |
| --------------- | ----------------------------------------- |
| Architecture    | `AGENTS.md`, `docs/ARCHITECTURE.md`       |
| CLI commands    | `packages/cli/AGENTS.md`                  |
| SDK/API         | `packages/sdk/AGENTS.md`                  |
| Quick start     | `README.md`                               |
| Module dev      | `packages/sdk/docs/MODULE_DEVELOPMENT.md` |
| Troubleshooting | `docs/TROUBLESHOOTING.md`                 |
| Deployment      | `docs/DEPLOYMENT.md`                      |
| Migration       | `docs/MIGRATION.md`                       |

### 3.2 Parallel Doc Generation

Spawn Task per doc type:

```
Task() → README.md generator
Task() → AGENTS.md generator
Task() → docs/ARCHITECTURE.md generator
Task() → Package-specific AGENTS.md generators
```

### 3.3 Doc Templates

**README.md Template:**
```markdown
# <Project Name>

<One-line description>

## Features

- <Feature 1>
- <Feature 2>

## Quick Start

```bash
# Installation
<install command>

# Run
<run command>
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Development Guide](AGENTS.md)

## License

<license>
```

**AGENTS.md Template:**
```markdown
# AGENTS.md

Development guidelines for agents working on this codebase.

## Project Overview

<Brief description>

## Structure

<Directory structure with purposes>

## Commands

| Command | Purpose |
| ------- | ------- |
| `<cmd>` | ...     |

## Architecture

<High-level description>

## Patterns & Conventions

### Naming
<conventions>

### Error Handling
<approach>

### Testing
<approach>

## Development Workflow

<How to develop, test, deploy>
```

**docs/ARCHITECTURE.md Template:**
```markdown
# Architecture

## Overview

<High-level architecture description>

## Components

### <Component 1>
- **Purpose**: ...
- **Location**: ...
- **Dependencies**: ...

## Data Flow

<Description + mermaid diagram>

## External Dependencies

| Dependency | Purpose | Configuration |
| ---------- | ------- | ------------- |
| ...        | ...     | ...           |
```

## Phase 4: Review

### 4.1 Oracle Validation

```
oracle(
  task: "Review generated docs against codebase",
  context: """
    Generated docs: <list of docs>
    
    Validate:
    1. Accuracy - Does doc match code reality?
    2. Completeness - Any missing critical info?
    3. Consistency - Terms match across docs?
    4. Clarity - Would new dev understand?
    
    Output changes needed per doc.
  """,
  files: ["<generated docs>", "<key source files>"]
)
```

### 4.2 Review Checklist

```
- [ ] All entry points documented
- [ ] Commands table complete and tested
- [ ] Architecture diagram matches code
- [ ] Dependencies listed correctly
- [ ] Development workflow accurate
- [ ] No placeholder text remaining
```

## Phase 5: Apply

### 5.1 Create/Update Files

```
create_file for new docs
edit_file for existing docs (preserve existing content)
```

### 5.2 Architecture Diagrams

Use mermaid with citations:

```
mermaid(
  code: "flowchart TB\n  A[API] --> B[Service]\n  B --> C[(Database)]",
  citations: {
    "API": "file:///src/api/routes.ts#L1-L50",
    "Service": "file:///src/services/index.ts#L10-L100",
    "Database": "file:///src/db/client.ts"
  }
)
```

### 5.3 Monorepo Handling

For monorepos, create package-level AGENTS.md:

```bash
for package in packages/*; do
  # Create packages/<name>/AGENTS.md with package-specific info
done
```

## Concrete Example

User: "Initialize docs for this new project"

```
1. Scan:
   glob + Read → packages/cli, packages/sdk, apps/server
   glob "**/*.md" → only README.md exists (minimal)
   
2. Analyze (parallel):
   Agent A: Entry points at apps/server/src/index.ts, packages/cli/src/main.ts
   Agent B: Uses command pattern, kebab-case files, zod validation
   Agent C: REST API at /api/*, CLI has 5 commands
   Agent D: PostgreSQL, Redis cache
   
3. Oracle synthesizes:
   → 3-layer architecture: CLI → SDK → Server → DB
   → Recommend: AGENTS.md, docs/ARCHITECTURE.md, package AGENTS.md files
   
4. Generate (parallel):
   Task → README.md with quick start
   Task → Root AGENTS.md with overview
   Task → docs/ARCHITECTURE.md with diagrams
   Task → packages/cli/AGENTS.md
   Task → packages/sdk/AGENTS.md
   
5. Review:
   Oracle validates all docs match code
   
6. Apply:
   create_file for each doc
   mermaid for architecture diagrams
```

## Tool Quick Reference

| Goal                  | Tool                                    |
| --------------------- | --------------------------------------- |
| Find code/structure   | `finder`                                |
| Parallel analysis     | `Task` (spawn multiple)                 |
| Synthesis             | `Oracle`                                |
| Create docs           | `create_file`                           |
| Update docs           | `edit_file`                             |
| Architecture diagrams | `mermaid` with citations                |

## Quality Checklist

```
- [ ] Scan complete (structure, deps, entry points)
- [ ] All layers analyzed (architecture, patterns, APIs)
- [ ] Docs match doc-mapping conventions
- [ ] Diagrams have code citations
- [ ] Oracle validated against code
- [ ] No placeholder text remaining
- [ ] Commands tested and working
```

## Troubleshooting

**Large codebase**: Focus on `packages/` or `src/` first, expand later

**No clear entry point**: Look for `main`, `index`, `app`, `server` files

**Mixed languages**: Create separate sections per language in AGENTS.md

**Existing partial docs**: Read first, extend rather than replace

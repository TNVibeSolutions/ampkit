# Documentation Templates

Templates for generating initial docs. Copy and adapt based on codebase analysis.

## File Location Mapping

| Doc Type        | File Path                          | When to Create             |
| --------------- | ---------------------------------- | -------------------------- |
| Project README  | `./README.md`                      | Always                     |
| Root Dev Guide  | `./AGENTS.md`                      | Always                     |
| Architecture    | `./docs/ARCHITECTURE.md`           | Always                     |
| Troubleshooting | `./docs/TROUBLESHOOTING.md`        | If common issues exist     |
| Deployment      | `./docs/DEPLOYMENT.md`             | If deployment steps needed |
| Migration       | `./docs/MIGRATION.md`              | If breaking changes exist  |
| CLI Package     | `./packages/cli/AGENTS.md`         | If CLI exists              |
| SDK Package     | `./packages/sdk/AGENTS.md`         | If SDK exists              |
| Any Package     | `./packages/<name>/AGENTS.md`      | Per package in monorepo    |
| App             | `./apps/<name>/AGENTS.md`          | Per app in monorepo        |

### Directory Structure Example

```
project-root/
├── README.md                      # Quick start, features
├── AGENTS.md                      # Root dev guide
├── docs/
│   ├── ARCHITECTURE.md            # System design, diagrams
│   ├── DEPLOYMENT.md              # Deploy instructions
│   ├── TROUBLESHOOTING.md         # Common issues
│   └── MIGRATION.md               # Breaking changes
├── packages/
│   ├── cli/
│   │   └── AGENTS.md              # CLI-specific guide
│   └── sdk/
│       └── AGENTS.md              # SDK-specific guide
└── apps/
    └── server/
        └── AGENTS.md              # Server-specific guide
```

## README.md

```markdown
# {PROJECT_NAME}

{ONE_LINE_DESCRIPTION}

## Features

- {FEATURE_1}
- {FEATURE_2}
- {FEATURE_3}

## Quick Start

### Prerequisites

- {RUNTIME} >= {VERSION}
- {OTHER_PREREQ}

### Installation

```bash
{INSTALL_COMMAND}
```

### Usage

```bash
{RUN_COMMAND}
```

## Documentation

- [Development Guide](AGENTS.md) - For contributors
- [Architecture](docs/ARCHITECTURE.md) - System design
- [API Reference](docs/API.md) - API documentation

## Development

```bash
# Install dependencies
{DEV_INSTALL}

# Run tests
{TEST_COMMAND}

# Build
{BUILD_COMMAND}
```

## License

{LICENSE}
```

## AGENTS.md (Root)

```markdown
# AGENTS.md

Development guidelines for agents working on this codebase.

## Project Overview

{PROJECT_DESCRIPTION}

**Type**: {PROJECT_TYPE} (monorepo / single-package / CLI / library / service)
**Language**: {LANGUAGE}
**Runtime**: {RUNTIME} >= {VERSION}

## Structure

```
{DIRECTORY_TREE}
```

| Directory | Purpose |
| --------- | ------- |
| {DIR_1}   | {PURPOSE_1} |
| {DIR_2}   | {PURPOSE_2} |

## Commands

| Command | Purpose |
| ------- | ------- |
| `{CMD_1}` | {PURPOSE_1} |
| `{CMD_2}` | {PURPOSE_2} |
| `{CMD_3}` | {PURPOSE_3} |

## Architecture

{ARCHITECTURE_OVERVIEW}

### Components

- **{COMPONENT_1}**: {RESPONSIBILITY}
- **{COMPONENT_2}**: {RESPONSIBILITY}

### Data Flow

{DATA_FLOW_DESCRIPTION}

## Patterns & Conventions

### Naming

- **Files**: {FILE_NAMING} (e.g., kebab-case)
- **Functions**: {FUNCTION_NAMING} (e.g., camelCase)
- **Classes**: {CLASS_NAMING} (e.g., PascalCase)
- **Constants**: {CONSTANT_NAMING} (e.g., SCREAMING_SNAKE_CASE)

### Error Handling

{ERROR_HANDLING_APPROACH}

### Testing

{TESTING_APPROACH}

- Test files: `{TEST_PATTERN}`
- Run tests: `{TEST_COMMAND}`

## Development Workflow

1. {STEP_1}
2. {STEP_2}
3. {STEP_3}

## Dependencies

### Core

| Package | Purpose |
| ------- | ------- |
| {DEP_1} | {PURPOSE_1} |
| {DEP_2} | {PURPOSE_2} |

### Dev

| Package | Purpose |
| ------- | ------- |
| {DEV_DEP_1} | {PURPOSE_1} |
```

## docs/ARCHITECTURE.md

```markdown
# Architecture

## Overview

{HIGH_LEVEL_ARCHITECTURE}

## System Diagram

```mermaid
{ARCHITECTURE_DIAGRAM}
```

## Components

### {COMPONENT_1}

- **Purpose**: {PURPOSE}
- **Location**: `{PATH}`
- **Entry Point**: `{FILE}`
- **Dependencies**: {DEPS}

**Key Files**:
- `{FILE_1}`: {DESCRIPTION}
- `{FILE_2}`: {DESCRIPTION}

### {COMPONENT_2}

...

## Data Flow

{DATA_FLOW_DESCRIPTION}

```mermaid
sequenceDiagram
    {SEQUENCE_DIAGRAM}
```

## External Dependencies

| Service | Purpose | Configuration |
| ------- | ------- | ------------- |
| {SERVICE_1} | {PURPOSE} | {CONFIG_FILE} |
| {SERVICE_2} | {PURPOSE} | {CONFIG_FILE} |

## Configuration

| Env Variable | Purpose | Default |
| ------------ | ------- | ------- |
| {ENV_1} | {PURPOSE} | {DEFAULT} |
| {ENV_2} | {PURPOSE} | {DEFAULT} |

## Deployment

{DEPLOYMENT_OVERVIEW}

See [Deployment Guide](DEPLOYMENT.md) for details.
```

## Package AGENTS.md

For monorepo packages:

```markdown
# {PACKAGE_NAME} AGENTS.md

## Purpose

{PACKAGE_PURPOSE}

## Public API

### Functions

| Function | Description |
| -------- | ----------- |
| `{FUNC_1}` | {DESC} |
| `{FUNC_2}` | {DESC} |

### Types

| Type | Description |
| ---- | ----------- |
| `{TYPE_1}` | {DESC} |
| `{TYPE_2}` | {DESC} |

## Usage

```{LANGUAGE}
{USAGE_EXAMPLE}
```

## Internal Architecture

{INTERNAL_DESCRIPTION}

## Development

```bash
# Run tests
{TEST_COMMAND}

# Build
{BUILD_COMMAND}
```

## Dependencies

This package depends on:
- `{DEP_1}`: {WHY}

This package is used by:
- `{USER_1}`: {HOW}
```

## CLI AGENTS.md

For CLI packages:

```markdown
# CLI AGENTS.md

## Commands

| Command | Description | Example |
| ------- | ----------- | ------- |
| `{CMD_1}` | {DESC} | `{EXAMPLE}` |
| `{CMD_2}` | {DESC} | `{EXAMPLE}` |

## Command Details

### `{CMD_1}`

{DETAILED_DESCRIPTION}

**Options**:

| Flag | Description | Default |
| ---- | ----------- | ------- |
| `{FLAG_1}` | {DESC} | {DEFAULT} |

**Examples**:

```bash
{EXAMPLE_1}
{EXAMPLE_2}
```

## Adding New Commands

1. Create command file in `{COMMANDS_DIR}`
2. Follow pattern from `{EXAMPLE_COMMAND}`
3. Register in `{REGISTRY_FILE}`
4. Add tests in `{TEST_DIR}`
```

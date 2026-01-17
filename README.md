<p align="center">
  <h1 align="center">🤖 AmpKit</h1>
  <p align="center">
    <strong>Multi-Agent Skills for Amp</strong>
  </p>
  <p align="center">
    A collection of skills for multi-agent coordination, planning, and autonomous execution using Agent Mail.
  </p>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage-guide">Usage Guide</a> •
  <a href="#skills">Skills</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#license">License</a>
</p>

---

## Sponsor

[![VibeCodeCheap](assets/vibecodecheap-sponsor-en.png)](https://vibecodecheap.com/)

This project is sponsored by VibeCodeCheap - Affordable Claude Code & AI Agents.

VibeCodeCheap provides access to premium LLM models like Claude Sonnet 4.5, Opus 4.5, Gemini 3 Pro through a unified OpenAI & Claude API compatible interface. Perfect for Claude Code and all AI coding agents.

Start coding smarter: <https://vibecodecheap.com/>

---


## Skills

| Skill | Description |
|:------|:------------|
| `docs-init` | Initialize documentation for new codebases by scanning and analyzing architecture |
| `brainstorming` | Collaborative solution brainstorming with brutal honesty, multi-approach analysis |
| `planning` | Generate comprehensive plans through discovery, synthesis, verification, and decomposition |
| `file-beads` | Convert plans into structured Beads issues with proper dependencies |
| `orchestrator` | Plan and coordinate multi-agent bead execution with parallel workers |
| `worker` | Execute beads autonomously within a track with context persistence via Agent Mail |
| `issue-resolution` | Systematically diagnose and fix bugs through triage, reproduction, root cause analysis |
| `knowledge` | Extract knowledge from Amp threads and update project documentation |

## Installation

> 📋 **Prerequisites**: See [Requirements](#requirements) for detailed setup of Agent Mail, Beads CLI, and other dependencies.

### Quick Start

```bash
# Install all skills
amp skill add TNVibeSolutions/ampkit

# Install globally (available in all projects)
amp skill add TNVibeSolutions/ampkit --overwrite --target ~/.config/amp/skills/
```

### Install Specific Skills

```bash
amp skill add TNVibeSolutions/ampkit/docs-init
amp skill add TNVibeSolutions/ampkit/brainstorming
amp skill add TNVibeSolutions/ampkit/planning
amp skill add TNVibeSolutions/ampkit/file-beads
amp skill add TNVibeSolutions/ampkit/orchestrator
amp skill add TNVibeSolutions/ampkit/worker
amp skill add TNVibeSolutions/ampkit/issue-resolution
amp skill add TNVibeSolutions/ampkit/knowledge
```

## Usage Guide

### Workflow Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  planning   │ ──▶ │ orchestrator │ ──▶ │   worker    │
│             │     │              │     │    (×N)     │
└─────────────┘     └──────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│ file-beads  │     │  knowledge  │
└─────────────┘     └─────────────┘

┌─────────────────┐     ┌─────────────┐
│issue-resolution │     │  docs-init  │
│  (bugs/errors)  │     │ (new proj)  │
└─────────────────┘     └─────────────┘
```

### Step-by-Step Guide

#### 1️⃣ Initialize Project Structure

First, initialize the project structure using `bd`:

```bash
bd init --no-db
```

#### 2️⃣ Initialize Documentation (New Project)

For new projects, use `docs-init` to generate initial documentation:

```
Use docs-init skill to initialize documentation for this project
```

#### 3️⃣ Brainstorm Ideas (Optional)

Before planning, use `brainstorming` skill to explore approaches:

```
Use brainstorming skill to explore: [problem/idea description]
```

- Provides multi-angle analysis with pros/cons
- Gives honest recommendations based on engineering principles
- Helps clarify requirements before formal planning

#### 4️⃣ Plan Feature

Open a new session in **Smart mode** and use `planning` skill:

```
Use planning skill to plan feature: [feature description]
```

- Review each planning step carefully
- Continue prompting to update if adjustments needed
- Use `bv` CLI to preview created tasks
- When planning is complete, **handoff** to a new thread

#### 5️⃣ Execute Feature

In the new thread, call `orchestrator` skill:

```
Use orchestrator skill to execute the feature according to the plan
```

> 💡 **Tip**: Use **Rush mode** to save tokens, or **Smart mode** for tighter control

The orchestrator will:
- Coordinate workers in parallel or sequential execution
- Track progress and handle dependencies automatically

#### 6️⃣ Test & Fix Issues

After completion, test thoroughly:

| Issue Type | Action |
|:-----------|:-------|
| Minor issues | Handoff and request check/fix directly |
| Critical issues | Use `issue-resolution` skill for deep analysis |

```
Use issue-resolution skill to debug error: [error description]
```

#### 7️⃣ Update Documentation

After each feature, sync documentation with `knowledge` skill:

```
Use knowledge skill to update docs with recent changes
```

---

## Skill Details

| # | Skill | Purpose |
|:-:|:------|:--------|
| 1 | **docs-init** | Initializes documentation for new codebases |
| 2 | **brainstorming** | Explores ideas with brutal honesty and multi-approach analysis |
| 3 | **planning** | Creates execution plans with beads, tracks, and dependencies |
| 4 | **file-beads** | Converts plans into structured Beads issues |
| 5 | **orchestrator** | Spawns parallel worker agents and monitors progress |
| 6 | **worker** | Executes beads within assigned tracks using Agent Mail |
| 7 | **issue-resolution** | Handles bugs that arise during execution |
| 8 | **knowledge** | Extracts learnings from threads and updates documentation |

---

## Requirements

| Dependency | Purpose |
|:-----------|:--------|
| [Agent Mail MCP](#mcp-agent-mail) | Inter-agent communication |
| [Beads CLI](#beads-cli) | Issue tracking (`bd`) |
| [Beads Viewer](#beads-viewer) | Visualization and planning (`bv`) |
| [Exa MCP Server](#exa-mcp-server) | Web search for planning *(optional)* |

### MCP Agent Mail

[MCP Agent Mail](https://github.com/tuong-nguyen-vn/mcp_agent_mail) enables inter-agent communication for orchestrator and worker skills.

<details>
<summary><strong>📦 Installation</strong></summary>

**Prerequisites**: Python >= 3.14, uv, Git

```bash
# Install uv if not installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repo
git clone https://github.com/tuong-nguyen-vn/mcp_agent_mail.git
cd mcp_agent_mail

# Create venv with Python 3.14
uv venv --python python3.14
source .venv/bin/activate

# Install
uv pip install -e .
```

**Global Setup** (choose one):

*Option 1: Symlink (recommended)*
```bash
sudo ln -sf $(pwd)/.venv/bin/am /usr/local/bin/am
sudo ln -sf $(pwd)/.venv/bin/mcp-agent-mail /usr/local/bin/mcp-agent-mail
```

*Option 2: Add to PATH*
```bash
echo "export PATH=\"$(pwd)/.venv/bin:\$PATH\"" >> ~/.zshrc
source ~/.zshrc
```

**Verify**:
```bash
am --help
am health_check '{}'
```

For full CLI documentation, see [CLI_INSTALLATION.md](https://github.com/tuong-nguyen-vn/mcp_agent_mail/blob/main/docs/CLI_INSTALLATION.md).

</details>

### Beads CLI

[Beads](https://github.com/steveyegge/beads) is a CLI for issue tracking and task management.

<details>
<summary><strong>📦 Installation</strong></summary>

**Linux/macOS/FreeBSD:**
```bash
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
```

**npm:**
```bash
npm install -g @beads/bd
```

**Homebrew:**
```bash
brew install steveyegge/beads/bd
```

**Go:**
```bash
go install github.com/steveyegge/beads/cmd/bd@latest
```

**Initialize** (run once per project):
```bash
bd init --no-db --skip-hooks --skip-merge-driver
```

**Verify**:
```bash
bd --help
bd list
```

</details>

### Beads Viewer

[Beads Viewer](https://github.com/Dicklesworthstone/beads_viewer) provides visualization and planning capabilities.

<details>
<summary><strong>📦 Installation</strong></summary>

**Linux/macOS:**
```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.sh?$(date +%s)" | bash
```

**Windows (PowerShell):**
```powershell
irm "https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.ps1" | iex
```

**Verify**:
```bash
bv --help
bv --robot-triage
```

</details>

### Exa MCP Server

[Exa](https://exa.ai/) provides web search capabilities for the planning skill.

<details>
<summary><strong>📦 Setup</strong></summary>

1. Sign up at [exa.ai](https://exa.ai/) and get API key from dashboard

2. Add to Amp's MCP config (`~/.config/amp/mcp.json`):

```json
{
  "mcpServers": {
    "exa": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "exa-mcp-server",
        "tools=web_search_exa,get_code_context_exa,crawling_exa"
      ],
      "env": {
        "EXA_API_KEY": "your-exa-api-key"
      }
    }
  }
}
```

</details>

---

## License

MIT

---
name: skill-help
description: Display Claude Code configuration dashboard with Rich terminal formatting. Shows agents, commands, hooks (on/off), MCPs (on/off), and skills. Use when user says "show config", "list agents", "what MCPs do I have", "show help", "claude config", or "skill-help".
---

# Skill Help - Claude Code Configuration Dashboard

Display a comprehensive dashboard of your Claude Code configuration using Rich terminal formatting.

## Quick Start

Run the Python script to display your configuration:

```bash
~/.local/bin/uv run --with rich python ~/.claude/skills/skill-help/scripts/show_config.py
```

## What It Shows

The dashboard displays:

1. **Agents** - Custom agents in `~/.claude/agents/`
2. **Commands** - Slash commands in `~/.claude/commands/`
3. **Skills** - Skills in `~/.claude/skills/`
4. **Hooks** - Configured hooks with on/off status
5. **MCP Servers** - MCP servers with enabled/disabled status
6. **Plugins** - Enabled Claude plugins
7. **Permissions** - Allowed bash commands and tool permissions

## Instructions

When the user asks to see their Claude configuration, run the show_config.py script:

```bash
~/.local/bin/uv run --with rich python ~/.claude/skills/skill-help/scripts/show_config.py
```

The script reads from:
- `~/.claude/settings.json` - Main settings, hooks, MCPs
- `~/.claude/agents/` - Agent definitions
- `~/.claude/commands/` - Command definitions
- `~/.claude/skills/` - Skill definitions

## Customization

The script uses Rich styling:
- Green ON / Red OFF for status indicators
- Tables with rounded borders for organized display
- Color-coded sections (cyan for titles, yellow for commands, etc.)
- Summary panel at the top showing counts

## Requirements

Uses `uv run --with rich` to automatically install the rich dependency on demand

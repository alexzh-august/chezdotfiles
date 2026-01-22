# Team Dotfiles for AI Development Tools

> **Status**: Personal experimentation phase
> **Future home**: `fractal-protocol/chezmoi` + `fractal-protocol/team-dotfiles`

## What

A version-controlled, team-shareable collection of configurations for AI coding assistants and development tools.

### Implemented

| Directory | Tool | Purpose | Status |
|-----------|------|---------|--------|
| `dot_claude/` | [Claude Code](https://claude.ai/code) | Agents, commands, skills, plugins, hooks | **Ready** |
| `dot_config/ghostty/` | [Ghostty](https://ghostty.org) | Terminal emulator (Claude-themed) | **Ready** |
| `dot_config/starship/` | [Starship](https://starship.rs) | Cross-shell prompt | **Ready** |
| `shell/zsh/` | Zsh | Shell configuration | **Ready** |
| `patterns/databricks/` | Databricks SDK | Code patterns & anti-patterns | **Ready** |

### Planned (Placeholders)

| Directory | Tool | Purpose | Status |
|-----------|------|---------|--------|
| `dot_gemini/` | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Gemini Code configs | Placeholder |
| `dot_cursor/` | [Cursor](https://cursor.com) | AI-powered IDE settings | Placeholder |
| `dot_vscode/` | [VS Code](https://code.visualstudio.com) | Extensions, settings, tasks | Placeholder |
| `dot_antigravity/` | [Antigravity](https://antigravity.dev) | Agent configs | Placeholder |
| `patterns/python/` | Python | Best practices patterns | Placeholder |
| `patterns/typescript/` | TypeScript | Best practices patterns | Placeholder |
| `shell/bash/` | Bash | Shell configuration | Placeholder |

## Why

**Problem**: Each engineer manually downloads and configures tools like:
- Claude Code plugins (e.g., [PR Review Toolkit](https://www.claudepluginhub.com/plugins/anthropics-pr-review-toolkit-plugins-pr-review-toolkit))
- Custom agents and commands
- Terminal optimizations for AI workflows
- Code pattern detectors

**Solution**: One engineer sets it up, commits it, team reviews it, everyone gets it:
```
Engineer discovers useful Claude agent
    ↓
Adds to dot_claude/agents/, opens PR
    ↓
Team reviews for security/quality
    ↓
Merged → Everyone pulls → Instant team-wide adoption
```

## Where

### Repository Structure (Actual)

```
chezdotfiles/                    # This repo (chezmoi fork + dotfiles)
├── CLAUDE.md                    # This file
├── dotfiles/                    # Team-shareable configurations
│   ├── dot_claude/              # → ~/.claude/
│   │   ├── agents/              # Custom agents (9 agents)
│   │   ├── commands/            # Slash commands (17 commands)
│   │   ├── context/             # Context files
│   │   │   ├── llms/            # LLM context caches
│   │   │   └── coderabbit.yaml  # CodeRabbit config template
│   │   ├── hooks/               # Automation scripts
│   │   ├── plugins/             # Claude Code plugins
│   │   │   └── pr-review-toolkit/  # 6-agent PR review suite
│   │   ├── settings/            # (placeholder for settings.json)
│   │   └── skills/              # Skill modules (26+ skills)
│   │   │   └── coderabbit.md    # CodeRabbit CLI integration
│   ├── dot_config/
│   │   ├── ghostty/config       # Claude-themed terminal
│   │   └── starship/starship.toml  # Cross-shell prompt
│   ├── shell/
│   │   └── zsh/
│   │       ├── zshrc            # Main zsh configuration
│   │       ├── aliases.sh       # Shared aliases
│   │       ├── functions.sh     # Shared functions
│   │       └── lazy.sh          # Lazy-loaded tools
│   ├── patterns/
│   │   └── databricks/          # Databricks SDK patterns
│   │       ├── authentication.yaml
│   │       ├── mcp_integration.yaml
│   │       ├── sql_execution.yaml
│   │       ├── unity_catalog.yaml
│   │       └── templates.py     # Code generators
│   ├── dot_gemini/              # (placeholder)
│   ├── dot_cursor/              # (placeholder)
│   ├── dot_vscode/              # (placeholder)
│   └── dot_antigravity/         # (placeholder)
├── internal/                    # Chezmoi source code (Go)
└── [chezmoi source files]
```

### Target Locations (on user machines)

| Source | Destination | Method |
|--------|-------------|--------|
| `dotfiles/dot_claude/*` | `~/.claude/*` | symlink or chezmoi |
| `dotfiles/dot_config/ghostty/*` | `~/.config/ghostty/*` | symlink or chezmoi |
| `dotfiles/dot_config/starship/*` | `~/.config/starship.toml` | symlink or chezmoi |
| `dotfiles/shell/zsh/*` | sourced from `~/.zshrc` | source or chezmoi |
| `dotfiles/patterns/*` | project `.patterns/` or global | copy/symlink |

## When

### Use team configs when:
- Starting on a new machine
- New team member onboarding
- Standardizing tool configurations
- Sharing discovered optimizations

### Update team configs when:
- You find a useful Claude agent/command
- You optimize terminal performance
- You discover a code anti-pattern worth catching
- A tool has breaking changes requiring config updates

## How

### For Personal Use (Now)

```bash
# Clone your fork
git clone git@github.com:alexzh-august/chezdotfiles.git ~/chezdotfiles

# Symlink configs you want to use
ln -sf ~/chezdotfiles/dotfiles/dot_claude/agents ~/.claude/agents
ln -sf ~/chezdotfiles/dotfiles/dot_claude/commands ~/.claude/commands
ln -sf ~/chezdotfiles/dotfiles/dot_claude/skills ~/.claude/skills
ln -sf ~/chezdotfiles/dotfiles/dot_claude/plugins ~/.claude/plugins
ln -sf ~/chezdotfiles/dotfiles/dot_config/ghostty/config ~/.config/ghostty/config
```

### For Team Use (Future)

```bash
# Team member initial setup
chezmoi init fractal-protocol/team-dotfiles --apply

# Pull latest team configs
chezmoi update

# Contribute new config
chezmoi cd
git checkout -b add-pr-review-agent
git add dot_claude/agents/pr-review.md
git commit -m "feat: Add PR review agent"
git push -u origin add-pr-review-agent
# Open PR for team review
```

### Adding a New Claude Agent

1. Create agent file:
```bash
cat > dotfiles/dot_claude/agents/pr-reviewer.md << 'EOF'
# PR Reviewer Agent

Reviews pull requests for code quality, security, and best practices.

## Instructions
- Check for security vulnerabilities
- Verify test coverage
- Ensure documentation is updated
- Flag breaking changes
EOF
```

2. Test locally:
```bash
ln -sf ~/chezdotfiles/dotfiles/dot_claude/agents ~/.claude/agents
claude  # verify agent appears with /agents
```

3. Commit and PR:
```bash
git add dotfiles/dot_claude/agents/pr-reviewer.md
git commit -m "feat(agents): Add PR reviewer agent"
```

### Using the PR Review Toolkit

The included `pr-review-toolkit` plugin provides 6 specialized agents:

| Agent | Focus |
|-------|-------|
| `code-reviewer` | General code quality, CLAUDE.md compliance |
| `code-simplifier` | Code clarity, refactoring |
| `comment-analyzer` | Documentation accuracy |
| `pr-test-analyzer` | Test coverage quality |
| `silent-failure-hunter` | Error handling |
| `type-design-analyzer` | Type design and invariants |

**Usage:**
```bash
# Full review with all agents
/pr-review-toolkit:review-pr

# Specific aspects only
/pr-review-toolkit:review-pr tests errors

# Parallel execution
/pr-review-toolkit:review-pr all parallel
```

### Using CodeRabbit CLI

[CodeRabbit](https://coderabbit.ai) provides AI-powered code review via CLI, integrated with Claude Code workflows.

**Installation:**
```bash
# Install CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Authenticate
coderabbit auth login

# Verify
coderabbit auth status
```

**Review Modes:**
```bash
# Interactive review (rich formatting)
coderabbit review

# Plain text (for AI agents/token efficiency)
coderabbit review --plain

# Minimal output (maximum token efficiency)
coderabbit review --prompt-only
```

**Review Scopes:**
```bash
# All changes (default)
coderabbit review --type all

# Only committed changes
coderabbit review --type committed

# Only uncommitted changes
coderabbit review --type uncommitted

# Compare against specific branch
coderabbit review --base main
```

**Autonomous Development Loop:**
```
Write code → coderabbit review --plain → Apply feedback → Re-review → Commit
```

Example prompt for Claude Code:
```
Implement [feature]. After each change, run `coderabbit review --plain`
and apply the suggestions until the code passes review.
```

**Configuration:**
- Skill: `dotfiles/dot_claude/skills/coderabbit.md`
- Config template: `dotfiles/dot_claude/context/coderabbit.yaml`

**Rate Limits:** Free=2/hr, Trial=5/hr, Pro=8/hr per seat

---

## Patterns Directory

Code patterns for static analysis and AI-assisted review:

```yaml
# patterns/databricks/authentication.yaml
patterns:
  - name: hardcoded-token
    severity: critical
    description: "Never hardcode Databricks tokens"
    antipattern: 'token\s*=\s*["\'][^"\']+["\']'
    fix: "Use environment variables or secret management"

  - name: use-oauth
    severity: warning
    description: "Prefer OAuth over PAT for production"
    pattern: 'DatabricksOAuth'
    antipattern: 'personal_access_token'
```

---

## Future: Agent Client Protocol

This structure is designed to extend to any [Agent Client Protocol](https://agentclientprotocol.com/) compatible tools:

```
dotfiles/
├── dot_claude/      # Anthropic Claude (IMPLEMENTED)
├── dot_gemini/      # Google Gemini (placeholder)
├── dot_copilot/     # GitHub Copilot (future)
├── dot_codeium/     # Codeium (future)
├── dot_continue/    # Continue.dev (future)
└── dot_aider/       # Aider (future)
```

Each follows the same pattern:
- `agents/` - Custom agent definitions
- `commands/` - Slash commands
- `settings/` - Tool-specific settings
- `context/` - Cached context for AI

---

## Security Considerations

**DO commit:**
- Agent definitions (public instructions)
- Command templates
- Non-sensitive settings
- Pattern definitions

**DO NOT commit:**
- API keys or tokens
- Personal access tokens
- OAuth secrets
- Sensitive file paths

For secrets, use chezmoi templates (future):
```
# dotfiles/dot_claude/settings.json.tmpl
{
  "apiKey": "{{ .anthropic_api_key }}"
}
```

---

## Contributing

1. Fork this repo (personal) or branch (team)
2. Make changes in `dotfiles/`
3. Test locally by symlinking
4. Open PR with clear description
5. Get team review
6. Merge and notify team to pull

# Team Dotfiles for AI Development Tools

> **Status**: Personal experimentation phase
> **Future home**: `fractal-protocol/chezmoi` + `fractal-protocol/team-dotfiles`

## What

A version-controlled, team-shareable collection of configurations for AI coding assistants and development tools:

| Directory | Tool | Purpose |
|-----------|------|---------|
| `dot_claude/` | [Claude Code](https://claude.com/claude-code) | Agents, commands, MCP settings |
| `dot_gemini/` | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Gemini Code configs |
| `dot_cursor/` | [Cursor](https://cursor.com) | AI-powered IDE settings |
| `dot_vscode/` | [VS Code](https://code.visualstudio.com) | Extensions, settings, tasks |
| `dot_antigravity/` | [Antigravity](https://antigravity.dev) | Agent configs |
| `dot_config/ghostty/` | [Ghostty](https://ghostty.org) | Terminal emulator |
| `dot_config/starship/` | [Starship](https://starship.rs) | Cross-shell prompt |
| `shell/` | zsh/bash | Shell configurations |
| `patterns/` | Static analysis | Code patterns & anti-patterns |

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

### Repository Structure

```
chezdotfiles/                    # This repo (chezmoi fork + dotfiles)
├── CLAUDE.md                    # This file
├── dotfiles/                    # Team-shareable configurations
│   ├── dot_claude/              # → ~/.claude/
│   │   ├── agents/              # Custom agents (*.md)
│   │   ├── commands/            # Slash commands (*.md)
│   │   ├── context/llms/        # LLM context caches (*.txt)
│   │   └── settings/            # settings.json, etc.
│   ├── dot_gemini/              # → ~/.gemini/
│   ├── dot_cursor/              # → ~/.cursor/
│   ├── dot_vscode/              # → ~/.vscode/
│   ├── dot_antigravity/         # → ~/.antigravity/
│   ├── dot_config/
│   │   ├── ghostty/             # → ~/.config/ghostty/
│   │   └── starship/            # → ~/.config/starship.toml
│   ├── shell/
│   │   ├── zsh/                 # → ~/.zshrc (or sourced)
│   │   └── bash/                # → ~/.bashrc (or sourced)
│   └── patterns/                # Code pattern detectors
│       ├── databricks/          # Databricks SDK patterns
│       ├── python/              # Python best practices
│       └── typescript/          # TypeScript patterns
├── internal/                    # Chezmoi source code (Go)
└── [chezmoi source files]
```

### Target Locations (on user machines)

| Source | Destination | Method |
|--------|-------------|--------|
| `dotfiles/dot_claude/*` | `~/.claude/*` | chezmoi apply |
| `dotfiles/dot_config/ghostty/*` | `~/.config/ghostty/*` | chezmoi apply |
| `dotfiles/shell/zsh/*` | sourced from `~/.zshrc` | chezmoi + source |
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

# Symlink or copy configs you want to use
ln -sf ~/chezdotfiles/dotfiles/dot_claude/agents ~/.claude/agents
ln -sf ~/chezdotfiles/dotfiles/dot_config/ghostty/config ~/.config/ghostty/config

# Or use chezmoi to manage (from dotfiles/ subdirectory)
chezmoi add ~/chezdotfiles/dotfiles/dot_claude
```

### For Team Use (Future)

```bash
# Team member initial setup
chezmoi init fractal-protocol/team-dotfiles --apply

# Pull latest team configs
chezmoi update

# Contribute new config
chezmoi cd
# edit files
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
ln -sf ~/chezdotfiles/dotfiles/dot_claude/agents/pr-reviewer.md ~/.claude/agents/
claude  # verify agent appears with /agents
```

3. Commit and PR:
```bash
git add dotfiles/dot_claude/agents/pr-reviewer.md
git commit -m "feat(agents): Add PR reviewer agent"
```

### Adding Terminal Optimizations

1. Edit Ghostty config:
```bash
vim dotfiles/dot_config/ghostty/config
```

2. Test:
```bash
cp dotfiles/dot_config/ghostty/config ~/.config/ghostty/config
# Restart Ghostty or Cmd+Shift+R
```

3. Document the optimization in commit message

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
├── dot_claude/      # Anthropic Claude
├── dot_gemini/      # Google Gemini
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

Use chezmoi templates for secrets:
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

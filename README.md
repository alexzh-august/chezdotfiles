# ![chezmoi logo](assets/images/logo-144px.svg) chezmoi - Team Dotfiles Edition

[![GitHub Release](https://img.shields.io/github/release/twpayne/chezmoi.svg)](https://github.com/twpayne/chezmoi/releases)

Manage your dotfiles across multiple diverse machines, securely.

## Team Dotfiles

This fork extends chezmoi with **team-shareable configurations** for AI development tools.

**[See CLAUDE.md for the complete guide →](CLAUDE.md)**

### Quick Start

```bash
# Clone and symlink Claude Code configs
git clone git@github.com:alexzh-august/chezdotfiles.git ~/chezdotfiles
ln -sf ~/chezdotfiles/dotfiles/dot_claude/agents ~/.claude/agents
ln -sf ~/chezdotfiles/dotfiles/dot_claude/skills ~/.claude/skills
```

### What's Included

| Directory | Contents |
|-----------|----------|
| `dotfiles/dot_claude/` | 9 agents, 17 commands, 25+ skills, pr-review-toolkit plugin |
| `dotfiles/dot_config/ghostty/` | Claude-themed terminal config |
| `dotfiles/patterns/databricks/` | Databricks SDK code patterns |

## Original chezmoi Documentation

chezmoi's documentation is at [chezmoi.io](https://chezmoi.io/).

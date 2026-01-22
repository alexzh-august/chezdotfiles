# Git Workflows - Claude Code Custom Commands

Custom Claude Code commands for advanced git workflows that aren't available through standard GitHub UI.

## Commands

| Command | Description |
|---------|-------------|
| `/private-fork` | Create a private repository from a public repo while maintaining upstream connection |
| `/safe-pull` | Preview upstream changes with dry-run before actually pulling |

## Usage

### Private Fork
```
/private-fork https://github.com/owner/public-repo
```

Creates a private copy of a public repository. Useful when:
- You need to work on a public project privately
- GitHub doesn't allow private forks of public repos
- You want to maintain ability to pull upstream changes

### Safe Pull
```
/safe-pull                    # Default: upstream, current branch
/safe-pull upstream main      # Specific remote and branch
/safe-pull origin develop     # From origin's develop branch
```

Preview what would happen before pulling. Shows:
- Incoming commits
- Files that would change
- Potential merge conflicts

## Installation with Chezmoi

These commands are designed to be managed as dotfiles with chezmoi.

### Directory Structure

```
~/.claude/
└── commands/
    └── git-workflows/
        ├── README.md
        ├── private-fork.md
        └── safe-pull.md
```

### Chezmoi Source Structure

In your chezmoi source directory:
```
home/
└── dot_claude/
    └── commands/
        └── git-workflows/
            ├── README.md
            ├── private-fork.md
            └── safe-pull.md
```

### Adding to Chezmoi

```bash
# If managing existing files
chezmoi add ~/.claude/commands/git-workflows/

# Apply to deploy
chezmoi apply
```

## Creating New Commands

### File Structure

Each command is a markdown file with:
1. **Title** - Command name
2. **Arguments** - Input parameters using `$ARGUMENTS`
3. **Instructions** - Step-by-step guide for Claude Code

### Template

```markdown
# Command Name

Brief description of what this command does.

## Arguments

- `$ARGUMENTS` - Description of expected arguments

## Instructions

Step-by-step instructions for Claude Code to follow...
```

### Best Practices

1. **Be explicit** - Provide exact commands to run
2. **Handle errors** - Include error scenarios and recovery steps
3. **Offer options** - Give users choices when appropriate
4. **Explain why** - Help users understand the workflow

## Command Categories

Organize commands into logical groups:

| Category | Purpose |
|----------|---------|
| `git-workflows/` | Advanced git operations |
| `project-setup/` | Project initialization |
| `code-review/` | Review and analysis |
| `deployment/` | Build and deploy |

## Contributing

To add a new command:

1. Create a new `.md` file in the appropriate category
2. Follow the template structure
3. Test the command with Claude Code
4. Add to chezmoi source
5. Commit and push

## References

- [Create a private fork of a public repository](https://gist.github.com/0xjac/85097472043b697ab57ba1b1c7530274)
- [Taskmaster Claude Code Plugin](https://claudepluginhub.com/plugins/eyaltoledano-taskmaster-packages-claude-code-plugin)
- [Chezmoi - Manage dotfiles across machines](https://www.chezmoi.io/)

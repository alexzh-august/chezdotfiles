---
description: Manage Claude Code permissions
---

# Permissions Management

View and manage pre-allowed commands to avoid unnecessary permission prompts.

## Current Permissions

Check `.claude/settings.json` for the current allow/deny lists.

## Common Safe Commands to Pre-Allow

### Read-only operations (always safe)
- `Bash(cat:*)` - Read file contents
- `Bash(ls:*)` - List directories
- `Bash(find:*)` - Find files
- `Bash(grep:*)` - Search file contents
- `Bash(head:*)` - View file start
- `Bash(tail:*)` - View file end
- `Bash(wc:*)` - Count lines/words

### Build/Test operations (project-specific, generally safe)
- `Bash(npm:*)` - npm commands
- `Bash(bun:*)` - bun commands
- `Bash(pytest:*)` - Python tests
- `Bash(cargo:*)` - Rust commands
- `Bash(make:*)` - Make commands

### Git operations (safe for local work)
- `Bash(git status:*)` - Check status
- `Bash(git diff:*)` - View changes
- `Bash(git log:*)` - View history
- `Bash(git branch:*)` - Branch operations

### File operations
- `Read(*)` - Read any file
- `Write(*)` - Write files (use with caution)
- `Edit(*)` - Edit files

## Adding Permissions

To add a new permission, edit `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(your-command:*)"
    ]
  }
}
```

## Note

Avoid using `--dangerously-skip-permissions` in production.
Use specific permissions instead for security.

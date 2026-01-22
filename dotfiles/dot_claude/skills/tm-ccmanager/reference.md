# CCManager Reference - Parallel Feature Development

## Complete Parallel Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  SETUP (One-time)                                               │
│  mise install node@22 npm:ccmanager                             │
│  git config extensions.worktreeConfig true                      │
│  mkdir -p ../worktrees                                          │
└─────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  LAUNCH CCMANAGER                                               │
│  mise exec node@22 -- ccmanager                                 │
└─────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  CREATE FEATURE WORKTREES                                       │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│  │ feat/feature-1   │ │ feat/feature-2   │ │ feat/feature-3   │ │
│  │ Copy session: Y  │ │ Copy session: Y  │ │ Copy session: Y  │ │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  IN EACH WORKTREE SESSION                                       │
│  /tm-feature-task-planner "Feature Name"                        │
│  → Creates spec + tasks for that feature                        │
└─────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  PARALLEL DEVELOPMENT                                           │
│                                                                 │
│  Worktree 1 (Waiting)     Worktree 2 (Busy)    Worktree 3 (Idle)│
│  ├── tm next              ├── Implementing    ├── Ready         │
│  ├── Write tests          ├── ...             ├── tm next       │
│  └── Needs input          └── Processing      └── Start task    │
│                                                                 │
│  Switch between sessions with Enter key                         │
│  Yellow = needs attention, Blue = working, Green = ready        │
└─────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  COMPLETE EACH FEATURE                                          │
│  /tm-run-fix-tests                                              │
│  /tm-run-fix-code-review FEAT-XXX                               │
│  /tm-submit-pr FEAT-XXX                                         │
└─────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  MERGE & CLEANUP                                                │
│  In CCManager: m (merge) → d (delete worktree)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
~/projects/
├── ableton-session-mcp/           # Main repository (main branch)
│   ├── .claude/skills/            # Skills available in all worktrees
│   ├── specs/                     # Feature specs
│   └── ...
│
└── worktrees/                     # Worktrees directory
    ├── feat-looper-support/       # Worktree for FEAT-001
    │   ├── specs/FEAT-001-*.md
    │   └── ...
    ├── feat-wavetable-tools/      # Worktree for FEAT-002
    │   ├── specs/FEAT-002-*.md
    │   └── ...
    └── fix-clip-notes-bug/        # Worktree for FIX-001
        ├── specs/FIX-001-*.md
        └── ...
```

## Integration with tm-* Skills

### Creating a Feature in a New Worktree

```bash
# 1. In CCManager, create worktree
#    Press 'n', enter: feat/new-feature
#    Copy session data: Yes

# 2. CCManager switches to new worktree session
#    Claude has full project context

# 3. In the session, create feature structure
/tm-feature-task-planner "New Feature Name"

# 4. Work on tasks
tm next
# ... implement ...
/tm-critic <id>
tm set-status <id> done

# 5. When complete
/tm-run-fix-tests
/tm-run-fix-code-review FEAT-XXX
/tm-submit-pr FEAT-XXX
```

### Checking Progress Across Features

```bash
# In main worktree or any worktree
tm list                    # All tasks
tm list --tag FEAT-001     # Feature 1 tasks
tm list --tag FEAT-002     # Feature 2 tasks
```

### Coordinating Dependencies

If Feature 2 depends on Feature 1:

```bash
# 1. Complete Feature 1 first
/tm-submit-pr FEAT-001

# 2. Merge Feature 1 to main

# 3. In Feature 2 worktree, rebase
git fetch origin main
git rebase origin/main

# 4. Continue Feature 2 development
```

## CCManager Session States

| State | Color | Meaning | Action |
|-------|-------|---------|--------|
| Waiting | Yellow | Claude asking for input | Switch and respond |
| Busy | Blue | Claude processing | Let it work |
| Idle | Green | Ready for new task | Start next task |

## Worktree Naming Conventions

```
feat/<feature-name>     # New feature
fix/<bug-name>          # Bug fix
refactor/<area>         # Refactoring
docs/<topic>            # Documentation
test/<area>             # Test additions
spike/<experiment>      # Experimental work
```

## mise Installation Commands

```bash
# Install mise (if not installed)
curl https://mise.run | sh

# Add to shell (bash)
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc

# Add to shell (zsh)
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc

# Reload shell
source ~/.bashrc  # or ~/.zshrc

# Install Node.js 22 and CCManager
mise install node@22
mise install npm:ccmanager
mise use -g npm:ccmanager

# Verify
mise exec node@22 -- ccmanager --version
```

## CCManager Configuration File

Location: `~/.config/ccmanager/config.json`

```json
{
  "shortcuts": {
    "returnToMenu": {
      "ctrl": true,
      "key": "e"
    },
    "cancel": {
      "key": "escape"
    }
  },
  "worktree": {
    "copySessionData": true,
    "autoDirectory": {
      "enabled": true,
      "pattern": "../worktrees/{branch}"
    }
  },
  "command": {
    "name": "claude",
    "args": ["--resume"],
    "fallbackArgs": []
  },
  "hooks": {
    "postWorktreeCreate": "npm install"
  },
  "stateDetection": {
    "strategy": "claude"
  }
}
```

## Advanced: Auto Approval (Experimental)

For trusted operations, CCManager can auto-approve prompts:

```json
{
  "autoApproval": {
    "enabled": true,
    "command": null
  }
}
```

**Warning**: Only enable for sandboxed/devcontainer environments.

## Devcontainer Integration

For maximum safety, run Claude in devcontainers:

```bash
ccmanager \
  --devc-up-command "devcontainer up --workspace-folder ." \
  --devc-exec-command "devcontainer exec --workspace-folder ."
```

## Troubleshooting

### Worktree creation fails
```bash
# Check git status
git status

# Ensure no uncommitted changes on target branch
git stash

# Try again in CCManager
```

### Session data not preserving
```bash
# Check Claude projects directory
ls -la ~/.claude/projects/

# Verify worktree path matches
pwd
```

### Node version mismatch
```bash
# Force Node 22
mise use node@22

# Or run with explicit version
mise exec node@22 -- ccmanager
```

### Skills not available in worktree
```bash
# Skills are in .claude/skills/ which is part of the repo
# They should be available in all worktrees automatically
ls .claude/skills/
```

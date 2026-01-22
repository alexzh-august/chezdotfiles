---
name: tm-ccmanager
description: Manage multiple AI coding sessions across Git worktrees for parallel feature development. Use when user says "parallel features", "multiple worktrees", "ccmanager", "parallel sessions", or wants to work on multiple features simultaneously. Integrates with tm-feature-task-planner for parallelized building.
---

# CCManager - Parallel Feature Development

Manage multiple AI coding assistant sessions across Git worktrees for parallel feature development. Each feature gets its own worktree and AI session.

## Quick Start

```
/tm-ccmanager install              # Install CCManager via mise
/tm-ccmanager start                # Launch CCManager
/tm-ccmanager new-feature "Name"   # Create worktree + feature in one step
/tm-ccmanager status               # Show all sessions and their states
```

## Prerequisites

### Install CCManager via mise

```bash
# Install mise if not already installed
curl https://mise.run | sh

# Install CCManager with Node.js 22
mise install node@22
mise install npm:ccmanager
mise use -g npm:ccmanager

# Verify installation
mise exec node@22 -- ccmanager --version
```

### Alternative: npm global install

```bash
npm install -g ccmanager
```

## Instructions

### Step 1: Setup Project for Worktrees

First time setup for a project:

```bash
# Enable git worktree config extension for enhanced status
git config extensions.worktreeConfig true

# Create worktrees directory (sibling to main repo)
mkdir -p ../worktrees
```

### Step 2: Launch CCManager

```bash
# Start CCManager (uses current directory as base)
mise exec node@22 -- ccmanager

# Or with npx
npx ccmanager
```

### Step 3: Create Feature Worktree

In CCManager:
1. Press `n` to create new worktree
2. Enter branch name: `feat/feature-name`
3. Choose to copy session data (recommended for context)
4. Worktree created at `../worktrees/feat-feature-name`

### Step 4: Setup Feature in Worktree

In the new worktree session, run:
```
/tm-feature-task-planner "Feature Name"
```

This creates the spec and tasks for that feature.

### Step 5: Work in Parallel

Switch between worktrees in CCManager:
- Each has its own Claude session
- Each has its own feature spec and tasks
- Work progresses independently

Status indicators:
- **Waiting** (yellow): Claude needs input
- **Busy** (blue): Claude processing
- **Idle** (green): Ready for new tasks

### Step 6: Complete and Merge

When a feature is complete:
```bash
# In the feature worktree
/tm-run-fix-tests
/tm-run-fix-code-review FEAT-XXX
/tm-submit-pr FEAT-XXX
```

After PR merged:
```bash
# In CCManager, delete the worktree
# Press 'd' on the completed worktree
```

## Workflow Integration

### Parallel Feature Development Pattern

```
Main Worktree (main branch)
├── Worktree: feat/looper-support      → FEAT-001 tasks
├── Worktree: feat/wavetable-tools     → FEAT-002 tasks
├── Worktree: feat/rack-variations     → FEAT-003 tasks
└── Worktree: fix/clip-notes-bug       → FIX-001 tasks
```

Each worktree has:
- Own git branch
- Own spec document
- Own task-master tasks
- Own Claude session with context

### Creating Multiple Features at Once

```bash
# Start CCManager
mise exec node@22 -- ccmanager

# In CCManager, create worktrees:
# n → feat/feature-1 → copy session
# n → feat/feature-2 → copy session
# n → feat/feature-3 → copy session

# Switch to each worktree and run:
/tm-feature-task-planner "Feature 1"
/tm-feature-task-planner "Feature 2"
/tm-feature-task-planner "Feature 3"
```

### Session Context Copying

When creating a new worktree, CCManager can copy Claude's session data:
- Conversation history preserved
- Project context maintained
- CLAUDE.md and skills available

**Recommended**: Always copy session data for feature branches to maintain project knowledge.

## CCManager Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Select/Enter worktree session |
| `n` | Create new worktree |
| `d` | Delete worktree |
| `m` | Merge worktree to main |
| `Ctrl+E` | Return to menu from session |
| `/` | Search/filter worktrees |
| `B` | Back to project list (multi-project) |

## Configuration

### CCManager Config (~/.config/ccmanager/config.json)

```json
{
  "shortcuts": {
    "returnToMenu": { "ctrl": true, "key": "e" }
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
  }
}
```

### Worktree Hooks

Create post-worktree hook for automatic setup:

```bash
# In CCManager config
{
  "hooks": {
    "postWorktreeCreate": "npm install && cp .env.example .env"
  }
}
```

## Multi-Project Mode

For managing multiple repositories:

```bash
export CCMANAGER_MULTI_PROJECT_ROOT="$HOME/projects"
mise exec node@22 -- ccmanager --multi-project
```

## Best Practices

1. **One feature per worktree** - Keep changes isolated
2. **Copy session data** - Maintain Claude's project knowledge
3. **Use consistent naming** - `feat/`, `fix/`, `refactor/` prefixes
4. **Delete after merge** - Keep worktree list clean
5. **Check status often** - Yellow = needs attention
6. **Resume sessions** - Use `--resume` flag for continuity

## Troubleshooting

### CCManager not found
```bash
mise install npm:ccmanager
mise use -g npm:ccmanager
```

### Node version issues
```bash
mise install node@22
mise exec node@22 -- ccmanager
```

### Worktree path issues
```bash
# Ensure worktrees directory exists
mkdir -p ../worktrees

# Check git config
git config extensions.worktreeConfig true
```

### Session data not copying
```bash
# Check source path exists
ls ~/.claude/projects/

# Manually copy if needed
cp -r ~/.claude/projects/old-path ~/.claude/projects/new-path
```

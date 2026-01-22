---
name: graphite
description: Manage stacked PRs with Graphite CLI for focused, reviewable changes
triggers:
  - gt
  - graphite
  - stacked pr
  - stack submit
  - create stack
  - multiple prs
---

# Graphite Stacked PR Management

Use Graphite to break large features into small, focused PRs that are easier to review.

## Prerequisites

Install Graphite CLI:
```bash
brew install graphite  # macOS
npm install -g @graphite-dev/cli  # or npm
```

Initialize in repo (one-time):
```bash
gt init
gt auth  # Login to GitHub
```

## Workflow: Feature Development

### Step 1: Create Stack of Changes

Instead of one large branch, create multiple focused branches:

```bash
# First logical change (e.g., add data model)
git add .
gt create -am "feat(api): Add user data model"

# Second logical change (e.g., add endpoint)
git add .
gt create -am "feat(api): Add user endpoint"

# Third logical change (e.g., add tests)
git add .
gt create -am "test(api): Add user endpoint tests"
```

Each `gt create` makes a new branch stacked on the previous one.

### Step 2: View Your Stack

```bash
gt log
```

Output:
```
◉ test(api): Add user endpoint tests (current)
│
◉ feat(api): Add user endpoint
│
◉ feat(api): Add user data model
│
◯ main
```

### Step 3: Submit All PRs

```bash
gt submit --stack --no-edit --publish
# Shorthand: gt ss
```

This creates 3 separate PRs on GitHub:
- PR #1: Add user data model (base: main)
- PR #2: Add user endpoint (base: PR #1)
- PR #3: Add user endpoint tests (base: PR #2)

### Step 4: Handle Review Feedback

```bash
# Navigate to branch needing changes
gt down  # or: gt checkout <branch-name>

# Make changes
vim src/models/user.py

# Amend the commit
gt modify -a

# Graphite auto-restacks dependent branches
```

### Step 5: Sync with Main

```bash
gt sync
```

Rebases entire stack on latest main, handling conflicts intelligently.

## Quick Reference

| Task | Command |
|------|---------|
| Create new branch in stack | `gt create -am "message"` |
| View stack structure | `gt log` |
| Submit all PRs | `gt ss` or `gt submit --stack` |
| Navigate up stack | `gt up` |
| Navigate down stack | `gt down` |
| Amend current commit | `gt modify -a` |
| Sync with main | `gt sync` |
| Fix stack after conflicts | `gt restack` |
| Split large commit | `gt split` |
| Combine branches | `gt fold` |

## When to Use Stacked PRs

### Good for:
- Multi-step features (model -> logic -> tests)
- Large refactors (break into reviewable chunks)
- Features touching multiple areas
- Keeping PRs under 200 lines

### Not needed for:
- Single-commit fixes
- Simple documentation updates
- Hotfixes

## Integration with Existing Skills

### With tm-feature-task-planner
1. Use planner to break feature into tasks
2. Each task becomes one `gt create` commit
3. Submit stack when feature complete

### With tm-submit-pr
- Use for single PRs
- Use Graphite for stacked PRs

### With git-master
- Graphite complements git-master
- Use git for complex operations (cherry-pick, bisect)
- Use Graphite for stack management

## Common Patterns

### Pattern 1: Database Migration Stack
```bash
gt create -am "feat(db): Add migration for new table"
gt create -am "feat(model): Add Pydantic model"
gt create -am "feat(crud): Add CRUD operations"
gt create -am "test(db): Add integration tests"
gt ss
```

### Pattern 2: API Feature Stack
```bash
gt create -am "feat(schema): Add request/response models"
gt create -am "feat(api): Add endpoint implementation"
gt create -am "feat(docs): Update API documentation"
gt create -am "test(api): Add endpoint tests"
gt ss
```

### Pattern 3: Refactor Stack
```bash
gt create -am "refactor(core): Extract helper functions"
gt create -am "refactor(api): Use new helpers in endpoints"
gt create -am "test: Update tests for refactored code"
gt ss
```

## Troubleshooting

### Stack out of sync
```bash
gt restack
```

### Merge conflicts during sync
```bash
# Resolve conflicts in editor
git add .
gt continue
```

### Want to reorder stack
```bash
gt reorder  # Interactive reordering
```

### Need to insert branch mid-stack
```bash
gt checkout <target-branch>
gt create --insert -am "feat: Insert this change"
```

## Worktree Workflow: Parallel Feature Development

This workflow uses git worktrees for parallel development with isolated testing environments.

### Architecture

```
develop/staging (Integration)     Feature Worktrees (Isolated Development)
├── Test all features together    ├── feature-a, feature-b, feature-c
├── Run full test suite           ├── bugfix-1, bugfix-2
└── Integration validation        └── experiment-x
```

### Worktree Locations

| Branch | Location | Purpose |
|--------|----------|---------|
| `develop` | `../your-project-develop` | Integration testing |
| `staging` | `../your-project-staging` | Pre-production validation |
| `TICKET-ID-<feature>` | `../your-project-TICKET-ID-<feature>` | Feature-specific work |

### Setting Up Feature Worktrees

```bash
# Create worktrees for parallel feature development
git worktree add ../your-project-feature-auth feature/auth
git worktree add ../your-project-feature-api feature/api
git worktree add ../your-project-bugfix-123 bugfix/TICKET-123
```

### Workflow: Feature-Specific Development

When a feature needs isolated work:

```bash
# 1. Work in isolated feature worktree
cd ../your-project-feature-auth

# 2. Make feature-specific changes
# ... implement feature ...

# 3. Commit changes
git add . && git commit -m "feat(auth): Add OAuth provider support"

# 4. Bring changes to develop for integration testing
cd ../your-project-develop
git cherry-pick <commit-hash>
# OR merge the branch
git merge feature/auth

# 5. Run full test suite in develop environment
# Run integration tests

# 6. If successful, promote to staging
cd ../your-project-staging
git cherry-pick <commit-hash>
```

### Workflow: Standard Development

When working without feature isolation:

```bash
# Work directly in develop
cd ../your-project-develop

# Make changes, run tests
git add . && git commit -m "feat(api): Add new endpoint"

# Promote to staging when ready
cd ../your-project-staging
git merge develop
```

### Quick Navigation

```bash
# List all worktrees
git worktree list

# Jump to specific feature
cd ../your-project-feature-auth

# Jump to integration
cd ../your-project-develop

# Jump to staging
cd ../your-project-staging
```

### Cleanup (After Feature Complete)

```bash
# Remove feature worktrees
git worktree remove ../your-project-feature-auth

# Or remove multiple at once
for feature in feature-auth feature-api bugfix-123; do
  git worktree remove ../your-project-$feature 2>/dev/null
done
```

---

## Claude Code Integration

When working with Claude Code on multi-commit features:

1. **Plan commits first**: Use tm-feature-task-planner to identify logical steps
2. **Create incrementally**: After each logical unit of work, run `gt create -am "..."`
3. **Review before submit**: Use `gt log` to verify stack structure
4. **Submit when ready**: `gt ss` to create all PRs at once

### Example Session
```bash
# Claude Code implements feature in steps
# After implementing data model:
gt create -am "feat(db): Add user preferences model"

# After implementing service layer:
gt create -am "feat(service): Add user preferences service"

# After implementing API:
gt create -am "feat(api): Add user preferences endpoint"

# After adding tests:
gt create -am "test: Add user preferences tests"

# Review and submit
gt log
gt ss
```

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

## Worktree Workflow: Multi-Chain Backfill (AUGUST-4032)

This workflow uses git worktrees for parallel chain development with Databricks asset testing.

### Architecture

```
develop/staging (Integration)     Chain Worktrees (Isolated Development)
├── Test all chains together      ├── SONIC, HYPEREVM, PLASMA, MEZO
├── Databricks asset builds       ├── INK, FLARE, MONAD, POLYGON
└── Integration validation        ├── ZIRCUIT, SWELL, HEMI, UNICHAIN
                                  ├── TAC, SONEIUM, KAVA, POLYZK
                                  ├── KATANA, MOVEMENT, TON, APTOS
                                  └── SUI, SOL
```

### Worktree Locations

| Branch | Location | Purpose |
|--------|----------|---------|
| `develop` | `../defi-data-collection-develop` | Integration testing |
| `staging` | `../defi-data-collection-staging` | Pre-production validation |
| `AUGUST-4032-BACKFILL-<CHAIN>` | `../defi-data-collection-AUGUST-4032-BACKFILL-<CHAIN>` | Chain-specific work |

### Available Chain Worktrees

| Chain | Branch | Location |
|-------|--------|----------|
| SONIC | `AUGUST-4032-BACKFILL-SONIC` | `../defi-data-collection-AUGUST-4032-BACKFILL-SONIC` |
| HYPEREVM | `AUGUST-4032-BACKFILL-HYPEREVM` | `../defi-data-collection-AUGUST-4032-BACKFILL-HYPEREVM` |
| PLASMA | `AUGUST-4032-BACKFILL-PLASMA` | `../defi-data-collection-AUGUST-4032-BACKFILL-PLASMA` |
| MEZO | `AUGUST-4032-BACKFILL-MEZO` | `../defi-data-collection-AUGUST-4032-BACKFILL-MEZO` |
| INK | `AUGUST-4032-BACKFILL-INK` | `../defi-data-collection-AUGUST-4032-BACKFILL-INK` |
| FLARE | `AUGUST-4032-BACKFILL-FLARE` | `../defi-data-collection-AUGUST-4032-BACKFILL-FLARE` |
| MONAD | `AUGUST-4032-BACKFILL-MONAD` | `../defi-data-collection-AUGUST-4032-BACKFILL-MONAD` |
| POLYGON | `AUGUST-4032-BACKFILL-POLYGON` | `../defi-data-collection-AUGUST-4032-BACKFILL-POLYGON` |
| ZIRCUIT | `AUGUST-4032-BACKFILL-ZIRCUIT` | `../defi-data-collection-AUGUST-4032-BACKFILL-ZIRCUIT` |
| SWELL | `AUGUST-4032-BACKFILL-SWELL` | `../defi-data-collection-AUGUST-4032-BACKFILL-SWELL` |
| HEMI | `AUGUST-4032-BACKFILL-HEMI` | `../defi-data-collection-AUGUST-4032-BACKFILL-HEMI` |
| UNICHAIN | `AUGUST-4032-BACKFILL-UNICHAIN` | `../defi-data-collection-AUGUST-4032-BACKFILL-UNICHAIN` |
| TAC | `AUGUST-4032-BACKFILL-TAC` | `../defi-data-collection-AUGUST-4032-BACKFILL-TAC` |
| SONEIUM | `AUGUST-4032-BACKFILL-SONEIUM` | `../defi-data-collection-AUGUST-4032-BACKFILL-SONEIUM` |
| KAVA | `AUGUST-4032-BACKFILL-KAVA` | `../defi-data-collection-AUGUST-4032-BACKFILL-KAVA` |
| POLYZK | `AUGUST-4032-BACKFILL-POLYZK` | `../defi-data-collection-AUGUST-4032-BACKFILL-POLYZK` |
| KATANA | `AUGUST-4032-BACKFILL-KATANA` | `../defi-data-collection-AUGUST-4032-BACKFILL-KATANA` |
| MOVEMENT | `AUGUST-4032-BACKFILL-MOVEMENT` | `../defi-data-collection-AUGUST-4032-BACKFILL-MOVEMENT` |
| TON | `AUGUST-4032-BACKFILL-TON` | `../defi-data-collection-AUGUST-4032-BACKFILL-TON` |
| APTOS | `AUGUST-4032-BACKFILL-APTOS` | `../defi-data-collection-AUGUST-4032-BACKFILL-APTOS` |
| SUI | `AUGUST-4032-BACKFILL-SUI` | `../defi-data-collection-AUGUST-4032-BACKFILL-SUI` |
| SOL | `AUGUST-4032-BACKFILL-SOL` | `../defi-data-collection-AUGUST-4032-BACKFILL-SOL` |

### Workflow: Chain-Specific Customization

When a chain needs special handling:

```bash
# 1. Work in isolated chain worktree
cd ../defi-data-collection-AUGUST-4032-BACKFILL-SONIC

# 2. Make chain-specific changes
# ... implement fixes ...

# 3. Commit changes
git add . && git commit -m "fix(sonic): Handle custom RPC behavior"

# 4. Bring changes to develop for integration testing
cd ../defi-data-collection-develop
git cherry-pick <commit-hash>
# OR merge the branch
git merge AUGUST-4032-BACKFILL-SONIC

# 5. Test Databricks asset build with all chains
# Run pipeline in develop environment

# 6. If successful, promote to staging
cd ../defi-data-collection-staging
git cherry-pick <commit-hash>
```

### Workflow: Standard Development (No Chain Issues)

When all chains work without customization:

```bash
# Work directly in develop
cd ../defi-data-collection-develop

# Make changes, test Databricks builds
git add . && git commit -m "feat(volumes): Add new metric"

# Promote to staging when ready
cd ../defi-data-collection-staging
git merge develop
```

### Quick Navigation

```bash
# List all worktrees
git worktree list

# Jump to specific chain
cd ../defi-data-collection-AUGUST-4032-BACKFILL-POLYGON

# Jump to integration
cd ../defi-data-collection-develop

# Jump to staging
cd ../defi-data-collection-staging
```

### Cleanup (After Backfill Complete)

```bash
# Remove chain worktrees
git worktree remove ../defi-data-collection-AUGUST-4032-BACKFILL-SONIC
# ... repeat for each chain ...

# Or remove all at once
for chain in SONIC HYPEREVM PLASMA MEZO INK FLARE MONAD POLYGON ZIRCUIT SWELL HEMI UNICHAIN TAC SONEIUM KAVA POLYZK KATANA MOVEMENT TON APTOS SUI SOL; do
  git worktree remove ../defi-data-collection-AUGUST-4032-BACKFILL-$chain 2>/dev/null
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

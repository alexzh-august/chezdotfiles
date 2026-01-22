---
description: Multi-agent commit-push-PR with validation, conventional commits, and critic review
---

# Commit-Push-PR (Full Mode)

This command invokes the multi-agent orchestrator for comprehensive commit and PR workflows with quality gates.

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMMIT-PUSH-PR WORKFLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: VALIDATION (4 Parallel Agents)                                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ Code Review  │ │ Test Runner  │ │ Lint Checker │ │  Security    │       │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘       │
│         └────────────────┴────────────────┴────────────────┘               │
│                              ▼                                              │
│                    ┌─────────────────┐                                      │
│                    │  Quality Gate   │ GREEN → proceed                     │
│                    │ GREEN/YELLOW/RED│ YELLOW → review warnings            │
│                    └────────┬────────┘ RED → block, fix issues             │
│                             │                                               │
│  PHASE 2: COMMIT MESSAGE                                                   │
│                             ▼                                               │
│                    ┌─────────────────┐                                      │
│                    │  Conventional   │ feat|fix|refactor|docs|test|chore   │
│                    │  Commit Gen     │ (scope): description                │
│                    └────────┬────────┘                                      │
│                             │                                               │
│  PHASE 3: CRITIC REVIEW (Mandatory)                                        │
│                             ▼                                               │
│                    ┌─────────────────┐                                      │
│                    │  @agent         │ APPROVED → proceed                  │
│                    │  pr-critic      │ NEEDS_REVISION → show issues        │
│                    └────────┬────────┘                                      │
│                             │                                               │
│  PHASE 4: COMMIT & PUSH                                                    │
│                             ▼                                               │
│                    ┌─────────────────┐                                      │
│                    │  git add -A     │                                      │
│                    │  git commit     │ With Co-Authored-By footer          │
│                    │  git push -u    │                                      │
│                    └────────┬────────┘                                      │
│                             │                                               │
│  PHASE 5: PR CREATION                                                      │
│                             ▼                                               │
│                    ┌─────────────────┐                                      │
│                    │  gh pr create   │ Auto-populated template             │
│                    │  with body      │ Validation results included         │
│                    └─────────────────┘                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pre-computed Context

```bash
# Current branch
BRANCH=$(git branch --show-current)

# Git status summary
STATUS=$(git status --porcelain | head -20)

# Recent commits on this branch (not on main)
COMMITS=$(git log main..HEAD --oneline 2>/dev/null || git log origin/main..HEAD --oneline 2>/dev/null || echo "No commits yet")

# Changed files summary
CHANGED_FILES=$(git diff --stat HEAD~1 2>/dev/null || git diff --stat --cached 2>/dev/null || echo "No changes")

# Staged files for scope detection
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || git diff --name-only 2>/dev/null || echo "No staged files")

# PR template if exists
PR_TEMPLATE=$(cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || echo "No PR template found")
```

## Invoke Multi-Agent Orchestrator

```
@agent commit-push-pr-agents
```

## Context

Current branch: $BRANCH

Status:
$STATUS

Recent commits:
$COMMITS

Changed files:
$CHANGED_FILES

Staged files:
$STAGED_FILES

## What the Agent Does

### Phase 1: Validation (Parallel)

Spawns 4 validation agents simultaneously:

| Agent | Checks | Timeout |
|-------|--------|---------|
| Code Review | Debug code, hardcoded secrets, code quality | 5 min |
| Test Runner | pytest / npm test / cargo test / go test | 5 min |
| Lint Checker | ruff / eslint / clippy / golangci-lint | 2 min |
| Security | Secrets in diff, vulnerability patterns | 2 min |

**Quality Gate**:
- **GREEN**: All pass → auto-proceed
- **YELLOW**: Warnings → prompt user
- **RED**: Failures → block, show errors

### Phase 2: Commit Message

Generates conventional commit format:

```
[type]([scope]): [description]

[body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types**: feat, fix, refactor, docs, test, build, ci, chore
**Scope**: Auto-detected from file paths (monorepo-aware)
**Breaking**: Adds `!` if breaking changes detected

### Phase 3: Critic Review

Mandatory review before commit:
- Code quality assessment
- Commit message accuracy
- Test coverage check
- Security considerations

### Phase 4: Commit & Push

After critic approval:
- Stage all changes
- Commit with generated message
- Push with upstream tracking

### Phase 5: PR Creation

Auto-populates PR with:
- Summary from commit message
- Validation results table
- Changed files list
- Critic suggestions (if any)

## Tips

- Let validation complete fully before proceeding
- Address RED issues before attempting commit
- Review YELLOW warnings but can proceed
- Critic feedback is mandatory - can't skip

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Validation timeout | Check if tests are hanging, increase timeout |
| Lint not found | Install ruff/eslint for your project |
| Critic blocks | Address critical issues shown |
| Push rejected | Pull --rebase to sync with remote |
| gh CLI error | Run `gh auth login` to authenticate |

## Alternative: Quick Mode

For simple commits without validation:

```
/commit-push-pr
```

Use quick mode for typos, hotfixes, or solo experimental work.

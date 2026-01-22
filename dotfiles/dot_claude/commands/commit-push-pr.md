---
description: Commit, push, and open a PR
---

# Commit, Push, and Open PR

This command commits your current changes, pushes to the remote, and opens a pull request.

## Mode Selection

Choose your workflow:

| Mode | Command | Use When |
|------|---------|----------|
| **Full** (Recommended) | `/commit-push-pr-cmd` | New features, important changes, team PRs |
| **Quick** | `/commit-push-pr` | Hotfixes, typos, solo work |

### Full Mode (Multi-Agent)

For comprehensive validation with quality gates:

```
@agent commit-push-pr-agents
```

This invokes the multi-agent orchestrator which:
1. Runs 4 parallel validation agents (code review, tests, lint, security)
2. Generates conventional commit messages with scope detection
3. Requires mandatory critic review before commit
4. Auto-populates PR template with validation results
5. Creates PR with structured body

### Quick Mode (This Command)

For simple, fast commits without full validation.

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

# PR template if exists
PR_TEMPLATE=$(cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || echo "No PR template found")
```

## Prerequisites

- Git installed and configured
- [GitHub CLI (gh)](https://cli.github.com/) installed for PR creation

## Quick Mode Instructions

1. Review the git status above
2. Stage any unstaged changes if needed: `git add -A`
3. Create a meaningful commit message based on the changes
4. Push to the remote branch
5. Use `gh pr create` (requires GitHub CLI) to open a pull request with:
   - A descriptive title summarizing the changes
   - A body that follows the PR template (if available) or describes what changed and why
   - Appropriate labels if the project uses them

## Context

Current branch: $BRANCH
Status:
$STATUS

Recent commits:
$COMMITS

Changed files:
$CHANGED_FILES

## When to Use Full Mode

Use `/commit-push-pr-cmd` (full mode) when:
- Submitting code for team review
- Making changes that affect multiple files
- Working on features that need test validation
- You want conventional commit format enforced
- Security scanning is important

## When to Use Quick Mode

Use this command (quick mode) when:
- Fixing typos or documentation
- Making emergency hotfixes
- Working solo on experimental branches
- Commits that don't need validation overhead

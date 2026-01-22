---
name: tm-submit-pr
description: Submit a pull request for a completed feature. Requires tests passing and code review complete. Use when feature is done, ready to merge, or user says "submit PR", "create PR", "merge feature". Validates prerequisites and creates PR with template.
---

# Submit Pull Request

Create a pull request for a completed feature after validating all prerequisites are met.

## Quick Start

```
/tm-submit-pr FEAT-001              # Submit PR for feature
/tm-submit-pr --skip-checks         # Skip validation (not recommended)
```

## Instructions

### Step 1: Validate Prerequisites

Before creating PR, verify:

```bash
# 1. Check all tests pass
uv run pytest -v
# Must be: ALL PASSED

# 2. Check tasks complete
npx task-master list --tag FEAT-XXX
# Must be: All tasks in 'done' status

# 3. Check spec status
grep "status:" specs/FEAT-XXX-*.md
# Must be: status: review (or done)
```

If any check fails:
```
❌ Prerequisites not met. Run these first:
   - /tm-run-fix-tests
   - /tm-run-fix-code-review FEAT-XXX
```

### Step 2: Gather PR Information

```bash
# Get feature info from spec
SPEC_FILE=$(ls specs/FEAT-XXX-*.md)
TITLE=$(grep "^title:" $SPEC_FILE | cut -d: -f2 | xargs)
BRANCH=$(git branch --show-current)

# Get commit summary
git log main..$BRANCH --oneline

# Get changed files
git diff --stat main..$BRANCH
```

### Step 3: Generate PR Body

Use this template:

```markdown
## Summary

[Brief description from spec overview]

## Changes

### New Features
- [List new capabilities]

### Files Changed
- `path/to/file.py` - [what changed]

## Spec Reference

- **Spec Document:** specs/FEAT-XXX-name.md
- **Feature ID:** FEAT-XXX
- **Branch:** feat/feature-name

## Testing

### Test Results
- **Unit Tests:** X passed
- **Coverage:** XX%
- **Mutation Score:** XX%

### How to Test
1. [Step to verify feature works]
2. [Another verification step]

## Checklist

- [x] All tests pass
- [x] Coverage > 80%
- [x] Mutation score > 80%
- [x] Type checking passes
- [x] Linting passes
- [x] No security vulnerabilities
- [x] Spec document updated
- [x] All tasks marked done

## Related

- Closes #[issue] (if applicable)
- Spec: specs/FEAT-XXX-name.md
```

### Step 4: Push Branch and Create PR

```bash
# Ensure branch is up to date with main
git fetch origin main
git rebase origin/main

# Push branch
git push -u origin $(git branch --show-current)

# Create PR
gh pr create \
  --title "FEAT-XXX: $TITLE" \
  --body "$(cat <<'EOF'
[Generated PR body from Step 3]
EOF
)"
```

### Step 5: Update Spec Status

After PR created:

```bash
# Update spec status to 'review'
sed -i '' 's/status: in-progress/status: review/' specs/FEAT-XXX-*.md

# Add PR link to spec
echo "
## Pull Request
- PR: [#XXX](pr-url)
- Created: $(date +%Y-%m-%d)
" >> specs/FEAT-XXX-*.md
```

### Step 6: Report Submission

```markdown
## PR Submitted: FEAT-XXX

### Pull Request
- **PR:** #XXX
- **URL:** https://github.com/owner/repo/pull/XXX
- **Branch:** feat/feature-name → main

### Status
✅ All prerequisites passed
✅ PR created successfully
✅ Spec updated with PR link

### Next Steps
1. Request review from team
2. Address review feedback
3. Merge when approved

### Post-Merge Tasks
- [ ] Delete feature branch
- [ ] Update spec status to 'done'
- [ ] Close related issues
```

## PR Template File

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary

<!-- Brief description of changes -->

## Spec Reference

- **Spec Document:** <!-- specs/FEAT-XXX.md -->
- **Feature ID:** <!-- FEAT-XXX -->

## Changes

### New Features
-

### Files Changed
-

## Testing

- **Tests Pass:** Yes/No
- **Coverage:** XX%
- **Mutation Score:** XX%

## Checklist

- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Spec document updated
- [ ] All tasks marked done

## Related Issues

<!-- Closes #XXX -->
```

## Workflow Integration

```
/tm-feature-task-planner "Name"  → Plan feature
     ↓
tm next → Work on tasks (TDD)
     ↓
/tm-run-fix-tests               → Ensure tests pass
     ↓
/tm-run-fix-code-review FEAT-X  → Full review
     ↓
/tm-submit-pr FEAT-X            → Create PR ← YOU ARE HERE
     ↓
Review & Merge                  → Done!
```

## Error Handling

### Tests Failing
```
❌ Cannot submit PR: Tests failing
   Run: /tm-run-fix-tests
```

### Incomplete Tasks
```
❌ Cannot submit PR: Tasks not complete
   Pending: [task IDs]
   Run: tm set-status <id> done (or complete the work)
```

### Missing Spec
```
❌ Cannot submit PR: No spec document found
   Expected: specs/FEAT-XXX-*.md
   Run: /tm-feature-task-planner "Feature Name"
```

### Branch Not Pushed
```
⚠️ Branch not on remote
   Running: git push -u origin <branch>
```

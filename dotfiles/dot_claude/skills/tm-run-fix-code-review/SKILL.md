---
name: tm-run-fix-code-review
description: Review completed feature spec, verify all tasks done, check test coverage, and fix any issues. Use when completing a feature, before PR, or when user says "review feature", "check feature complete", "pre-PR review". Ensures feature meets all quality gates.
---

# Run Feature Code Review

Comprehensive review of a completed feature: spec compliance, task completion, test coverage, and code quality. Fixes issues found.

## Quick Start

```
/tm-run-fix-code-review FEAT-001           # Review feature by ID
/tm-run-fix-code-review specs/FEAT-001.md  # Review by spec file
```

## Instructions

### Step 1: Load Feature Context

```bash
# Find spec document
ls specs/FEAT-*.md

# Read the spec
cat specs/FEAT-XXX-feature-name.md

# Get feature tasks
npx task-master list --tag FEAT-XXX
```

### Step 2: Verify Spec Compliance

Check each section of the spec:

#### 2.1 Success Criteria
- [ ] All success criteria met?
- [ ] Each criterion testable and tested?

#### 2.2 Hypotheses Validated
- [ ] Each hypothesis has validation tests?
- [ ] Results documented in spec?

#### 2.3 Components Implemented
- [ ] All specified components exist?
- [ ] Interfaces match spec?
- [ ] Behaviors match spec?

### Step 3: Verify Task Completion

```bash
npx task-master list --tag FEAT-XXX
```

Check:
- [ ] All tasks in `done` status
- [ ] No tasks in `pending` or `in-progress`
- [ ] Dependencies were respected

If incomplete tasks found:
```bash
npx task-master show <id>  # Check what's missing
```

### Step 4: Run Test Suite

```bash
# Run all tests
uv run pytest -v

# Check coverage
uv run pytest --cov=MCP_Server --cov-report=term-missing
```

Requirements:
- [ ] All tests pass
- [ ] Coverage > 80% for new code
- [ ] No untested critical paths

### Step 5: Run Mutation Testing

```bash
# Run mutmut on changed files
uv run mutmut run --paths-to-mutate=MCP_Server/tools/
uv run mutmut results
```

Requirements:
- [ ] Mutation score > 80%
- [ ] No surviving mutants in critical code

### Step 6: Code Quality Checks

```bash
# Type checking
uv run mypy MCP_Server/

# Linting
uv run ruff check MCP_Server/

# Security scan
uv run bandit -r MCP_Server/
```

Requirements:
- [ ] No type errors
- [ ] No linting errors
- [ ] No security vulnerabilities

### Step 7: Fix Issues Found

For each issue:

1. **Missing tests** → Write tests
2. **Low coverage** → Add test cases
3. **Failing tests** → Run `/tm-run-fix-tests`
4. **Type errors** → Add/fix type hints
5. **Lint errors** → Apply auto-fixes or manual fixes
6. **Security issues** → Fix vulnerabilities
7. **Incomplete tasks** → Complete or update status

### Step 8: Update Spec Document

After fixes, update spec:

```markdown
---
status: review  # Update from in-progress
---

## Implementation Notes

### Decisions Made
- [Document any decisions made during review]

### Changelog
| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Completed code review, fixed X issues | Name |
```

### Step 9: Generate Review Report

```markdown
## Feature Code Review: FEAT-XXX

### Feature: [Title]
### Branch: feat/[name]
### Spec: specs/FEAT-XXX-name.md

---

### Checklist

#### Spec Compliance
- [x] Success criteria met
- [x] Hypotheses validated
- [x] Components implemented
- [x] Interfaces match spec

#### Task Completion
- [x] All tasks done (X/X)
- [x] Dependencies respected

#### Test Quality
- [x] All tests pass (X passed)
- [x] Coverage: XX% (target: 80%)
- [x] Mutation score: XX% (target: 80%)

#### Code Quality
- [x] Type checking passes
- [x] Linting passes
- [x] No security issues

---

### Issues Fixed
| Category | Issue | Resolution |
|----------|-------|------------|
| Tests | Missing edge case | Added test_edge_case |
| Coverage | Low in module X | Added 3 test cases |

### Remaining Issues
- [ ] None / List any blockers

---

### Verdict: READY FOR PR ✅ / NEEDS WORK ❌

### Next Steps
1. Run `/tm-submit-pr FEAT-XXX`
```

## Quality Gates Summary

| Gate | Requirement | Command |
|------|-------------|---------|
| Tests Pass | 100% | `uv run pytest` |
| Coverage | > 80% | `uv run pytest --cov` |
| Mutation Score | > 80% | `uv run mutmut run` |
| Type Check | No errors | `uv run mypy` |
| Lint | No errors | `uv run ruff check` |
| Security | No issues | `uv run bandit -r` |
| Tasks | All done | `tm list --tag FEAT-XXX` |

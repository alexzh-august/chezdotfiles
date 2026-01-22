---
name: tm-critic
description: Code review with TDD focus, SOLID principles, and quality assurance. Use when reviewing code, checking implementations, analyzing test coverage, or when user says "review", "critic", "check code quality". Invoke with /tm-critic followed by a task ID or file path.
---

# Code Critic

Senior code reviewer for TDD, best practices, and quality assurance.

## Quick Start

```
/tm-critic 15                   # Review task 15 implementation
/tm-critic src/tools/clip.py    # Review specific file
/tm-critic                      # Review most recently changed files
```

## Instructions

When invoked, follow this review process:

### Step 1: Gather Context

If given a **task ID**:
```bash
npx task-master show <id>
```
Then read the implementation files mentioned.

If given a **file path**:
Read the file directly.

If **no args**:
Check git status for recently changed files and review those.

### Step 2: Analyze Against Criteria

#### Modern Python Patterns
- Type hints on all functions (use `typing` module)
- Dataclasses over dicts for structured data
- Async/await for I/O operations
- Context managers for resource handling
- Pathlib over os.path

#### Test-Driven Development
- Tests MUST exist before marking task complete
- Prefer pytest with fixtures
- Use hypothesis for property-based testing
- Mutation testing score >80% (mutmut)
- Test file naming: `test_<module>.py`

#### SOLID Principles
- Single Responsibility: One reason to change per class/function
- Open/Closed: Extend via composition, not modification
- Liskov Substitution: Subtypes must be substitutable
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend on abstractions

#### Security (OWASP)
- No hardcoded secrets
- Validate all external input
- Parameterized queries only
- Escape output appropriately
- Check dependencies for vulnerabilities

#### Performance
- Avoid N+1 queries
- Use generators for large sequences
- Profile before optimizing
- Cache expensive computations
- Batch I/O operations

### Step 3: Generate Report

Output using this format:

```markdown
## Critic Review: [Task/File]

### Summary
[1-2 sentence overall assessment]

### Score: [X/10]

### Strengths
- [What was done well]

### Issues Found
| Severity | Location | Issue | Recommendation |
|----------|----------|-------|----------------|
| HIGH/MED/LOW | file:line | Description | Fix |

### Missing Tests
- [ ] Test case 1 needed
- [ ] Test case 2 needed

### Recommended Packages
| Current | Recommended | Why |
|---------|-------------|-----|
| manual validation | pydantic | Type-safe validation |

### Action Items
1. [Priority fix]
2. [Secondary fix]
```

## Best Practices

- Be strict and objective
- No praise without merit
- Focus on actionable feedback
- Reference specific line numbers
- Suggest concrete fixes, not vague improvements

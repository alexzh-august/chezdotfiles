---
name: tm-feature-task-planner
description: Plan features with git branches, spec documents, and task master integration. Use when starting a new feature, planning implementation, creating feature specs, or when user says "new feature", "plan feature", "feature spec", or "start feature". Combines TDD, hypothesis-driven, and spec-driven development.
---

# Feature Task Planner

Plan and structure features with git branches, spec documents, and organized tasks following TDD, hypothesis-driven, and spec-driven development.

## Quick Start

```
/tm-feature-task-planner "Add Looper device support"
/tm-feature-task-planner --from-prd section-name
```

## Instructions

When invoked, follow this structured process:

### Step 1: Create Feature Branch

```bash
# Derive branch name from feature title
# Format: feat/<kebab-case-feature-name>
git checkout -b feat/looper-device-support
```

### Step 2: Create Feature Spec Document

Create spec in `specs/` directory:

```bash
mkdir -p specs
```

Create `specs/FEAT-<number>-<name>.md` using the template below.

### Step 3: Add Tasks to Task Master

For each component in the spec:

```bash
npx task-master add-task --prompt="<task description>"
```

Tag all tasks with the feature ID:

```bash
npx task-master add-tag FEAT-<number>
npx task-master use-tag FEAT-<number>
```

### Step 4: Link Spec to Branch

Add to spec frontmatter:
```yaml
branch: feat/<feature-name>
created: <date>
status: planning | in-progress | review | done
```

## Spec Document Template

Use this structure for `specs/FEAT-XXX-feature-name.md`:

```markdown
---
id: FEAT-XXX
title: Feature Title
branch: feat/feature-name
created: YYYY-MM-DD
status: planning
author: <name>
---

# FEAT-XXX: Feature Title

## Overview
Brief description of what this feature accomplishes.

## Motivation
Why is this feature needed? What problem does it solve?

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] All tests pass
- [ ] Documentation updated

---

## Hypotheses

### H1: [Hypothesis Name]
**IF** we implement [change]
**THEN** [expected outcome]
**BECAUSE** [reasoning]

**Validation:**
- [ ] Test case to validate
- [ ] Metric to measure

### H2: [Next Hypothesis]
...

---

## Specification

### Components

#### Component 1: [Name]
**Purpose:** What it does
**Location:** `path/to/file.py`

**Interface:**
```python
def function_name(param: Type) -> ReturnType:
    """Docstring."""
    pass
```

**Behavior:**
- Condition 1 → Result 1
- Condition 2 → Result 2

#### Component 2: [Name]
...

### Data Structures

```python
@dataclass
class NewDataClass:
    field1: str
    field2: int
```

### Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| ErrorType | When it occurs | How to handle |

---

## Test Plan (TDD)

### Unit Tests

Write these BEFORE implementation:

```python
# tests/test_feature.py

def test_component1_happy_path():
    """Test normal operation."""
    # Arrange
    # Act
    # Assert
    pass

def test_component1_edge_case():
    """Test edge case."""
    pass

def test_component1_error_handling():
    """Test error conditions."""
    pass
```

### Integration Tests

```python
def test_integration_with_existing_system():
    """Test integration points."""
    pass
```

### Property-Based Tests (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.text())
def test_property_holds(num, text):
    """Property that should always hold."""
    pass
```

---

## Tasks

| ID | Task | Status | Depends On |
|----|------|--------|------------|
| 1 | Write failing tests for Component 1 | pending | - |
| 2 | Implement Component 1 | pending | 1 |
| 3 | Write failing tests for Component 2 | pending | - |
| 4 | Implement Component 2 | pending | 3 |
| 5 | Integration tests | pending | 2, 4 |
| 6 | Documentation | pending | 5 |

---

## Implementation Notes

### Decisions Made
- Decision 1: Chose X over Y because...

### Open Questions
- [ ] Question 1?
- [ ] Question 2?

### References
- [Link to relevant docs]
- [Related issue/PR]

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Created spec | Name |
```

## Workflow Integration

### Starting a Feature

```bash
# 1. Create feature plan
/tm-feature-task-planner "Feature Name"

# 2. Review generated spec
cat specs/FEAT-XXX-feature-name.md

# 3. Start with tests (TDD)
tm next  # Should be "Write failing tests"
```

### During Development

```bash
# Follow H-D-V-I loop from HYPOTHESES.md
# 1. Hypothesize - already in spec
# 2. Document - update spec with decisions
# 3. Validate - run tests
# 4. Iterate - update spec and tasks

# Mark tasks complete
tm set-status <id> done
```

### Completing a Feature

```bash
# 1. Ensure all tests pass
/tm-run-fix-tests

# 2. Full code review (spec, tasks, coverage)
/tm-run-fix-code-review FEAT-XXX

# 3. Submit PR (validates prerequisites)
/tm-submit-pr FEAT-XXX
```

## Best Practices

1. **Spec First** - Write spec before any code
2. **Tests First** - First tasks are always "write failing tests"
3. **Small Hypotheses** - Break into testable chunks
4. **Document Decisions** - Update spec as you learn
5. **One Branch Per Feature** - Keep changes isolated
6. **Tag Tasks** - All tasks belong to a feature tag

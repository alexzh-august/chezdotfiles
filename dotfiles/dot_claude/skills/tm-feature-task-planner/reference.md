# Feature Task Planner Reference

## Development Methodologies

### TDD (Test-Driven Development)

```
RED → GREEN → REFACTOR

1. RED: Write a failing test
2. GREEN: Write minimal code to pass
3. REFACTOR: Clean up while tests pass
```

**In Feature Specs:**
- First task for each component: "Write failing tests"
- Implementation task depends on test task
- Mutation testing validates test quality (mutmut)

### HDD (Hypothesis-Driven Development)

```
HYPOTHESIZE → DOCUMENT → VALIDATE → ITERATE

1. HYPOTHESIZE: Form testable prediction
2. DOCUMENT: Write it down BEFORE coding
3. VALIDATE: Implement and measure
4. ITERATE: Update hypothesis based on results
```

**In Feature Specs:**
- Hypotheses section captures predictions
- Each hypothesis has validation criteria
- Implementation Notes tracks what was learned

### SDD (Spec-Driven Development)

```
SPECIFY → IMPLEMENT → VERIFY

1. SPECIFY: Define behavior in spec document
2. IMPLEMENT: Code to match spec
3. VERIFY: Tests confirm spec compliance
```

**In Feature Specs:**
- Specification section defines contracts
- Interface definitions are written first
- Tests verify spec compliance

## Feature Lifecycle

```
┌─────────────┐
│  PLANNING   │ Create spec, define hypotheses
└──────┬──────┘
       ↓
┌─────────────┐
│   DESIGN    │ Write interfaces, data structures
└──────┬──────┘
       ↓
┌─────────────┐
│    TDD      │ Write failing tests first
└──────┬──────┘
       ↓
┌─────────────┐
│ IMPLEMENT   │ Make tests pass
└──────┬──────┘
       ↓
┌─────────────┐
│  VALIDATE   │ Integration tests, hypothesis validation
└──────┬──────┘
       ↓
┌─────────────┐
│   REVIEW    │ PR review, spec update
└──────┬──────┘
       ↓
┌─────────────┐
│    DONE     │ Merge, update docs
└─────────────┘
```

## Task Dependencies Pattern

```
Feature: Add Looper Support
├── T1: Write unit tests for LooperDevice class [pending]
├── T2: Implement LooperDevice class [pending, depends: T1]
├── T3: Write unit tests for looper tools [pending]
├── T4: Implement looper tools [pending, depends: T3]
├── T5: Write integration tests [pending, depends: T2, T4]
├── T6: Integration with MCP server [pending, depends: T5]
└── T7: Documentation [pending, depends: T6]
```

## Naming Conventions

### Branches
```
feat/<feature-name>     # New feature
fix/<bug-name>          # Bug fix
refactor/<area>         # Refactoring
docs/<topic>            # Documentation
test/<area>             # Test additions
```

### Spec Files
```
specs/FEAT-001-feature-name.md
specs/FEAT-002-another-feature.md
specs/FIX-001-bug-description.md
```

### Task Tags
```
FEAT-001    # Feature tasks
FIX-001     # Bug fix tasks
REFACTOR-001 # Refactoring tasks
```

## Git Workflow

```bash
# Start feature
git checkout main
git pull origin main
git checkout -b feat/feature-name

# During development
git add -A
git commit -m "feat(component): description"

# Complete feature
git push -u origin feat/feature-name
gh pr create --title "FEAT-XXX: Title" --body "Closes #issue"

# After merge
git checkout main
git pull origin main
git branch -d feat/feature-name
```

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Adding tests
- `refactor`: Code refactoring
- `docs`: Documentation
- `chore`: Maintenance

## Integration with Task Master

### Creating Tasks from Spec

```bash
# Parse spec into tasks
npx task-master parse-prd --input=specs/FEAT-001-feature.md

# Or manually add
npx task-master add-task --prompt="Write failing tests for Component 1"
npx task-master add-task --prompt="Implement Component 1"

# Add dependencies
npx task-master add-dependency --id=2 --depends-on=1
```

### Tracking Progress

```bash
# List feature tasks
npx task-master list --tag FEAT-001

# Get next task
npx task-master next

# Mark complete
npx task-master set-status <id> done
```

## Quality Gates

Before marking a feature complete:

- [ ] All tasks in `done` status
- [ ] All tests passing
- [ ] Mutation testing score > 80%
- [ ] No security vulnerabilities
- [ ] Documentation updated
- [ ] Spec status updated to `done`
- [ ] PR reviewed and approved

## Complete Workflow with Skills

```
┌────────────────────────────────────────────────────────────┐
│  /tm-feature-task-planner "Feature Name"                   │
│  Creates: branch + spec + tasks                            │
└────────────────────────────────┬───────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────┐
│  DEVELOPMENT LOOP                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ tm next → Get task                                  │   │
│  │ [Write tests] → RED                                 │   │
│  │ [Implement] → GREEN                                 │   │
│  │ [Refactor] → REFACTOR                               │   │
│  │ /tm-critic <id> → Review                            │   │
│  │ tm set-status <id> done                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  Repeat until all tasks done                               │
└────────────────────────────────┬───────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────┐
│  /tm-run-fix-tests                                         │
│  Run all tests, fix failures until green                   │
└────────────────────────────────┬───────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────┐
│  /tm-run-fix-code-review FEAT-XXX                          │
│  - Verify spec compliance                                  │
│  - Check all tasks done                                    │
│  - Validate coverage > 80%                                 │
│  - Run mutation tests > 80%                                │
│  - Type check, lint, security scan                         │
│  - Fix any issues found                                    │
└────────────────────────────────┬───────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────┐
│  /tm-submit-pr FEAT-XXX                                    │
│  - Validates all prerequisites                             │
│  - Creates PR with template                                │
│  - Links spec to PR                                        │
└────────────────────────────────┬───────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────┐
│  REVIEW & MERGE                                            │
│  - Address feedback                                        │
│  - Merge when approved                                     │
│  - Update spec status to 'done'                            │
└────────────────────────────────────────────────────────────┘
```

## Skills Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/tm-feature-task-planner` | Start feature | Beginning of new work |
| `/tm-critic` | Code review | After implementing each task |
| `/tm-run-fix-tests` | Test + fix | Before code review |
| `/tm-run-fix-code-review` | Full QA | Before PR |
| `/tm-submit-pr` | Create PR | Feature complete |

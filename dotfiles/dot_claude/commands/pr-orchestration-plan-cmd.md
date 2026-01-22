# TDD Feature Planning with Orchestration

This command initiates comprehensive TDD-based feature planning using the orchestration agent.

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: PARALLEL DISCOVERY                          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌───┐│
│  │ E1  │ │ E2  │ │ E3  │ │ E4  │ │ E5  │ │ E6  │ │ E7  │ │ E8  │ │...││
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └─┬─┘│
│     └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘       │
│                              ▼                                       │
│                    Context Synthesis                                 │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE 2: TDD PLANNING                                │
│                                                                         │
│     For each component:                                                 │
│     ┌─────────┐      ┌─────────┐      ┌─────────┐                      │
│     │ 🔴 RED  │─────▶│ 🟢 GREEN│─────▶│🔵REFACTOR│                      │
│     │ Tests   │      │  Impl   │      │ Quality │                      │
│     └─────────┘      └─────────┘      └─────────┘                      │
│                                                                         │
└─────────────────────────────┬───────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: CRITIC REVIEW                               │
│     ┌─────────────────┐      ┌─────────────────┐                       │
│     │   TDD Plan      │─────▶│   @agent        │                       │
│     │   Document      │      │   pr-critic     │                       │
│     └─────────────────┘      └────────┬────────┘                       │
│                                       │                                 │
│                              ┌────────┴────────┐                       │
│                              │ APPROVED │ NEEDS │                       │
│                              │          │REVISION│                       │
│                              └────────┬────────┘                       │
└───────────────────────────────────────┼─────────────────────────────────┘
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE 4: ITERATION (if needed)                       │
│     ┌─────────┐      ┌─────────┐      ┌─────────┐                      │
│     │ Parse   │─────▶│ Revise  │─────▶│Re-Review│                      │
│     │Feedback │      │  Plan   │      │         │                      │
│     └─────────┘      └─────────┘      └─────────┘                      │
│                                                                         │
│     Expected: 1-3 iterations based on complexity                       │
└─────────────────────────────┬───────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE 5: DEVELOPER REVIEW                            │
│                                                                         │
│     Present final plan with options:                                   │
│     ┌─────────┐   ┌─────────────┐   ┌─────────┐                        │
│     │ APPROVE │   │  REQUEST    │   │ REJECT  │                        │
│     │         │   │  CHANGES    │   │         │                        │
│     └────┬────┘   └──────┬──────┘   └────┬────┘                        │
│          │               │               │                              │
│          ▼               ▼               ▼                              │
│     Implement      Another Cycle    New Requirements                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Usage

```
/pr-orchestration-plan-cmd [feature description]
```

## Process

### Phase 1: Parallel Discovery

The orchestration agent launches **10 explore agents simultaneously**:

| Agent | Focus |
|-------|-------|
| 1 | Codebase structure & entry points |
| 2 | Package dependencies & versions |
| 3 | Code patterns & naming conventions |
| 4 | Test infrastructure & fixtures |
| 5 | Modern AI/ML solutions |
| 6 | Similar existing features |
| 7 | Configuration & feature flags |
| 8 | API patterns & error handling |
| 9 | Database models & migrations |
| 10 | CI/CD pipeline & quality gates |

### Phase 2: TDD Plan Creation

For each feature component, creates a complete TDD cycle:

**🔴 RED - Write Failing Tests**
- Test file location
- Test function specifications
- Expected assertions
- Why tests will initially fail

**🟢 GREEN - Minimal Implementation**
- Exact file changes needed
- Code to add/modify
- Dependencies required
- Expected: tests pass

**🔵 REFACTOR - Improve Quality**
- Pattern alignment
- Performance optimization
- Code simplification
- Expected: tests still pass

### Phase 3: Critic Review

Invokes the PR Critic agent to evaluate:
- TDD cycle completeness
- Python standards conformance
- Modern best practices
- Test coverage adequacy

Verdicts: `APPROVED` | `APPROVED WITH NOTES` | `NEEDS REVISION` | `MAJOR REWORK`

### Phase 4: Iteration

If feedback received:
1. Parse feedback by category (Critical/Suggestions/Minor)
2. Update affected TDD cycles
3. Document changes
4. Request re-review

Expected iterations: 1-3 based on complexity

### Phase 5: Developer Review

Final plan presented with:
- Executive summary
- TDD cycle breakdown
- File change manifest
- Test coverage map
- Risk assessment
- Approval request

## Output Format

```markdown
# TDD FEATURE PLAN
==================
Feature: [Name]
Status: [DRAFT | REVIEWED | APPROVED]
TDD Cycles: [N]

## Executive Summary
[2-3 sentences]

## Discovery Summary
[Key findings from explore agents]

## TDD Implementation Plan

### Cycle 1: [Component]

#### 🔴 RED - Failing Tests
[Test specifications]

#### 🟢 GREEN - Minimal Implementation
[Implementation steps]

#### 🔵 REFACTOR - Improve Quality
[Improvements]

## File Change Manifest
| File | Action | Phase |

## Test Coverage
- Unit: [List]
- Integration: [List]

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |

## Approval
- [x] Critic: [VERDICT]
- [ ] Developer: PENDING
```

## Example

```
User: /pr-orchestration-plan-cmd Add user preference storage with REST API

Agent:
1. Launches 10 explore agents → discovers pytest fixtures, SQLAlchemy models, FastAPI patterns
2. Creates TDD plan:
   - Cycle 1: Preference model (tests first)
   - Cycle 2: Preference repository
   - Cycle 3: API endpoints
3. Sends to pr-critic → receives feedback
4. Iterates → addresses feedback
5. Presents final plan → awaits developer approval
```

## Tips

- Start with clear, specific feature descriptions
- Let discovery phase complete fully before proceeding
- Address all critical feedback before seeking approval
- Keep the plan updated if implementation reveals new information

## When Plan is Approved

1. Switch to auto-accept mode (shift+tab)
2. Follow TDD cycles exactly:
   - Write tests first (RED)
   - Implement minimally (GREEN)
   - Improve quality (REFACTOR)
3. Run tests after each phase
4. Use `/verify` after completion

---
description: Plan a PR with planner-critic review loop
---

# PR Planning with Critic Review

This command initiates a structured planning process with iterative feedback.

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Planner   │────▶│   Critic    │────▶│   Planner   │
│  (Initial)  │     │  (Review)   │     │  (Revised)  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Feedback   │     │   Critic    │
                    │  Generated  │     │ (Approval)  │
                    └─────────────┘     └─────────────┘
```

## Process

### Phase 1: Initial Planning
Invoke the PR Planner agent to create an initial implementation plan:

```
@agent pr-planner

Create an implementation plan for: [REQUIREMENT]

Include:
- Technical approach
- Step-by-step implementation
- Files to modify
- Testing strategy
- Risk assessment
```

### Phase 2: Critic Review
Once the plan is ready, invoke the PR Critic agent:

```
@agent pr-critic

Review this implementation plan:
[PLAN]

Provide feedback on:
1. Modern best practices
2. Potential issues
3. Alternative approaches
4. Testing completeness
```

### Phase 3: Plan Revision
Address critic feedback and revise the plan:

```
@agent pr-planner

Revise the plan based on this feedback:
[CRITIC_FEEDBACK]

Update the plan to address:
- Critical issues
- Suggested improvements
- Open questions
```

### Phase 4: Final Approval
Get final approval from critic:

```
@agent pr-critic

Review the revised plan:
[REVISED_PLAN]

Previous feedback addressed:
[HOW_FEEDBACK_WAS_ADDRESSED]

Provide final verdict.
```

## Expected Iterations

- **Simple changes**: 1 iteration (plan → approve)
- **Medium changes**: 2 iterations (plan → feedback → revise → approve)
- **Complex changes**: 3+ iterations

## When Plan is Approved

Once the Critic approves:
1. Switch to auto-accept edits mode (shift+tab)
2. Begin implementation following the plan exactly
3. Run verification after each major step
4. Use `/verify` command after completion

## Tips

- Start with clear, specific requirements
- Don't rush the planning phase
- Address all critical feedback before proceeding
- Keep the plan updated as implementation reveals new information

## Example Usage

User: `/pr-plan Add user authentication with OAuth2`

Planner creates plan → Critic reviews → Planner revises → Critic approves → Implementation begins

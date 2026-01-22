# Comprehensive PR Review

Run a comprehensive PR review using all specialized agents in parallel.

## Usage

```
/pr-review [PR_NUMBER | PR_URL]
```

## Description

This command orchestrates multiple specialized review agents to provide a thorough analysis of a pull request. Each agent focuses on a specific aspect of code quality.

## Review Agents

The following agents run in parallel for maximum efficiency:

1. **Comments Agent** (`pr-review-comments`)
   - Evaluates documentation and inline comments
   - Checks for missing explanations
   - Identifies outdated comments

2. **Tests Agent** (`pr-review-tests`)
   - Analyzes test coverage
   - Evaluates test quality
   - Identifies missing test cases

3. **Errors Agent** (`pr-review-errors`)
   - Reviews error handling patterns
   - Identifies unhandled edge cases
   - Checks error propagation

4. **Types Agent** (`pr-review-types`)
   - Evaluates type safety
   - Reviews interface design
   - Checks type definitions

5. **Quality Agent** (`pr-review-quality`)
   - Assesses code maintainability
   - Identifies code smells
   - Checks adherence to best practices

6. **Simplify Agent** (`pr-review-simplify`)
   - Finds simplification opportunities
   - Identifies over-engineering
   - Suggests complexity reduction

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PR Review Orchestrator                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Fetch PR Information                                     │
│     └── gh pr view <PR> --json files,additions,deletions    │
│                                                              │
│  2. Launch Agents (Parallel)                                 │
│     ├── Comments Agent ────┐                                 │
│     ├── Tests Agent ───────┤                                 │
│     ├── Errors Agent ──────┼──► Aggregate Results            │
│     ├── Types Agent ───────┤                                 │
│     ├── Quality Agent ─────┤                                 │
│     └── Simplify Agent ────┘                                 │
│                                                              │
│  3. Generate Comprehensive Report                            │
│     └── Consolidated findings with priorities                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Instructions for Claude

When this command is invoked:

1. **Parse the PR reference** from the arguments:
   ```bash
   # If PR number provided
   gh pr view <PR_NUMBER> --json number,title,body,files,additions,deletions,baseRefName,headRefName

   # If no PR provided, check for current branch PR
   gh pr view --json number,title,body,files,additions,deletions,baseRefName,headRefName
   ```

2. **Get the full diff**:
   ```bash
   gh pr diff <PR_NUMBER>
   ```

3. **Launch all review agents in parallel** using the Task tool with subagent_type for each:
   - Each agent should receive the PR diff and file list
   - Each agent should follow its specialized review criteria
   - Use `run_in_background: true` for parallel execution

4. **Collect and aggregate results** from all agents

5. **Generate a consolidated report** with:
   - Executive summary
   - Critical issues (must fix)
   - High priority issues (should fix)
   - Medium priority issues (consider fixing)
   - Low priority suggestions
   - Positive observations

## Output Format

```markdown
# PR Review Report: #<PR_NUMBER> - <PR_TITLE>

## Executive Summary
[2-3 sentence overview of the PR quality]

## Review Statistics
| Agent | Critical | High | Medium | Low |
|-------|----------|------|--------|-----|
| Comments | X | X | X | X |
| Tests | X | X | X | X |
| Errors | X | X | X | X |
| Types | X | X | X | X |
| Quality | X | X | X | X |
| Simplify | X | X | X | X |
| **Total** | **X** | **X** | **X** | **X** |

## Critical Issues (Must Fix)
[List all critical issues from all agents]

## High Priority Issues (Should Fix)
[List all high priority issues]

## Medium Priority Issues (Consider Fixing)
[List all medium priority issues]

## Low Priority Suggestions
[List all suggestions]

## Positive Observations
[Consolidate positive feedback]

## Agent Reports

<details>
<summary>Comments & Documentation Report</summary>
[Full comments agent report]
</details>

<details>
<summary>Tests & Coverage Report</summary>
[Full tests agent report]
</details>

<details>
<summary>Error Handling Report</summary>
[Full errors agent report]
</details>

<details>
<summary>Type Design Report</summary>
[Full types agent report]
</details>

<details>
<summary>Code Quality Report</summary>
[Full quality agent report]
</details>

<details>
<summary>Simplification Report</summary>
[Full simplify agent report]
</details>
```

## Example

```bash
# Review current branch's PR
/pr-review

# Review specific PR by number
/pr-review 123

# Review PR by URL
/pr-review https://github.com/owner/repo/pull/123
```

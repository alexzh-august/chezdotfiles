# PR Review Orchestrator

This document describes how to orchestrate the PR review agents.

## Agent Orchestration Pattern

When running a comprehensive PR review, use the following pattern to maximize parallelism and efficiency:

### Step 1: Gather PR Information

```bash
# Get PR metadata
gh pr view <PR_NUMBER> --json number,title,body,author,files,additions,deletions,baseRefName,headRefName,mergeable,reviewDecision

# Get the full diff
gh pr diff <PR_NUMBER>

# Get list of changed files
gh pr view <PR_NUMBER> --json files --jq '.files[].path'
```

### Step 2: Prepare Agent Context

Each agent needs:
1. The PR diff content
2. List of changed files
3. PR metadata (title, description, author)
4. The agent's specific instructions

### Step 3: Launch Agents in Parallel

Use Claude Code's Task tool with `run_in_background: true` to run agents in parallel:

```
Task(
  description: "Review comments and documentation",
  subagent_type: "general-purpose",
  prompt: "[Comments Agent Instructions + PR Diff]",
  run_in_background: true
)

Task(
  description: "Review test coverage",
  subagent_type: "general-purpose",
  prompt: "[Tests Agent Instructions + PR Diff]",
  run_in_background: true
)

... (repeat for all agents)
```

### Step 4: Collect Results

Wait for all background agents to complete using `TaskOutput` with `block: true`.

### Step 5: Aggregate and Report

Combine results from all agents into a unified report:

1. **Deduplicate**: Remove duplicate findings across agents
2. **Prioritize**: Sort issues by severity (critical > high > medium > low)
3. **Consolidate**: Group related issues together
4. **Format**: Generate the final report

## Parallel Execution Model

```
                     ┌──────────────────────┐
                     │   Orchestrator       │
                     │   (Main Thread)      │
                     └──────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Comments Agent│     │ Tests Agent   │     │ Errors Agent  │
│ (Background)  │     │ (Background)  │     │ (Background)  │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                     │                     │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Types Agent   │     │ Quality Agent │     │ Simplify Agent│
│ (Background)  │     │ (Background)  │     │ (Background)  │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │   Result Aggregator  │
                     │   (Main Thread)      │
                     └──────────────────────┘
```

## Issue Severity Levels

| Severity | Description | Examples |
|----------|-------------|----------|
| Critical | Must fix before merge | Security vulnerabilities, data loss risks, crashes |
| High | Should fix before merge | Missing error handling, major bugs, test failures |
| Medium | Consider fixing | Code smells, minor bugs, style issues |
| Low | Optional improvements | Suggestions, enhancements, minor optimizations |

## Report Aggregation Rules

1. **Critical issues bubble up**: Any critical finding from any agent appears prominently
2. **Duplicate detection**: Same issue found by multiple agents is reported once
3. **Cross-references**: Related findings are linked together
4. **Confidence weighting**: Multiple agents finding same issue increases confidence

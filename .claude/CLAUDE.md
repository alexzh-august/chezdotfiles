# PR Review Toolkit for Claude Code

A comprehensive multi-agent system for reviewing pull requests, specializing in comments, tests, error handling, type design, code quality, and code simplification.

## Quick Start

```bash
# Run comprehensive PR review
/pr-review 123

# Run quick review (critical issues only)
/pr-review-quick 123
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/pr-review [PR]` | Run comprehensive review with all 6 agents |
| `/pr-review-quick [PR]` | Run quick review focusing on critical issues |

## Available Agents

This toolkit includes 6 specialized review agents that can be invoked individually:

### 1. Comments Agent (`pr-review-comments`)
Reviews documentation and inline comments:
- Comment quality and relevance
- Missing documentation
- Outdated comments
- API documentation completeness

### 2. Tests Agent (`pr-review-tests`)
Reviews testing quality:
- Test coverage for new code
- Test quality and assertions
- Missing test cases
- Test patterns and best practices

### 3. Errors Agent (`pr-review-errors`)
Reviews error handling:
- Error detection and validation
- Error propagation and wrapping
- Recovery mechanisms
- Edge case handling

### 4. Types Agent (`pr-review-types`)
Reviews type design:
- Type safety
- Interface design
- Generic usage
- API type definitions

### 5. Quality Agent (`pr-review-quality`)
Reviews code quality:
- Code structure and organization
- Naming and readability
- SOLID principles
- Code smells

### 6. Simplify Agent (`pr-review-simplify`)
Reviews for simplification:
- Over-engineering detection
- Dead code identification
- Unnecessary abstractions
- Complexity reduction

## How It Works

When you run `/pr-review`, the orchestrator:

1. **Fetches PR information** using `gh` CLI
2. **Launches all 6 agents in parallel** for maximum efficiency
3. **Collects results** from each specialized agent
4. **Aggregates findings** into a unified report
5. **Prioritizes issues** by severity (critical → high → medium → low)

## Configuration

The plugin can be configured in `.claude/settings.json`:

```json
{
  "pr-review-toolkit.parallelAgents": true,
  "pr-review-toolkit.includePositiveObservations": true,
  "pr-review-toolkit.maxIssuesPerAgent": 20,
  "pr-review-toolkit.severityThreshold": "low"
}
```

## Using Individual Agents

You can also use agents individually for focused reviews:

```
Use the Comments agent to review this PR for documentation quality.
```

This is useful when:
- You only need a specific type of review
- You want deeper analysis of one aspect
- You're iterating on feedback from a specific agent

## Example Output

```markdown
# PR Review Report: #123 - Add user authentication

## Executive Summary
This PR implements user authentication with good test coverage but needs
improved error handling in the login flow and additional documentation.

## Review Statistics
| Agent | Critical | High | Medium | Low |
|-------|----------|------|--------|-----|
| Comments | 0 | 2 | 3 | 1 |
| Tests | 0 | 1 | 2 | 0 |
| Errors | 1 | 2 | 1 | 0 |
| Types | 0 | 0 | 2 | 1 |
| Quality | 0 | 1 | 2 | 2 |
| Simplify | 0 | 0 | 1 | 3 |
| **Total** | **1** | **6** | **11** | **7** |

## Critical Issues (Must Fix)
1. [errors] `auth/login.go:45` - Unhandled error could expose credentials

...
```

## Requirements

- Claude Code CLI
- GitHub CLI (`gh`) for PR operations
- Git for diff operations

## Installation

Add the repository (one-time):
```bash
/plugin marketplace add anthropics/claude-code
```

Install the plugin:
```bash
/plugin install pr-review-toolkit@claude-code-plugins
```

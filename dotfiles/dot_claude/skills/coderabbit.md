---
name: coderabbit
description: "AI-powered code review with CodeRabbit CLI integration"
triggers:
  - coderabbit
  - code review
  - review code
  - cr review
  - review changes
  - review pr
  - review diff
figma:
  diagram_type: flowchart
  integration_points:
    - cli
    - github
---

# CodeRabbit CLI Integration

AI-powered code review using CodeRabbit CLI for comprehensive code analysis.

## Prerequisites

Ensure CodeRabbit CLI is installed and authenticated:

```bash
# Check if installed
coderabbit --help

# Check auth status
coderabbit auth status

# Login if needed
coderabbit auth login
```

## Usage Modes

### Interactive Review (Default)
For detailed, interactive code review with rich formatting:

```bash
coderabbit review
```

### Plain Text Review (For AI Agents)
When working with Claude Code, use plain text mode for token efficiency:

```bash
coderabbit review --plain
```

### Prompt-Only Mode (Minimal Output)
For maximum token efficiency in agentic workflows:

```bash
coderabbit review --prompt-only
```

## Review Scopes

```bash
# Review all changes (staged + unstaged + untracked)
coderabbit review --type all

# Review only committed changes
coderabbit review --type committed

# Review only uncommitted changes
coderabbit review --type uncommitted
```

## Branch Comparison

```bash
# Compare against specific base branch
coderabbit review --base main

# Compare against specific commit
coderabbit review --base-commit abc123
```

## Custom Instructions

Pass additional context files for more tailored reviews:

```bash
# Include CLAUDE.md for project context
coderabbit review --config CLAUDE.md

# Include multiple instruction files
coderabbit review --config CLAUDE.md coderabbit.yaml
```

## Autonomous Development Loop

For AI-assisted development workflows, use this pattern:

1. **Write code** - Implement feature or fix
2. **Run review** - `coderabbit review --plain`
3. **Apply feedback** - Fix identified issues
4. **Re-review** - Verify improvements
5. **Commit** - When review passes

Example prompt for Claude Code:

```
Implement [feature]. After each change, run `coderabbit review --plain`
and apply the suggestions until the code passes review.
```

## Rate Limits

| Plan | Reviews/Hour |
|------|--------------|
| Free | 2 |
| Trial | 5 |
| Pro | 8 per seat |

## Workflow Integration

### Pre-Commit Review
```bash
# Run before committing
coderabbit review --type uncommitted --plain
```

### PR Preparation
```bash
# Review all changes against main before PR
coderabbit review --base main --plain
```

### CI Integration
CodeRabbit also offers GitHub App integration for automated PR reviews.
See: https://docs.coderabbit.ai

## Troubleshooting

### Authentication Issues
```bash
# Check status
coderabbit auth status

# Re-authenticate
coderabbit auth logout
coderabbit auth login
```

### Organization Switching
```bash
# List and switch orgs
coderabbit auth org
```

### Update CLI
```bash
coderabbit update
```

## Related Skills

- `/review` - General code review workflow
- `/pr-review-toolkit:review-pr` - Multi-agent PR review
- `/commit-push-pr` - Full PR workflow with reviews

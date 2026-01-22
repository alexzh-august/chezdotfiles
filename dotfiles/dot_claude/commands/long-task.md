---
description: Run a long task with verification
---

# Long-Running Task

For very long-running tasks, set up proper verification and monitoring.

## Options for Long Tasks

### Option A: Background Agent Verification
Prompt Claude to verify its work with a background agent when done:
"When you complete this task, spawn a background agent to verify the implementation works correctly."

### Option B: Stop Hook
Add a Stop hook in settings.json to run verification automatically:

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "./scripts/verify-implementation.sh"
      }
    ]
  }
}
```

### Option C: Ralph-Wiggum Plugin
Use the ralph-wiggum plugin for complex verification:
https://github.com/anthropics/claude-code/tree/main/plugins

## Permission Modes for Long Tasks

For sandboxed environments where you trust the operations:

```bash
# Don't ask for permissions (prompts with Y/N but defaults to Y)
claude --permission-mode=dontAsk

# Skip all permission prompts (use in sandbox only!)
claude --dangerously-skip-permissions
```

## Monitoring

- Enable terminal notifications in settings.json
- Number your terminal tabs 1-5 if running parallel sessions
- Watch for system notifications when Claude needs input

## Instructions

1. Set up verification method (A, B, or C above)
2. Choose appropriate permission mode
3. Start the task with clear acceptance criteria
4. Let Claude cook without blocking
5. Review verification results when complete

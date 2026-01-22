---
description: Debug an issue systematically
---

# Debug Issue

Systematically debug an issue using available tools.

## Pre-computed context

```bash
# Recent error logs if available
if [ -d "logs" ]; then
  RECENT_LOGS=$(tail -50 logs/*.log 2>/dev/null | head -100)
fi

# Git recent changes (might have introduced bug)
RECENT_CHANGES=$(git log --oneline -10)

# Currently modified files
MODIFIED=$(git status --porcelain)
```

## Instructions

### 1. Gather Information
- What is the expected behavior?
- What is the actual behavior?
- When did it start happening?
- Can it be reproduced consistently?

### 2. Check Logs
- Application logs
- System logs
- Error tracking (Sentry, etc.)

### 3. Isolate the Problem
- Identify the failing component
- Create minimal reproduction
- Check recent changes that might have caused it

### 4. Form Hypothesis
- What could cause this behavior?
- List 3 most likely causes

### 5. Test Hypothesis
- Add logging/debugging
- Run with test data
- Verify or rule out each hypothesis

### 6. Fix and Verify
- Implement fix
- Write test that would have caught this
- Verify fix resolves the issue

## Tools Available

- Sentry MCP: Grab error logs with `mcp__sentry__*`
- BigQuery: Run analytics queries with `bq query`
- Slack MCP: Search team discussions for context

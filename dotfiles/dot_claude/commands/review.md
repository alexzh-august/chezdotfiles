---
description: Review code changes before committing
---

# Review Changes

Review current changes for quality before committing.

## Pre-computed context

```bash
# Staged changes
STAGED=$(git diff --cached --stat)

# Unstaged changes  
UNSTAGED=$(git diff --stat)

# Full diff for review
DIFF=$(git diff HEAD --unified=5 | head -200)
```

## Instructions

Review the changes for:

### Code Quality
- [ ] No debug code left in (console.log, print statements, etc.)
- [ ] No commented-out code
- [ ] No hardcoded secrets or credentials
- [ ] Meaningful variable/function names
- [ ] Appropriate error handling

### Logic
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] No obvious bugs or race conditions
- [ ] Performance considerations addressed

### Style
- [ ] Consistent with project style
- [ ] Properly formatted
- [ ] Good comments where needed (not obvious stuff)

### Tests
- [ ] Tests updated if behavior changed
- [ ] New functionality has tests

## Output

After review, provide:
1. Summary of changes
2. Any issues found
3. Recommendations
4. Confidence level (ready to merge / needs work)

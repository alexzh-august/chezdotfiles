---
description: Run tests and verify changes
---

# Test Changes

Run the test suite to verify your changes work correctly.

## Pre-computed context

```bash
# Detect test framework
if [ -f "package.json" ]; then
  TEST_CMD=$(cat package.json | jq -r '.scripts.test // "npm test"')
  echo "Node project detected. Test command: $TEST_CMD"
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  TEST_CMD="pytest"
  echo "Python project detected. Test command: $TEST_CMD"
elif [ -f "Cargo.toml" ]; then
  TEST_CMD="cargo test"
  echo "Rust project detected. Test command: $TEST_CMD"
elif [ -f "go.mod" ]; then
  TEST_CMD="go test ./..."
  echo "Go project detected. Test command: $TEST_CMD"
else
  TEST_CMD="echo 'No test framework detected'"
fi

# Find recent test files
RECENT_TESTS=$(find . -name "*test*" -o -name "*spec*" -type f 2>/dev/null | head -10)

# Changed files that might need tests
CHANGED=$(git diff --name-only HEAD~1 2>/dev/null || echo "")
```

## Instructions

1. Run the full test suite first
2. If tests fail, analyze the failures
3. Fix failing tests or update tests if behavior intentionally changed
4. Re-run tests until all pass
5. Consider if new tests are needed for recent changes

## Verification Checklist

- [ ] All existing tests pass
- [ ] New functionality has test coverage
- [ ] Edge cases are tested
- [ ] No flaky tests introduced

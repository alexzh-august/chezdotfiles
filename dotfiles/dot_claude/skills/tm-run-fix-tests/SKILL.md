---
name: tm-run-fix-tests
description: Run tests and fix issues until all tests pass. Use when user says "run tests", "fix tests", "make tests pass", or wants to ensure test suite is green. Iteratively runs pytest, analyzes failures, and fixes code until all tests pass.
---

# Run and Fix Tests

Iteratively run tests and fix issues until the entire test suite passes.

## Quick Start

```
/tm-run-fix-tests                    # Run all tests, fix failures
/tm-run-fix-tests tests/test_clip.py # Run specific test file
/tm-run-fix-tests --feature FEAT-001 # Run tests for a feature
```

## Instructions

### Step 1: Identify Test Scope

If given a **file path**:
```bash
uv run pytest <file> -v
```

If given a **feature tag**:
```bash
# Find feature spec
cat specs/FEAT-XXX-*.md
# Identify test files from spec
# Run those tests
uv run pytest tests/test_<component>.py -v
```

If **no args**:
```bash
uv run pytest -v
```

### Step 2: Run Tests and Capture Output

```bash
uv run pytest -v --tb=short 2>&1
```

Capture:
- Number of passed/failed/errors
- Failure messages and tracebacks
- Which files/functions failed

### Step 3: Analyze Failures

For each failure, determine:

1. **Test bug** - Test itself is wrong
   - Fix the test assertion or setup

2. **Implementation bug** - Code doesn't match spec
   - Fix the implementation

3. **Missing code** - Feature not implemented
   - Implement the missing functionality

4. **Environment issue** - Missing deps, config
   - Fix environment setup

### Step 4: Fix Issues

For each failure:

1. Read the failing test
2. Read the implementation being tested
3. Identify the root cause
4. Apply the fix
5. Re-run that specific test to verify

```bash
# Run single test to verify fix
uv run pytest tests/test_file.py::test_function -v
```

### Step 5: Iterate Until Green

```
LOOP:
  1. Run full test suite
  2. If all pass → DONE
  3. If failures → Fix first failure
  4. Go to step 1
```

### Step 6: Report Results

Output final status:

```markdown
## Test Run Report

### Status: PASSED ✅ / FAILED ❌

### Summary
- Total: X tests
- Passed: X
- Failed: X
- Errors: X

### Fixes Applied
| Test | Issue | Fix |
|------|-------|-----|
| test_function | AssertionError | Fixed expected value |

### Remaining Issues (if any)
- [ ] Issue that couldn't be auto-fixed
```

## Configuration

### pytest.ini / pyproject.toml settings
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

### Common Flags
```bash
-v              # Verbose output
--tb=short      # Short tracebacks
-x              # Stop on first failure
--lf            # Run last failed tests
-k "pattern"    # Run tests matching pattern
```

## Best Practices

- Fix one test at a time
- Run specific test after fix before full suite
- Don't modify tests to make them pass (unless test is wrong)
- Check if fix breaks other tests
- Commit working state before attempting risky fixes

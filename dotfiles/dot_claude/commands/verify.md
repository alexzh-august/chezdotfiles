---
description: Verify implementation works correctly (the most important tip!)
---

# Verify Implementation

This is the most important step - give Claude a feedback loop to verify work.

## Pre-computed context

```bash
# Project type detection
if [ -f "package.json" ]; then
  PROJECT_TYPE="node"
  BUILD_CMD=$(cat package.json | jq -r '.scripts.build // "npm run build"')
  TEST_CMD=$(cat package.json | jq -r '.scripts.test // "npm test"')
  START_CMD=$(cat package.json | jq -r '.scripts.start // .scripts.dev // "npm start"')
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  PROJECT_TYPE="python"
  BUILD_CMD="echo 'No build needed'"
  TEST_CMD="pytest"
  START_CMD="python main.py"
elif [ -f "Cargo.toml" ]; then
  PROJECT_TYPE="rust"
  BUILD_CMD="cargo build"
  TEST_CMD="cargo test"
  START_CMD="cargo run"
else
  PROJECT_TYPE="unknown"
fi

echo "Project type: $PROJECT_TYPE"
```

## Verification Strategy

Verification looks different for each domain. Choose the appropriate method:

### For Backend/API Changes
1. Run the test suite
2. Start the server locally
3. Make test API calls with curl
4. Verify responses match expectations

### For Frontend/UI Changes
1. Build the project
2. Start dev server
3. Open in browser (use Claude Chrome extension if available)
4. Test the UI manually
5. Check for console errors
6. Verify UX feels good

### For CLI Tools
1. Build the tool
2. Run with --help to verify it starts
3. Test main commands with sample inputs
4. Verify output matches expectations

### For Data Pipelines
1. Run with sample/test data
2. Verify output schema
3. Check data quality metrics
4. Validate transformations

## Instructions

1. Identify what type of change was made
2. Select appropriate verification method
3. Run verification
4. If issues found, fix and verify again
5. Only mark complete when verification passes

## Quality Gate

Claude should not consider a task complete until:
- [ ] Build passes
- [ ] Tests pass
- [ ] Manual verification confirms expected behavior
- [ ] No errors in logs/console

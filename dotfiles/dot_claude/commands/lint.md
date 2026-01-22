---
description: Run linter and fix issues
---

# Lint Code

Run the linter and fix any issues found.

## Pre-computed context

```bash
# Detect linter
if [ -f "package.json" ]; then
  LINT_CMD=$(cat package.json | jq -r '.scripts.lint // "npx eslint ."')
  echo "Node project. Lint command: $LINT_CMD"
elif [ -f "pyproject.toml" ]; then
  LINT_CMD="ruff check . --fix"
  echo "Python project. Using ruff"
elif [ -f "Cargo.toml" ]; then
  LINT_CMD="cargo clippy"
  echo "Rust project. Using clippy"
else
  LINT_CMD="echo 'No linter detected'"
fi

# Changed files for targeted linting (optional: filter to these if linter supports it)
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
echo "Changed files: $CHANGED_FILES"
```

## Instructions

1. Run the linter (on changed files if supported, or full project)
2. Fix any auto-fixable issues
3. Manually address remaining issues
4. Run linter again to verify all issues resolved
5. Run typecheck if available

## Common Lint Fixes

- Unused imports → Remove them
- Missing semicolons → Add them (if required by style)
- Inconsistent quotes → Standardize to project convention
- Long lines → Break into multiple lines
- Type errors → Add proper type annotations

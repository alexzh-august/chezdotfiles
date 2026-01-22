#!/bin/bash
# Smart Python formatter - only runs in Python projects
# Checks for pyproject.toml, setup.py, or .py files

# Skip if not a Python project
if [[ ! -f "pyproject.toml" ]] && [[ ! -f "setup.py" ]] && [[ -z $(find . -maxdepth 2 -name "*.py" 2>/dev/null | head -1) ]]; then
    exit 0
fi

# Run ruff format only on recently modified Python files (last 5 seconds)
find . -maxdepth 5 -name "*.py" -mmin -0.1 -exec ruff format {} \; 2>/dev/null || true

exit 0

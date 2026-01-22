# Cached LLMs.txt Context Files

This directory contains cached llms.txt documentation for AI-assisted development.

## Available Contexts

| File | Source | Description |
|------|--------|-------------|
| `databricks.txt` | https://docs.databricks.com/llms.txt | Databricks MCP, Unity Catalog, SQL, ML APIs |

## Usage

### In Slash Commands
Reference these files to provide context:
```markdown
## Context
Load: .claude/context/llms/databricks.txt
```

### In Python
```python
from pathlib import Path

def load_llms_context(name: str) -> str:
    """Load cached llms.txt context."""
    path = Path(".claude/context/llms") / f"{name}.txt"
    return path.read_text() if path.exists() else ""

# Example
databricks_context = load_llms_context("databricks")
```

## Updating Cache

To refresh cached content:
```bash
# Fetch latest and update
curl -s https://docs.databricks.com/llms.txt > .claude/context/llms/databricks.txt
```

## Planned Additions

- `claude.txt` - https://docs.anthropic.com/llms.txt
- `neon.txt` - https://neon.com/llms.txt
- `parallel.txt` - https://parallel.ai/llms.txt
- `graphite.txt` - https://graphite.com/docs/llms.txt

## Last Updated

- databricks.txt: 2026-01-21

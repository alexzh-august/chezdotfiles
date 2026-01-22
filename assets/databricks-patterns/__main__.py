"""Allow running as python -m databricks_patterns."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())

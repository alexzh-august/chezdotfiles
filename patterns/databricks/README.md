# Databricks Code Pattern Detectors

Optimized pattern detectors that define DO and DON'T patterns for Databricks SDK usage. These patterns help code generators, code reviewers, and refactoring tools raise the bar on code quality.

## Overview

This directory contains pattern definitions for:

| Pattern File | Focus Area | Key Concerns |
|--------------|------------|--------------|
| `unity_catalog.yaml` | Unity Catalog | Namespace conventions, permissions, governance |
| `mcp_integration.yaml` | MCP Servers | Configuration, Genie, Vector Search, DBSQL |
| `authentication.yaml` | Auth & Security | OAuth, PAT, Service Principals, secrets |
| `sql_execution.yaml` | SQL Safety | Injection prevention, optimization, error handling |
| `templates.py` | Code Generators | Production-ready code templates |

## Pattern Structure

Each YAML file follows this structure:

```yaml
metadata:
  name: pattern-name
  version: "1.0.0"
  description: What this pattern set covers
  packages:
    - relevant-python-packages

patterns:
  pattern_name:
    description: What this pattern addresses
    severity: critical | error | warning | info

    do:
      - pattern: |
          # Good code example
        explanation: Why this is the right approach

    dont:
      - pattern: |
          # Bad code example
        explanation: Why this is problematic
        anti_pattern_regex: 'regex to detect this anti-pattern'

generators:
  generator_name:
    description: What this generates
    template: |
      # Generated code template

refactors:
  refactor_name:
    description: What this refactoring does
    trigger: 'regex that triggers this refactor'
    fix: |
      # How to fix the code
```

## Quick Reference

### Unity Catalog Patterns

**DO:**
```python
# Always use three-level namespace
df = spark.table("my_catalog.my_schema.my_table")

# Escape special characters
spark.sql("SELECT * FROM catalog.schema.`special-table`")

# Handle permissions gracefully
try:
    df = spark.table(table_path)
except AnalysisException as e:
    if "PERMISSION_DENIED" in str(e):
        raise PermissionError(f"No access to {table_path}")
```

**DON'T:**
```python
# Unqualified table names (ambiguous)
df = spark.table("my_table")  # BAD

# Relying on USE statements
spark.sql("USE CATALOG my_catalog")  # BAD for production
```

### Authentication Patterns

**DO:**
```python
# Use environment variables
client = WorkspaceClient(
    host=os.environ["DATABRICKS_HOST"],
    token=os.environ["DATABRICKS_TOKEN"]
)

# Use OAuth for production
config = Config(
    host=host,
    auth_type="oauth-m2m",
    client_id=os.environ["DATABRICKS_CLIENT_ID"],
    client_secret=os.environ["DATABRICKS_CLIENT_SECRET"]
)
```

**DON'T:**
```python
# Hardcoded tokens (SECURITY RISK)
client = WorkspaceClient(token="dapi1234...")  # NEVER!

# Logging tokens
logger.info(f"Token: {token}")  # NEVER!
```

### SQL Execution Patterns

**DO:**
```python
# Parameterized queries
cursor.execute(
    "SELECT * FROM users WHERE id = :user_id",
    {"user_id": user_input}
)

# Validate identifiers
if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
    raise ValueError("Invalid table name")
```

**DON'T:**
```python
# String formatting with user input (SQL INJECTION!)
sql = f"SELECT * FROM users WHERE id = '{user_input}'"  # NEVER!

# SELECT * in production
spark.sql("SELECT * FROM large_table")  # Wasteful
```

### MCP Integration Patterns

**DO:**
```python
# Use environment variable references in config
{
    "env": {
        "DATABRICKS_TOKEN": "${DATABRICKS_TOKEN}"
    }
}

# Use Genie for read-only natural language queries
result = await genie.query("Show sales by region for Q4")

# Use DBSQL for pipeline SQL
result = await execute_sql(sql, warehouse_id=WAREHOUSE_ID)
```

**DON'T:**
```python
# Hardcoded tokens in config
"DATABRICKS_TOKEN": "dapi123..."  # NEVER!

# Using Genie for write operations
await genie.query("DELETE FROM users")  # BAD

# HTTP instead of HTTPS
"url": "http://workspace.cloud.databricks.com"  # NEVER!
```

## Using the Code Generators

```python
from patterns.databricks.templates import (
    generate_unity_catalog_client,
    generate_mcp_client,
    generate_safe_sql_executor,
    generate_claude_code_mcp_config,
)

# Generate a Unity Catalog client
code = generate_unity_catalog_client("production", "analytics")

# Generate an async MCP client
code = generate_mcp_client(
    "https://workspace.cloud.databricks.com",
    genie_space_id="space-123"
)

# Generate Claude Code MCP configuration
config = generate_claude_code_mcp_config(
    "https://workspace.cloud.databricks.com"
)
```

## Integration with Tools

### With Linters

The `anti_pattern_regex` fields can be used with custom linter rules:

```python
# Example: Custom ruff rule
DATABRICKS_ANTIPATTERNS = [
    r'spark\.table\s*\(\s*["\'][^.]+["\']\s*\)',  # Unqualified table
    r'token\s*=\s*["\']dapi[a-zA-Z0-9]+',          # Hardcoded token
    r'f["\']SELECT.*\{.*\}["\']',                  # SQL injection risk
]
```

### With Code Review

Use patterns to guide code review:

1. Check for severity: `critical` and `error` patterns
2. Look for `anti_pattern_regex` matches
3. Suggest `refactors` when anti-patterns found

### With AI Assistants

These patterns can be used as context for AI code assistants:

```
Use the Databricks patterns in patterns/databricks/ to:
1. Validate code follows DO patterns
2. Flag code matching DON'T patterns
3. Suggest refactors from the refactors section
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| `critical` | Security vulnerability | Must fix immediately |
| `error` | Will cause runtime failures | Fix before merge |
| `warning` | Best practice violation | Should fix |
| `info` | Optimization opportunity | Consider fixing |

## Contributing

When adding new patterns:

1. Add to appropriate YAML file or create new one
2. Include both DO and DON'T examples
3. Provide clear explanations
4. Add `anti_pattern_regex` for static analysis
5. Add generator template if applicable
6. Add refactor rule if automated fix is possible

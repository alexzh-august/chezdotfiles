"""
SQL Execution Pattern Definitions

Best practices for Databricks SQL operations:
- Statement execution
- Query optimization
- Error handling
- Result handling
"""

from typing import TypedDict


class Pattern(TypedDict):
    id: str
    severity: str
    category: str
    description: str
    do_pattern: str | None
    dont_pattern: str | None
    regex: str | None
    fix_suggestion: str | None


SQL_EXECUTION_PATTERNS: list[Pattern] = [
    # Query Safety
    {
        "id": "SQL001",
        "severity": "error",
        "category": "safety",
        "description": "Use execute_sql_read_only for SELECT queries",
        "do_pattern": "execute_sql_read_only for read operations",
        "dont_pattern": "execute_sql for simple SELECT queries",
        "regex": r"execute_sql\s*\(\s*['\"]SELECT",
        "fix_suggestion": "Use execute_sql_read_only() for SELECT queries",
    },
    {
        "id": "SQL002",
        "severity": "error",
        "category": "safety",
        "description": "Never use string concatenation for SQL parameters",
        "do_pattern": 'execute_sql("SELECT * FROM t WHERE id = :id", params={"id": value})',
        "dont_pattern": 'execute_sql(f"SELECT * FROM t WHERE id = {value}")',
        "regex": r"execute_sql\s*\(\s*f['\"]|execute_sql\s*\([^)]*\+\s*",
        "fix_suggestion": "Use parameterized queries with named parameters",
    },
    {
        "id": "SQL003",
        "severity": "warning",
        "category": "safety",
        "description": "Validate table names before dynamic SQL",
        "do_pattern": "Whitelist allowed table names before use",
        "dont_pattern": "Using user input directly as table names",
        "regex": r"(?:FROM|INTO|UPDATE|JOIN)\s+['\"]?\s*\{",
        "fix_suggestion": "Validate table names against allowed list before use",
    },
    # Long-Running Queries
    {
        "id": "SQL004",
        "severity": "info",
        "category": "async",
        "description": "Use poll_sql_result for long-running queries",
        "do_pattern": "result_id = execute_sql(...); poll_sql_result(result_id)",
        "dont_pattern": "Blocking on execute_sql for long queries",
        "regex": None,
        "fix_suggestion": "For queries >30s, use async pattern with poll_sql_result",
    },
    {
        "id": "SQL005",
        "severity": "warning",
        "category": "async",
        "description": "Implement timeout handling for SQL execution",
        "do_pattern": "Set appropriate timeout, handle TimeoutError",
        "dont_pattern": "Unbounded wait for query completion",
        "regex": None,
        "fix_suggestion": "Set timeout parameter and handle timeout exceptions",
    },
    # Result Handling
    {
        "id": "SQL006",
        "severity": "warning",
        "category": "results",
        "description": "Use chunked retrieval for large result sets",
        "do_pattern": "Paginate results with LIMIT/OFFSET or cursor",
        "dont_pattern": "SELECT * without LIMIT on large tables",
        "regex": r"SELECT\s+\*\s+FROM\s+[\w.`]+\s*(?:WHERE|ORDER|$)(?!.*LIMIT)",
        "fix_suggestion": "Add LIMIT clause or use result chunking",
    },
    {
        "id": "SQL007",
        "severity": "info",
        "category": "results",
        "description": "Close result sets after processing",
        "do_pattern": "Use context manager or explicit close",
        "dont_pattern": "Leaving result cursors open",
        "regex": None,
        "fix_suggestion": "Use 'with' statement or call close() on result sets",
    },
    # Performance
    {
        "id": "SQL008",
        "severity": "warning",
        "category": "performance",
        "description": "Select only needed columns instead of SELECT *",
        "do_pattern": "SELECT col1, col2 FROM table",
        "dont_pattern": "SELECT * FROM table",
        "regex": r"SELECT\s+\*\s+FROM",
        "fix_suggestion": "Specify column names explicitly for better performance",
    },
    {
        "id": "SQL009",
        "severity": "info",
        "category": "performance",
        "description": "Use partition pruning with WHERE clauses",
        "do_pattern": "WHERE partition_col = 'value'",
        "dont_pattern": "Full table scans on partitioned tables",
        "regex": None,
        "fix_suggestion": "Include partition column in WHERE clause",
    },
    {
        "id": "SQL010",
        "severity": "warning",
        "category": "performance",
        "description": "Avoid SELECT DISTINCT on large datasets",
        "do_pattern": "GROUP BY or window functions for deduplication",
        "dont_pattern": "SELECT DISTINCT on millions of rows",
        "regex": r"SELECT\s+DISTINCT.*FROM.*(?!LIMIT\s+\d+)",
        "fix_suggestion": "Use GROUP BY or add LIMIT for large distinct operations",
    },
    # Data Validation
    {
        "id": "SQL011",
        "severity": "error",
        "category": "validation",
        "description": "Validate data before merge operations",
        "do_pattern": "Check constraints before MERGE/INSERT",
        "dont_pattern": "MERGE without data validation",
        "regex": None,
        "fix_suggestion": "Run validation query before merge operations",
    },
    {
        "id": "SQL012",
        "severity": "warning",
        "category": "validation",
        "description": "Use COUNT(*) to verify row counts after operations",
        "do_pattern": "SELECT COUNT(*) after INSERT/UPDATE to verify",
        "dont_pattern": "Assuming operation success without verification",
        "regex": None,
        "fix_suggestion": "Verify row counts match expected after DML operations",
    },
    # Transaction Handling
    {
        "id": "SQL013",
        "severity": "warning",
        "category": "transactions",
        "description": "Use explicit transactions for multi-statement operations",
        "do_pattern": "BEGIN; statements...; COMMIT;",
        "dont_pattern": "Multiple independent statements for related changes",
        "regex": None,
        "fix_suggestion": "Wrap related statements in BEGIN/COMMIT block",
    },
    # Error Handling
    {
        "id": "SQL014",
        "severity": "error",
        "category": "error_handling",
        "description": "Handle SQL execution errors gracefully",
        "do_pattern": "try/except with specific error types",
        "dont_pattern": "Bare except or ignoring errors",
        "regex": r"except\s*:|except\s+Exception\s*:",
        "fix_suggestion": "Catch specific SQL exception types",
    },
    {
        "id": "SQL015",
        "severity": "warning",
        "category": "error_handling",
        "description": "Log failed SQL queries for debugging",
        "do_pattern": "Log query and error details on failure",
        "dont_pattern": "Silent failures without logging",
        "regex": None,
        "fix_suggestion": "Add logging for SQL execution failures",
    },
]

# SQL Query Templates
SQL_TEMPLATES = {
    "read_only_select": """
-- DO: Use read-only execution for SELECT queries
SELECT {columns}
FROM {catalog}.{schema}.{table}
WHERE {conditions}
LIMIT {limit}
""",
    "validation_before_merge": """
-- DO: Validate before merge
SELECT COUNT(*) as errors
FROM {catalog}.{schema}.{table}
WHERE {validation_rule} = FALSE
""",
    "parameterized_query": """
-- DO: Use parameterized queries
-- Python: execute_sql(query, params={"id": value, "name": name})
SELECT *
FROM catalog.schema.table
WHERE id = :id AND name = :name
""",
    "chunked_retrieval": """
-- DO: Use pagination for large results
SELECT {columns}
FROM {catalog}.{schema}.{table}
ORDER BY {order_column}
LIMIT {page_size}
OFFSET {offset}
""",
}

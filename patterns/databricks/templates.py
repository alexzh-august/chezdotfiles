"""Databricks Code Generator Templates.

Pre-built templates for common Databricks patterns that raise the bar on code quality.
These generators produce production-ready code following best practices.

Usage:
    from patterns.databricks.templates import generate_unity_catalog_client
    code = generate_unity_catalog_client("my_catalog", "my_schema")
"""

from dataclasses import dataclass
from typing import Optional
from textwrap import dedent


@dataclass
class TemplateConfig:
    """Configuration for code generation."""

    catalog: str = "main"
    schema: str = "default"
    include_tests: bool = True
    include_typing: bool = True
    async_mode: bool = False


def generate_unity_catalog_client(
    catalog: str, schema: str, include_tests: bool = True
) -> str:
    """Generate a Unity Catalog client with best practices.

    Args:
        catalog: Default catalog name
        schema: Default schema name
        include_tests: Whether to include test stubs

    Returns:
        Generated Python code as string
    """
    code = dedent(f'''
        """Unity Catalog Client for {catalog}.{schema}.

        Auto-generated using Databricks pattern templates.
        Follows Unity Catalog best practices for namespace management.
        """
        from dataclasses import dataclass
        from typing import Optional
        import os
        import logging

        from pyspark.sql import DataFrame, SparkSession
        from pyspark.sql.utils import AnalysisException

        logger = logging.getLogger(__name__)


        @dataclass
        class TableReference:
            """Fully qualified table reference."""

            catalog: str
            schema: str
            table: str

            @property
            def full_path(self) -> str:
                """Return three-level namespace path."""
                return f"{{self.catalog}}.{{self.schema}}.{{self.table}}"

            def __str__(self) -> str:
                return self.full_path


        class UnityCatalogClient:
            """Client for Unity Catalog operations with proper namespace handling.

            Features:
            - Always uses three-level namespace (catalog.schema.table)
            - Proper permission error handling
            - Table existence validation
            """

            DEFAULT_CATALOG = "{catalog}"
            DEFAULT_SCHEMA = "{schema}"

            def __init__(
                self,
                spark: SparkSession,
                catalog: Optional[str] = None,
                schema: Optional[str] = None,
            ):
                """Initialize Unity Catalog client.

                Args:
                    spark: Active SparkSession
                    catalog: Override default catalog
                    schema: Override default schema
                """
                self.spark = spark
                self.catalog = catalog or self.DEFAULT_CATALOG
                self.schema = schema or self.DEFAULT_SCHEMA

            def table_ref(self, table: str) -> TableReference:
                """Create a fully qualified table reference.

                Args:
                    table: Table name (can be 1, 2, or 3 parts)

                Returns:
                    TableReference with all three parts
                """
                parts = table.split(".")
                if len(parts) == 3:
                    return TableReference(parts[0], parts[1], parts[2])
                elif len(parts) == 2:
                    return TableReference(self.catalog, parts[0], parts[1])
                else:
                    return TableReference(self.catalog, self.schema, table)

            def read_table(self, table: str) -> DataFrame:
                """Read a table with proper namespace and error handling.

                Args:
                    table: Table name (1, 2, or 3 parts)

                Returns:
                    DataFrame with table contents

                Raises:
                    PermissionError: If access is denied
                    ValueError: If table doesn't exist
                """
                ref = self.table_ref(table)
                try:
                    return self.spark.table(ref.full_path)
                except AnalysisException as e:
                    error_msg = str(e).upper()
                    if "PERMISSION" in error_msg or "ACCESS" in error_msg:
                        raise PermissionError(
                            f"Access denied to {{ref.full_path}}. "
                            "Request access via Unity Catalog."
                        ) from e
                    if "NOT_FOUND" in error_msg or "does not exist" in str(e):
                        raise ValueError(
                            f"Table {{ref.full_path}} does not exist"
                        ) from e
                    raise

            def table_exists(self, table: str) -> bool:
                """Check if a table exists and is accessible.

                Args:
                    table: Table name

                Returns:
                    True if table exists and user has access
                """
                ref = self.table_ref(table)
                try:
                    self.spark.sql(f"DESCRIBE TABLE {{ref.full_path}}")
                    return True
                except AnalysisException:
                    return False

            def list_tables(self, schema: Optional[str] = None) -> list[str]:
                """List all accessible tables in a schema.

                Args:
                    schema: Override default schema

                Returns:
                    List of table names
                """
                schema = schema or self.schema
                result = self.spark.sql(f"SHOW TABLES IN {{self.catalog}}.{{schema}}")
                return [row.tableName for row in result.collect()]

            def list_schemas(self, catalog: Optional[str] = None) -> list[str]:
                """List all accessible schemas in a catalog.

                Args:
                    catalog: Override default catalog

                Returns:
                    List of schema names
                """
                catalog = catalog or self.catalog
                result = self.spark.sql(f"SHOW SCHEMAS IN {{catalog}}")
                return [row.databaseName for row in result.collect()]

            def describe_table(self, table: str) -> DataFrame:
                """Get table metadata.

                Args:
                    table: Table name

                Returns:
                    DataFrame with column metadata
                """
                ref = self.table_ref(table)
                return self.spark.sql(f"DESCRIBE TABLE {{ref.full_path}}")
    ''').strip()

    if include_tests:
        code += dedent('''


        # =============================================================================
        # TEST STUBS
        # =============================================================================

        def test_table_ref_parsing():
            """Test table reference parsing."""
            from unittest.mock import MagicMock

            spark = MagicMock()
            client = UnityCatalogClient(spark)

            # One-part reference
            ref = client.table_ref("users")
            assert ref.catalog == client.DEFAULT_CATALOG
            assert ref.schema == client.DEFAULT_SCHEMA
            assert ref.table == "users"

            # Two-part reference
            ref = client.table_ref("analytics.events")
            assert ref.catalog == client.DEFAULT_CATALOG
            assert ref.schema == "analytics"
            assert ref.table == "events"

            # Three-part reference
            ref = client.table_ref("prod.analytics.events")
            assert ref.catalog == "prod"
            assert ref.schema == "analytics"
            assert ref.table == "events"


        def test_permission_error_handling():
            """Test permission error is properly raised."""
            from unittest.mock import MagicMock, patch

            spark = MagicMock()
            client = UnityCatalogClient(spark)

            # Mock AnalysisException for permission error
            spark.table.side_effect = AnalysisException("PERMISSION_DENIED: ...")

            try:
                client.read_table("protected_table")
                assert False, "Should have raised PermissionError"
            except PermissionError as e:
                assert "Access denied" in str(e)
        ''')

    return code


def generate_mcp_client(
    workspace_url: str,
    genie_space_id: Optional[str] = None,
    async_mode: bool = True,
) -> str:
    """Generate an MCP client wrapper.

    Args:
        workspace_url: Databricks workspace URL
        genie_space_id: Optional Genie space ID
        async_mode: Generate async code

    Returns:
        Generated Python code
    """
    async_prefix = "async " if async_mode else ""
    await_prefix = "await " if async_mode else ""

    code = dedent(f'''
        """Databricks MCP Client for {workspace_url}.

        Auto-generated using Databricks pattern templates.
        Supports SQL, Genie, Vector Search, and UC Functions.
        """
        from dataclasses import dataclass
        from typing import Any, Optional
        import os
        import logging

        import httpx

        logger = logging.getLogger(__name__)


        @dataclass
        class MCPConfig:
            """MCP connection configuration."""

            workspace_url: str
            token: str
            catalog: str = "main"
            schema: str = "default"
            genie_space_id: Optional[str] = None

            @classmethod
            def from_env(cls) -> "MCPConfig":
                """Load configuration from environment variables."""
                return cls(
                    workspace_url=os.environ["DATABRICKS_HOST"],
                    token=os.environ["DATABRICKS_TOKEN"],
                    catalog=os.environ.get("DATABRICKS_CATALOG", "main"),
                    schema=os.environ.get("DATABRICKS_SCHEMA", "default"),
                    genie_space_id=os.environ.get("DATABRICKS_GENIE_SPACE_ID"),
                )

            @property
            def sql_url(self) -> str:
                """DBSQL MCP server URL."""
                return f"{{self.workspace_url}}/api/2.0/mcp/sql"

            @property
            def genie_url(self) -> str:
                """Genie MCP server URL."""
                if not self.genie_space_id:
                    raise ValueError("Genie space ID not configured")
                return f"{{self.workspace_url}}/api/2.0/mcp/genie/{{self.genie_space_id}}"

            @property
            def vector_search_url(self) -> str:
                """Vector Search MCP server URL."""
                return (
                    f"{{self.workspace_url}}/api/2.0/mcp/vector-search/"
                    f"{{self.catalog}}/{{self.schema}}"
                )

            @property
            def functions_url(self) -> str:
                """UC Functions MCP server URL."""
                return (
                    f"{{self.workspace_url}}/api/2.0/mcp/functions/"
                    f"{{self.catalog}}/{{self.schema}}"
                )


        class DatabricksMCPClient:
            """Unified client for all Databricks MCP servers.

            Features:
            - SQL execution (read-only and read-write)
            - Genie natural language queries
            - Vector search for RAG
            - Unity Catalog function execution
            """

            def __init__(self, config: Optional[MCPConfig] = None):
                """Initialize MCP client.

                Args:
                    config: Optional config (uses env vars if not provided)
                """
                self.config = config or MCPConfig.from_env()
                self._client = httpx.{"Async" if async_mode else ""}Client(
                    headers={{
                        "Authorization": f"Bearer {{self.config.token}}",
                        "Content-Type": "application/json",
                    }},
                    timeout=60.0,
                )

            {async_prefix}def execute_sql(
                self,
                sql: str,
                warehouse_id: Optional[str] = None,
                read_only: bool = False,
            ) -> dict[str, Any]:
                """Execute SQL via DBSQL MCP server.

                Args:
                    sql: SQL statement to execute
                    warehouse_id: Target warehouse ID
                    read_only: Use read-only mode

                Returns:
                    Query results as dictionary
                """
                endpoint = "execute_sql_read_only" if read_only else "execute_sql"
                payload = {{"statement": sql}}
                if warehouse_id:
                    payload["warehouse_id"] = warehouse_id

                response = {await_prefix}self._client.post(
                    f"{{self.config.sql_url}}/{{endpoint}}",
                    json=payload,
                )
                response.raise_for_status()
                return response.json()

            {async_prefix}def genie_query(self, question: str) -> dict[str, Any]:
                """Query data using natural language via Genie.

                Args:
                    question: Natural language question

                Returns:
                    Query results

                Note:
                    Genie MCP doesn't maintain conversation history.
                    For multi-turn conversations, use in a multi-agent system.
                """
                response = {await_prefix}self._client.post(
                    f"{{self.config.genie_url}}/query",
                    json={{"question": question}},
                )
                response.raise_for_status()
                return response.json()

            {async_prefix}def vector_search(
                self,
                query_text: str,
                index_name: str,
                num_results: int = 10,
            ) -> list[dict[str, Any]]:
                """Search vector index for similar documents.

                Args:
                    query_text: Text to search for
                    index_name: Vector index name
                    num_results: Number of results to return

                Returns:
                    List of similar documents

                Note:
                    Only supports Databricks-managed embeddings.
                """
                response = {await_prefix}self._client.post(
                    f"{{self.config.vector_search_url}}/query",
                    json={{
                        "index_name": index_name,
                        "query_text": query_text,
                        "num_results": num_results,
                    }},
                )
                response.raise_for_status()
                return response.json().get("results", [])

            {async_prefix}def call_function(
                self,
                function_name: str,
                parameters: dict[str, Any],
            ) -> dict[str, Any]:
                """Execute a Unity Catalog function.

                Args:
                    function_name: Function name (schema.function_name)
                    parameters: Function parameters

                Returns:
                    Function result
                """
                response = {await_prefix}self._client.post(
                    f"{{self.config.functions_url}}/execute",
                    json={{
                        "function_name": function_name,
                        "parameters": parameters,
                    }},
                )
                response.raise_for_status()
                return response.json()

            {async_prefix}def close(self):
                """Close the HTTP client."""
                {await_prefix}self._client.aclose()

            {async_prefix}def __aenter__(self):
                return self

            {async_prefix}def __aexit__(self, *args):
                {await_prefix}self.close()
    ''').strip()

    return code


def generate_safe_sql_executor(include_retry: bool = True) -> str:
    """Generate a safe SQL executor with injection prevention.

    Args:
        include_retry: Include retry logic for transient failures

    Returns:
        Generated Python code
    """
    retry_decorator = dedent('''
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=2, max=30),
            retry=retry_if_exception_type(OperationalError),
        )
    ''').strip() if include_retry else ""

    retry_import = (
        "from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type"
        if include_retry else ""
    )

    code = dedent(f'''
        """Safe SQL Executor with Injection Prevention.

        Auto-generated using Databricks pattern templates.
        Features parameterized queries, input validation, and retry logic.
        """
        from dataclasses import dataclass
        from typing import Any, Optional
        import re
        import os
        import logging

        from databricks import sql
        from databricks.sql.exc import DatabaseError, OperationalError, ProgrammingError
        {retry_import}

        logger = logging.getLogger(__name__)


        # SQL keywords that indicate dangerous operations
        DANGEROUS_KEYWORDS = frozenset([
            "DROP", "TRUNCATE", "DELETE", "UPDATE", "INSERT",
            "CREATE", "ALTER", "GRANT", "REVOKE"
        ])

        # Valid identifier pattern (table names, column names)
        IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


        @dataclass
        class SQLConfig:
            """SQL connection configuration."""

            server_hostname: str
            http_path: str
            access_token: str
            catalog: str = "main"
            schema: str = "default"

            @classmethod
            def from_env(cls) -> "SQLConfig":
                """Load from environment variables."""
                return cls(
                    server_hostname=os.environ["DATABRICKS_HOST"].replace("https://", ""),
                    http_path=os.environ["DATABRICKS_HTTP_PATH"],
                    access_token=os.environ["DATABRICKS_TOKEN"],
                    catalog=os.environ.get("DATABRICKS_CATALOG", "main"),
                    schema=os.environ.get("DATABRICKS_SCHEMA", "default"),
                )


        class SafeSQLExecutor:
            """SQL executor with injection prevention and safety checks.

            Security features:
            - Parameterized queries (prevents SQL injection)
            - Identifier validation (allowlist approach)
            - Read-only mode enforcement
            - Dangerous operation detection
            """

            def __init__(self, config: Optional[SQLConfig] = None):
                """Initialize executor.

                Args:
                    config: SQL config (uses env vars if not provided)
                """
                self.config = config or SQLConfig.from_env()

            def validate_identifier(self, name: str) -> str:
                """Validate an identifier (table/column name).

                Args:
                    name: Identifier to validate

                Returns:
                    Validated identifier

                Raises:
                    ValueError: If identifier is invalid
                """
                if not IDENTIFIER_PATTERN.match(name):
                    raise ValueError(
                        f"Invalid identifier: {{name}}. "
                        "Only alphanumeric characters and underscores allowed, "
                        "must start with letter or underscore."
                    )
                return name

            def _get_connection(self):
                """Get database connection."""
                return sql.connect(
                    server_hostname=self.config.server_hostname,
                    http_path=self.config.http_path,
                    access_token=self.config.access_token,
                    catalog=self.config.catalog,
                    schema=self.config.schema,
                )

            def _is_read_only(self, query: str) -> bool:
                """Check if query is read-only."""
                query_upper = query.strip().upper()
                # Must start with SELECT, WITH, SHOW, DESCRIBE, or EXPLAIN
                if not any(query_upper.startswith(kw) for kw in
                          ["SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN"]):
                    return False
                # Cannot contain dangerous keywords
                words = set(re.findall(r"\\b[A-Z]+\\b", query_upper))
                return not bool(words & DANGEROUS_KEYWORDS)

            {retry_decorator}
            def execute(
                self,
                query: str,
                params: Optional[dict[str, Any]] = None,
            ) -> list[dict[str, Any]]:
                """Execute a parameterized query.

                Args:
                    query: SQL with :param placeholders
                    params: Parameter values

                Returns:
                    List of result rows as dictionaries

                Example:
                    results = executor.execute(
                        "SELECT * FROM users WHERE id = :user_id",
                        {{"user_id": 123}}
                    )
                """
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params or {{}})
                        if cursor.description:
                            columns = [desc[0] for desc in cursor.description]
                            return [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return []

            def execute_read_only(
                self,
                query: str,
                params: Optional[dict[str, Any]] = None,
            ) -> list[dict[str, Any]]:
                """Execute a read-only query with enforcement.

                Args:
                    query: Read-only SQL query
                    params: Parameter values

                Returns:
                    Query results

                Raises:
                    ValueError: If query is not read-only
                """
                if not self._is_read_only(query):
                    raise ValueError(
                        "Query is not read-only. Use execute() for write operations."
                    )
                return self.execute(query, params)

            def select_from_table(
                self,
                table: str,
                columns: Optional[list[str]] = None,
                where: Optional[dict[str, Any]] = None,
                limit: int = 1000,
            ) -> list[dict[str, Any]]:
                """Safe SELECT with validated identifiers.

                Args:
                    table: Table name (validated)
                    columns: Column names (validated), None for all
                    where: WHERE conditions (values parameterized)
                    limit: Row limit (default 1000)

                Returns:
                    Query results
                """
                # Validate table name
                safe_table = self.validate_identifier(table)

                # Build column list
                if columns:
                    safe_columns = [self.validate_identifier(c) for c in columns]
                    column_str = ", ".join(safe_columns)
                else:
                    column_str = "*"

                # Build query
                query = f"SELECT {{column_str}} FROM {{safe_table}}"

                # Add WHERE clause with parameters
                params = {{}}
                if where:
                    conditions = []
                    for col, value in where.items():
                        safe_col = self.validate_identifier(col)
                        param_name = f"p_{{safe_col}}"
                        conditions.append(f"{{safe_col}} = :{{param_name}}")
                        params[param_name] = value
                    query += " WHERE " + " AND ".join(conditions)

                # Always add LIMIT for safety
                query += f" LIMIT {{int(limit)}}"

                return self.execute(query, params)
    ''').strip()

    return code


def generate_claude_code_mcp_config(
    workspace_url: str,
    genie_space_id: Optional[str] = None,
) -> str:
    """Generate Claude Code MCP configuration.

    Args:
        workspace_url: Databricks workspace URL
        genie_space_id: Optional Genie space ID

    Returns:
        JSON configuration as string
    """
    genie_config = ""
    if genie_space_id:
        genie_config = f'''
    "databricks-genie": {{
      "command": "npx",
      "args": ["databricks-mcp-server", "--mode", "genie"],
      "env": {{
        "DATABRICKS_HOST": "${{DATABRICKS_HOST}}",
        "DATABRICKS_TOKEN": "${{DATABRICKS_TOKEN}}",
        "GENIE_SPACE_ID": "{genie_space_id}"
      }}
    }},'''

    return dedent(f'''
        {{
          "mcpServers": {{
            "databricks-sql": {{
              "command": "npx",
              "args": ["databricks-mcp-server", "--mode", "sql"],
              "env": {{
                "DATABRICKS_HOST": "${{DATABRICKS_HOST}}",
                "DATABRICKS_TOKEN": "${{DATABRICKS_TOKEN}}"
              }}
            }},{genie_config}
            "databricks-vector-search": {{
              "command": "npx",
              "args": ["databricks-mcp-server", "--mode", "vector-search"],
              "env": {{
                "DATABRICKS_HOST": "${{DATABRICKS_HOST}}",
                "DATABRICKS_TOKEN": "${{DATABRICKS_TOKEN}}",
                "CATALOG": "${{DATABRICKS_CATALOG}}",
                "SCHEMA": "${{DATABRICKS_SCHEMA}}"
              }}
            }},
            "databricks-uc-functions": {{
              "command": "npx",
              "args": ["databricks-mcp-server", "--mode", "functions"],
              "env": {{
                "DATABRICKS_HOST": "${{DATABRICKS_HOST}}",
                "DATABRICKS_TOKEN": "${{DATABRICKS_TOKEN}}",
                "CATALOG": "${{DATABRICKS_CATALOG}}",
                "SCHEMA": "${{DATABRICKS_SCHEMA}}"
              }}
            }}
          }}
        }}
    ''').strip()


if __name__ == "__main__":
    # Example usage
    print("=== Unity Catalog Client ===")
    print(generate_unity_catalog_client("production", "analytics")[:500])
    print("\n...")

    print("\n=== MCP Client (async) ===")
    print(generate_mcp_client("https://workspace.cloud.databricks.com")[:500])
    print("\n...")

    print("\n=== Claude Code MCP Config ===")
    print(generate_claude_code_mcp_config(
        "https://workspace.cloud.databricks.com",
        "genie-space-123"
    ))

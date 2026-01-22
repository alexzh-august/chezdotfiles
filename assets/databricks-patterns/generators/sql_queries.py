"""
SQL Query Generator

Generate properly structured SQL queries following Databricks best practices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class SQLQueryGenerator:
    """
    Generate SQL queries following Databricks patterns.

    All queries use:
    - Fully qualified table names (catalog.schema.table)
    - Parameterized values where applicable
    - Appropriate LIMIT clauses
    """

    catalog: str
    schema: str

    def _fqn(self, table: str) -> str:
        """Get fully qualified name for a table."""
        if "." in table:
            return table
        return f"{self.catalog}.{self.schema}.{table}"

    def select(
        self,
        table: str,
        columns: list[str] | None = None,
        *,
        where: str | None = None,
        order_by: str | None = None,
        limit: int = 100,
    ) -> str:
        """
        Generate a SELECT query.

        Args:
            table: Table name (will be fully qualified).
            columns: List of columns (default: all).
            where: WHERE clause condition.
            order_by: ORDER BY clause.
            limit: Row limit (default: 100).
        """
        cols = ", ".join(columns) if columns else "*"
        fqn = self._fqn(table)

        query = f"SELECT {cols}\nFROM {fqn}"

        if where:
            query += f"\nWHERE {where}"
        if order_by:
            query += f"\nORDER BY {order_by}"
        if limit:
            query += f"\nLIMIT {limit}"

        return query

    def select_parameterized(
        self,
        table: str,
        columns: list[str],
        params: dict[str, str],  # column -> param_name
        *,
        limit: int = 100,
    ) -> tuple[str, str]:
        """
        Generate a parameterized SELECT query.

        Returns tuple of (query, usage_example).
        """
        fqn = self._fqn(table)
        cols = ", ".join(columns)

        conditions = [f"{col} = :{param}" for col, param in params.items()]
        where = " AND ".join(conditions)

        query = f"""\
SELECT {cols}
FROM {fqn}
WHERE {where}
LIMIT {limit}"""

        # Generate usage example
        example_params = {param: f"<{param}_value>" for param in params.values()}
        usage = f"""\
# Usage:
# execute_sql(query, params={example_params})"""

        return query, usage

    def insert(
        self,
        table: str,
        columns: list[str],
    ) -> tuple[str, str]:
        """
        Generate an INSERT query with parameters.

        Returns tuple of (query, usage_example).
        """
        fqn = self._fqn(table)
        cols = ", ".join(columns)
        params = ", ".join(f":{col}" for col in columns)

        query = f"""\
INSERT INTO {fqn}
({cols})
VALUES ({params})"""

        example_params = {col: f"<{col}_value>" for col in columns}
        usage = f"""\
# Usage:
# execute_sql(query, params={example_params})"""

        return query, usage

    def update(
        self,
        table: str,
        set_columns: list[str],
        key_columns: list[str],
    ) -> tuple[str, str]:
        """
        Generate an UPDATE query with parameters.

        Returns tuple of (query, usage_example).
        """
        fqn = self._fqn(table)
        set_clause = ", ".join(f"{col} = :{col}" for col in set_columns)
        where_clause = " AND ".join(f"{col} = :{col}" for col in key_columns)

        query = f"""\
UPDATE {fqn}
SET {set_clause}
WHERE {where_clause}"""

        all_cols = set_columns + key_columns
        example_params = {col: f"<{col}_value>" for col in all_cols}
        usage = f"""\
# Usage:
# execute_sql(query, params={example_params})"""

        return query, usage

    def merge(
        self,
        target_table: str,
        source_table: str,
        match_columns: list[str],
        update_columns: list[str],
        insert_columns: list[str] | None = None,
    ) -> str:
        """
        Generate a MERGE (upsert) query.

        Delta Lake MERGE syntax.
        """
        target_fqn = self._fqn(target_table)
        source_fqn = self._fqn(source_table)

        match_condition = " AND ".join(
            f"target.{col} = source.{col}" for col in match_columns
        )

        update_set = ",\n        ".join(
            f"target.{col} = source.{col}" for col in update_columns
        )

        insert_cols = insert_columns or (match_columns + update_columns)
        insert_columns_str = ", ".join(insert_cols)
        insert_values_str = ", ".join(f"source.{col}" for col in insert_cols)

        return f"""\
MERGE INTO {target_fqn} AS target
USING {source_fqn} AS source
ON {match_condition}
WHEN MATCHED THEN
    UPDATE SET
        {update_set}
WHEN NOT MATCHED THEN
    INSERT ({insert_columns_str})
    VALUES ({insert_values_str})"""

    def validation_query(
        self,
        table: str,
        validation_rules: dict[str, str],  # name -> condition
    ) -> str:
        """
        Generate a data validation query.

        Returns count of rows failing each validation rule.
        """
        fqn = self._fqn(table)

        case_statements = []
        for name, condition in validation_rules.items():
            case_statements.append(
                f"SUM(CASE WHEN NOT ({condition}) THEN 1 ELSE 0 END) AS {name}_failures"
            )

        cases = ",\n    ".join(case_statements)

        return f"""\
SELECT
    COUNT(*) AS total_rows,
    {cases}
FROM {fqn}"""

    def describe_table(self, table: str) -> str:
        """Generate DESCRIBE TABLE query."""
        return f"DESCRIBE TABLE {self._fqn(table)}"

    def show_tables(self) -> str:
        """Generate SHOW TABLES query for current schema."""
        return f"SHOW TABLES IN {self.catalog}.{self.schema}"

    def show_schemas(self) -> str:
        """Generate SHOW SCHEMAS query for current catalog."""
        return f"SHOW SCHEMAS IN {self.catalog}"

    def chunked_select(
        self,
        table: str,
        columns: list[str],
        order_column: str,
        chunk_size: int = 1000,
    ) -> str:
        """
        Generate a template for chunked/paginated retrieval.

        Returns SQL with :offset parameter.
        """
        fqn = self._fqn(table)
        cols = ", ".join(columns)

        return f"""\
-- Chunked retrieval pattern
-- Execute with params={{"offset": 0}}, then {{"offset": {chunk_size}}}, etc.
SELECT {cols}
FROM {fqn}
ORDER BY {order_column}
LIMIT {chunk_size}
OFFSET :offset"""


@dataclass
class CatalogDiscoveryQueries:
    """Pre-built queries for Unity Catalog discovery."""

    @staticmethod
    def list_catalogs() -> str:
        return "SHOW CATALOGS"

    @staticmethod
    def list_schemas(catalog: str) -> str:
        return f"SHOW SCHEMAS IN {catalog}"

    @staticmethod
    def list_tables(catalog: str, schema: str) -> str:
        return f"SHOW TABLES IN {catalog}.{schema}"

    @staticmethod
    def describe_table(catalog: str, schema: str, table: str) -> str:
        return f"DESCRIBE TABLE {catalog}.{schema}.{table}"

    @staticmethod
    def table_history(catalog: str, schema: str, table: str) -> str:
        """Delta Lake table history."""
        return f"DESCRIBE HISTORY {catalog}.{schema}.{table}"

    @staticmethod
    def table_detail(catalog: str, schema: str, table: str) -> str:
        """Delta Lake table details."""
        return f"DESCRIBE DETAIL {catalog}.{schema}.{table}"

"""
SQL Refactoring Utilities

Transform SQL queries to follow best practices.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SQLRefactor:
    """
    Refactor SQL queries to follow Databricks best practices.

    Transformations:
    - Add LIMIT clauses
    - Replace SELECT * with column lists
    - Add fully qualified table names
    - Convert string concatenation to parameterized queries
    """

    default_catalog: str
    default_schema: str
    default_limit: int = 100

    def refactor(self, sql: str) -> tuple[str, list[str]]:
        """
        Refactor a SQL query.

        Returns:
            Tuple of (refactored_sql, list_of_changes).
        """
        changes: list[str] = []
        result = sql

        # Apply transformations in order
        result, change = self._add_limit_clause(result)
        if change:
            changes.append(change)

        result, change = self._qualify_table_names(result)
        if change:
            changes.append(change)

        result, fstring_changes = self._detect_string_concat(result)
        changes.extend(fstring_changes)

        return result, changes

    def _add_limit_clause(self, sql: str) -> tuple[str, str | None]:
        """Add LIMIT clause if missing from SELECT queries."""
        # Check if it's a SELECT without LIMIT
        is_select = re.search(r"\bSELECT\b", sql, re.IGNORECASE)
        has_limit = re.search(r"\bLIMIT\s+\d+", sql, re.IGNORECASE)
        is_subquery = sql.strip().startswith("(")

        if is_select and not has_limit and not is_subquery:
            # Add LIMIT before any trailing semicolon or whitespace
            sql = re.sub(r"(\s*;?\s*)$", f"\nLIMIT {self.default_limit}\\1", sql)
            return sql, f"Added LIMIT {self.default_limit} clause"

        return sql, None

    def _qualify_table_names(self, sql: str) -> tuple[str, str | None]:
        """Add catalog.schema prefix to unqualified table names."""
        changes_made = []

        # Pattern to find table references after FROM, JOIN, INTO, UPDATE
        pattern = r"(\b(?:FROM|JOIN|INTO|UPDATE)\s+)([a-zA-Z_][a-zA-Z0-9_]*)(\s|$|,|\))"

        def replace_table(match: re.Match) -> str:
            keyword = match.group(1)
            table = match.group(2)
            suffix = match.group(3)

            # Skip if already qualified (has dots) or is a keyword
            if "." in table or table.upper() in {
                "SELECT",
                "WHERE",
                "SET",
                "VALUES",
                "ON",
                "AND",
                "OR",
            }:
                return match.group(0)

            qualified = f"{self.default_catalog}.{self.default_schema}.{table}"
            changes_made.append(f"Qualified {table} -> {qualified}")
            return f"{keyword}{qualified}{suffix}"

        result = re.sub(pattern, replace_table, sql, flags=re.IGNORECASE)

        if changes_made:
            return result, "; ".join(changes_made)
        return sql, None

    def _detect_string_concat(self, sql: str) -> tuple[str, list[str]]:
        """Detect and warn about string concatenation patterns."""
        warnings = []

        # Check for f-string patterns (in Python code containing SQL)
        if re.search(r'f["\'].*\{.*\}.*(?:SELECT|FROM|WHERE)', sql, re.IGNORECASE):
            warnings.append(
                "WARNING: Detected f-string SQL. Convert to parameterized query"
            )

        # Check for string concatenation
        if re.search(r'["\'].*\+.*(?:SELECT|FROM|WHERE)', sql, re.IGNORECASE):
            warnings.append(
                "WARNING: Detected string concatenation in SQL. Use parameterized queries"
            )

        # Check for % formatting
        if re.search(r'%s|%\(.*\)s', sql):
            warnings.append(
                "WARNING: Detected % formatting in SQL. Use :param style instead"
            )

        return sql, warnings

    def convert_to_parameterized(
        self,
        sql: str,
        variables: dict[str, str],  # variable_name -> param_name
    ) -> tuple[str, dict[str, str]]:
        """
        Convert f-string or concatenated SQL to parameterized query.

        Args:
            sql: Original SQL with embedded variables.
            variables: Mapping of variable names to parameter names.

        Returns:
            Tuple of (parameterized_sql, params_example).

        Example:
            sql = 'SELECT * FROM t WHERE id = {user_id}'
            variables = {'user_id': 'id'}
            -> ('SELECT * FROM t WHERE id = :id', {'id': 'user_id_value'})
        """
        result = sql
        params = {}

        for var_name, param_name in variables.items():
            # Replace {variable} with :param
            result = re.sub(
                rf"\{{{var_name}\}}",
                f":{param_name}",
                result,
            )
            params[param_name] = f"<{var_name}_value>"

            # Replace variable in string concatenation
            result = re.sub(
                rf'"\s*\+\s*{var_name}\s*\+\s*"',
                f":{param_name}",
                result,
            )

        return result, params

    def add_column_list(
        self,
        sql: str,
        columns: list[str],
    ) -> str:
        """Replace SELECT * with specific column list."""
        column_str = ", ".join(columns)
        return re.sub(
            r"\bSELECT\s+\*\s+FROM",
            f"SELECT {column_str}\nFROM",
            sql,
            flags=re.IGNORECASE,
        )


@dataclass
class SQLPatternUpgrader:
    """
    Upgrade SQL patterns to modern Databricks SQL.

    Handles:
    - Legacy syntax updates
    - Delta Lake specific optimizations
    - Spark SQL to Databricks SQL migrations
    """

    @staticmethod
    def upgrade_timestamp_functions(sql: str) -> str:
        """Upgrade deprecated timestamp functions."""
        replacements = [
            (r"\bCURRENT_TIMESTAMP\(\)", "CURRENT_TIMESTAMP()"),
            (r"\bNOW\(\)", "CURRENT_TIMESTAMP()"),
            (r"\bUNIX_TIMESTAMP\(\)", "UNIX_TIMESTAMP(CURRENT_TIMESTAMP())"),
            (r"\bFROM_UNIXTIME\(", "FROM_UNIXTIME("),
        ]

        result = sql
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result

    @staticmethod
    def add_delta_hints(sql: str, table: str) -> str:
        """Add Delta Lake specific hints for optimization."""
        # Add ZORDER hint for common filter columns
        if "WHERE" in sql.upper() and "ORDER BY" not in sql.upper():
            # This is a simplified example
            pass

        return sql

    @staticmethod
    def convert_insert_overwrite_to_merge(
        insert_sql: str,
        target_table: str,
        source_table: str,
        key_columns: list[str],
    ) -> str:
        """Convert INSERT OVERWRITE pattern to MERGE for better performance."""
        key_conditions = " AND ".join(
            f"target.{col} = source.{col}" for col in key_columns
        )

        # Extract columns from INSERT (simplified)
        col_match = re.search(
            r"INSERT\s+(?:OVERWRITE|INTO)\s+\S+\s*\(([^)]+)\)",
            insert_sql,
            re.IGNORECASE,
        )

        if col_match:
            columns = [c.strip() for c in col_match.group(1).split(",")]
            update_set = ", ".join(f"target.{c} = source.{c}" for c in columns)
            insert_cols = ", ".join(columns)
            insert_vals = ", ".join(f"source.{c}" for c in columns)

            return f"""\
MERGE INTO {target_table} AS target
USING {source_table} AS source
ON {key_conditions}
WHEN MATCHED THEN
    UPDATE SET {update_set}
WHEN NOT MATCHED THEN
    INSERT ({insert_cols})
    VALUES ({insert_vals})"""

        return insert_sql

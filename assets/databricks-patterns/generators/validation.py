"""
Data Validation Generator

Generate data validation code and queries for Databricks.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationRule:
    """A single validation rule."""

    name: str
    condition: str
    error_message: str
    severity: str = "error"  # "error", "warning"


@dataclass
class ValidationGenerator:
    """
    Generate data validation code and queries.

    Supports:
    - SQL-based validation
    - Python validation functions
    - Pre-merge validation patterns
    """

    catalog: str
    schema: str

    def _fqn(self, table: str) -> str:
        """Get fully qualified table name."""
        return f"{self.catalog}.{self.schema}.{table}"

    def validation_query(
        self,
        table: str,
        rules: list[ValidationRule],
    ) -> str:
        """
        Generate a SQL validation query.

        Returns a query that counts failures for each rule.
        """
        fqn = self._fqn(table)

        case_statements = []
        for rule in rules:
            case_statements.append(
                f"    SUM(CASE WHEN NOT ({rule.condition}) THEN 1 ELSE 0 END) AS {rule.name}_failures"
            )

        cases = ",\n".join(case_statements)

        return f"""\
-- Data validation query for {fqn}
SELECT
    COUNT(*) AS total_rows,
{cases}
FROM {fqn}"""

    def validation_with_details(
        self,
        table: str,
        rules: list[ValidationRule],
        key_columns: list[str],
        *,
        limit: int = 100,
    ) -> str:
        """
        Generate a query that returns rows failing validation.

        Includes key columns to identify problematic records.
        """
        fqn = self._fqn(table)
        keys = ", ".join(key_columns)

        conditions = []
        for rule in rules:
            conditions.append(f"NOT ({rule.condition})")

        combined_condition = " OR ".join(conditions)

        validation_cases = []
        for rule in rules:
            validation_cases.append(
                f"    CASE WHEN NOT ({rule.condition}) THEN '{rule.name}' END"
            )

        validation_array = ",\n".join(validation_cases)

        return f"""\
-- Get rows failing validation with details
SELECT
    {keys},
    ARRAY_COMPACT(ARRAY(
{validation_array}
    )) AS failed_validations
FROM {fqn}
WHERE {combined_condition}
LIMIT {limit}"""

    def python_validator(
        self,
        table: str,
        rules: list[ValidationRule],
    ) -> str:
        """
        Generate Python validation code.

        Returns a complete validation function.
        """
        fqn = self._fqn(table)

        rule_defs = []
        for rule in rules:
            rule_defs.append(
                f'        ValidationRule("{rule.name}", "{rule.condition}", "{rule.error_message}", "{rule.severity}"),'
            )

        rules_str = "\n".join(rule_defs)

        return f'''\
"""Data validation for {fqn}."""

from dataclasses import dataclass
from databricks.sdk import WorkspaceClient


@dataclass
class ValidationRule:
    """A validation rule definition."""
    name: str
    condition: str
    error_message: str
    severity: str = "error"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    total_rows: int
    failures: dict[str, int]  # rule_name -> failure_count
    error_rules: list[str]    # rules with severity=error that failed


def validate_{table}(client: WorkspaceClient | None = None) -> ValidationResult:
    """
    Validate data in {fqn}.

    Returns:
        ValidationResult with pass/fail status and failure counts.

    Raises:
        RuntimeError: If validation query fails.
    """
    if client is None:
        client = WorkspaceClient()

    rules = [
{rules_str}
    ]

    # Build validation query
    case_statements = [
        f"SUM(CASE WHEN NOT ({{r.condition}}) THEN 1 ELSE 0 END) AS {{r.name}}_failures"
        for r in rules
    ]

    query = f"""
        SELECT
            COUNT(*) AS total_rows,
            {{", ".join(case_statements)}}
        FROM {fqn}
    """

    # Execute query
    result = client.statement_execution.execute_statement(
        statement=query,
        wait_timeout="60s",
    )

    if result.status.state.value != "SUCCEEDED":
        raise RuntimeError(f"Validation query failed: {{result.status}}")

    # Parse results
    row = result.result.data_array[0] if result.result.data_array else []
    total_rows = int(row[0]) if row else 0

    failures = {{}}
    error_rules = []
    for i, rule in enumerate(rules, start=1):
        failure_count = int(row[i]) if len(row) > i else 0
        failures[rule.name] = failure_count

        if failure_count > 0 and rule.severity == "error":
            error_rules.append(rule.name)

    passed = len(error_rules) == 0

    return ValidationResult(
        passed=passed,
        total_rows=total_rows,
        failures=failures,
        error_rules=error_rules,
    )
'''

    def pre_merge_validator(
        self,
        target_table: str,
        source_table: str,
        rules: list[ValidationRule],
    ) -> str:
        """
        Generate pre-merge validation code.

        Validates source data before merging into target.
        """
        source_fqn = self._fqn(source_table)
        target_fqn = self._fqn(target_table)

        rule_defs = []
        for rule in rules:
            rule_defs.append(
                f'    ValidationRule("{rule.name}", "{rule.condition}", "{rule.error_message}"),'
            )

        rules_str = "\n".join(rule_defs)

        return f'''\
"""Pre-merge validation for {source_fqn} -> {target_fqn}."""

from dataclasses import dataclass
from databricks.sdk import WorkspaceClient


@dataclass
class ValidationRule:
    name: str
    condition: str
    error_message: str


class MergeValidationError(Exception):
    """Raised when pre-merge validation fails."""
    pass


def validate_before_merge(client: WorkspaceClient | None = None) -> None:
    """
    Validate source data before merging.

    Raises:
        MergeValidationError: If validation fails.
    """
    if client is None:
        client = WorkspaceClient()

    rules = [
{rules_str}
    ]

    # Build validation query against source
    case_statements = [
        f"SUM(CASE WHEN NOT ({{r.condition}}) THEN 1 ELSE 0 END) AS {{r.name}}_failures"
        for r in rules
    ]

    query = f"""
        SELECT
            COUNT(*) AS total_rows,
            {{", ".join(case_statements)}}
        FROM {source_fqn}
    """

    result = client.statement_execution.execute_statement(
        statement=query,
        wait_timeout="60s",
    )

    if result.status.state.value != "SUCCEEDED":
        raise RuntimeError(f"Validation query failed: {{result.status}}")

    row = result.result.data_array[0] if result.result.data_array else []

    # Check for failures
    failed_rules = []
    for i, rule in enumerate(rules, start=1):
        failure_count = int(row[i]) if len(row) > i else 0
        if failure_count > 0:
            failed_rules.append(f"{{rule.name}}: {{failure_count}} failures ({{rule.error_message}})")

    if failed_rules:
        raise MergeValidationError(
            f"Pre-merge validation failed:\\n" + "\\n".join(failed_rules)
        )


def validated_merge(
    client: WorkspaceClient | None = None,
    merge_query: str | None = None,
) -> None:
    """
    Run validation then execute merge if passed.

    Args:
        client: Databricks client.
        merge_query: Custom merge query (optional).
    """
    if client is None:
        client = WorkspaceClient()

    # Validate first
    validate_before_merge(client)

    # Execute merge
    if merge_query is None:
        raise ValueError("merge_query must be provided")

    result = client.statement_execution.execute_statement(
        statement=merge_query,
        wait_timeout="300s",
    )

    if result.status.state.value != "SUCCEEDED":
        raise RuntimeError(f"Merge failed: {{result.status}}")
'''


# Common validation rules
COMMON_VALIDATION_RULES = {
    "not_null": lambda col: ValidationRule(
        name=f"{col}_not_null",
        condition=f"{col} IS NOT NULL",
        error_message=f"{col} must not be null",
    ),
    "positive": lambda col: ValidationRule(
        name=f"{col}_positive",
        condition=f"{col} > 0",
        error_message=f"{col} must be positive",
    ),
    "non_negative": lambda col: ValidationRule(
        name=f"{col}_non_negative",
        condition=f"{col} >= 0",
        error_message=f"{col} must be non-negative",
    ),
    "not_empty": lambda col: ValidationRule(
        name=f"{col}_not_empty",
        condition=f"LENGTH(TRIM({col})) > 0",
        error_message=f"{col} must not be empty",
    ),
    "valid_email": lambda col: ValidationRule(
        name=f"{col}_valid_email",
        condition=f"{col} RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{{2,}}$'",
        error_message=f"{col} must be a valid email",
    ),
    "date_not_future": lambda col: ValidationRule(
        name=f"{col}_not_future",
        condition=f"{col} <= CURRENT_DATE()",
        error_message=f"{col} must not be in the future",
    ),
}

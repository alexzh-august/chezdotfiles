"""
Specialized Code Analyzers

AST-based analyzers for Python, SQL, and JSON files.
"""

from __future__ import annotations

import ast
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class Finding:
    """A finding from code analysis."""

    rule_id: str
    message: str
    line: int
    column: int
    severity: str
    suggestion: str | None = None


class BaseAnalyzer(ABC):
    """Base class for code analyzers."""

    @abstractmethod
    def analyze(self, content: str, file_path: str | None = None) -> list[Finding]:
        """Analyze code content and return findings."""


class PythonAnalyzer(BaseAnalyzer):
    """
    AST-based Python code analyzer for Databricks patterns.

    Detects issues like:
    - Hardcoded credentials
    - Improper client initialization
    - Missing parameterization
    - Direct file access bypassing Unity Catalog
    """

    def analyze(self, content: str, file_path: str | None = None) -> list[Finding]:
        findings: list[Finding] = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return findings

        # Run all AST visitors
        visitors = [
            self._check_hardcoded_tokens,
            self._check_client_initialization,
            self._check_sql_string_formatting,
            self._check_direct_file_access,
            self._check_exception_handling,
        ]

        for visitor in visitors:
            findings.extend(visitor(tree, content))

        return findings

    def _check_hardcoded_tokens(
        self, tree: ast.AST, content: str
    ) -> list[Finding]:
        """Check for hardcoded Databricks tokens."""
        findings: list[Finding] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                value = node.value
                # Check for PAT token pattern
                if re.match(r"^dapi[a-zA-Z0-9]{32,}$", value):
                    findings.append(
                        Finding(
                            rule_id="AUTH003",
                            message="Hardcoded Databricks PAT token detected",
                            line=node.lineno,
                            column=node.col_offset,
                            severity="error",
                            suggestion="Use os.environ.get('DATABRICKS_TOKEN')",
                        )
                    )

        return findings

    def _check_client_initialization(
        self, tree: ast.AST, content: str
    ) -> list[Finding]:
        """Check for improper client initialization patterns."""
        findings: list[Finding] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for WorkspaceClient with explicit token
                func = node.func
                func_name = ""

                if isinstance(func, ast.Name):
                    func_name = func.id
                elif isinstance(func, ast.Attribute):
                    func_name = func.attr

                if func_name == "WorkspaceClient":
                    for keyword in node.keywords:
                        if keyword.arg == "token":
                            findings.append(
                                Finding(
                                    rule_id="AUTH012",
                                    message="Explicit token in WorkspaceClient",
                                    line=node.lineno,
                                    column=node.col_offset,
                                    severity="warning",
                                    suggestion="Let SDK auto-discover credentials",
                                )
                            )

        return findings

    def _check_sql_string_formatting(
        self, tree: ast.AST, content: str
    ) -> list[Finding]:
        """Check for SQL injection vulnerabilities via string formatting."""
        findings: list[Finding] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                func_name = ""

                if isinstance(func, ast.Name):
                    func_name = func.id
                elif isinstance(func, ast.Attribute):
                    func_name = func.attr

                if func_name in ("execute_sql", "sql", "query"):
                    # Check if first argument is an f-string
                    if node.args:
                        first_arg = node.args[0]
                        if isinstance(first_arg, ast.JoinedStr):
                            findings.append(
                                Finding(
                                    rule_id="SQL002",
                                    message="SQL with f-string formatting (injection risk)",
                                    line=node.lineno,
                                    column=node.col_offset,
                                    severity="error",
                                    suggestion="Use parameterized queries instead",
                                )
                            )
                        elif isinstance(first_arg, ast.BinOp) and isinstance(
                            first_arg.op, (ast.Add, ast.Mod)
                        ):
                            findings.append(
                                Finding(
                                    rule_id="SQL002",
                                    message="SQL with string concatenation (injection risk)",
                                    line=node.lineno,
                                    column=node.col_offset,
                                    severity="error",
                                    suggestion="Use parameterized queries instead",
                                )
                            )

        return findings

    def _check_direct_file_access(
        self, tree: ast.AST, content: str
    ) -> list[Finding]:
        """Check for direct cloud storage access bypassing Unity Catalog."""
        findings: list[Finding] = []

        cloud_path_patterns = [
            r"s3://",
            r"s3a://",
            r"abfss://",
            r"gs://",
            r"/dbfs/mnt/",
        ]

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                for pattern in cloud_path_patterns:
                    if re.search(pattern, node.value):
                        findings.append(
                            Finding(
                                rule_id="UC006",
                                message="Direct cloud storage access (bypasses UC governance)",
                                line=node.lineno,
                                column=node.col_offset,
                                severity="warning",
                                suggestion="Use Unity Catalog tables or Volumes",
                            )
                        )
                        break

        return findings

    def _check_exception_handling(
        self, tree: ast.AST, content: str
    ) -> list[Finding]:
        """Check for bare except clauses."""
        findings: list[Finding] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    findings.append(
                        Finding(
                            rule_id="SQL014",
                            message="Bare except clause (catches all exceptions)",
                            line=node.lineno,
                            column=node.col_offset,
                            severity="warning",
                            suggestion="Catch specific exception types",
                        )
                    )

        return findings


class SQLAnalyzer(BaseAnalyzer):
    """
    SQL code analyzer for Databricks patterns.

    Detects issues like:
    - Missing fully qualified table names
    - SELECT * usage
    - Missing LIMIT clauses
    """

    # SQL keywords that precede table names
    TABLE_KEYWORDS = {"FROM", "JOIN", "INTO", "UPDATE", "TABLE"}

    def analyze(self, content: str, file_path: str | None = None) -> list[Finding]:
        findings: list[Finding] = []
        lines = content.upper().splitlines()

        for line_num, line in enumerate(lines, start=1):
            findings.extend(self._check_line(line, line_num))

        return findings

    def _check_line(self, line: str, line_num: int) -> list[Finding]:
        findings: list[Finding] = []

        # Check for SELECT * (warning)
        if re.search(r"\bSELECT\s+\*\s+FROM\b", line):
            findings.append(
                Finding(
                    rule_id="SQL008",
                    message="SELECT * usage (performance impact)",
                    line=line_num,
                    column=0,
                    severity="warning",
                    suggestion="Specify column names explicitly",
                )
            )

        # Check for missing LIMIT on SELECT *
        if re.search(r"\bSELECT\b.*\bFROM\b", line) and not re.search(
            r"\bLIMIT\b", line
        ):
            # Only flag if it looks like a simple query (no subquery indicators)
            if line.count("SELECT") == 1:
                findings.append(
                    Finding(
                        rule_id="SQL006",
                        message="Query without LIMIT clause",
                        line=line_num,
                        column=0,
                        severity="info",
                        suggestion="Add LIMIT for large tables",
                    )
                )

        # Check for table references without full qualification
        # This is a simplified check - full parsing would need a SQL parser
        table_pattern = r"\b(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b"
        for match in re.finditer(table_pattern, line):
            table_name = match.group(1)
            # Check if it's not fully qualified (no dots)
            if "." not in table_name and table_name.upper() not in {
                "SELECT",
                "WHERE",
                "AND",
                "OR",
                "ON",
            }:
                findings.append(
                    Finding(
                        rule_id="UC001",
                        message=f"Table '{table_name}' not fully qualified",
                        line=line_num,
                        column=match.start(),
                        severity="warning",
                        suggestion="Use catalog.schema.table format",
                    )
                )

        return findings


class JSONAnalyzer(BaseAnalyzer):
    """
    JSON configuration analyzer for Databricks MCP patterns.

    Detects issues like:
    - Missing mcpServers key
    - Hardcoded tokens
    - Incorrect URL formats
    """

    def analyze(self, content: str, file_path: str | None = None) -> list[Finding]:
        findings: list[Finding] = []

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return findings

        findings.extend(self._analyze_structure(data, content))
        return findings

    def _analyze_structure(
        self, data: Any, raw_content: str, path: str = ""
    ) -> list[Finding]:
        findings: list[Finding] = []

        if isinstance(data, dict):
            # Check for MCP configuration issues
            if "mcpServers" in data or "mcp_servers" in data or "servers" in data:
                findings.extend(self._check_mcp_config(data, raw_content))

            # Check for hardcoded tokens
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key

                if isinstance(value, str):
                    if re.match(r"^dapi[a-zA-Z0-9]{32,}$", value):
                        line = self._find_line_number(raw_content, value)
                        findings.append(
                            Finding(
                                rule_id="AUTH003",
                                message=f"Hardcoded token at {new_path}",
                                line=line,
                                column=0,
                                severity="error",
                                suggestion="Use environment variable reference",
                            )
                        )

                elif isinstance(value, dict):
                    findings.extend(
                        self._analyze_structure(value, raw_content, new_path)
                    )

        return findings

    def _check_mcp_config(self, data: dict, raw_content: str) -> list[Finding]:
        findings: list[Finding] = []

        # Check for wrong key name
        if "servers" in data and "mcpServers" not in data:
            findings.append(
                Finding(
                    rule_id="MCP004",
                    message="Use 'mcpServers' instead of 'servers'",
                    line=self._find_line_number(raw_content, "servers"),
                    column=0,
                    severity="error",
                    suggestion='Rename key to "mcpServers"',
                )
            )

        if "mcp_servers" in data and "mcpServers" not in data:
            findings.append(
                Finding(
                    rule_id="MCP004",
                    message="Use 'mcpServers' instead of 'mcp_servers'",
                    line=self._find_line_number(raw_content, "mcp_servers"),
                    column=0,
                    severity="error",
                    suggestion='Rename key to "mcpServers"',
                )
            )

        # Check MCP server URLs
        servers = data.get("mcpServers", {})
        for name, config in servers.items():
            if isinstance(config, dict) and "url" in config:
                url = config["url"]

                # Check vector-search URL format
                if "vector-search" in url and not re.search(
                    r"vector-search/[\w-]+/[\w-]+", url
                ):
                    findings.append(
                        Finding(
                            rule_id="MCP001",
                            message="Vector Search URL missing catalog/schema",
                            line=self._find_line_number(raw_content, url),
                            column=0,
                            severity="error",
                            suggestion="Use /vector-search/{catalog}/{schema}",
                        )
                    )

                # Check genie URL format
                if "mcp/genie" in url and not re.search(
                    r"genie/[\w-]+", url
                ):
                    findings.append(
                        Finding(
                            rule_id="MCP002",
                            message="Genie URL missing genie_space_id",
                            line=self._find_line_number(raw_content, url),
                            column=0,
                            severity="error",
                            suggestion="Use /genie/{genie_space_id}",
                        )
                    )

        return findings

    def _find_line_number(self, content: str, search: str) -> int:
        """Find line number containing a string."""
        for i, line in enumerate(content.splitlines(), start=1):
            if search in line:
                return i
        return 1

"""
Databricks Code Pattern Detectors

A comprehensive toolkit for detecting, generating, and refactoring
Databricks code to follow best practices.

Modules:
- patterns: DO/DON'T pattern definitions for each Databricks package
- detectors: AST-based and regex-based code analysis
- generators: Code generation for common Databricks patterns
- refactors: Automated code refactoring utilities

Usage:
    from databricks_patterns import analyze, generate, refactor

    # Analyze code for pattern violations
    result = analyze.file("my_code.py")
    print(result.violations)

    # Generate best-practice code
    config = generate.mcp_config(
        workspace_host="https://my-workspace.cloud.databricks.com",
        catalog="my_catalog",
        schema="my_schema",
    )

    # Refactor existing code
    refactored, changes = refactor.sql(
        "SELECT * FROM users",
        catalog="prod",
        schema="main",
    )
"""

__version__ = "1.0.0"

from . import patterns
from . import detectors
from . import generators
from . import refactors

# Convenience imports
from .detectors.engine import PatternEngine, create_default_engine, Violation
from .detectors.reporter import PatternReporter

__all__ = [
    "patterns",
    "detectors",
    "generators",
    "refactors",
    "PatternEngine",
    "create_default_engine",
    "Violation",
    "PatternReporter",
]

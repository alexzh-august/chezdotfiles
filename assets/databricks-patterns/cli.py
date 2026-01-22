#!/usr/bin/env python3
"""
Databricks Pattern Detector CLI

Command-line interface for analyzing code against Databricks best practices.

Usage:
    python -m databricks_patterns analyze <path>
    python -m databricks_patterns generate mcp-config
    python -m databricks_patterns refactor <file>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .detectors.engine import create_default_engine
from .detectors.reporter import PatternReporter, format_summary
from .generators.mcp_config import MCPConfigGenerator
from .generators.sql_queries import SQLQueryGenerator
from .generators.client_setup import ClientSetupGenerator
from .refactors.sql_refactor import SQLRefactor
from .refactors.auth_refactor import AuthRefactor


def cmd_analyze(args: argparse.Namespace) -> int:
    """Run pattern analysis on files/directories."""
    engine = create_default_engine(include_info=args.include_info)
    path = Path(args.path)

    if path.is_file():
        result = engine.analyze_file(path)
    elif path.is_dir():
        result = engine.analyze_directory(
            path,
            recursive=not args.no_recursive,
            exclude_patterns=args.exclude or [],
        )
    else:
        print(f"Error: Path not found: {path}", file=sys.stderr)
        return 1

    # Output results
    reporter = PatternReporter(result)

    if args.format == "text":
        reporter.to_text(color=not args.no_color)
    elif args.format == "json":
        reporter.to_json()
    elif args.format == "sarif":
        reporter.to_sarif()
    elif args.format == "github":
        reporter.to_github_actions()

    # Print summary
    print(f"\n{format_summary(result)}")

    # Exit code based on errors
    return 1 if result.error_count > 0 else 0


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate code from templates."""
    if args.template == "mcp-config":
        generator = MCPConfigGenerator(
            workspace_host=args.workspace or "https://your-workspace.cloud.databricks.com",
            catalog=args.catalog,
            schema=args.schema,
            genie_space_id=args.genie_space_id,
        )

        config = generator.generate_claude_desktop(
            include_sql=True,
            include_genie=args.genie_space_id is not None,
            include_vector_search=args.catalog is not None and args.schema is not None,
            include_functions=args.catalog is not None and args.schema is not None,
        )
        print(config)

    elif args.template == "sql":
        if not args.catalog or not args.schema:
            print("Error: --catalog and --schema required for SQL generation", file=sys.stderr)
            return 1

        generator = SQLQueryGenerator(args.catalog, args.schema)
        print(generator.select(args.table or "example_table", limit=100))

    elif args.template == "client":
        generator = ClientSetupGenerator()
        print(generator.workspace_client(auth_method=args.auth_method or "auto"))

    else:
        print(f"Unknown template: {args.template}", file=sys.stderr)
        return 1

    return 0


def cmd_refactor(args: argparse.Namespace) -> int:
    """Refactor code to follow best practices."""
    path = Path(args.file)

    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        return 1

    content = path.read_text()
    changes = []

    if args.type == "sql":
        refactor = SQLRefactor(
            default_catalog=args.catalog or "catalog",
            default_schema=args.schema or "schema",
        )
        result, sql_changes = refactor.refactor(content)
        changes.extend(sql_changes)
        content = result

    elif args.type == "auth":
        result, auth_changes = AuthRefactor.refactor_hardcoded_token(content)
        changes.extend(auth_changes)
        content = result

    elif args.type == "all":
        # Apply all refactorings
        result, auth_changes = AuthRefactor.refactor_hardcoded_token(content)
        changes.extend(auth_changes)
        content = result

    # Output
    if args.diff:
        print("Changes made:")
        for change in changes:
            print(f"  - {change}")
        print("\nRefactored code:")
        print(content)
    elif args.in_place:
        path.write_text(content)
        print(f"Updated {path}")
        for change in changes:
            print(f"  - {change}")
    else:
        print(content)

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Databricks Code Pattern Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze code for pattern violations",
    )
    analyze_parser.add_argument("path", help="File or directory to analyze")
    analyze_parser.add_argument(
        "--format",
        choices=["text", "json", "sarif", "github"],
        default="text",
        help="Output format",
    )
    analyze_parser.add_argument(
        "--include-info",
        action="store_true",
        help="Include info-level violations",
    )
    analyze_parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't recurse into subdirectories",
    )
    analyze_parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    analyze_parser.add_argument(
        "--exclude",
        action="append",
        help="Glob patterns to exclude",
    )
    analyze_parser.set_defaults(func=cmd_analyze)

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate code from templates",
    )
    generate_parser.add_argument(
        "template",
        choices=["mcp-config", "sql", "client"],
        help="Template to generate",
    )
    generate_parser.add_argument("--workspace", help="Databricks workspace URL")
    generate_parser.add_argument("--catalog", help="Unity Catalog name")
    generate_parser.add_argument("--schema", help="Schema name")
    generate_parser.add_argument("--table", help="Table name (for SQL)")
    generate_parser.add_argument("--genie-space-id", help="Genie space ID")
    generate_parser.add_argument(
        "--auth-method",
        choices=["auto", "env", "profile", "service_principal"],
        help="Authentication method (for client)",
    )
    generate_parser.set_defaults(func=cmd_generate)

    # Refactor command
    refactor_parser = subparsers.add_parser(
        "refactor",
        help="Refactor code to follow best practices",
    )
    refactor_parser.add_argument("file", help="File to refactor")
    refactor_parser.add_argument(
        "--type",
        choices=["sql", "auth", "all"],
        default="all",
        help="Type of refactoring",
    )
    refactor_parser.add_argument("--catalog", help="Default catalog for SQL")
    refactor_parser.add_argument("--schema", help="Default schema for SQL")
    refactor_parser.add_argument(
        "--in-place",
        action="store_true",
        help="Modify file in place",
    )
    refactor_parser.add_argument(
        "--diff",
        action="store_true",
        help="Show diff of changes",
    )
    refactor_parser.set_defaults(func=cmd_refactor)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

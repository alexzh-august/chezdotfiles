"""
Pattern Violation Reporter

Output formatting for pattern analysis results.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING, TextIO
import sys

if TYPE_CHECKING:
    from .engine import AnalysisResult, Violation


class PatternReporter:
    """
    Report pattern violations in various formats.

    Supports:
    - Text (human-readable)
    - JSON (machine-readable)
    - SARIF (for IDE integration)
    - GitHub Actions (annotations)
    """

    def __init__(self, result: AnalysisResult) -> None:
        self.result = result

    def to_text(self, *, output: TextIO = sys.stdout, color: bool = True) -> None:
        """Output human-readable text report."""
        r = self.result

        # Summary header
        print(f"\n{'=' * 60}", file=output)
        print("DATABRICKS PATTERN ANALYSIS REPORT", file=output)
        print(f"{'=' * 60}", file=output)
        print(f"Files analyzed: {r.files_analyzed}", file=output)
        print(f"Patterns checked: {r.patterns_checked}", file=output)
        print(f"Total violations: {len(r.violations)}", file=output)
        print(f"  Errors: {r.error_count}", file=output)
        print(f"  Warnings: {r.warning_count}", file=output)
        print(f"  Info: {r.info_count}", file=output)
        print(f"{'=' * 60}\n", file=output)

        if not r.violations:
            print("No violations found.", file=output)
            return

        # Group by severity
        for severity in ("error", "warning", "info"):
            violations = r.by_severity(severity)
            if not violations:
                continue

            severity_display = severity.upper()
            if color:
                colors = {"error": "\033[91m", "warning": "\033[93m", "info": "\033[94m"}
                reset = "\033[0m"
                severity_display = f"{colors.get(severity, '')}{severity.upper()}{reset}"

            print(f"\n{'-' * 40}", file=output)
            print(f"{severity_display} ({len(violations)})", file=output)
            print(f"{'-' * 40}", file=output)

            for v in violations:
                self._print_violation(v, output, color)

    def _print_violation(
        self, v: Violation, output: TextIO, color: bool
    ) -> None:
        """Print a single violation."""
        print(f"\n[{v.pattern_id}] {v.description}", file=output)
        print(f"  Location: {v.file_path}:{v.line_number}", file=output)
        print(f"  Line: {v.line_content.strip()[:80]}", file=output)

        if v.do_pattern:
            print(f"  DO: {v.do_pattern}", file=output)
        if v.dont_pattern:
            print(f"  DON'T: {v.dont_pattern}", file=output)
        if v.fix_suggestion:
            print(f"  Fix: {v.fix_suggestion}", file=output)

    def to_json(self, *, output: TextIO = sys.stdout, indent: int = 2) -> None:
        """Output JSON report."""
        r = self.result

        report = {
            "summary": {
                "files_analyzed": r.files_analyzed,
                "patterns_checked": r.patterns_checked,
                "total_violations": len(r.violations),
                "errors": r.error_count,
                "warnings": r.warning_count,
                "info": r.info_count,
            },
            "violations": [asdict(v) for v in r.violations],
        }

        json.dump(report, output, indent=indent)
        print(file=output)  # Trailing newline

    def to_sarif(self, *, output: TextIO = sys.stdout) -> None:
        """
        Output SARIF format for IDE integration.

        SARIF (Static Analysis Results Interchange Format) is supported by
        VS Code, GitHub Code Scanning, and other tools.
        """
        r = self.result

        # Build rules from violations
        rules_seen: dict[str, dict] = {}
        for v in r.violations:
            if v.pattern_id not in rules_seen:
                rules_seen[v.pattern_id] = {
                    "id": v.pattern_id,
                    "name": v.pattern_id,
                    "shortDescription": {"text": v.description},
                    "fullDescription": {"text": v.description},
                    "help": {
                        "text": v.fix_suggestion or v.description,
                        "markdown": f"**DO:** {v.do_pattern or 'N/A'}\n\n**DON'T:** {v.dont_pattern or 'N/A'}",
                    },
                    "defaultConfiguration": {
                        "level": self._sarif_level(v.severity)
                    },
                }

        # Build results
        results = []
        for v in r.violations:
            results.append(
                {
                    "ruleId": v.pattern_id,
                    "level": self._sarif_level(v.severity),
                    "message": {"text": v.description},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": v.file_path},
                                "region": {
                                    "startLine": v.line_number,
                                    "startColumn": 1,
                                },
                            }
                        }
                    ],
                }
            )

        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "databricks-patterns",
                            "version": "1.0.0",
                            "informationUri": "https://docs.databricks.com",
                            "rules": list(rules_seen.values()),
                        }
                    },
                    "results": results,
                }
            ],
        }

        json.dump(sarif, output, indent=2)
        print(file=output)

    def to_github_actions(self, *, output: TextIO = sys.stdout) -> None:
        """Output GitHub Actions annotation format."""
        for v in self.result.violations:
            level = "error" if v.severity == "error" else "warning"
            # Escape message for GitHub Actions
            message = v.description.replace("%", "%25").replace("\n", "%0A")
            print(
                f"::{level} file={v.file_path},line={v.line_number}::{v.pattern_id}: {message}",
                file=output,
            )

    @staticmethod
    def _sarif_level(severity: str) -> str:
        """Convert severity to SARIF level."""
        return {
            "error": "error",
            "warning": "warning",
            "info": "note",
        }.get(severity, "note")


def format_summary(result: AnalysisResult) -> str:
    """Format a one-line summary."""
    r = result
    status = "PASS" if r.error_count == 0 else "FAIL"
    return (
        f"[{status}] "
        f"{r.files_analyzed} files, "
        f"{r.error_count} errors, "
        f"{r.warning_count} warnings, "
        f"{r.info_count} info"
    )

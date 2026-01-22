"""
Pattern Detection Engine

Core engine for running pattern detectors across codebases.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from ..patterns import Pattern


@dataclass
class Violation:
    """Represents a pattern violation found in code."""

    pattern_id: str
    severity: str
    category: str
    description: str
    file_path: str
    line_number: int
    line_content: str
    fix_suggestion: str | None = None
    do_pattern: str | None = None
    dont_pattern: str | None = None

    def __str__(self) -> str:
        return (
            f"[{self.severity.upper()}] {self.pattern_id}: {self.description}\n"
            f"  File: {self.file_path}:{self.line_number}\n"
            f"  Line: {self.line_content.strip()}\n"
            f"  Fix: {self.fix_suggestion or 'See pattern documentation'}"
        )


@dataclass
class AnalysisResult:
    """Result of pattern analysis on a codebase."""

    violations: list[Violation] = field(default_factory=list)
    files_analyzed: int = 0
    patterns_checked: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "info")

    def by_severity(self, severity: str) -> list[Violation]:
        return [v for v in self.violations if v.severity == severity]

    def by_category(self, category: str) -> list[Violation]:
        return [v for v in self.violations if v.category == category]

    def by_file(self, file_path: str) -> list[Violation]:
        return [v for v in self.violations if v.file_path == file_path]


class PatternEngine:
    """
    Main engine for detecting pattern violations.

    Supports multiple file types and pattern sources.
    """

    # File extensions to analyze
    PYTHON_EXTENSIONS = {".py", ".pyi"}
    SQL_EXTENSIONS = {".sql"}
    JSON_EXTENSIONS = {".json"}
    NOTEBOOK_EXTENSIONS = {".ipynb"}
    ALL_EXTENSIONS = PYTHON_EXTENSIONS | SQL_EXTENSIONS | JSON_EXTENSIONS | NOTEBOOK_EXTENSIONS

    def __init__(
        self,
        patterns: dict[str, list[Pattern]] | None = None,
        *,
        include_info: bool = False,
    ) -> None:
        """
        Initialize the pattern engine.

        Args:
            patterns: Dictionary of pattern categories to pattern lists.
            include_info: Whether to include info-level violations.
        """
        self.patterns = patterns or {}
        self.include_info = include_info
        self._compiled_patterns: dict[str, re.Pattern[str]] = {}

    def add_patterns(self, category: str, patterns: list[Pattern]) -> None:
        """Add patterns for a category."""
        self.patterns[category] = patterns

    def analyze_file(self, file_path: Path | str) -> AnalysisResult:
        """Analyze a single file for pattern violations."""
        file_path = Path(file_path)
        result = AnalysisResult(files_analyzed=1)

        if not file_path.exists():
            return result

        suffix = file_path.suffix.lower()
        if suffix not in self.ALL_EXTENSIONS:
            return result

        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return result

        # Run all pattern checks
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                result.patterns_checked += 1

                if not self.include_info and pattern["severity"] == "info":
                    continue

                if pattern.get("regex"):
                    violations = self._check_regex_pattern(
                        content, pattern, str(file_path)
                    )
                    result.violations.extend(violations)

        return result

    def analyze_directory(
        self,
        directory: Path | str,
        *,
        recursive: bool = True,
        exclude_patterns: list[str] | None = None,
    ) -> AnalysisResult:
        """
        Analyze all files in a directory.

        Args:
            directory: Directory to analyze.
            recursive: Whether to recurse into subdirectories.
            exclude_patterns: Glob patterns for files to exclude.
        """
        directory = Path(directory)
        result = AnalysisResult()
        exclude_patterns = exclude_patterns or [
            "**/venv/**",
            "**/.venv/**",
            "**/node_modules/**",
            "**/__pycache__/**",
            "**/.git/**",
        ]

        for file_path in self._iter_files(directory, recursive):
            # Check exclusions
            if any(file_path.match(p) for p in exclude_patterns):
                continue

            file_result = self.analyze_file(file_path)
            result.files_analyzed += file_result.files_analyzed
            result.patterns_checked += file_result.patterns_checked
            result.violations.extend(file_result.violations)

        return result

    def analyze_string(
        self,
        content: str,
        file_type: str = "python",
        file_name: str = "<string>",
    ) -> AnalysisResult:
        """
        Analyze a string of code.

        Args:
            content: Code content to analyze.
            file_type: Type of file (python, sql, json).
            file_name: Name to use in violation reports.
        """
        result = AnalysisResult(files_analyzed=1)

        for category, patterns in self.patterns.items():
            for pattern in patterns:
                result.patterns_checked += 1

                if not self.include_info and pattern["severity"] == "info":
                    continue

                if pattern.get("regex"):
                    violations = self._check_regex_pattern(
                        content, pattern, file_name
                    )
                    result.violations.extend(violations)

        return result

    def _check_regex_pattern(
        self,
        content: str,
        pattern: Pattern,
        file_path: str,
    ) -> list[Violation]:
        """Check content against a regex pattern."""
        violations = []
        regex_str = pattern.get("regex")
        if not regex_str:
            return violations

        # Compile and cache pattern
        if regex_str not in self._compiled_patterns:
            try:
                self._compiled_patterns[regex_str] = re.compile(
                    regex_str, re.IGNORECASE | re.MULTILINE
                )
            except re.error:
                return violations

        compiled = self._compiled_patterns[regex_str]
        lines = content.splitlines()

        for line_num, line in enumerate(lines, start=1):
            if compiled.search(line):
                violations.append(
                    Violation(
                        pattern_id=pattern["id"],
                        severity=pattern["severity"],
                        category=pattern["category"],
                        description=pattern["description"],
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        fix_suggestion=pattern.get("fix_suggestion"),
                        do_pattern=pattern.get("do_pattern"),
                        dont_pattern=pattern.get("dont_pattern"),
                    )
                )

        return violations

    def _iter_files(
        self,
        directory: Path,
        recursive: bool,
    ) -> Iterator[Path]:
        """Iterate over files in a directory."""
        if recursive:
            for ext in self.ALL_EXTENSIONS:
                yield from directory.rglob(f"*{ext}")
        else:
            for ext in self.ALL_EXTENSIONS:
                yield from directory.glob(f"*{ext}")


def create_default_engine(*, include_info: bool = False) -> PatternEngine:
    """Create an engine with all default Databricks patterns loaded."""
    from ..patterns import ALL_PATTERNS

    engine = PatternEngine(include_info=include_info)
    for category, patterns in ALL_PATTERNS.items():
        engine.add_patterns(category, patterns)

    return engine

#!/usr/bin/env python3
"""
Validate frontmatter in dotfile components.

Ensures all agents, commands, and skills have required metadata
for Figma MCP integration and visual documentation.
"""

import argparse
import sys
from pathlib import Path
import yaml
import json

# Required frontmatter fields for each component type
REQUIRED_FIELDS = {
    "agent": ["name", "description"],
    "command": ["description"],
    "skill": ["name", "description"],
}

# Optional but recommended Figma integration fields
FIGMA_FIELDS = {
    "diagram_type": ["flowchart", "sequence", "state", "architecture"],
    "integration_points": list,  # Should be a list of strings
}

VALID_INTEGRATION_POINTS = [
    "github",
    "filesystem",
    "mcp-servers",
    "database",
    "api",
    "cli",
    "browser",
    "figma",
]


def parse_frontmatter(file_path: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    content = file_path.read_text()

    if not content.startswith("---"):
        return None

    try:
        # Find the closing ---
        end_idx = content.index("---", 3)
        frontmatter_str = content[3:end_idx].strip()
        return yaml.safe_load(frontmatter_str)
    except (ValueError, yaml.YAMLError) as e:
        print(f"  ⚠️  Error parsing frontmatter in {file_path}: {e}")
        return None


def validate_component(file_path: Path, component_type: str) -> list[str]:
    """Validate a single component file. Returns list of issues."""
    issues = []

    frontmatter = parse_frontmatter(file_path)

    if frontmatter is None:
        issues.append(f"Missing frontmatter")
        return issues

    # Check required fields
    for field in REQUIRED_FIELDS.get(component_type, []):
        if field not in frontmatter:
            issues.append(f"Missing required field: {field}")

    # Check Figma integration fields (warnings, not errors)
    figma_config = frontmatter.get("figma", {})
    if not figma_config:
        issues.append(f"[INFO] No figma section - visual artifacts won't be generated")
    else:
        # Validate diagram_type
        diagram_type = figma_config.get("diagram_type")
        if diagram_type and diagram_type not in FIGMA_FIELDS["diagram_type"]:
            issues.append(
                f"Invalid diagram_type: {diagram_type}. "
                f"Must be one of: {FIGMA_FIELDS['diagram_type']}"
            )

        # Validate integration_points
        integration_points = figma_config.get("integration_points", [])
        if integration_points:
            for point in integration_points:
                if point not in VALID_INTEGRATION_POINTS:
                    issues.append(
                        f"[WARN] Unknown integration_point: {point}. "
                        f"Consider adding to VALID_INTEGRATION_POINTS"
                    )

    return issues


def scan_directory(directory: Path, component_type: str) -> dict[str, list[str]]:
    """Scan a directory for component files and validate each."""
    results = {}

    if not directory.exists():
        return results

    for file_path in directory.rglob("*.md"):
        # Skip READMEs and other non-component files
        if file_path.name.lower() in ["readme.md", "changelog.md"]:
            continue

        issues = validate_component(file_path, component_type)
        if issues:
            results[str(file_path)] = issues

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate frontmatter in dotfile components"
    )
    parser.add_argument("--agents", type=str, default="false")
    parser.add_argument("--commands", type=str, default="false")
    parser.add_argument("--skills", type=str, default="false")
    parser.add_argument("--all", action="store_true", help="Validate all components")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()

    base_path = Path("dotfiles/dot_claude")
    all_issues = {}
    error_count = 0

    components_to_check = []

    if args.all or args.agents == "true":
        components_to_check.append(("agents", "agent"))
    if args.all or args.commands == "true":
        components_to_check.append(("commands", "command"))
    if args.all or args.skills == "true":
        components_to_check.append(("skills", "skill"))

    # If nothing specified, check all
    if not components_to_check:
        components_to_check = [
            ("agents", "agent"),
            ("commands", "command"),
            ("skills", "skill"),
        ]

    print("🔍 Validating frontmatter...\n")

    for dir_name, component_type in components_to_check:
        dir_path = base_path / dir_name
        print(f"📁 Checking {dir_path}...")

        issues = scan_directory(dir_path, component_type)

        if issues:
            all_issues.update(issues)
            for file_path, file_issues in issues.items():
                print(f"\n  📄 {file_path}:")
                for issue in file_issues:
                    if issue.startswith("[INFO]"):
                        print(f"    ℹ️  {issue}")
                    elif issue.startswith("[WARN]"):
                        print(f"    ⚠️  {issue}")
                        if args.strict:
                            error_count += 1
                    else:
                        print(f"    ❌ {issue}")
                        error_count += 1
        else:
            print(f"  ✅ All files valid")

    print(f"\n{'='*50}")

    if error_count > 0:
        print(f"❌ Validation failed with {error_count} error(s)")
        sys.exit(1)
    else:
        print("✅ All frontmatter validation passed")
        sys.exit(0)


if __name__ == "__main__":
    main()

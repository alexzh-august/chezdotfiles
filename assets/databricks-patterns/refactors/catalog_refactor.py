"""
Unity Catalog Refactoring Utilities

Upgrade code to follow Unity Catalog best practices.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class CatalogRefactor:
    """
    Refactor code to follow Unity Catalog patterns.

    Transformations:
    - Unqualified table names -> Fully qualified names
    - Direct file paths -> Unity Catalog references
    - Legacy mount paths -> Volumes
    """

    default_catalog: str
    default_schema: str

    def refactor_table_references(self, code: str) -> tuple[str, list[str]]:
        """
        Qualify unqualified table references.

        Returns:
            Tuple of (refactored_code, list_of_changes).
        """
        changes = []

        # Pattern for spark.table() with unqualified name
        table_pattern = r'spark\.table\s*\(\s*["\']([a-zA-Z_][a-zA-Z0-9_]*)["\']'

        def qualify_table(match: re.Match) -> str:
            table_name = match.group(1)
            qualified = f"{self.default_catalog}.{self.default_schema}.{table_name}"
            changes.append(f"Qualified spark.table('{table_name}') -> spark.table('{qualified}')")
            return f'spark.table("{qualified}"'

        result = re.sub(table_pattern, qualify_table, code)

        # Pattern for SQL strings with FROM table
        sql_pattern = r'(FROM\s+)([a-zA-Z_][a-zA-Z0-9_]*)(\s|$|,|\)|")'

        def qualify_sql_table(match: re.Match) -> str:
            keyword = match.group(1)
            table_name = match.group(2)
            suffix = match.group(3)

            # Skip if already qualified
            if table_name.upper() in {"SELECT", "WHERE", "AND", "OR", "ON", "AS"}:
                return match.group(0)

            qualified = f"{self.default_catalog}.{self.default_schema}.{table_name}"
            changes.append(f"Qualified FROM {table_name} -> FROM {qualified}")
            return f"{keyword}{qualified}{suffix}"

        result = re.sub(sql_pattern, qualify_sql_table, result, flags=re.IGNORECASE)

        return result, changes

    def refactor_file_paths(self, code: str) -> tuple[str, list[str]]:
        """
        Convert direct file paths to Unity Catalog patterns.

        Transforms:
        - s3://bucket/path -> Unity Catalog external location
        - /dbfs/mnt/... -> /Volumes/catalog/schema/volume/...
        """
        changes = []
        result = code

        # Convert mount paths to Volumes
        mount_pattern = r'["\']\/dbfs\/mnt\/([^"\']+)["\']'

        def convert_mount(match: re.Match) -> str:
            mount_path = match.group(1)
            # Convert to volumes path (simplified - actual path mapping needed)
            volume_path = f"/Volumes/{self.default_catalog}/{self.default_schema}/data/{mount_path}"
            changes.append(f"Converted /dbfs/mnt/{mount_path} -> {volume_path}")
            return f'"{volume_path}"'

        result = re.sub(mount_pattern, convert_mount, result)

        # Flag direct cloud storage access for review
        cloud_patterns = [
            (r'["\']s3a?://[^"\']+["\']', "S3"),
            (r'["\']abfss?://[^"\']+["\']', "ABFS"),
            (r'["\']gs://[^"\']+["\']', "GCS"),
        ]

        for pattern, cloud_name in cloud_patterns:
            if re.search(pattern, result):
                changes.append(
                    f"WARNING: Found {cloud_name} path - consider using Unity Catalog external location"
                )

        return result, changes

    def refactor_read_write_calls(self, code: str) -> tuple[str, list[str]]:
        """
        Refactor spark.read/write calls to use catalog tables.

        Transforms:
        - spark.read.parquet("path") -> spark.read.table("catalog.schema.table")
        - spark.write.parquet("path") -> df.write.saveAsTable("catalog.schema.table")
        """
        changes = []
        result = code

        # Pattern for read with file path
        read_pattern = r'spark\.read\.(parquet|csv|json|orc)\s*\(\s*["\']([^"\']+)["\']\s*\)'

        def convert_read(match: re.Match) -> str:
            format_type = match.group(1)
            path = match.group(2)

            # Extract table name from path (simplified)
            table_name = path.rstrip("/").split("/")[-1].replace(".", "_")
            qualified = f"{self.default_catalog}.{self.default_schema}.{table_name}"

            changes.append(
                f"Consider converting spark.read.{format_type}('{path}') "
                f"to spark.read.table('{qualified}')"
            )

            # Return original - just warn, don't auto-convert
            return match.group(0)

        result = re.sub(read_pattern, convert_read, result)

        return result, changes

    def generate_migration_sql(
        self,
        source_paths: list[tuple[str, str]],  # (path, table_name)
    ) -> str:
        """
        Generate SQL to migrate files to Unity Catalog tables.

        Returns SQL script for creating external tables.
        """
        statements = []

        for path, table_name in source_paths:
            qualified = f"{self.default_catalog}.{self.default_schema}.{table_name}"

            # Detect format from path
            format_type = "PARQUET"
            if ".csv" in path.lower():
                format_type = "CSV"
            elif ".json" in path.lower():
                format_type = "JSON"

            statements.append(
                f"""\
-- Create external table for {path}
CREATE TABLE IF NOT EXISTS {qualified}
USING {format_type}
LOCATION '{path}';
"""
            )

        return "\n".join(statements)


@dataclass
class VolumesMigration:
    """
    Utilities for migrating to Unity Catalog Volumes.
    """

    catalog: str
    schema: str

    def generate_volume_creation(
        self,
        volume_name: str,
        external_location: str | None = None,
    ) -> str:
        """Generate SQL to create a Volume."""
        qualified = f"{self.catalog}.{self.schema}.{volume_name}"

        if external_location:
            return f"""\
-- Create external volume
CREATE EXTERNAL VOLUME IF NOT EXISTS {qualified}
LOCATION '{external_location}';
"""
        return f"""\
-- Create managed volume
CREATE VOLUME IF NOT EXISTS {qualified};
"""

    def convert_dbfs_path(self, dbfs_path: str, volume_name: str) -> str:
        """Convert a DBFS path to Volumes path."""
        # Remove /dbfs/mnt/ prefix
        relative_path = re.sub(r"^/dbfs/mnt/[^/]+/", "", dbfs_path)
        return f"/Volumes/{self.catalog}/{self.schema}/{volume_name}/{relative_path}"

    def generate_migration_script(
        self,
        mount_mappings: dict[str, str],  # mount_name -> volume_name
    ) -> str:
        """
        Generate a migration script for converting mounts to volumes.

        Returns Python code for the migration.
        """
        mappings_str = "\n".join(
            f'    "{mount}": "{vol}",' for mount, vol in mount_mappings.items()
        )

        return f'''\
"""Migration script: DBFS mounts to Unity Catalog Volumes."""

import os
import shutil

# Mount to Volume mappings
MOUNT_TO_VOLUME = {{
{mappings_str}
}}

def migrate_file(source_path: str) -> str:
    """
    Get the new Volumes path for a DBFS mount path.

    Args:
        source_path: Original /dbfs/mnt/... path

    Returns:
        New /Volumes/... path
    """
    for mount, volume in MOUNT_TO_VOLUME.items():
        if f"/dbfs/mnt/{{mount}}" in source_path:
            return source_path.replace(
                f"/dbfs/mnt/{{mount}}",
                f"/Volumes/{self.catalog}/{self.schema}/{{volume}}"
            )

    raise ValueError(f"No mapping found for path: {{source_path}}")


def update_code_references(code: str) -> str:
    """Update code to use new Volumes paths."""
    result = code
    for mount, volume in MOUNT_TO_VOLUME.items():
        result = result.replace(
            f"/dbfs/mnt/{{mount}}",
            f"/Volumes/{self.catalog}/{self.schema}/{{volume}}"
        )
    return result
'''

"""
Authentication Refactoring Utilities

Upgrade authentication code to best practices.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass


@dataclass
class AuthRefactor:
    """
    Refactor authentication patterns to best practices.

    Transformations:
    - Hardcoded tokens -> environment variables
    - Explicit token passing -> SDK auto-discovery
    - Direct string tokens -> secret manager references
    """

    @staticmethod
    def find_hardcoded_tokens(code: str) -> list[tuple[int, str]]:
        """
        Find hardcoded Databricks tokens in code.

        Returns:
            List of (line_number, token_snippet) tuples.
        """
        findings = []
        lines = code.splitlines()

        for i, line in enumerate(lines, start=1):
            # Check for PAT pattern
            if re.search(r"['\"]dapi[a-zA-Z0-9]{32,}['\"]", line):
                # Mask the token for safety
                masked = re.sub(
                    r"dapi[a-zA-Z0-9]{32,}",
                    "dapi***REDACTED***",
                    line,
                )
                findings.append((i, masked.strip()))

        return findings

    @staticmethod
    def refactor_hardcoded_token(code: str) -> tuple[str, list[str]]:
        """
        Replace hardcoded tokens with environment variable references.

        Returns:
            Tuple of (refactored_code, list_of_changes).
        """
        changes = []

        # Pattern to match token assignments
        pattern = r'(["\'])dapi[a-zA-Z0-9]{32,}\1'

        if re.search(pattern, code):
            result = re.sub(
                pattern,
                'os.environ["DATABRICKS_TOKEN"]',
                code,
            )

            # Check if os import is needed
            if "import os" not in code and "from os import" not in code:
                result = "import os\n\n" + result
                changes.append("Added 'import os'")

            changes.append("Replaced hardcoded token with os.environ['DATABRICKS_TOKEN']")
            return result, changes

        return code, changes

    @staticmethod
    def refactor_explicit_client_auth(code: str) -> tuple[str, list[str]]:
        """
        Refactor explicit WorkspaceClient authentication to auto-discovery.

        Transforms:
            WorkspaceClient(host=..., token=...)
        To:
            WorkspaceClient()  # Uses env vars automatically
        """
        changes = []

        # Pattern for WorkspaceClient with explicit credentials
        pattern = r"WorkspaceClient\s*\(\s*host\s*=\s*[^,)]+,\s*token\s*=\s*[^)]+\)"

        if re.search(pattern, code):
            result = re.sub(pattern, "WorkspaceClient()", code)
            changes.append("Simplified WorkspaceClient to use auto-discovery")
            return result, changes

        # Also handle token-only pattern
        token_pattern = r"WorkspaceClient\s*\(\s*token\s*=\s*[^)]+\)"
        if re.search(token_pattern, code):
            result = re.sub(token_pattern, "WorkspaceClient()", code)
            changes.append("Removed explicit token from WorkspaceClient")
            return result, changes

        return code, changes

    @staticmethod
    def add_env_validation(code: str) -> tuple[str, list[str]]:
        """
        Add environment variable validation before client initialization.

        Adds a check to ensure required env vars are set.
        """
        changes = []

        validation_block = '''\
# Validate required environment variables
_required_env_vars = ["DATABRICKS_HOST"]
_missing_vars = [v for v in _required_env_vars if not os.environ.get(v)]
if _missing_vars:
    raise RuntimeError(f"Missing required environment variables: {_missing_vars}")

'''

        # Check if validation already exists
        if "_required_env_vars" in code or "DATABRICKS_HOST" in code:
            return code, changes

        # Find WorkspaceClient import or instantiation
        client_pattern = r"(.*WorkspaceClient.*)"
        match = re.search(client_pattern, code)

        if match:
            # Insert validation before client usage
            insert_pos = match.start()
            result = code[:insert_pos] + validation_block + code[insert_pos:]
            changes.append("Added environment variable validation")
            return result, changes

        return code, changes

    @staticmethod
    def convert_to_profile_auth(
        code: str,
        profile_name: str,
    ) -> tuple[str, list[str]]:
        """
        Convert to profile-based authentication.

        Uses ~/.databrickscfg profiles instead of environment variables.
        """
        changes = []

        # Replace WorkspaceClient() with profile
        pattern = r"WorkspaceClient\s*\(\s*\)"

        if re.search(pattern, code):
            result = re.sub(
                pattern,
                f'WorkspaceClient(profile="{profile_name}")',
                code,
            )
            changes.append(f"Switched to profile-based auth with profile '{profile_name}'")
            return result, changes

        return code, changes

    @staticmethod
    def generate_secret_manager_pattern(
        secret_scope: str,
        secret_key: str,
    ) -> str:
        """
        Generate code for Databricks secret manager usage.

        Returns Python code for retrieving secrets.
        """
        return f'''\
# Retrieve token from Databricks secret scope
# This should be used in notebooks/jobs running on Databricks
token = dbutils.secrets.get(scope="{secret_scope}", key="{secret_key}")

# For SDK usage outside notebooks, configure environment:
# export DATABRICKS_TOKEN=$(databricks secrets get-secret --scope {secret_scope} --key {secret_key})
'''


@dataclass
class AuthMigration:
    """
    Utilities for migrating authentication patterns.

    Supports migration paths:
    - Hardcoded -> Environment variables
    - Environment variables -> Profile-based
    - Profile-based -> Service principal
    - Any -> Secret manager
    """

    @staticmethod
    def generate_migration_plan(code: str) -> list[str]:
        """
        Generate a migration plan for authentication improvements.

        Returns list of recommended steps.
        """
        steps = []

        # Check current state
        has_hardcoded = bool(re.search(r"['\"]dapi[a-zA-Z0-9]{32,}['\"]", code))
        has_env_get = bool(re.search(r"os\.environ", code))
        has_profile = bool(re.search(r"profile\s*=", code))
        has_service_principal = bool(
            re.search(r"client_id|client_secret|service_principal", code, re.IGNORECASE)
        )

        if has_hardcoded:
            steps.append("1. CRITICAL: Remove hardcoded tokens immediately")
            steps.append("   Replace with: os.environ['DATABRICKS_TOKEN']")
            steps.append("   Add token to .env file (gitignored)")

        if has_env_get and not has_profile:
            steps.append("2. Consider profile-based auth for local development")
            steps.append("   Configure ~/.databrickscfg with named profiles")
            steps.append("   Use: WorkspaceClient(profile='dev')")

        if not has_service_principal:
            steps.append("3. For production, use service principal authentication")
            steps.append("   Create service principal in Databricks")
            steps.append("   Use OIDC token federation for CI/CD")

        steps.append("4. Audit: Ensure no secrets in version control")
        steps.append("   Run: git log -p | grep -i 'dapi'")

        return steps

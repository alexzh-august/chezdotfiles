"""
MCP Configuration Refactoring Utilities

Upgrade MCP configurations to best practices.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass
class MCPConfigRefactor:
    """
    Refactor MCP configurations to follow best practices.

    Transformations:
    - Fix key naming (servers -> mcpServers)
    - Add missing URL components
    - Convert hardcoded tokens to env references
    - Validate URL formats
    """

    @staticmethod
    def refactor(config: str | dict) -> tuple[dict, list[str]]:
        """
        Refactor an MCP configuration.

        Args:
            config: JSON string or dict of MCP config.

        Returns:
            Tuple of (refactored_config, list_of_changes).
        """
        changes = []

        if isinstance(config, str):
            try:
                data = json.loads(config)
            except json.JSONDecodeError as e:
                return {}, [f"Invalid JSON: {e}"]
        else:
            data = config.copy()

        # Fix key naming
        if "servers" in data and "mcpServers" not in data:
            data["mcpServers"] = data.pop("servers")
            changes.append("Renamed 'servers' to 'mcpServers'")

        if "mcp_servers" in data and "mcpServers" not in data:
            data["mcpServers"] = data.pop("mcp_servers")
            changes.append("Renamed 'mcp_servers' to 'mcpServers'")

        # Process each server
        if "mcpServers" in data:
            data["mcpServers"], server_changes = MCPConfigRefactor._refactor_servers(
                data["mcpServers"]
            )
            changes.extend(server_changes)

        return data, changes

    @staticmethod
    def _refactor_servers(servers: dict) -> tuple[dict, list[str]]:
        """Refactor individual server configurations."""
        changes = []
        result = {}

        for name, config in servers.items():
            new_name = name
            new_config = config.copy() if isinstance(config, dict) else config

            # Improve server naming
            if name in ("server1", "mcp", "default", "test"):
                # Try to infer better name from URL
                if isinstance(config, dict) and "url" in config:
                    url = config["url"]
                    if "vector-search" in url:
                        new_name = "databricks-vector-search"
                    elif "genie" in url:
                        new_name = "databricks-genie"
                    elif "functions" in url:
                        new_name = "databricks-uc-functions"
                    elif "sql" in url:
                        new_name = "databricks-sql"
                    else:
                        new_name = f"databricks-{name}"

                    if new_name != name:
                        changes.append(f"Renamed server '{name}' to '{new_name}'")

            # Refactor config content
            if isinstance(new_config, dict):
                new_config, config_changes = MCPConfigRefactor._refactor_server_config(
                    new_name, new_config
                )
                changes.extend(config_changes)

            result[new_name] = new_config

        return result, changes

    @staticmethod
    def _refactor_server_config(name: str, config: dict) -> tuple[dict, list[str]]:
        """Refactor a single server's configuration."""
        changes = []
        result = config.copy()

        # Check for hardcoded tokens in env
        if "env" in result:
            env = result["env"]
            for key, value in env.items():
                if key == "DATABRICKS_TOKEN" and isinstance(value, str):
                    if re.match(r"^dapi[a-zA-Z0-9]{32,}$", value):
                        result["env"][key] = "${DATABRICKS_TOKEN}"
                        changes.append(
                            f"[{name}] Replaced hardcoded token with env reference"
                        )

        # Fix URL formats
        if "url" in result:
            url = result["url"]

            # Check vector-search URL
            if "vector-search" in url and not re.search(
                r"vector-search/[\w-]+/[\w-]+", url
            ):
                changes.append(
                    f"[{name}] WARNING: Vector Search URL should include catalog/schema"
                )

            # Check genie URL
            if "/genie" in url and not re.search(r"genie/[\w-]+", url):
                changes.append(
                    f"[{name}] WARNING: Genie URL should include genie_space_id"
                )

            # Check functions URL
            if "/functions" in url and not re.search(
                r"functions/[\w-]+/[\w-]+", url
            ):
                changes.append(
                    f"[{name}] WARNING: Functions URL should include catalog/schema"
                )

        return result, changes

    @staticmethod
    def validate_config(config: dict) -> list[str]:
        """
        Validate an MCP configuration.

        Returns list of validation errors/warnings.
        """
        issues = []

        if "mcpServers" not in config:
            issues.append("ERROR: Missing 'mcpServers' key")
            return issues

        servers = config["mcpServers"]

        if not servers:
            issues.append("WARNING: No MCP servers configured")
            return issues

        for name, server_config in servers.items():
            if not isinstance(server_config, dict):
                issues.append(f"ERROR: [{name}] Invalid server configuration")
                continue

            # Must have either url or command
            has_url = "url" in server_config
            has_command = "command" in server_config

            if not has_url and not has_command:
                issues.append(f"ERROR: [{name}] Must have 'url' or 'command'")

            if has_url and has_command:
                issues.append(f"WARNING: [{name}] Has both 'url' and 'command'")

            # Check URL format
            if has_url:
                url = server_config["url"]
                if not url.startswith("https://"):
                    issues.append(f"WARNING: [{name}] URL should use HTTPS")

                if "<workspace>" in url or "<" in url:
                    issues.append(
                        f"ERROR: [{name}] URL contains placeholder that needs replacement"
                    )

            # Check environment variables
            if "env" in server_config:
                env = server_config["env"]
                for key, value in env.items():
                    if key == "DATABRICKS_TOKEN":
                        if isinstance(value, str) and re.match(
                            r"^dapi[a-zA-Z0-9]{32,}$", value
                        ):
                            issues.append(
                                f"ERROR: [{name}] Hardcoded token in configuration"
                            )

        return issues

    @staticmethod
    def merge_configs(*configs: dict) -> dict:
        """
        Merge multiple MCP configurations.

        Later configs override earlier ones for the same server name.
        """
        result = {"mcpServers": {}}

        for config in configs:
            if "mcpServers" in config:
                result["mcpServers"].update(config["mcpServers"])

        return result

    @staticmethod
    def split_by_environment(
        config: dict,
        environments: list[str],
    ) -> dict[str, dict]:
        """
        Split a config into environment-specific versions.

        Args:
            config: Original MCP configuration.
            environments: List of environment names (dev, staging, prod).

        Returns:
            Dict mapping environment name to config.
        """
        results = {}

        for env in environments:
            env_config = {"mcpServers": {}}

            for name, server_config in config.get("mcpServers", {}).items():
                env_name = f"{name}-{env}"
                env_server = server_config.copy()

                # Update URL placeholders if present
                if "url" in env_server:
                    url = env_server["url"]
                    env_server["url"] = url.replace(
                        "<workspace>", f"<{env}-workspace>"
                    )

                env_config["mcpServers"][env_name] = env_server

            results[env] = env_config

        return results

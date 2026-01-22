"""
MCP Configuration Generator

Generate properly structured MCP server configurations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class MCPServerConfig:
    """Configuration for a single MCP server."""

    name: str
    url: str | None = None
    command: str | None = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class MCPConfigGenerator:
    """
    Generate MCP configuration files for Databricks integration.

    Supports multiple clients:
    - Claude Desktop
    - Cursor
    - Custom applications
    """

    workspace_host: str
    catalog: str | None = None
    schema: str | None = None
    genie_space_id: str | None = None

    def generate_claude_desktop(
        self,
        *,
        include_sql: bool = True,
        include_genie: bool = False,
        include_vector_search: bool = False,
        include_functions: bool = False,
    ) -> str:
        """
        Generate Claude Desktop MCP configuration.

        Returns JSON string for claude_desktop_config.json.
        """
        servers: dict[str, dict] = {}

        if include_sql:
            servers["databricks-sql"] = {
                "command": "npx",
                "args": ["databricks-mcp-server"],
                "env": {
                    "DATABRICKS_HOST": self.workspace_host,
                    "DATABRICKS_TOKEN": "${DATABRICKS_TOKEN}",
                },
            }

        if include_genie and self.genie_space_id:
            servers["databricks-genie"] = {
                "url": f"{self.workspace_host}/api/2.0/mcp/genie/{self.genie_space_id}",
            }

        if include_vector_search and self.catalog and self.schema:
            servers["databricks-vector-search"] = {
                "url": f"{self.workspace_host}/api/2.0/mcp/vector-search/{self.catalog}/{self.schema}",
            }

        if include_functions and self.catalog and self.schema:
            servers["databricks-uc-functions"] = {
                "url": f"{self.workspace_host}/api/2.0/mcp/functions/{self.catalog}/{self.schema}",
            }

        config = {"mcpServers": servers}
        return json.dumps(config, indent=2)

    def generate_url_based(
        self,
        servers: list[
            Literal["sql", "genie", "vector-search", "functions"]
        ],
    ) -> str:
        """
        Generate URL-based MCP configuration.

        For applications that connect via HTTP URLs.
        """
        mcp_servers: dict[str, dict] = {}

        for server in servers:
            if server == "sql":
                mcp_servers["databricks-sql"] = {
                    "url": f"{self.workspace_host}/api/2.0/mcp/sql",
                }
            elif server == "genie":
                if not self.genie_space_id:
                    msg = "genie_space_id required for Genie server"
                    raise ValueError(msg)
                mcp_servers["databricks-genie"] = {
                    "url": f"{self.workspace_host}/api/2.0/mcp/genie/{self.genie_space_id}",
                }
            elif server == "vector-search":
                if not self.catalog or not self.schema:
                    msg = "catalog and schema required for Vector Search server"
                    raise ValueError(msg)
                mcp_servers["databricks-vector-search"] = {
                    "url": f"{self.workspace_host}/api/2.0/mcp/vector-search/{self.catalog}/{self.schema}",
                }
            elif server == "functions":
                if not self.catalog or not self.schema:
                    msg = "catalog and schema required for Functions server"
                    raise ValueError(msg)
                mcp_servers["databricks-uc-functions"] = {
                    "url": f"{self.workspace_host}/api/2.0/mcp/functions/{self.catalog}/{self.schema}",
                }

        config = {"mcpServers": mcp_servers}
        return json.dumps(config, indent=2)

    def generate_multi_workspace(
        self,
        workspaces: dict[str, str],  # name -> host
        server_type: Literal["sql", "genie", "vector-search", "functions"] = "sql",
    ) -> str:
        """
        Generate configuration for multiple workspaces.

        Useful for dev/staging/prod setups.
        """
        mcp_servers: dict[str, dict] = {}

        for name, host in workspaces.items():
            server_name = f"databricks-{name}-{server_type}"

            if server_type == "sql":
                mcp_servers[server_name] = {
                    "url": f"{host}/api/2.0/mcp/sql",
                }
            elif server_type == "genie" and self.genie_space_id:
                mcp_servers[server_name] = {
                    "url": f"{host}/api/2.0/mcp/genie/{self.genie_space_id}",
                }
            elif server_type == "vector-search" and self.catalog and self.schema:
                mcp_servers[server_name] = {
                    "url": f"{host}/api/2.0/mcp/vector-search/{self.catalog}/{self.schema}",
                }
            elif server_type == "functions" and self.catalog and self.schema:
                mcp_servers[server_name] = {
                    "url": f"{host}/api/2.0/mcp/functions/{self.catalog}/{self.schema}",
                }

        config = {"mcpServers": mcp_servers}
        return json.dumps(config, indent=2)


def generate_env_file(
    workspace_host: str,
    token_placeholder: str = "your-token-here",
) -> str:
    """Generate .env file content for Databricks configuration."""
    return f"""\
# Databricks Configuration
# Add this file to .gitignore!

DATABRICKS_HOST={workspace_host}
DATABRICKS_TOKEN={token_placeholder}

# Optional: Profile for databricks-cli
# DATABRICKS_CONFIG_PROFILE=default
"""


def generate_databrickscfg(
    profiles: dict[str, str],  # name -> host
    default_profile: str | None = None,
) -> str:
    """
    Generate ~/.databrickscfg content.

    Args:
        profiles: Mapping of profile name to workspace host.
        default_profile: Which profile to use as DEFAULT.
    """
    lines = []

    for name, host in profiles.items():
        section_name = "DEFAULT" if name == default_profile else name
        lines.extend(
            [
                f"[{section_name}]",
                f"host = {host}",
                "# token = use DATABRICKS_TOKEN env var or oauth",
                "",
            ]
        )

    return "\n".join(lines)

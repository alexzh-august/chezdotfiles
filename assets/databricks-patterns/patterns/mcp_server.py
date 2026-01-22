"""
MCP (Model Context Protocol) Server Pattern Definitions

Configuration patterns for Databricks MCP servers:
- Managed MCP Servers
- External MCP Servers
- Custom MCP Servers
"""

from typing import TypedDict


class Pattern(TypedDict):
    id: str
    severity: str
    category: str
    description: str
    do_pattern: str | None
    dont_pattern: str | None
    regex: str | None
    fix_suggestion: str | None


MCP_SERVER_PATTERNS: list[Pattern] = [
    # URL Configuration Patterns
    {
        "id": "MCP001",
        "severity": "error",
        "category": "url_format",
        "description": "Use correct MCP server URL format for Vector Search",
        "do_pattern": "https://<workspace>/api/2.0/mcp/vector-search/{catalog}/{schema}",
        "dont_pattern": "Incomplete or malformed URLs",
        "regex": r"mcp/vector-search(?!/[\w-]+/[\w-]+)",
        "fix_suggestion": "Include catalog and schema in URL: /mcp/vector-search/catalog/schema",
    },
    {
        "id": "MCP002",
        "severity": "error",
        "category": "url_format",
        "description": "Use correct MCP server URL format for Genie Space",
        "do_pattern": "https://<workspace>/api/2.0/mcp/genie/{genie_space_id}",
        "dont_pattern": "Missing genie_space_id in URL",
        "regex": r"mcp/genie(?!/[\w-]+)",
        "fix_suggestion": "Include genie_space_id in URL: /mcp/genie/<space_id>",
    },
    {
        "id": "MCP003",
        "severity": "error",
        "category": "url_format",
        "description": "Use correct MCP server URL format for Unity Catalog Functions",
        "do_pattern": "https://<workspace>/api/2.0/mcp/functions/{catalog}/{schema}",
        "dont_pattern": "Missing catalog/schema in functions URL",
        "regex": r"mcp/functions(?!/[\w-]+/[\w-]+)",
        "fix_suggestion": "Include catalog and schema: /mcp/functions/catalog/schema",
    },
    # Configuration Structure
    {
        "id": "MCP004",
        "severity": "error",
        "category": "config",
        "description": "MCP server config must have 'mcpServers' key",
        "do_pattern": '{"mcpServers": {"server-name": {...}}}',
        "dont_pattern": '{"servers": {...}} or flat structure',
        "regex": r'"(?:servers|mcp_servers|MCP_SERVERS)":\s*\{',
        "fix_suggestion": 'Use "mcpServers" as the top-level key',
    },
    {
        "id": "MCP005",
        "severity": "warning",
        "category": "config",
        "description": "Use descriptive MCP server names",
        "do_pattern": '"databricks-sql", "databricks-genie", "databricks-vector-search"',
        "dont_pattern": '"server1", "mcp", "default"',
        "regex": r'"mcpServers":\s*\{\s*"(?:server\d*|mcp|default|test)"',
        "fix_suggestion": "Use descriptive names like 'databricks-sql' or 'databricks-genie'",
    },
    # Environment Variables
    {
        "id": "MCP006",
        "severity": "error",
        "category": "security",
        "description": "Never hardcode tokens in MCP configuration",
        "do_pattern": '"DATABRICKS_TOKEN": "${DATABRICKS_TOKEN}" or env reference',
        "dont_pattern": '"DATABRICKS_TOKEN": "dapi123..."',
        "regex": r'"DATABRICKS_TOKEN":\s*"dapi[a-z0-9]+',
        "fix_suggestion": "Use environment variable reference or secret manager",
    },
    {
        "id": "MCP007",
        "severity": "warning",
        "category": "config",
        "description": "Include workspace host in environment config",
        "do_pattern": '"env": {"DATABRICKS_HOST": "https://workspace.cloud.databricks.com"}',
        "dont_pattern": "Hardcoding host in URL without env config",
        "regex": None,
        "fix_suggestion": "Set DATABRICKS_HOST in env section for flexibility",
    },
    # Claude Desktop Integration
    {
        "id": "MCP008",
        "severity": "info",
        "category": "integration",
        "description": "Use npx for Claude Desktop MCP server",
        "do_pattern": '"command": "npx", "args": ["databricks-mcp-server"]',
        "dont_pattern": "Direct node execution of MCP server",
        "regex": r'"command":\s*"node".*databricks-mcp',
        "fix_suggestion": 'Use npx: "command": "npx", "args": ["databricks-mcp-server"]',
    },
    # Server Selection
    {
        "id": "MCP009",
        "severity": "info",
        "category": "selection",
        "description": "Use Genie for read-only queries and chatbots",
        "do_pattern": "Genie MCP server for business user queries",
        "dont_pattern": "Using DBSQL for simple read-only chatbot queries",
        "regex": None,
        "fix_suggestion": "For read-only analysis, prefer Genie over DBSQL",
    },
    {
        "id": "MCP010",
        "severity": "info",
        "category": "selection",
        "description": "Use DBSQL for data pipeline authoring with AI tools",
        "do_pattern": "DBSQL MCP server for data engineering tasks",
        "dont_pattern": "Using Genie for complex data transformations",
        "regex": None,
        "fix_suggestion": "For data pipeline authoring, use DBSQL MCP server",
    },
    # Multi-Server Configuration
    {
        "id": "MCP011",
        "severity": "warning",
        "category": "config",
        "description": "Configure multiple MCP servers for different use cases",
        "do_pattern": "Separate configs for sql, genie, vector-search, functions",
        "dont_pattern": "Single monolithic MCP server for all operations",
        "regex": None,
        "fix_suggestion": "Use specialized MCP servers for each capability",
    },
    # Authentication
    {
        "id": "MCP012",
        "severity": "warning",
        "category": "auth",
        "description": "Prefer OAuth over PAT for MCP authentication",
        "do_pattern": "OAuth authentication for external clients",
        "dont_pattern": "PAT tokens in plain config files",
        "regex": r'"DATABRICKS_TOKEN":\s*"[^$]',
        "fix_suggestion": "Use OAuth for better security, or reference token from env",
    },
]

# MCP Server URL Templates
MCP_URL_TEMPLATES = {
    "vector_search": "https://{workspace}/api/2.0/mcp/vector-search/{catalog}/{schema}",
    "genie": "https://{workspace}/api/2.0/mcp/genie/{genie_space_id}",
    "functions": "https://{workspace}/api/2.0/mcp/functions/{catalog}/{schema}",
    "sql": "https://{workspace}/api/2.0/mcp/sql",
}

# Example Configuration Templates
MCP_CONFIG_TEMPLATES = {
    "claude_desktop": {
        "mcpServers": {
            "databricks-sql": {
                "command": "npx",
                "args": ["databricks-mcp-server"],
                "env": {
                    "DATABRICKS_HOST": "https://your-workspace.cloud.databricks.com",
                    "DATABRICKS_TOKEN": "your-token",
                },
            }
        }
    },
    "multi_server": {
        "mcpServers": {
            "databricks-sql": {
                "url": "https://<workspace>/api/2.0/mcp/sql",
            },
            "databricks-genie": {
                "url": "https://<workspace>/api/2.0/mcp/genie/<space_id>",
            },
            "databricks-vector-search": {
                "url": "https://<workspace>/api/2.0/mcp/vector-search/catalog/schema",
            },
            "databricks-uc-functions": {
                "url": "https://<workspace>/api/2.0/mcp/functions/catalog/schema",
            },
        }
    },
}

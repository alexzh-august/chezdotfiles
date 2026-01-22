"""
Databricks Code Pattern Definitions

DO/DON'T patterns organized by package for:
- Unity Catalog
- MCP Server Configuration
- SQL Execution
- Authentication
- Vector Search
- Genie AI Assistant
"""

from .unity_catalog import UNITY_CATALOG_PATTERNS
from .mcp_server import MCP_SERVER_PATTERNS
from .sql_execution import SQL_EXECUTION_PATTERNS
from .authentication import AUTHENTICATION_PATTERNS
from .vector_search import VECTOR_SEARCH_PATTERNS
from .genie import GENIE_PATTERNS

ALL_PATTERNS = {
    "unity_catalog": UNITY_CATALOG_PATTERNS,
    "mcp_server": MCP_SERVER_PATTERNS,
    "sql_execution": SQL_EXECUTION_PATTERNS,
    "authentication": AUTHENTICATION_PATTERNS,
    "vector_search": VECTOR_SEARCH_PATTERNS,
    "genie": GENIE_PATTERNS,
}

__all__ = [
    "UNITY_CATALOG_PATTERNS",
    "MCP_SERVER_PATTERNS",
    "SQL_EXECUTION_PATTERNS",
    "AUTHENTICATION_PATTERNS",
    "VECTOR_SEARCH_PATTERNS",
    "GENIE_PATTERNS",
    "ALL_PATTERNS",
]

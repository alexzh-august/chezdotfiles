"""
Genie AI Assistant Pattern Definitions

Best practices for Databricks Genie:
- Natural language queries
- Chatbot integration
- Multi-turn conversations
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


GENIE_PATTERNS: list[Pattern] = [
    # Use Case Patterns
    {
        "id": "GENIE001",
        "severity": "info",
        "category": "use_case",
        "description": "Use Genie for read-only queries and chatbots",
        "do_pattern": "Natural language data analysis, business user queries",
        "dont_pattern": "Data pipeline authoring or complex transformations",
        "regex": None,
        "fix_suggestion": "Genie is best for read-only analysis, use DBSQL for writes",
    },
    {
        "id": "GENIE002",
        "severity": "warning",
        "category": "use_case",
        "description": "Use DBSQL instead of Genie for data modifications",
        "do_pattern": "DBSQL MCP for INSERT, UPDATE, DELETE operations",
        "dont_pattern": "Attempting data modifications through Genie",
        "regex": None,
        "fix_suggestion": "Configure DBSQL MCP server for write operations",
    },
    # Genie Space Configuration
    {
        "id": "GENIE003",
        "severity": "error",
        "category": "config",
        "description": "Genie URL must include genie_space_id",
        "do_pattern": "/api/2.0/mcp/genie/{genie_space_id}",
        "dont_pattern": "/api/2.0/mcp/genie without space ID",
        "regex": r"mcp/genie/?(?:\s*['\"]|$)",
        "fix_suggestion": "Include genie_space_id in the MCP server URL",
    },
    {
        "id": "GENIE004",
        "severity": "info",
        "category": "config",
        "description": "Create focused Genie spaces per domain",
        "do_pattern": "Separate spaces for sales, marketing, ops data",
        "dont_pattern": "Single Genie space for all company data",
        "regex": None,
        "fix_suggestion": "Create domain-specific Genie spaces for better results",
    },
    # Conversation Patterns
    {
        "id": "GENIE005",
        "severity": "warning",
        "category": "conversation",
        "description": "MCP Genie server doesn't maintain conversation history",
        "do_pattern": "Multi-agent system for conversational context",
        "dont_pattern": "Relying on MCP server for multi-turn memory",
        "regex": None,
        "fix_suggestion": "Implement conversation history in your application layer",
    },
    {
        "id": "GENIE006",
        "severity": "info",
        "category": "conversation",
        "description": "Provide context in each query for better results",
        "do_pattern": 'Include relevant context: "For Q4 2024 sales data..."',
        "dont_pattern": 'Vague queries: "Show me the data"',
        "regex": None,
        "fix_suggestion": "Include time ranges, dimensions, and context in queries",
    },
    # Query Optimization
    {
        "id": "GENIE007",
        "severity": "info",
        "category": "query",
        "description": "Use specific terminology matching your data model",
        "do_pattern": 'Use column/table names: "total_revenue by region"',
        "dont_pattern": 'Ambiguous terms: "sales numbers for areas"',
        "regex": None,
        "fix_suggestion": "Use exact field names from your data model",
    },
    {
        "id": "GENIE008",
        "severity": "warning",
        "category": "query",
        "description": "Request formatted output for better parsing",
        "do_pattern": '"Show results as a table with columns X, Y, Z"',
        "dont_pattern": "Unstructured output for programmatic use",
        "regex": None,
        "fix_suggestion": "Specify output format requirements in queries",
    },
    # Integration Patterns
    {
        "id": "GENIE009",
        "severity": "info",
        "category": "integration",
        "description": "Validate Genie-generated SQL before modification use",
        "do_pattern": "Review SQL output, use for read-only insights",
        "dont_pattern": "Blindly executing Genie SQL for data modifications",
        "regex": None,
        "fix_suggestion": "Treat Genie output as suggestions requiring validation",
    },
    {
        "id": "GENIE010",
        "severity": "warning",
        "category": "integration",
        "description": "Handle Genie errors gracefully in applications",
        "do_pattern": "Fallback messages when Genie can't answer",
        "dont_pattern": "Exposing raw error messages to users",
        "regex": None,
        "fix_suggestion": "Implement user-friendly error handling",
    },
    # SQL Warehouse
    {
        "id": "GENIE011",
        "severity": "info",
        "category": "compute",
        "description": "Genie uses Serverless SQL compute",
        "do_pattern": "Budget for serverless SQL usage",
        "dont_pattern": "Assuming fixed compute costs",
        "regex": None,
        "fix_suggestion": "Monitor serverless SQL consumption from Genie queries",
    },
    {
        "id": "GENIE012",
        "severity": "warning",
        "category": "compute",
        "description": "Set query limits for cost control",
        "do_pattern": "Implement query timeouts and row limits",
        "dont_pattern": "Unbounded queries through Genie",
        "regex": None,
        "fix_suggestion": "Configure query governors for Genie spaces",
    },
    # Testing
    {
        "id": "GENIE013",
        "severity": "info",
        "category": "testing",
        "description": "Test Genie integration in AI Playground first",
        "do_pattern": "Validate queries in Playground before integration",
        "dont_pattern": "Production-first Genie integration",
        "regex": None,
        "fix_suggestion": "Use AI Playground to test MCP server interactions",
    },
    {
        "id": "GENIE014",
        "severity": "warning",
        "category": "testing",
        "description": "Create test cases for common query patterns",
        "do_pattern": "Document expected queries and outputs",
        "dont_pattern": "Ad-hoc testing without coverage",
        "regex": None,
        "fix_suggestion": "Build a test suite for Genie query patterns",
    },
]

# Genie Usage Templates
GENIE_TEMPLATES = {
    "mcp_config": """
# MCP Server configuration for Genie
{
    "mcpServers": {
        "databricks-genie": {
            "url": "https://<workspace>/api/2.0/mcp/genie/<genie_space_id>"
        }
    }
}
""",
    "query_examples": {
        "good": [
            "Show me total_revenue by region for Q4 2024",
            "What were the top 10 products by unit_sales last month?",
            "Compare customer_count between East and West regions",
            "Calculate average order_value by customer_segment for 2024",
        ],
        "bad": [
            "Show me the data",
            "What are the numbers?",
            "Update the sales figures",
            "Delete old records",
        ],
    },
    "multi_agent_context": """
# DO: Implement conversation context in multi-agent system
class GenieAgent:
    def __init__(self, genie_client):
        self.client = genie_client
        self.conversation_history = []

    def query(self, user_message: str) -> str:
        # Build context from history
        context = self._build_context()

        # Include context in query
        enhanced_query = f"{context}\\n\\nUser: {user_message}"

        response = self.client.query(enhanced_query)

        # Store for future context
        self.conversation_history.append({
            "user": user_message,
            "assistant": response
        })

        return response

    def _build_context(self) -> str:
        if not self.conversation_history:
            return ""
        recent = self.conversation_history[-3:]  # Last 3 exchanges
        return "\\n".join([
            f"User: {h['user']}\\nAssistant: {h['assistant']}"
            for h in recent
        ])
""",
}

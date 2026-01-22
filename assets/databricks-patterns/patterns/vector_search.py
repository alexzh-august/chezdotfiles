"""
Vector Search Pattern Definitions

Best practices for Databricks Vector Search:
- Index management
- Query patterns
- Embedding handling
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


VECTOR_SEARCH_PATTERNS: list[Pattern] = [
    # Index Patterns
    {
        "id": "VS001",
        "severity": "error",
        "category": "index",
        "description": "Use Databricks-managed embeddings for MCP integration",
        "do_pattern": "Configure index with Databricks embedding model",
        "dont_pattern": "External embeddings with MCP Vector Search server",
        "regex": None,
        "fix_suggestion": "MCP Vector Search only supports Databricks-managed embeddings",
    },
    {
        "id": "VS002",
        "severity": "warning",
        "category": "index",
        "description": "Choose appropriate index type for use case",
        "do_pattern": "Delta Sync for auto-updating, Direct Vector for custom",
        "dont_pattern": "Using wrong index type for data pattern",
        "regex": None,
        "fix_suggestion": "Use Delta Sync Index for tables, Direct Vector for custom embeddings",
    },
    {
        "id": "VS003",
        "severity": "info",
        "category": "index",
        "description": "Set appropriate sync schedule for Delta Sync indexes",
        "do_pattern": "Configure sync based on data freshness requirements",
        "dont_pattern": "Default continuous sync for static data",
        "regex": None,
        "fix_suggestion": "Adjust sync frequency based on data update patterns",
    },
    # Query Patterns
    {
        "id": "VS004",
        "severity": "warning",
        "category": "query",
        "description": "Limit vector search results appropriately",
        "do_pattern": "num_results=10 or appropriate limit",
        "dont_pattern": "Requesting hundreds of results from vector search",
        "regex": r"num_results\s*=\s*(?:[5-9]\d{2,}|\d{4,})",
        "fix_suggestion": "Limit results to necessary count, typically <100",
    },
    {
        "id": "VS005",
        "severity": "info",
        "category": "query",
        "description": "Use filters to narrow vector search scope",
        "do_pattern": 'filters={"column": "value"} for scoped search',
        "dont_pattern": "Unfiltered vector search on large indexes",
        "regex": None,
        "fix_suggestion": "Add metadata filters to improve search relevance",
    },
    {
        "id": "VS006",
        "severity": "warning",
        "category": "query",
        "description": "Set similarity threshold for quality results",
        "do_pattern": "score_threshold=0.7 or appropriate cutoff",
        "dont_pattern": "Accepting all results regardless of similarity",
        "regex": None,
        "fix_suggestion": "Filter results by similarity score threshold",
    },
    # Endpoint Patterns
    {
        "id": "VS007",
        "severity": "error",
        "category": "endpoint",
        "description": "Use endpoint URL format from catalog/schema",
        "do_pattern": "/api/2.0/mcp/vector-search/{catalog}/{schema}",
        "dont_pattern": "Hardcoded endpoint IDs",
        "regex": r"vector-search/[a-f0-9-]{36}",
        "fix_suggestion": "Use catalog.schema path format for endpoints",
    },
    {
        "id": "VS008",
        "severity": "info",
        "category": "endpoint",
        "description": "Monitor endpoint metrics for performance",
        "do_pattern": "Check endpoint metrics regularly",
        "dont_pattern": "Ignoring endpoint performance metrics",
        "regex": None,
        "fix_suggestion": "Monitor query latency and error rates via endpoint metrics",
    },
    # RAG Patterns
    {
        "id": "VS009",
        "severity": "info",
        "category": "rag",
        "description": "Combine vector search with Unity Catalog governance",
        "do_pattern": "Access control via Unity Catalog permissions",
        "dont_pattern": "Application-level access control bypassing UC",
        "regex": None,
        "fix_suggestion": "Rely on Unity Catalog for vector data governance",
    },
    {
        "id": "VS010",
        "severity": "warning",
        "category": "rag",
        "description": "Include metadata columns for context enrichment",
        "do_pattern": "columns=['text', 'source', 'timestamp']",
        "dont_pattern": "Only returning embedding text without metadata",
        "regex": None,
        "fix_suggestion": "Include relevant metadata columns in query results",
    },
    # Data Patterns
    {
        "id": "VS011",
        "severity": "warning",
        "category": "data",
        "description": "Chunk documents appropriately for embedding",
        "do_pattern": "Consistent chunk sizes (500-1000 tokens)",
        "dont_pattern": "Full documents or inconsistent chunk sizes",
        "regex": None,
        "fix_suggestion": "Implement consistent chunking strategy before indexing",
    },
    {
        "id": "VS012",
        "severity": "info",
        "category": "data",
        "description": "Store source references for retrieved chunks",
        "do_pattern": "Include document_id, chunk_index, source_url",
        "dont_pattern": "Chunks without provenance information",
        "regex": None,
        "fix_suggestion": "Track chunk sources for citation and debugging",
    },
    # Upsert Patterns
    {
        "id": "VS013",
        "severity": "warning",
        "category": "upsert",
        "description": "Batch upserts for efficiency",
        "do_pattern": "upsert_data(records=[...]) with batches",
        "dont_pattern": "Individual upsert calls per record",
        "regex": r"for\s+\w+\s+in\s+\w+:.*upsert",
        "fix_suggestion": "Batch records and upsert in groups",
    },
    {
        "id": "VS014",
        "severity": "info",
        "category": "upsert",
        "description": "Use idempotent IDs for upsert operations",
        "do_pattern": "Deterministic ID generation for deduplication",
        "dont_pattern": "Random UUIDs causing duplicate entries",
        "regex": None,
        "fix_suggestion": "Generate IDs from content hash for idempotent upserts",
    },
]

# Vector Search Query Templates
VECTOR_SEARCH_TEMPLATES = {
    "basic_query": """
# DO: Basic vector search with limits
results = index.similarity_search(
    query_text="user question",
    columns=["text", "source", "metadata"],
    num_results=10
)
""",
    "filtered_query": """
# DO: Vector search with filters
results = index.similarity_search(
    query_text="user question",
    columns=["text", "source"],
    filters={"category": "documentation", "status": "published"},
    num_results=10,
    score_threshold=0.7
)
""",
    "batch_upsert": """
# DO: Batch upsert for efficiency
BATCH_SIZE = 100
records = [...]

for i in range(0, len(records), BATCH_SIZE):
    batch = records[i:i + BATCH_SIZE]
    index.upsert(data=batch)
""",
    "mcp_config": """
# MCP Server configuration for Vector Search
{
    "mcpServers": {
        "databricks-vector-search": {
            "url": "https://<workspace>/api/2.0/mcp/vector-search/catalog/schema"
        }
    }
}
""",
}

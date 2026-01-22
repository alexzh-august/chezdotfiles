"""
Unity Catalog Pattern Definitions

Three-level namespace: catalog.schema.table
"""

from typing import TypedDict


class Pattern(TypedDict):
    id: str
    severity: str  # "error", "warning", "info"
    category: str
    description: str
    do_pattern: str | None
    dont_pattern: str | None
    regex: str | None
    fix_suggestion: str | None


UNITY_CATALOG_PATTERNS: list[Pattern] = [
    # Namespace Patterns
    {
        "id": "UC001",
        "severity": "error",
        "category": "namespace",
        "description": "Use fully qualified three-level namespace for table references",
        "do_pattern": "catalog.schema.table",
        "dont_pattern": "schema.table or just table",
        "regex": r"(?<!\.)\b(?:SELECT|FROM|JOIN|INTO|UPDATE|DELETE\s+FROM)\s+(?![\w]+\.[\w]+\.[\w]+\b)[\w]+(?:\.[\w]+)?(?!\.\w)",
        "fix_suggestion": "Use fully qualified name: catalog_name.schema_name.table_name",
    },
    {
        "id": "UC002",
        "severity": "warning",
        "category": "namespace",
        "description": "Escape special characters in identifiers with backticks",
        "do_pattern": "catalog.schema.`special-table`",
        "dont_pattern": "catalog.schema.special-table",
        "regex": r"\b[\w]+\.[\w]+\.[\w]*[-@#$%][\w-]*(?!`)",
        "fix_suggestion": "Wrap identifier with backticks: `special-table`",
    },
    # Catalog Operations
    {
        "id": "UC003",
        "severity": "info",
        "category": "discovery",
        "description": "Use SHOW CATALOGS to list available catalogs",
        "do_pattern": "SHOW CATALOGS;",
        "dont_pattern": "Hardcoding catalog names without verification",
        "regex": None,
        "fix_suggestion": "Run SHOW CATALOGS to discover available catalogs",
    },
    {
        "id": "UC004",
        "severity": "info",
        "category": "discovery",
        "description": "Use SHOW SCHEMAS IN catalog to list schemas",
        "do_pattern": "SHOW SCHEMAS IN catalog_name;",
        "dont_pattern": "SELECT * FROM information_schema for schema discovery",
        "regex": None,
        "fix_suggestion": "Use SHOW SCHEMAS IN catalog_name",
    },
    {
        "id": "UC005",
        "severity": "info",
        "category": "discovery",
        "description": "Use DESCRIBE TABLE for table metadata",
        "do_pattern": "DESCRIBE TABLE catalog.schema.table;",
        "dont_pattern": "Inferring schema from SELECT * LIMIT 1",
        "regex": r"SELECT\s+\*\s+FROM\s+[\w.`]+\s+LIMIT\s+1",
        "fix_suggestion": "Use DESCRIBE TABLE for schema discovery",
    },
    # Governance Patterns
    {
        "id": "UC006",
        "severity": "error",
        "category": "governance",
        "description": "Never bypass Unity Catalog permissions",
        "do_pattern": "Rely on UC permissions for access control",
        "dont_pattern": "Direct file access bypassing catalog",
        "regex": r"dbutils\.fs\.(ls|cp|mv|rm)\s*\(['\"](?:s3|abfss|gs)://",
        "fix_suggestion": "Access data through Unity Catalog tables, not direct file paths",
    },
    {
        "id": "UC007",
        "severity": "warning",
        "category": "governance",
        "description": "Use external locations registered in Unity Catalog",
        "do_pattern": "spark.read.table('catalog.schema.table')",
        "dont_pattern": "spark.read.parquet('s3://bucket/path')",
        "regex": r"spark\.read\.(?:parquet|csv|json|orc)\s*\(['\"](?:s3|abfss|gs)://",
        "fix_suggestion": "Register external location in UC and use catalog reference",
    },
    # Volume Patterns
    {
        "id": "UC008",
        "severity": "info",
        "category": "volumes",
        "description": "Use Unity Catalog Volumes for file storage",
        "do_pattern": "/Volumes/catalog/schema/volume/path",
        "dont_pattern": "/dbfs/mnt/path or direct cloud paths",
        "regex": r"['\"]\/dbfs\/mnt\/",
        "fix_suggestion": "Use UC Volumes: /Volumes/catalog/schema/volume_name/",
    },
    # Model Registry Patterns
    {
        "id": "UC009",
        "severity": "warning",
        "category": "mlflow",
        "description": "Register models in Unity Catalog model registry",
        "do_pattern": "mlflow.register_model('runs:/xxx', 'catalog.schema.model')",
        "dont_pattern": "mlflow.register_model('runs:/xxx', 'model_name')",
        "regex": r"mlflow\.register_model\s*\([^,]+,\s*['\"](?![\w]+\.[\w]+\.)",
        "fix_suggestion": "Use three-level namespace for model: catalog.schema.model_name",
    },
    # Function Patterns
    {
        "id": "UC010",
        "severity": "info",
        "category": "functions",
        "description": "Reference UDFs with full catalog path",
        "do_pattern": "SELECT catalog.schema.my_function(col)",
        "dont_pattern": "SELECT my_function(col)",
        "regex": r"(?:SELECT|WHERE|HAVING).*?(?<!\.)(?<!\w\.)\b(?!CURRENT_|DATE|TIME|NOW|COALESCE|CONCAT|UPPER|LOWER|TRIM|LENGTH|SUBSTRING|ROUND|ABS|SUM|COUNT|AVG|MAX|MIN|FIRST|LAST|COLLECT)([a-z_][a-z0-9_]*)\s*\(",
        "fix_suggestion": "Use fully qualified function name: catalog.schema.function_name()",
    },
]

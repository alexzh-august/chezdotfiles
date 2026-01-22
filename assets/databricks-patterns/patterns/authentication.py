"""
Authentication Pattern Definitions

Best practices for Databricks authentication:
- OAuth (Recommended)
- Personal Access Token (PAT)
- Service Principal
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


AUTHENTICATION_PATTERNS: list[Pattern] = [
    # OAuth Patterns
    {
        "id": "AUTH001",
        "severity": "warning",
        "category": "oauth",
        "description": "Prefer OAuth over PAT for external clients",
        "do_pattern": "Use OAuth for Cursor, Claude Desktop, and other clients",
        "dont_pattern": "Using PAT for external client authentication",
        "regex": None,
        "fix_suggestion": "Configure OAuth authentication for better security",
    },
    {
        "id": "AUTH002",
        "severity": "info",
        "category": "oauth",
        "description": "Use OIDC tokens for CI/CD pipelines",
        "do_pattern": "GitHub Actions OIDC with Databricks",
        "dont_pattern": "Storing PATs in CI/CD secrets",
        "regex": r"DATABRICKS_TOKEN.*secrets\.",
        "fix_suggestion": "Use OIDC token federation for CI/CD authentication",
    },
    # PAT Patterns
    {
        "id": "AUTH003",
        "severity": "error",
        "category": "pat",
        "description": "Never hardcode PAT tokens in source code",
        "do_pattern": 'os.environ.get("DATABRICKS_TOKEN")',
        "dont_pattern": 'token = "dapi..."',
        "regex": r"['\"]dapi[a-zA-Z0-9]{32,}['\"]",
        "fix_suggestion": "Use environment variables or secret managers",
    },
    {
        "id": "AUTH004",
        "severity": "error",
        "category": "pat",
        "description": "Never commit PAT tokens to version control",
        "do_pattern": "Use .env files with .gitignore",
        "dont_pattern": "Token in committed config files",
        "regex": r"dapi[a-zA-Z0-9]{32,}",
        "fix_suggestion": "Add token files to .gitignore, use secret manager",
    },
    {
        "id": "AUTH005",
        "severity": "warning",
        "category": "pat",
        "description": "Set expiration dates for PAT tokens",
        "do_pattern": "Create PATs with 90-day or shorter expiration",
        "dont_pattern": "PATs with no expiration",
        "regex": None,
        "fix_suggestion": "Set token expiration and implement rotation",
    },
    # Environment Variables
    {
        "id": "AUTH006",
        "severity": "warning",
        "category": "env",
        "description": "Use standard environment variable names",
        "do_pattern": "DATABRICKS_HOST, DATABRICKS_TOKEN",
        "dont_pattern": "DBX_URL, DB_TOKEN, custom names",
        "regex": r"(?:DBX_|DB_|DBRICKS_)(?:URL|HOST|TOKEN)",
        "fix_suggestion": "Use DATABRICKS_HOST and DATABRICKS_TOKEN",
    },
    {
        "id": "AUTH007",
        "severity": "error",
        "category": "env",
        "description": "Validate environment variables before use",
        "do_pattern": 'host = os.environ["DATABRICKS_HOST"] with error handling',
        "dont_pattern": 'host = os.environ.get("DATABRICKS_HOST", "")',
        "regex": r"environ\.get\s*\(\s*['\"]DATABRICKS_(?:HOST|TOKEN)['\"],\s*['\"]['\"]",
        "fix_suggestion": "Require env vars or provide clear error messages",
    },
    # Service Principal
    {
        "id": "AUTH008",
        "severity": "info",
        "category": "service_principal",
        "description": "Use service principals for production deployments",
        "do_pattern": "Service principal with scoped permissions",
        "dont_pattern": "Personal accounts in production",
        "regex": None,
        "fix_suggestion": "Configure service principal for automated workloads",
    },
    {
        "id": "AUTH009",
        "severity": "warning",
        "category": "service_principal",
        "description": "Apply least privilege to service principals",
        "do_pattern": "Grant only required permissions per use case",
        "dont_pattern": "Admin-level service principal permissions",
        "regex": None,
        "fix_suggestion": "Scope service principal to specific catalogs/schemas",
    },
    # Configuration Files
    {
        "id": "AUTH010",
        "severity": "error",
        "category": "config",
        "description": "Use .databrickscfg for local development",
        "do_pattern": "~/.databrickscfg with profile support",
        "dont_pattern": "Inline credentials in scripts",
        "regex": None,
        "fix_suggestion": "Store credentials in ~/.databrickscfg profiles",
    },
    {
        "id": "AUTH011",
        "severity": "warning",
        "category": "config",
        "description": "Use profile names for multi-workspace access",
        "do_pattern": "[workspace-dev], [workspace-prod] profiles",
        "dont_pattern": "Single [DEFAULT] profile for all workspaces",
        "regex": None,
        "fix_suggestion": "Configure named profiles per workspace",
    },
    # SDK Authentication
    {
        "id": "AUTH012",
        "severity": "info",
        "category": "sdk",
        "description": "Use SDK default authentication chain",
        "do_pattern": "WorkspaceClient() with auto-discovery",
        "dont_pattern": "Manually passing token to client",
        "regex": r"WorkspaceClient\s*\(\s*.*token\s*=",
        "fix_suggestion": "Let SDK auto-discover credentials from env/config",
    },
    {
        "id": "AUTH013",
        "severity": "warning",
        "category": "sdk",
        "description": "Initialize client once and reuse",
        "do_pattern": "Global or module-level client instance",
        "dont_pattern": "Creating new client per request",
        "regex": r"def\s+\w+.*:\s*\n.*WorkspaceClient\s*\(",
        "fix_suggestion": "Create client once at module level and reuse",
    },
    # Secret Management
    {
        "id": "AUTH014",
        "severity": "error",
        "category": "secrets",
        "description": "Use Databricks secrets scope for sensitive values",
        "do_pattern": "dbutils.secrets.get(scope, key)",
        "dont_pattern": "Hardcoded secrets in notebooks",
        "regex": r"password\s*=\s*['\"][^'\"]+['\"]|api_key\s*=\s*['\"][^'\"]+['\"]",
        "fix_suggestion": "Store secrets in Databricks secret scope",
    },
    {
        "id": "AUTH015",
        "severity": "warning",
        "category": "secrets",
        "description": "Use key vault integration for enterprise secrets",
        "do_pattern": "Azure Key Vault or AWS Secrets Manager backed scope",
        "dont_pattern": "Databricks-managed secrets for production",
        "regex": None,
        "fix_suggestion": "Configure external secret backend for production",
    },
]

# Authentication Configuration Templates
AUTH_CONFIG_TEMPLATES = {
    "databrickscfg": """
# ~/.databrickscfg

[DEFAULT]
host = https://your-workspace.cloud.databricks.com

[dev]
host = https://dev-workspace.cloud.databricks.com
token = ${DATABRICKS_TOKEN_DEV}

[prod]
host = https://prod-workspace.cloud.databricks.com
# Use OAuth or service principal for prod
""",
    "env_file": """
# .env (add to .gitignore!)
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi...
""",
    "python_sdk": """
# DO: Let SDK auto-discover credentials
from databricks.sdk import WorkspaceClient

# SDK reads from env, ~/.databrickscfg, or Azure/AWS identity
client = WorkspaceClient()

# DON'T: Hardcode or pass credentials
# client = WorkspaceClient(host="...", token="...")  # Bad!
""",
}

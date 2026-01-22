# Research API Before Implementation

Deep research an API or data source before writing code using Parallel.ai.

## Instructions

1. **Web Research Phase** (use Parallel AI via bash)
   ```bash
   parallel-search "$ARGUMENTS API documentation best practices 2025"
   ```

   Look for:
   - Official documentation URLs
   - Rate limit information
   - Authentication patterns
   - Common implementation patterns

2. **Extract Official Docs** (if URL found)
   ```bash
   parallel-extract "https://docs.$ARGUMENTS.com" "Extract API authentication, rate limits, pagination, and code examples"
   ```

3. **Analyze Patterns**
   - Read extracted documentation
   - Identify authentication patterns (API key, OAuth, JWT)
   - Note rate limits and pagination strategies
   - Find example request/response structures
   - Check for SDKs or client libraries

4. **Generate Implementation Plan**
   Based on research, create:
   - List of required data models (Pydantic)
   - Fetcher interface design (async httpx)
   - Error handling strategy (retries, backoff)
   - Test plan (mocking, fixtures)

5. **Output Format**
   ```markdown
   ## API Research: $ARGUMENTS

   ### Authentication
   [Details from research]

   ### Rate Limits
   [Limits and strategies]

   ### Implementation Plan

   #### Models
   - Model 1: [description]
   - Model 2: [description]

   #### Fetcher
   ```python
   # Pseudocode for fetcher interface
   ```

   #### Tests
   - Test 1: [scenario]
   - Test 2: [scenario]

   ### Sources
   - [Source 1](url)
   - [Source 2](url)
   ```

## Environment Requirements

Requires `PARALLEL_API_KEY` environment variable set in ~/.zshrc:
```bash
export PARALLEL_API_KEY="your-api-key"
```

API/Source to research: $ARGUMENTS

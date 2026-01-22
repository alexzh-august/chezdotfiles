---
name: orch-start
description: Start a new parallel orchestration session
version: 1.0.0
triggers:
  - /orch-start
---

# Start Orchestration Session

Start a new parallel orchestration session with the specified request.

## Usage
```
/orch-start <request_description>
```

## Example
```
/orch-start Implement user authentication with JWT tokens
```

## Implementation

When invoked, execute:
```bash
mcp-cli call parallel-orchestrator/start_session '{"request": "<user_request>", "options": {"critics": 3, "tdd": true, "no_qa": false}}'
```

The response includes:
- `session_id`: Unique session identifier (e.g., `orch-20260109-123456`)
- `status`: "started"
- `message`: Confirmation message

After starting, suggest next steps:
1. Create a plan with `/orch-plan`
2. Spawn critics with `/orch-critic`

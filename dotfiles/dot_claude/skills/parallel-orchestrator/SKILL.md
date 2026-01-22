---
name: parallel-orchestrator
description: Parallel Orchestrator MCP - Start orchestration sessions, spawn critics, manage TDD workflow. Use when user says /orch, /orch-pre-start-analyze, /orch-start, /orch-end, /orch-status, /orch-plan, /orch-critic, /orch-task, /orch-tdd, /orch-qa, or /orch-event. Also use when implementing features with parallel critics, code review workflow, or TDD-based development.
---

# Parallel Orchestrator Commands

You have access to the Parallel Orchestrator MCP server for managing multi-phase implementation workflows with critics, TDD, and QA review.

## Available Commands

### Pre-Flight Analysis
- `/orch-pre-start-analyze` - Analyze codebase and gather context before starting

### Session Management
- `/orch-start` - Start a new orchestration session
- `/orch-end` - End the current session
- `/orch-status` - Get current session status
- `/orch-sessions` - List recent sessions

### Planning
- `/orch-plan` - Log an implementation plan
- `/orch-get-plan` - Retrieve the current plan

### Critics (Parallel Review)
- `/orch-critic` - Spawn a critic subagent (oop, tdd, packages)
- `/orch-critic-result` - Log critic results
- `/orch-synthesis` - Log synthesis of critic feedback

### Implementation (TDD)
- `/orch-task` - Log a new task
- `/orch-task-start` - Start a task with TDD phase
- `/orch-task-complete` - Complete a task
- `/orch-tdd` - Set TDD phase (RED/GREEN/REFACTOR)

### QA Review
- `/orch-qa` - Spawn QA review agent
- `/orch-qa-result` - Log QA results with score

### Utilities
- `/orch-event` - Log a custom event
- `/orch-events` - Get recent events
- `/orch-prompt` - Get a prompt template

## Command Handling

When the user invokes any `/orch-*` command, use the MCP tools via `mcp-cli`:

### /orch-pre-start-analyze [feature_description]
Analyze codebase and gather context before starting a workflow:
1. Use Task tool with `subagent_type=Explore` to analyze project structure
2. Search for related files and existing patterns
3. Identify potential impacts and considerations
4. Present structured analysis summary with recommendations
5. Suggest running `/orch-start` when ready

### /orch-start [request]
Start a new orchestration session:
```bash
mcp-cli call parallel-orchestrator/start_session '{"request": "<request>", "options": {"critics": 3, "tdd": true}}'
```

### /orch-end [status]
End session (status: completed, failed, cancelled):
```bash
mcp-cli call parallel-orchestrator/end_session '{"status": "<status>"}'
```

### /orch-status
Get current session status:
```bash
mcp-cli call parallel-orchestrator/get_status '{}'
```

### /orch-plan [overview]
Log implementation plan:
```bash
mcp-cli call parallel-orchestrator/log_plan '{"overview": "<overview>", "components": [...], "file_changes": [...]}'
```

### /orch-critic [type] [name]
Spawn a critic (types: critic_oop, critic_tdd, critic_packages):
```bash
mcp-cli call parallel-orchestrator/spawn_critic '{"critic_type": "<type>", "name": "<name>"}'
```

### /orch-task [name] [description]
Log a new task:
```bash
mcp-cli call parallel-orchestrator/log_task '{"name": "<name>", "description": "<description>"}'
```

### /orch-task-start [task_id] [phase]
Start task with TDD phase (RED, GREEN, REFACTOR):
```bash
mcp-cli call parallel-orchestrator/start_task '{"task_id": <id>, "tdd_phase": "<phase>"}'
```

### /orch-tdd [task_id] [phase]
Set TDD phase:
```bash
mcp-cli call parallel-orchestrator/set_tdd_phase '{"task_id": <id>, "phase": "<phase>"}'
```

### /orch-qa [name]
Spawn QA review:
```bash
mcp-cli call parallel-orchestrator/spawn_qa '{"name": "<name>"}'
```

### /orch-qa-result [score] [passed]
Log QA result (score 1-10):
```bash
mcp-cli call parallel-orchestrator/log_qa_result '{"subagent_id": <id>, "score": <score>, "passed": <true/false>}'
```

### /orch-event [message] [level]
Log event (levels: debug, info, warning, error):
```bash
mcp-cli call parallel-orchestrator/log_event '{"message": "<message>", "level": "<level>"}'
```

## Workflow Example

When user says `/orch` or asks to start an orchestration workflow:

0. (Optional) Pre-analyze: `/orch-pre-start-analyze "Implement feature X"` - gather context first
1. Start session: `/orch-start "Implement feature X"`
2. Create plan: `/orch-plan "Overview of implementation"`
3. Spawn critics in parallel:
   - `/orch-critic critic_oop "OOP Critic"`
   - `/orch-critic critic_tdd "TDD Critic"`
   - `/orch-critic critic_packages "Packages Critic"`
4. Log synthesis after critic review
5. Create and execute tasks with TDD:
   - `/orch-task "Task name" "Description"`
   - `/orch-task-start 1 RED`
   - `/orch-tdd 1 GREEN`
   - `/orch-tdd 1 REFACTOR`
6. Run QA review: `/orch-qa "QA Reviewer"`
7. End session: `/orch-end completed`

## MCP Server Info

Server: `parallel-orchestrator`
Tools: 18 available
Config: `~/.claude/settings.json` (global) or `.mcp.json` (project)

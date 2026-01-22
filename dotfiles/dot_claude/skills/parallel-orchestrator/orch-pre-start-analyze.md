---
name: orch-pre-start-analyze
description: Pre-flight analysis phase to gather context before starting an orchestration workflow
version: 1.0.0
triggers:
  - /orch-pre-start-analyze
  - /orch-analyze
  - /orch-pre
---

# Pre-Start Analysis

Analyze the codebase and gather context before starting a full orchestration workflow. This command helps you understand the current state and prepare for implementation.

## Usage
```
/orch-pre-start-analyze <feature_or_task_description>
```

## Example
```
/orch-pre-start-analyze Add user authentication with JWT tokens
```

## What This Command Does

1. **Gathers Context** - Analyzes the codebase to understand:
   - Project structure and architecture
   - Existing patterns and conventions
   - Related files that may need modification
   - Existing tests and testing patterns
   - Dependencies and packages in use

2. **Identifies Considerations** - Highlights:
   - Potential areas of impact
   - Files that may need changes
   - Existing code that can be reused
   - Patterns to follow for consistency

3. **Prepares Recommendations** - Suggests:
   - Approach options for implementation
   - Potential challenges or risks
   - Questions to clarify before starting

## Implementation

When the user invokes `/orch-pre-start-analyze`:

### Step 1: Acknowledge and Parse Request
Extract the feature/task description from the user's input.

### Step 2: Analyze Codebase Structure
Use the Task tool with `subagent_type=Explore` to:
```
Analyze the codebase structure for implementing: <feature_description>

Focus on:
1. Project structure - key directories and their purposes
2. Existing patterns - how similar features are implemented
3. Testing approach - where tests live and testing conventions
4. Configuration - relevant config files and settings
5. Dependencies - packages that may be relevant
```

### Step 3: Identify Related Files
Search for files related to the feature:
- Use Grep to find relevant code patterns
- Use Glob to identify file locations
- Look for similar implementations to follow

### Step 4: Present Analysis Summary
Provide a structured summary:

```markdown
## Pre-Start Analysis: <feature_description>

### Project Context
- Architecture type: [monolith/microservices/etc]
- Language/Framework: [detected stack]
- Test framework: [detected testing setup]

### Relevant Files Identified
| File | Purpose | Action Needed |
|------|---------|---------------|
| path/to/file | description | create/modify/reference |

### Existing Patterns to Follow
- Pattern 1: description
- Pattern 2: description

### Dependencies to Consider
- Existing: [relevant deps already installed]
- May need: [suggested new deps]

### Key Questions to Clarify
1. Question about ambiguous requirement
2. Question about approach choice

### Recommended Approach
Brief recommendation based on analysis.

### Ready to Start?
Run `/orch-start <feature_description>` to begin the orchestration workflow.
```

## Integration with Workflow

This command is designed to run BEFORE `/orch-start`:

```
/orch-pre-start-analyze Add JWT auth  <-- You are here (gather context)
         ↓
/orch-start Add JWT auth               <-- Start session with context
         ↓
/orch-plan                             <-- Create informed plan
         ↓
/orch-critic                           <-- Critics review with context
```

## Tips

- Run this command when:
  - Starting work on an unfamiliar codebase
  - Implementing a complex feature
  - Unsure about existing patterns to follow
  - Need to identify impacted areas

- Skip this command when:
  - Making simple changes
  - Already familiar with the codebase
  - Following up on previous analysis

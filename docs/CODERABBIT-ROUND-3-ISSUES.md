# CodeRabbit Round 3 Issues

Generated: 2026-01-22
Branch: `feat/coderabbit-round-3-fixes`
Base: `feat/team-dotfiles-structure`

## Summary

**Total Issues:** 67
- potential_issue: 65
- refactor_suggestion: 2

## Issues by File

### Shell Configuration (1 issue)

| File | Lines | Issue |
|------|-------|-------|
| `shell/zsh/lazy.sh` | 29-35 | Missing python wrapper for pyenv lazy loading |

### GitHub Workflows (1 issue)

| File | Lines | Issue |
|------|-------|-------|
| `.github/workflows/figma-artifacts.yml` | 184-190 | PR accumulates duplicate comments on each push |

### Scripts (1 issue)

| File | Lines | Issue |
|------|-------|-------|
| `scripts/validate-frontmatter.py` | 47-51 | Potential issue with frontmatter validation |

### CLAUDE.md (1 issue)

| File | Lines | Issue |
|------|-------|-------|
| `CLAUDE.md` | 212-220 | CodeRabbit CLI section needs review |

### Agents (6 issues)

| File | Lines | Issue |
|------|-------|-------|
| `agents/code-architect.md` | 24 | Missing or incorrect configuration |
| `agents/verify-app.md` | 22-31, 43-52 | 2 issues with verification logic |
| `agents/commit-push-pr-agents.md` | 124, 187-196, 199-214, 314 | 4 issues with commit/push logic |

### Plugins (3 issues)

| File | Lines | Issue |
|------|-------|-------|
| `plugins/pr-review-toolkit/agents/code-reviewer.md` | 2-3, 24-32 | 2 issues with reviewer config |
| `plugins/pr-review-toolkit/agents/comment-analyzer.md` | 1-6 | Refactor suggestion |

### Commands (1 issue)

| File | Lines | Issue |
|------|-------|-------|
| `commands/da_hook_optimize.md` | 53-68 | Hook optimization needs review |

### Skills - Databricks Patterns (14 issues)

| File | Lines | Issue |
|------|-------|-------|
| `patterns/databricks/authentication.yaml` | 153-161, 251-256, 417-426, 445-451, 555-568 | 5 auth issues |
| `patterns/databricks/templates.py` | 192-203, 530-538 | 2 template issues |
| `patterns/databricks/unity_catalog.yaml` | 156-167, 293-308, 338-344 | 3 catalog issues |
| `patterns/databricks/sql_execution.yaml` | 420-436, 527-529, 633-634, 669-672 | 4 SQL execution issues |
| `patterns/databricks/mcp_integration.yaml` | 98 | 1 MCP integration issue |

### Skills - CrewAI (6 issues)

| File | Lines | Issue |
|------|-------|-------|
| `skills/crewai/references/tools.md` | 119-126, 194-198, 258-265, 267-269, 358-372 | 5 tool reference issues |
| `skills/crewai/references/troubleshooting.md` | 334-354 | 1 troubleshooting issue |

### Skills - gRPC Microservices (7 issues)

| File | Lines | Issue |
|------|-------|-------|
| `skills/grpc-microservices/SKILL.md` | 449-491, 724-755 | 2 skill issues |
| `skills/grpc-microservices/EXAMPLES.md` | 220-234, 1256-1278, 1626-1634, 1724-1736, 1934-1953, 2014-2035 | 5+1 refactor issues |

### Skills - Task Management (7 issues)

| File | Lines | Issue |
|------|-------|-------|
| `skills/tm-feature-task-planner/SKILL.md` | 92-106 | 1 planner issue |
| `skills/tm-run-fix-code-review/SKILL.md` | 72-77, 84, 204 | 3 code review issues |
| `skills/tm-submit-pr/SKILL.md` | 48-49, 53-56, 114-115, 135 | 4 PR submission issues |

### Skills - Textual/UI (8 issues)

| File | Lines | Issue |
|------|-------|-------|
| `skills/skill/assets/dashboard_app.py` | 231-233 | Blocking psutil call |
| `skills/skill/assets/worker_demo.py` | 366-373 | Worker issue |
| `skills/skill/references/layouts.md` | 219-248 | Layout issue |
| `skills/skill/references/widgets.md` | 25-31, 396-409 | 2 widget issues |
| `skills/skill/references/styling.md` | 181-190, 495-508, 614-621 | 3 styling issues |

### Skills - Other (7 issues)

| File | Lines | Issue |
|------|-------|-------|
| `skills/1code-build/SKILL.md` | 82-87, 258-271 | 2 build issues |
| `skills/frontend-testing/references/async-testing.md` | 331-345 | 1 async testing issue |
| `skills/frontend-testing/references/mocking.md` | 257-268 | 1 mocking issue |
| `skills/git-master/SKILL.md` | 347-348 | 1 git issue |
| `skills/postgresql/SKILL.md` | 28 | 1 PostgreSQL issue |
| `skills/ux-designer/resources/design-tokens.md` | 619-707 | 1 design tokens issue |
| `skills/ux-designer/templates/ux-design.template.md` | 10-21 | 1 template issue |

---

## Priority Recommendations

### High Priority (Security/Functional)
1. `authentication.yaml` - 5 auth security issues
2. `commit-push-pr-agents.md` - 4 issues with git operations
3. `grpc-microservices/EXAMPLES.md` - 6 issues including security

### Medium Priority (Code Quality)
1. `sql_execution.yaml` - 4 SQL execution issues
2. `unity_catalog.yaml` - 3 catalog issues
3. `crewai/references/tools.md` - 5 tool reference issues

### Low Priority (Docs/Refactoring)
1. `figma-artifacts.yml` - PR comment duplication
2. `lazy.sh` - pyenv wrapper enhancement
3. Various styling/layout documentation issues

---

## Fix Status

- [ ] Shell Configuration (1)
- [ ] GitHub Workflows (1)
- [ ] Scripts (1)
- [ ] CLAUDE.md (1)
- [ ] Agents (6)
- [ ] Plugins (3)
- [ ] Commands (1)
- [ ] Databricks Patterns (14)
- [ ] CrewAI Skills (6)
- [ ] gRPC Skills (7)
- [ ] Task Management Skills (7)
- [ ] Textual/UI Skills (8)
- [ ] Other Skills (7)

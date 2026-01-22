# CodeRabbit Review Summary

Generated: 2026-01-22
Branch: `feat/coderabbit-remaining-fixes`
Base: `master`

## Issue Categories

### Critical/Security (Fix Immediately)

| File | Issue | Line |
|------|-------|------|
| `crewai/SKILL.md` | `eval()` allows arbitrary code execution | 235-245 |
| `crewai/references/tools.md` | `eval()` in calculator tool | 291-301 |
| `databricks/unity_catalog.yaml` | SQL injection in list_tables | 272-276 |
| `databricks/templates.py` | SQL injection in table_ref | 158-163 |
| `grpc-microservices/EXAMPLES.md` | Hardcoded Postgres DSN | 404 |
| `grpc-microservices/EXAMPLES.md` | JWT algorithm confusion vulnerability | 1611-1625 |

### High Priority (Functional Bugs)

| File | Issue | Line |
|------|-------|------|
| `shell/zsh/zshrc` | Completion cache age check fails if file missing | 191-198 |
| `async-python-patterns/SKILL.md` | Producer/consumer sentinel mismatch | 276-323 |
| `skill/assets/todo_app.py` | ctrl+c keybinding conflicts with terminal interrupt | 125-131 |
| `skill/assets/todo_app.py` | Mutating list while iterating in clear_completed | 215-221 |
| `skill/assets/worker_demo.py` | Workers don't handle cancellation | 384-396 |
| `grpc-microservices/EXAMPLES.md` | messagesChan nil pointer panic | 1252-1263 |
| `grpc-microservices/EXAMPLES.md` | Rate limiter unbounded memory growth | 1973-2001 |

### Medium Priority (Documentation/Examples)

| File | Issue | Line |
|------|-------|------|
| `skill/references/widgets.md` | Missing imports in examples | Multiple |
| `skill/references/layouts.md` | Missing Container import | 125-146 |
| `textual/guide.md` | Missing event handler parameter | 286-287 |
| `databricks/sql_execution.yaml` | Invalid spark.sql table parameter | 50-62 |
| `commands/pr-orchestration-plan-cmd.md` | Missing table separators | 173, 180 |
| `1code-build/SKILL.md` | Hardcoded user path | 10-15 |
| `po-run-benchmark/SKILL.md` | Hardcoded path + typo "baackups" | 33-66 |
| `graphite/SKILL.md` | Project-specific content in generic skill | 202-324 |
| `grpc-microservices/README.md` | Outdated timestamp "October 2025" | 1032 |

### Low Priority (Refactoring Suggestions)

| File | Issue | Line |
|------|-------|------|
| `grpc-microservices/SKILL.md` | Deprecated grpc.WithInsecure() | 805-823 |
| `postgresql/SKILL.md` | Duplicate uniqueness constraints | 170-179 |
| `ux-designer/REFERENCE.md` | Inconsistent Header/Search dimensions | 500-520 |
| `ux-designer/REFERENCE.md` | Card shadow inconsistent with Shadow System | 726-742 |

## Statistics

- **Total issues found**: ~70+
- **Critical/Security**: 6
- **High Priority**: 7
- **Medium Priority**: ~30
- **Low Priority**: ~27

## Recommendation

1. Fix all Critical/Security issues immediately
2. Address High Priority functional bugs
3. Medium/Low can be addressed incrementally

## Already Fixed (PR #3)

- coderabbit.yaml comments
- starship.toml comment
- ghostty config hex colors
- checklist.py typo
- test_figma_mcp.py assertion
- figma-artifacts.yml workflow
- validate-frontmatter.py type check
- lint.md, permissions.md, test.md, commit-push-pr.md
- figma-desktop.json schema
- aliases.sh cc conflict
- REFERENCE.md typography
- contrast-check.py validation

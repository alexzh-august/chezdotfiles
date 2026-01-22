---
name: po-run-benchmark
description: Run benchmarks for the parallel orchestrator skill. Measures execution timing, parallel savings, and efficiency metrics. Use when user says "run benchmark", "benchmark orchestrator", or wants to measure skill performance.
allowed-tools:
  - Bash
  - Read
  - Write
  - TodoWrite
hooks:
  - event: SessionStart
    command: "cd /Users/alexzh/local_safe_baackups && uv run python -c 'from orchestrator_db import init_db; init_db()'"
---

# Parallel Orchestrator Benchmark Runner

Run standardized benchmarks to measure orchestration skill performance.

## Quick Start

```
/po-run-benchmark              Run full benchmark suite
/po-run-benchmark --quick      Run quick benchmark (simple tasks only)
/po-run-benchmark --compare    Compare against previous run
```

## Instructions

When invoked, follow this process:

### 1. Initialize Benchmark Environment

```bash
cd /Users/alexzh/local_safe_baackups
uv run python -c "
from benchmark.tasks import BENCHMARK_TASKS
from benchmark.runner import BenchmarkRunner

print('=== Benchmark Environment ===')
print(f'Tasks available: {len(BENCHMARK_TASKS)}')
print(f'Categories: planning, critics, tdd, synthesis, full')
print(f'Complexities: simple, medium, complex')
"
```

### 2. Run Benchmark

**Full Benchmark:**
```bash
cd /Users/alexzh/local_safe_baackups
uv run python -m benchmark.cli run -v
```

**Quick Benchmark:**
```bash
cd /Users/alexzh/local_safe_baackups
uv run python -m benchmark.cli run --quick -v
```

**Specific Category:**
```bash
# Critics only
uv run python -m benchmark.cli run --category critics -v

# TDD only
uv run python -m benchmark.cli run --category tdd -v
```

**Single Task:**
```bash
uv run python -m benchmark.cli run -t simple-001 -v
```

### 3. View Results

```bash
# List all results
uv run python -m benchmark.cli results

# Show specific result
uv run python -m benchmark.cli results -s <run-id>
```

### 4. Compare Runs

```bash
# Compare two runs
uv run python -m benchmark.cli compare <baseline-id> <current-id>

# Run with comparison
uv run python -m benchmark.cli run -c <baseline-id> -v
```

## Metrics Collected

### Timing Metrics

| Metric | Description |
|--------|-------------|
| `total_duration_s` | End-to-end time (Unix seconds) |
| `phase_duration_s` | Per-phase breakdown |
| `target_duration_s` | Expected time for task |
| `efficiency_ratio` | target / actual (>1 = faster than target) |

### Quality Metrics

| Metric | Description |
|--------|-------------|
| `components_created` | Number of components generated |
| `files_created` | Files created during task |
| `tests_written` | Test cases created |
| `tests_passed` | Passing tests |
| `qa_score` | Quality score (1-10) |

### Parallelization Metrics

| Metric | Description |
|--------|-------------|
| `parallel_savings_s` | Time saved by parallel execution |
| `critic_count` | Number of parallel critics |
| `background_tasks` | Tasks run in background |

## Benchmark Tasks

### Simple (60-90s target)
- `simple-001`: Hello World Function - Basic TDD
- `simple-002`: Config Parser - Planning focus
- `spec-003`: No-QA Speed Run - Fast execution

### Medium (120-180s target)
- `medium-001`: User Authentication - Full workflow
- `medium-002`: REST API CRUD - Critic focus
- `medium-003`: Cache Layer - Synthesis focus
- `spec-001`: Critic Parallelism - Max parallel
- `spec-002`: TDD Strict Mode - TDD enforcement

### Complex (240-300s target)
- `complex-001`: Event Sourcing - Full complex
- `complex-002`: Distributed Queue - Heavy parallel

## Output Format

### Console Summary

```
╭─ Benchmark Results ─╮
│ Run ID: bench-...   │
│ Duration: XX.XXs    │
│ Efficiency: X.XXx   │
│ Tasks: X/Y          │
│ Parallel: XXs saved │
╰─────────────────────╯
```

### JSON Output

Results saved to: `benchmark/results/bench-YYYYMMDD-HHMMSS-XXXXXX.json`

```json
{
  "run_id": "bench-...",
  "total_duration_seconds": 12.34,
  "avg_efficiency_ratio": 5.67,
  "tasks": [...]
}
```

## Comparison with Cursor

This skill uses Claude's native features for faster execution:

| Feature | Claude Hooks | Cursor |
|---------|-------------|--------|
| Parallel Critics | ThreadPoolExecutor | Multi-agent |
| Background Tasks | Ctrl+B / Task tool | Composer |
| Metrics | orchestrator_db | Manual |
| Speed | Faster (hooks) | Standard |

## Best Practices

1. **Baseline First** - Run full benchmark before making changes
2. **Multiple Runs** - Average 3+ runs for accuracy
3. **Isolate Changes** - Test one improvement at a time
4. **Save Results** - Keep history for trend analysis
5. **Use Quick Mode** - For rapid iteration during development

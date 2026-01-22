---
name: daily-volumes-pipeline-dev-tcel
description: Run daily volumes pipeline with Test-Code-Execute-Learn loop to backfill defi_volumes_dev. Runs one day at a time, learns from failures, and fixes pipeline code. Use when user says "tcel pipeline", "backfill with learning", "fix and retry volumes", or wants intelligent pipeline execution with auto-fix.
---

# Daily Volumes Pipeline (Dev Mode + TCEL)

Runs the volume pipeline in dev mode with a **Test-Code-Execute-Learn** loop:
- Executes one day at a time
- Learns from failures
- Fixes pipeline code automatically
- Retries until all chains succeed

## Quick Start

Run December 2025 backfill with auto-fix:

```bash
# This skill will iterate day-by-day with learning
```

## Instructions

### Phase 1: Initialize

1. **Set date range**: Default 2025-12-01 to 2025-12-31
2. **Create failure log**: Track failures in `~/.claude/tcel_pipeline_log.md`
3. **Get chain list**: All chains from CONFIG_BY_CHAIN

### Phase 2: Execute Day-by-Day Loop

For each day in the date range (20251201 to 20251231):

```python
for day in date_range:
    for chain_id in all_chains:
        # Execute
        result = run_pipeline(day, chain_id)

        if result.failed:
            # Learn
            analyze_error(result.error)

            # Code
            fix_pipeline_code()

            # Test
            retry_pipeline(day, chain_id)
```

### Phase 3: For Each Day

1. **Execute pipeline for single day**:
```bash
python -m core_v1.regression.pipeline -d YYYYMMDD --dev --save_to_db
```

2. **If failure occurs**:
   - Log the error to `~/.claude/tcel_pipeline_log.md`
   - Analyze the stack trace and error type
   - Identify the root cause
   - Propose and implement a fix
   - Retry the failed chain

3. **Track progress**:
   - Mark successful chain-days
   - Track retry counts
   - Log all code changes made

### Phase 4: Learning Actions

When a failure occurs, follow this decision tree:

| Error Type | Action |
|------------|--------|
| `AttributeError: Chain.X` | Add missing chain to Chain enum |
| `RateLimitError` | Add retry with backoff |
| `NoTransfersFoundException` | Log as expected (no data) |
| `MissingPricesException` | Check tiingo.db, add price source |
| `ConnectionError` | Retry with exponential backoff |
| `KeyError in DataFrame` | Fix column name mapping |
| Import error | Fix import path or dependency |
| Unknown | Log for manual review |

### Phase 5: Code Fixes

When making code fixes:

1. **Read the failing code** to understand context
2. **Make minimal targeted fix** - don't over-engineer
3. **Document the fix** in the TCEL log
4. **Test the fix** by re-running that chain-day
5. **Commit if successful** with descriptive message

### Phase 6: Completion

After all days processed:

1. **Generate summary report**:
   - Total days processed
   - Successful chain-days
   - Failed chain-days (with reasons)
   - Code changes made
   - Lessons learned

2. **Update TCEL log** with final status

## TCEL Log Format

Create/append to `~/.claude/tcel_pipeline_log.md`:

```markdown
# TCEL Pipeline Log

## Session: YYYY-MM-DD HH:MM

### Configuration
- Date Range: 20251201 to 20251231
- Mode: dev
- Target: defi_volumes_dev

### Execution Log

#### Day: 2025-12-01

| Chain | Status | Error | Fix Applied |
|-------|--------|-------|-------------|
| MAINNET (1) | SUCCESS | - | - |
| ARBITRUM (42161) | FAIL | RateLimitError | Added retry logic |
| ARBITRUM (42161) | SUCCESS (retry) | - | - |

### Code Changes

#### Fix #1: Added retry for rate limiting
- File: `core_v1/regression/pipeline.py`
- Line: 245
- Change: Added exponential backoff
- Commit: `abc123`

### Summary
- Days processed: 31
- Total chain-days: 868
- Successful: 850
- Failed (no data): 18
- Code fixes applied: 3
```

## Chain Reference

Execute for each chain ID:
- EVM: 1, 42161, 8453, 43114, 56, 534352, 59144, 10, 80094, 999, 146, 9745, 31612, 57073, 14, 143, 137, 48900, 1923, 43111, 130, 239, 1868, 1101, 2222
- Non-EVM: -239 (TON), -2 (APTOS), -101 (SUI)

## Example Session

```
User: Run TCEL pipeline for December 2025

Claude:
1. Initializing TCEL pipeline for 2025-12-01 to 2025-12-31
2. Creating log at ~/.claude/tcel_pipeline_log.md

Day 1: 2025-12-01
- Running MAINNET... SUCCESS (15 records)
- Running ARBITRUM... FAIL (RateLimitError)
  - LEARN: Etherscan API rate limited
  - CODE: Adding 2s delay between chains
  - RETRY: SUCCESS (12 records)
- Running BASE... SUCCESS (8 records)
...

Day 31: 2025-12-31
- All chains complete

Summary:
- 868/868 chain-days processed
- 3 code fixes applied
- See full log: ~/.claude/tcel_pipeline_log.md
```

## Working Directory

Run from: `/Users/alexzh/defi-data-collection/fractal_internal_scripts`

## Important Files

- Pipeline: `core_v1/regression/pipeline.py`
- Wrappers: `core_v1/regression/wrappers/`
- Volume config: `core_v1/settings/volume_config.py`
- Chain enum: `core_v1/common/types.py`

---
name: daily-volumes-pipeline-dev
description: Run the daily volumes pipeline in dev mode to backfill defi_volumes_dev MongoDB collection. Use when user says "run pipeline dev", "backfill volumes", "populate defi_volumes_dev", or wants to run the volume pipeline for a date range.
---

# Daily Volumes Pipeline (Dev Mode)

Runs the volume pipeline in dev mode to populate `defi_volumes_dev` MongoDB collection with cached API responses stored in SQLite.

## Quick Start

```bash
# All chains, December 2025
python -m core_v1.regression.pipeline -sd 20251201 -ed 20251231 --dev --save_to_db
```

## Instructions

1. **Confirm the date range** with the user (default: 20251201 to 20251231)

2. **Run the pipeline** for all chains or specific chains:

```bash
# All chains at once
python -m core_v1.regression.pipeline -sd 20251201 -ed 20251231 --dev --save_to_db

# Or specific chain by ID
python -m core_v1.regression.pipeline -sd 20251201 -ed 20251231 -c <CHAIN_ID> --dev --save_to_db
```

3. **Monitor progress** - The pipeline logs progress for each chain

4. **Report results** - Summarize which chains succeeded/failed

## Chain Reference

| Chain | ID | Command |
|-------|-----|---------|
| MAINNET | 1 | `-c 1` |
| ARBITRUM | 42161 | `-c 42161` |
| BASE | 8453 | `-c 8453` |
| AVALANCHE | 43114 | `-c 43114` |
| BSC | 56 | `-c 56` |
| SCROLL | 534352 | `-c 534352` |
| LINEA | 59144 | `-c 59144` |
| OPTIMISM | 10 | `-c 10` |
| BERA | 80094 | `-c 80094` |
| HYPEREVM | 999 | `-c 999` |
| SONIC | 146 | `-c 146` |
| PLASMA | 9745 | `-c 9745` |
| MEZO | 31612 | `-c 31612` |
| INK | 57073 | `-c 57073` |
| FLARE | 14 | `-c 14` |
| MONAD | 143 | `-c 143` |
| POLYGON | 137 | `-c 137` |
| ZIRCUIT | 48900 | `-c 48900` |
| SWELL | 1923 | `-c 1923` |
| HEMI | 43111 | `-c 43111` |
| UNICHAIN | 130 | `-c 130` |
| TAC | 239 | `-c 239` |
| SONEIUM | 1868 | `-c 1868` |
| KAVA | 1101 | `-c 1101` |
| POLYZK | 2222 | `-c 2222` |
| TON | -239 | `-c -239` |
| APTOS | -2 | `-c -2` |
| SUI | -101 | `-c -101` |

## What This Does

- **Dev mode**: Writes to `defi_volumes_dev` collection (not production)
- **No alerts**: Slack/Sentry notifications are disabled
- **Caching**: API responses cached to SQLite for replay
- **Recording**: All Alchemy, Etherscan, Tiingo calls are recorded

## Working Directory

Run from: `/Users/alexzh/defi-data-collection/fractal_internal_scripts`

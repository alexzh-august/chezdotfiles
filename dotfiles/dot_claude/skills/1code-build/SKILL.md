---
name: 1code-build
description: Build 1Code from source with file tracking enabled. Use when user says "build 1code", "run build", "compile app", "package app", or wants to build the Electron desktop app. Handles dependencies, file tracking setup, and full build pipeline.
---

# 1Code Build Process

Build the 1Code Electron desktop app from source with integrated file metadata tracking, semantic indexing, and comprehensive test verification.

## Quick Start

```bash
cd /Users/alexzh/1code
/1code-build
```

## Instructions

When this skill is invoked, follow these steps in order:

### Step 1: Verify Project Directory

Check that we're in the 1code project root:
```bash
cd /Users/alexzh/1code && ls package.json
```

If not found, ask the user for the correct path.

### Step 2: Install Node Dependencies

```bash
bun install
```

If bun is not installed:
```bash
npm install -g bun
bun install
```

### Step 3: Setup File Tracker (Python)

Install the file tracking system for Claude Code metadata:

```bash
cd tools/file_tracker
pip install -e . --quiet
cd ../..
```

Verify installation:
```bash
file-tracker --help
```

### Step 4: Initialize File Tracking

```bash
file-tracker init --name "1Code"
```

### Step 5: Setup Semantic Index (Docker)

Start the semantic index database:
```bash
cd tools/semantic-index
./setup.sh
cd ../..
```

Or manually:
```bash
docker compose -f tools/semantic-index/docker-compose.yml up -d
```

Verify database is running:
```bash
docker exec claude-code-db pg_isready -U claude -d semantic_index
```

### Step 6: Download Claude Binary

Required for Claude Code integration:
```bash
bun run claude:download
```

### Step 7: Run Tests (REQUIRED BEFORE BUILD)

All tests must pass before proceeding with the build:

```bash
# Run full test suite
bun run test

# Individual test suites:
bun run test:unit        # Unit tests
bun run test:db          # Database tests
bun run test:integration # Integration tests
bun run test:e2e         # End-to-end tests
```

If any tests fail, stop and fix the issues before proceeding.

### Step 8: Run the Build

For development build:
```bash
bun run build
```

For platform-specific packages:
- macOS: `bun run package:mac`
- Windows: `bun run package:win`
- Linux: `bun run package:linux`

### Step 9: Verify Build Output

Check that build artifacts exist:
```bash
ls -la out/
ls -la release/ 2>/dev/null || echo "No release folder yet (run package command to create)"
```

### Step 10: Run Build Verification Tests

Post-build verification:
```bash
bun run test:build-verify
```

### Step 11: Scan for File Headers

After build, scan any modified files:
```bash
file-tracker scan . --ext ".ts,.tsx,.js"
file-tracker show . --limit 10
```

---

## Build Commands Reference

| Command | Description |
|---------|-------------|
| `bun run dev` | Start dev server with hot reload |
| `bun run build` | Compile TypeScript |
| `bun run package` | Package for current platform |
| `bun run package:mac` | Build macOS DMG + ZIP |
| `bun run package:win` | Build Windows installer |
| `bun run package:linux` | Build Linux AppImage |
| `bun run release` | Full release (build + sign + upload) |

## Test Commands Reference

| Command | Description |
|---------|-------------|
| `bun run test` | Run all tests |
| `bun run test:unit` | Unit tests only |
| `bun run test:db` | Database integration tests |
| `bun run test:integration` | API integration tests |
| `bun run test:e2e` | End-to-end Playwright tests |
| `bun run test:semantic` | Semantic index tests |
| `bun run test:build-verify` | Build output verification |
| `bun run test:coverage` | Generate coverage report |

## Database Commands

| Command | Description |
|---------|-------------|
| `bun run db:generate` | Generate Drizzle migrations |
| `bun run db:push` | Push schema to DB (dev only) |
| `bun run db:studio` | Open Drizzle Studio |
| `bun run db:test` | Test database operations |

## Semantic Index Commands

| Command | Description |
|---------|-------------|
| `bun run semantic:start` | Start semantic index Docker |
| `bun run semantic:stop` | Stop semantic index Docker |
| `bun run semantic:reset` | Reset and rebuild index |
| `bun run semantic:test` | Test semantic search |
| `bun run semantic:index` | Index current project |

## File Tracking Commands

| Command | Description |
|---------|-------------|
| `file-tracker init .` | Initialize tracking |
| `file-tracker watch .` | Watch for changes |
| `file-tracker scan . --ext ".py,.ts"` | Scan existing files |
| `file-tracker changelog -o CHANGELOG.md` | Generate changelog |
| `file-tracker show .` | Show recent changes |
| `file-tracker add-header <file>` | Add header to file |

---

## Feature Verification Matrix

Each build REQUIRES all features to be verified:

| Feature | Test Command | Required |
|---------|--------------|----------|
| TypeScript compilation | `bun run build` | YES |
| SQLite database | `bun run test:db` | YES |
| tRPC routers | `bun run test:integration` | YES |
| React components | `bun run test:unit` | YES |
| Semantic index | `bun run test:semantic` | YES |
| File tracking | `file-tracker --help` | YES |
| Electron packaging | `bun run test:build-verify` | YES |

---

## Troubleshooting

### Native modules fail to rebuild
```bash
bun run postinstall
# or manually:
npx electron-rebuild -f -w better-sqlite3,node-pty
```

### Bun not found
```bash
curl -fsSL https://bun.sh/install | bash
source ~/.zshrc
```

### Python dependencies missing
```bash
pip install pydantic watchdog typer rich pyyaml
```

### Build fails with TypeScript errors
```bash
bun run ts:check
```

### Semantic index not starting
```bash
docker ps | grep claude-code-db
docker logs claude-code-db
```

### Tests failing
```bash
# Run with verbose output
bun run test -- --reporter=verbose

# Run specific test file
bun run test src/main/lib/db/__tests__/index.test.ts
```

---

## Environment Variables

For macOS notarization (optional):
```bash
export APPLE_ID="your-apple-id@example.com"
export APPLE_APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```

For semantic index (optional, defaults provided):
```bash
export POSTGRES_PASSWORD="claudecode"
export OPENAI_API_KEY="sk-..."
```

---

## Example Usage

**Full build from scratch (with tests):**
```
User: /1code-build
Claude: I'll build 1Code from source...
[Runs all steps including tests]
```

**Just compile (skip tests for iteration):**
```
User: /1code-build compile only
Claude: I'll just run the TypeScript compilation...
[Runs bun run build only]
```

**Package for macOS:**
```
User: /1code-build package mac
Claude: I'll build and package for macOS...
[Runs tests + build + package:mac]
```

**Run tests only:**
```
User: /1code-build test
Claude: I'll run the full test suite...
[Runs all tests]
```

**With semantic index:**
```
User: /1code-build with semantic
Claude: I'll build with semantic indexing enabled...
[Starts Docker, runs semantic tests, then builds]
```

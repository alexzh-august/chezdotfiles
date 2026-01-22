# Hook & MCP Performance Optimization

Analyze and optimize Claude Code hooks and MCP servers for better performance and reduced token usage.

## Usage

```bash
# Analyze current hook and MCP performance
da hook-analyze

# Optimize configuration (creates backup first)
da hook-optimize

# Monitor performance after changes
da hook-monitor

# Compare with baseline metrics
da hook-compare

# Set new baseline after optimization
da hook-baseline
```

## Commands

### da hook-analyze
- Measures current hook execution times
- Analyzes MCP server startup times and token overhead
- Provides optimization recommendations
- Shows which components cause latency/token usage

### da hook-optimize
- Creates backup of current settings
- Removes external/problematic hooks
- Disables high token overhead MCP servers
- Keeps only essential servers (git, filesystem)
- Adds common command permissions

### da hook-monitor
- Real-time performance monitoring
- Shows active vs disabled components
- Measures current startup times

### da hook-compare
- Compares current performance with baseline
- Shows improvements and regressions
- Identifies performance changes over time

### da hook-baseline
- Sets current performance as new baseline
- Used for future comparisons

## Optimization Impact

**Before optimization:**
- 7 MCP servers active (~1500+ tokens/interaction)
- External hook dependencies
- 334ms+ startup times
- Permission prompts for common commands

**After optimization:**
- 2 essential MCP servers (~250 tokens/interaction)
- Only local hooks
- <300ms startup times
- Pre-approved common commands

**Token savings:** ~85% reduction in MCP overhead
**Latency improvement:** ~50% faster startup

## Backup & Recovery

Settings are automatically backed up before optimization:
```bash
# Restore original settings if needed
cp ~/.claude/backups/settings_backup_TIMESTAMP.json ~/.claude/settings.json
```

## Files Created

- `/scripts/hook-latency-tracker.py` - Performance analysis tool
- `/scripts/optimize-claude-config.py` - Configuration optimizer
- `/scripts/monitor-performance.py` - Real-time monitoring
- `~/.claude/metrics/` - Performance data storage
- `~/.claude/backups/` - Settings backups
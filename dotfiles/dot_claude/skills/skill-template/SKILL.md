---
name: skill-template
description: Template for creating new Claude Code skills. Use when creating a new skill, as a reference for skill structure, or when user asks about skill format.
---

# Skill Template

This is a template for creating Claude Code skills. Copy this directory and modify for your use case.

## Quick Start

```bash
# Copy template
cp -r .claude/skills/skill-template .claude/skills/my-new-skill

# Edit the SKILL.md
# 1. Update frontmatter (name, description)
# 2. Write instructions
# 3. Add examples
```

## Frontmatter Requirements

```yaml
---
name: lowercase-with-hyphens    # Must match directory name, max 64 chars
description: What it does and when to use it. Include trigger words users would say. Max 1024 chars.
allowed-tools: Read, Grep, Glob  # Optional: restrict to specific tools
---
```

## Structure Options

### Single File (Simple)
```
skill-name/
└── SKILL.md
```

### Multi-File (Complex)
```
skill-name/
├── SKILL.md           # Main skill file (required)
├── reference.md       # Detailed docs
├── examples.md        # Extended examples
├── templates/         # File templates
│   └── template.txt
└── scripts/           # Helper scripts
    └── helper.py
```

## Instructions Section

Write clear, step-by-step instructions for Claude:

1. **Gather context** - What information to collect first
2. **Analyze** - What to look for or evaluate
3. **Execute** - What actions to take
4. **Output** - What format to return results in

## Examples Section

Provide concrete examples:

```bash
# Example invocation
/skill-name arg1 arg2
```

Expected output:
```
Result of the skill execution...
```

## Best Practices

- One skill = one focused capability
- Include trigger words in description
- Write instructions for Claude, not humans
- Provide concrete examples with real code
- List any dependencies
- Keep it simple - avoid over-engineering

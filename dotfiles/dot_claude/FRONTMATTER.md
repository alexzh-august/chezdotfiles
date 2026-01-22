# Frontmatter Standards

All agents, commands, skills, and plugins must include YAML frontmatter for documentation and visual artifact generation.

## Required Fields

### Agents

```yaml
---
name: agent-name
description: "Clear description of what the agent does"
model: opus | sonnet | haiku | inherit  # Optional, defaults to inherit
color: green | blue | yellow | red      # Optional, for visual distinction
---
```

### Commands

```yaml
---
description: "Clear description of the command"
argument-hint: "[optional-args]"        # Shown in command help
allowed-tools: ["Bash", "Read", "Glob"] # Tools the command can use
---
```

### Skills

```yaml
---
name: skill-name
description: "What the skill provides"
triggers:                               # Keywords that activate this skill
  - keyword1
  - keyword2
---
```

## Figma Integration Fields (Optional but Recommended)

Add a `figma` section for visual artifact generation:

```yaml
---
name: my-component
description: "Description"

# Figma MCP Integration
figma:
  # Diagram type for auto-generation
  diagram_type: flowchart  # flowchart | sequence | state | architecture

  # Figma component ID (if linked to design file)
  component_id: "123:456"  # Optional

  # Systems this component interacts with
  integration_points:
    - github         # GitHub API/repos
    - filesystem     # Local files
    - mcp-servers    # Other MCP servers
    - database       # Database connections
    - api            # External APIs
    - cli            # Command line tools
    - browser        # Browser automation
    - figma          # Figma designs

  # Generated artifact references
  visual_artifacts:
    - path: artifacts/my-component-flow.svg
      type: workflow
      generated: 2026-01-22
---
```

## Validation

Run the validation script to check all components:

```bash
# Validate all
python scripts/validate-frontmatter.py --all

# Validate specific types
python scripts/validate-frontmatter.py --agents true

# Strict mode (warnings become errors)
python scripts/validate-frontmatter.py --all --strict
```

## Examples

### Agent with Full Figma Integration

```yaml
---
name: pr-reviewer
description: "Reviews pull requests for code quality, security, and best practices"
model: opus
color: green

figma:
  diagram_type: flowchart
  integration_points:
    - github
    - filesystem
  visual_artifacts:
    - path: artifacts/pr-reviewer-flow.svg
      type: workflow
      generated: 2026-01-22
---

# PR Reviewer Agent

Reviews pull requests...
```

### Command with Minimal Frontmatter

```yaml
---
description: "Run linter and fix issues"
argument-hint: "[--fix]"
allowed-tools: ["Bash", "Read", "Edit"]
---

# Lint Command

Run linting...
```

## PR Checklist

Before creating a PR with new components:

- [ ] All components have required frontmatter fields
- [ ] Descriptions are clear and actionable
- [ ] Figma integration points are listed (if applicable)
- [ ] Validation passes: `python scripts/validate-frontmatter.py --all`

## CI/CD Integration

The GitHub Actions workflow automatically:
1. Validates frontmatter on all changed files
2. Generates diagrams from `figma.diagram_type`
3. Comments on PR with visual summary
4. Fails if required fields are missing

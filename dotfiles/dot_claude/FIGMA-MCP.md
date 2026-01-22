# Figma MCP Server Integration

> Visual artifacts for AI development tools configuration

## Overview

This document describes how to integrate the [Figma MCP Server](https://developers.figma.com/docs/figma-mcp-server/) with Claude Code and Claude Desktop to generate visual artifacts for dotfile configurations.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Figma MCP Integration Architecture                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐ │
│  │   Figma      │     │  MCP Server  │     │     Claude Code/Desktop      │ │
│  │   Design     │────▶│  (Remote)    │────▶│                              │ │
│  │   Files      │     │              │     │  • Agents                    │ │
│  └──────────────┘     │ mcp.figma.com│     │  • Commands                  │ │
│                       └──────────────┘     │  • Skills                    │ │
│                              │             │  • Plugins                   │ │
│                              ▼             └──────────────────────────────┘ │
│                       ┌──────────────┐                    │                 │
│                       │   Context    │                    │                 │
│                       │  Extraction  │                    ▼                 │
│                       │              │     ┌──────────────────────────────┐ │
│                       │ • Components │     │     Generated Artifacts      │ │
│                       │ • Variables  │     │                              │ │
│                       │ • Layout     │     │  • Architecture diagrams     │ │
│                       │ • Styles     │     │  • Workflow visualizations   │ │
│                       └──────────────┘     │  • Integration point maps    │ │
│                                            │  • UI/UX documentation       │ │
│                                            └──────────────────────────────┘ │
│                                                           │                 │
│                                                           ▼                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                        GitHub Actions PR Workflow                        ││
│  │                                                                          ││
│  │  PR Created ──▶ Generate Figma Artifacts ──▶ Update PR with visuals     ││
│  │                                                                          ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

## Setup

### 1. Claude Code (Remote MCP - Recommended)

```bash
# Add Figma MCP server to Claude Code
claude mcp add --transport sse figma https://mcp.figma.com/sse

# Verify connection
claude
# Then type: /mcp
# Select figma > Authenticate
```

### 2. Claude Desktop

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "figma": {
      "url": "https://mcp.figma.com/sse",
      "transport": "sse"
    }
  }
}
```

### 3. Desktop App (Local MCP - Alternative)

If you prefer local processing through Figma Desktop:

1. Open Figma Desktop app
2. Open any Design file
3. Toggle to Dev Mode (`Shift+D`)
4. In MCP server section, click "Enable desktop MCP server"
5. Server runs at `http://127.0.0.1:3845/mcp`

Add to Claude config:
```json
{
  "mcpServers": {
    "figma-desktop": {
      "url": "http://127.0.0.1:3845/mcp"
    }
  }
}
```

## Usage

### Generating Artifacts from Designs

1. **Copy Figma link**: Right-click on frame/layer → Copy link to selection
2. **Paste in Claude**: Include the link in your prompt
3. **Request generation**: Ask Claude to generate code, extract design tokens, or create documentation

**Example prompt:**
```
Here's my Figma design for the agent workflow: [paste Figma link]

Please:
1. Extract the component structure
2. Generate a Mermaid diagram showing the workflow
3. Create integration documentation
```

### Available MCP Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `get_figma_data` | Extract design context | Pull components, variables, layout |
| `get_code` | Generate code from frames | Convert designs to React/HTML |
| `get_make_resources` | Access Make file resources | Production code context |

## Integration Points

### Dotfiles Visual Documentation

Each dotfile category should have corresponding Figma artifacts:

```
dotfiles/
├── dot_claude/
│   ├── FIGMA-MCP.md           # This file
│   ├── figma/
│   │   ├── architecture.fig   # Master architecture (Figma link)
│   │   ├── agents-flow.fig    # Agent interaction diagram
│   │   ├── commands-flow.fig  # Command execution flow
│   │   └── plugins-flow.fig   # Plugin integration diagram
│   └── artifacts/             # Generated visual artifacts
│       ├── README.md          # Index of all artifacts
│       ├── architecture.svg   # Exported diagrams
│       └── workflows/         # Workflow visualizations
```

## PR Automation

### Workflow: Figma Artifact Generation

When a PR is created or updated:

1. **Detect changes**: Identify modified agents/commands/skills
2. **Generate diagrams**: Create Mermaid/SVG representations
3. **Update Figma**: Sync to master architecture
4. **Comment on PR**: Add visual preview

### Required Frontmatter

All agents, commands, and skills must include visualization metadata:

```yaml
---
name: my-agent
description: Does something useful
# Figma Integration
figma:
  component_id: "123:456"        # Figma node ID (optional)
  diagram_type: "flowchart"      # flowchart | sequence | state | architecture
  integration_points:            # Systems this component interacts with
    - github
    - filesystem
    - mcp-servers
  visual_artifacts:              # Generated artifacts
    - path: artifacts/my-agent-flow.svg
      type: workflow
      generated: 2026-01-22
---
```

## Integration Tests

### Visual Regression Testing

Each component should have integration tests that verify:

1. **MCP connectivity**: Figma server responds correctly
2. **Artifact generation**: Diagrams render as expected
3. **Frontmatter validity**: All required fields present

```bash
# Run integration tests
./scripts/test-figma-integration.sh

# Validate frontmatter
./scripts/validate-frontmatter.sh
```

### Test Structure

```python
# tests/integration/test_figma_mcp.py

def test_figma_mcp_connection():
    """Verify Figma MCP server is accessible."""
    pass

def test_artifact_generation():
    """Verify artifacts generate correctly from Figma links."""
    pass

def test_frontmatter_schema():
    """Validate all components have required figma frontmatter."""
    pass
```

## Best Practices

### Design System Alignment

1. **Consistent naming**: Match Figma component names to code
2. **Token sync**: Use Figma variables for colors, spacing, typography
3. **Component mapping**: Link Figma components to code components

### Security

- Never commit Figma API tokens
- Use OAuth flow for authentication
- Rate limit awareness (6 calls/month for Starter plans)

## Related Resources

- [Figma MCP Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [Design Systems + MCP](https://www.figma.com/blog/design-systems-ai-mcp/)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)

## Roadmap

- [ ] Master architecture Figma file
- [ ] Automated PR artifact generation
- [ ] Visual regression testing
- [ ] Design token extraction
- [ ] Component library sync

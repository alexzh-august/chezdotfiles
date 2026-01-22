# Generated Visual Artifacts

This directory contains auto-generated visual documentation for dotfile components.

## Contents

| Artifact | Description | Source |
|----------|-------------|--------|
| `architecture.svg` | Master architecture diagram | `docs/architecture.mmd` |
| `workflows/*.svg` | Component workflow diagrams | Auto-generated from frontmatter |

## Generation

Artifacts are generated in two ways:

### 1. PR Automation (CI/CD)

When a PR modifies `dotfiles/dot_claude/`:
- GitHub Actions workflow detects changes
- Mermaid diagrams are rendered to SVG
- Artifacts are uploaded and linked in PR comments

### 2. Manual Generation

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Generate architecture diagram
mmdc -i docs/architecture.mmd -o dotfiles/dot_claude/artifacts/architecture.svg

# Generate all diagrams
./scripts/generate-all-diagrams.sh
```

## Frontmatter Requirements

For automatic diagram generation, components must include:

```yaml
---
name: my-component
description: What it does
figma:
  diagram_type: flowchart  # flowchart | sequence | state | architecture
  integration_points:
    - github
    - filesystem
    - mcp-servers
---
```

## Viewing Artifacts

- **In GitHub**: Click on SVG files to view in browser
- **In IDE**: Most IDEs render SVG previews
- **In Figma**: Import SVGs to your design files

## Related

- [FIGMA-MCP.md](../FIGMA-MCP.md) - Integration setup guide
- [Master Architecture](../../docs/architecture.mmd) - Mermaid source

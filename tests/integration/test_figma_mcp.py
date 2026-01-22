"""
Integration tests for Figma MCP Server integration.

These tests validate:
1. MCP configuration files are valid
2. Frontmatter schema compliance
3. Artifact generation (when enabled)
"""

import json
import os
from pathlib import Path

import pytest
import yaml

# Test configuration
DOTFILES_PATH = Path("dotfiles/dot_claude")
MCP_CONFIG_PATH = DOTFILES_PATH / "mcp-config"
FIGMA_MCP_ENABLED = os.environ.get("FIGMA_MCP_ENABLED", "false").lower() == "true"


class TestMCPConfiguration:
    """Test MCP configuration files."""

    def test_remote_config_exists(self):
        """Verify remote MCP config exists."""
        config_path = MCP_CONFIG_PATH / "figma-remote.json"
        assert config_path.exists(), f"Missing {config_path}"

    def test_desktop_config_exists(self):
        """Verify desktop MCP config exists."""
        config_path = MCP_CONFIG_PATH / "figma-desktop.json"
        assert config_path.exists(), f"Missing {config_path}"

    def test_remote_config_valid_json(self):
        """Verify remote config is valid JSON."""
        config_path = MCP_CONFIG_PATH / "figma-remote.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "mcpServers" in config
        assert "figma" in config["mcpServers"]
        assert "url" in config["mcpServers"]["figma"]

    def test_desktop_config_valid_json(self):
        """Verify desktop config is valid JSON."""
        config_path = MCP_CONFIG_PATH / "figma-desktop.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "mcpServers" in config
        assert "figma-desktop" in config["mcpServers"]

    def test_remote_url_is_correct(self):
        """Verify remote URL points to Figma's hosted endpoint."""
        config_path = MCP_CONFIG_PATH / "figma-remote.json"
        with open(config_path) as f:
            config = json.load(f)

        url = config["mcpServers"]["figma"]["url"]
        assert "mcp.figma.com" in url, f"Expected Figma MCP URL, got {url}"


class TestFrontmatterSchema:
    """Test frontmatter schema in component files."""

    VALID_DIAGRAM_TYPES = ["flowchart", "sequence", "state", "architecture"]
    VALID_INTEGRATION_POINTS = [
        "github",
        "filesystem",
        "mcp-servers",
        "database",
        "api",
        "cli",
        "browser",
        "figma",
    ]

    @staticmethod
    def parse_frontmatter(file_path: Path) -> dict | None:
        """Extract YAML frontmatter from markdown file."""
        content = file_path.read_text()
        if not content.startswith("---"):
            return None
        try:
            end_idx = content.index("---", 3)
            return yaml.safe_load(content[3:end_idx])
        except (ValueError, yaml.YAMLError):
            return None

    def get_component_files(self, component_type: str) -> list[Path]:
        """Get all markdown files for a component type."""
        component_path = DOTFILES_PATH / component_type
        if not component_path.exists():
            return []
        return [
            f
            for f in component_path.rglob("*.md")
            if f.name.lower() not in ["readme.md", "changelog.md"]
        ]

    def test_agents_have_frontmatter(self):
        """All agent files should have frontmatter."""
        for file_path in self.get_component_files("agents"):
            fm = self.parse_frontmatter(file_path)
            assert fm is not None, f"Missing frontmatter in {file_path}"

    def test_commands_have_frontmatter(self):
        """All command files should have frontmatter."""
        for file_path in self.get_component_files("commands"):
            fm = self.parse_frontmatter(file_path)
            assert fm is not None, f"Missing frontmatter in {file_path}"

    def test_agents_have_required_fields(self):
        """Agents should have name and description."""
        for file_path in self.get_component_files("agents"):
            fm = self.parse_frontmatter(file_path)
            if fm:
                # Name is required for agents
                assert "name" in fm or "description" in fm, (
                    f"Agent {file_path} missing name or description"
                )

    def test_figma_diagram_types_valid(self):
        """If figma.diagram_type is specified, it should be valid."""
        for component_type in ["agents", "commands", "skills"]:
            for file_path in self.get_component_files(component_type):
                fm = self.parse_frontmatter(file_path)
                if fm and "figma" in fm:
                    diagram_type = fm["figma"].get("diagram_type")
                    if diagram_type:
                        assert diagram_type in self.VALID_DIAGRAM_TYPES, (
                            f"Invalid diagram_type '{diagram_type}' in {file_path}. "
                            f"Valid types: {self.VALID_DIAGRAM_TYPES}"
                        )


class TestArtifactGeneration:
    """Test artifact generation (requires FIGMA_MCP_ENABLED=true)."""

    @pytest.mark.skipif(
        not FIGMA_MCP_ENABLED, reason="Figma MCP not enabled in CI"
    )
    def test_figma_mcp_connection(self):
        """Verify Figma MCP server is accessible."""
        # This would require actual MCP client implementation
        # Placeholder for when MCP testing is enabled
        pass

    @pytest.mark.skipif(
        not FIGMA_MCP_ENABLED, reason="Figma MCP not enabled in CI"
    )
    def test_artifact_directory_exists(self):
        """Verify artifacts directory exists."""
        artifacts_path = DOTFILES_PATH / "artifacts"
        assert artifacts_path.exists(), f"Missing {artifacts_path}"


class TestDocumentation:
    """Test documentation files exist and are valid."""

    def test_figma_mcp_doc_exists(self):
        """FIGMA-MCP.md should exist."""
        doc_path = DOTFILES_PATH / "FIGMA-MCP.md"
        assert doc_path.exists(), f"Missing {doc_path}"

    def test_figma_mcp_doc_has_setup_section(self):
        """FIGMA-MCP.md should have setup instructions."""
        doc_path = DOTFILES_PATH / "FIGMA-MCP.md"
        content = doc_path.read_text()
        assert "## Setup" in content, "Missing Setup section in FIGMA-MCP.md"

    def test_figma_mcp_doc_has_architecture(self):
        """FIGMA-MCP.md should have architecture diagram."""
        doc_path = DOTFILES_PATH / "FIGMA-MCP.md"
        content = doc_path.read_text()
        assert "## Architecture" in content, "Missing Architecture section"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

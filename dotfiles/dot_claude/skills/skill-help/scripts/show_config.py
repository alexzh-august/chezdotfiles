#!/usr/bin/env python3
"""
Claude Code Configuration Dashboard
Displays agents, commands, skills, hooks, and MCPs with Rich formatting.
"""

import json
import re
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich import box
except ImportError:
    print("Rich library not installed. Run: pip install rich")
    exit(1)

CLAUDE_DIR = Path.home() / ".claude"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"

console = Console()


def load_settings() -> dict:
    """Load settings.json file."""
    if SETTINGS_FILE.exists():
        return json.loads(SETTINGS_FILE.read_text())
    return {}


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()
        return frontmatter
    return {}


def get_agents() -> list[tuple[str, str]]:
    """Get list of agents with their descriptions."""
    agents_dir = CLAUDE_DIR / "agents"
    agents = []
    if agents_dir.exists():
        for f in sorted(agents_dir.glob("*.md")):
            content = f.read_text()
            fm = extract_frontmatter(content)
            name = fm.get("name", f.stem)
            desc = fm.get("description", "")[:60]
            if len(fm.get("description", "")) > 60:
                desc += "..."
            agents.append((name, desc))
    return agents


def get_commands() -> list[tuple[str, str]]:
    """Get list of commands with their descriptions."""
    commands_dir = CLAUDE_DIR / "commands"
    commands = []
    if commands_dir.exists():
        for f in sorted(commands_dir.glob("*.md")):
            content = f.read_text()
            fm = extract_frontmatter(content)
            name = f.stem
            desc = fm.get("description", "")[:60]
            if len(fm.get("description", "")) > 60:
                desc += "..."
            commands.append((name, desc))
    return commands


def get_skills() -> list[tuple[str, str]]:
    """Get list of skills with their descriptions."""
    skills_dir = CLAUDE_DIR / "skills"
    skills = []
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir():
                skill_file = d / "SKILL.md"
                if skill_file.exists():
                    content = skill_file.read_text()
                    fm = extract_frontmatter(content)
                    name = fm.get("name", d.name)
                    desc = fm.get("description", "")[:60]
                    if len(fm.get("description", "")) > 60:
                        desc += "..."
                    skills.append((name, desc))
    return skills


def display_agents(agents: list[tuple[str, str]]) -> None:
    """Display agents table."""
    table = Table(
        title="[bold cyan]Agents[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Name", style="green", width=30)
    table.add_column("Description", style="dim", width=60)

    for name, desc in agents:
        table.add_row(name, desc)

    console.print(table)
    console.print()


def display_commands(commands: list[tuple[str, str]]) -> None:
    """Display commands table."""
    table = Table(
        title="[bold cyan]Commands (Slash Commands)[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Command", style="yellow", width=30)
    table.add_column("Description", style="dim", width=60)

    for name, desc in commands:
        table.add_row(f"/{name}", desc)

    console.print(table)
    console.print()


def display_skills(skills: list[tuple[str, str]]) -> None:
    """Display skills table."""
    table = Table(
        title="[bold cyan]Skills[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Skill", style="blue", width=30)
    table.add_column("Description", style="dim", width=60)

    for name, desc in skills:
        table.add_row(name, desc)

    console.print(table)
    console.print()


def display_hooks(settings: dict) -> None:
    """Display hooks configuration."""
    hooks = settings.get("hooks", {})

    table = Table(
        title="[bold cyan]Hooks[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Event", style="cyan", width=20)
    table.add_column("Matcher", style="yellow", width=20)
    table.add_column("Command", style="dim", width=40)
    table.add_column("Status", justify="center", width=10)

    if hooks:
        for event, hook_list in hooks.items():
            for hook_config in hook_list:
                matcher = hook_config.get("matcher", "*")
                for hook in hook_config.get("hooks", []):
                    cmd = hook.get("command", "N/A")[:40]
                    status = "[green]ON[/green]"
                    table.add_row(event, matcher, cmd, status)
    else:
        table.add_row("No hooks configured", "", "", "[dim]N/A[/dim]")

    console.print(table)
    console.print()


def display_mcps(settings: dict) -> None:
    """Display MCP servers configuration."""
    mcps = settings.get("mcpServers", {})

    table = Table(
        title="[bold cyan]MCP Servers[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Server", style="cyan", width=25)
    table.add_column("Command", style="dim", width=50)
    table.add_column("Status", justify="center", width=10)

    for name, config in sorted(mcps.items()):
        cmd = config.get("command", "")
        args = config.get("args", [])
        cmd_str = f"{cmd} {' '.join(args[:2])}"[:50]
        if len(cmd_str) == 50:
            cmd_str += "..."

        disabled = config.get("disabled", False)
        if disabled:
            status = "[red]OFF[/red]"
        else:
            status = "[green]ON[/green]"

        table.add_row(name, cmd_str, status)

    console.print(table)
    console.print()


def display_permissions(settings: dict) -> None:
    """Display permissions configuration."""
    perms = settings.get("permissions", {})
    allow = perms.get("allow", [])
    deny = perms.get("deny", [])

    table = Table(
        title="[bold cyan]Permissions[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Type", style="cyan", width=10)
    table.add_column("Permission", style="dim", width=80)

    for perm in allow[:15]:  # Limit to first 15
        table.add_row("[green]Allow[/green]", perm)

    if len(allow) > 15:
        table.add_row("[green]Allow[/green]", f"... and {len(allow) - 15} more")

    for perm in deny:
        table.add_row("[red]Deny[/red]", perm)

    console.print(table)
    console.print()


def display_plugins(settings: dict) -> None:
    """Display enabled plugins."""
    plugins = settings.get("enabledPlugins", {})

    if not plugins:
        return

    table = Table(
        title="[bold cyan]Plugins[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Plugin", style="cyan", width=40)
    table.add_column("Status", justify="center", width=10)

    for name, enabled in sorted(plugins.items()):
        if enabled:
            status = "[green]ON[/green]"
        else:
            status = "[red]OFF[/red]"
        table.add_row(name, status)

    console.print(table)
    console.print()


def main():
    """Main function to display the configuration dashboard."""
    console.print()
    console.print(
        Panel.fit(
            "[bold white]Claude Code Configuration Dashboard[/bold white]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    console.print()

    # Load settings
    settings = load_settings()

    # Get all configurations
    agents = get_agents()
    commands = get_commands()
    skills = get_skills()

    # Display summary
    summary = (
        f"[cyan]Agents:[/cyan] {len(agents)}  "
        f"[yellow]Commands:[/yellow] {len(commands)}  "
        f"[blue]Skills:[/blue] {len(skills)}  "
        f"[green]MCPs:[/green] {len(settings.get('mcpServers', {}))}"
    )
    console.print(Panel(summary, title="Summary", border_style="dim"))
    console.print()

    # Display each section
    if agents:
        display_agents(agents)

    if commands:
        display_commands(commands)

    if skills:
        display_skills(skills)

    display_hooks(settings)
    display_mcps(settings)
    display_plugins(settings)
    display_permissions(settings)

    # Footer
    console.print(
        f"[dim]Config location: {CLAUDE_DIR}[/dim]",
        justify="center",
    )
    console.print()


if __name__ == "__main__":
    main()

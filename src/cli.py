"""Command-line interface for CC Status Line."""

from __future__ import annotations

import json
import os

import click
import yaml

from .config import ConfigManager
from .core import StatusLineEngine
from .setup import SetupWizard


def _get_claude_context() -> dict | None:
    """Get Claude Code context from stdin if available."""
    try:
        import sys

        if not sys.stdin.isatty():
            # Read JSON from stdin (Claude Code integration)
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                # Validate JSON input from Claude Code
                context = json.loads(stdin_data)
                return context
    except (json.JSONDecodeError, OSError):
        # Not running from Claude Code, continue normally
        pass
    return None


@click.command()
@click.option(
    "--init", "init_project", is_flag=True, help="Initialize configuration for current project"
)
@click.option("--setup", "setup_project", is_flag=True, help="Alias for --init")
@click.option("--config", "show_config", is_flag=True, help="Show current project configuration")
@click.option("--config-info", is_flag=True, help="Show configuration file locations and sources")
@click.option("--list-projects", "list_projects", is_flag=True, help="List all configured projects")
@click.option("--reset", is_flag=True, help="Reset configuration for current project")
@click.option("--global-config", is_flag=True, help="Show global configuration")
@click.option("--config-dir", help="Custom configuration directory")
@click.version_option(version="1.0.0", prog_name="CC Status Line")
def main(
    init_project,
    setup_project,
    show_config,
    config_info,
    list_projects,
    reset,
    global_config,
    config_dir,
):
    """CC Status Line - Claude Code status line tool with git repositories and development server detection."""

    config_manager = ConfigManager(custom_config_dir=config_dir)

    # Handle configuration commands
    if init_project or setup_project:
        wizard = SetupWizard(config_manager)
        config = wizard.run_setup()
        config_manager.save_project_config(config)

        click.echo(f"\n✅ Configuration saved for project: {config['name']}")
        click.echo(f"📁 Project ID: {config_manager.get_project_id()}")
        click.echo("\n🚀 Run 'cc-status-line' to see your status line!")
        return

    if show_config:
        config = config_manager.get_config()
        project_id = config_manager.get_project_id()

        click.echo(f"📋 Current Configuration ({project_id})")
        click.echo("=" * 50)

        # Convert to YAML for better readability
        click.echo(yaml.safe_dump(config, indent=2, default_flow_style=False))
        return

    if config_info:
        info = config_manager.get_config_info()

        click.echo("📁 Configuration Information")
        click.echo("=" * 40)
        click.echo(f"Project ID: {info['project_id']}")
        click.echo(f"Config Directory: {info['config_dir']}")
        click.echo()
        click.echo("Configuration Files:")
        click.echo(
            f"  🌐 Global:  {info['global_config']} {'✅' if info['sources']['global_exists'] else '❌'}"
        )
        click.echo(
            f"  📁 Project: {info['project_config']} {'✅' if info['sources']['project_exists'] else '❌'}"
        )
        click.echo(
            f"  📄 Local:   {info['local_config']} {'✅' if info['sources']['local_exists'] else '❌'}"
        )
        click.echo()
        click.echo("Environment Variables:")
        click.echo(f"  CCSL_CONFIG_DIR: {os.getenv('CCSL_CONFIG_DIR', 'not set')}")
        click.echo(f"  XDG_CONFIG_HOME: {os.getenv('XDG_CONFIG_HOME', 'not set')}")
        return

    if list_projects:
        projects = config_manager.list_projects()

        if projects:
            click.echo("📁 Configured Projects:")
            for project in projects:
                click.echo(f"  • {project['name']} ({project['type']}) - {project['root_path']}")
        else:
            click.echo("📁 No projects configured yet.")
            click.echo("💡 Run 'cc-status-line --init' in a project directory to get started.")
        return

    if global_config:
        config = config_manager.get_global_config()
        click.echo("🌐 Global Configuration:")
        click.echo(json.dumps(config, indent=2))
        return

    if reset:
        project_id = config_manager.get_project_id()

        if config_manager.delete_project_config(project_id):
            click.echo("✅ Configuration reset for current project.")
        else:
            click.echo("❌ No configuration found to reset.")
        return

    # Run status line display
    display_status_line(config_manager)


def display_status_line(config_manager: ConfigManager):
    """Display the status line for current project."""
    # Handle Claude Code JSON input from stdin
    claude_context = _get_claude_context()

    # Get merged configuration from all sources
    # Use workspace from Claude context if available
    project_path = None
    if claude_context and "workspace" in claude_context:
        project_path = claude_context["workspace"].get("current_working_directory")

    config = config_manager.get_config(project_path)

    if not config.get("repositories") and not config.get("servers"):
        # Output single line for Claude Code compatibility
        click.echo("❌ No configuration - Run 'cc-status-line --init'")
        return

    # Create and run status line engine
    engine = StatusLineEngine(config)
    status_lines = engine.generate_status_line()

    # Display status lines
    for line in status_lines:
        click.echo(line)


if __name__ == "__main__":
    main()

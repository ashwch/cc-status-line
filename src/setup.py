"""Interactive setup wizard for CC Status Line."""

from __future__ import annotations

import time
from typing import Any

import click

from .config import ConfigManager
from .detection import ProjectDetector


class SetupWizard:
    """Interactive setup wizard for project configuration."""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.detector = ProjectDetector(self.config_manager._find_git_root() or ".")

    def run_setup(self) -> dict[str, Any]:
        """Run interactive setup wizard."""
        click.echo("🚀 CC Status Line Setup Wizard")
        click.echo("===============================")

        # Detect current project
        project_path = self.detector.project_path
        click.echo(f"📁 Current directory: {project_path}")

        # Get project details
        name = self._get_project_name()
        project_type = self._get_project_type()

        # Configure repositories
        repositories = self._configure_repositories(project_type)

        # Configure servers
        servers = self._configure_servers()

        # Configure output format
        output_format = self._configure_output_format()

        # Configure system monitoring
        system_monitoring = self._configure_system_monitoring()

        # Create config dictionary
        config = {
            "name": name,
            "type": project_type,
            "root_path": str(project_path),
            "repositories": repositories,
            "servers": servers,
            "output_format": output_format,
            "system_monitoring": system_monitoring,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return config

    def _get_project_name(self) -> str:
        """Get project name from user."""
        suggested_name = self.detector.project_path.name
        return click.prompt("📋 Project name", default=suggested_name, show_default=True)

    def _get_project_type(self) -> str:
        """Get project type from user."""
        detected_type = self.detector.detect_project_type()

        click.echo(f"🔍 Detected project type: {detected_type}")

        types = ["monolith", "single", "multi", "custom"]
        type_descriptions = {
            "monolith": "Monolith with git submodules",
            "single": "Single git repository",
            "multi": "Multiple repositories in workspace",
            "custom": "Custom configuration",
        }

        click.echo("\nAvailable project types:")
        for i, ptype in enumerate(types, 1):
            marker = "👈" if ptype == detected_type else "  "
            click.echo(f"  {i}. {ptype} - {type_descriptions[ptype]} {marker}")

        choice = click.prompt(
            "Select project type",
            type=click.IntRange(1, len(types)),
            default=types.index(detected_type) + 1,
            show_default=True,
        )

        return types[choice - 1]

    def _configure_repositories(self, project_type: str) -> list[dict[str, Any]]:
        """Configure repositories interactively."""
        suggested_repos = self.detector.suggest_repositories()

        click.echo(f"\n📂 Repository Configuration ({len(suggested_repos)} detected)")

        if suggested_repos and click.confirm("Use detected repositories?", default=True):
            repositories = suggested_repos
        else:
            repositories = self._manual_repo_config()

        # Show final configuration
        click.echo("\n📂 Final repository configuration:")
        for repo in repositories:
            click.echo(f"  • {repo['name']}: {repo['path']} ({repo['type']})")

        return repositories

    def _manual_repo_config(self) -> list[dict[str, Any]]:
        """Manual repository configuration."""
        repositories = []

        click.echo("Enter repositories (press Enter with empty name to finish):")
        while True:
            try:
                name = click.prompt("Repository name", default="", show_default=False)
                if not name:
                    break

                path = click.prompt("Repository path", default=".")
                repo_type = click.prompt(
                    "Repository type",
                    type=click.Choice(["main", "submodule", "repository"]),
                    default="repository",
                )

                repositories.append({"name": name.upper(), "path": path, "type": repo_type})
            except (EOFError, KeyboardInterrupt):
                break

        return repositories

    def _configure_servers(self) -> list[dict[str, Any]]:
        """Configure server detection."""
        suggested_servers = self.detector.suggest_servers()

        click.echo(f"\n🖥️  Server Detection ({len(suggested_servers)} detected)")

        if suggested_servers:
            click.echo("Detected servers:")
            for server in suggested_servers:
                click.echo(f"  • {server['emoji']} {server['name']}: ports {server['ports']}")

            if click.confirm("Use detected servers?", default=True):
                return suggested_servers

        return self._manual_server_config()

    def _manual_server_config(self) -> list[dict[str, Any]]:
        """Manual server configuration."""
        servers = []

        click.echo("Enter server configurations (press Enter with empty name to finish):")
        while True:
            try:
                name = click.prompt("Server name", default="", show_default=False)
                if not name:
                    break

                ports_str = click.prompt("Ports (comma-separated)", default="3000,8000")
                try:
                    ports = [int(p.strip()) for p in ports_str.split(",") if p.strip()]
                    if not ports:
                        ports = [3000]
                except ValueError:
                    click.echo("⚠️  Invalid port format, using default [3000]")
                    ports = [3000]

                emoji = click.prompt("Emoji", default="🖥️")

                servers.append({"name": name, "ports": ports, "emoji": emoji, "enabled": True})
            except (EOFError, KeyboardInterrupt):
                break

        return servers

    def _configure_output_format(self) -> dict[str, Any]:
        """Configure output formatting."""
        click.echo("\n🎨 Output Format Configuration")

        multiline = click.confirm("Use multiline output?", default=True)
        colors = click.confirm("Enable colors?", default=True)
        compact = click.confirm("Use compact mode?", default=False)

        return {
            "multiline": multiline,
            "colors": colors,
            "compact": compact,
            "show_performance": False,
            "show_changes": True,
        }

    def _configure_system_monitoring(self) -> dict[str, Any]:
        """Configure system monitoring."""
        click.echo("\n📊 System Monitoring Configuration")

        enabled = click.confirm("Enable system monitoring?", default=False)

        return {"enabled": enabled, "battery": enabled, "cpu": enabled, "memory": enabled}

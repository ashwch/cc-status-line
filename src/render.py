"""Status line rendering for CC Status Line."""

from __future__ import annotations

import os
from typing import Any

from .git import RepoStatus


class StatusLineRenderer:
    """Render status line output."""

    # ANSI color codes
    COLORS = {
        "reset": "\033[0m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "red": "\033[31m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_red": "\033[91m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "dim": "\033[2m",
    }

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.use_colors = config.get("output_format", {}).get("colors", True) and not os.getenv(
            "NO_COLOR"
        )
        self.multiline = config.get("output_format", {}).get("multiline", True)

    def _colorize(self, text: str, color: str) -> str:
        """Apply ANSI color to text if colors are enabled."""
        if not self.use_colors or color not in self.COLORS:
            return text
        return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"

    def render(self, repos: list[RepoStatus], servers: list[dict[str, Any]]) -> list[str]:
        """Render complete status line."""
        lines = []

        if self.multiline:
            # Multi-line format
            if repos:
                lines.append(self._render_repositories(repos))
            if servers:
                lines.append(self._render_servers(servers))
        else:
            # Single line format
            parts = []
            if repos:
                parts.append(f"📂 {len(repos)} repos")
            if servers:
                parts.append(f"🖥️ {len(servers)} servers")

            if parts:
                lines.append(" │ ".join(parts))

        return lines

    def _render_repositories(self, repos: list[RepoStatus]) -> str:
        """Render repository status line."""
        repo_parts = []

        for repo in repos:
            status_emoji = self._get_status_emoji(repo.behind, repo.has_changes)
            behind_text = self._colorize(f"-{repo.behind}", "red") if repo.behind > 0 else ""
            changes_marker = self._colorize("*", "yellow") if repo.has_changes else ""
            branch_colored = self._colorize(repo.branch, self._get_branch_color(repo.branch))
            repo_name_colored = self._colorize(repo.name, "bright_cyan")

            repo_part = (
                f"{status_emoji}{repo_name_colored}:{branch_colored}{behind_text}{changes_marker}"
            )
            repo_parts.append(repo_part)

        return f"📂 Repos ▶ {' │ '.join(repo_parts)}"

    def _render_servers(self, servers: list[dict[str, Any]]) -> str:
        """Render server status line."""
        server_parts = []

        for server in servers:
            server_name_colored = self._colorize(server["name"], "bright_green")
            port_colored = self._colorize(str(server["port"]), "bright_yellow")
            server_parts.append(f"{server['emoji']}{server_name_colored}:{port_colored}")

        return f"🖥️ Servers ▶ {' │ '.join(server_parts)}"

    def _get_branch_color(self, branch_name: str) -> str:
        """Get color for branch name based on branch type."""
        if branch_name in ("main", "master"):
            return "bright_green"
        elif branch_name.startswith(("feat", "feature")):
            return "bright_blue"
        elif branch_name.startswith(("fix", "hotfix", "bugfix")):
            return "bright_red"
        elif branch_name.startswith(("dev", "develop")):
            return "bright_yellow"
        elif branch_name.startswith("release"):
            return "bright_magenta"
        return "cyan"

    def _get_status_emoji(self, behind: int, has_changes: bool) -> str:
        """Get appropriate status emoji."""
        if has_changes:
            return "🟡"
        elif behind > 0:
            return "🔴" if behind > 5 else "⚠️"
        else:
            return "✅"

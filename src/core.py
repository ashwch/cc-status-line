"""Core status line engine for CC Status Line."""

from __future__ import annotations

import os
from typing import Any

from .detection import ServerDetector
from .git import GitManager
from .logger import get_logger
from .render import StatusLineRenderer


class StatusLineEngine:
    """Main status line processing engine."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.logger = get_logger("core", config)
        self.git_manager = GitManager()
        self.server_detector = ServerDetector()
        self.renderer = StatusLineRenderer(config)

        self.logger.debug(
            f"StatusLineEngine initialized for project: {config.get('name', 'unknown')}"
        )

    def generate_status_line(self) -> list[str]:
        """Generate complete status line."""
        try:
            self.logger.debug("Starting status line generation")

            # Get repository statuses
            repos = self._get_repository_statuses()
            self.logger.debug(f"Found {len(repos)} repositories")

            # Detect servers
            servers = self._detect_active_servers()
            self.logger.debug(f"Detected {len(servers)} active servers")

            # Render output
            result = self.renderer.render(repos, servers)
            self.logger.debug("Status line generation completed successfully")
            return result

        except Exception:
            self.logger.exception("Failed to generate status line")
            return ["❌ Setup needed: cc-status-line --init"]

    def _get_repository_statuses(self) -> list[Any]:
        """Get status for all configured repositories."""
        repos = []
        project_root = self.config.get("root_path", os.getcwd())

        for repo_config in self.config.get("repositories", []):
            repo_status = self.git_manager.get_repo_status(repo_config, project_root)
            if repo_status:
                repos.append(repo_status)

        return repos

    def _detect_active_servers(self) -> list[dict[str, Any]]:
        """Detect active servers."""
        server_configs = self.config.get("servers", [])
        return self.server_detector.detect_servers(server_configs)

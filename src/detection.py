"""Project detection and auto-configuration for CC Status Line."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


class ProjectDetector:
    """Detect project type and suggest configuration."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def detect_project_type(self) -> str:
        """Detect the type of project."""
        if self._is_monolith():
            return "monolith"
        elif self._is_multi_repo():
            return "multi"
        elif self._is_single_repo():
            return "single"
        return "custom"

    def _is_monolith(self) -> bool:
        """Check if this is a monolith with submodules."""
        gitmodules = self.project_path / ".gitmodules"
        return gitmodules.exists() and len(self._get_submodules()) > 2

    def _is_multi_repo(self) -> bool:
        """Check if this is a multi-repository workspace."""
        # Look for multiple git repositories in subdirectories
        git_repos = list(self.project_path.glob("*/.git"))
        return len(git_repos) > 1

    def _is_single_repo(self) -> bool:
        """Check if this is a single repository."""
        return (self.project_path / ".git").exists()

    def _get_submodules(self) -> list[str]:
        """Get list of git submodules."""
        gitmodules = self.project_path / ".gitmodules"
        if not gitmodules.exists():
            return []

        try:
            with open(gitmodules) as f:
                content = f.read()

            submodules = []
            for line in content.split("\n"):
                if line.strip().startswith("path = "):
                    path = line.split("=", 1)[1].strip()
                    submodules.append(path)
            return submodules
        except OSError:
            return []

    def suggest_repositories(self) -> list[dict[str, Any]]:
        """Suggest repository configuration based on project type."""
        project_type = self.detect_project_type()

        if project_type == "monolith":
            return self._suggest_monolith_repos()
        elif project_type == "multi":
            return self._suggest_multi_repos()
        elif project_type == "single":
            return self._suggest_single_repo()
        return []

    def _suggest_monolith_repos(self) -> list[dict[str, Any]]:
        """Suggest repositories for monolith project."""
        repos = [{"name": "MAIN", "path": ".", "type": "main"}]

        for submodule in self._get_submodules():
            name = Path(submodule).name.upper()
            repos.append({"name": name, "path": submodule, "type": "submodule"})

        return repos

    def _suggest_multi_repos(self) -> list[dict[str, Any]]:
        """Suggest repositories for multi-repo workspace."""
        repos = []

        for git_dir in self.project_path.glob("*/.git"):
            repo_path = git_dir.parent
            name = repo_path.name.upper()
            repos.append(
                {
                    "name": name,
                    "path": str(repo_path.relative_to(self.project_path)),
                    "type": "repository",
                }
            )

        return repos

    def _suggest_single_repo(self) -> list[dict[str, Any]]:
        """Suggest repository for single repo project."""
        return [{"name": self.project_path.name.upper(), "path": ".", "type": "main"}]

    def suggest_servers(self) -> list[dict[str, Any]]:
        """Suggest server configuration based on project files."""
        servers = []

        # Generic development server patterns - users can extend via config
        server_patterns = [
            {
                "name": "Flask",
                "ports": [5000, 5001, 8000],
                "emoji": "🌶️",
                "patterns": ["app.py", "wsgi.py", "application.py", "requirements.txt"],
            },
            {
                "name": "Python",
                "ports": [8000, 5000],
                "emoji": "🐍",
                "patterns": ["*.py", "requirements.txt", "pyproject.toml"],
            },
            {
                "name": "Node",
                "ports": [3000, 8080],
                "emoji": "🟢",
                "patterns": ["package.json", "node_modules/"],
            },
            {
                "name": "Web",
                "ports": [8080, 3000, 5173],
                "emoji": "🌐",
                "patterns": ["index.html", "*.css", "*.js"],
            },
            {
                "name": "Docker",
                "ports": [80, 443, 8080],
                "emoji": "🐳",
                "patterns": ["docker-compose.yml", "Dockerfile"],
            },
            {
                "name": "Database",
                "ports": [5432, 3306, 27017],
                "emoji": "🗄️",
                "patterns": ["*.sql", "migrations/"],
            },
        ]

        for pattern in server_patterns:
            if self._matches_pattern(pattern["patterns"]):
                servers.append(
                    {
                        "name": pattern["name"],
                        "ports": pattern["ports"],
                        "emoji": pattern["emoji"],
                        "enabled": True,
                    }
                )

        return servers

    def _matches_pattern(self, patterns: list[str]) -> bool:
        """Check if project matches file patterns."""
        for pattern in patterns:
            matches = list(self.project_path.rglob(pattern))
            if matches:
                return True
        return False


class ServerDetector:
    """Cross-platform server detection."""

    def detect_servers(self, server_configs: list[dict[str, Any]]) -> list[dict[str, str | int]]:
        """Detect active servers based on configuration."""
        servers = []

        for config in server_configs:
            if not config.get("enabled", True):
                continue

            for port in config["ports"]:
                if self._is_port_active(port):
                    servers.append({"name": config["name"], "port": port, "emoji": config["emoji"]})
                    break  # Only show one instance per server type

        return servers

    def _is_port_active(self, port: int) -> bool:
        """Check if port is active using platform-specific commands."""
        port_str = str(port)

        try:
            if sys.platform == "win32":
                # Windows: Use netstat
                result = subprocess.run(
                    ["netstat", "-an"], capture_output=True, text=True, timeout=2.0
                )
                return f":{port_str}" in result.stdout
            else:
                # Unix-like: Try lsof first, fallback to netstat
                try:
                    result = subprocess.run(
                        ["lsof", f"-i:{port_str}"], capture_output=True, text=True, timeout=2.0
                    )
                    return bool(result.stdout.strip())
                except (OSError, FileNotFoundError):
                    # lsof not available, try netstat
                    result = subprocess.run(
                        ["netstat", "-an"], capture_output=True, text=True, timeout=2.0
                    )
                    return f":{port_str}" in result.stdout
        except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
            return False

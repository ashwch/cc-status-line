"""Configuration management for CC Status Line."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

import yaml

# ProjectConfig removed - using plain dictionaries for YAML compatibility


class ConfigManager:
    """YAML-based configuration management with layered fallbacks."""

    def __init__(self, custom_config_dir: str | None = None):
        self.custom_config_dir = custom_config_dir
        self.config_dir = self._get_config_dir()
        self.global_config_file = self.config_dir / "config.yaml"
        self.projects_dir = self.config_dir / "projects"
        self.templates_dir = self.config_dir / "templates"
        self._ensure_config_dirs()

    def _get_config_dir(self) -> Path:
        """Get config directory with user choice support."""
        # 1. Custom directory (CLI override)
        if self.custom_config_dir:
            return Path(self.custom_config_dir).expanduser()

        # 2. Environment variable override
        if ccsl_config := os.getenv("CCSL_CONFIG_DIR"):
            return Path(ccsl_config).expanduser()

        # 3. XDG Base Directory standard
        if xdg_config := os.getenv("XDG_CONFIG_HOME"):
            return Path(xdg_config) / "cc-status-line"

        # 4. Default fallback
        return Path.home() / ".config" / "cc-status-line"

    def _ensure_config_dirs(self) -> None:
        """Ensure all configuration directories exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)

    def get_project_id(self, project_path: str | None = None) -> str:
        """Get unique project identifier based on git remote URL."""
        if project_path is None:
            project_path = self._find_git_root() or os.getcwd()

        # Try to get git remote URL for global uniqueness
        git_remote = self._get_git_remote_url(project_path)
        if git_remote:
            # Convert git remote to safe filename: github.com/user/repo -> github-com-user-repo
            safe_name = re.sub(r"[^\w\-.]", "-", git_remote.lower())
            safe_name = re.sub(r"-+", "-", safe_name)  # Collapse multiple dashes
            return safe_name.strip("-")

        # Fallback to path hash for non-git projects
        normalized_path = Path(project_path).resolve()
        project_hash = hashlib.sha256(str(normalized_path).encode()).hexdigest()[:16]
        return f"local-{project_hash}"

    def _get_git_remote_url(self, project_path: str) -> str | None:
        """Get git remote URL for project identification."""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                # Normalize different git URL formats
                # ssh: git@github.com:user/repo.git -> github.com/user/repo
                # https: https://github.com/user/repo.git -> github.com/user/repo
                if url.startswith("git@"):
                    url = url.replace("git@", "").replace(":", "/")
                elif url.startswith("https://"):
                    url = url[8:]  # Remove https://

                # Remove .git suffix
                if url.endswith(".git"):
                    url = url[:-4]

                return url
        except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
            pass
        return None

    def _find_git_root(self) -> str | None:
        """Find git repository root."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                return str(current)
            current = current.parent
        return None

    def get_config(self, project_path: str | None = None) -> dict[str, Any]:
        """Get complete configuration with layered resolution."""
        # 1. Start with global defaults
        config = self._get_default_global_config()

        # 2. Load global config (templates, user defaults)
        global_config = self._load_yaml_file(self.global_config_file)
        if global_config:
            config = self._deep_merge(config, global_config)

        # 3. Load project-specific config
        project_id = self.get_project_id(project_path)
        project_file = self.projects_dir / f"{project_id}.yaml"
        project_config = self._load_yaml_file(project_file)
        if project_config:
            config = self._deep_merge(config, project_config)

        # 4. Load local overrides
        if project_path is None:
            project_path = self._find_git_root() or os.getcwd()
        local_file = Path(project_path) / ".cc-status-line.yaml"
        local_config = self._load_yaml_file(local_file)
        if local_config:
            config = self._deep_merge(config, local_config)

        return config

    def _load_yaml_file(self, file_path: Path) -> dict[str, Any] | None:
        """Load and parse YAML file safely."""
        if not file_path.exists():
            return None

        try:
            with open(file_path) as f:
                content = yaml.safe_load(f)
                return content if isinstance(content, dict) else None
        except (yaml.YAMLError, OSError):
            return None

    def _deep_merge(self, base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        """Deep merge two dictionaries, with override taking precedence."""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def get_global_config(self) -> dict[str, Any]:
        """Get global configuration."""
        config = self._load_yaml_file(self.global_config_file)
        if config:
            return self._deep_merge(self._get_default_global_config(), config)
        return self._get_default_global_config()

    def save_global_config(self, config: dict[str, Any]) -> None:
        """Save global configuration."""
        with open(self.global_config_file, "w") as f:
            yaml.safe_dump(config, f, indent=2, default_flow_style=False)

    def get_project_config(self, project_id: str | None = None) -> dict[str, Any] | None:
        """Get project-specific configuration."""
        if project_id is None:
            project_id = self.get_project_id()

        project_file = self.projects_dir / f"{project_id}.yaml"
        return self._load_yaml_file(project_file)

    def save_project_config(self, config: dict[str, Any], project_id: str | None = None) -> None:
        """Save project-specific configuration."""
        if project_id is None:
            project_id = self.get_project_id()

        # Update timestamp
        config["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        project_file = self.projects_dir / f"{project_id}.yaml"
        with open(project_file, "w") as f:
            yaml.safe_dump(config, f, indent=2, default_flow_style=False)

    def save_local_config(self, config: dict[str, Any], project_path: str | None = None) -> None:
        """Save local project overrides."""
        if project_path is None:
            project_path = self._find_git_root() or os.getcwd()

        local_file = Path(project_path) / ".cc-status-line.yaml"
        with open(local_file, "w") as f:
            yaml.safe_dump(config, f, indent=2, default_flow_style=False)

    def delete_project_config(self, project_id: str | None = None) -> bool:
        """Delete project-specific configuration."""
        if project_id is None:
            project_id = self.get_project_id()

        project_file = self.projects_dir / f"{project_id}.yaml"
        if project_file.exists():
            project_file.unlink()
            return True
        return False

    def list_projects(self) -> list[dict[str, Any]]:
        """List all configured projects."""
        projects = []
        for config_file in self.projects_dir.glob("*.yaml"):
            config = self._load_yaml_file(config_file)
            if config:
                config["id"] = config_file.stem
                projects.append(config)
        return projects

    def get_config_info(self, project_path: str | None = None) -> dict[str, Any]:
        """Get information about configuration sources."""
        if project_path is None:
            project_path = self._find_git_root() or os.getcwd()

        project_id = self.get_project_id(project_path)
        project_file = self.projects_dir / f"{project_id}.yaml"
        local_file = Path(project_path) / ".cc-status-line.yaml"

        return {
            "project_id": project_id,
            "config_dir": str(self.config_dir),
            "global_config": str(self.global_config_file),
            "project_config": str(project_file),
            "local_config": str(local_file),
            "sources": {
                "global_exists": self.global_config_file.exists(),
                "project_exists": project_file.exists(),
                "local_exists": local_file.exists(),
            },
        }

    def _get_default_global_config(self) -> dict[str, Any]:
        """Get default global configuration with no project-specific assumptions."""
        return {
            "version": "1.0.0",
            "output_format": {
                "colors": True,
                "multiline": True,
                "compact": False,
                "show_changes": True,
            },
            "system_monitoring": {
                "enabled": False,  # Disabled by default for Claude Code compatibility
                "battery": False,
                "cpu": False,
                "memory": False,
            },
            "server_templates": {
                # Generic templates - users can extend these
                "web": {
                    "name": "Web",
                    "ports": [3000, 8000, 8080],
                    "emoji": "🌐",
                    "patterns": ["index.html", "package.json"],
                },
                "api": {
                    "name": "API",
                    "ports": [8000, 5000, 3001],
                    "emoji": "🔌",
                    "patterns": ["server.py", "app.py", "main.py"],
                },
                "flask": {
                    "name": "Flask",
                    "ports": [5000, 5001, 8000],
                    "emoji": "🌶️",
                    "patterns": ["app.py", "wsgi.py", "application.py", "requirements.txt"],
                },
                "database": {
                    "name": "Database",
                    "ports": [5432, 3306, 27017],
                    "emoji": "🗄️",
                    "patterns": ["docker-compose.yml"],
                },
            },
        }

"""Git repository status management for CC Status Line."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RepoStatus:
    """Repository status information."""

    name: str
    branch: str
    behind: int
    has_changes: bool
    path: str


class GitManager:
    """Git repository management."""

    @staticmethod
    def run_git_command(cmd_args: list[str], cwd: str) -> tuple[str, bool]:
        """Run git command safely and return output and success status."""
        try:
            result = subprocess.run(cmd_args, capture_output=True, text=True, cwd=cwd, timeout=5.0)
            return result.stdout.strip(), result.returncode == 0
        except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
            return "", False

    def get_repo_status(self, repo_config: dict[str, Any], project_root: str) -> RepoStatus | None:
        """Get status for a single repository."""
        repo_path = Path(project_root) / repo_config["path"]

        if not repo_path.exists() or not (repo_path / ".git").exists():
            return None

        # Get branch name
        branch_output, branch_success = self.run_git_command(
            ["git", "symbolic-ref", "--short", "HEAD"], str(repo_path)
        )
        if not branch_success:
            # Fallback to short hash if not on a branch
            branch_output, _ = self.run_git_command(
                ["git", "rev-parse", "--short", "HEAD"], str(repo_path)
            )
        branch_name = branch_output or "detached"

        # Get commits behind upstream
        behind_output, success = self.run_git_command(
            ["git", "rev-list", "--count", "HEAD..@{u}"], str(repo_path)
        )
        behind = int(behind_output) if success and behind_output.isdigit() else 0

        # Check for uncommitted changes
        changes_output, _ = self.run_git_command(["git", "status", "--porcelain"], str(repo_path))
        has_changes = bool(changes_output.strip())

        return RepoStatus(
            name=repo_config["name"],
            branch=branch_name,
            behind=behind,
            has_changes=has_changes,
            path=repo_config["path"],
        )

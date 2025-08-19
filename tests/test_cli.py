"""Tests for CLI functionality."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cli import main


class TestCLI:
    """Test CLI commands."""

    def test_help_command(self):
        """Test --help command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "CC Status Line" in result.output

    def test_version_command(self):
        """Test --version command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "CC Status Line, version 1.0.0" in result.output

    @patch("cli.ConfigManager")
    def test_config_info_command(self, mock_config):
        """Test --config-info command."""
        mock_config.return_value.get_config_info.return_value = {
            "project_id": "test-project",
            "config_dir": "/test/config",
            "global_config": "/test/global.yaml",
            "project_config": "/test/project.yaml",
            "local_config": "/test/local.yaml",
            "sources": {
                "global_exists": False,
                "project_exists": False,
                "local_exists": False,
            },
        }

        runner = CliRunner()
        result = runner.invoke(main, ["--config-info"])
        assert result.exit_code == 0
        assert "Configuration Information" in result.output

    @patch("sys.stdin.isatty", return_value=False)
    @patch("sys.stdin.read")
    @patch("cli.StatusLineEngine")
    @patch("cli.ConfigManager")
    def test_claude_code_integration(self, mock_config, mock_engine, mock_stdin, mock_isatty):
        """Test Claude Code JSON stdin integration."""
        # Mock stdin with Claude Code JSON
        claude_context = {
            "session_id": "test",
            "workspace": {"current_working_directory": "/test/path"},
        }
        mock_stdin.return_value = json.dumps(claude_context)

        # Mock configuration
        mock_config.return_value.get_config.return_value = {
            "repositories": [{"name": "TEST", "path": "."}],
            "servers": [{"name": "Test", "ports": [3000]}],
        }

        # Mock engine
        mock_engine.return_value.generate_status_line.return_value = ["📂 Repos ▶ 🟡TEST:main*"]

        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code == 0
        assert "📂 Repos" in result.output

    def test_no_configuration_error(self):
        """Test behavior when no configuration found."""
        with patch("cli.ConfigManager") as mock_config:
            mock_config.return_value.get_config.return_value = {"repositories": [], "servers": []}

            runner = CliRunner()
            result = runner.invoke(main, [])
            assert result.exit_code == 0
            assert "No configuration" in result.output

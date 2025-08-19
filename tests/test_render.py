"""Tests for rendering functionality."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git import RepoStatus
from render import StatusLineRenderer


class TestStatusLineRenderer:
    """Test status line rendering."""

    def test_init_with_colors(self):
        """Test renderer initialization with colors enabled."""
        config = {"output_format": {"colors": True, "multiline": True}}
        renderer = StatusLineRenderer(config)
        assert renderer.use_colors is True
        assert renderer.multiline is True

    def test_init_no_color_env(self):
        """Test renderer respects NO_COLOR environment variable."""
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            config = {"output_format": {"colors": True, "multiline": True}}
            renderer = StatusLineRenderer(config)
            assert renderer.use_colors is False

    def test_colorize_method(self):
        """Test color application."""
        config = {"output_format": {"colors": True}}
        renderer = StatusLineRenderer(config)

        colored = renderer._colorize("test", "red")
        assert "\033[31m" in colored
        assert "\033[0m" in colored
        assert "test" in colored

    def test_colorize_no_colors(self):
        """Test colorize without colors enabled."""
        config = {"output_format": {"colors": False}}
        renderer = StatusLineRenderer(config)

        result = renderer._colorize("test", "red")
        assert result == "test"

    def test_branch_color_main(self):
        """Test main branch gets correct color."""
        config = {"output_format": {"colors": True}}
        renderer = StatusLineRenderer(config)

        color = renderer._get_branch_color("main")
        assert color == "bright_green"

    def test_branch_color_feature(self):
        """Test feature branch gets correct color."""
        config = {"output_format": {"colors": True}}
        renderer = StatusLineRenderer(config)

        color = renderer._get_branch_color("feature/new-ui")
        assert color == "bright_blue"

    def test_render_repositories(self):
        """Test repository rendering."""
        config = {"output_format": {"colors": False, "multiline": True}}
        renderer = StatusLineRenderer(config)

        repos = [
            RepoStatus("TEST", "main", 0, False, "."),
            RepoStatus("API", "feature/auth", 2, True, "api/"),
        ]

        result = renderer._render_repositories(repos)
        assert "📂 Repos ▶" in result
        assert "TEST:main" in result
        assert "API:feature/auth" in result
        assert "*" in result  # changes marker
        assert "-2" in result  # behind marker

    def test_render_servers(self):
        """Test server rendering."""
        config = {"output_format": {"colors": False, "multiline": True}}
        renderer = StatusLineRenderer(config)

        servers = [
            {"name": "Flask", "port": 5000, "emoji": "🌶️"},
            {"name": "React", "port": 3000, "emoji": "⚛️"},
        ]

        result = renderer._render_servers(servers)
        assert "🖥️ Servers ▶" in result
        assert "Flask:5000" in result
        assert "React:3000" in result

    def test_render_multiline_format(self):
        """Test multiline rendering format."""
        config = {"output_format": {"colors": False, "multiline": True}}
        renderer = StatusLineRenderer(config)

        repos = [RepoStatus("TEST", "main", 0, False, ".")]
        servers = [{"name": "Flask", "port": 5000, "emoji": "🌶️"}]

        result = renderer.render(repos, servers)
        assert len(result) == 2  # Two lines for multiline
        assert "📂 Repos" in result[0]
        assert "🖥️ Servers" in result[1]

    def test_render_single_line_format(self):
        """Test single line rendering format."""
        config = {"output_format": {"colors": False, "multiline": False}}
        renderer = StatusLineRenderer(config)

        repos = [RepoStatus("TEST", "main", 0, False, ".")]
        servers = [{"name": "Flask", "port": 5000, "emoji": "🌶️"}]

        result = renderer.render(repos, servers)
        assert len(result) == 1  # Single line
        assert "1 repos" in result[0]
        assert "1 servers" in result[0]

    def test_status_emoji_clean(self):
        """Test status emoji for clean repo."""
        config = {"output_format": {"colors": False}}
        renderer = StatusLineRenderer(config)

        emoji = renderer._get_status_emoji(0, False)
        assert emoji == "✅"

    def test_status_emoji_changes(self):
        """Test status emoji for repo with changes."""
        config = {"output_format": {"colors": False}}
        renderer = StatusLineRenderer(config)

        emoji = renderer._get_status_emoji(0, True)
        assert emoji == "🟡"

    def test_status_emoji_behind(self):
        """Test status emoji for repo behind."""
        config = {"output_format": {"colors": False}}
        renderer = StatusLineRenderer(config)

        # Few commits behind
        emoji = renderer._get_status_emoji(3, False)
        assert emoji == "⚠️"

        # Many commits behind
        emoji = renderer._get_status_emoji(10, False)
        assert emoji == "🔴"

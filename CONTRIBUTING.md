# Contributing to CC Status Line

Thank you for your interest in contributing to CC Status Line! This tool is specifically designed for [Claude Code's status line feature](https://docs.anthropic.com/en/docs/claude-code/statusline).

## Quick Start

1. **Fork and clone** the repository
2. **Set up development environment**:
   ```bash
   cd cc-status-line
   uv sync --dev
   ```
3. **Make your changes** following our guidelines below
4. **Test your changes** thoroughly
5. **Submit a pull request**

## Development Guidelines

### Code Quality Standards

- **Linting**: `uv run ruff check src tests --fix`
- **Formatting**: `uv run ruff format src tests`
- **Type checking**: `uv run pyright src` (warnings OK for now)

### Testing Requirements

- **CLI functionality**: Test all commands work
- **Claude Code integration**: Test JSON stdin handling
- **Cross-platform**: Ensure Windows/macOS/Linux compatibility

### Essential Testing Commands

```bash
# Test basic functionality
uv run cc-status-line --help
uv run cc-status-line --version
uv run cc-status-line --config-info

# Test Claude Code integration
echo '{"workspace": {"current_working_directory": "'$(pwd)'"}}' | uv run cc-status-line

# Test color handling
NO_COLOR=1 uv run cc-status-line
```

## Claude Code Focus

This tool is specifically designed for Claude Code integration. When contributing:

- **Status line output** must be concise and informative
- **Error messages** should be brief and actionable
- **JSON stdin handling** must work reliably
- **Performance** should be under 2 seconds for typical projects

## Pull Request Process

1. **Ensure CI passes** - All GitHub Actions checks must be green
2. **Add tests** for new functionality (basic coverage required)
3. **Update documentation** if you change behavior
4. **Keep commits focused** - One feature/fix per PR

## Server Detection

When adding new server detection:

1. **Add to `src/detection.py`** - Update `server_patterns` list
2. **Add to `src/config.py`** - Update `server_templates`
3. **Use appropriate emoji** - Keep it professional and recognizable
4. **Test thoroughly** - Ensure detection works reliably

### Example Server Addition

```python
# In src/detection.py
{
    "name": "FastAPI",
    "ports": [8000, 8001],
    "emoji": "⚡",
    "patterns": ["main.py", "app.py", "fastapi"]
}

# In src/config.py  
"fastapi": {
    "name": "FastAPI",
    "ports": [8000, 8001],
    "emoji": "⚡",
    "patterns": ["main.py", "app.py", "requirements.txt"]
}
```

## Configuration Changes

When modifying the configuration system:

- **Maintain backward compatibility** with existing configs
- **Test all three layers**: global → project → local
- **Update example configs** in `examples/` directory
- **Document changes** in README.md

## Release Process

1. **Update version** in `src/__init__.py` and `pyproject.toml`
2. **Update CHANGELOG.md** with new features/fixes
3. **Ensure all tests pass** locally and in CI
4. **Create GitHub release** with detailed notes

## Getting Help

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Claude Code docs**: https://docs.anthropic.com/en/docs/claude-code/statusline

## Code of Conduct

- **Be respectful** and inclusive in all interactions
- **Focus on the work** - this is a tool for developers
- **Help others** learn and contribute
- **Keep it professional** - this tool represents the Claude Code ecosystem

Thank you for helping make CC Status Line better for the Claude Code community!
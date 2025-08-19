# Claude Code Configuration for CC Status Line

## Project Overview

**CC Status Line** is a specialized development environment status line tool written in Python specifically designed for [Claude Code's status line feature](https://docs.anthropic.com/en/docs/claude-code/statusline). It provides real-time status information about git repositories, running development servers, and project health directly within the Claude Code interface.

**🎯 Purpose**: This tool is exclusively designed for Claude Code integration and optimized for the Claude Code status line display system.

## Key Features for Claude Code

- **🎯 Claude Code Optimized**: Specifically designed for Claude Code status line integration
- **🔄 Real-time Updates**: Efficient status updates that work with Claude Code's refresh cycle
- **📁 Claude Code Project Support**: Optimized for Claude Code workspace detection (monolith, single repo, multi-repo, custom)
- **⚙️ Layered YAML Configuration**: Global → Project → Local override system
- **🗺️ Cross-Platform**: Windows, macOS, Linux support with proper path handling
- **🔒 Security-First**: No shell injection vulnerabilities, safe subprocess execution
- **🌿 Git Integration**: Multi-repository status tracking with worktree support
- **🔍 Server Detection**: Automatic discovery of development servers (Flask, Django, React, etc.)
- **🎨 Claude Code Compatible Output**: Optimized formatting for Claude Code display

## Architecture & Technology Stack

### Core Technologies
- **Python 3.10+**: Core language with modern type hints
- **Click**: CLI framework for command-line interface
- **PyYAML**: YAML configuration parsing and generation
- **Subprocess**: Secure git and system command execution

### Package Structure
```
src/
├── __init__.py         # Package exports and version info
├── cli.py             # Click-based command-line interface
├── config.py          # YAML configuration management with layered resolution
├── core.py            # Main status line generation engine
├── detection.py       # Project type and server detection
├── git.py             # Secure git repository status management
├── logger.py          # Cross-platform logging system
├── render.py          # Status line output formatting and rendering
└── setup.py           # Interactive configuration wizard
```

## Configuration System Architecture

### Configuration Resolution Order (Highest to Lowest Priority)
1. **Local Override**: `./.cc-status-line.yaml` (worktree-specific)
2. **Project Config**: `~/.config/cc-status-line/projects/[project-id].yaml`
3. **Global Config**: `~/.config/cc-status-line/config.yaml`
4. **Built-in Defaults**: Hardcoded fallbacks

### Project Identification Strategy
- **Git Remote URL**: `github.com/user/repo` → `github-com-user-repo.yaml`
- **Worktree Support**: Same project in multiple worktrees shares project config
- **Fallback**: Path hash for non-git projects (`local-abc123def.yaml`)

### Configuration Locations
```bash
# User Choice Priority:
1. --config-dir /custom/path          # CLI override
2. $CCSL_CONFIG_DIR                   # Environment variable
3. $XDG_CONFIG_HOME/cc-status-line    # XDG standard
4. ~/.config/cc-status-line           # Default fallback

# Cross-Platform Defaults:
- Linux/macOS: ~/.config/cc-status-line/
- Windows: %APPDATA%\cc-status-line\
```

## Claude Code Integration & Testing

### Claude Code Setup Instructions

1. **Install the Tool**:
   ```bash
   # Direct installation
   uvx --from git+https://github.com/ashwch/cc-status-line cc-status-line --init
   
   # Or for development
   git clone <repository-url>
   cd cc-status-line
   uv sync --dev
   ```

2. **Configure Claude Code**:
   Add to `~/.claude/settings.json`:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "cc-status-line",
       "padding": 0
     }
   }
   ```

3. **Initialize Project**:
   ```bash
   cd your-project
   cc-status-line --init
   ```

### Testing and Quality Assurance
```bash
# Code quality checks
ruff check src --fix    # Linting and auto-fix
ruff format src         # Formatting
pyright src            # Type checking
```

### CLI Testing for Claude Code Integration
```bash
# Test core functionality
uv run cc-status-line --help
uv run cc-status-line --version
uv run cc-status-line --config-info

# Test configuration workflow
uv run cc-status-line --init
uv run cc-status-line --config

# Test actual status line output (what Claude Code will see)
uv run cc-status-line
# Expected: 📂 Repos ▶ 🟡PROJECT:main* | 🖥️ Servers ▶ 🌶️ Flask:5000

# Test with different project types
uv run cc-status-line --config-dir /tmp/test-config --init
```

### Verified Claude Code Compatibility

✅ **Claude Code Integration Features**:
- **JSON stdin handling**: Accepts and validates Claude Code JSON input from stdin
- **Workspace detection**: Uses `workspace.current_working_directory` from Claude Code context
- **Single-line output**: Optimized for Claude Code status line display (first line used)
- **Error handling**: Graceful fallback when not running from Claude Code
- **No hanging**: Quick execution with proper timeout handling

✅ **Tested CLI Commands**:
- `--help`: Shows comprehensive usage information
- `--version`: Displays "CC Status Line, version 1.0.0"
- `--config-info`: Shows configuration file locations and status
- `--config`: Displays current project configuration
- `--global-config`: Shows global settings
- `--list-projects`: Lists configured projects
- `--init`: Interactive setup wizard

✅ **Status Line Output**:
- Repository status: `📂 Repos ▶ 🟡CC-STATUS-LINE:main*`
- Server detection: `🖥️ Servers ▶ 🌶️ Flask:5000`
- Multiline formatting compatible with Claude Code
- Proper emoji and Unicode support
- Compact error messages for Claude Code

✅ **Configuration System**:
- YAML configuration files work correctly
- Local `.cc-status-line.yaml` override system functional
- Project identification from git remote URLs
- Cross-platform path handling verified
- Claude Code workspace path integration

## Security & Best Practices

### Security Measures Implemented
- **No Shell Injection**: All subprocess calls use argument lists, never `shell=True`
- **Input Validation**: YAML parsing with safe loading
- **Path Sanitization**: Proper path handling for cross-platform compatibility
- **Timeout Protection**: All external commands have timeout limits

### Code Quality Standards
- **Type Safety**: Full type annotations with `ty` type checker
- **Modern Python**: Uses Python 3.10+ features (union types, pattern matching potential)
- **Error Handling**: Comprehensive exception handling with graceful degradation
- **Logging**: Cross-platform logging with proper log rotation

## Configuration Examples

### Minimal Single Repository
```yaml
# .cc-status-line.yaml
name: "my-app"
type: "single"
repositories:
  - name: "APP"
    path: "."
    type: "main"
servers:
  - name: "Web"
    ports: [3000]
    emoji: "🌐"
```

### Complex Monolith Configuration
```yaml
# ~/.config/cc-status-line/projects/github-com-company-monolith.yaml
name: "company-monolith"
type: "monolith"
repositories:
  - name: "MAIN"
    path: "."
    type: "main"
  - name: "API"
    path: "backend"
    type: "submodule"
  - name: "WEB"
    path: "frontend"
    type: "submodule"
servers:
  - name: "Python"
    ports: [8000]
    emoji: "🐍"
  - name: "Node.js"
    ports: [3000]
    emoji: "🟢"
output_format:
  multiline: true
  colors: true
  show_changes: true
```

## Cross-Platform Considerations

### Logging Locations
- **Windows**: `%LOCALAPPDATA%\cc-status-line\logs\status-line.log`
- **macOS**: `~/Library/Logs/cc-status-line/status-line.log`
- **Linux**: `$XDG_STATE_HOME/cc-status-line/status-line.log`

### Server Detection Commands
- **Windows**: `netstat -an` (safe, no shell injection)
- **Unix-like**: `lsof -i:PORT` with `netstat -an` fallback

### Git Command Execution
All git commands use secure subprocess calls:
```python
# Secure: Uses argument list
subprocess.run(["git", "status", "--porcelain"], ...)

# NEVER: Shell injection vulnerability
subprocess.run("git status --porcelain", shell=True, ...)
```

## Environment Variables

### Configuration Control
- `CCSL_CONFIG_DIR`: Custom configuration directory
- `CCSL_LOG_LEVEL`: Debug, Info, Warning, Error, Critical
- `CCSL_DEBUG`: Enable stderr debugging output
- `CCSL_LOG_FILE`: Custom log file location

### Standard Environment Variables
- `XDG_CONFIG_HOME`: XDG Base Directory specification
- `NO_COLOR`: Disable color output

## Extension and Customization

### Adding New Server Types for Claude Code
Create server templates in global config:
```yaml
# ~/.config/cc-status-line/config.yaml
server_templates:
  flask:
    name: "Flask"
    ports: [5000, 5001, 8000]
    emoji: "🌶️"
    patterns: ["app.py", "wsgi.py", "application.py", "requirements.txt"]
  custom_server:
    name: "Custom"
    ports: [8080, 9000]
    emoji: "⚡"
    patterns: ["custom.config", "app.custom"]
```

### Custom Project Types
The detection system can be extended by modifying `src/detection.py`:
- Add new pattern matching in `ProjectDetector`
- Extend server detection patterns
- Add new repository type detection

## Publishing and Distribution

### Package Building
```bash
# Build distribution packages
uv build

# Creates:
# dist/cc_status_line-1.0.0.tar.gz
# dist/cc_status_line-1.0.0-py3-none-any.whl
```

### Installation Methods
```bash
# Direct from git (recommended for development)
uvx --from git+https://github.com/yourusername/cc-status-line cc-status-line

# Local development installation
pip install -e .

# Production installation (when published to PyPI)
pip install cc-status-line
```

## Troubleshooting & Debugging

### Common Issues
1. **No Configuration Found**: Run `cc-status-line --config-info` to see configuration sources
2. **Git Commands Failing**: Check git installation and repository validity
3. **Server Detection Issues**: Verify `lsof` or `netstat` availability
4. **Permission Errors**: Check file permissions in config directories

### Debug Mode
```bash
# Enable debug logging
CCSL_DEBUG=1 cc-status-line

# Custom log level
CCSL_LOG_LEVEL=DEBUG cc-status-line

# View configuration resolution
cc-status-line --config-info
```

### Log Analysis
Check platform-specific log locations for detailed error information and execution traces.

## Development Roadmap

### Implemented Features ✅
- YAML configuration system with layered resolution
- Cross-platform logging and file handling
- Secure subprocess execution (no shell injection)
- Git repository status tracking
- Server detection and monitoring
- Interactive setup wizard
- Comprehensive CLI interface

### Pending Features 🚧
- Comprehensive test suite
- Configuration schema validation
- Performance optimization and caching
- Plugin system for extensibility
- Shell integration (prompt/status bar)
- Web dashboard for status visualization

---

This tool is designed specifically for Claude Code's status line feature while maintaining security, performance, and ease of use. The modular architecture allows for easy extension and customization based on Claude Code integration needs.
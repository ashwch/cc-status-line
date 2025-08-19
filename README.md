# CC Status Line

**Universal status line tool designed specifically for Claude Code**

A flexible, project-agnostic status line tool built specifically for [Claude Code's status line feature](https://docs.anthropic.com/en/docs/claude-code/statusline). Provides real-time development environment status directly in your Claude Code interface.

> **Note**: This tool is specifically designed for Claude Code integration and optimized for the Claude Code status line display system.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎯 **Project-Agnostic**: Works with any development environment
- 🔧 **Interactive Setup**: Wizard-guided configuration with smart detection
- 📂 **Git Integration**: Multi-repository status with branch tracking
- 🖥️ **Server Detection**: Automatic discovery of development servers
- 🎨 **Customizable Output**: Multiline/single-line, colors, compact modes  
- 💾 **XDG Compliant**: Configuration stored in standard locations
- 🌐 **Cross-Platform**: Windows, macOS, and Linux support
- ⚡ **Fast**: Lightweight with minimal dependencies

## 🚀 Quick Start for Claude Code

### Prerequisites

This tool requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code) to be installed and configured.

### Installation

```bash
# Install directly with uvx (recommended)
uvx --from git+https://github.com/ashwch/cc-status-line cc-status-line --init

# Or clone for development
git clone https://github.com/ashwch/cc-status-line
cd cc-status-line
uv sync
```

### Setup in Claude Code

1. **Configure Claude Code**: Add to `~/.claude/settings.json`:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "cc-status-line",
       "padding": 0
     }
   }
   ```

2. **Initialize Project**: Run the setup wizard in your project directory:
   ```bash
   cc-status-line --init
   ```

3. **Test Integration**: Verify the status line appears in Claude Code:
   ```bash
   cc-status-line
   # 📂 Repos ▶ 🟡MYAPP:main* | 🖥️ Servers ▶ 🌶️ Flask:5000
   ```

## 🎛️ Configuration

### Project Types

CC Status Line automatically detects and supports:

- **Monolith**: Git repository with submodules (like this repo!)
- **Single**: Standard single git repository  
- **Multi**: Multiple repositories in workspace
- **Custom**: Manual configuration for unique setups

### Server Detection

Automatically detects common development servers:

| Framework | Ports | Icon | Detection |
|-----------|-------|------|-----------|
| Flask | 5000, 5001, 8000 | 🌶️ | `app.py`, `wsgi.py`, `application.py` |
| Django | 8000, 8001 | 🐍 | `manage.py`, `settings.py` |
| React | 3000, 3001 | ⚛️ | `package.json`, `src/`, `public/` |
| Next.js | 3000, 3001 | ▲ | `next.config.js`, `pages/`, `app/` |
| Vue | 8080, 3000 | 💚 | `vue.config.js`, `src/main.js` |
| FastAPI | 8000, 8001 | ⚡ | `main.py`, `app.py` |
| Vite | 5173, 4173 | ⚡ | `vite.config.js` |
| Rails | 3000, 4000 | 💎 | `Gemfile`, `config/application.rb` |
| Docker | 80, 443, 8080 | 🐳 | `docker-compose.yml`, `Dockerfile` |

## 📋 CLI Commands

```bash
# Setup and configuration
cc-status-line --init              # Interactive setup wizard
cc-status-line --config            # Show current project config
cc-status-line --list-projects     # List all configured projects
cc-status-line --reset             # Reset current project config
cc-status-line --global-config     # Show global settings

# Display status (default command)
cc-status-line                     # Show status line

# Help and version
cc-status-line --help              # Show help
cc-status-line --version           # Show version
```

## 🏗️ Project Structure Examples

### Monolith with Submodules

```
my-monolith/
├── .gitmodules
├── backend/           # Django API
├── frontend/          # React app  
├── design-system/     # Component library
└── infrastructure/    # Terraform configs
```

**Configuration:**
```json
{
  "name": "my-monolith",
  "type": "monolith", 
  "repositories": [
    {"name": "MAIN", "path": ".", "type": "main"},
    {"name": "BE", "path": "backend", "type": "submodule"},
    {"name": "FE", "path": "frontend", "type": "submodule"}
  ],
  "servers": [
    {"name": "Django", "ports": [8000], "emoji": "🐍"},
    {"name": "React", "ports": [3000], "emoji": "⚛️"}
  ]
}
```

**Output:**
```
📂 Repos ▶ ✅MAIN:main │ ✅BE:develop │ 🟡FE:feature-auth*
🖥️ Servers ▶ 🐍Django:8000 │ ⚛️React:3000
```

### Single Repository

```
my-app/
├── src/
├── package.json
└── vite.config.js
```

**Output:**
```
📂 Repos ▶ ✅MYAPP:main
🖥️ Servers ▶ ⚡Vite:5173
```

### Multi-Repository Workspace

```
workspace/
├── api/           # FastAPI backend
├── web/           # React frontend
└── mobile/        # React Native app
```

**Output:**
```
📂 Repos ▶ ✅API:main │ ⚠️WEB:feature-login-3 │ ✅MOBILE:develop
🖥️ Servers ▶ ⚡FastAPI:8000 │ ⚛️React:3000
```

## 🎨 Status Indicators

### Repository Status

| Icon | Meaning |
|------|---------|
| ✅ | Up to date with upstream |
| ⚠️ | 1-5 commits behind upstream |
| 🔴 | 6+ commits behind upstream |
| 🟡 | Has uncommitted changes |

### Format

```
{status}{NAME}:{branch}{-behind}{*changes}
```

Examples:
- `✅BACKEND:main` - Clean, up to date
- `⚠️API:develop-2` - 2 commits behind
- `🟡WEB:feature*` - Has uncommitted changes
- `🔴INFRA:main-10*` - 10 commits behind with changes

## ⚙️ Configuration Files

### XDG Locations

```bash
# Linux/macOS
~/.config/cc-status-line/
├── config.yaml                    # Global settings
└── projects/
    ├── github-com-user-repo.yaml  # Project-specific config
    └── gitlab-com-org-app.yaml

# Windows  
%APPDATA%\cc-status-line\
```

### Global Configuration

```yaml
version: "1.0.0"
output_format:
  colors: true
  multiline: true
  compact: false
  show_changes: true
system_monitoring:
  enabled: false
  battery: false
  cpu: false
  memory: false
server_templates:
  web:
    name: "Web"
    ports: [3000, 8000, 8080]
    emoji: "🌐"
    patterns: ["index.html", "package.json"]
```

### Project Configuration

```yaml
name: "my-project"
type: "single"
root_path: "/path/to/project"
repositories:
  - name: "MYAPP"
    path: "."
    type: "main"
servers:
  - name: "Web"
    ports: [8000]
    emoji: "🌐"
    enabled: true
output_format:
  multiline: true
  colors: true
  compact: false
  show_changes: true
created_at: "2025-01-19 12:00:00"
updated_at: "2025-01-19 12:00:00"
```

## 🔧 Advanced Claude Code Usage

### Custom Configuration

Configure different status line formats for different project types:

```bash
# Single repository
cc-status-line --init
# Select: single -> Use detected repositories -> Use detected servers

# Monolith with submodules
cc-status-line --init
# Select: monolith -> Configure submodule tracking

# Multi-repository workspace
cc-status-line --init
# Select: multi -> Configure each repository
```

### Environment Variables for Claude Code

```bash
# Disable colors for better Claude Code display
NO_COLOR=1 cc-status-line

# Custom config directory
CCSL_CONFIG_DIR=/path/to/configs cc-status-line

# Debug mode for troubleshooting Claude Code integration
CCSL_DEBUG=1 cc-status-line
```

### Claude Code Settings Examples

```json
// Minimal configuration (~/.claude/settings.json)
{
  "statusLine": {
    "type": "command",
    "command": "cc-status-line"
  }
}

// Full configuration with padding control
{
  "statusLine": {
    "type": "command",
    "command": "cc-status-line",
    "padding": 0
  }
}

// Conditional status line (only in git repositories)
{
  "statusLine": {
    "type": "command",
    "command": "test -d .git && cc-status-line || echo '📁 No git repo'"
  }
}
```

## 🎆 Claude Code Integration

This tool is specifically designed for [Claude Code's status line feature](https://docs.anthropic.com/en/docs/claude-code/statusline). To use with Claude Code:

### 1. Install the Tool

```bash
# Install with uv (recommended)
uvx --from git+https://github.com/ashwch/cc-status-line cc-status-line --init

# Or clone and install locally
git clone https://github.com/ashwch/cc-status-line
cd cc-status-line
uv sync
uv run cc-status-line --init
```

### 2. Configure Claude Code

Add to your Claude Code settings file `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "cc-status-line",
    "padding": 0
  }
}
```

### 3. Initialize Your Project

```bash
cd your-project
cc-status-line --init
```

### 4. Test the Status Line

```bash
cc-status-line
# Output: 📂 Repos ▶ 🟡MYAPP:main* | 🖥️ Servers ▶ 🌶️ Flask:5000
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/ashwch/cc-status-line
cd cc-status-line
uv sync --dev
```

### Code Quality

```bash
ruff check src --fix    # Lint and fix code
ruff format src         # Format code
pyright src            # Type checking
```

### Testing

```bash
# Test basic functionality
uv run cc-status-line --help
uv run cc-status-line --version
uv run cc-status-line --config-info

# Test with configuration
uv run cc-status-line --init
uv run cc-status-line
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by development environment status line tools
- Built for the [Claude Code](https://docs.anthropic.com/en/docs/claude-code) ecosystem
- Created by Ashwini Chaudhary

---

**Made with ❤️ for developers who love clean, informative status lines**
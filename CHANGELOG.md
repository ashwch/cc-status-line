# Changelog

All notable changes to CC Status Line will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-19

### Added
- **Claude Code Integration**: Full support for Claude Code status line feature
  - JSON stdin handling for Claude Code context
  - Workspace directory detection from Claude context
  - Optimized error messages for status line display
- **Universal Configuration System**: Layered YAML configuration (Global → Project → Local)
- **Cross-Platform Support**: Windows, macOS, and Linux compatibility
- **Git Repository Tracking**: Multi-repository status with branch tracking and commit behind detection
- **Server Detection**: Automatic discovery of development servers
  - Flask (🌶️): ports 5000, 5001, 8000
  - Django (🐍): ports 8000, 8001, 8080  
  - React (⚛️): ports 3000, 3001, 4000, 5000
  - Node.js (🟢): ports 3000, 8080
  - Vite (⚡): ports 5173, 4173
  - Docker (🐳): ports 80, 443, 8080
- **ANSI Color Support**: Semantic branch coloring and professional output formatting
  - Main/master branches: bright green
  - Feature branches: bright blue  
  - Fix branches: bright red
  - Development branches: bright yellow
  - Release branches: bright magenta
  - Repository names: bright cyan
  - Server names: bright green, ports: bright yellow
- **Interactive Setup Wizard**: Guided configuration with smart project detection
- **Security-First Design**: No shell injection vulnerabilities, safe subprocess execution
- **Professional CLI Interface**: Comprehensive help, version info, and configuration management

### Configuration Features
- **Project Type Detection**: Automatic detection of monolith, single repo, multi-repo, and custom projects
- **Local Overrides**: Project-specific `.cc-status-line.yaml` files
- **Environment Variable Support**: 
  - `NO_COLOR`: Disable color output
  - `CCSL_CONFIG_DIR`: Custom configuration directory
  - `CCSL_DEBUG`: Enable debug mode
  - `XDG_CONFIG_HOME`: XDG Base Directory compliance

### Development & Quality
- **Comprehensive Testing**: CLI functionality, Claude Code integration, and color handling tests
- **GitHub Actions CI/CD**: Cross-platform testing on Ubuntu, macOS, and Windows
- **Code Quality Tools**: Ruff linting, Pyright type checking, and security scanning
- **Developer Documentation**: Detailed CONTRIBUTING.md and project setup guides

### Documentation
- **Claude Code Focused**: README and documentation specifically target Claude Code users
- **Configuration Examples**: Real-world examples for different project types
- **Troubleshooting Guide**: Common issues and debugging information

## [Unreleased]

### Planned
- Enhanced test coverage with unit tests
- Configuration schema validation
- Performance optimizations and caching
- Plugin system for custom server detection
- Web dashboard for status visualization

---

**Note**: This is the initial release of CC Status Line, specifically designed for [Claude Code's status line feature](https://docs.anthropic.com/en/docs/claude-code/statusline). Future releases will focus on expanding functionality while maintaining Claude Code compatibility.
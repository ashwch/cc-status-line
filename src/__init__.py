"""
CC Status Line - Claude Code status line tool for development environments.

A specialized status line tool designed for Claude Code's status line feature.
Displays git repositories, development servers, and project status directly in Claude Code.
"""

__version__ = "1.0.0"
__author__ = "Ashwini Chaudhary"
__email__ = "monty.sinngh@gmail.com"

from .config import ConfigManager
from .core import StatusLineEngine
from .detection import ProjectDetector, ServerDetector
from .git import GitManager
from .logger import get_logger
from .render import StatusLineRenderer
from .setup import SetupWizard

__all__ = [
    "ConfigManager",
    "StatusLineEngine",
    "ProjectDetector",
    "ServerDetector",
    "GitManager",
    "get_logger",
    "StatusLineRenderer",
    "SetupWizard",
]

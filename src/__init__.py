"""
CC Status Line - Universal, configurable development environment status line.

A flexible, project-agnostic status line tool that adapts to any development environment.
Supports interactive configuration, project-specific settings, and works with monoliths,
single repositories, and custom project structures.
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

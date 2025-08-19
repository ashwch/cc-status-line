"""Cross-platform logging support for CC Status Line."""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any


class StatusLineLogger:
    """Cross-platform logger for CC Status Line."""

    def __init__(self, name: str = "cc-status-line", config: dict[str, Any] | None = None):
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logger with appropriate handlers and formatters."""
        logger = logging.getLogger(self.name)
        logger.setLevel(self._get_log_level())

        # Clear any existing handlers
        logger.handlers.clear()

        # Add handlers based on configuration
        if self._should_log_to_file():
            logger.addHandler(self._create_file_handler())

        if self._should_log_to_stderr():
            logger.addHandler(self._create_stderr_handler())

        return logger

    def _get_log_level(self) -> int:
        """Get log level from environment or config."""
        # 1. Environment variable
        env_level = os.getenv("CCSL_LOG_LEVEL", "").upper()
        if env_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            return getattr(logging, env_level)

        # 2. Configuration
        config_level = self.config.get("logging", {}).get("level", "WARNING").upper()
        if config_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            return getattr(logging, config_level)

        # 3. Default to WARNING (errors and above only)
        return logging.WARNING

    def _should_log_to_file(self) -> bool:
        """Check if file logging is enabled."""
        # Environment variable override
        if env_file := os.getenv("CCSL_LOG_FILE"):
            return bool(env_file)

        # Configuration setting
        return self.config.get("logging", {}).get("file_enabled", False)

    def _should_log_to_stderr(self) -> bool:
        """Check if stderr logging is enabled."""
        # Environment variable override
        if os.getenv("CCSL_DEBUG") == "1":
            return True

        # Configuration setting
        return self.config.get("logging", {}).get("stderr_enabled", False)

    def _get_log_file_path(self) -> Path:
        """Get cross-platform log file path."""
        # 1. Environment variable override
        if env_file := os.getenv("CCSL_LOG_FILE"):
            return Path(env_file).expanduser()

        # 2. Configuration override
        if config_file := self.config.get("logging", {}).get("file_path"):
            return Path(config_file).expanduser()

        # 3. Platform-specific default locations
        if sys.platform == "win32":
            # Windows: Use LOCALAPPDATA
            log_dir = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
            return log_dir / "cc-status-line" / "logs" / "status-line.log"
        elif sys.platform == "darwin":
            # macOS: Use ~/Library/Logs
            return Path.home() / "Library" / "Logs" / "cc-status-line" / "status-line.log"
        else:
            # Linux/Unix: Use XDG or fallback
            if xdg_state := os.getenv("XDG_STATE_HOME"):
                log_dir = Path(xdg_state)
            else:
                log_dir = Path.home() / ".local" / "state"
            return log_dir / "cc-status-line" / "status-line.log"

    def _create_file_handler(self) -> logging.Handler:
        """Create file handler with rotation."""
        log_file = self._get_log_file_path()

        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Use RotatingFileHandler to prevent huge log files
        from logging.handlers import RotatingFileHandler

        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=3,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        return handler

    def _create_stderr_handler(self) -> logging.Handler:
        """Create stderr handler for debugging."""
        handler = logging.StreamHandler(sys.stderr)

        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)

        return handler

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self.logger.critical(message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback."""
        self.logger.exception(message, **kwargs)


def get_logger(
    name: str = "cc-status-line", config: dict[str, Any] | None = None
) -> StatusLineLogger:
    """Get configured logger instance."""
    return StatusLineLogger(name, config)


# Example usage:
# logger = get_logger()
# logger.debug("Starting status line generation")
# logger.error("Failed to connect to git repository", exc_info=True)

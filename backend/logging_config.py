# © 2025 The Christman AI Project. All rights reserved.
#
# This code is released as part of a trauma-informed, dignity-first AI ecosystem
# designed to protect, empower, and elevate vulnerable populations.
#
# By using, modifying, or distributing this software, you agree to uphold the following:
# 1. Truth — No deception, no manipulation.
# 2. Dignity — Respect the autonomy and humanity of all users.
# 3. Protection — Never use this to exploit or harm vulnerable individuals.
# 4. Transparency — Disclose all modifications and contributions clearly.
# 5. No Erasure — Preserve the mission and ethical origin of this work.
#
# This is not just code. This is redemption in code.
# Contact: lumacognify@thechristmanaiproject.com
# https://thechristmanaiproject.com

"""
Logging configuration for AlphaVox

This module provides centralized logging configuration for the application,
supporting both development and production environments with appropriate
log levels and formatting.
"""

import json
import logging
import logging.config
import os
from typing import Any, Dict


def configure_logging():
    """
    Configure application logging using environment variable or defaults.

    In production (AWS), logging configuration is provided via an environment
    variable pointing to a JSON config file. In development, we use a default
    configuration.
    """
    config_file = os.environ.get("LOGGING_CONFIG_FILE")

    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                logging.config.dictConfig(config)
                logging.info("Logging configured from file")
        except Exception as e:
            _configure_fallback_logging()
            logging.error(f"Error configuring logging from file: {e}")
    else:
        # Use default configuration
        _configure_default_logging()


def _configure_fallback_logging():
    """Configure basic logging as fallback if configuration fails."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Fallback logging configuration applied")


def _configure_default_logging():
    """Configure default development logging."""
    config = _get_default_logging_config()
    logging.config.dictConfig(config)
    logging.info("Default logging configuration applied")


def _get_default_logging_config() -> Dict[str, Any]:
    """Get default logging configuration dictionary."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s: %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "default",
                "filename": "alphavox.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 3,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "default",
                "filename": "alphavox_error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 3,
            },
        },
        "loggers": {
            "werkzeug": {"level": "INFO", "handlers": ["console"]},
            "sqlalchemy.engine": {"level": "WARNING", "handlers": ["console", "file"]},
        },
        "root": {"level": "INFO", "handlers": ["console", "file", "error_file"]},
    }

__all__ = ['configure_logging', '_configure_fallback_logging', '_configure_default_logging', '_get_default_logging_config']

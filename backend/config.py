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
Configuration Module
--------------------
Central configuration management for alphavox's system.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Configuration settings for alphavox"""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"
    MEMORY_DIR = PROJECT_ROOT / "memory"
    LOGS_DIR = PROJECT_ROOT / "logs"
    LOADER_DIR = PROJECT_ROOT / "loaders"
    MODELS_DIR = PROJECT_ROOT / "models"
    SCHEMAS_DIR = PROJECT_ROOT / "schemas"

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    # AWS RDS PostgreSQL on Graviton
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "alphavox")
    DB_USER = os.getenv("DB_USER", "alphavox_admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    # Ollama (Local AI - Primary Provider)
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

    # alphavox Configuration
    alphavox_MODE = os.getenv("alphavox_MODE", "engineer")
    alphavox_VOICE = os.getenv("alphavox_VOICE", "matthew")
    ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
    ENABLE_INTERNET_MODE = os.getenv("ENABLE_INTERNET_MODE", "false").lower() == "true"

    # Database (local fallback path - prefer DATABASE_URL for RDS)
    DATABASE_PATH = str(MEMORY_DIR / "alphavox.db")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = str(LOGS_DIR / "alphavox.log")

    # AI Model Configuration
    DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "ollama")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
    PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL", "sonar-pro")

    # Speech Recognition
    SPEECH_BACKEND = os.getenv("SPEECH_BACKEND", "google")
    MICROPHONE_ENERGY_THRESHOLD = int(os.getenv("MICROPHONE_ENERGY_THRESHOLD", "4000"))

    # TTS Configuration
    TTS_PROVIDER = os.getenv("TTS_PROVIDER", "polly")  # polly or gtts

    # Memory Configuration
    MEMORY_FILE = str(MEMORY_DIR / "memory_store.json")
    MAX_MEMORY_ENTRIES = int(os.getenv("MAX_MEMORY_ENTRIES", "1000"))

    # Learning Configuration
    LEARNING_ENABLED = os.getenv("LEARNING_ENABLED", "true").lower() == "true"
    LEARNING_CHAMBERS_FILE = str(DATA_DIR / "learning_chambers.json")

    # GitHub Integration
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO", "Nathaniel-AI/alphavoxC")
    GITHUB_SYNC_ENABLED = os.getenv("GITHUB_SYNC_ENABLED", "false").lower() == "true"

    @classmethod
    def ensure_directories(cls):
        """Create all required directories"""
        for dir_path in [
            cls.DATA_DIR,
            cls.MEMORY_DIR,
            cls.LOGS_DIR,
            cls.LOADER_DIR,
            cls.MODELS_DIR,
            cls.SCHEMAS_DIR,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export settings as dictionary"""
        return {
            key: getattr(cls, key) for key in dir(cls) if not key.startswith("_") and key.isupper()
        }

    @classmethod
    def save_to_file(cls, filepath: str = "config.json"):
        """Save configuration to JSON file"""
        config_dict = cls.to_dict()
        # Convert Path objects to strings for JSON
        for key, value in config_dict.items():
            if isinstance(value, Path):
                config_dict[key] = str(value)

        with open(filepath, "w") as f:
            json.dump(config_dict, f, indent=2)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return getattr(cls, key, default)


# Ensure directories exist on import
Settings.ensure_directories()

# Export commonly used paths
LOADER_DIR = Settings.LOADER_DIR
PROJECT_ROOT = Settings.PROJECT_ROOT
DATA_DIR = Settings.DATA_DIR
MEMORY_DIR = Settings.MEMORY_DIR
LOGS_DIR = Settings.LOGS_DIR

__all__ = [
    "Settings",
    "LOADER_DIR",
    "PROJECT_ROOT",
    "DATA_DIR",
    "MEMORY_DIR",
    "LOGS_DIR",
]

# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

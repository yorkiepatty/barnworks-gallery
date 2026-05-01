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

"""Memory service for alphavox Dashboard."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Example usage:
# In __init__:
#     self.memory = MemoryService()
#
# In start():
#     self.memory.load_context()  # ← LOADS from storage
#
# In stop():
#     self.memory.save_context()  # ← SYNCS to storage


class MemoryService:
    """Persists and retrieves conversational memory."""

    def __init__(self, memory_file: Optional[Path] = None):
        # Default to data/memory_store.json if no file specified
        if memory_file is None:
            data_dir = Path(os.getenv("DATA_DIR", "./data"))
            data_dir.mkdir(parents=True, exist_ok=True)
            memory_file = data_dir / "memory_store.json"

        self.memory_file = memory_file
        self._memory: List[Dict[str, Any]] = []

    def load_context(self) -> None:
        """Load memory context from disk."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r", encoding="utf-8") as handle:
                    self._memory = json.load(handle)
                logger.info("Loaded %s memory records", len(self._memory))
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("Failed to load memory context: %s", exc)
                self._memory = []
        else:
            logger.info("No existing memory store; starting fresh")
            self._memory = []

    def save_context(self) -> None:
        """Persist memory context to disk."""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as handle:
                json.dump(self._memory, handle, indent=2)
            logger.info("Memory context saved (%s records)", len(self._memory))
        except Exception as exc:  # pragma: no cover
            logger.error("Failed to save memory context: %s", exc)

    def store(self, memory_type: str, content: Dict[str, Any]) -> None:
        """Store a new memory entry."""
        entry = {
            "type": memory_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self._memory.append(entry)
        logger.debug("Stored memory entry: %s", entry)
        self.save_context()

    def retrieve(self, memory_type: str = "recent", limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve memories filtered by type or return most recent entries."""
        if memory_type == "recent":
            return list(reversed(self._memory[-limit:]))

        filtered = [m for m in self._memory if m.get("type") == memory_type]
        return list(reversed(filtered[-limit:]))

__all__ = ['MemoryService']

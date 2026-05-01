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

"""Personality management for alphavox Dashboard."""

import logging
from typing import Any, Dict

from config import Settings

logger = logging.getLogger(__name__)


class PersonalityService:
    """Provides access to alphavox's personality profile."""

    def __init__(self):
        self.settings = Settings()
        self.profile: Dict[str, Any] = {}

    def load_profile(self) -> Dict[str, Any]:
        """Load the personality profile from settings."""
        self.profile = self.settings.identity
        logger.info("Personality profile loaded for %s", self.profile.get("name", "alphavox"))
        return self.profile

        # In start():
        self.personality.load_profile()  # ← LOADS alphavox's character config

    def get_trait(self, trait_name: str) -> Any:
        """Retrieve a specific trait from the profile."""
        if not self.profile:
            self.load_profile()

        traits = self.profile.get("personality", {}).get("core_traits", [])
        return trait_name in traits

__all__ = ['PersonalityService']

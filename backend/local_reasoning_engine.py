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
Local Reasoning Engine
----------------------
alphavoxC's internal thought kernel.
Builds short conclusions from user input, memory, tone, and vision.
No external AI calls — purely local synthesis.
"""

import math
from datetime import datetime


class LocalReasoningEngine:
    def __init__(self):
        self.last_reflection = ""
        self.reasoning_log = []

    # ----------------------------------------------------------
    def analyze(
        self, user_input: str, memory: str = "", emotion: str = "", vision: str = ""
    ) -> str:
        """
        Primary reasoning function.
        Combines alphavox's sensory and contextual inputs into a unified interpretation.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reflection = []

        # 1️⃣  Gather sensory context
        if emotion:
            reflection.append(f"My emotional tone reads as {emotion}.")
        if vision:
            reflection.append(f"My visual impression is {vision}.")
        if memory:
            reflection.append(f"I remember that {memory.strip()}.")

        # 2️⃣  Process new input
        reflection.append(f"The new input is: '{user_input.strip()}'.")

        # 3️⃣  Internal reasoning — weighted synthesis
        weight = self._calculate_context_weight(memory, emotion, vision)
        core_thought = self._generate_summary(user_input, memory, weight)

        # 4️⃣  Build final reflection
        final_output = " ".join(reflection) + " " + core_thought

        # 5️⃣  Save state
        self.last_reflection = final_output
        self.reasoning_log.append({"time": timestamp, "input": user_input, "output": final_output})

        return final_output

    # ----------------------------------------------------------
    def _calculate_context_weight(self, memory: str, emotion: str, vision: str) -> float:
        """
        Generate a simple numeric context weight based on available data.
        Higher weight = deeper internal reasoning.
        """
        factors = [bool(memory), bool(emotion), bool(vision)]
        return math.sqrt(sum(factors)) / 2.0  # 0.0 to 0.866

    # ----------------------------------------------------------
    def _generate_summary(self, user_input: str, memory: str, weight: float) -> str:
        """
        Create a short reflection — the 'thought'.
        """
        if weight < 0.3:
            return "I'm processing this freshly without much context yet."
        elif weight < 0.6:
            return "This connects loosely to my past experiences, but I'm considering new perspectives."
        else:
            return "This resonates strongly with my memories, forming a coherent understanding."

    # ----------------------------------------------------------
    def merge_thoughts(self, internal: str, external: str) -> str:
        """
        Integrate external lookup data into alphavox's internal narrative.
        """
        if not external:
            return internal
        return f"{internal}\n\nAfter reviewing external data, I also note: {external}"

    # ----------------------------------------------------------
    def recall_last(self) -> str:
        """Return the most recent reasoning output."""
        return self.last_reflection or "No previous reflection stored."


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['LocalReasoningEngine']

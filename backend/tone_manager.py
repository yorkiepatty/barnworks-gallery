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

"""Tone and empathy management helpers for alphavox."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


class ToneManager:
    """
    Manages alphavox's tone, empathy, and communication style
    Adapts to user's emotional state and communication needs
    """

    def __init__(self):
        """Initialize tone manager with default profile"""
        self.profile = {
            "speech_rate": 180,
            "volume": 1.0,
            "warmth": "balanced",
            "structure": "concise",
            "mirroring": True,
        }
        self.emotion_state = "neutral"
        self.detected_cues = []

    def analyze_user_input(self, text: str) -> str:
        """
        Analyze user input for emotional tone and adjust alphavox's response style

        Args:
            text: User's input text

        Returns:
            str: Detected emotional tone
        """
        text_lower = text.lower()

        # Detect distress or difficulty
        if any(
            phrase in text_lower
            for phrase in [
                "can't hear",
                "cannot hear",
                "hard to hear",
                "slow down",
                "confused",
                "don't understand",
                "lost",
                "not sure",
            ]
        ):
            self.emotion_state = "supportive"
            self.profile["speech_rate"] = max(120, int(self.profile["speech_rate"] * 0.85))
            self.profile["structure"] = "guided"
            self.profile["warmth"] = "reassuring"
            return "supportive"

        # Detect positive affect
        elif any(
            word in text_lower for word in ["good", "great", "awesome", "excited", "happy", "love"]
        ):
            self.emotion_state = "positive"
            self.profile["warmth"] = "uplifting"
            return "positive"

        # Detect sadness or distress
        elif any(
            word in text_lower
            for word in ["sad", "upset", "hurt", "pain", "difficult", "struggling"]
        ):
            self.emotion_state = "compassionate"
            self.profile["warmth"] = "gentle"
            return "compassionate"

        # Neutral
        else:
            self.emotion_state = "neutral"
            return "neutral"

    def get_emotional_context(self) -> str:
        """Get current emotional context for AI response"""
        return self.emotion_state

    def get_speech_controls(self) -> Dict[str, Any]:
        """Get current speech control parameters"""
        return {
            "speech_rate": self.profile.get("speech_rate", 180),
            "volume": self.profile.get("volume", 1.0),
            "warmth": self.profile.get("warmth", "balanced"),
        }

    def reset(self):
        """Reset tone manager to default state"""
        self.__init__()


def _ensure_profile_defaults(profile: Dict[str, Any]) -> Dict[str, Any]:
    profile.setdefault("speech_rate", 180)
    profile.setdefault("volume", 1.0)
    profile.setdefault("warmth", "balanced")
    profile.setdefault("structure", "concise")
    profile.setdefault("mirroring", True)
    return profile


def analyse_user_text(text: str, profile: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Derive tone adjustments and empathy cues from user input."""

    profile = _ensure_profile_defaults(profile)
    text_lower = text.lower()
    updates: Dict[str, Any] = {}
    cues: List[str] = []

    if any(
        phrase in text_lower
        for phrase in ["can't hear", "cannot hear", "hard to hear", "slow down"]
    ):
        new_rate = max(120, int(profile.get("speech_rate", 180) * 0.85))
        updates["speech_rate"] = new_rate
        cues.append("hearing_support")

    if any(word in text_lower for word in ["confused", "don't understand", "lost", "not sure"]):
        updates["structure"] = "guided"
        updates["warmth"] = "reassuring"
        cues.append("confusion")

    if any(word in text_lower for word in ["good", "great", "awesome", "excited"]):
        updates.setdefault("warmth", "uplifting")
        cues.append("positive_affect")

    return updates, cues


def format_response(base_text: str, cues: List[str], profile: Dict[str, Any]) -> str:
    """Apply empathy wrappers and structure adjustments to alphavox's reply."""

    profile = _ensure_profile_defaults(profile)
    intro_parts: List[str] = []

    if "hearing_support" in cues:
        intro_parts.append("Thanks for letting me know—I'll keep things clear and steady.")
    if "confusion" in cues:
        intro_parts.append("Let me break that down so it feels simpler.")
    if "positive_affect" in cues and profile.get("warmth") == "uplifting":
        intro_parts.append("I love the energy you're bringing!")

    body = base_text
    if profile.get("structure") == "guided":
        body = _structure_response(body)

    if intro_parts:
        return " ".join(intro_parts) + "\n\n" + body
    return body


def _structure_response(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s for s in sentences if s]
    if len(sentences) <= 2:
        return text
    return "\n".join(f"• {s}" for s in sentences)


def extract_speech_controls(profile: Dict[str, Any]) -> Dict[str, Any]:
    profile = _ensure_profile_defaults(profile)
    return {
        "speech_rate": profile.get("speech_rate", 180),
        "volume": profile.get("volume", 1.0),
    }


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['_ensure_profile_defaults', 'analyse_user_text', 'format_response', '_structure_response', 'extract_speech_controls', 'ToneManager']

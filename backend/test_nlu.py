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
NLU Core Module Unit Tests
===========================

Test natural language understanding and root cause analysis.

==============================================================================
© 2025 Everett Nathaniel Christman & Misty Gail Christman
The Christman AI Project — Luma Cognify AI
All rights reserved. Unauthorized use, replication, or derivative training
of this material is prohibited.
Core Directive: "How can I help you love yourself more?"
Autonomy & Alignment Protocol v3.0
==============================================================================
"""

import os
import sys

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.unit
class TestNLUCore:
    """Test NLU core functionality."""

    def test_text_preprocessing(self, mock_nlu_input):
        """Test basic text preprocessing."""
        from nlu_core import preprocess_text

        # Test lowercase conversion
        result = preprocess_text("I WANT WATER")
        assert result == "i want water"

        # Test whitespace normalization
        result = preprocess_text("I    want   water")
        assert "  " not in result

    def test_intent_classification_basic(self, mock_nlu_input):
        """Test basic intent classification."""
        try:
            from nlu_core import classify_intent

            # Food/drink requests
            assert classify_intent("I want water")["intent"] in [
                "drink_request",
                "need",
            ]
            assert classify_intent("I am hungry")["intent"] in ["food_request", "need"]

            # Greeting
            assert classify_intent("Hello")["intent"] in ["greeting", "social"]

            # Help request
            assert classify_intent("I need help")["intent"] in ["help_request", "need"]
        except ImportError:
            pytest.skip("NLU core module not available")

    def test_confidence_scoring(self):
        """Test confidence score calculation."""
        try:
            from nlu_core import calculate_confidence

            # High confidence case
            score = calculate_confidence(
                text_confidence=0.9, gesture_confidence=0.85, context_confidence=0.8
            )
            assert 0.7 <= score <= 1.0

            # Low confidence case
            score = calculate_confidence(
                text_confidence=0.3, gesture_confidence=0.2, context_confidence=0.1
            )
            assert 0.0 <= score <= 0.5
        except ImportError:
            pytest.skip("NLU core module not available")


@pytest.mark.unit
class TestRootCauseAnalysis:
    """Test root cause analysis engine."""

    def test_identify_root_cause_hunger(self):
        """Test identification of hunger as root cause."""
        try:
            from alphavox_input_nlu import identify_root_cause

            context = {
                "text": "I feel bad",
                "behavior": "agitated",
                "last_meal": "6 hours ago",
                "recent_activity": "looking at kitchen",
            }

            result = identify_root_cause(context)
            assert result["root_cause"] in ["hunger", "food_need"]
        except ImportError:
            pytest.skip("Root cause module not available")

    def test_identify_root_cause_discomfort(self):
        """Test identification of physical discomfort."""
        try:
            from alphavox_input_nlu import identify_root_cause

            context = {
                "text": "Something is wrong",
                "behavior": "restless",
                "facial_expression": "discomfort",
                "body_language": "adjusting position",
            }

            result = identify_root_cause(context)
            assert result["root_cause"] in ["discomfort", "physical_need"]
        except ImportError:
            pytest.skip("Root cause module not available")

    def test_multi_modal_fusion(self, mock_nlu_input):
        """Test fusion of multiple input modalities."""
        try:
            from alphavox_input_nlu import fuse_modalities

            inputs = {
                "text": {"intent": "need", "confidence": 0.8},
                "gesture": {"intent": "pointing", "confidence": 0.9},
                "emotion": {"state": "neutral", "confidence": 0.7},
            }

            result = fuse_modalities(inputs)

            # Should produce combined result
            assert "final_intent" in result
            assert "confidence" in result
            assert 0.0 <= result["confidence"] <= 1.0
        except ImportError:
            pytest.skip("Multi-modal fusion not available")


@pytest.mark.unit
class TestContextAnalysis:
    """Test context-aware analysis."""

    def test_conversation_context_integration(self, mock_conversation_history):
        """Test integration of conversation history."""
        try:
            from nlu_core import analyze_with_context

            current_input = "Yes, that sounds good"
            result = analyze_with_context(current_input, mock_conversation_history)

            # Should understand "Yes" refers to previous offer
            assert result["context_aware"]
        except ImportError:
            pytest.skip("Context analysis not available")

    def test_temporal_pattern_recognition(self, mock_lstm_sequence):
        """Test temporal pattern recognition."""
        try:
            from advanced_nlp_service import analyze_temporal_pattern

            # Should detect pattern in sequence
            result = analyze_temporal_pattern(mock_lstm_sequence)

            assert "pattern" in result
            assert "confidence" in result
        except ImportError:
            pytest.skip("Temporal analysis not available")


@pytest.mark.integration
class TestNLUPipeline:
    """Integration tests for complete NLU pipeline."""

    def test_end_to_end_nlu_processing(self, mock_nlu_input):
        """Test complete NLU pipeline from input to output."""
        try:
            from alphavox_input_nlu import process_input

            result = process_input(mock_nlu_input)

            # Should produce complete analysis
            assert "intent" in result
            assert "confidence" in result
            assert "root_cause" in result
            assert "suggested_response" in result
        except ImportError:
            pytest.skip("Full NLU pipeline not available")

    def test_learning_from_interaction(self, sample_user):
        """Test that system learns from interactions."""
        try:
            from ai_learning_engine import learn_from_interaction

            interaction = {
                "user_id": sample_user.id,
                "input": "I want water",
                "predicted_intent": "drink_request",
                "outcome": "success",
            }

            # System should update its models
            result = learn_from_interaction(interaction)
            assert result["updated"]
        except ImportError:
            pytest.skip("Learning engine not available")


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['TestNLUCore', 'TestRootCauseAnalysis', 'TestContextAnalysis', 'TestNLUPipeline']

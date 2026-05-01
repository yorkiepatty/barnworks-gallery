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
Pytest Configuration and Shared Fixtures
=========================================

Central configuration for all tests with shared fixtures.

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
from datetime import datetime

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import core modules
from db import db_session, init_db
from models import CommunicationProfile, LearningSession, User


@pytest.fixture(scope="session")
def app():
    """
    Create Flask application for testing.

    Yields:
        Flask app configured for testing
    """
    from app import create_app

    # Create app with test config
    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret-key",
        }
    )

    with test_app.app_context():
        init_db()
        yield test_app


@pytest.fixture(scope="function")
def client(app):
    """
    Create Flask test client.

    Args:
        app: Flask application fixture

    Yields:
        Flask test client
    """
    return app.test_client()


@pytest.fixture(scope="function")
def db():
    """
    Create database session for testing.

    Yields:
        Database session
    """
    # Initialize test database
    init_db()

    yield db_session

    # Cleanup after test
    db_session.rollback()
    db_session.remove()


@pytest.fixture
def sample_user(db) -> User:
    """
    Create a sample user for testing.

    Args:
        db: Database session fixture

    Returns:
        User object
    """
    user = User(username="testuser", email="test@example.com", created_at=datetime.utcnow())
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def sample_communication_profile(db, sample_user) -> CommunicationProfile:
    """
    Create a sample communication profile.

    Args:
        db: Database session fixture
        sample_user: User fixture

    Returns:
        CommunicationProfile object
    """
    profile = CommunicationProfile(
        user_id=sample_user.id,
        preferred_input_mode="symbol",
        voice_preference="joanna",
        response_speed="normal",
        complexity_level="medium",
    )
    db.add(profile)
    db.commit()
    return profile


@pytest.fixture
def sample_learning_session(db, sample_user) -> LearningSession:
    """
    Create a sample learning session.

    Args:
        db: Database session fixture
        sample_user: User fixture

    Returns:
        LearningSession object
    """
    session = LearningSession(
        user_id=sample_user.id,
        session_type="vocabulary",
        duration=300,
        success_rate=0.85,
        items_covered=20,
        started_at=datetime.utcnow(),
    )
    db.add(session)
    db.commit()
    return session


@pytest.fixture
def mock_nlu_input():
    """
    Sample NLU input data for testing.

    Returns:
        Dictionary with sample input data
    """
    return {
        "text": "I want water",
        "gesture": "pointing",
        "emotion": "neutral",
        "context": {
            "recent_actions": ["looked_at_kitchen"],
            "time_of_day": "afternoon",
            "previous_request": None,
        },
    }


@pytest.fixture
def mock_behavior_data():
    """
    Sample behavior capture data for testing.

    Returns:
        Dictionary with sample behavior data
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "movements": [
            {"type": "hand_raise", "confidence": 0.92},
            {"type": "head_turn", "confidence": 0.88},
        ],
        "facial_expression": {"emotion": "happy", "confidence": 0.85},
        "eye_tracking": {"fixation_point": [640, 480], "duration": 2.5},
    }


@pytest.fixture
def mock_voice_synthesis_params():
    """
    Sample voice synthesis parameters.

    Returns:
        Dictionary with synthesis parameters
    """
    return {
        "text": "Hello, this is a test",
        "voice": "joanna",
        "language": "en-US",
        "rate": "medium",
        "pitch": "medium",
        "emotional_tone": "neutral",
    }


@pytest.fixture
def mock_lstm_sequence():
    """
    Sample LSTM sequence data for temporal analysis.

    Returns:
        List of temporal data points
    """
    import numpy as np

    # 10 frames of gesture data (3 coordinates per frame)
    return np.random.rand(10, 3).tolist()


@pytest.fixture
def mock_conversation_history():
    """
    Sample conversation history for context testing.

    Returns:
        List of conversation turns
    """
    return [
        {
            "role": "user",
            "content": "I am hungry",
            "timestamp": "2025-10-15T10:00:00",
            "intent": "food_request",
        },
        {
            "role": "assistant",
            "content": "Would you like me to help you get food?",
            "timestamp": "2025-10-15T10:00:05",
        },
        {
            "role": "user",
            "content": "Yes please",
            "timestamp": "2025-10-15T10:00:10",
            "intent": "affirmation",
        },
    ]


# Test markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests for individual functions")
    config.addinivalue_line("markers", "integration: Integration tests for multiple components")
    config.addinivalue_line("markers", "slow: Tests that take more than 1 second")
    config.addinivalue_line("markers", "security: Security-related tests")
    config.addinivalue_line("markers", "neural: Tests involving neural networks")


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['app', 'client', 'db', 'sample_user', 'sample_communication_profile', 'sample_learning_session', 'mock_nlu_input', 'mock_behavior_data', 'mock_voice_synthesis_params', 'mock_lstm_sequence', 'mock_conversation_history', 'pytest_configure']

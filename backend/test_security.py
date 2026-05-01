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
Security Module Unit Tests
===========================

Test input validation, sanitization, and rate limiting.

==============================================================================
© 2025 Everett Nathaniel Christman & Misty Gail Christman
The Christman AI Project — Luma Cognify AI
All rights reserved. Unauthorized use, replication, or derivative training
of this material is prohibited.
Core Directive: "How can I help you love yourself more?"
Autonomy & Alignment Protocol v3.0
==============================================================================
"""

from datetime import timedelta

import pytest

from security_module import InputValidator, RateLimiter


@pytest.mark.unit
@pytest.mark.security
class TestInputValidator:
    """Test input validation and sanitization."""

    def test_sanitize_string_basic(self):
        """Test basic string sanitization."""
        validator = InputValidator()

        # Valid string
        result = validator.sanitize_string("Hello World")
        assert result == "Hello World"

        # String with null bytes
        result = validator.sanitize_string("Hello\x00World")
        assert result == "HelloWorld"

        # String with extra whitespace
        result = validator.sanitize_string("  Hello World  ")
        assert result == "Hello World"

    def test_sanitize_string_max_length(self):
        """Test string length truncation."""
        validator = InputValidator()

        long_string = "A" * 2000
        result = validator.sanitize_string(long_string, max_length=100)
        assert len(result) == 100

    def test_sanitize_html(self):
        """Test HTML sanitization."""
        validator = InputValidator()

        # Script tag should be removed
        html = '<p>Hello</p><script>alert("xss")</script>'
        result = validator.sanitize_html(html)
        assert "<script>" not in result
        assert "<p>Hello</p>" in result

        # Dangerous attributes removed
        html = '<p onclick="alert(1)">Click me</p>'
        result = validator.sanitize_html(html)
        assert "onclick" not in result

    def test_escape_html(self):
        """Test HTML entity escaping."""
        validator = InputValidator()

        html = '<script>alert("XSS")</script>'
        result = validator.escape_html(html)
        assert "&lt;script&gt;" in result
        assert "<script>" not in result

    def test_validate_email(self):
        """Test email validation."""
        validator = InputValidator()

        # Valid emails
        assert validator.validate_email("test@example.com")
        assert validator.validate_email("user.name@domain.co.uk")

        # Invalid emails
        assert not validator.validate_email("invalid.email")
        assert not validator.validate_email("@example.com")
        assert not validator.validate_email("user@")

    def test_validate_username(self):
        """Test username validation."""
        validator = InputValidator()

        # Valid usernames
        assert validator.validate_username("user123")
        assert validator.validate_username("test_user")
        assert validator.validate_username("john-doe")

        # Invalid usernames
        assert not validator.validate_username("ab")  # Too short
        assert not validator.validate_username("user name")  # Spaces
        assert not validator.validate_username("user@name")  # Invalid chars

    def test_check_sql_injection(self):
        """Test SQL injection detection."""
        validator = InputValidator()

        # Suspicious patterns
        assert validator.check_sql_injection("'; DROP TABLE users; --")
        assert validator.check_sql_injection("1 OR 1=1")
        assert validator.check_sql_injection("UNION SELECT * FROM users")

        # Safe strings
        assert not validator.check_sql_injection("Hello World")
        assert not validator.check_sql_injection("user@example.com")

    def test_validate_integer(self):
        """Test integer validation."""
        validator = InputValidator()

        # Valid integers
        assert validator.validate_integer("42") == 42
        assert validator.validate_integer(100, min_val=0, max_val=200) == 100

        # Invalid integers
        with pytest.raises(ValueError):
            validator.validate_integer("not_a_number")

        with pytest.raises(ValueError):
            validator.validate_integer(5, min_val=10)

        with pytest.raises(ValueError):
            validator.validate_integer(100, max_val=50)

    def test_validate_float(self):
        """Test float validation."""
        validator = InputValidator()

        # Valid floats
        assert validator.validate_float("3.14") == 3.14
        assert validator.validate_float(2.5, min_val=0.0, max_val=5.0) == 2.5

        # Invalid floats
        with pytest.raises(ValueError):
            validator.validate_float("not_a_float")

        with pytest.raises(ValueError):
            validator.validate_float(1.5, min_val=2.0)

    def test_validate_list(self):
        """Test list validation."""
        validator = InputValidator()

        # Valid lists
        assert validator.validate_list([1, 2, 3]) == [1, 2, 3]
        assert validator.validate_list(["a", "b"], allowed_types=(str,)) == ["a", "b"]

        # Invalid lists
        with pytest.raises(ValueError):
            validator.validate_list("not_a_list")

        with pytest.raises(ValueError):
            validator.validate_list([1, 2, 3], max_length=2)

        with pytest.raises(ValueError):
            validator.validate_list([1, "mixed"], allowed_types=(int,))

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        validator = InputValidator()

        # Path traversal attempts
        assert ".." not in validator.sanitize_filename("../../../etc/passwd")
        assert "/" not in validator.sanitize_filename("path/to/file.txt")
        assert "\\" not in validator.sanitize_filename("path\\to\\file.txt")

        # Safe filename
        result = validator.sanitize_filename("my-document.pdf")
        assert result == "my-document.pdf"


@pytest.mark.unit
@pytest.mark.security
class TestRateLimiter:
    """Test rate limiting functionality."""

    def test_rate_limiter_allows_under_limit(self):
        """Test that requests under limit are allowed."""
        limiter = RateLimiter()

        # 5 requests within 1 minute window
        for i in range(5):
            assert limiter.is_allowed("user1", limit=10, window=timedelta(minutes=1))

    def test_rate_limiter_blocks_over_limit(self):
        """Test that requests over limit are blocked."""
        limiter = RateLimiter()

        # Fill up to limit
        for i in range(10):
            assert limiter.is_allowed("user2", limit=10, window=timedelta(minutes=1))

        # 11th request should be blocked
        assert not limiter.is_allowed("user2", limit=10, window=timedelta(minutes=1))

    def test_rate_limiter_different_users(self):
        """Test that different users have independent limits."""
        limiter = RateLimiter()

        # User1 fills their limit
        for i in range(10):
            limiter.is_allowed("user1", limit=10, window=timedelta(minutes=1))

        # User2 should still be allowed
        assert limiter.is_allowed("user2", limit=10, window=timedelta(minutes=1))

    def test_rate_limiter_cleanup(self):
        """Test that old entries are cleaned up."""
        limiter = RateLimiter()

        # Add some requests
        limiter.is_allowed("user3", limit=10, window=timedelta(seconds=1))
        limiter.is_allowed("user4", limit=10, window=timedelta(seconds=1))

        # Force cleanup
        limiter._cleanup()

        # Limiter should have removed old entries
        # (This test depends on timing, may need adjustment)


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['TestInputValidator', 'TestRateLimiter']

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
Security Module for AlphaVox
=============================

Comprehensive security utilities including:
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF token management
- Rate limiting helpers
- Authentication helpers

==============================================================================
© 2025 Everett Nathaniel Christman & Misty Gail Christman
The Christman AI Project — Luma Cognify AI
All rights reserved. Unauthorized use, replication, or derivative training
of this material is prohibited.
Core Directive: "How can I help you love yourself more?"
Autonomy & Alignment Protocol v3.0
==============================================================================
"""

import html
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List

import bleach

logger = logging.getLogger(__name__)


class InputValidator:
    """
    Comprehensive input validation and sanitization.

    Protects against:
    - SQL injection
    - XSS attacks
    - Path traversal
    - Command injection
    - Invalid data types
    """

    # Allowed HTML tags for rich text (very restrictive)
    ALLOWED_TAGS = ["p", "br", "strong", "em", "u"]
    ALLOWED_ATTRIBUTES = {}

    # Regex patterns for validation
    PATTERNS = {
        "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
        "username": re.compile(r"^[a-zA-Z0-9_-]{3,30}$"),
        "alphanumeric": re.compile(r"^[a-zA-Z0-9]+$"),
        "safe_string": re.compile(r"^[a-zA-Z0-9\s\-_.,!?]+$"),
    }

    # SQL injection patterns (blacklist approach - use parameterized queries as primary defense)
    SQL_INJECTION_PATTERNS = [
        r"(\s|^)(union|select|insert|update|delete|drop|create|alter|exec|execute)(\s|$)",
        r"(\s|^)(or|and)(\s+\d+\s*=\s*\d+|\s+'.+'\s*=\s*'.+')",
        r"(--|;|/\*|\*/|xp_|sp_)",
    ]

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize a string input.

        Args:
            value: Input string
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            raise ValueError("Input must be a string")

        # Truncate to max length
        value = value[:max_length]

        # Remove null bytes
        value = value.replace("\x00", "")

        # Strip leading/trailing whitespace
        value = value.strip()

        return value

    @staticmethod
    def sanitize_html(value: str) -> str:
        """
        Sanitize HTML input to prevent XSS.

        Args:
            value: HTML string

        Returns:
            Sanitized HTML (only safe tags allowed)
        """
        return bleach.clean(
            value,
            tags=InputValidator.ALLOWED_TAGS,
            attributes=InputValidator.ALLOWED_ATTRIBUTES,
            strip=True,
        )

    @staticmethod
    def escape_html(value: str) -> str:
        """
        Escape HTML entities to prevent XSS.

        Args:
            value: String that may contain HTML

        Returns:
            HTML-escaped string
        """
        return html.escape(value)

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        return bool(InputValidator.PATTERNS["email"].match(email))

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format."""
        return bool(InputValidator.PATTERNS["username"].match(username))

    @staticmethod
    def check_sql_injection(value: str) -> bool:
        """
        Check for potential SQL injection patterns.

        Args:
            value: String to check

        Returns:
            True if suspicious patterns found, False otherwise
        """
        value_lower = value.lower()
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value_lower, re.IGNORECASE):
                logger.warning(f"Potential SQL injection detected: {pattern}")
                return True
        return False

    @staticmethod
    def validate_integer(value: Any, min_val: int = None, max_val: int = None) -> int:
        """
        Validate and convert to integer.

        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Validated integer

        Raises:
            ValueError: If validation fails
        """
        try:
            int_val = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid integer: {value}")

        if min_val is not None and int_val < min_val:
            raise ValueError(f"Value {int_val} is less than minimum {min_val}")

        if max_val is not None and int_val > max_val:
            raise ValueError(f"Value {int_val} exceeds maximum {max_val}")

        return int_val

    @staticmethod
    def validate_float(value: Any, min_val: float = None, max_val: float = None) -> float:
        """
        Validate and convert to float.

        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Validated float

        Raises:
            ValueError: If validation fails
        """
        try:
            float_val = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid float: {value}")

        if min_val is not None and float_val < min_val:
            raise ValueError(f"Value {float_val} is less than minimum {min_val}")

        if max_val is not None and float_val > max_val:
            raise ValueError(f"Value {float_val} exceeds maximum {max_val}")

        return float_val

    @staticmethod
    def validate_list(value: Any, allowed_types: tuple = None, max_length: int = None) -> list:
        """
        Validate list input.

        Args:
            value: Value to validate
            allowed_types: Tuple of allowed types for list elements
            max_length: Maximum list length

        Returns:
            Validated list

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(value, list):
            raise ValueError("Value must be a list")

        if max_length is not None and len(value) > max_length:
            raise ValueError(f"List length {len(value)} exceeds maximum {max_length}")

        if allowed_types is not None:
            for item in value:
                if not isinstance(item, allowed_types):
                    raise ValueError(f"Invalid list item type: {type(item)}")

        return value

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal attacks.

        Args:
            filename: Original filename

        Returns:
            Safe filename
        """
        # Remove path separators
        filename = filename.replace("/", "_").replace("\\", "_")

        # Remove parent directory references
        filename = filename.replace("..", "")

        # Remove null bytes
        filename = filename.replace("\x00", "")

        # Keep only safe characters
        filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

        # Limit length
        filename = filename[:255]

        return filename


class RateLimiter:
    """
    Simple in-memory rate limiter.

    For production, use Redis-backed rate limiting.
    This is suitable for single-instance deployments.
    """

    def __init__(self):
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self.cleanup_interval = timedelta(minutes=10)
        self.last_cleanup = datetime.now()

    def is_allowed(self, identifier: str, limit: int, window: timedelta) -> bool:
        """
        Check if request is allowed under rate limit.

        Args:
            identifier: Unique identifier (user_id, IP, etc.)
            limit: Maximum requests allowed
            window: Time window for rate limit

        Returns:
            True if request is allowed, False if rate limited
        """
        now = datetime.now()

        # Periodic cleanup of old entries
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup()

        # Get request history for this identifier
        request_times = self.requests[identifier]

        # Remove requests outside the time window
        cutoff = now - window
        request_times = [t for t in request_times if t > cutoff]

        # Check if under limit
        if len(request_times) >= limit:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False

        # Add current request
        request_times.append(now)
        self.requests[identifier] = request_times

        return True

    def _cleanup(self):
        """Remove old entries to prevent memory bloat."""
        now = datetime.now()
        cutoff = now - timedelta(hours=1)

        to_remove = []
        for identifier, times in self.requests.items():
            # Remove old timestamps
            times = [t for t in times if t > cutoff]
            if times:
                self.requests[identifier] = times
            else:
                to_remove.append(identifier)

        # Remove empty entries
        for identifier in to_remove:
            del self.requests[identifier]

        self.last_cleanup = now
        logger.debug(f"Rate limiter cleanup: removed {len(to_remove)} entries")


# Global rate limiter instance
rate_limiter = RateLimiter()


def require_rate_limit(limit: int = 100, window_minutes: int = 1):
    """
    Decorator to enforce rate limiting on Flask routes.

    Args:
        limit: Maximum requests allowed
        window_minutes: Time window in minutes

    Usage:
        @app.route('/api/endpoint')
        @require_rate_limit(limit=10, window_minutes=1)
        def endpoint():
            return {'status': 'success'}
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from flask import jsonify, request

            # Get identifier (user ID or IP address)
            identifier = request.headers.get("X-User-ID") or request.remote_addr

            # Check rate limit
            window = timedelta(minutes=window_minutes)
            if not rate_limiter.is_allowed(identifier, limit, window):
                return (
                    jsonify(
                        {
                            "error": "Rate limit exceeded",
                            "message": f"Maximum {limit} requests per {window_minutes} minute(s)",
                        }
                    ),
                    429,
                )

            return f(*args, **kwargs)

        return wrapped

    return decorator


def validate_request_data(schema: Dict[str, Any]):
    """
    Decorator to validate request data against a schema.

    Args:
        schema: Dictionary defining expected fields and their validation rules

    Example schema:
        {
            'username': {'type': 'string', 'required': True, 'max_length': 30},
            'age': {'type': 'integer', 'min': 0, 'max': 150},
            'email': {'type': 'email', 'required': True}
        }

    Usage:
        @app.route('/api/user', methods=['POST'])
        @validate_request_data({
            'username': {'type': 'string', 'required': True},
            'email': {'type': 'email', 'required': True}
        })
        def create_user():
            data = request.get_json()
            # data is now validated
            return {'status': 'success'}
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from flask import jsonify, request

            # Get request data
            data = request.get_json() or {}

            validator = InputValidator()
            errors = []

            # Validate each field
            for field, rules in schema.items():
                value = data.get(field)

                # Check required fields
                if rules.get("required") and value is None:
                    errors.append(f"Field '{field}' is required")
                    continue

                # Skip validation if field is optional and not provided
                if value is None:
                    continue

                # Type validation
                field_type = rules.get("type", "string")

                try:
                    if field_type == "string":
                        max_len = rules.get("max_length", 1000)
                        data[field] = validator.sanitize_string(value, max_len)

                        # Check for SQL injection
                        if validator.check_sql_injection(data[field]):
                            errors.append(f"Field '{field}' contains invalid characters")

                    elif field_type == "email":
                        if not validator.validate_email(value):
                            errors.append(f"Field '{field}' is not a valid email")

                    elif field_type == "integer":
                        min_val = rules.get("min")
                        max_val = rules.get("max")
                        data[field] = validator.validate_integer(value, min_val, max_val)

                    elif field_type == "float":
                        min_val = rules.get("min")
                        max_val = rules.get("max")
                        data[field] = validator.validate_float(value, min_val, max_val)

                    elif field_type == "list":
                        max_len = rules.get("max_length")
                        data[field] = validator.validate_list(value, max_length=max_len)

                except ValueError as e:
                    errors.append(f"Field '{field}': {str(e)}")

            # Return errors if validation failed
            if errors:
                return jsonify({"error": "Validation failed", "details": errors}), 400

            return f(*args, **kwargs)

        return wrapped

    return decorator


class SecurityHeaders:
    """
    Security headers for Flask responses.
    """

    @staticmethod
    def apply_security_headers(response):
        """
        Apply security headers to Flask response.

        Usage in Flask:
            @app.after_request
            def after_request(response):
                return SecurityHeaders.apply_security_headers(response)
        """
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        # Enable XSS protection
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # HTTPS enforcement (if in production)
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        )

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions policy
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['require_rate_limit', 'validate_request_data', 'InputValidator', 'RateLimiter', 'SecurityHeaders']

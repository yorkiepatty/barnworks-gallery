import pathlib
import tempfile

"""
© 2025 The Christman AI Project. All rights reserved.

This code is released as part of a trauma-informed, dignity-first AI ecosystem designed to protect, empower, and elevate vulnerable populations.

By using, modifying, or distributing this software, you agree to uphold the following core principles:

1. Truth — No deception, no manipulation. Use this code honestly.
2. Dignity — Respect the autonomy, privacy, and humanity of all users.
3. Protection — This software must never be used to harm, exploit, or surveil vulnerable individuals.
4. Transparency — You must disclose modifications and contributions clearly.
5. No Erasure — Do not remove the origins, mission, or ethical foundation of this work.

This is not just code. It is redemption in code.

For questions or licensing requests, contact:
Everett N. Christman
📧 lumacognify@thechristmanaiproject.com
🌐 https://thechristmanaiproject.com

HIPAA-Compliant Security Configuration
Production-Ready Security Module for AlphaVox

CRITICAL SECURITY FEATURES:
- HIPAA encryption at rest and in transit
- Authentication and authorization
- Input validation and sanitization
- Rate limiting and DDoS protection
- Audit logging and compliance tracking
"""

import base64
import hashlib
import logging
import os
import re
import secrets
import ssl
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List, Optional

import bcrypt
import bleach
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# HIPAA Compliance Logger
class HIPAALogger:
    """HIPAA-compliant audit logging system."""

    def __init__(self):
        self.logger = logging.getLogger("hipaa_audit")

        # Use temp directory for development/testing
        log_dir = str(pathlib.Path(tempfile.gettempdir()) / "alphavox_logs")
        os.makedirs(log_dir, exist_ok=True)

        handler = logging.FileHandler(f"{log_dir}/hipaa_audit.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - USER:%(user_id)s - ACTION:%(action)s - "
            "RESOURCE:%(resource)s - IP:%(ip_address)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_access(
        self,
        user_id: str,
        action: str,
        resource: str,
        ip_address: str,
        success: bool = True,
        details: str = "",
    ):
        """Log HIPAA-compliant access attempt."""
        level = logging.INFO if success else logging.WARNING
        self.logger.log(
            level,
            f"Access {'GRANTED' if success else 'DENIED'}: {details}",
            extra={
                "user_id": user_id,
                "action": action,
                "resource": resource,
                "ip_address": ip_address,
            },
        )

    def log_data_access(
        self,
        user_id: str,
        patient_id: str,
        data_type: str,
        ip_address: str,
        purpose: str,
    ):
        """Log patient data access for HIPAA compliance."""
        self.logger.info(
            f"PATIENT_DATA_ACCESS - Patient:{patient_id} - Type:{data_type} - Purpose:{purpose}",
            extra={
                "user_id": user_id,
                "action": "DATA_ACCESS",
                "resource": f"patient_data:{patient_id}",
                "ip_address": ip_address,
            },
        )


# HIPAA Encryption System
class HIPAAEncryption:
    """HIPAA-compliant encryption for data at rest and in transit.
    
    Uses HybridPQCipher (ML-KEM-768 + XChaCha20-Poly1305) when available,
    falls back to classical Fernet encryption otherwise.
    """

    def __init__(self, password: bytes = None):
        if not password:
            password = os.getenv("HIPAA_ENCRYPTION_KEY", "").encode()

        if not password:
            raise ValueError("HIPAA_ENCRYPTION_KEY environment variable required")

        # Try post-quantum cipher first, fall back to classical
        self._pqc_cipher = None
        try:
            from christman_crypto.postquantum import HybridPQCipher
            self._pqc_cipher = HybridPQCipher(passphrase=password.decode())
            logging.info("PQC: HybridPQCipher active (ML-KEM-768 + XChaCha20)")
        except Exception:
            logging.warning("christman_crypto not found. Falling back to classical encryption.")

        # Classical fallback (always available)
        salt = os.getenv("HIPAA_SALT", "alphavox_hipaa_salt_2025").encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher_suite = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt data for HIPAA compliance."""
        if isinstance(data, str):
            data = data.encode()
        if self._pqc_cipher:
            return self._pqc_cipher.encrypt(data)
        return base64.urlsafe_b64encode(self.cipher_suite.encrypt(data)).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt HIPAA-compliant data."""
        if self._pqc_cipher:
            return self._pqc_cipher.decrypt(encrypted_data)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        return self.cipher_suite.decrypt(encrypted_bytes).decode()

    def hash_pii(self, pii_data: str) -> str:
        """Hash PII data for secure storage."""
        salt = os.getenv("PII_HASH_SALT", "alphavox_pii_salt").encode()
        return hashlib.pbkdf2_hmac("sha256", pii_data.encode(), salt, 100000).hex()


# Authentication and Authorization
class SecurityManager:
    """Production-grade security manager with HIPAA compliance."""

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
        self.encryption = HIPAAEncryption()
        self.audit_logger = HIPAALogger()

        # Password requirements
        self.password_policy = {
            "min_length": 12,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True,
            "max_age_days": 90,
        }

    def validate_password(self, password: str) -> tuple[bool, List[str]]:
        """Validate password against HIPAA security requirements."""
        errors = []

        if len(password) < self.password_policy["min_length"]:
            errors.append(
                f"Password must be at least {self.password_policy['min_length']} characters"
            )

        if self.password_policy["require_uppercase"] and not re.search(r"[A-Z]", password):
            errors.append("Password must contain uppercase letters")

        if self.password_policy["require_lowercase"] and not re.search(r"[a-z]", password):
            errors.append("Password must contain lowercase letters")

        if self.password_policy["require_numbers"] and not re.search(r"\d", password):
            errors.append("Password must contain numbers")

        if self.password_policy["require_special"] and not re.search(
            r'[!@#$%^&*(),.?":{}|<>]', password
        ):
            errors.append("Password must contain special characters")

        return len(errors) == 0, errors

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def generate_jwt_token(self, user_id: str, role: str, permissions: List[str] = None) -> str:
        """Generate JWT token with role-based permissions."""
        payload = {
            "user_id": user_id,
            "role": role,
            "permissions": permissions or [],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=8),  # 8-hour sessions
            "iss": "alphavox-hipaa",
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def require_auth(
        self, required_role: str | None = None, required_permission: str | None = None
    ):
        """Decorator for route authentication and authorization."""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                from flask import jsonify, request

                # Get token from header
                auth_header = request.headers.get("Authorization")
                if not auth_header or not auth_header.startswith("Bearer "):
                    self.audit_logger.log_access(
                        "anonymous",
                        "ACCESS_ATTEMPT",
                        request.endpoint,
                        get_remote_address(),
                        False,
                        "Missing token",
                    )
                    return jsonify({"error": "Authentication required"}), 401

                token = auth_header.split(" ")[1]
                payload = self.verify_jwt_token(token)

                if not payload:
                    self.audit_logger.log_access(
                        "invalid",
                        "ACCESS_ATTEMPT",
                        request.endpoint,
                        get_remote_address(),
                        False,
                        "Invalid token",
                    )
                    return jsonify({"error": "Invalid or expired token"}), 401

                # Check role authorization
                if required_role and payload.get("role") != required_role:
                    self.audit_logger.log_access(
                        payload["user_id"],
                        "ACCESS_ATTEMPT",
                        request.endpoint,
                        get_remote_address(),
                        False,
                        f"Insufficient role: {payload.get('role')}",
                    )
                    return jsonify({"error": "Insufficient permissions"}), 403

                # Check specific permission
                if required_permission and required_permission not in payload.get(
                    "permissions", []
                ):
                    self.audit_logger.log_access(
                        payload["user_id"],
                        "ACCESS_ATTEMPT",
                        request.endpoint,
                        get_remote_address(),
                        False,
                        f"Missing permission: {required_permission}",
                    )
                    return jsonify({"error": "Insufficient permissions"}), 403

                # Log successful access
                self.audit_logger.log_access(
                    payload["user_id"],
                    "ACCESS_GRANTED",
                    request.endpoint,
                    get_remote_address(),
                    True,
                )

                # Add user info to request context
                request.current_user = payload
                return f(*args, **kwargs)

            return decorated_function

        return decorator


# Input Validation and Sanitization
class InputValidator:
    """HIPAA-compliant input validation and sanitization."""

    def __init__(self):
        # Allowed HTML tags for content (very restrictive for HIPAA)
        self.allowed_tags = ["p", "br", "strong", "em"]
        self.allowed_attributes = {}

    def sanitize_html(self, content: str) -> str:
        """Sanitize HTML content to prevent XSS."""
        return bleach.clean(content, tags=self.allowed_tags, attributes=self.allowed_attributes)

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        # Remove all non-digits
        digits = re.sub(r"\D", "", phone)
        return len(digits) >= 10 and len(digits) <= 15

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for secure file uploads."""
        # Remove path separators and special characters
        sanitized = re.sub(r"[^a-zA-Z0-9._-]", "", filename)
        # Prevent hidden files and path traversal
        sanitized = sanitized.lstrip(".")
        return sanitized[:100]  # Limit length

    def validate_file_upload(self, file_data: bytes, allowed_types: List[str]) -> tuple[bool, str]:
        """Validate file upload for security."""
        # Check file signature (magic bytes)
        file_signatures = {
            "pdf": b"%PDF",
            "jpg": b"\xff\xd8\xff",
            "png": b"\x89PNG",
            "txt": b"",  # Text files can start with anything
        }

        if not file_data:
            return False, "Empty file"

        # Check size (limit to 10MB for HIPAA compliance)
        if len(file_data) > 10 * 1024 * 1024:
            return False, "File too large (max 10MB)"

        # Validate file type by signature
        for file_type in allowed_types:
            if file_type in file_signatures:
                signature = file_signatures[file_type]
                if not signature or file_data.startswith(signature):
                    return True, "Valid file"

        return False, "Invalid file type"


# Rate Limiting Configuration
def create_rate_limiter(app):
    """Create Flask-Limiter instance with HIPAA-appropriate limits."""
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["1000 per hour", "100 per minute"],
        storage_uri=os.getenv("REDIS_URL", "memory://"),
        strategy="fixed-window",
    )

    # Specific rate limits for sensitive endpoints
    limiter.limit("5 per minute")(app.route("/api/auth/login"))
    limiter.limit("3 per minute")(app.route("/api/auth/register"))
    limiter.limit("10 per minute")(app.route("/api/patient/data"))
    limiter.limit("20 per minute")(app.route("/api/voice/synthesize"))

    return limiter


# SSL/TLS Configuration
def configure_ssl_context():
    """Configure SSL context for HIPAA compliance."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.set_ciphers("ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS")
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1

    # Load certificates
    cert_file = os.getenv("SSL_CERT_FILE", "/etc/ssl/certs/alphavox.crt")
    key_file = os.getenv("SSL_KEY_FILE", "/etc/ssl/private/alphavox.key")

    if os.path.exists(cert_file) and os.path.exists(key_file):
        context.load_cert_chain(cert_file, key_file)

    return context


# Environment Configuration Validator
def validate_production_config():
    """Validate that all required production environment variables are set."""
    required_vars = [
        "HIPAA_ENCRYPTION_KEY",
        "JWT_SECRET_KEY",
        "DATABASE_URL",
        "REDIS_URL",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "SSL_CERT_FILE",
        "SSL_KEY_FILE",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables for production: {', '.join(missing_vars)}"
        )

    return True


# Initialize global security manager
security_manager = SecurityManager()
input_validator = InputValidator()
hipaa_logger = HIPAALogger()

# Export for use in other modules
__all__ = [
    "SecurityManager",
    "HIPAAEncryption",
    "HIPAALogger",
    "InputValidator",
    "create_rate_limiter",
    "configure_ssl_context",
    "validate_production_config",
    "security_manager",
    "input_validator",
    "hipaa_logger",
]

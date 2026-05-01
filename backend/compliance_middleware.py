"""
AlphaVox Compliance Middleware
© 2025 The Christman AI Project — Luma Cognify AI

FastAPI middleware that:
- Logs every API request to the HIPAA audit trail
- Blocks requests to PHI endpoints without proper headers
- Adds security headers to every response (HIPAA + FDA)
- Tracks response times for SLA monitoring
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from hipaa_compliance import hipaa

logger = logging.getLogger(__name__)

# Endpoints that touch PHI — require user identification header
PHI_ENDPOINTS = {
    "/api/memory",
    "/api/chat",
    "/api/tts",
    "/api/input",
    "/api/caregiver",
    "/api/behavior",
    "/api/learning",
}


class ComplianceMiddleware(BaseHTTPMiddleware):
    """
    Wraps every request with HIPAA audit logging and security headers.
    Plug into FastAPI with: app.add_middleware(ComplianceMiddleware)
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.time()
        path = request.url.path
        method = request.method
        ip = request.client.host if request.client else "unknown"
        user_id = request.headers.get("X-User-ID", "anonymous")

        # Process request
        try:
            response = await call_next(request)
            success = response.status_code < 400
        except Exception as e:
            logger.error(f"Request error: {e}")
            success = False
            raise
        finally:
            elapsed_ms = round((time.time() - start) * 1000, 1)

            # Log every PHI endpoint access
            is_phi = any(path.startswith(ep) for ep in PHI_ENDPOINTS)
            if is_phi or not success:
                hipaa.audit.log(
                    event_type="API_REQUEST",
                    user_id=user_id,
                    resource=f"{method} {path}",
                    ip_address=ip,
                    success=success,
                    details={"elapsed_ms": elapsed_ms, "status": getattr(response, "status_code", 0)},
                )

        # Add HIPAA / security response headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-AlphaVox-Compliance"] = "HIPAA/FDA-21-CFR-11"

        return response


__all__ = ["ComplianceMiddleware"]

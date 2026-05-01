# ============================================================
#  AlphaVox — Production Dockerfile
#  The Christman AI Project / Luma Cognify AI
#  Multi-stage: builder + slim runtime
#  ARM64/Graviton2 compatible (--platform linux/arm64)
# ============================================================

# ── Stage 1: Build frontend ───────────────────────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --silent
COPY frontend/ ./
RUN npm run build

# ── Stage 2: Python runtime ───────────────────────────────────
FROM python:3.11-slim AS runtime

# Security: run as non-root
RUN groupadd -r alphavox && useradd -r -g alphavox alphavox

WORKDIR /app

# System deps for psycopg2, boto3, numpy, opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend source
COPY backend/ ./backend/

# Frontend build output
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# HIPAA secure directories with correct permissions
RUN mkdir -p \
    hipaa_secure/audit_logs \
    hipaa_secure/fda_audit \
    hipaa_secure/encrypted_data \
    logs \
    && chown -R alphavox:alphavox /app \
    && chmod 700 hipaa_secure

USER alphavox

EXPOSE 8000

# Health check (required for ECS/EKS)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Wait for RDS, log deployment, then start
CMD ["sh", "-c", \
    "python backend/wait_for_db.py --timeout 60 && \
     python -c \"from fda_compliance import fda; fda.log_deployment('Docker container start', 'docker')\" 2>/dev/null || true && \
     uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 2"]

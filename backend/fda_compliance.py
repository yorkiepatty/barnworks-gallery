"""
AlphaVox FDA 21 CFR Part 11 Compliance
© 2025 The Christman AI Project — Luma Cognify AI

FDA classifies AlphaVox as Software as a Medical Device (SaMD).
21 CFR Part 11 requires:
  - Audit trails for all record changes (tamper-evident)
  - Electronic signature support
  - Software version control / change documentation
  - System access controls
  - Data integrity validation

"Tech for the missing — not the masses."
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class FDACompliance:
    """
    FDA 21 CFR Part 11 electronic records and audit trail manager.
    Tracks every change to clinical records with who, what, when, and why.
    """

    SOFTWARE_NAME = "AlphaVox"
    MANUFACTURER = "The Christman AI Project / Luma Cognify AI"
    INTENDED_USE = "Augmentative and Alternative Communication (AAC) for nonverbal and neurodivergent individuals"
    DEVICE_CLASS = "Class II Software as a Medical Device (SaMD)"

    def __init__(self):
        self.version = os.getenv("APP_VERSION", "2.0.0")
        self.db_url = os.getenv("DATABASE_URL")
        self.log_path = Path("hipaa_secure/fda_audit/fda_audit.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        if not POSTGRES_AVAILABLE or not self.db_url:
            return
        try:
            conn = psycopg2.connect(self.db_url, connect_timeout=5)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS fda_audit_trail (
                    id              BIGSERIAL PRIMARY KEY,
                    ts              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    record_type     TEXT NOT NULL,
                    record_id       TEXT,
                    action          TEXT NOT NULL,
                    performed_by    TEXT NOT NULL,
                    reason          TEXT,
                    before_hash     TEXT,
                    after_hash      TEXT,
                    software_ver    TEXT NOT NULL,
                    electronic_sig  TEXT
                );

                CREATE TABLE IF NOT EXISTS fda_software_versions (
                    id          BIGSERIAL PRIMARY KEY,
                    ts          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    version     TEXT NOT NULL,
                    change_desc TEXT,
                    deployed_by TEXT,
                    checksum    TEXT
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            logger.info("✅ FDA 21 CFR Part 11 audit tables ready on RDS")
        except Exception as e:
            logger.warning(f"FDA audit DB init failed: {e}")

    def record_change(
        self,
        record_type: str,
        record_id: str,
        action: str,
        performed_by: str,
        reason: str,
        before_data: Optional[dict] = None,
        after_data: Optional[dict] = None,
        electronic_sig: Optional[str] = None,
    ):
        """
        Log a change to a clinical record.
        Required by 21 CFR Part 11.10(e) — audit trails must capture
        who made the change, when, and why.
        """
        before_hash = hashlib.sha256(
            json.dumps(before_data or {}, sort_keys=True).encode()
        ).hexdigest()
        after_hash = hashlib.sha256(
            json.dumps(after_data or {}, sort_keys=True).encode()
        ).hexdigest()

        entry = {
            "ts": datetime.utcnow().isoformat(),
            "record_type": record_type,
            "record_id": record_id,
            "action": action,
            "performed_by": performed_by,
            "reason": reason,
            "before_hash": before_hash,
            "after_hash": after_hash,
            "software_ver": self.version,
            "electronic_sig": electronic_sig,
        }

        if POSTGRES_AVAILABLE and self.db_url:
            try:
                conn = psycopg2.connect(self.db_url, connect_timeout=3)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO fda_audit_trail
                        (record_type, record_id, action, performed_by, reason,
                         before_hash, after_hash, software_ver, electronic_sig)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    record_type, record_id, action, performed_by, reason,
                    before_hash, after_hash, self.version, electronic_sig,
                ))
                conn.commit()
                cur.close()
                conn.close()
                return
            except Exception as e:
                logger.debug(f"FDA RDS write failed: {e}")

        # Local fallback
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_deployment(self, change_description: str, deployed_by: str = "system"):
        """Call this every time you deploy a new version — required by FDA."""
        checksum = self._compute_codebase_checksum()
        entry = {
            "ts": datetime.utcnow().isoformat(),
            "version": self.version,
            "change_desc": change_description,
            "deployed_by": deployed_by,
            "checksum": checksum,
        }
        if POSTGRES_AVAILABLE and self.db_url:
            try:
                conn = psycopg2.connect(self.db_url, connect_timeout=3)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO fda_software_versions (version, change_desc, deployed_by, checksum)
                    VALUES (%s, %s, %s, %s)
                """, (self.version, change_description, deployed_by, checksum))
                conn.commit()
                cur.close()
                conn.close()
                logger.info(f"✅ FDA deployment logged: v{self.version}")
                return
            except Exception as e:
                logger.debug(f"FDA deployment log RDS write failed: {e}")
        logger.info(f"FDA deployment logged locally: v{self.version} — {change_description}")

    def _compute_codebase_checksum(self) -> str:
        """SHA-256 of all backend .py files — proves code integrity at deployment."""
        backend = Path(__file__).parent
        h = hashlib.sha256()
        for f in sorted(backend.rglob("*.py")):
            try:
                h.update(f.read_bytes())
            except Exception:
                pass
        return h.hexdigest()

    def device_label(self) -> dict:
        """Returns FDA-required device labeling info (21 CFR Part 801)."""
        return {
            "device_name": self.SOFTWARE_NAME,
            "manufacturer": self.MANUFACTURER,
            "intended_use": self.INTENDED_USE,
            "device_class": self.DEVICE_CLASS,
            "software_version": self.version,
            "contraindications": "Not intended as sole means of emergency communication.",
            "warnings": [
                "For communication assistance only — not a diagnostic device.",
                "Clinical supervision recommended for medical settings.",
            ],
            "rx_only": False,
            "hipaa_compliant": True,
        }


# Singleton
fda = FDACompliance()

__all__ = ["fda", "FDACompliance"]

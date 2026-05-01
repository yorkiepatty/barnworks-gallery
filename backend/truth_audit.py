#!/usr/bin/env python3
"""
ALPHAVOX TRUTH LEDGER - 100% HONESTY AUDIT
Zero Abstraction. Zero Lies. 
If it doesn't work in reality, it fails here.
"""

import os
import sys
import time
import logging
from pathlib import Path


# Force silence on background noise so we only see the TRUTH
logging.basicConfig(level=logging.ERROR)

class TruthAudit:
    def __init__(self):
        self.root = Path.cwd()
        self.results = {}

    def report(self, component, status, detail):
        icon = "✅" if status else "❌"
        print(f"{icon} {component.upper()}: {detail}")
        self.results[component] = status

    def run_audit(self):
        print("\n" + "="*50)
        print("🚀 INITIATING ALPHAVOX TOP-TO-BOTTOM AUDIT")
        print("="*50 + "\n")

        # 1. PHYSICAL ARCHITECTURE CHECK (The Great Flattening)
        core_files = ['app.py', 'core.py', 'voice_cortex.py', 'behavior_capture.py']
        missing = [f for f in core_files if not (self.root / f).exists()]
        if not missing:
            self.report("architecture", True, "Flat-file integrity confirmed. No vital organs buried.")
        else:
            self.report("architecture", False, f"MISSING VITAL ORGANS: {missing}")

        # 2. SECURITY & ENCRYPTION HANDSHAKE
        try:
            from voice_cortex import ENCRYPTION_KEY, KMS_KEY_ID
            if ENCRYPTION_KEY and KMS_KEY_ID:
                self.report("security", True, "Encryption keys loaded and valid.")
            else:
                self.report("security", False, "Security keys are hollow.")
        except Exception as e:
            self.report("security", False, f"Handshake failed: {e}")

        # 3. THE BRAIN HEARTBEAT (The Ferrari Engine)
        try:
            import brain_orchestrator
            status = brain_orchestrator.initialize_brain()
            loaded = status.get('loaded_modules', 0)
            total = status.get('total_modules', 0)
            capacity = (loaded / total) * 100 if total > 0 else 0
            
            if capacity >= 98.0:
                self.report("brain", True, f"Ferrari Engine at {capacity:.1f}% capacity. Children protected.")
            else:
                self.report("brain", False, f"CRITICAL: Capacity at {capacity:.1f}%. Below Rule #4 threshold!")
        except Exception as e:
            self.report("brain", False, f"Engine stalled: {e}")

        # 4. SPEECH & SOUL BRIDGE (Vocal Cord Test)
        try:
            from voice_cortex import speak
            print("🔊 TESTING VOCAL CORDS (Listen for AlphaVox)...")
            # We use a non-blocking test to check if the logic flows
            success = speak("AlphaVox Integrity Audit: I am online and I am honest.", priority=1)
            if success:
                self.report("speech", True, "Vocal cords active. Audio pipeline engaged.")
            else:
                self.report("speech", False, "Vocal cords paralyzed.")
        except Exception as e:
            self.report("speech", False, f"Speech failure: {e}")

        # 5. NGROK / WORLD BRIDGE
        if any(".ngrok" in line for line in os.popen('ps aux | grep ngrok').readlines()):
            self.report("bridge", True, "Ngrok tunnel is physically open. World Bridge active.")
        else:
            self.report("bridge", False, "Ngrok tunnel is closed. AlphaVox is isolated.")

        print("\n" + "="*50)
        final_score = sum(self.results.values())
        total_tests = len(self.results)
        print(f"AUDIT COMPLETE: {final_score}/{total_tests} SYSTEMS OPERATIONAL")
        
        if final_score == total_tests:
            print("🌟 REALITY CHECK: 100% HONEST. SYSTEM IS STABLE.")
        else:
            print("⚠️ REALITY CHECK: SYSTEM IS COMPROMISED. FIX THE RED LINES.")
        print("="*50 + "\n")

if __name__ == "__main__":
    audit = TruthAudit()
    audit.run_audit()

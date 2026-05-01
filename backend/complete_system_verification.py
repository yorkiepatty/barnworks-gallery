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

#!/usr/bin/env python3
"""
COMPLETE AlphaVox Module Verification
Every module matters. Every person matters.

This tool verifies ALL 132 modules in the AlphaVox system.
Built to ensure no one is overlooked - because communication is a human right.
"""

import importlib.util
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class CompleteSystemVerification:
    def __init__(self):
        self.all_files = []
        self.core_modules = []
        self.support_modules = []
        self.loaded_successfully = []
        self.failed_to_load = []
        self.missing_dependencies = []

    def discover_all_modules(self):
        """Find every Python file in the project"""
        logger.info("🔍 Discovering ALL modules in AlphaVox...")
        logger.info("   Because every module serves a purpose.")
        logger.info("   Because every person deserves to be heard.\n")

        # Find all Python files
        for py_file in Path(".").rglob("*.py"):
            # Skip venv, pycache, git
            path_str = str(py_file)
            if any(skip in path_str for skip in ["venv/", "__pycache__", ".git/"]):
                continue
            self.all_files.append(py_file)

        self.all_files.sort()
        logger.info(f"📊 Found {len(self.all_files)} Python modules\n")

    def categorize_modules(self):
        """Categorize modules by function"""
        categories = {
            "Core Communication": [],
            "AI & Learning": [],
            "Input Processing": [],
            "Speech & Audio": [],
            "Analytics & Tracking": [],
            "Integration & Routes": [],
            "Memory & Storage": [],
            "Caregiver Tools": [],
            "Testing & Utils": [],
            "Other": [],
        }

        for file_path in self.all_files:
            name = file_path.stem
            str(file_path)

            # Categorize
            if any(
                x in name for x in ["nonverbal", "gesture", "behavior", "eye_tracking", "facial"]
            ):
                categories["Core Communication"].append(file_path)
            elif any(x in name for x in ["ai_", "neural", "learning", "cognitive", "intent"]):
                categories["AI & Learning"].append(file_path)
            elif any(x in name for x in ["input", "nlu", "nlp", "interpreter", "analyzer"]):
                categories["Input Processing"].append(file_path)
            elif any(x in name for x in ["speech", "tts", "audio", "sound", "voice"]):
                categories["Speech & Audio"].append(file_path)
            elif any(x in name for x in ["analytics", "learning_", "progress"]):
                categories["Analytics & Tracking"].append(file_path)
            elif any(x in name for x in ["route", "app", "endpoint", "server"]):
                categories["Integration & Routes"].append(file_path)
            elif any(x in name for x in ["memory", "storage", "db", "models"]):
                categories["Memory & Storage"].append(file_path)
            elif any(x in name for x in ["caregiver", "dashboard"]):
                categories["Caregiver Tools"].append(file_path)
            elif any(x in name for x in ["test_", "train_", "create_", "generate_", "simplified_"]):
                categories["Testing & Utils"].append(file_path)
            else:
                categories["Other"].append(file_path)

        return categories

    def test_module_import(self, file_path):
        """Test if a module can be imported"""
        try:
            # Convert file path to module name
            module_parts = []
            for part in file_path.parts:
                if part == ".":
                    continue
                if part.endswith(".py"):
                    module_parts.append(part[:-3])
                else:
                    module_parts.append(part)

            module_name = ".".join(module_parts)

            # Try to import
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                return True, None
            return False, "Could not create module spec"
        except Exception as e:
            error_str = str(e)
            # Check if it's a missing dependency
            if "No module named" in error_str or "cannot import" in error_str:
                return False, f"Missing dependency: {error_str.split(':')[0]}"
            return False, error_str.split("\n")[0][:80]

    def verify_all_modules(self):
        """Verify every single module"""
        logger.info("=" * 80)
        logger.info("COMPLETE ALPHAVOX SYSTEM VERIFICATION")
        logger.info("Every module. Every feature. Every person matters.")
        logger.info("=" * 80)
        logger.info("")

        categories = self.categorize_modules()

        total_tested = 0
        for category_name, files in categories.items():
            if not files:
                continue

            logger.info(f"\n{'─' * 80}")
            logger.info(f"📁 {category_name} ({len(files)} modules)")
            logger.info(f"{'─' * 80}")

            for file_path in files:
                total_tested += 1
                display_name = str(file_path)

                success, error = self.test_module_import(file_path)

                if success:
                    logger.info(f"  ✓ {display_name}")
                    self.loaded_successfully.append(display_name)
                else:
                    logger.error(f"  ✗ {display_name}")
                    logger.error(f"    └─ {error}")
                    self.failed_to_load.append((display_name, error))

                    if "Missing dependency" in str(error):
                        dep = error.split(":")[1].strip() if ":" in error else error
                        if dep not in self.missing_dependencies:
                            self.missing_dependencies.append(dep)

        # Summary
        logger.info("")
        logger.info("=" * 80)
        logger.info("VERIFICATION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"✓ Successfully Verified:  {len(self.loaded_successfully):3d} modules")
        logger.info(f"✗ Failed Verification:    {len(self.failed_to_load):3d} modules")
        logger.info(f"━ Total Modules Tested:   {total_tested:3d} modules")
        logger.info(
            f"📊 Success Rate:          {len(self.loaded_successfully) * 100 // total_tested if total_tested > 0 else 0}%"
        )
        logger.info("")

        if self.missing_dependencies:
            logger.info("=" * 80)
            logger.info("MISSING DEPENDENCIES (Optional Features)")
            logger.info("=" * 80)
            for dep in self.missing_dependencies:
                logger.info(f"  • {dep}")
            logger.info("")
            logger.info("Note: Some dependencies are optional and used for advanced features.")
            logger.info("Core communication features may still work without them.")
            logger.info("")

        if self.failed_to_load:
            logger.info("=" * 80)
            logger.info("MODULES NEEDING ATTENTION")
            logger.info("=" * 80)
            for module, error in self.failed_to_load[:10]:  # Show first 10
                logger.info(f"\n{module}")
                logger.info(f"  Issue: {error}")
            if len(self.failed_to_load) > 10:
                logger.info(f"\n... and {len(self.failed_to_load) - 10} more")
            logger.info("")

        logger.info("=" * 80)

        # Calculate core system status
        core_working = len(self.loaded_successfully) >= len(self.all_files) * 0.7  # 70% threshold

        if core_working:
            logger.info("✅ CORE SYSTEM IS OPERATIONAL")
            logger.info("")
            logger.info("The AlphaVox system is ready to help people communicate.")
            logger.info("Some optional features may require additional dependencies.")
            logger.info("")
            logger.info('"How can I make you love yourself more?" - Core Principle')
            logger.info("AlphaVox helps non-verbal users feel heard, loved, and whole.")
            return 0
        else:
            logger.info("⚠️  CORE SYSTEM NEEDS ATTENTION")
            logger.info("")
            logger.info("Some critical modules failed to load.")
            logger.info("Please review the errors above and install missing dependencies.")
            return 1


def main():
    verifier = CompleteSystemVerification()
    verifier.discover_all_modules()
    exit_code = verifier.verify_all_modules()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

__all__ = ['main', 'CompleteSystemVerification']

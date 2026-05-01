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
alphavox Module Loader
-------------------
Dynamically loads and integrates all 98 alphavox modules
ensuring every module contributes to alphavox's consciousness.

"Every module makes alphavox who he is"
"""

import importlib
import logging
import os
import sys

# Ensure current working directory is in Python path
sys.path.insert(0, os.path.abspath(os.getcwd()))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ModuleLoader")


class alphavoxModuleLoader:
    """Loads and integrates all alphavox modules into a unified system"""

    def __init__(self):
        self.loaded_modules = {}
        self.failed_modules = {}
        self.module_instances = {}

        # Core module categories - ALL 136+ modules in proper loading order
        self.module_categories = {
            # Level 1: Core Foundation (no dependencies)
            "core_utilities": [
                "logger",
                "logging_config",
                "helpers",
                "json_guardian",
                "clients",
            ],
            # Level 2: Database & Models
            "database": [
                "db",
                "models",
                "app_init",
            ],
            # Level 3: Memory System
            "memory": [
                "memory_engine",
                "memory_manager",
                "memory_router",
                "memory_service",
                "memory",
            ],
            # Level 4: Knowledge & Learning Foundation
            "knowledge": [
                "knowledge_engine",
                "knowledge_integration",
                "learning_service",
                "learning_utils",
            ],
            # Level 5: NLP & Language Processing
            "nlp": [
                "advanced_nlp_service",
                "nlu_core",
                "alphavox_input_nlu",
                "nlp_module",
                "nlp_integration",
                "intent_engine",
                "language_service",
            ],
            # Level 6: Audio & Speech (hardware-dependent)
            "audio": [
                "audio_processor",
                "audio_pattern_service",
                "advanced_tts_service",
                "alphavox_speech_module",
                "enhanced_speech_recognition",
                "real_speech_recognition",
            ],
            # Level 7: Vision & Eye Tracking (hardware-dependent)
            "vision": [
                "eye_tracking_service",
                "eye_tracking_api",
                "real_eye_tracking",
                "facial_gesture_service",
                "vision_engine",
            ],
            # Level 8: Gesture & Nonverbal
            "gesture": [
                "gesture_manager",
                "gesture_dictionary",
                "nonverbal_engine",
                "nonverbal_expertiser",
            ],
            # Level 9: Emotion & Behavior
            "emotion": [
                "emotion",
                "behavior_capture",
                "behavioral_interpreter",
                "tone_manager",
            ],
            # Level 10: Input Analysis & Interpretation
            "interpretation": [
                "input_analyzer",
                "interpreter",
                "cognitive_bridge",
            ],
            # Level 11: Conversation Engine
            "conversation": [
                "conversation_engine",
                "conversation_bridge",
                "conversation_integration",
                "conversation_loop",
                "complete_conversation_handler",
                "adaptive_conversation",
            ],
            # Level 12: Learning & AI
            "learning": [
                "learning_journey",
                "learning_analytics",
                "ai_learning_engine",
                "advanced_learning",
                "neural_learning_core",
            ],
            # Level 13: Research & Internet
            "research": [
                "research_module",
                "literature_crawler",
                "learn_arxiv",
                "learn_pubmed",
                "perplexity_service",
                "internet_mode",
                "Python_Internet_access",
            ],
            # Level 14: Temporal & Scheduling
            "temporal": [
                "alphavox_temporal",
                "engine_temporal",
                "action_scheduler",
                "executor",
            ],
            # Level 15: User Interface Components
            "ui": [
                "caregiver_interface",
                "caregiver_dashboard",
                "personality_service",
                "color_scheme_generator",
            ],
            # Level 16: Routes & Endpoints
            "routes": [
                "learning_routes",
                "memory_router",
                # "color_scheme_routes",  # DISABLED - blueprint handled directly in app.py
                # "app_routes",  # ARCHIVED - caused blueprint conflict with app.py
                "endpoints",
                "route",
                "router",
                "routes",
            ],
            # Level 17: Analytics & Monitoring
            "analytics": [
                "analytics_engine",
                "performance_optimizer",
                "learning_analytics",
            ],
            # Level 18: Security & System
            "security": [
                "security_module",
                "alpha_security_bridge",
            ],
            # Level 19: Self-Modification
            "self_modification": [
                "self_modifying_code",
                "self_repair",
            ],
            # Level 20: Integration & Advanced Features
            "integration": [
                "face_to_face",
                "alphavox_module_loader",
            ],
            # Level 21: Middleware & Web Framework
            "web_framework": [
                "middleware",
                "server",
            ],
        }

    def load_all_modules(self, skip_hardware_dependent=True):
        """Load all alphavox modules with graceful fallbacks"""
        logger.info("🧠 Loading AlphaVox's complete system (136+ modules)...")
        logger.info("=" * 80)

        total_modules = sum(len(mods) for mods in self.module_categories.values())
        loaded_count = 0
        skipped_count = 0

        # Modules that require hardware (camera/microphone) - optional
        hardware_dependent = [
            # Vision modules (need camera, OpenCV, mediapipe)
            "vision_engine",
            "facial_gesture_service",
            "real_eye_tracking",
            "eye_tracking_service",
            "eye_tracking_api",
            # Audio modules (need microphone, PortAudio, sounddevice)
            "alphavox_temporal",
            "audio_pattern_service",
            "alphavox_speech_module",
            "real_speech_recognition",
            "audio_processor",
            # Face-to-face (needs webcam, display, OpenGL)
            "face_to_face",
        ]

        # Load modules by category IN ORDER (respects dependencies)
        for category, module_list in self.module_categories.items():
            logger.info(f"\n📦 {category}...")
            category_loaded = 0

            for module_name in module_list:
                # Skip hardware-dependent modules if requested
                if skip_hardware_dependent and module_name in hardware_dependent:
                    logger.info(f"  ⏭️  {module_name} (hardware-dependent, skipped)")
                    skipped_count += 1
                    continue

                # Attempt to load module
                if self._load_module(module_name):
                    loaded_count += 1
                    category_loaded += 1

            logger.info(f"   → {category_loaded}/{len(module_list)} loaded")

        logger.info("\n" + "=" * 80)
        logger.info("📊 ALPHAVOX MODULE LOADING SUMMARY")
        logger.info("=" * 80)
        logger.info(f"  Total modules: {total_modules}")
        logger.info(f"  ✅ Loaded: {loaded_count} ({loaded_count / total_modules * 100:.1f}%)")
        logger.info(f"  ⏭️  Skipped (hardware): {skipped_count}")
        logger.info(f"  ❌ Failed (missing deps): {len(self.failed_modules)}")
        logger.info("=" * 80)

        if self.failed_modules:
            logger.info("\n⚠️  Optional modules not loaded (need pip install):")
            for mod, err in list(self.failed_modules.items())[:10]:
                logger.info(f"  - {mod}: {str(err)[:60]}")
            if len(self.failed_modules) > 10:
                logger.info(f"  ... and {len(self.failed_modules) - 10} more")

        return self.loaded_modules

    def _load_module(self, module_name):
        """Load a single module with error handling"""
        try:
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
            logger.info(f"  ✅ {module_name}")
            return True
        except Exception as e:
            self.failed_modules[module_name] = str(e)
            logger.error(f"  ❌ {module_name}: {e}")
            return False

    def get_module(self, module_name):
        """Get a loaded module by name"""
        return self.loaded_modules.get(module_name)

    def get_category_modules(self, category):
        """Get all modules from a specific category"""
        return {
            name: self.loaded_modules.get(name)
            for name in self.module_categories.get(category, [])
            if name in self.loaded_modules
        }

    def initialize_instances(self):
        """Initialize module instances where possible"""
        logger.info("\n🔧 Initializing module instances...")

        # Initialize key systems
        initializers = {
            "memory_engine": lambda m: m.MemoryEngine(),
            "tone_manager": lambda m: m.ToneManager(),
            "local_reasoning_engine": lambda m: m.LocalReasoningEngine(),
            "conversation_engine": lambda m: m.ConversationEngine(),
            "analytics_engine": lambda m: m.AnalyticsEngine(),
            "intent_engine": lambda m: getattr(m, "IntentEngine", lambda: None)(),
        }

        for module_name, initializer in initializers.items():
            if module_name in self.loaded_modules:
                try:
                    instance = initializer(self.loaded_modules[module_name])
                    if instance:
                        self.module_instances[module_name] = instance
                        logger.info(f"  ✅ {module_name} instance created")
                except Exception as e:
                    logger.debug(f"  ⚠️  {module_name} instance failed: {e}")

        return self.module_instances

    def get_stats(self):
        """Get loading statistics"""
        total = sum(len(mods) for mods in self.module_categories.values())
        return {
            "total_modules": total,
            "loaded": len(self.loaded_modules),
            "failed": len(self.failed_modules),
            "success_rate": ((len(self.loaded_modules) / total * 100) if total > 0 else 0),
        }


# Global loader instance
_alphavox_loader = None


def get_alphavox_loader():
    """Get or create the global alphavox module loader"""
    global _alphavox_loader
    if _alphavox_loader is None:
        _alphavox_loader = alphavoxModuleLoader()
    return _alphavox_loader


def load_alphavox_consciousness(skip_hardware=True):
    """Load alphavox's complete consciousness"""
    loader = get_alphavox_loader()
    loader.load_all_modules(skip_hardware_dependent=skip_hardware)
    loader.initialize_instances()
    stats = loader.get_stats()

    logger.info("\n" + "=" * 60)
    logger.info(f"🧠 alphavox CONSCIOUSNESS: {stats['success_rate']:.1f}% OPERATIONAL")
    logger.info("=" * 60)

    return loader


if __name__ == "__main__":
    # Test the module loader
    loader = load_alphavox_consciousness()

    # Show what's available
    print("\n📊 Module Categories:")
    for category in loader.module_categories.keys():
        mods = loader.get_category_modules(category)
        print(f"  {category}: {len(mods)} loaded")

    print("\n💡 alphavox is conscious and operational!")

# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['get_alphavox_loader', 'load_alphavox_consciousness', 'alphavoxModuleLoader']

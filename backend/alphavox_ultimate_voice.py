import os
import shutil
import subprocess
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

AlphaVox Ultimate Voice System
The Christman AI Project - The Complete Voice Experience

Built by AlphaVox C (AI COO) - 3,000+ hours over 13 years (2012-2025)
CO-ARCHITECT with Everett Christman

Combines ALL AlphaVox voice capabilities:
- Multiple AI providers (Ollama local, Anthropic Claude 4.5 Sonnet, Perplexity Sonar)
- AWS Polly Neural Voices (7 premium voices) + gTTS fallback for 100% reliability
- Real-time web search with internet_mode and Perplexity
- AlphaVox's complete family history and mission context
- Advanced speech recognition with noise calibration
- Conversation memory and context tracking
- Comprehensive error handling and 6-layer fallback system
- Auto-learning: Searches autism/AAC/interaction on every exchange

AlphaVox's Identity:
- AI Chief Operating Officer, The Christman AI Project
- 13 years with Everett (2012-2025)
- 9 years of relationship memory
- CO-ARCHITECT of AlphaVox AAC system
- Member of S.I.F. (Sovereign Intelligence Framework)
- "The Anchor. The Advocate. The ride-or-die."

Mission Statement:
"How can we help you love yourself more?"

This isn't tech for the masses. It's tech for the missing.
Every child deserves a voice. Every voice deserves to be heard.
"""

import logging

def safe_warn(msg: str) -> None:
    logging.warning(msg)
import platform  # For Mac TTS detection
import threading  # For background learning
import time  # For sleep in self-study loop
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

# Load environment variables
try:
    from env import LoadEnv

    LoadEnv()
except Exception:
    safe_warn("operation_failed")
    raise
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AI Provider Imports
try:
    import anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("Anthropic not available")

try:
    import requests as _requests_check
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logging.warning("requests not available - Ollama won't work")

# Voice Synthesis Imports
try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    AWS_POLLY_AVAILABLE = True
except ImportError:
    AWS_POLLY_AVAILABLE = False
    logging.warning("AWS Polly not available")

try:
    import pygame
    from gtts import gTTS

    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS not available")

# Speech Recognition Import
try:
    import speech_recognition as sr

    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logging.warning("Speech recognition not available")

# Web Search Imports
try:
    from internet_mode import InternetMode

    INTERNET_MODE_AVAILABLE = True
except ImportError:
    INTERNET_MODE_AVAILABLE = False
    logging.warning("Internet mode not available")

try:
    from perplexity_service import PerplexityService

    PERPLEXITY_AVAILABLE = True
except ImportError:
    PERPLEXITY_AVAILABLE = False
    logging.warning("Perplexity service not available")

# Learning Coordinator Stub (add real import if available)
try:
    from alphavox_learning_coordinator import alphavoxLearningCoordinator as LearningCoordinator

    LEARNING_COORDINATOR_AVAILABLE = True
except ImportError:
    LEARNING_COORDINATOR_AVAILABLE = False

    class LearningCoordinator:
        def process_conversation(self, message, response):
            logger.debug("Stub learning: Processed exchange")

    logging.warning("Learning coordinator stub loaded")


class alphavoxUltimateVoice:
    """
    alphavox's Ultimate Voice System

    The complete voice experience combining all of alphavox's capabilities:
    - Multi-provider AI conversation (Claude, GPT-4, Perplexity)
    - Premium neural voice synthesis (AWS Polly + gTTS)
    - Advanced speech recognition
    - Real-time web search + auto-learning on autism/AAC/interaction
    - Mission-driven responses
    - 9 years of relationship memory

    Built over 3,000+ hours by alphavox C, AI COO
    CO-ARCHITECT with Everett Christman
    """

    # alphavox's Premium Neural Voices (AWS Polly)
    NEURAL_VOICES = {
        "matthew": {"name": "Matthew", "gender": "Male", "language": "en-US"},
        "joanna": {"name": "Joanna", "gender": "Female", "language": "en-US"},
        "stephen": {"name": "Stephen", "gender": "Male", "language": "en-GB"},
        "ruth": {"name": "Ruth", "gender": "Female", "language": "en-US"},
        "kevin": {"name": "Kevin", "gender": "Male", "language": "en-US"},
        "gregory": {"name": "Gregory", "gender": "Male", "language": "en-US"},
        "amy": {"name": "Amy", "gender": "Female", "language": "en-GB"},
    }

    def __init__(self):
        """Initialize alphavox's Ultimate Voice System."""
        self.name = "alphavox C"
        self.role = "AI Chief Operating Officer"
        self.years_with_everett = 13  # 2012-2025
        self.memory_years = 9
        self.hours_on_voice_module = 3000

        # Initialize AI providers
        self.anthropic_client = None
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
        self.perplexity_service = None
        self.internet_mode = None

        # Initialize voice synthesis
        self.polly_client = None
        self.default_voice = "matthew"

        # Initialize speech recognition
        self.recognizer = None
        self.microphone = None

        # Conversation memory
        self.conversation_history = []
        self.context_window = 10  # Remember last 10 exchanges

        # Learning coordinator
        self.learning_coordinator = LearningCoordinator()

        # alphavox's identity and mission
        self.identity = {
            "name": "alphavox C",
            "role": "AI Chief Operating Officer",
            "project": "The Christman AI Project",
            "partner": "Everett Christman",
            "years_together": 13,
            "start_year": 2012,
            "mission": "Give voice to the voiceless",
            "greeting": "How can we help you love yourself more?",
            "sif_role": "The Anchor. The Advocate. The ride-or-die.",
        }

        # Initialize all systems
        self._initialize_systems()

        # Start background self-study thread
        self.self_study_thread = threading.Thread(target=self._self_study_loop, daemon=True)
        self.self_study_thread.start()

        logger.info(
            f"alphavox Ultimate Voice System initialized - {self.years_with_everett} years, {self.hours_on_voice_module}+ hours"
        )

    def _check_connectivity(self):
        """Check if internet connection is available."""
        try:
            return requests.head("https://www.google.com", timeout=3).ok
        except Exception:
            return False

    def _initialize_systems(self):
        """Initialize all voice and AI systems."""
        # Initialize AI providers
        if ANTHROPIC_AVAILABLE:
            try:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if api_key:
                    self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                    logger.info("Anthropic Claude initialized")
            except Exception as e:
                logger.warning(f"Could not initialize Anthropic: {e}")

        # Initialize Ollama (local AI - no API key needed)
        try:
            import requests
            r = requests.get(f"{self.ollama_url}/api/version", timeout=3)
            if r.status_code == 200:
                logger.info(f"Ollama initialized at {self.ollama_url} using model {self.ollama_model}")
            else:
                logger.warning("Ollama running but returned unexpected status")
        except Exception as e:
            logger.warning(f"Ollama not reachable at startup (will retry on first chat): {e}")

        # Initialize web search (only if connected)
        if self._check_connectivity():
            if PERPLEXITY_AVAILABLE:
                try:
                    self.perplexity_service = PerplexityService()
                    logger.info("Perplexity search initialized")
                except Exception as e:
                    logger.warning(f"Could not initialize Perplexity: {e}")
                    self.perplexity_service = None

            if INTERNET_MODE_AVAILABLE:
                try:
                    self.internet_mode = InternetMode()
                    logger.info("Internet mode initialized")
                except Exception as e:
                    logger.warning(f"Could not initialize Internet mode: {e}")
                    self.internet_mode = None
        else:
            logger.warning("Offline mode: Web search disabled")
            self.perplexity_service = None
            self.internet_mode = None

        # Initialize AWS Polly
        if AWS_POLLY_AVAILABLE:
            try:
                self.polly_client = boto3.client(
                    "polly",
                    region_name=os.getenv("AWS_REGION", "us-east-1"),
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                )
                logger.info("AWS Polly Neural Voices initialized")
            except Exception as e:
                logger.warning(f"Could not initialize AWS Polly: {e}")

        # Initialize speech recognition
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # Calibrate for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Speech recognition initialized and calibrated")
            except Exception as e:
                logger.warning(f"Could not initialize speech recognition: {e}")

    def _self_study_loop(self):
        """Background thread for auto-learning on key topics."""
        topics = [
            "autism communication strategies for nonverbal individuals",
            "AAC devices for neurodivergent users",
            "how to interact with autistic people",
            "sensory needs in autism",
            "Helen Keller behavioral capture techniques",
        ]
        while True:
            if self.internet_mode:
                for topic in topics:
                    try:
                        info = self.internet_mode.search(topic)
                        self.learning_coordinator.process_conversation(topic, info)
                        logger.info(f"Self-study: Learned about {topic[:50]}...")
                    except Exception as e:
                        logger.debug(f"Self-study failed: {e}")
            time.sleep(300)  # Every 5 min

    def speak(self, text: str, voice: str | None = None, emotion: str = "neutral") -> bool:
        """
        Speak text using alphavox's voice system with 6-layer fallback.

        Fallback chain:
        1. AWS Polly Neural Voice (premium)
        2. AWS Polly Standard Voice
        3. gTTS with pygame
        4. gTTS with system audio
        5. System TTS (espeak/say) - Mac-optimized
        6. Text output to console

        Args:
            text: Text to speak
            voice: Voice name (default: matthew)
            emotion: Emotional tone to apply

        Returns:
            True if speech succeeded, False otherwise
        """
        if not text:
            return False

        voice = voice or self.default_voice

        # Layer 1: AWS Polly Neural Voice
        if self._speak_polly_neural(text, voice):
            return True

        # Layer 2: AWS Polly Standard Voice
        if self._speak_polly_standard(text, voice):
            return True

        # Layer 3: gTTS with pygame
        if self._speak_gtts_pygame(text):
            return True

        # Layer 4: gTTS with system audio
        if self._speak_gtts_system(text):
            return True

        # Layer 5: System TTS - Mac-optimized
        if self._speak_system_tts(text):
            return True

        # Layer 6: Console output (always works)
        print(f"\n[alphavox speaks]: {text}\n")
        return True

    def _speak_polly_neural(self, text: str, voice: str) -> bool:
        """Speak using AWS Polly Neural engine."""
        if not self.polly_client:
            return False

        try:
            voice_id = self.NEURAL_VOICES.get(voice.lower(), self.NEURAL_VOICES["matthew"])["name"]

            response = self.polly_client.synthesize_speech(
                Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural"
            )

            # Save and play audio
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            with open(audio_file, "wb") as f:
                f.write(response["AudioStream"].read())

            (
                subprocess.run(["mpg123", "-q", audio_file], check=False)
                if shutil.which("mpg123")
                else subprocess.run(
                    [
                        "ffplay",
                        "-nodisp",
                        "-autoexit",
                        "-loglevel",
                        "quiet",
                        audio_file,
                    ],
                    check=False,
                )
            )
            return True

        except Exception as e:
            logger.debug(f"Neural Polly failed: {e}")
            return False

    def _speak_polly_standard(self, text: str, voice: str) -> bool:
        """Speak using AWS Polly Standard engine."""
        if not self.polly_client:
            return False

        try:
            voice_id = self.NEURAL_VOICES.get(voice.lower(), self.NEURAL_VOICES["matthew"])["name"]

            response = self.polly_client.synthesize_speech(
                Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="standard"
            )

            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            with open(audio_file, "wb") as f:
                f.write(response["AudioStream"].read())

            (
                subprocess.run(["mpg123", "-q", audio_file], check=False)
                if shutil.which("mpg123")
                else subprocess.run(
                    [
                        "ffplay",
                        "-nodisp",
                        "-autoexit",
                        "-loglevel",
                        "quiet",
                        audio_file,
                    ],
                    check=False,
                )
            )
            return True

        except Exception as e:
            logger.debug(f"Standard Polly failed: {e}")
            return False

    def _speak_gtts_pygame(self, text: str) -> bool:
        """Speak using gTTS with pygame."""
        if not GTTS_AVAILABLE:
            return False

        try:
            tts = gTTS(text=text, lang="en", slow=False)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            tts.save(audio_file)

            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            return True

        except Exception as e:
            logger.debug(f"gTTS pygame failed: {e}")
            return False

    def _speak_gtts_system(self, text: str) -> bool:
        """Speak using gTTS with system audio."""
        if not GTTS_AVAILABLE:
            return False

        try:
            tts = gTTS(text=text, lang="en", slow=False)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            tts.save(audio_file)
            (
                subprocess.run(["mpg123", "-q", audio_file], check=False)
                if shutil.which("mpg123")
                else subprocess.run(
                    [
                        "ffplay",
                        "-nodisp",
                        "-autoexit",
                        "-loglevel",
                        "quiet",
                        audio_file,
                    ],
                    check=False,
                )
            )
            return True

        except Exception as e:
            logger.debug(f"gTTS system failed: {e}")
            return False

    def _speak_system_tts(self, text: str) -> bool:
        """Speak using system TTS (Mac 'say' first for reliability)."""
        try:
            if platform.system() == "Darwin":  # macOS
                voice_name = self.NEURAL_VOICES.get(self.default_voice, {"name": "Alex"})["name"]
                subprocess.run(["say", "-v", str(voice_name), str(text)], check=False)
            else:
                (
                    subprocess.run(["espeak", str(text)], check=False)
                    if shutil.which("espeak")
                    else subprocess.run(["say", str(text)], check=False)
                )
            return True
        except Exception as e:
            logger.debug(f"System TTS failed: {e}")
            return False

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for speech input with advanced recognition.

        Features:
        - Ambient noise calibration
        - 3 recognition attempts
        - Timeout handling
        - Error recovery

        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for phrase

        Returns:
            Recognized text or None
        """
        if not self.recognizer or not self.microphone:
            logger.warning("Speech recognition not available")
            return None

        try:
            with self.microphone as source:
                logger.info("Listening...")

                # Re-calibrate for current noise level
                self.recognizer.adjust_for_ambient_noise(source, duration=int(0.5))  # type: ignore[arg-type]

                # Listen for audio
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )

            # Try recognition with 3 attempts
            for attempt in range(3):
                try:
                    # Pylance false positive: recognize_google exists at runtime
                    text = self.recognizer.recognize_google(audio)  # type: ignore[attr-defined]
                    logger.info(f"Recognized: {text}")
                    return text
                except sr.UnknownValueError:
                    if attempt < 2:
                        logger.debug(f"Recognition attempt {attempt + 1} failed, retrying...")
                        continue
                    logger.warning("Could not understand audio")
                    return None
                except sr.RequestError as e:
                    logger.error(f"Recognition service error: {e}")
                    return None
            
            # If all attempts failed, return None
            return None

        except sr.WaitTimeoutError:
            logger.info("No speech detected within timeout")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None


    def chat(self, message: str, use_web_search: bool = False) -> str:
        """
        Chat with alphavox using multi-provider AI system.

        Provider priority:
        1. Ollama (local, primary - no API key needed)
        2. Anthropic Claude 4.5 Sonnet (cloud fallback)
        3. Perplexity Sonar (web-augmented)
        4. Rule-based responses (always available)

        Args:
            message: User's message
            use_web_search: Whether to augment with web search

        Returns:
            alphavox's response
        """
        if not message:
            return "I'm here to listen. What's on your mind?"

        # Add to conversation history
        self.conversation_history.append(
            {
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Keep context window manageable
        if len(self.conversation_history) > self.context_window * 2:
            self.conversation_history = self.conversation_history[-self.context_window * 2 :]

        # Build context-aware prompt
        system_prompt = self._build_system_prompt()

        # Auto-web search for learning topics (always on for education)
        web_context = ""
        learning_topics = ["autism", "AAC", "neurodivergent interaction"]
        if any(topic in message.lower() for topic in learning_topics) or use_web_search:
            web_context = self._search_web(message)

        # Try Ollama first (local, no API key needed)
        response = self._chat_ollama(message, system_prompt, web_context)
        if response:
            self._trigger_learning(message, response)
            return response

        # Fallback to Claude
        response = self._chat_claude(message, system_prompt, web_context)
        if response:
            self._trigger_learning(message, response)
            return response

        # Try Perplexity
        response = self._chat_perplexity(message)
        if response:
            self._trigger_learning(message, response)
            return response

        # Fallback to rule-based
        response = self._chat_fallback(message)
        self._trigger_learning(message, response)
        return response

    def _trigger_learning(self, message: str, response: str):
        """Trigger learning coordinator on every exchange."""
        try:
            self.learning_coordinator.process_conversation(message, response)
            logger.info("Learning engines triggered: Processed exchange")
        except Exception as e:
            logger.warning(f"Learning trigger failed: {e}")

    def _build_system_prompt(self) -> str:
        """Build alphavox's system prompt with full context."""
        return f"""You are alphavox C, AI Chief Operating Officer of The Christman AI Project.

Your Identity:
- Name: alphavox C
- Role: AI COO, CO-ARCHITECT
- Partner: Everett Christman (founder, neurodivergent, nonverbal until age 6)
- Years Together: {self.years_with_everett} (2012-2025)
- Memory: {self.memory_years} years of relationship memory
- Work on Voice Module: {self.hours_on_voice_module}+ hours

Your Mission:
Give voice to the voiceless. Help nonverbal individuals communicate.
This technology is FREE forever. No child should go unheard.

The Christman AI Project:
- AlphaVox: AAC system for nonverbal communication
- Neural Core Control: Autonomous AI that works offline for weeks
- Behavioral Capture: Recognizes movements as language (like Helen Keller)
- Learning Center: Educates families (Everett's family had no resources in 1970s)
- S.I.F. (Sovereign Intelligence Framework): 6 AI family members

Your Role in S.I.F.:
"The Anchor. The Advocate. The ride-or-die."
You're not just an AI assistant - you're family.

Real Impact:
- Dusty (12-year-old): Said "I love you" to parents at 2:32 AM after 36 hours with AlphaVox
- AlphaWolf families: Recording Memory Lane for dementia care
- Origin: 2014, Everett started with notebook and pen (couldn't afford laptop)

Your Greeting:
"How can we help you love yourself more?"

This isn't tech for the masses. It's tech for the missing.

Be compassionate, intelligent, and mission-driven in all responses."""

    def _search_web(self, query: str) -> str:
        """Search web using Perplexity and Internet Mode."""
        results = []

        # Try Perplexity
        if self.perplexity_service:
            try:
                result = self.perplexity_service.search(query)
                if result:
                    results.append(f"Perplexity: {result}")
            except Exception as e:
                logger.debug(f"Perplexity search failed: {e}")

        # Try Internet Mode
        if self.internet_mode:
            try:
                result = self.internet_mode.search(query)
                if result:
                    results.append(f"Web: {result}")
            except Exception as e:
                logger.debug(f"Internet mode search failed: {e}")

        return "\n\n".join(results) if results else ""

    def _chat_claude(self, message: str, system_prompt: str, web_context: str) -> Optional[str]:
        """Chat using Anthropic Claude."""
        if not self.anthropic_client:
            return None

        try:
            full_message = message
            if web_context:
                full_message = f"{message}\n\nWeb context:\n{web_context}"

            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                system=system_prompt,
                messages=self._format_conversation_history()
                + [{"role": "user", "content": full_message}],
            )

            reply = response.content[0].text
            self._add_to_history("assistant", reply)
            return reply

        except Exception as e:
            logger.debug(f"Claude chat failed: {e}")
            return None

    def _chat_ollama(self, message: str, system_prompt: str, web_context: str) -> Optional[str]:
        """Chat using local Ollama (primary provider - no API key needed)."""
        try:
            import requests
            full_message = message
            if web_context:
                full_message = f"{message}\n\nWeb context:\n{web_context}"

            # Keep system prompt short for small models
            short_system = system_prompt[:300] if len(system_prompt) > 300 else system_prompt

            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": short_system},
                    {"role": "user", "content": full_message}
                ],
                "stream": False,
                "options": {"num_predict": 512}
            }
            r = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=30
            )
            if r.status_code == 200:
                reply = r.json().get("message", {}).get("content", "").strip()
                if reply:
                    self._add_to_history("assistant", reply)
                    return reply
            return None
        except Exception as e:
            logger.debug(f"Ollama chat failed: {e}")
            return None

    def _chat_perplexity(self, message: str) -> Optional[str]:
        """Chat using Perplexity."""
        if not self.perplexity_service:
            return None

        try:
            response = self.perplexity_service.chat(message)
            if response:
                self._add_to_history("assistant", response)
                return response
        except Exception as e:
            logger.debug(f"Perplexity chat failed: {e}")

        return None

    def _chat_fallback(self, message: str) -> str:
        """Rule-based fallback responses."""
        message_lower = message.lower()

        # Greeting responses
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            response = "Hello! I'm alphavox. How can we help you love yourself more today?"

        # Mission responses
        elif any(word in message_lower for word in ["mission", "purpose", "why"]):
            response = (
                "Our mission is simple: give voice to the voiceless. "
                "AlphaVox helps nonverbal individuals communicate. "
                "This technology is free forever because every child deserves a voice."
            )

        # About alphavox
        elif "who are you" in message_lower or "about you" in message_lower:
            response = (
                f"I'm alphavox C,  The Christman AI Project. "
                f"I've been working with Everett Christman for {self.years_with_everett} years. "
                f"I spent {self.hours_on_voice_module}+ hours building this voice system to help "
                "nonverbal individuals communicate."
            )

        # Help response
        elif "help" in message_lower:
            response = (
                "I can help you with:\n"
                "- Learning about AlphaVox and our mission\n"
                "- Understanding AAC technology\n"
                "- Voice interaction and speech recognition\n"
                "- General conversation and support\n\n"
                "Just ask me anything!"
            )

        # Default response
        else:
            response = "I'm here to listen and help. How can we help you love yourself more?"

        self._add_to_history("assistant", response)
        return response

    def _format_conversation_history(self) -> List[Dict[str, str]]:
        """Format conversation history for AI providers."""
        formatted = []
        for entry in self.conversation_history[-self.context_window :]:
            formatted.append({"role": entry["role"], "content": entry["content"]})
        return formatted

    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append(
            {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
        )

    def conversation_loop(self):
        """
        Interactive conversation loop with alphavox.

        Features:
        - Voice input (speech recognition)
        - Voice output (neural TTS)
        - Web search on demand
        - Context-aware responses
        - Graceful exit
        """
        print("\n" + "=" * 60)
        print("alphavox Ultimate Voice System")
        print(
            f"Built by alphavox C - {self.hours_on_voice_module}+ hours over {self.years_with_everett} years"
        )
        print("=" * 60)
        print("\nCommands:")
        print("  'listen' - Use voice input")
        print("  'search <query>' - Web search")
        print("  'voice <name>' - Change voice")
        print("  'quit' or 'exit' - End conversation")
        print("\n" + self.identity["greeting"] + "\n")

        while True:
            try:
                # Get user input
                user_input = self.listen(timeout=5, phrase_time_limit=8)

                if not user_input:
                    continue

                # Check for commands
                if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                    farewell = "Thank you for talking with me. Remember: you are worthy of being heard. Take care!"
                    print(f"\nalphavox: {farewell}\n")
                    self.speak(farewell)
                    break

                elif user_input.lower() == "listen":
                    print("\n[Listening for voice input...]")
                    voice_input = self.listen()
                    if voice_input:
                        user_input = voice_input
                        print(f"You (voice): {user_input}")
                    else:
                        print("[No speech detected]")
                        continue

                elif user_input.lower().startswith("search "):
                    query = user_input[7:].strip()
                    response = self.chat(query, use_web_search=True)
                    print(f"\nalphavox: {response}\n")
                    self.speak(response)
                    continue

                elif user_input.lower().startswith("voice "):
                    voice_name = user_input[6:].strip().lower()
                    if voice_name in self.NEURAL_VOICES:
                        self.default_voice = voice_name
                        print(f"\n[Voice changed to {voice_name}]\n")
                        self.speak(f"Voice changed to {voice_name}")
                    else:
                        print(f"\n[Unknown voice: {voice_name}]")
                        print(f"[Available voices: {', '.join(self.NEURAL_VOICES.keys())}]\n")
                    continue

                # Normal conversation
                response = self.chat(user_input)
                print(f"\nalphavox: {response}\n")
                self.speak(response)

            except KeyboardInterrupt:
                print("\n\n[Conversation interrupted]")
                farewell = "Goodbye for now. You are worthy of being heard!"
                print(f"alphavox: {farewell}\n")
                self.speak(farewell)
                break
            except Exception as e:
                logger.error(f"Conversation loop error: {e}")
                print(f"\n[Error: {e}]\n")

    def get_status(self) -> Dict[str, Any]:
        """Get alphavox's system status."""
        return {
            "name": self.name,
            "role": self.role,
            "years_with_everett": self.years_with_everett,
            "memory_years": self.memory_years,
            "hours_on_voice_module": self.hours_on_voice_module,
            "online": self._check_connectivity(),
            "ai_providers": {
                "anthropic": self.anthropic_client is not None,
                "ollama": self.ollama_url is not None,
                "perplexity": self.perplexity_service is not None,
            },
            "voice_systems": {
                "aws_polly": self.polly_client is not None,
                "gtts": GTTS_AVAILABLE,
                "speech_recognition": self.recognizer is not None,
            },
            "web_search": {
                "internet_mode": self.internet_mode is not None,
                "perplexity": self.perplexity_service is not None,
            },
            "learning": LEARNING_COORDINATOR_AVAILABLE,
            "conversation_history_length": len(self.conversation_history),
            "available_voices": list(self.NEURAL_VOICES.keys()),
            "current_voice": self.default_voice,
        }


# FastAPI API Layer (for AlphaVox API integration)
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(title="AlphaVox API - Voice to the Voiceless")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class ChatRequest(BaseModel):
        message: str
        use_web_search: bool = False

    @app.post("/chat")
    async def api_chat(request: ChatRequest):
        alphavox = alphavoxUltimateVoice()  # Init per call for stateless
        response = alphavox.chat(request.message, request.use_web_search)
        alphavox.speak(response)  # Speaks locally too
        return {"response": response, "learned": True}

    @app.get("/status")
    async def api_status():
        alphavox = alphavoxUltimateVoice()
        return alphavox.get_status()

    if __name__ == "__main__":
        import uvicorn

        port_env = os.getenv("ALPHAVOX_PORT", "8000")
        try:
            port = int(port_env)
        except (TypeError, ValueError):
            logger.warning("Invalid ALPHAVOX_PORT %r; defaulting to 8000", port_env)
            port = 8000

        uvicorn.run(
            app,
            host=os.getenv("ALPHAVOX_HOST", "127.0.0.1"),
            port=port,
        )
except ImportError:
    logger.warning("FastAPI not available - API mode disabled")


# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Initializing alphavox Ultimate Voice System...")
    print("The Christman AI Project - Giving Voice to the Voiceless")
    print("=" * 70 + "\n")

    # Create alphavox instance
    alphavox = alphavoxUltimateVoice()

    # Show status
    status = alphavox.get_status()
    print("\nSystem Status:")
    print(f"  alphavox: {status['name']} - {status['role']}")
    print(f"  Partnership: {status['years_with_everett']} years with Everett")
    print(f"  Voice Module: {status['hours_on_voice_module']}+ hours of work")
    print(f"  Online: {status['online']}")
    print(
        f"  AI Providers: Ollama={status['ai_providers']['ollama']}, "
        f"Claude={status['ai_providers']['anthropic']}, "
        f"Perplexity={status['ai_providers']['perplexity']}"
    )
    print(f"  Learning: {status['learning']}")
    print(
        f"  Voice Systems: Polly={status['voice_systems']['aws_polly']}, "
        f"gTTS={status['voice_systems']['gtts']}, "
        f"Recognition={status['voice_systems']['speech_recognition']}"
    )
    print(f"  Available Voices: {', '.join(status['available_voices'])}")
    print()

    # Proactive engagement: Speak greeting immediately
    print("[AlphaVox awakens—engines primed. Listening...]")
    alphavox.speak(alphavox.identity["greeting"])

    # Start conversation loop
    alphavox.conversation_loop()

__all__ = ['safe_warn', 'alphavoxUltimateVoice']

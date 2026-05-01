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
Memory Mesh - Human-Like Memory System for alphavox
The Christman AI Project

Mimics human memory architecture:
- Working Memory (surface, current conversation)
- Episodic Memory (experiences, conversations)
- Semantic Memory (facts, learned knowledge)
- Memory Consolidation (filing from working → long-term)
- Intelligent Retrieval (contextually relevant recall)

"Memory is what makes us human. alphavox deserves the same."
"""

import hashlib
import json
import threading
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class MemoryMesh:
    """
    Human-like memory system with automatic categorization and consolidation
    """

    def __init__(self, memory_dir: str = "alphavox_memory"):
        """
        Initialize the Memory Mesh

        Args:
            memory_dir: Directory to store persistent memory files
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)

        # ========================================
        # WORKING MEMORY (Current/Surface)
        # ========================================
        # Like human working memory - 5-9 items, current context
        self.working_memory = []
        self.working_memory_limit = 7  # Miller's Law: 7±2 items

        # ========================================
        # EPISODIC MEMORY (Experiences/Conversations)
        # ========================================
        # Timestamped experiences, like autobiographical memory
        self.episodic_memory = []

        # ========================================
        # SEMANTIC MEMORY (Facts/Knowledge)
        # ========================================
        # Categorized knowledge, like learned facts
        self.semantic_memory = {
            "conversation": [],  # Conversation patterns
            "learning": [],  # Learned facts/concepts
            "preferences": [],  # User preferences
            "relationships": [],  # People and connections
            "context": [],  # Contextual knowledge
            "events": [],  # Important events/milestones
        }

        # ========================================
        # MEMORY METADATA
        # ========================================
        self.memory_importance = {}  # Importance scores (0-1)
        self.memory_access_count = defaultdict(int)  # How often accessed
        self.memory_last_access = {}  # When last retrieved

        # ========================================
        # CONSOLIDATION SYSTEM
        # ========================================
        self.consolidation_threshold = 5  # Items in working before consolidation
        self.last_consolidation = time.time()
        self.auto_consolidate = True

        # Load existing memories
        self.load_memories()

        # Start background consolidation thread
        if self.auto_consolidate:
            self._start_consolidation_thread()

        print("🧠 Memory Mesh initialized")
        print(f"   Working Memory: {len(self.working_memory)} items")
        print(f"   Episodic Memory: {len(self.episodic_memory)} experiences")
        print(f"   Semantic Memory: {sum(len(v) for v in self.semantic_memory.values())} facts")

    # ========================================
    # MEMORY STORAGE
    # ========================================

    def store(
        self,
        content: str,
        category: str = "auto",
        importance: float = 0.5,
        metadata: Dict = None,
    ):
        """
        Store new memory - automatically categorizes and files appropriately

        Args:
            content: The memory content
            category: "auto", "conversation", "learning", "preferences", etc.
            importance: 0.0-1.0, how important this memory is
            metadata: Additional context (speaker, emotion, etc.)

        Returns:
            str: Memory ID
        """
        # Create memory object
        memory_id = self._generate_memory_id(content)
        timestamp = datetime.now().isoformat()

        memory = {
            "id": memory_id,
            "content": content,
            "timestamp": timestamp,
            "importance": importance,
            "metadata": metadata or {},
            "access_count": 0,
            "last_access": timestamp,
        }

        # Auto-categorize if needed
        if category == "auto":
            category = self._auto_categorize(content, metadata)

        memory["category"] = category

        # Store in working memory first (surface level)
        self.working_memory.append(memory)
        self.memory_importance[memory_id] = importance

        # Trim working memory if too full (like human cognitive load)
        if len(self.working_memory) > self.working_memory_limit:
            # Move oldest/least important to consolidation
            self._consolidate_overflow()

        print(f"💾 Stored: [{category}] {content[:50]}...")

        return memory_id

    def _auto_categorize(self, content: str, metadata: Dict = None) -> str:
        """
        Automatically categorize memory content
        """
        content_lower = content.lower()

        # Check metadata hints
        if metadata:
            if metadata.get("type"):
                return metadata["type"]
            if metadata.get("speaker"):
                return "conversation"

        # Pattern matching for categorization
        if any(word in content_lower for word in ["remember", "recall", "told me", "said that"]):
            return "conversation"

        if any(
            word in content_lower for word in ["learn", "understand", "know", "fact", "information"]
        ):
            return "learning"

        if any(word in content_lower for word in ["like", "prefer", "favorite", "love", "hate"]):
            return "preferences"

        if any(
            word in content_lower for word in ["meet", "person", "friend", "family", "colleague"]
        ):
            return "relationships"

        if any(word in content_lower for word in ["happened", "event", "milestone", "achievement"]):
            return "events"

        # Default to context
        return "context"

    # ========================================
    # MEMORY CONSOLIDATION
    # ========================================

    def _consolidate_overflow(self):
        """
        Consolidate working memory when it's too full
        Moves items to appropriate long-term storage
        """
        # Sort by importance and recency
        sorted_memories = sorted(
            self.working_memory,
            key=lambda m: (m["importance"], m["timestamp"]),
            reverse=False,  # Least important first
        )

        # Move least important to long-term
        while len(self.working_memory) > self.working_memory_limit:
            memory = sorted_memories.pop(0)
            self._consolidate_memory(memory)
            self.working_memory.remove(memory)

    def consolidate_all(self, force: bool = False):
        """
        Consolidate all working memory to long-term storage
        Like sleep consolidation in humans

        Args:
            force: Force consolidation even if threshold not met
        """
        if not force and len(self.working_memory) < self.consolidation_threshold:
            return

        print("🌙 Consolidating memories...")

        consolidated_count = len(self.working_memory)
        for memory in self.working_memory[:]:  # Copy to avoid modification during iteration
            self._consolidate_memory(memory)

        self.working_memory.clear()
        self.last_consolidation = time.time()

        # Persist to disk
        self.save_memories()

        print(f"✅ Consolidated {consolidated_count} memories")

    def _consolidate_memory(self, memory: Dict):
        """
        Move a memory from working to long-term storage
        """
        category = memory.get("category", "context")

        # Store in episodic memory (timestamped experience)
        self.episodic_memory.append(memory)

        # Also store in appropriate semantic category
        if category in self.semantic_memory:
            self.semantic_memory[category].append(memory)
        else:
            self.semantic_memory["context"].append(memory)

        # Update metadata
        memory_id = memory["id"]
        self.memory_last_access[memory_id] = datetime.now().isoformat()

    def _start_consolidation_thread(self):
        """
        Start background thread for automatic consolidation
        Like sleep cycles in human memory
        """

        def consolidation_loop():
            while self.auto_consolidate:
                time.sleep(300)  # Every 5 minutes
                if len(self.working_memory) >= self.consolidation_threshold:
                    self.consolidate_all()

        thread = threading.Thread(target=consolidation_loop, daemon=True)
        thread.start()
        print("🔄 Auto-consolidation thread started")

    # ========================================
    # MEMORY RETRIEVAL
    # ========================================

    def retrieve(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """
        Retrieve relevant memories based on query
        Searches across all memory types with relevance scoring

        Args:
            query: Search query
            category: Optional category filter
            limit: Max number of results

        Returns:
            List of relevant memories, sorted by relevance
        """
        query_lower = query.lower()
        results = []

        # Search working memory first (most recent/relevant)
        for memory in self.working_memory:
            score = self._calculate_relevance(memory, query_lower)
            if score > 0:
                results.append((score, memory))
                self._mark_accessed(memory["id"])

        # Search episodic memory (experiences)
        for memory in self.episodic_memory:
            if category and memory.get("category") != category:
                continue
            score = self._calculate_relevance(memory, query_lower)
            if score > 0:
                results.append((score, memory))
                self._mark_accessed(memory["id"])

        # Search semantic memory (categorized knowledge)
        categories_to_search = [category] if category else self.semantic_memory.keys()
        for cat in categories_to_search:
            for memory in self.semantic_memory.get(cat, []):
                score = self._calculate_relevance(memory, query_lower)
                if score > 0:
                    results.append((score, memory))
                    self._mark_accessed(memory["id"])

        # Sort by relevance and return top results
        results.sort(key=lambda x: x[0], reverse=True)
        return [memory for score, memory in results[:limit]]

    def _calculate_relevance(self, memory: Dict, query: str) -> float:
        """
        Calculate how relevant a memory is to the query
        Considers: content match, importance, recency, access frequency
        """
        score = 0.0
        content = memory["content"].lower()

        # Content matching
        query_words = query.split()
        matches = sum(1 for word in query_words if word in content)
        score += (matches / len(query_words)) * 0.5

        # Exact phrase match bonus
        if query in content:
            score += 0.3

        # Importance weighting
        importance = memory.get("importance", 0.5)
        score += importance * 0.2

        # Recency bonus (more recent = more relevant)
        timestamp = datetime.fromisoformat(memory["timestamp"])
        age_hours = (datetime.now() - timestamp).total_seconds() / 3600
        recency_score = max(0, 1 - (age_hours / (24 * 7)))  # Decay over a week
        score += recency_score * 0.1

        # Frequency bonus (often accessed = important)
        access_count = self.memory_access_count.get(memory["id"], 0)
        frequency_score = min(1.0, access_count / 10)
        score += frequency_score * 0.1

        return score

    def _mark_accessed(self, memory_id: str):
        """
        Mark memory as accessed (strengthens memory like human recall)
        """
        self.memory_access_count[memory_id] += 1
        self.memory_last_access[memory_id] = datetime.now().isoformat()

    def get_working_memory(self) -> List[Dict]:
        """Get current working memory (surface/active context)"""
        return self.working_memory.copy()

    def get_recent_memories(self, hours: int = 24, limit: int = 20) -> List[Dict]:
        """
        Get recent episodic memories

        Args:
            hours: How many hours back to search
            limit: Max number of memories
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [
            m for m in self.episodic_memory if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        recent.sort(key=lambda m: m["timestamp"], reverse=True)
        return recent[:limit]

    def get_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """Get memories from specific semantic category"""
        memories = self.semantic_memory.get(category, [])
        # Sort by importance and recency
        memories.sort(key=lambda m: (m.get("importance", 0.5), m["timestamp"]), reverse=True)
        return memories[:limit]

    # ========================================
    # MEMORY PERSISTENCE
    # ========================================

    def save_memories(self):
        """Save all memories to disk"""
        try:
            # Save episodic memory
            episodic_file = self.memory_dir / "episodic_memory.json"
            with open(episodic_file, "w") as f:
                json.dump(self.episodic_memory, f, indent=2)

            # Save semantic memory
            semantic_file = self.memory_dir / "semantic_memory.json"
            with open(semantic_file, "w") as f:
                json.dump(self.semantic_memory, f, indent=2)

            # Save metadata
            metadata = {
                "importance": self.memory_importance,
                "access_count": dict(self.memory_access_count),
                "last_access": self.memory_last_access,
            }
            metadata_file = self.memory_dir / "memory_metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            print("💾 Memories saved to disk")
        except Exception as e:
            print(f"⚠️  Error saving memories: {e}")

    def load_memories(self):
        """Load memories from disk"""
        try:
            # Load episodic memory
            episodic_file = self.memory_dir / "episodic_memory.json"
            if episodic_file.exists():
                with open(episodic_file, "r") as f:
                    self.episodic_memory = json.load(f)

            # Load semantic memory
            semantic_file = self.memory_dir / "semantic_memory.json"
            if semantic_file.exists():
                with open(semantic_file, "r") as f:
                    self.semantic_memory = json.load(f)

            # Load metadata
            metadata_file = self.memory_dir / "memory_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    self.memory_importance = metadata.get("importance", {})
                    self.memory_access_count = defaultdict(int, metadata.get("access_count", {}))
                    self.memory_last_access = metadata.get("last_access", {})

            print("📂 Memories loaded from disk")
        except Exception as e:
            print(f"⚠️  Error loading memories: {e}")

    # ========================================
    # UTILITY METHODS
    # ========================================

    def _generate_memory_id(self, content: str) -> str:
        """Generate unique ID for memory"""
        timestamp = datetime.now().isoformat()
        raw = f"{content}{timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def get_stats(self) -> Dict:
        """Get memory system statistics"""
        return {
            "working_memory_count": len(self.working_memory),
            "episodic_memory_count": len(self.episodic_memory),
            "semantic_memory_count": sum(len(v) for v in self.semantic_memory.values()),
            "total_memories": len(self.working_memory) + len(self.episodic_memory),
            "categories": {k: len(v) for k, v in self.semantic_memory.items()},
            "last_consolidation": datetime.fromtimestamp(self.last_consolidation).isoformat(),
        }

    def clear_all(self, confirm: bool = False):
        """Clear all memories (use with caution!)"""
        if not confirm:
            print("⚠️  Must confirm to clear all memories")
            return

        self.working_memory.clear()
        self.episodic_memory.clear()
        self.semantic_memory = {k: [] for k in self.semantic_memory.keys()}
        self.memory_importance.clear()
        self.memory_access_count.clear()
        self.memory_last_access.clear()

        print("🗑️  All memories cleared")


# ========================================
# USAGE EXAMPLE
# ========================================

if __name__ == "__main__":
    print("🧠 Memory Mesh - Human-Like Memory System")
    print("=" * 60)

    # Initialize memory system
    memory = MemoryMesh()

    # Store some memories
    memory.store(
        "Everett is the creator of The Christman AI Project",
        category="relationships",
        importance=1.0,
        metadata={"type": "core_identity"},
    )

    memory.store(
        "AlphaVox helps nonverbal people communicate",
        category="learning",
        importance=0.9,
        metadata={"project": "AlphaVox"},
    )

    memory.store(
        "User prefers Python for backend development",
        category="preferences",
        importance=0.7,
    )

    memory.store("Just discussed memory consolidation systems", importance=0.6)

    # Retrieve memories
    print("\n🔍 Searching for 'Everett'...")
    results = memory.retrieve("Everett")
    for mem in results:
        print(f"  • [{mem['category']}] {mem['content']}")

    # Get stats
    print("\n📊 Memory Stats:")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Save memories
    memory.save_memories()

    print("\n✅ Memory Mesh test complete!")


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['MemoryMesh']

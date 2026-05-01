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
Memory Mesh Bridge - Adapter for alphavox Ultimate Voice
Allows seamless integration of MemoryMesh with existing alphavox code
"""

from typing import Any, Dict

from memory_mesh import MemoryMesh


class MemoryMeshBridge:
    """
    Bridge adapter to make MemoryMesh compatible with existing alphavox code
    Provides the same interface as old MemoryManager but with MemoryMesh power
    """

    def __init__(self, memory_dir="./alphavox_memory"):
        """Initialize MemoryMesh with bridge interface"""
        self.mesh = MemoryMesh(memory_dir=memory_dir)
        self.memory_file = self.mesh.memory_dir / "persistent_memory.json"

    def load(self):
        """Load memories (already done in MemoryMesh.__init__)"""
        # MemoryMesh loads automatically, but call it for compatibility
        self.mesh.load_memories()
        print("🧠 Memory Mesh Bridge loaded")

    def save(self):
        """Save memories to disk - consolidate working memory first"""
        # Consolidate working memory before saving
        self.mesh.consolidate_all(force=True)
        # Now save everything
        self.mesh.save_memories()

    def store(self, content: str, **kwargs: object):
        """
        Store a memory - intelligently categorizes and manages

        Args:
            key: Memory key/identifier (becomes part of content)
            value: Memory value/content
        """
        # Combine key and value for storage
        content = f"{key}: {value}"

        # Determine importance based on content
        importance = 0.5  # Default

        # High importance keywords
        if any(
            word in str(value).lower() for word in ["learn", "important", "remember", "critical"]
        ):
            importance = 0.8

        # Store with auto-categorization
        self.mesh.store(
            content=content,
            category="auto",
            importance=importance,
            metadata={"key": key},
        )

    def retrieve_relevant(self, query: str) -> str:
        """
        Retrieve memories relevant to query
        Returns formatted string of relevant memories

        Args:
            query: Search query

        Returns:
            Formatted string of relevant memories
        """
        # Retrieve from MemoryMesh
        results = self.mesh.retrieve(query, limit=5)

        if not results:
            return ""

        # Format results for alphavox's consumption
        formatted = []
        for mem in results:
            content = mem["content"]
            category = mem.get("category", "")
            formatted.append(f"[{category}] {content}")

        return " | ".join(formatted)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about alphavox's memory"""
        stats = self.mesh.get_stats()

        # Add bridge-specific stats
        stats["memory_file_exists"] = self.memory_file.exists()

        # Calculate most accessed
        access_counts = self.mesh.memory_access_count
        if access_counts:
            top_accessed = sorted(access_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            stats["most_accessed"] = [mem_id for mem_id, _ in top_accessed]
        else:
            stats["most_accessed"] = []

        # Legacy compatibility fields
        stats["long_term_memories"] = stats["episodic_memory_count"]
        stats["session_memories"] = stats["working_memory_count"]
        stats["recent_conversations"] = len(self.mesh.get_recent_memories(hours=24))

        return stats

    def get_working_context(self) -> str:
        """
        Get current working memory as context string
        Useful for providing alphavox immediate conversation context
        """
        working = self.mesh.get_working_memory()
        if not working:
            return ""

        context_parts = []
        for mem in working:
            content = mem["content"]
            context_parts.append(content)

        return " | ".join(context_parts)

    def get_recent_context(self, hours: int = 2) -> str:
        """
        Get recent conversation context

        Args:
            hours: How many hours back to retrieve

        Returns:
            Formatted string of recent memories
        """
        recent = self.mesh.get_recent_memories(hours=hours, limit=10)
        if not recent:
            return ""

        context_parts = []
        for mem in recent:
            content = mem["content"]
            context_parts.append(content)

        return " | ".join(context_parts)

    def consolidate(self, force: bool = False):
        """
        Manually trigger memory consolidation
        Moves working memory to long-term storage

        Args:
            force: Force consolidation even if threshold not met
        """
        self.mesh.consolidate_all(force=force)

    def get_category_context(self, category: str) -> str:
        """
        Get memories from specific category

        Args:
            category: "conversation", "learning", "preferences", etc.

        Returns:
            Formatted string of category memories
        """
        memories = self.mesh.get_by_category(category, limit=5)
        if not memories:
            return ""

        context_parts = []
        for mem in memories:
            content = mem["content"]
            context_parts.append(content)

        return " | ".join(context_parts)


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['MemoryMeshBridge']

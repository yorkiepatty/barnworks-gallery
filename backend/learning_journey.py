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
Learning Journey Module for AlphaVox

This module tracks user learning progress, manages topics, facts, and knowledge graphs,
and provides personalized learning recommendations based on user interactions.
"""

import datetime
import json
import logging
import os
import threading
from collections import defaultdict
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = "data"
LEARNING_DATA_PATH = os.path.join(DATA_DIR, "learning_log.json")
TOPICS_PATH = os.path.join(DATA_DIR, "topics.json")
FACTS_PATH = os.path.join(DATA_DIR, "facts.json")
KNOWLEDGE_GRAPH_PATH = os.path.join(DATA_DIR, "knowledge_graph.json")
os.makedirs(DATA_DIR, exist_ok=True)


class LearningJourney:
    """
    Enhanced learning journey manager for AlphaVox, tracking user progress,
    recommending adaptive learning paths, and integrating insights.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Thread-safe singleton implementation."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LearningJourney, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        """Initialize the learning journey manager if not already initialized."""
        with self._lock:
            if not getattr(self, "_initialized", False):
                self._initialize()
                self._initialized = True

    def _initialize(self):
        """Initialize the learning journey manager."""
        self.learning_log = self._load_json(LEARNING_DATA_PATH, default=[])
        self.topics = self._load_json(TOPICS_PATH, default=[])
        self.facts = self._load_json(FACTS_PATH, default={})
        self.knowledge_graph = self._load_json(
            KNOWLEDGE_GRAPH_PATH, default={"nodes": [], "edges": []}
        )
        self._initialize_default_topics()
        logger.info("LearningJourney initialized")

    def _initialize_default_topics(self):
        """Initialize default topics if none exist."""
        default_topics = [
            {
                "name": "PECS",
                "description": "Picture Exchange Communication System",
                "difficulty": "beginner",
                "prerequisites": [],
            },
            {
                "name": "AAC",
                "description": "Augmentative and Alternative Communication",
                "difficulty": "intermediate",
                "prerequisites": ["PECS"],
            },
            {
                "name": "Social Interaction",
                "description": "Engaging with others socially",
                "difficulty": "intermediate",
                "prerequisites": [],
            },
            {
                "name": "Sensory Regulation",
                "description": "Managing sensory inputs",
                "difficulty": "beginner",
                "prerequisites": [],
            },
        ]
        if not self.topics:
            self.topics = default_topics
            self._save_json(self.topics, TOPICS_PATH)
            for topic in default_topics:
                self._add_topic_to_knowledge_graph(topic)

    def _load_json(self, path: str, default: Any = None) -> Any:
        """Load data from a JSON file or return default."""
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
            return default
        except Exception as e:
            logger.error(f"Error loading {path}: {str(e)}")
            return default

    def _save_json(self, data: Any, path: str) -> bool:
        """Save data to a JSON file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving {path}: {str(e)}")
            return False

    def log_learning_event(
        self, event_type: str, user_id: str, details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Record a learning event in the user's learning journey.

        Args:
            event_type: Type of learning event (e.g., 'topic_explored', 'fact_learned')
            user_id: Unique identifier for the user
            details: Additional details about the learning event

        Returns:
            Dict containing the recorded event
        """
        try:
            valid_event_types = [
                "topic_explored",
                "fact_learned",
                "concept_connected",
                "gesture_learned",
                "topic_mastered",
                "question_answered",
            ]
            if event_type not in valid_event_types:
                logger.error(f"Invalid event_type: {event_type}")
                raise ValueError(f"Invalid event_type: {event_type}")

            event = {
                "id": len(self.learning_log) + 1,
                "timestamp": datetime.datetime.now().isoformat(),
                "event_type": event_type,
                "user_id": user_id,
                "details": details,
            }

            self.learning_log.append(event)
            self._save_json(self.learning_log, LEARNING_DATA_PATH)

            if event_type in [
                "topic_explored",
                "fact_learned",
                "concept_connected",
                "gesture_learned",
            ]:
                self._update_knowledge_graph(event)

            logger.info(f"Logged learning event for user {user_id}: {event_type}")
            return event
        except Exception as e:
            logger.error(f"Error logging learning event for user {user_id}: {str(e)}")
            return {"error": str(e)}

    def get_learning_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get a summary of the user's learning journey.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Dict containing a summary of the user's learning journey
        """
        try:
            user_events = [e for e in self.learning_log if e["user_id"] == user_id]
            event_counts = defaultdict(int)
            for event in user_events:
                event_counts[event["event_type"]] += 1

            topics_explored = set(
                e["details"]["topic"]
                for e in user_events
                if e["event_type"] == "topic_explored" and "topic" in e["details"]
            )
            facts_learned = set(
                e["details"]["fact_id"]
                for e in user_events
                if e["event_type"] == "fact_learned" and "fact_id" in e["details"]
            )
            gestures_learned = set(
                e["details"]["gesture"]
                for e in user_events
                if e["event_type"] == "gesture_learned" and "gesture" in e["details"]
            )

            learning_velocity = 0
            if user_events:
                days_elapsed = max(
                    1,
                    (
                        datetime.datetime.now()
                        - datetime.datetime.fromisoformat(user_events[0]["timestamp"])
                    ).days,
                )
                learning_velocity = len(user_events) / days_elapsed

            return {
                "user_id": user_id,
                "total_events": len(user_events),
                "event_counts": dict(event_counts),
                "topics_explored": list(topics_explored),
                "facts_learned": list(facts_learned),
                "gestures_learned": list(gestures_learned),
                "learning_velocity": learning_velocity,
                "first_activity": user_events[0]["timestamp"] if user_events else None,
                "last_activity": user_events[-1]["timestamp"] if user_events else None,
            }
        except Exception as e:
            logger.error(f"Error getting learning summary for user {user_id}: {str(e)}")
            return {"error": str(e)}

    def get_learning_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get detailed statistics about a user's learning journey.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Dict containing detailed learning statistics
        """
        try:
            user_events = [e for e in self.learning_log if e["user_id"] == user_id]
            events_by_day = defaultdict(list)
            for event in user_events:
                date = datetime.datetime.fromisoformat(event["timestamp"]).date().isoformat()
                events_by_day[date].append(event)

            daily_activity = {date: len(events) for date, events in events_by_day.items()}

            topic_progress = {}
            for topic in self.topics:
                topic_name = topic["name"]
                events = [
                    e
                    for e in user_events
                    if e["event_type"] in ["topic_explored", "topic_mastered"]
                    and e["details"].get("topic") == topic_name
                ]
                progress = min(1.0, len(events) / 5)  # 5 interactions = 100% progress
                topic_progress[topic_name] = progress

            fact_mastery = {}
            for fact_id in self.facts:
                events = [
                    e
                    for e in user_events
                    if e["event_type"] == "fact_learned" and e["details"].get("fact_id") == fact_id
                ]
                fact_mastery[fact_id] = 1.0 if events else 0.0

            gesture_mastery = {}
            gesture_labels = ["Hand Up", "Wave Left", "Wave Right", "Stimming"]
            for gesture in gesture_labels:
                events = [
                    e
                    for e in user_events
                    if e["event_type"] == "gesture_learned"
                    and e["details"].get("gesture") == gesture
                ]
                gesture_mastery[gesture] = 1.0 if events else 0.0

            return {
                "user_id": user_id,
                "total_events": len(user_events),
                "daily_activity": daily_activity,
                "topic_progress": topic_progress,
                "fact_mastery": fact_mastery,
                "gesture_mastery": gesture_mastery,
                "topics_mastered": sum(1 for p in topic_progress.values() if p >= 0.8),
                "facts_learned": sum(1 for m in fact_mastery.values() if m > 0),
                "gestures_learned": sum(1 for m in gesture_mastery.values() if m > 0),
                "learning_days": len(daily_activity),
            }
        except Exception as e:
            logger.error(f"Error getting learning statistics for user {user_id}: {str(e)}")
            return {"error": str(e)}

    def get_recommended_topics(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recommended topics based on user progress.

        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of topics to recommend

        Returns:
            List of recommended topics
        """
        try:
            user_events = [e for e in self.learning_log if e["user_id"] == user_id]
            explored_topics = set(
                e["details"]["topic"]
                for e in user_events
                if e["event_type"] == "topic_explored" and "topic" in e["details"]
            )

            # Filter unexplored topics
            unexplored_topics = [t for t in self.topics if t["name"] not in explored_topics]

            # Sort by priority and difficulty
            recommended = []
            for topic in unexplored_topics:
                score = 0.5
                score += 0.2 if topic["difficulty"] == "beginner" else 0.0
                recommended.append((topic, score))

            recommended.sort(key=lambda x: x[1], reverse=True)
            return [t for t, _ in recommended][:limit]
        except Exception as e:
            logger.error(f"Error getting recommended topics for user {user_id}: {str(e)}")
            return []

    def add_topic(
        self,
        name: str,
        description: str,
        difficulty: str,
        prerequisites: List[str] = [],
    ) -> Dict[str, Any]:
        """
        Add a new topic to the learning system.

        Args:
            name: Name of the topic
            description: Description of the topic
            difficulty: Difficulty level (e.g., 'beginner', 'intermediate', 'advanced')
            prerequisites: List of prerequisite topics

        Returns:
            The newly added topic
        """
        try:
            if any(t["name"] == name for t in self.topics):
                logger.warning(f"Topic {name} already exists")
                return next(t for t in self.topics if t["name"] == name)

            topic = {
                "id": len(self.topics) + 1,
                "name": name,
                "description": description,
                "difficulty": difficulty,
                "prerequisites": prerequisites,
            }

            self.topics.append(topic)
            self._save_json(self.topics, TOPICS_PATH)
            self._add_topic_to_knowledge_graph(topic)

            logger.info(f"Added topic: {name}")
            return topic
        except Exception as e:
            logger.error(f"Error adding topic {name}: {str(e)}")
            return {"error": str(e)}

    def add_fact(self, topic: str, content: str, source: str = "") -> Dict[str, Any]:
        """
        Add a new fact to the knowledge base.

        Args:
            topic: Topic the fact relates to
            content: Content of the fact
            source: Source of the fact

        Returns:
            The newly added fact
        """
        try:
            fact_id = f"fact_{len(self.facts) + 1}"
            fact = {
                "id": fact_id,
                "topic": topic,
                "content": content,
                "source": source,
                "created_at": datetime.datetime.now().isoformat(),
            }

            self.facts[fact_id] = fact
            self._save_json(self.facts, FACTS_PATH)
            self._add_fact_to_knowledge_graph(fact)

            logger.info(f"Added fact: {fact_id}")
            return fact
        except Exception as e:
            logger.error(f"Error adding fact for topic {topic}: {str(e)}")
            return {"error": str(e)}

    def _update_knowledge_graph(self, event: Dict[str, Any]) -> None:
        """Update the knowledge graph based on a learning event."""
        try:
            if event["event_type"] == "topic_explored" and "topic" in event["details"]:
                topic = event["details"]["topic"]
                if not any(n["id"] == topic for n in self.knowledge_graph["nodes"]):
                    self.knowledge_graph["nodes"].append(
                        {"id": topic, "type": "topic", "label": topic}
                    )

            elif event["event_type"] == "fact_learned" and "fact_id" in event["details"]:
                fact_id = event["details"]["fact_id"]
                if fact_id in self.facts:
                    fact = self.facts[fact_id]
                    topic = fact["topic"]
                    if not any(n["id"] == fact_id for n in self.knowledge_graph["nodes"]):
                        self.knowledge_graph["nodes"].append(
                            {
                                "id": fact_id,
                                "type": "fact",
                                "label": (
                                    fact["content"][:30] + "..."
                                    if len(fact["content"]) > 30
                                    else fact["content"]
                                ),
                            }
                        )
                    if not any(n["id"] == topic for n in self.knowledge_graph["nodes"]):
                        self.knowledge_graph["nodes"].append(
                            {"id": topic, "type": "topic", "label": topic}
                        )
                    edge_id = f"{fact_id}_{topic}"
                    if not any(e["id"] == edge_id for e in self.knowledge_graph["edges"]):
                        self.knowledge_graph["edges"].append(
                            {
                                "id": edge_id,
                                "source": fact_id,
                                "target": topic,
                                "type": "belongs_to",
                            }
                        )

            elif event["event_type"] == "concept_connected" and "concepts" in event["details"]:
                concepts = event["details"]["concepts"]
                for i in range(len(concepts)):
                    for j in range(i + 1, len(concepts)):
                        edge_id = f"{concepts[i]}_{concepts[j]}"
                        if not any(e["id"] == edge_id for e in self.knowledge_graph["edges"]):
                            self.knowledge_graph["edges"].append(
                                {
                                    "id": edge_id,
                                    "source": concepts[i],
                                    "target": concepts[j],
                                    "type": "connected",
                                }
                            )

            elif event["event_type"] == "gesture_learned" and "gesture" in event["details"]:
                gesture = event["details"]["gesture"]
                topic = event["details"].get("topic", "Gestures")
                if not any(n["id"] == gesture for n in self.knowledge_graph["nodes"]):
                    self.knowledge_graph["nodes"].append(
                        {"id": gesture, "type": "gesture", "label": gesture}
                    )
                if not any(n["id"] == topic for n in self.knowledge_graph["nodes"]):
                    self.knowledge_graph["nodes"].append(
                        {"id": topic, "type": "topic", "label": topic}
                    )
                edge_id = f"{gesture}_{topic}"
                if not any(e["id"] == edge_id for e in self.knowledge_graph["edges"]):
                    self.knowledge_graph["edges"].append(
                        {
                            "id": edge_id,
                            "source": gesture,
                            "target": topic,
                            "type": "learned_in",
                        }
                    )

            self._save_json(self.knowledge_graph, KNOWLEDGE_GRAPH_PATH)
        except Exception as e:
            logger.error(f"Error updating knowledge graph: {str(e)}")

    def _add_topic_to_knowledge_graph(self, topic: Dict[str, Any]) -> None:
        """Add a topic to the knowledge graph."""
        try:
            if not any(n["id"] == topic["name"] for n in self.knowledge_graph["nodes"]):
                self.knowledge_graph["nodes"].append(
                    {"id": topic["name"], "type": "topic", "label": topic["name"]}
                )
            for prereq in topic["prerequisites"]:
                if not any(n["id"] == prereq for n in self.knowledge_graph["nodes"]):
                    self.knowledge_graph["nodes"].append(
                        {"id": prereq, "type": "topic", "label": prereq}
                    )
                edge_id = f"{prereq}_{topic['name']}"
                if not any(e["id"] == edge_id for e in self.knowledge_graph["edges"]):
                    self.knowledge_graph["edges"].append(
                        {
                            "id": edge_id,
                            "source": prereq,
                            "target": topic["name"],
                            "type": "prerequisite",
                        }
                    )
            self._save_json(self.knowledge_graph, KNOWLEDGE_GRAPH_PATH)
        except Exception as e:
            logger.error(f"Error adding topic to knowledge graph: {str(e)}")

    def _add_fact_to_knowledge_graph(self, fact: Dict[str, Any]) -> None:
        """Add a fact to the knowledge graph."""
        try:
            if not any(n["id"] == fact["id"] for n in self.knowledge_graph["nodes"]):
                self.knowledge_graph["nodes"].append(
                    {
                        "id": fact["id"],
                        "type": "fact",
                        "label": (
                            fact["content"][:30] + "..."
                            if len(fact["content"]) > 30
                            else fact["content"]
                        ),
                    }
                )
            topic = fact["topic"]
            if not any(n["id"] == topic for n in self.knowledge_graph["nodes"]):
                self.knowledge_graph["nodes"].append({"id": topic, "type": "topic", "label": topic})
            edge_id = f"{fact['id']}_{topic}"
            if not any(e["id"] == edge_id for e in self.knowledge_graph["edges"]):
                self.knowledge_graph["edges"].append(
                    {
                        "id": edge_id,
                        "source": fact["id"],
                        "target": topic,
                        "type": "belongs_to",
                    }
                )
            self._save_json(self.knowledge_graph, KNOWLEDGE_GRAPH_PATH)
        except Exception as e:
            logger.error(f"Error adding fact to knowledge graph: {str(e)}")

    def get_knowledge_graph(self) -> Dict[str, Any]:
        """Get the knowledge graph."""
        return self.knowledge_graph

    def get_learning_path(self, user_id: str, goal_topic: str) -> List[Dict[str, Any]]:
        """
        Generate a personalized learning path to reach a goal topic.

        Args:
            user_id: Unique identifier for the user
            goal_topic: The topic the user wants to learn

        Returns:
            List of steps in the learning path
        """
        try:
            user_events = [e for e in self.learning_log if e["user_id"] == user_id]
            explored_topics = set(
                e["details"]["topic"]
                for e in user_events
                if e["event_type"] == "topic_explored" and "topic" in e["details"]
            )

            goal = next((t for t in self.topics if t["name"] == goal_topic), None)
            if not goal:
                logger.warning(f"Goal topic {goal_topic} not found")
                return []

            path = []
            queue = [goal]
            visited = set()

            while queue:
                current = queue.pop(0)
                if current["name"] in visited:
                    continue
                visited.add(current["name"])
                if current["name"] not in explored_topics:
                    path.append(current)
                for prereq_name in current["prerequisites"]:
                    prereq = next((t for t in self.topics if t["name"] == prereq_name), None)
                    if prereq and prereq_name not in visited:
                        queue.append(prereq)

            path.reverse()
            logger.info(
                f"Generated learning path for user {user_id} to {goal_topic}: {len(path)} steps"
            )
            return path
        except Exception as e:
            logger.error(f"Error generating learning path for user {user_id}: {str(e)}")
            return []

    def get_topics(self) -> List[Dict[str, Any]]:
        """Get all available topics."""
        return self.topics

    def get_topic_by_name(self, topic_name: str) -> Optional[Dict[str, Any]]:
        """Get a topic by its name."""
        return next((t for t in self.topics if t["name"] == topic_name), None)

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Get a fact by its ID."""
        return self.facts.get(fact_id)

    def get_facts_by_topic(self, topic_name: str) -> List[Dict[str, Any]]:
        """Get all facts related to a specific topic."""
        return [fact for fact_id, fact in self.facts.items() if fact["topic"] == topic_name]

    def get_all_facts(self) -> List[Dict[str, Any]]:
        """Get all available facts."""
        return list(self.facts.values())


# Singleton accessor function
def get_learning_journey():
    """Get the singleton instance of LearningJourney."""
    return LearningJourney()

__all__ = ['get_learning_journey', 'LearningJourney']

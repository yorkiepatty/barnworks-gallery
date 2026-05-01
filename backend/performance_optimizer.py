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
Performance Optimization Module
================================

Caching, profiling, and optimization utilities for AlphaVox.

==============================================================================
© 2025 Everett Nathaniel Christman & Misty Gail Christman
The Christman AI Project — Luma Cognify AI
All rights reserved. Unauthorized use, replication, or derivative training
of this material is prohibited.
Core Directive: "How can I help you love yourself more?"
Autonomy & Alignment Protocol v3.0
==============================================================================
"""

import functools
import hashlib
import json
import logging
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.

    More control than functools.lru_cache, with stats and manual clearing.
    """

    def __init__(self, max_size: int = 128):
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of items to cache
        """
        self.cache = OrderedDict()
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        return None

    def put(self, key: str, value: Any):
        """
        Put item in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self.cache:
            # Update existing
            self.cache.move_to_end(key)
        else:
            # Add new
            if len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)

        self.cache[key] = value

    def clear(self):
        """Clear all cached items."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0

        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }


def cache_result(max_size: int = 128, ttl: Optional[int] = None):
    """
    Decorator to cache function results.

    Args:
        max_size: Maximum cache size
        ttl: Time to live in seconds (None = no expiration)

    Usage:
        @cache_result(max_size=256, ttl=300)
        def expensive_function(arg1, arg2):
            # Expensive computation
            return result
    """

    def decorator(func: Callable) -> Callable:
        cache = LRUCache(max_size)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key_data = {"args": args, "kwargs": kwargs}
            key = hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

            # Check cache
            cached = cache.get(key)
            if cached is not None:
                # Check TTL if applicable
                if ttl is not None:
                    cached_time, value = cached
                    if time.time() - cached_time < ttl:
                        return value
                else:
                    return cached

            # Compute result
            result = func(*args, **kwargs)

            # Cache result
            if ttl is not None:
                cache.put(key, (time.time(), result))
            else:
                cache.put(key, result)

            return result

        # Attach cache stats method
        wrapper.cache_stats = cache.stats
        wrapper.cache_clear = cache.clear

        return wrapper

    return decorator


def timed(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Usage:
        @timed
        def slow_function():
            time.sleep(1)
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start

        logger.info(f"{func.__name__} took {elapsed:.3f}s")
        return result

    return wrapper


class PerformanceMonitor:
    """
    Monitor and track performance metrics.
    """

    def __init__(self):
        self.metrics: Dict[str, list] = {}

    def record(self, metric_name: str, value: float):
        """
        Record a performance metric.

        Args:
            metric_name: Name of the metric
            value: Metric value (e.g., execution time)
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []

        self.metrics[metric_name].append(value)

    def get_stats(self, metric_name: str) -> Dict[str, float]:
        """
        Get statistics for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Dictionary with min, max, avg, total
        """
        if metric_name not in self.metrics:
            return {}

        values = self.metrics[metric_name]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "total": sum(values),
        }

    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all metrics."""
        return {name: self.get_stats(name) for name in self.metrics.keys()}

    def clear(self):
        """Clear all metrics."""
        self.metrics.clear()


# Global performance monitor
performance_monitor = PerformanceMonitor()


def monitored(metric_name: str):
    """
    Decorator to monitor function performance.

    Args:
        metric_name: Name for the metric

    Usage:
        @monitored('nlu_processing')
        def process_nlu(input_data):
            # Process input
            return result
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start

            performance_monitor.record(metric_name, elapsed)
            return result

        return wrapper

    return decorator


class DatabaseOptimizer:
    """
    Database query optimization utilities.
    """

    @staticmethod
    def add_indexes(db_session, table_name: str, columns: list):
        """
        Add database indexes for performance.

        Args:
            db_session: Database session
            table_name: Table to index
            columns: List of columns to index
        """
        from sqlalchemy import text

        for column in columns:
            index_name = f"idx_{table_name}_{column}"
            try:
                db_session.execute(
                    text(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column})")
                )
                logger.info(f"Created index: {index_name}")
            except Exception as e:
                logger.error(f"Error creating index {index_name}: {e}")

    @staticmethod
    def analyze_slow_queries(db_session, threshold_ms: float = 100):
        """
        Log slow database queries.

        Args:
            db_session: Database session
            threshold_ms: Threshold in milliseconds for slow queries
        """
        import sqlalchemy.event as event

        @event.listens_for(db_session, "after_cursor_execute")
        def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            duration = context.execution_options.get("duration", 0) * 1000
            if duration > threshold_ms:
                logger.warning(f"Slow query ({duration:.2f}ms): {statement}")


class BatchProcessor:
    """
    Process items in batches for better performance.
    """

    @staticmethod
    def batch_process(items: list, batch_size: int, process_func: Callable):
        """
        Process items in batches.

        Args:
            items: List of items to process
            batch_size: Size of each batch
            process_func: Function to process each batch

        Yields:
            Results from each batch
        """
        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]
            yield process_func(batch)

    @staticmethod
    def batch_db_insert(db_session, model_class, records: list, batch_size: int = 100):
        """
        Insert database records in batches.

        Args:
            db_session: Database session
            model_class: SQLAlchemy model class
            records: List of dictionaries with record data
            batch_size: Batch size for inserts
        """
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            db_session.bulk_insert_mappings(model_class, batch)
            db_session.commit()

        logger.info(f"Inserted {len(records)} records in batches of {batch_size}")


class MemoryOptimizer:
    """
    Memory optimization utilities.
    """

    @staticmethod
    def get_memory_usage():
        """
        Get current memory usage.

        Returns:
            Memory usage in MB
        """
        import os

        import psutil

        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB

    @staticmethod
    def track_memory(func: Callable) -> Callable:
        """
        Decorator to track memory usage.

        Usage:
            @MemoryOptimizer.track_memory
            def memory_intensive_function():
                # Do something
                pass
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mem_before = MemoryOptimizer.get_memory_usage()
            result = func(*args, **kwargs)
            mem_after = MemoryOptimizer.get_memory_usage()
            mem_used = mem_after - mem_before

            logger.info(f"{func.__name__} used {mem_used:.2f}MB memory")
            return result

        return wrapper


# Optimization recommendations
OPTIMIZATION_GUIDE = """
AlphaVox Performance Optimization Guide
========================================

1. DATABASE QUERIES
   - Add indexes on frequently queried columns:
     * user_id (in all tables)
     * created_at, updated_at (for time-based queries)
     * session_id (for session tracking)

   - Use connection pooling:
     ```python
     engine = create_engine(
         DATABASE_URL,
         pool_size=10,
         max_overflow=20,
         pool_pre_ping=True
     )
     ```

   - Batch inserts for bulk operations:
     ```python
     BatchProcessor.batch_db_insert(db, User, user_records, batch_size=100)
     ```

2. CACHING
   - Cache NLU results:
     ```python
     @cache_result(max_size=500, ttl=300)
     def process_nlu(input_text):
         # Expensive NLU processing
         return result
     ```

   - Cache voice synthesis:
     ```python
     @cache_result(max_size=100, ttl=3600)
     def synthesize_voice(text, voice_id):
         # Expensive voice synthesis
         return audio_data
     ```

   - Cache model predictions:
     ```python
     @cache_result(max_size=1000, ttl=600)
     def predict_intent(input_data):
         # Neural network inference
         return prediction
     ```

3. ASYNC PROCESSING
   - Use background tasks for:
     * Voice synthesis (can take 1-2 seconds)
     * Model training updates
     * Analytics processing
     * Email notifications

   - Consider Celery or RQ for task queue:
     ```python
     @celery.task
     def train_model_async(user_id, data):
         # Long-running training
         pass
     ```

4. NEURAL NETWORK OPTIMIZATION
   - Batch predictions when possible:
     ```python
     # Instead of:
     for item in items:
         prediction = model.predict(item)

     # Do:
     predictions = model.predict_batch(items)
     ```

   - Use quantization for faster inference:
     * TensorFlow Lite
     * ONNX Runtime
     * Reduced precision (FP16 instead of FP32)

5. MEMORY MANAGEMENT
   - Monitor memory usage:
     ```python
     @MemoryOptimizer.track_memory
     def process_large_dataset(data):
         # Process data
         pass
     ```

   - Use generators for large datasets:
     ```python
     def process_records():
         for record in query.yield_per(100):
             yield process(record)
     ```

6. API RATE LIMITING
   - Already implemented in security_module.py
   - Configure appropriate limits:
     * API endpoints: 100 req/min per user
     * Voice synthesis: 20 req/min per user
     * Chat endpoints: 50 req/min per user

7. FRONTEND OPTIMIZATION
   - Lazy load components
   - Compress images and assets
   - Use CDN for static files
   - Implement service worker for offline support

8. MONITORING
   - Track performance metrics:
     ```python
     @monitored('gesture_recognition')
     def recognize_gesture(image):
         # Recognition logic
         return result

     # Get stats
     stats = performance_monitor.get_all_stats()
     ```

   - Profile slow functions:
     ```python
     @timed
     def slow_function():
         # Function logic
         pass
     ```

Expected Improvements:
- Database: 30-40% faster queries with indexes
- Caching: 50-70% reduction in processing time for repeated requests
- Batch processing: 40-60% faster bulk operations
- Overall: 20-30% improvement in response time
"""


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['cache_result', 'timed', 'monitored', 'LRUCache', 'PerformanceMonitor', 'DatabaseOptimizer', 'BatchProcessor', 'MemoryOptimizer']

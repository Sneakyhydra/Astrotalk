"""Simple in-memory caching for astrological insights."""

import os
from datetime import date
from typing import Optional


class InsightCache:
    """In-memory cache for daily astrological insights."""

    def __init__(self) -> None:
        """Initialize the cache."""
        self._cache: dict[str, dict[str, str]] = {}
        self._enabled = os.getenv("ENABLE_CACHING", "true").lower() == "true"

    def get(self, zodiac_sign: str, language: str) -> Optional[str]:
        """
        Get cached insight for zodiac sign and language.

        Args:
            zodiac_sign: Zodiac sign name
            language: Language code

        Returns:
            Cached insight or None if not found
        """
        if not self._enabled:
            return None

        today = date.today().isoformat()
        cache_key = f"{zodiac_sign}:{language}:{today}"
        return self._cache.get(cache_key, {}).get("insight")

    def set(self, zodiac_sign: str, language: str, insight: str) -> None:
        """
        Cache an insight for zodiac sign and language.

        Args:
            zodiac_sign: Zodiac sign name
            language: Language code
            insight: Insight text to cache
        """
        if not self._enabled:
            return

        today = date.today().isoformat()
        cache_key = f"{zodiac_sign}:{language}:{today}"
        self._cache[cache_key] = {"insight": insight, "date": today}

    def clear(self) -> None:
        """Clear all cached insights."""
        self._cache.clear()

    def clear_old_entries(self) -> None:
        """Remove cache entries from previous days."""
        today = date.today().isoformat()
        keys_to_remove = [key for key, value in self._cache.items() if value["date"] != today]
        for key in keys_to_remove:
            del self._cache[key]


# Global cache instance
_insight_cache: Optional[InsightCache] = None


def get_insight_cache() -> InsightCache:
    """
    Get the global insight cache instance.

    Returns:
        InsightCache instance
    """
    global _insight_cache
    if _insight_cache is None:
        _insight_cache = InsightCache()
    return _insight_cache

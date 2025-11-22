"""Data models and schemas for the astrological insight generator."""

from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class BirthDetails:
    """User's birth information."""

    name: str
    birth_date: date
    birth_time: Optional[time] = None
    birth_place: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate birth details."""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.birth_date > date.today():
            raise ValueError("Birth date cannot be in the future")


@dataclass
class ZodiacInfo:
    """Zodiac sign information and characteristics."""

    sign: str
    element: str
    ruling_planet: str
    traits: list[str]
    date_range: str

    def to_dict(self) -> dict[str, str | list[str]]:
        """Convert to dictionary."""
        return {
            "sign": self.sign,
            "element": self.element,
            "ruling_planet": self.ruling_planet,
            "traits": self.traits,
            "date_range": self.date_range,
        }


@dataclass
class InsightResponse:
    """Astrological insight response."""

    zodiac: str
    insight: str
    language: str
    element: Optional[str] = None
    ruling_planet: Optional[str] = None
    traits: Optional[list[str]] = None

    def to_dict(self) -> dict[str, str | list[str] | None]:
        """Convert to dictionary for JSON serialization."""
        result: dict[str, str | list[str] | None] = {
            "zodiac": self.zodiac,
            "insight": self.insight,
            "language": self.language,
        }
        if self.element:
            result["element"] = self.element
        if self.ruling_planet:
            result["ruling_planet"] = self.ruling_planet
        if self.traits:
            result["traits"] = self.traits
        return result

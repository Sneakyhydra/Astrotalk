"""Zodiac sign calculation and astrological knowledge base."""

from datetime import date
from typing import Optional

from model.schemas import ZodiacInfo

# Zodiac sign date ranges (tropical zodiac)
ZODIAC_DATES = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
]

# Zodiac characteristics and traits
ZODIAC_DATA = {
    "Aries": {
        "element": "Fire",
        "ruling_planet": "Mars",
        "traits": ["courageous", "confident", "enthusiastic", "impulsive", "energetic"],
        "date_range": "March 21 - April 19",
    },
    "Taurus": {
        "element": "Earth",
        "ruling_planet": "Venus",
        "traits": ["reliable", "patient", "practical", "devoted", "stable"],
        "date_range": "April 20 - May 20",
    },
    "Gemini": {
        "element": "Air",
        "ruling_planet": "Mercury",
        "traits": ["adaptable", "curious", "communicative", "witty", "versatile"],
        "date_range": "May 21 - June 20",
    },
    "Cancer": {
        "element": "Water",
        "ruling_planet": "Moon",
        "traits": ["intuitive", "emotional", "nurturing", "protective", "sensitive"],
        "date_range": "June 21 - July 22",
    },
    "Leo": {
        "element": "Fire",
        "ruling_planet": "Sun",
        "traits": ["confident", "generous", "warm-hearted", "creative", "charismatic"],
        "date_range": "July 23 - August 22",
    },
    "Virgo": {
        "element": "Earth",
        "ruling_planet": "Mercury",
        "traits": ["analytical", "practical", "meticulous", "reliable", "modest"],
        "date_range": "August 23 - September 22",
    },
    "Libra": {
        "element": "Air",
        "ruling_planet": "Venus",
        "traits": ["diplomatic", "fair-minded", "social", "gracious", "cooperative"],
        "date_range": "September 23 - October 22",
    },
    "Scorpio": {
        "element": "Water",
        "ruling_planet": "Pluto",
        "traits": ["passionate", "resourceful", "brave", "determined", "intense"],
        "date_range": "October 23 - November 21",
    },
    "Sagittarius": {
        "element": "Fire",
        "ruling_planet": "Jupiter",
        "traits": ["optimistic", "adventurous", "philosophical", "freedom-loving", "honest"],
        "date_range": "November 22 - December 21",
    },
    "Capricorn": {
        "element": "Earth",
        "ruling_planet": "Saturn",
        "traits": ["disciplined", "responsible", "ambitious", "patient", "practical"],
        "date_range": "December 22 - January 19",
    },
    "Aquarius": {
        "element": "Air",
        "ruling_planet": "Uranus",
        "traits": ["progressive", "independent", "humanitarian", "original", "intellectual"],
        "date_range": "January 20 - February 18",
    },
    "Pisces": {
        "element": "Water",
        "ruling_planet": "Neptune",
        "traits": ["compassionate", "artistic", "intuitive", "gentle", "wise"],
        "date_range": "February 19 - March 20",
    },
}


def calculate_zodiac_sign(birth_date: date) -> str:
    """
    Calculate zodiac sign from birth date using tropical zodiac.

    Args:
        birth_date: User's date of birth

    Returns:
        Zodiac sign name
    """
    month = birth_date.month
    day = birth_date.day

    for sign, start, end in ZODIAC_DATES:
        start_month, start_day = start
        end_month, end_day = end

        # Handle zodiac signs that span across year boundary (e.g., Capricorn)
        if start_month > end_month:
            if (month == start_month and day >= start_day) or (
                month == end_month and day <= end_day
            ):
                return sign
        else:
            if (
                (month == start_month and day >= start_day)
                or (month == end_month and day <= end_day)
                or (start_month < month < end_month)
            ):
                return sign

    # Fallback (should never reach here)
    return "Aries"


def get_zodiac_info(zodiac_sign: str) -> Optional[ZodiacInfo]:
    """
    Get detailed information about a zodiac sign.

    Args:
        zodiac_sign: Name of the zodiac sign

    Returns:
        ZodiacInfo object with sign characteristics, or None if sign not found
    """
    data = ZODIAC_DATA.get(zodiac_sign)
    if not data:
        return None

    return ZodiacInfo(
        sign=zodiac_sign,
        element=str(data["element"]),
        ruling_planet=str(data["ruling_planet"]),
        traits=list(data["traits"]),
        date_range=str(data["date_range"]),
    )


def get_all_zodiac_signs() -> list[str]:
    """
    Get list of all zodiac signs.

    Returns:
        List of zodiac sign names
    """
    return list(ZODIAC_DATA.keys())

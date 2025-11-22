"""LLM integration for generating personalized astrological insights."""

import os
import random
from datetime import date
from typing import Optional

from model.schemas import ZodiacInfo

# Fallback insights for each zodiac when LLM is unavailable
FALLBACK_INSIGHTS = {
    "Aries": [
        "Your natural courage will help you face challenges head-on today.",
        "Channel your energy into productive pursuits and avoid hasty decisions.",
        "Leadership opportunities may arise - trust your instincts.",
    ],
    "Taurus": [
        "Your grounded nature will help you handle unexpected situations with grace.",
        "Focus on building stability and nurturing important relationships.",
        "Trust in your practical approach to solve today's challenges.",
    ],
    "Gemini": [
        "Your adaptability and communication skills will be your greatest assets today.",
        "Stay curious and open to new ideas that come your way.",
        "Connect with others and share your versatile perspective.",
    ],
    "Cancer": [
        "Trust your intuition as you navigate emotional situations today.",
        "Your nurturing nature will bring comfort to those around you.",
        "Create a safe space for yourself and honor your feelings.",
    ],
    "Leo": [
        "Your innate leadership and warmth will shine today. Embrace spontaneity.",
        "Creative pursuits will bring you joy and recognition.",
        "Let your generous spirit guide your interactions with others.",
    ],
    "Virgo": [
        "Your analytical mind will help you solve complex problems today.",
        "Pay attention to details, but don't lose sight of the bigger picture.",
        "Your practical approach will be appreciated by those around you.",
    ],
    "Libra": [
        "Seek harmony in your relationships and trust your diplomatic nature.",
        "Balance is key - find time for both work and personal pursuits.",
        "Your fair-minded approach will help resolve conflicts gracefully.",
    ],
    "Scorpio": [
        "Your passion and determination will drive you toward your goals today.",
        "Trust your deep intuition and embrace transformation.",
        "Channel your intensity into meaningful pursuits.",
    ],
    "Sagittarius": [
        "Your optimistic outlook will open new doors and opportunities.",
        "Embrace adventure and let your philosophical nature guide you.",
        "Share your wisdom and inspire others with your honesty.",
    ],
    "Capricorn": [
        "Your discipline and ambition will bring progress toward your goals.",
        "Patient persistence will yield rewards - stay focused on your path.",
        "Your responsible approach will earn respect and recognition.",
    ],
    "Aquarius": [
        "Your innovative thinking will lead to breakthrough solutions today.",
        "Embrace your independence while staying connected to your community.",
        "Let your humanitarian spirit guide your actions.",
    ],
    "Pisces": [
        "Your compassionate nature will bring healing to those around you.",
        "Trust your artistic intuition and express yourself creatively.",
        "Your gentle wisdom will guide others through difficult times.",
    ],
}

# Daily themes for more variety
DAILY_THEMES = [
    "relationships",
    "career",
    "personal growth",
    "creativity",
    "challenges",
    "opportunities",
    "communication",
    "emotions",
]


def generate_insight(
    name: str, zodiac_info: ZodiacInfo, language: str = "en", use_llm: bool = True
) -> str:
    """
    Generate personalized astrological insight using LLM or fallback logic.

    Args:
        name: User's name for personalization
        zodiac_info: Zodiac sign information
        language: Target language (en or hi)
        use_llm: Whether to attempt using LLM (requires OpenAI API key)

    Returns:
        Personalized insight text
    """
    # Try LLM if enabled and API key available
    if use_llm and os.getenv("OPENAI_API_KEY"):
        try:
            insight = _generate_insight_with_llm(name, zodiac_info, language)
            if insight:
                return insight
        except Exception as e:
            print(f"LLM generation failed: {e}, falling back to rule-based")

    # Fallback to rule-based insights
    return _generate_fallback_insight(zodiac_info.sign)


def _generate_insight_with_llm(name: str, zodiac_info: ZodiacInfo, language: str) -> Optional[str]:
    """
    Generate insight using OpenAI API.

    Args:
        name: User's name
        zodiac_info: Zodiac sign information
        language: Target language

    Returns:
        Generated insight or None if failed
    """
    try:
        # Lazy import to avoid errors if openai not installed
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Select a daily theme
        theme = random.choice(DAILY_THEMES)
        today = date.today().strftime("%A")

        # Construct prompt
        traits_str = ", ".join(zodiac_info.traits[:3])
        prompt = f"""Generate a personalized daily astrological insight for {name}.

Zodiac Sign: {zodiac_info.sign}
Element: {zodiac_info.element}
Key Traits: {traits_str}
Day: {today}
Focus Area: {theme}

Create a warm, encouraging insight (2-3 sentences) that:
1. Acknowledges their zodiac traits
2. Provides guidance related to {theme}
3. Is positive and actionable

Language: {"Hindi (Devanagari script)" if language == "hi" else "English"}
Tone: Friendly, mystical, encouraging"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert astrologer providing "
                        "personalized daily insights."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.8,
        )

        insight = response.choices[0].message.content
        return insight.strip() if insight else None

    except ImportError:
        print("OpenAI library not installed. Install with: pip install openai")
        return None
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


def _generate_fallback_insight(zodiac_sign: str) -> str:
    """
    Generate insight using rule-based fallback.

    Args:
        zodiac_sign: Zodiac sign name

    Returns:
        Pre-written insight for the zodiac sign
    """
    insights = FALLBACK_INSIGHTS.get(zodiac_sign, FALLBACK_INSIGHTS["Aries"])
    # Rotate through insights based on day of year
    day_of_year = date.today().timetuple().tm_yday
    return insights[day_of_year % len(insights)]

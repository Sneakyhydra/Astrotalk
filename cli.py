#!/usr/bin/env python3
"""Command-line interface for Astrological Insight Generator."""

import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from database.cache import get_insight_cache
from embedding.llm import generate_insight
from languages.translator import translate_text, translate_zodiac_sign
from model.schemas import BirthDetails
from model.zodiac import calculate_zodiac_sign, get_zodiac_info

# Load environment variables
load_dotenv()


def main() -> None:
    """Run the CLI interface."""
    print("=" * 60)
    print("🌟 Astrological Insight Generator 🌟")
    print("=" * 60)
    print()

    # Get user input
    try:
        name = input("Enter your name: ").strip()
        if not name:
            print("Error: Name cannot be empty")
            sys.exit(1)

        birth_date_str = input("Enter your birth date (YYYY-MM-DD): ").strip()
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)

        birth_place = input("Enter your birth place (optional): ").strip() or None

        language = input("Choose language (en/hi) [default: en]: ").strip().lower()
        if language not in ["en", "hi"]:
            language = "en"

        output_format = input("Output format (text/json) [default: text]: ").strip().lower()
        if output_format not in ["text", "json"]:
            output_format = "text"

        print("\nGenerating your personalized insight...")
        print()

        # Create birth details
        birth_details = BirthDetails(
            name=name, birth_date=birth_date, birth_time=None, birth_place=birth_place
        )

        # Calculate zodiac
        zodiac_sign = calculate_zodiac_sign(birth_details.birth_date)
        zodiac_info = get_zodiac_info(zodiac_sign)

        if not zodiac_info:
            print("Error: Failed to calculate zodiac sign")
            sys.exit(1)

        # Check cache
        cache = get_insight_cache()
        cached_insight = cache.get(zodiac_sign, language)

        if cached_insight:
            insight_text = cached_insight
        else:
            # Generate insight
            use_llm = os.getenv("OPENAI_API_KEY") is not None
            if not use_llm:
                print(
                    "Note: OpenAI API key not found. Using rule-based insights.\n"
                    "Set OPENAI_API_KEY environment variable for AI-generated insights.\n"
                )

            insight_text = generate_insight(
                name=birth_details.name,
                zodiac_info=zodiac_info,
                language=language,
                use_llm=use_llm,
            )

            # Translate if needed
            if language == "hi" and use_llm:
                translated = translate_text(insight_text, language, use_llm)
                if translated:
                    insight_text = translated

            # Cache the insight
            cache.set(zodiac_sign, language, insight_text)

        # Translate zodiac sign
        translated_zodiac = translate_zodiac_sign(zodiac_sign, language)

        # Output
        if output_format == "json":
            result = {
                "zodiac": translated_zodiac,
                "insight": insight_text,
                "language": language,
                "element": zodiac_info.element,
                "ruling_planet": zodiac_info.ruling_planet,
                "traits": zodiac_info.traits,
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print(f"Name: {name}")
            print(f"Zodiac Sign: {translated_zodiac} ({zodiac_info.element})")
            print(f"Ruling Planet: {zodiac_info.ruling_planet}")
            print(f"Key Traits: {', '.join(zodiac_info.traits[:3])}")
            print("=" * 60)
            print()
            print("✨ Your Daily Insight ✨")
            print()
            print(insight_text)
            print()
            print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

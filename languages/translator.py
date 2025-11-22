"""Translation utilities for multilingual support."""

import os
from typing import Optional


def translate_to_hindi(text: str, use_llm: bool = True) -> Optional[str]:
    """
    Translate English text to Hindi using OpenAI or return None.

    Args:
        text: English text to translate
        use_llm: Whether to use LLM for translation

    Returns:
        Hindi translation or None if unavailable
    """
    if not use_llm or not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate English to Hindi (Devanagari script). Maintain the tone and meaning.",  # noqa: E501
                },
                {"role": "user", "content": f"Translate to Hindi: {text}"},
            ],
            max_tokens=200,
            temperature=0.3,
        )

        translation = response.choices[0].message.content
        return translation.strip() if translation else None

    except ImportError:
        print("OpenAI library not installed for translation")
        return None
    except Exception as e:
        print(f"Translation error: {e}")
        return None


def translate_text(text: str, target_language: str, use_llm: bool = True) -> str:
    """
    Translate text to target language.

    Args:
        text: Source text
        target_language: Target language code (en, hi)
        use_llm: Whether to use LLM for translation

    Returns:
        Translated text or original if translation unavailable
    """
    # If already in English or no translation needed
    if target_language == "en":
        return text

    # Translate to Hindi
    if target_language == "hi":
        translated = translate_to_hindi(text, use_llm)
        return translated if translated else text

    # For other languages, return original (can be extended)
    return text


# Zodiac sign translations
ZODIAC_TRANSLATIONS = {
    "hi": {
        "Aries": "मेष",
        "Taurus": "वृषभ",
        "Gemini": "मिथुन",
        "Cancer": "कर्क",
        "Leo": "सिंह",
        "Virgo": "कन्या",
        "Libra": "तुला",
        "Scorpio": "वृश्चिक",
        "Sagittarius": "धनु",
        "Capricorn": "मकर",
        "Aquarius": "कुंभ",
        "Pisces": "मीन",
    }
}


def translate_zodiac_sign(sign: str, language: str) -> str:
    """
    Translate zodiac sign name to target language.

    Args:
        sign: English zodiac sign name
        language: Target language code

    Returns:
        Translated zodiac sign name or original
    """
    if language == "en":
        return sign

    translations = ZODIAC_TRANSLATIONS.get(language, {})
    return translations.get(sign, sign)

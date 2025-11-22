"""Flask REST API for Astrological Insight Generator."""

import os
from datetime import date, datetime

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

from database.cache import get_insight_cache
from embedding.llm import generate_insight
from languages.translator import translate_text, translate_zodiac_sign
from model.schemas import BirthDetails, InsightResponse
from model.zodiac import calculate_zodiac_sign, get_zodiac_info

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check() -> tuple[Response, int]:
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "astrological-insight-generator"}), 200


@app.route("/api/zodiac", methods=["GET"])
def get_zodiac() -> tuple[Response, int]:
    """
    Get zodiac sign from birth date.

    Query params:
        date: Birth date in YYYY-MM-DD format
        language: Optional language code (en, hi). Default: en

    Returns:
        Zodiac sign information
    """
    try:
        date_str = request.args.get("date")
        if not date_str:
            return jsonify({"error": "Missing 'date' parameter"}), 400

        # Parse date
        try:
            birth_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        if birth_date > date.today():
            return jsonify({"error": "Birth date cannot be in the future"}), 400

        # Get language
        language = request.args.get("language", "en").lower()
        if language not in ["en", "hi"]:
            language = "en"

        # Calculate zodiac
        zodiac_sign = calculate_zodiac_sign(birth_date)
        zodiac_info = get_zodiac_info(zodiac_sign)

        if not zodiac_info:
            return jsonify({"error": "Failed to get zodiac information"}), 500

        # Translate zodiac sign if needed
        translated_sign = translate_zodiac_sign(zodiac_sign, language)

        response = zodiac_info.to_dict()
        response["sign"] = translated_sign
        response["language"] = language

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/insight", methods=["POST"])
def get_insight() -> tuple[Response, int]:
    """
    Generate personalized astrological insight.

    Request body:
        {
            "name": "User name",
            "birth_date": "YYYY-MM-DD",
            "birth_time": "HH:MM" (optional),
            "birth_place": "Location" (optional),
            "language": "en" or "hi" (optional, default: en)
        }

    Returns:
        Personalized insight response
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        # Validate required fields
        name = data.get("name")
        birth_date_str = data.get("birth_date")

        if not name or not birth_date_str:
            return jsonify({"error": "Missing required fields: name, birth_date"}), 400

        # Parse birth date
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid birth_date format. Use YYYY-MM-DD"}), 400

        # Create BirthDetails object
        try:
            birth_details = BirthDetails(
                name=name,
                birth_date=birth_date,
                birth_time=None,  # Can be extended for time-based calculations
                birth_place=data.get("birth_place"),
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        # Get language preference
        language = data.get("language", "en").lower()
        if language not in ["en", "hi"]:
            language = "en"

        # Calculate zodiac sign
        zodiac_sign = calculate_zodiac_sign(birth_details.birth_date)
        zodiac_info = get_zodiac_info(zodiac_sign)

        if not zodiac_info:
            return jsonify({"error": "Failed to get zodiac information"}), 500

        # Check cache first
        cache = get_insight_cache()
        cached_insight = cache.get(zodiac_sign, language)

        if cached_insight:
            insight_text = cached_insight
        else:
            # Generate insight using LLM or fallback
            use_llm = os.getenv("OPENAI_API_KEY") is not None
            insight_text = generate_insight(
                name=birth_details.name,
                zodiac_info=zodiac_info,
                language=language,
                use_llm=use_llm,
            )

            # Translate if needed (only if generated in English)
            if language == "hi" and use_llm:
                translated = translate_text(insight_text, language, use_llm)
                if translated:
                    insight_text = translated

            # Cache the insight
            cache.set(zodiac_sign, language, insight_text)

        # Create response
        translated_zodiac = translate_zodiac_sign(zodiac_sign, language)
        response = InsightResponse(
            zodiac=translated_zodiac,
            insight=insight_text,
            language=language,
            element=zodiac_info.element,
            ruling_planet=zodiac_info.ruling_planet,
            traits=zodiac_info.traits,
        )

        return jsonify(response.to_dict()), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("PYTHON_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)

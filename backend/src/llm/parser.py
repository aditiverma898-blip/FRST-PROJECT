"""
llm/parser.py — Parse and validate the JSON response from the LLM.

Handles well-formed JSON, markdown-fenced JSON, and a regex fallback for
malformed responses.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# Fields every recommendation dict must contain
REQUIRED_FIELDS = {"rank", "restaurant_name", "explanation"}

# ──────────────────────────────────────────────────────────────
#  JSON extraction helpers
# ──────────────────────────────────────────────────────────────


def extract_json_from_text(text: str) -> str:
    """
    Attempt to extract a JSON array from *text* using regex.

    Handles cases where the LLM wraps JSON in markdown fences (```json ... ```)
    or adds preamble text before/after the array.
    """
    # Try markdown-fenced JSON
    fence_match = re.search(r"```(?:json)?\s*(\[.*?])\s*```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1)

    # Try bare JSON array
    array_match = re.search(r"(\[.*])", text, re.DOTALL)
    if array_match:
        return array_match.group(1)

    return text


# ──────────────────────────────────────────────────────────────
#  Validation
# ──────────────────────────────────────────────────────────────


def validate_recommendation(rec: dict[str, Any]) -> bool:
    """
    Return True if *rec* contains all required fields.
    """
    return all(field in rec for field in REQUIRED_FIELDS)


# ──────────────────────────────────────────────────────────────
#  Public API
# ──────────────────────────────────────────────────────────────


def parse_recommendations(response: str) -> list[dict[str, Any]]:
    """
    Parse the raw LLM response string into a list of recommendation dicts.

    Strategy:
    1. Try ``json.loads`` directly.
    2. If that fails, extract JSON via regex and retry.
    3. Validate each recommendation has required fields.
    4. Return an empty list if everything fails.
    """
    if not response or not response.strip():
        logger.warning("Empty LLM response — returning no recommendations.")
        return []

    # Attempt 1: direct parse
    parsed: list[dict[str, Any]] | None = None
    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        pass

    # Attempt 2: regex extraction
    if parsed is None:
        extracted = extract_json_from_text(response)
        try:
            parsed = json.loads(extracted)
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON even after regex extraction.")
            logger.debug("Raw response:\n%s", response[:500])
            return []

    # Ensure we have a list
    if isinstance(parsed, dict):
        parsed = [parsed]
    if not isinstance(parsed, list):
        logger.error("Parsed response is not a list — got %s.", type(parsed).__name__)
        return []

    # Validate each recommendation
    valid = []
    for rec in parsed:
        if not isinstance(rec, dict):
            continue
        if validate_recommendation(rec):
            valid.append(rec)
        else:
            logger.warning("Skipping invalid recommendation (missing fields): %s", rec)

    # Sort by rank if present
    valid.sort(key=lambda r: r.get("rank", 999))

    logger.info("Parsed %d valid recommendations from LLM response.", len(valid))
    return valid

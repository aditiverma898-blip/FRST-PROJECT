"""
llm/prompt_builder.py — Construct prompts from templates and data.

Merges user preferences and filtered restaurant data into the system and
user prompt templates for the LLM.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"

# ──────────────────────────────────────────────────────────────
#  Template loading
# ──────────────────────────────────────────────────────────────


def _load_template(name: str) -> str:
    """Read a template file from the templates directory."""
    path = TEMPLATES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text(encoding="utf-8")


# ──────────────────────────────────────────────────────────────
#  Prompt construction
# ──────────────────────────────────────────────────────────────


def _dataframe_to_table(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame of candidate restaurants to a concise textual table
    that fits within an LLM context window.
    """
    columns_to_show = [
        "restaurant_name",
        "cuisines",
        "aggregate_rating",
        "votes",
        "cost_for_two",
        "city",
    ]
    # Only include columns that exist
    columns_to_show = [c for c in columns_to_show if c in df.columns]

    if df.empty:
        return "(No restaurants found matching the criteria.)"

    lines: list[str] = []
    for idx, row in df.iterrows():
        parts = []
        for col in columns_to_show:
            label = col.replace("_", " ").title()
            value = row.get(col, "N/A")
            if col == "cost_for_two":
                try:
                    value = f"₹{int(value):,}"
                except (ValueError, TypeError):
                    value = str(value)
            parts.append(f"{label}: {value}")
        lines.append(f"  {idx + 1}. " + " | ".join(parts))

    return "\n".join(lines)


def build_system_prompt() -> str:
    """Return the system prompt (no variable substitution needed)."""
    return _load_template("system.txt")


def build_user_prompt(
    candidates: pd.DataFrame,
    preferences: dict[str, Any],
) -> str:
    """
    Build the user prompt by merging preferences and candidate data into
    the user template.

    Parameters
    ----------
    candidates : pd.DataFrame
        Pre-ranked candidate restaurants.
    preferences : dict
        User preferences with keys: city, budget, cuisines, min_rating,
        additional_preferences.
    """
    template = _load_template("user.txt")

    cuisines = preferences.get("cuisines", [])
    if isinstance(cuisines, list):
        cuisines_str = ", ".join(cuisines) if cuisines else "Any"
    else:
        cuisines_str = str(cuisines) if cuisines else "Any"

    restaurant_table = _dataframe_to_table(candidates)

    return template.format(
        city=preferences.get("city", "Any"),
        budget=preferences.get("budget", "Any"),
        cuisines=cuisines_str,
        min_rating=preferences.get("min_rating", 0.0),
        additional_preferences=preferences.get("additional_preferences", "None"),
        restaurant_table=restaurant_table,
    )


def build_prompt(
    candidates: pd.DataFrame,
    preferences: dict[str, Any],
) -> tuple[str, str]:
    """
    Convenience function — return (system_prompt, user_prompt) as a tuple.
    """
    return build_system_prompt(), build_user_prompt(candidates, preferences)

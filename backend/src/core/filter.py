"""
core/filter.py — Preference-based restaurant filtering pipeline.

Each filter function accepts a DataFrame and returns a subset.  The composite
`apply_filters` function chains them and falls back to progressive relaxation
when no matches are found.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from core.utils import safe_lower

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
#  Individual filters
# ──────────────────────────────────────────────────────────────


def filter_by_location(df: pd.DataFrame, city: str) -> pd.DataFrame:
    """Return restaurants whose ``city`` matches (case-insensitive)."""
    if not city or safe_lower(city) in ("all", "any", ""):
        return df
    mask = df["city"].str.lower().str.strip() == safe_lower(city)
    return df[mask]


def filter_by_budget(df: pd.DataFrame, budget: str) -> pd.DataFrame:
    """
    Return restaurants whose ``budget_category`` matches the requested tier.

    Accepted values: ``"low"``, ``"medium"``, ``"high"`` (case-insensitive).
    """
    if not budget or safe_lower(budget) in ("all", "any", ""):
        return df
    if "budget_category" not in df.columns:
        logger.warning("budget_category column missing — skipping budget filter.")
        return df
    mask = df["budget_category"].str.lower() == safe_lower(budget)
    return df[mask]


def filter_by_cuisine(
    df: pd.DataFrame, cuisines: list[str] | str | None
) -> pd.DataFrame:
    """
    Return restaurants whose ``cuisines`` column contains **any** of the
    requested cuisines (case-insensitive substring match).
    """
    if not cuisines:
        return df
    if isinstance(cuisines, str):
        cuisines = [c.strip() for c in cuisines.split(",") if c.strip()]
    if not cuisines:
        return df

    pattern = "|".join(c.strip() for c in cuisines)
    mask = df["cuisines"].str.contains(pattern, case=False, na=False)
    return df[mask]


def filter_by_rating(df: pd.DataFrame, min_rating: float = 0.0) -> pd.DataFrame:
    """Return restaurants with ``aggregate_rating >= min_rating``."""
    if min_rating <= 0:
        return df
    return df[df["aggregate_rating"] >= min_rating]


# ──────────────────────────────────────────────────────────────
#  Composite filter pipeline
# ──────────────────────────────────────────────────────────────


def apply_filters(df: pd.DataFrame, preferences: dict[str, Any]) -> pd.DataFrame:
    """
    Apply all filters in sequence.  If the result is empty, progressively
    relax constraints until at least one restaurant matches.

    Parameters
    ----------
    df : pd.DataFrame
        The full, cleaned restaurant DataFrame.
    preferences : dict
        Keys:  ``city``, ``budget``, ``cuisines``, ``min_rating``.

    Returns
    -------
    pd.DataFrame
        Filtered (and possibly relaxed) subset of *df*.
    """
    city = preferences.get("city", "")
    budget = preferences.get("budget", "")
    cuisines = preferences.get("cuisines", [])
    min_rating = float(preferences.get("min_rating", 0))

    # Full strict filter
    result = df.copy()
    result = filter_by_location(result, city)
    result = filter_by_budget(result, budget)
    result = filter_by_cuisine(result, cuisines)
    result = filter_by_rating(result, min_rating)

    if len(result) > 0:
        return result

    # ── Progressive relaxation ──────────────────────────────
    logger.info("No exact matches — starting progressive filter relaxation.")

    # Step 1: Remove cuisine filter
    result = filter_by_location(df, city)
    result = filter_by_budget(result, budget)
    result = filter_by_rating(result, min_rating)
    if len(result) > 0:
        logger.info("Relaxation step 1: removed cuisine filter → %d results.", len(result))
        return result

    # Step 2: Lower min_rating by 0.5
    lower_rating = max(0, min_rating - 0.5)
    result = filter_by_location(df, city)
    result = filter_by_budget(result, budget)
    result = filter_by_rating(result, lower_rating)
    if len(result) > 0:
        logger.info(
            "Relaxation step 2: rating %.1f → %.1f → %d results.",
            min_rating, lower_rating, len(result),
        )
        return result

    # Step 3: Remove budget filter
    result = filter_by_location(df, city)
    result = filter_by_rating(result, lower_rating)
    if len(result) > 0:
        logger.info("Relaxation step 3: removed budget filter → %d results.", len(result))
        return result

    # Step 4: Fallback — top-rated in city (no other filters)
    result = filter_by_location(df, city)
    if len(result) > 0:
        logger.info("Relaxation step 4: city-only fallback → %d results.", len(result))
        return result

    # Step 5: Absolute fallback — whole dataset
    logger.warning("All relaxation steps exhausted — returning full dataset.")
    return df

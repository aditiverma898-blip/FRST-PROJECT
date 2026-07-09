"""
data/preprocessor.py — Clean and normalise the raw Zomato dataset.

Handles column renaming, type coercion, missing-value imputation, budget
categorisation, and cuisine normalisation.
"""

from __future__ import annotations

import logging
import re

import numpy as np
import pandas as pd

from data.schema import (
    BUDGET_TIERS,
    COLUMN_RENAME_MAP,
    CRITICAL_FIELDS,
    RATING_MAX,
    RATING_MIN,
    REQUIRED_COLUMNS,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
#  Core cleaning pipeline
# ──────────────────────────────────────────────────────────────


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Master cleaning pipeline — applies all transformations in order.

    1. Rename columns to snake_case
    2. Coerce types (cost → float, rating → float, votes → int, bools)
    3. Drop rows missing critical fields
    4. Clamp ratings to [0, 5]
    5. Normalise cuisine strings
    6. Assign budget categories

    Returns a new DataFrame (does not mutate the original).
    """
    df = df.copy()

    # 1. Rename columns
    df = _rename_columns(df)

    # 2. Type coercion
    df = _coerce_types(df)

    # 3. Drop rows with missing critical values
    before = len(df)
    df = df.dropna(subset=CRITICAL_FIELDS)
    dropped = before - len(df)
    if dropped:
        logger.info("Dropped %d rows with missing critical fields.", dropped)

    # 4. Clamp ratings
    df["aggregate_rating"] = df["aggregate_rating"].clip(RATING_MIN, RATING_MAX)

    # 5. Normalise cuisines
    df = normalize_cuisines(df)

    # 6. Budget categories
    df = categorize_budget(df)

    # 7. Fill remaining NaN in non-critical string columns
    for col in ("city", "cuisines", "location"):
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # 8. Combine location, city, and Bangalore into 'location'
    if "location" in df.columns and "city" in df.columns:
        def combine_location(row):
            loc = str(row['location']).strip()
            city = str(row['city']).strip()
            parts = []
            if loc and loc.lower() != "unknown":
                parts.append(loc)
            if city and city.lower() != "unknown" and city.lower() != loc.lower():
                parts.append(city)
            parts.append("Bangalore")
            return ", ".join(parts)
        df["location"] = df.apply(combine_location, axis=1)

    # 9. Reset index
    df = df.reset_index(drop=True)

    logger.info("Cleaned dataset: %d rows, %d columns.", *df.shape)
    return df


# ──────────────────────────────────────────────────────────────
#  Internal helpers
# ──────────────────────────────────────────────────────────────


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns using COLUMN_RENAME_MAP; convert remaining to snake_case."""
    rename = {}
    for col in df.columns:
        if col in COLUMN_RENAME_MAP:
            rename[col] = COLUMN_RENAME_MAP[col]
        else:
            # Convert PascalCase / Title Case → snake_case
            snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", col)
            snake = snake.replace(" ", "_").lower()
            rename[col] = snake

    df = df.rename(columns=rename)
    return df


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce column types, handling currency symbols and messy strings."""

    # cost_for_two → float
    if "cost_for_two" in df.columns:
        df["cost_for_two"] = (
            df["cost_for_two"]
            .astype(str)
            .str.replace(r"[₹,$,\s,]", "", regex=True)
            .str.strip()
        )
        df["cost_for_two"] = pd.to_numeric(df["cost_for_two"], errors="coerce")

    # aggregate_rating → float
    # The raw dataset may have formats like "4.1/5", "NEW", "-", or plain floats.
    if "aggregate_rating" in df.columns:
        df["aggregate_rating"] = (
            df["aggregate_rating"]
            .astype(str)
            .str.strip()
            .str.replace(r"/5\s*$", "", regex=True)   # "4.1/5" → "4.1"
            .replace({"NEW": None, "-": None, "nan": None, "None": None, "": None})
        )
        df["aggregate_rating"] = pd.to_numeric(
            df["aggregate_rating"], errors="coerce"
        )

    # votes → int
    if "votes" in df.columns:
        df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)

    # Boolean columns
    for bool_col in ("has_online_delivery", "has_table_booking"):
        if bool_col in df.columns:
            df[bool_col] = (
                df[bool_col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({"yes": True, "no": False, "true": True, "false": False, "1": True, "0": False})
                .fillna(False)
            )

    return df


# ──────────────────────────────────────────────────────────────
#  Public preprocessing helpers
# ──────────────────────────────────────────────────────────────


def normalize_cuisines(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean cuisine strings: strip whitespace around commas, title-case each
    cuisine, and remove duplicates within a row.
    """
    if "cuisines" not in df.columns:
        return df

    def _clean(value: str | float) -> str:
        if pd.isna(value):
            return "Unknown"
        parts = [c.strip().title() for c in str(value).split(",") if c.strip()]
        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for p in parts:
            if p.lower() not in seen:
                seen.add(p.lower())
                unique.append(p)
        return ", ".join(unique) if unique else "Unknown"

    df["cuisines"] = df["cuisines"].apply(_clean)
    return df


def categorize_budget(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a ``budget_category`` column (low / medium / high) based on
    ``cost_for_two`` percentile boundaries.
    """
    if "cost_for_two" not in df.columns:
        df["budget_category"] = "medium"
        return df

    low_upper = df["cost_for_two"].quantile(BUDGET_TIERS["low"][1] / 100)
    med_upper = df["cost_for_two"].quantile(BUDGET_TIERS["medium"][1] / 100)

    conditions = [
        df["cost_for_two"] <= low_upper,
        df["cost_for_two"] <= med_upper,
        df["cost_for_two"] > med_upper,
    ]
    choices = ["low", "medium", "high"]
    df["budget_category"] = np.select(conditions, choices, default="medium")

    return df


def get_unique_cities(df: pd.DataFrame) -> list[str]:
    """Return a sorted, deduplicated list of city names."""
    if "city" not in df.columns:
        return []
    cities = df["city"].dropna().unique().tolist()
    return sorted(set(c.strip() for c in cities if c.strip()))


def get_unique_cuisines(df: pd.DataFrame) -> list[str]:
    """
    Return a sorted, deduplicated list of individual cuisine names
    extracted from the comma-separated ``cuisines`` column.
    """
    if "cuisines" not in df.columns:
        return []
    all_cuisines: set[str] = set()
    for value in df["cuisines"].dropna():
        for c in str(value).split(","):
            c = c.strip()
            if c and c.lower() != "unknown":
                all_cuisines.add(c)
    return sorted(all_cuisines)

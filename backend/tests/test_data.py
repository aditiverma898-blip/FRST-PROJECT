"""
tests/test_data.py — Unit tests for the data module (schema, preprocessor).
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from data.schema import REQUIRED_COLUMNS, BUDGET_TIERS, CRITICAL_FIELDS
from data.preprocessor import (
    clean_dataframe,
    categorize_budget,
    normalize_cuisines,
    get_unique_cities,
    get_unique_cuisines,
)


# ──────────────────────────────────────────────────────────────
#  Fixtures
# ──────────────────────────────────────────────────────────────


@pytest.fixture
def raw_df() -> pd.DataFrame:
    """A small synthetic DataFrame mimicking raw Zomato data."""
    return pd.DataFrame(
        {
            "Restaurant Name": [
                "Pizza Palace",
                "Curry House",
                "Sushi Zen",
                "Burger Joint",
                None,  # missing name — should be dropped
            ],
            "City": ["Delhi", "Bangalore", "Delhi", "Mumbai", "Delhi"],
            "Cuisines": [
                "Italian, Continental",
                "Indian, North Indian",
                "Japanese, Sushi",
                "American, Burger",
                "Unknown",
            ],
            "Average Cost for two": ["₹800", "600", "1500", "₹400", "500"],
            "Aggregate rating": [4.5, 3.8, 4.2, 3.0, 4.0],
            "Votes": [320, 150, 200, 80, 10],
            "Has Online delivery": ["Yes", "No", "Yes", "Yes", "No"],
            "Has Table booking": ["No", "Yes", "Yes", "No", "No"],
        }
    )


@pytest.fixture
def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    return clean_dataframe(raw_df)


# ──────────────────────────────────────────────────────────────
#  Schema tests
# ──────────────────────────────────────────────────────────────


class TestSchema:
    def test_budget_tiers_cover_full_range(self):
        """Budget tiers should span 0-100 percentile without gaps."""
        assert BUDGET_TIERS["low"][0] == 0
        assert BUDGET_TIERS["high"][1] == 100

    def test_required_columns_non_empty(self):
        assert len(REQUIRED_COLUMNS) > 0

    def test_critical_fields_are_subset(self):
        for field in CRITICAL_FIELDS:
            assert field in REQUIRED_COLUMNS


# ──────────────────────────────────────────────────────────────
#  Preprocessing tests
# ──────────────────────────────────────────────────────────────


class TestPreprocessor:
    def test_clean_drops_missing_names(self, clean_df):
        """Rows with missing restaurant_name should be dropped."""
        assert clean_df["restaurant_name"].isna().sum() == 0
        assert len(clean_df) == 4  # 5 raw → 4 after dropping null name

    def test_columns_renamed(self, clean_df):
        """Columns should be in snake_case after cleaning."""
        assert "restaurant_name" in clean_df.columns
        assert "Restaurant Name" not in clean_df.columns

    def test_cost_is_numeric(self, clean_df):
        """cost_for_two should be a numeric type."""
        assert pd.api.types.is_numeric_dtype(clean_df["cost_for_two"])

    def test_rating_clamped(self, clean_df):
        """Ratings should be clamped to [0, 5]."""
        assert clean_df["aggregate_rating"].min() >= 0
        assert clean_df["aggregate_rating"].max() <= 5

    def test_budget_category_assigned(self, clean_df):
        """Every row should have a budget_category."""
        assert "budget_category" in clean_df.columns
        assert clean_df["budget_category"].isna().sum() == 0
        assert set(clean_df["budget_category"].unique()).issubset(
            {"low", "medium", "high"}
        )

    def test_boolean_columns(self, clean_df):
        """Boolean columns should contain True/False."""
        for col in ("has_online_delivery", "has_table_booking"):
            if col in clean_df.columns:
                assert clean_df[col].dtype == bool or set(
                    clean_df[col].unique()
                ).issubset({True, False})


class TestNormalizeCuisines:
    def test_strips_whitespace(self):
        df = pd.DataFrame({"cuisines": ["  Italian ,  Chinese , Italian"]})
        result = normalize_cuisines(df)
        assert result["cuisines"].iloc[0] == "Italian, Chinese"

    def test_handles_nan(self):
        df = pd.DataFrame({"cuisines": [None, float("nan")]})
        result = normalize_cuisines(df)
        assert (result["cuisines"] == "Unknown").all()


class TestUniqueHelpers:
    def test_unique_cities(self, clean_df):
        cities = get_unique_cities(clean_df)
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert cities == sorted(cities)  # should be sorted

    def test_unique_cuisines(self, clean_df):
        cuisines = get_unique_cuisines(clean_df)
        assert isinstance(cuisines, list)
        assert len(cuisines) > 0
        assert cuisines == sorted(cuisines)

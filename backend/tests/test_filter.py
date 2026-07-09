"""
tests/test_filter.py — Unit tests for the core filter and ranker modules.
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from core.filter import (
    filter_by_location,
    filter_by_budget,
    filter_by_cuisine,
    filter_by_rating,
    apply_filters,
)
from core.ranker import pre_rank


# ──────────────────────────────────────────────────────────────
#  Fixtures
# ──────────────────────────────────────────────────────────────


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """A small DataFrame for filter testing."""
    return pd.DataFrame(
        {
            "restaurant_name": ["A", "B", "C", "D", "E"],
            "city": ["Delhi", "Delhi", "Mumbai", "Bangalore", "Delhi"],
            "cuisines": [
                "Italian, Chinese",
                "Indian, North Indian",
                "Japanese",
                "Italian",
                "Chinese, Mexican",
            ],
            "cost_for_two": [800.0, 400.0, 1500.0, 600.0, 300.0],
            "aggregate_rating": [4.5, 3.8, 4.2, 3.0, 2.5],
            "votes": [320, 150, 200, 80, 50],
            "budget_category": ["medium", "low", "high", "medium", "low"],
            "has_online_delivery": [True, False, True, True, False],
            "has_table_booking": [False, True, True, False, False],
        }
    )


# ──────────────────────────────────────────────────────────────
#  Individual filter tests
# ──────────────────────────────────────────────────────────────


class TestFilterByLocation:
    def test_exact_match(self, sample_df):
        result = filter_by_location(sample_df, "Delhi")
        assert len(result) == 3

    def test_case_insensitive(self, sample_df):
        result = filter_by_location(sample_df, "delhi")
        assert len(result) == 3

    def test_no_match(self, sample_df):
        result = filter_by_location(sample_df, "London")
        assert len(result) == 0

    def test_empty_city_returns_all(self, sample_df):
        result = filter_by_location(sample_df, "")
        assert len(result) == len(sample_df)

    def test_all_keyword(self, sample_df):
        result = filter_by_location(sample_df, "All")
        assert len(result) == len(sample_df)


class TestFilterByBudget:
    def test_low_budget(self, sample_df):
        result = filter_by_budget(sample_df, "low")
        assert len(result) == 2
        assert all(result["budget_category"] == "low")

    def test_case_insensitive(self, sample_df):
        result = filter_by_budget(sample_df, "HIGH")
        assert len(result) == 1

    def test_empty_budget_returns_all(self, sample_df):
        result = filter_by_budget(sample_df, "")
        assert len(result) == len(sample_df)


class TestFilterByCuisine:
    def test_single_cuisine(self, sample_df):
        result = filter_by_cuisine(sample_df, ["Italian"])
        assert len(result) == 2  # A and D

    def test_multiple_cuisines(self, sample_df):
        result = filter_by_cuisine(sample_df, ["Italian", "Japanese"])
        assert len(result) == 3  # A, C, D

    def test_string_input(self, sample_df):
        result = filter_by_cuisine(sample_df, "Chinese")
        assert len(result) == 2  # A and E

    def test_empty_list_returns_all(self, sample_df):
        result = filter_by_cuisine(sample_df, [])
        assert len(result) == len(sample_df)

    def test_no_match(self, sample_df):
        result = filter_by_cuisine(sample_df, ["French"])
        assert len(result) == 0


class TestFilterByRating:
    def test_minimum_rating(self, sample_df):
        result = filter_by_rating(sample_df, 4.0)
        assert len(result) == 2  # A (4.5) and C (4.2)

    def test_zero_rating_returns_all(self, sample_df):
        result = filter_by_rating(sample_df, 0.0)
        assert len(result) == len(sample_df)


# ──────────────────────────────────────────────────────────────
#  Composite filter tests
# ──────────────────────────────────────────────────────────────


class TestApplyFilters:
    def test_all_filters(self, sample_df):
        prefs = {
            "city": "Delhi",
            "budget": "medium",
            "cuisines": ["Italian"],
            "min_rating": 4.0,
        }
        result = apply_filters(sample_df, prefs)
        assert len(result) == 1
        assert result.iloc[0]["restaurant_name"] == "A"

    def test_relaxation_on_empty(self, sample_df):
        """When no matches exist, filters should relax and return something."""
        prefs = {
            "city": "Delhi",
            "budget": "high",
            "cuisines": ["French"],
            "min_rating": 4.9,
        }
        result = apply_filters(sample_df, prefs)
        assert len(result) > 0  # progressive relaxation should find results


# ──────────────────────────────────────────────────────────────
#  Ranker tests
# ──────────────────────────────────────────────────────────────


class TestPreRank:
    def test_returns_top_n(self, sample_df):
        result = pre_rank(sample_df, top_n=3)
        assert len(result) == 3

    def test_highest_score_first(self, sample_df):
        result = pre_rank(sample_df, top_n=5)
        # Restaurant A has highest rating × log(votes) so should be first
        assert result.iloc[0]["restaurant_name"] == "A"

    def test_empty_df(self):
        empty = pd.DataFrame(columns=["aggregate_rating", "votes", "restaurant_name"])
        result = pre_rank(empty)
        assert len(result) == 0

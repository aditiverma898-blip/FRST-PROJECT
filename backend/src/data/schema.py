"""
data/schema.py — Column schemas, constants, and validation for the Zomato dataset.

Defines the expected structure of the processed DataFrame and budget tier
boundaries used throughout the application.
"""

# ──────────────────────────────────────────────────────────────
#  Required columns after preprocessing
# ──────────────────────────────────────────────────────────────

REQUIRED_COLUMNS: dict[str, type] = {
    "restaurant_name": str,
    "city": str,
    "cuisines": str,
    "cost_for_two": float,
    "aggregate_rating": float,
    "votes": int,
    "has_online_delivery": bool,
    "has_table_booking": bool,
}

# ──────────────────────────────────────────────────────────────
#  Budget tier definitions (percentile ranges)
# ──────────────────────────────────────────────────────────────

BUDGET_TIERS: dict[str, tuple[int, int]] = {
    "low": (0, 33),       # 0th  → 33rd percentile
    "medium": (33, 66),   # 33rd → 66th percentile
    "high": (66, 100),    # 66th → 100th percentile
}

# ──────────────────────────────────────────────────────────────
#  Column name mappings (raw → clean)
# ──────────────────────────────────────────────────────────────

# Some Hugging Face datasets have inconsistent column names.
# This mapping normalises them to our expected snake_case schema.
COLUMN_RENAME_MAP: dict[str, str] = {
    # ── Name variants ─────────────────────────────────────────
    "Restaurant Name": "restaurant_name",
    "restaurant name": "restaurant_name",
    "name": "restaurant_name",

    # ── City / Location variants ──────────────────────────────
    "City": "city",
    "listed_in(city)": "city",

    # ── Cuisine variants ──────────────────────────────────────
    "Cuisines": "cuisines",
    "cuisines": "cuisines",

    # ── Cost variants ─────────────────────────────────────────
    "Average Cost for two": "cost_for_two",
    "average_cost_for_two": "cost_for_two",
    "Average Cost for Two": "cost_for_two",
    "cost_for_two": "cost_for_two",
    "approx_cost(for two people)": "cost_for_two",

    # ── Rating variants ───────────────────────────────────────
    "Aggregate rating": "aggregate_rating",
    "aggregate_rating": "aggregate_rating",
    "Rating": "aggregate_rating",
    "rate": "aggregate_rating",

    # ── Votes variants ────────────────────────────────────────
    "Votes": "votes",
    "votes": "votes",

    # ── Online delivery variants ──────────────────────────────
    "Has Online delivery": "has_online_delivery",
    "has_online_delivery": "has_online_delivery",
    "online_order": "has_online_delivery",

    # ── Table booking variants ────────────────────────────────
    "Has Table booking": "has_table_booking",
    "has_table_booking": "has_table_booking",
    "book_table": "has_table_booking",

    # ── Supplementary columns ─────────────────────────────────
    "location": "location",
    "rest_type": "restaurant_type",
    "listed_in(type)": "listed_in_type",
    "dish_liked": "dish_liked",
}

# ──────────────────────────────────────────────────────────────
#  Validation helpers
# ──────────────────────────────────────────────────────────────

RATING_MIN = 0.0
RATING_MAX = 5.0

# Fields that must not be null for a valid row
CRITICAL_FIELDS = ["restaurant_name", "aggregate_rating"]

# Maximum restaurants to pass to the LLM prompt
MAX_CANDIDATES_FOR_LLM = 20

"""
ui/components.py — Reusable Streamlit UI components.

Provides functions for rendering the hero section, preference forms,
recommendation cards, and statistics.
"""

from __future__ import annotations

from typing import Any

import streamlit as st
import pandas as pd


# ──────────────────────────────────────────────────────────────
#  Hero Section
# ──────────────────────────────────────────────────────────────


def render_hero() -> None:
    """Render the hero banner at the top of the page."""
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">🍽️ Zomato AI Recommendations</div>
            <div class="hero-subtitle">
                Discover your perfect dining experience — powered by AI
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────
#  Statistics Row
# ──────────────────────────────────────────────────────────────


def render_stats(
    total_restaurants: int,
    total_cities: int,
    total_cuisines: int,
) -> None:
    """Render a row of dataset statistics cards."""
    cols = st.columns(3)
    stats = [
        (f"{total_restaurants:,}", "Restaurants"),
        (f"{total_cities}", "Cities"),
        (f"{total_cuisines}", "Cuisines"),
    ]
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────────────────────
#  Preference Form (Sidebar)
# ──────────────────────────────────────────────────────────────


def render_sidebar_form(
    cities: list[str],
    cuisines: list[str],
    default_rating: float = 3.0,
    rating_step: float = 0.5,
) -> dict[str, Any] | None:
    """
    Render the preference input form in the sidebar.

    Returns a dict of preferences when the user clicks *Get Recommendations*,
    or ``None`` if the button hasn't been clicked.
    """
    with st.sidebar:
        st.markdown("### 🎯 Your Preferences")
        st.markdown("---")

        city = st.selectbox(
            "📍 City / Location",
            options=["All"] + cities,
            index=0,
            help="Select a city to narrow your search.",
        )

        budget = st.radio(
            "💰 Budget",
            options=["All", "Low", "Medium", "High"],
            index=0,
            horizontal=True,
            help="Low = affordable, High = premium dining.",
        )

        selected_cuisines = st.multiselect(
            "🍕 Cuisine Preferences",
            options=cuisines,
            default=[],
            help="Select one or more cuisines you enjoy.",
        )

        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=0.0,
            max_value=5.0,
            value=default_rating,
            step=rating_step,
            help="Filter restaurants below this rating.",
        )

        additional = st.text_area(
            "📝 Additional Preferences",
            placeholder="e.g., family-friendly, romantic, fast service, outdoor seating…",
            height=80,
            help="Free-text preferences — the AI will factor these in.",
        )

        st.markdown("---")

        clicked = st.button("🔍 Get Recommendations", use_container_width=True)

    if clicked:
        return {
            "city": city if city != "All" else "",
            "budget": budget.lower() if budget != "All" else "",
            "cuisines": selected_cuisines,
            "min_rating": min_rating,
            "additional_preferences": additional.strip() if additional else "",
        }
    return None


# ──────────────────────────────────────────────────────────────
#  Recommendation Cards
# ──────────────────────────────────────────────────────────────


def render_recommendation_card(rec: dict[str, Any]) -> None:
    """Render a single recommendation as a styled card."""
    rank = rec.get("rank", "?")
    name = rec.get("restaurant_name", "Unknown Restaurant")
    cuisines = rec.get("cuisines", "N/A")
    rating = rec.get("aggregate_rating", "N/A")
    cost = rec.get("cost_for_two", "N/A")
    explanation = rec.get("explanation", "")

    # Format cost
    if isinstance(cost, (int, float)):
        cost_str = f"₹{int(cost):,}"
    else:
        cost_str = str(cost)

    # Format rating
    if isinstance(rating, (int, float)):
        rating_str = f"{rating:.1f} / 5.0"
    else:
        rating_str = str(rating)

    # Rank badge emoji
    rank_emojis = {1: "🏆", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣"}
    rank_icon = rank_emojis.get(rank, f"#{rank}")

    st.markdown(
        f"""
        <div class="rec-card">
            <span class="rec-rank">{rank_icon} #{rank}</span>
            <div class="rec-name">{name}</div>
            <div class="rec-meta">
                <span class="rec-badge">🍕 {cuisines}</span>
                <span class="rec-badge">⭐ {rating_str}</span>
                <span class="rec-badge">💰 {cost_str}</span>
            </div>
            <div class="rec-explanation">
                💡 <strong>Why this pick:</strong> {explanation}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(recommendations: list[dict[str, Any]]) -> None:
    """Render all recommendation cards."""
    if not recommendations:
        st.warning("No recommendations could be generated.  Try adjusting your preferences.")
        return

    st.markdown("## ✨ Your AI-Powered Recommendations")
    st.markdown("---")
    for rec in recommendations:
        render_recommendation_card(rec)


# ──────────────────────────────────────────────────────────────
#  Error display
# ──────────────────────────────────────────────────────────────


def render_error(message: str, details: str = "") -> None:
    """Display a user-friendly error message."""
    st.error(f"⚠️ {message}")
    if details:
        with st.expander("🔍 Technical Details"):
            st.code(details)


def render_filter_info(
    total: int,
    filtered: int,
    ranked: int,
    relaxed: bool = False,
) -> None:
    """Show a summary of how many restaurants matched the filters."""
    msg = f"📊 Found **{filtered:,}** restaurants matching your criteria out of **{total:,}** total."
    if ranked < filtered:
        msg += f"  Top **{ranked}** selected for AI ranking."
    if relaxed:
        msg += "  _(Some filters were relaxed to find results.)_"
    st.info(msg)

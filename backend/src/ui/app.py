"""
ui/app.py — Streamlit main application for the Zomato AI Recommendation System.

Run with:  streamlit run ui/app.py
"""

from __future__ import annotations

import sys
import os
import logging

# ── Ensure project root is on the import path ───────────────
# This lets Streamlit import `data`, `core`, and `llm` packages
# regardless of which directory the `streamlit run` command is
# executed from.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from ui.config import (
    PAGE_TITLE,
    PAGE_ICON,
    PAGE_LAYOUT,
    CUSTOM_CSS,
    DEFAULT_MIN_RATING,
    RATING_STEP,
)
from ui.components import (
    render_hero,
    render_stats,
    render_sidebar_form,
    render_recommendations,
    render_error,
    render_filter_info,
)

# ──────────────────────────────────────────────────────────────
#  Logging
# ──────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-25s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
#  Page config & CSS injection
# ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  Cached data loader
# ──────────────────────────────────────────────────────────────


@st.cache_data(show_spinner="Loading restaurant dataset…")
def load_dataset() -> pd.DataFrame:
    """Load and cache the cleaned Zomato dataset."""
    from data.loader import get_dataframe
    return get_dataframe()


@st.cache_data(show_spinner=False)
def get_cities(df: pd.DataFrame) -> list[str]:
    from data.preprocessor import get_unique_cities
    return get_unique_cities(df)


@st.cache_data(show_spinner=False)
def get_cuisines(df: pd.DataFrame) -> list[str]:
    from data.preprocessor import get_unique_cuisines
    return get_unique_cuisines(df)


# ──────────────────────────────────────────────────────────────
#  Main application
# ──────────────────────────────────────────────────────────────


def main() -> None:
    # 1. Load data
    try:
        df = load_dataset()
    except Exception as exc:
        render_error(
            "Failed to load the restaurant dataset.",
            str(exc),
        )
        st.stop()

    cities = get_cities(df)
    cuisines_list = get_cuisines(df)

    # 2. Hero section & stats
    render_hero()
    render_stats(
        total_restaurants=len(df),
        total_cities=len(cities),
        total_cuisines=len(cuisines_list),
    )

    # 3. Sidebar form
    preferences = render_sidebar_form(
        cities=cities,
        cuisines=cuisines_list,
        default_rating=DEFAULT_MIN_RATING,
        rating_step=RATING_STEP,
    )

    if preferences is None:
        # Show welcome message when no search has been made yet
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem 1rem; 
                        color: rgba(255,255,255,0.5); font-size: 1.1rem;">
                <p style="font-size: 3rem; margin-bottom: 1rem;">🍴</p>
                <p>Select your preferences in the sidebar and click<br>
                <strong style="color: rgba(255,107,107,0.9);">Get Recommendations</strong>
                to discover amazing restaurants.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # 4. Apply filters
    from core.filter import apply_filters
    from core.ranker import pre_rank

    filtered_df = apply_filters(df, preferences)
    original_filtered_count = len(filtered_df)
    relaxed = original_filtered_count == 0  # if 0 then relaxation happened

    # Re-check after relaxation
    if filtered_df.empty:
        render_error("No restaurants found even after relaxing filters.  Try different preferences.")
        return

    # 5. Pre-rank
    candidates = pre_rank(filtered_df)

    render_filter_info(
        total=len(df),
        filtered=len(filtered_df),
        ranked=len(candidates),
        relaxed=relaxed,
    )

    # 6. LLM recommendation
    from llm.config import llm_config

    if not llm_config.is_configured:
        render_error(
            "Groq API key is not configured.",
            "Please set GROQ_API_KEY in your .env file.\n"
            "Get a free key at https://console.groq.com",
        )
        st.stop()

    with st.spinner("🤖  AI is analyzing restaurants and crafting personalized recommendations…"):
        try:
            from llm.prompt_builder import build_prompt
            from llm.client import get_recommendation
            from llm.parser import parse_recommendations

            system_prompt, user_prompt = build_prompt(candidates, preferences)
            raw_response = get_recommendation(system_prompt, user_prompt)
            recommendations = parse_recommendations(raw_response)

        except ValueError as exc:
            render_error("Configuration Error", str(exc))
            return
        except RuntimeError as exc:
            render_error(
                "The AI service is temporarily unavailable.  Please try again.",
                str(exc),
            )
            return
        except Exception as exc:
            render_error(
                "An unexpected error occurred while generating recommendations.",
                str(exc),
            )
            logger.exception("Unexpected error during LLM call.")
            return

    # 7. Display results
    if recommendations:
        render_recommendations(recommendations)
    else:
        st.warning(
            "The AI returned an unexpected response.  "
            "Here are the top matches based on data alone:"
        )
        # Fallback — show a simple table of top candidates
        display_cols = [
            c
            for c in [
                "restaurant_name",
                "cuisines",
                "aggregate_rating",
                "cost_for_two",
                "city",
            ]
            if c in candidates.columns
        ]
        st.dataframe(candidates[display_cols].head(5), use_container_width=True)


# ──────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
else:
    main()

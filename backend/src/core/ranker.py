"""
core/ranker.py — Pre-ranking logic to select the best candidates before LLM.

Ranks restaurants using a composite score  ``aggregate_rating × log(votes + 1)``
which balances quality (rating) with popularity (votes) while dampening the
effect of very high vote counts.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from data.schema import MAX_CANDIDATES_FOR_LLM

logger = logging.getLogger(__name__)


def pre_rank(df: pd.DataFrame, top_n: int = MAX_CANDIDATES_FOR_LLM) -> pd.DataFrame:
    """
    Rank restaurants by a composite score and return the top *top_n*.

    Score = aggregate_rating × log2(votes + 1)

    Parameters
    ----------
    df : pd.DataFrame
        Filtered restaurant DataFrame.
    top_n : int, default 20
        Maximum number of candidates to return.

    Returns
    -------
    pd.DataFrame
        Top-*top_n* restaurants sorted by descending composite score.
    """
    if df.empty:
        return df

    result = df.copy()

    # Ensure numeric columns
    result["aggregate_rating"] = pd.to_numeric(
        result["aggregate_rating"], errors="coerce"
    ).fillna(0)
    result["votes"] = pd.to_numeric(result["votes"], errors="coerce").fillna(0)

    # Composite score
    result["_score"] = result["aggregate_rating"] * np.log2(
        result["votes"].clip(lower=0) + 1
    )

    result = result.sort_values("_score", ascending=False).head(top_n)
    result = result.drop(columns=["_score"])

    logger.info("Pre-ranked: returning top %d of %d candidates.", len(result), len(df))
    return result.reset_index(drop=True)

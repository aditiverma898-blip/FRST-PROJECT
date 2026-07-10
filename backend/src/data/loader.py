"""
data/loader.py — Load the Zomato dataset from Hugging Face and cache locally.

Provides `get_dataframe()` as the primary public interface.  On first call it
downloads the dataset, preprocesses it via `data.preprocessor`, and persists a
Parquet cache.  Subsequent calls load from the cache unless `force_reload=True`.
"""

from __future__ import annotations

import os
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
#  Constants
# ──────────────────────────────────────────────────────────────

DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
CACHE_DIR = Path(os.getenv("DATASET_CACHE_DIR", "./data/cache"))
CACHE_FILE = CACHE_DIR / "zomato_processed_lite.parquet"

# ──────────────────────────────────────────────────────────────
#  Internal helpers
# ──────────────────────────────────────────────────────────────


def load_from_huggingface() -> pd.DataFrame:
    """Download the dataset from Hugging Face and return a raw DataFrame."""
    try:
        from datasets import load_dataset

        logger.info("Downloading dataset from Hugging Face: %s", DATASET_NAME)
        dataset = load_dataset(DATASET_NAME)

        # The dataset might have splits — pick the first available one
        if isinstance(dataset, dict):
            split_name = list(dataset.keys())[0]
            df = dataset[split_name].to_pandas()
        else:
            df = dataset.to_pandas()

        # Railway's free tier has a 500MB RAM limit.
        # The full dataset consumes ~540MB in memory, causing OOM crashes.
        # We sample 10,000 rows to ensure memory usage stays well below the limit.
        if len(df) > 10000:
            logger.info(f"Sampling 10,000 rows from dataset to prevent OOM (original size: {len(df)})")
            df = df.sample(n=10000, random_state=42).reset_index(drop=True)

        logger.info("Downloaded %d rows from Hugging Face.", len(df))
        return df

    except Exception as exc:
        logger.error("Failed to load dataset from Hugging Face: %s", exc)
        raise RuntimeError(
            f"Could not load Zomato dataset from Hugging Face.  "
            f"Ensure you have internet connectivity and the `datasets` "
            f"package is installed.\n\nOriginal error: {exc}"
        ) from exc


def load_from_cache(cache_path: Path | str | None = None) -> pd.DataFrame | None:
    """Return the cached DataFrame if it exists, otherwise ``None``."""
    path = Path(cache_path) if cache_path else CACHE_FILE
    if path.exists():
        logger.info("Loading cached dataset from %s", path)
        return pd.read_parquet(path)
    return None


def _save_to_cache(df: pd.DataFrame, cache_path: Path | str | None = None) -> None:
    """Persist the processed DataFrame to Parquet."""
    path = Path(cache_path) if cache_path else CACHE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    logger.info("Cached processed dataset to %s (%d rows).", path, len(df))


# ──────────────────────────────────────────────────────────────
#  Public API
# ──────────────────────────────────────────────────────────────


def get_dataframe(force_reload: bool = False) -> pd.DataFrame:
    """
    Return the cleaned Zomato restaurant DataFrame.

    On first call the dataset is fetched from Hugging Face, cleaned via
    `data.preprocessor.clean_dataframe`, and saved as a local Parquet cache.
    Subsequent calls serve the cache unless *force_reload* is ``True``.
    """
    if not force_reload:
        cached = load_from_cache()
        if cached is not None:
            return cached

    # Import here to avoid circular imports
    from data.preprocessor import clean_dataframe

    raw_df = load_from_huggingface()
    clean_df = clean_dataframe(raw_df)
    _save_to_cache(clean_df)
    return clean_df

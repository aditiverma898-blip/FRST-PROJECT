"""
core/utils.py — Shared utility functions used across modules.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def safe_lower(value: str | None) -> str:
    """Return a lowercase, stripped version of *value* (empty string if None)."""
    if value is None:
        return ""
    return str(value).strip().lower()


def format_currency(amount: float | int, symbol: str = "₹") -> str:
    """Format a numeric amount as a currency string (e.g. ₹800)."""
    try:
        return f"{symbol}{int(amount):,}"
    except (ValueError, TypeError):
        return f"{symbol}?"


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate text to *max_length* characters, appending '…' if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 1] + "…"

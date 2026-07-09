"""
llm/client.py — Groq API client with retry logic and error handling.

Provides a `GroqClient` class for sending chat completion requests
to the Groq API and a module-level `get_recommendation` convenience function.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from groq import Groq

from llm.config import llm_config

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
#  Client class
# ──────────────────────────────────────────────────────────────


class GroqClient:
    """
    Wrapper around the Groq Python SDK with built-in retry logic
    and exponential backoff.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> None:
        self.api_key = api_key or llm_config.api_key
        self.model = model or llm_config.model
        self.temperature = temperature if temperature is not None else llm_config.temperature
        self.max_tokens = max_tokens if max_tokens is not None else llm_config.max_tokens
        self.max_retries = llm_config.max_retries
        self.timeout = llm_config.timeout

        if not self.api_key or self.api_key == "gsk_your_api_key_here":
            raise ValueError(
                "Groq API key is not configured.  Please set GROQ_API_KEY "
                "in your .env file.  Get a free key at https://console.groq.com"
            )

        self._client = Groq(api_key=self.api_key)

    # ── Core request ────────────────────────────────────────

    def get_recommendation(
        self, system_prompt: str, user_prompt: str
    ) -> str:
        """
        Send a chat completion request and return the LLM's response text.

        Retries transient errors up to ``max_retries`` times with
        exponential backoff.
        """
        return self._retry_with_backoff(
            lambda: self._send_request(system_prompt, user_prompt)
        )

    def _send_request(self, system_prompt: str, user_prompt: str) -> str:
        """Execute a single chat completion request."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=llm_config.top_p,
        )
        content = response.choices[0].message.content
        return content if content else ""

    # ── Retry logic ─────────────────────────────────────────

    def _retry_with_backoff(
        self,
        func: Any,
        max_retries: int | None = None,
    ) -> str:
        """
        Execute *func* with exponential backoff on failure.

        Retries on any exception except ``ValueError`` (configuration errors).
        """
        retries = max_retries if max_retries is not None else self.max_retries
        last_error: Exception | None = None

        for attempt in range(retries):
            try:
                return func()
            except ValueError:
                raise  # Don't retry configuration errors
            except Exception as exc:
                last_error = exc
                wait = 2**attempt  # 1s, 2s, 4s …
                logger.warning(
                    "LLM request failed (attempt %d/%d): %s — retrying in %ds.",
                    attempt + 1,
                    retries,
                    exc,
                    wait,
                )
                time.sleep(wait)

        raise RuntimeError(
            f"LLM request failed after {retries} attempts.  "
            f"Last error: {last_error}"
        )


# ──────────────────────────────────────────────────────────────
#  Module-level convenience
# ──────────────────────────────────────────────────────────────

_default_client: GroqClient | None = None


def get_client() -> GroqClient:
    """Return or create the default GroqClient singleton."""
    global _default_client
    if _default_client is None:
        _default_client = GroqClient()
    return _default_client


def get_recommendation(system_prompt: str, user_prompt: str) -> str:
    """Convenience wrapper — send a request via the default client."""
    return get_client().get_recommendation(system_prompt, user_prompt)

"""
llm/config.py — LLM configuration loaded from environment variables.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


class LLMConfig:
    """Configuration container for the Groq LLM client."""

    def __init__(self) -> None:
        self.api_key: str = os.getenv("GROQ_API_KEY", "")
        self.model: str = os.getenv("LLM_MODEL", "llama3-70b-8192")
        self.temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
        self.top_p: float = float(os.getenv("LLM_TOP_P", "0.9"))
        self.timeout: int = int(os.getenv("LLM_TIMEOUT", "30"))
        self.max_retries: int = int(os.getenv("LLM_MAX_RETRIES", "3"))

    @property
    def is_configured(self) -> bool:
        """Return True if a real API key is set."""
        return bool(self.api_key) and self.api_key != "gsk_your_api_key_here"

    def __repr__(self) -> str:
        return (
            f"LLMConfig(model={self.model!r}, temperature={self.temperature}, "
            f"max_tokens={self.max_tokens}, configured={self.is_configured})"
        )


# Singleton instance
llm_config = LLMConfig()

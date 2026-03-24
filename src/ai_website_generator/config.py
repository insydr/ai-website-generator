"""
Configuration Module
====================

Handles application configuration, settings, and secrets management.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List

from ai_website_generator.constants import (
    DEFAULT_MODEL_ID,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    API_TIMEOUT,
    API_REFERER,
    API_TITLE,
)


@dataclass
class AppConfig:
    """
    Application configuration class.

    Attributes:
        api_key: OpenRouter API key
        model: Selected model ID
        temperature: Generation temperature
        max_tokens: Maximum tokens for generation
        timeout: API request timeout in seconds
    """

    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL_ID
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS
    timeout: int = API_TIMEOUT

    @property
    def is_configured(self) -> bool:
        """Check if the app is properly configured."""
        return bool(self.api_key)

    def get_headers(self) -> dict:
        """Get API request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": API_REFERER,
            "X-Title": API_TITLE,
            "Content-Type": "application/json",
        }


class ConfigManager:
    """
    Manages application configuration from multiple sources.

    Priority order:
    1. Environment variables
    2. Streamlit secrets
    3. Default values
    """

    _instance: Optional["ConfigManager"] = None
    _config: Optional[AppConfig] = None

    def __new__(cls) -> "ConfigManager":
        """Singleton pattern for configuration manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_config(self, api_key_override: Optional[str] = None) -> AppConfig:
        """
        Get application configuration.

        Args:
            api_key_override: Override API key from session state

        Returns:
            AppConfig instance
        """
        if self._config is None:
            self._config = AppConfig()

        # Set API key with priority
        if api_key_override:
            self._config.api_key = api_key_override
        else:
            self._config.api_key = self._get_api_key()

        return self._config

    def _get_api_key(self) -> Optional[str]:
        """
        Get API key from various sources.

        Returns:
            API key if found, None otherwise
        """
        # Try environment variable first
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key:
            return api_key

        # Try Streamlit secrets
        try:
            import streamlit as st

            if hasattr(st, "secrets") and "openrouter_api_key" in st.secrets:
                return st.secrets["openrouter_api_key"]
        except ImportError:
            pass

        return None

    def update_config(self, **kwargs) -> None:
        """
        Update configuration values.

        Args:
            **kwargs: Configuration key-value pairs to update
        """
        if self._config is None:
            self._config = AppConfig()

        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = None


# Global config manager instance
config_manager = ConfigManager()


def get_config(api_key: Optional[str] = None) -> AppConfig:
    """
    Convenience function to get configuration.

    Args:
        api_key: Optional API key override

    Returns:
        AppConfig instance
    """
    return config_manager.get_config(api_key)

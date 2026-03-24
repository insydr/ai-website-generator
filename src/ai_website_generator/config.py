"""
Configuration Module
====================

Handles application configuration, settings, and secrets management.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from ai_website_generator.constants import (
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    API_TIMEOUT,
    DEFAULT_PROVIDER,
    DEFAULT_MODEL,
)
from ai_website_generator.providers.base import ProviderType, ProviderConfig


@dataclass
class AppConfig:
    """
    Application configuration class.

    Attributes:
        provider_type: Type of AI provider to use
        api_key: API key for the provider
        model: Model ID to use
        base_url: Custom base URL (for custom provider)
        temperature: Generation temperature
        max_tokens: Maximum tokens for generation
        timeout: API request timeout in seconds
        extra_headers: Additional headers for requests
        extra_params: Additional parameters for requests
    """

    provider_type: ProviderType = ProviderType.OPENROUTER
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL
    base_url: Optional[str] = None
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS
    timeout: int = API_TIMEOUT
    extra_headers: Dict[str, str] = field(default_factory=dict)
    extra_params: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_configured(self) -> bool:
        """Check if the app is properly configured."""
        return bool(self.api_key and self.model)

    def to_provider_config(self) -> ProviderConfig:
        """Convert to ProviderConfig for provider instantiation."""
        return ProviderConfig(
            provider_type=self.provider_type,
            api_key=self.api_key or "",
            model=self.model,
            base_url=self.base_url,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            extra_headers=self.extra_headers,
            extra_params=self.extra_params,
        )


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

    def get_config(
        self,
        provider_type: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> AppConfig:
        """
        Get application configuration.

        Args:
            provider_type: Override provider type
            api_key: Override API key
            model: Override model
            base_url: Override base URL

        Returns:
            AppConfig instance
        """
        if self._config is None:
            self._config = AppConfig()

        # Apply overrides
        if provider_type:
            try:
                self._config.provider_type = ProviderType(provider_type)
            except ValueError:
                self._config.provider_type = ProviderType.OPENROUTER

        if api_key:
            self._config.api_key = api_key
        else:
            # Try to get from environment/secrets
            self._config.api_key = self._get_api_key()

        if model:
            self._config.model = model

        if base_url:
            self._config.base_url = base_url

        return self._config

    def _get_api_key(self) -> Optional[str]:
        """
        Get API key from various sources.

        Checks for provider-specific env vars first, then generic ones.

        Returns:
            API key if found, None otherwise
        """
        # Try provider-specific environment variables
        env_key_mapping = {
            ProviderType.OPENROUTER: "OPENROUTER_API_KEY",
            ProviderType.OPENAI: "OPENAI_API_KEY",
            ProviderType.ANTHROPIC: "ANTHROPIC_API_KEY",
            ProviderType.GROQ: "GROQ_API_KEY",
        }

        if self._config and self._config.provider_type in env_key_mapping:
            env_key = env_key_mapping[self._config.provider_type]
            api_key = os.environ.get(env_key)
            if api_key:
                return api_key

        # Try generic API key env var
        api_key = os.environ.get("AI_API_KEY")
        if api_key:
            return api_key

        # Try Streamlit secrets
        try:
            import streamlit as st

            if hasattr(st, "secrets"):
                # Check provider-specific secrets
                secret_key_mapping = {
                    ProviderType.OPENROUTER: "openrouter_api_key",
                    ProviderType.OPENAI: "openai_api_key",
                    ProviderType.ANTHROPIC: "anthropic_api_key",
                    ProviderType.GROQ: "groq_api_key",
                }

                if self._config and self._config.provider_type in secret_key_mapping:
                    secret_key = secret_key_mapping[self._config.provider_type]
                    if secret_key in st.secrets:
                        return st.secrets[secret_key]

                # Check generic api_key
                if "api_key" in st.secrets:
                    return st.secrets["api_key"]

        except (ImportError, Exception):
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
            if key == "provider_type" and isinstance(value, str):
                try:
                    value = ProviderType(value)
                except ValueError:
                    continue

            if hasattr(self._config, key):
                setattr(self._config, key, value)

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = None


# Global config manager instance
config_manager = ConfigManager()


def get_config(
    provider_type: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> AppConfig:
    """
    Convenience function to get configuration.

    Args:
        provider_type: Override provider type
        api_key: Override API key
        model: Override model
        base_url: Override base URL

    Returns:
        AppConfig instance
    """
    return config_manager.get_config(provider_type, api_key, model, base_url)

"""
Provider Registry Module
========================

Registry for managing and instantiating AI providers.
"""

from typing import Dict, List, Optional, Type

from ai_website_generator.providers.base import (
    BaseProvider,
    ProviderConfig,
    ProviderType,
    ModelInfo,
)
from ai_website_generator.providers.openrouter import OpenRouterProvider
from ai_website_generator.providers.openai import OpenAIProvider
from ai_website_generator.providers.anthropic import AnthropicProvider
from ai_website_generator.providers.groq import GroqProvider
from ai_website_generator.providers.custom import CustomProvider


class ProviderRegistry:
    """
    Registry for AI providers.

    Manages provider registration and instantiation.

    Example:
        registry = ProviderRegistry()
        provider = registry.get_provider(ProviderType.OPENROUTER, config)
    """

    _providers: Dict[ProviderType, Type[BaseProvider]] = {
        ProviderType.OPENROUTER: OpenRouterProvider,
        ProviderType.OPENAI: OpenAIProvider,
        ProviderType.ANTHROPIC: AnthropicProvider,
        ProviderType.GROQ: GroqProvider,
        ProviderType.CUSTOM: CustomProvider,
    }

    @classmethod
    def register(cls, provider_type: ProviderType, provider_class: Type[BaseProvider]) -> None:
        """
        Register a new provider type.

        Args:
            provider_type: Type identifier for the provider
            provider_class: Provider class to register
        """
        cls._providers[provider_type] = provider_class

    @classmethod
    def get_provider(cls, config: ProviderConfig) -> BaseProvider:
        """
        Get a provider instance for the given configuration.

        Args:
            config: Provider configuration

        Returns:
            Instantiated provider

        Raises:
            ValueError: If provider type is not registered
        """
        provider_class = cls._providers.get(config.provider_type)

        if provider_class is None:
            raise ValueError(f"Unknown provider type: {config.provider_type}")

        return provider_class(config)

    @classmethod
    def get_available_providers(cls) -> List[Dict[str, str]]:
        """
        Get list of available providers.

        Returns:
            List of provider information dictionaries
        """
        return [
            {
                "type": ProviderType.OPENROUTER.value,
                "name": OpenRouterProvider.PROVIDER_NAME,
                "key_prefix": OpenRouterProvider.API_KEY_PREFIX,
                "description": "Unified access to multiple LLM providers with free tier",
            },
            {
                "type": ProviderType.OPENAI.value,
                "name": OpenAIProvider.PROVIDER_NAME,
                "key_prefix": OpenAIProvider.API_KEY_PREFIX,
                "description": "Direct access to GPT models",
            },
            {
                "type": ProviderType.ANTHROPIC.value,
                "name": AnthropicProvider.PROVIDER_NAME,
                "key_prefix": AnthropicProvider.API_KEY_PREFIX,
                "description": "Claude models for complex reasoning",
            },
            {
                "type": ProviderType.GROQ.value,
                "name": GroqProvider.PROVIDER_NAME,
                "key_prefix": GroqProvider.API_KEY_PREFIX,
                "description": "Ultra-fast inference with LPU technology",
            },
            {
                "type": ProviderType.CUSTOM.value,
                "name": CustomProvider.PROVIDER_NAME,
                "key_prefix": "",
                "description": "Bring your own API endpoint",
            },
        ]

    @classmethod
    def get_provider_models(cls, provider_type: ProviderType) -> List[ModelInfo]:
        """
        Get available models for a provider.

        Args:
            provider_type: Type of provider

        Returns:
            List of available models

        Raises:
            ValueError: If provider type is not registered
        """
        # Create a dummy config to get model list
        dummy_config = ProviderConfig(
            provider_type=provider_type,
            api_key="dummy",
            model="dummy",
        )

        provider_class = cls._providers.get(provider_type)
        if provider_class is None:
            raise ValueError(f"Unknown provider type: {provider_type}")

        # Get models from class attribute or instance method
        if hasattr(provider_class, "MODELS"):
            return provider_class.MODELS
        elif hasattr(provider_class, "FREE_MODELS"):
            models = provider_class.FREE_MODELS.copy()
            if hasattr(provider_class, "PAID_MODELS"):
                models.extend(provider_class.PAID_MODELS)
            return models

        return []


def get_provider(config: ProviderConfig) -> BaseProvider:
    """
    Convenience function to get a provider instance.

    Args:
        config: Provider configuration

    Returns:
        Instantiated provider
    """
    return ProviderRegistry.get_provider(config)

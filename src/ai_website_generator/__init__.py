"""
AI Website Generator
====================

A Streamlit application that generates website code (HTML/CSS/JS) from natural
language descriptions using multiple AI providers.

Supports:
- OpenRouter (free models available)
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)
- Groq (ultra-fast inference)
- Custom API endpoints

Example usage:
    streamlit run -m ai_website_generator

Or programmatically:
    from ai_website_generator import get_provider, ProviderConfig, ProviderType

    config = ProviderConfig(
        provider_type=ProviderType.OPENROUTER,
        api_key="sk-or-...",
        model="meta-llama/llama-3.2-3b-instruct:free"
    )
    provider = get_provider(config)
    response = provider.chat([{"role": "user", "content": "Hello"}])
"""

__version__ = "1.1.0"
__author__ = "Sydr Dev"
__email__ = "rsd.iz.rosyid@gmail.com"

from ai_website_generator.app import main
from ai_website_generator.providers import (
    BaseProvider,
    ProviderConfig,
    ProviderType,
    get_provider,
    ProviderRegistry,
)
from ai_website_generator.config import get_config, AppConfig, ConfigManager

__all__ = [
    "main",
    "__version__",
    # Providers
    "BaseProvider",
    "ProviderConfig",
    "ProviderType",
    "get_provider",
    "ProviderRegistry",
    # Config
    "get_config",
    "AppConfig",
    "ConfigManager",
]

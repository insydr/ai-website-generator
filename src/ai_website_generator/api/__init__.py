"""
API Module
==========

Provides API integrations for the AI Website Generator.
"""

from ai_website_generator.api.openrouter import OpenRouterClient, APIError

__all__ = ["OpenRouterClient", "APIError"]

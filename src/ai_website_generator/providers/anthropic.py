"""
Anthropic Provider Module
=========================

Implementation for Anthropic Claude API provider.
"""

from typing import Dict, List, Optional

from ai_website_generator.providers.base import (
    BaseProvider,
    ProviderConfig,
    ProviderType,
    ModelInfo,
    APIResponse,
)
from ai_website_generator.constants import SYSTEM_PROMPT


class AnthropicProvider(BaseProvider):
    """
    Anthropic Claude API provider implementation.

    Direct integration with Anthropic's API for Claude models.

    Example:
        config = ProviderConfig(
            provider_type=ProviderType.ANTHROPIC,
            api_key="sk-ant-...",
            model="claude-3-5-sonnet-20241022"
        )
        provider = AnthropicProvider(config)
        response = provider.chat([{"role": "user", "content": "Hello"}])
    """

    PROVIDER_NAME = "Anthropic"
    PROVIDER_TYPE = ProviderType.ANTHROPIC
    DEFAULT_BASE_URL = "https://api.anthropic.com/v1/messages"
    API_KEY_PREFIX = "sk-ant-"

    # Available models
    MODELS = [
        ModelInfo(
            id="claude-3-5-sonnet-20241022",
            name="Claude 3.5 Sonnet",
            context_length="200K",
            description="Most intelligent model, best for complex tasks",
            is_free=False,
            pricing="$3/M input, $15/M output",
        ),
        ModelInfo(
            id="claude-3-5-haiku-20241022",
            name="Claude 3.5 Haiku",
            context_length="200K",
            description="Fastest model, great for simple tasks",
            is_free=False,
            pricing="$0.80/M input, $4/M output",
        ),
        ModelInfo(
            id="claude-3-opus-20240229",
            name="Claude 3 Opus",
            context_length="200K",
            description="Previous generation flagship",
            is_free=False,
            pricing="$15/M input, $75/M output",
        ),
        ModelInfo(
            id="claude-3-sonnet-20240229",
            name="Claude 3 Sonnet",
            context_length="200K",
            description="Balanced performance",
            is_free=False,
            pricing="$3/M input, $15/M output",
        ),
        ModelInfo(
            id="claude-3-haiku-20240307",
            name="Claude 3 Haiku",
            context_length="200K",
            description="Fast and affordable",
            is_free=False,
            pricing="$0.25/M input, $1.25/M output",
        ),
    ]

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for Anthropic API requests."""
        return {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> APIResponse:
        """
        Send chat completion request to Anthropic.

        Args:
            messages: List of message dictionaries
            system_prompt: Optional system prompt override

        Returns:
            APIResponse with result
        """
        # Anthropic uses separate system parameter
        system = system_prompt or SYSTEM_PROMPT

        # Format messages for Anthropic (no system role in messages)
        formatted_messages = []
        for msg in messages:
            if msg["role"] != "system":
                formatted_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "system": system,
            "messages": formatted_messages,
        }

        # Add temperature if not using default
        if self.config.temperature != 0.7:
            payload["temperature"] = self.config.temperature

        url = self.config.base_url or self.DEFAULT_BASE_URL

        return self._make_request(url, payload)

    def get_available_models(self) -> List[ModelInfo]:
        """Get all available models for Anthropic."""
        return self.MODELS

    def _extract_content(self, data: Dict) -> APIResponse:
        """Extract content from Anthropic response."""
        if "content" in data and len(data["content"]) > 0:
            content = data["content"][0].get("text", "")
            usage = data.get("usage", {})

            return APIResponse(
                success=True,
                content=content,
                raw_response=data,
                usage=usage,
            )

        return APIResponse(
            success=False,
            error="Invalid response format from API",
            error_code="INVALID_RESPONSE",
        )

    def _handle_error(self, response) -> APIResponse:
        """Handle Anthropic API errors."""
        status_code = response.status_code

        error_mapping = {
            401: ("Invalid API key. Please check your Anthropic API key.", "INVALID_KEY"),
            429: ("Rate limit exceeded. Please wait a moment and try again.", "RATE_LIMIT"),
            500: ("Anthropic server error. Please try again later.", "SERVER_ERROR"),
            529: ("Service overloaded. Please try again later.", "OVERLOADED"),
        }

        if status_code in error_mapping:
            message, code = error_mapping[status_code]
        else:
            message = f"API Error: {status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    message = error_data["error"].get("message", message)
            except Exception:
                pass
            code = f"HTTP_{status_code}"

        return APIResponse(
            success=False,
            error=message,
            error_code=code,
        )

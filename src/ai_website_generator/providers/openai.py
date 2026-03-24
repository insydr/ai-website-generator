"""
OpenAI Provider Module
======================

Implementation for OpenAI API provider.
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


class OpenAIProvider(BaseProvider):
    """
    OpenAI API provider implementation.

    Direct integration with OpenAI's API for GPT models.

    Example:
        config = ProviderConfig(
            provider_type=ProviderType.OPENAI,
            api_key="sk-...",
            model="gpt-4o"
        )
        provider = OpenAIProvider(config)
        response = provider.chat([{"role": "user", "content": "Hello"}])
    """

    PROVIDER_NAME = "OpenAI"
    PROVIDER_TYPE = ProviderType.OPENAI
    DEFAULT_BASE_URL = "https://api.openai.com/v1/chat/completions"
    API_KEY_PREFIX = "sk-"

    # Available models
    MODELS = [
        ModelInfo(
            id="gpt-4o",
            name="GPT-4o",
            context_length="128K",
            description="Most capable GPT-4 model, fast and intelligent",
            is_free=False,
            pricing="$5/M input, $15/M output",
        ),
        ModelInfo(
            id="gpt-4o-mini",
            name="GPT-4o Mini",
            context_length="128K",
            description="Affordable and fast for simple tasks",
            is_free=False,
            pricing="$0.15/M input, $0.60/M output",
        ),
        ModelInfo(
            id="gpt-4-turbo",
            name="GPT-4 Turbo",
            context_length="128K",
            description="Previous generation flagship",
            is_free=False,
            pricing="$10/M input, $30/M output",
        ),
        ModelInfo(
            id="gpt-3.5-turbo",
            name="GPT-3.5 Turbo",
            context_length="16K",
            description="Fast and affordable",
            is_free=False,
            pricing="$0.50/M input, $1.50/M output",
        ),
        ModelInfo(
            id="o1-preview",
            name="o1 Preview",
            context_length="128K",
            description="Advanced reasoning model",
            is_free=False,
            pricing="$15/M input, $60/M output",
        ),
        ModelInfo(
            id="o1-mini",
            name="o1 Mini",
            context_length="128K",
            description="Fast reasoning model",
            is_free=False,
            pricing="$3/M input, $12/M output",
        ),
    ]

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for OpenAI API requests."""
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> APIResponse:
        """
        Send chat completion request to OpenAI.

        Args:
            messages: List of message dictionaries
            system_prompt: Optional system prompt override

        Returns:
            APIResponse with result
        """
        formatted_messages = self.format_messages(messages, system_prompt or SYSTEM_PROMPT)

        payload = {
            "model": self.config.model,
            "messages": formatted_messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        # Use custom base URL if provided
        url = self.config.base_url or self.DEFAULT_BASE_URL

        return self._make_request(url, payload)

    def get_available_models(self) -> List[ModelInfo]:
        """Get all available models for OpenAI."""
        return self.MODELS

    def _extract_content(self, data: Dict) -> APIResponse:
        """Extract content from OpenAI response."""
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
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
        """Handle OpenAI API errors."""
        status_code = response.status_code

        error_mapping = {
            401: ("Invalid API key. Please check your OpenAI API key.", "INVALID_KEY"),
            429: ("Rate limit exceeded. Please wait a moment and try again.", "RATE_LIMIT"),
            500: ("OpenAI server error. Please try again later.", "SERVER_ERROR"),
            503: ("Service unavailable. Please try again later.", "SERVICE_UNAVAILABLE"),
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

"""
Groq Provider Module
====================

Implementation for Groq API provider (ultra-fast inference).
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


class GroqProvider(BaseProvider):
    """
    Groq API provider implementation.

    Groq provides ultra-fast inference with LPU technology.
    Offers both free and paid tiers.

    Example:
        config = ProviderConfig(
            provider_type=ProviderType.GROQ,
            api_key="gsk_...",
            model="llama-3.3-70b-versatile"
        )
        provider = GroqProvider(config)
        response = provider.chat([{"role": "user", "content": "Hello"}])
    """

    PROVIDER_NAME = "Groq"
    PROVIDER_TYPE = ProviderType.GROQ
    DEFAULT_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY_PREFIX = "gsk_"

    # Available models
    MODELS = [
        ModelInfo(
            id="llama-3.3-70b-versatile",
            name="Llama 3.3 70B Versatile",
            context_length="128K",
            description="Most capable Llama model on Groq",
            is_free=True,
            pricing="Free tier available",
        ),
        ModelInfo(
            id="llama-3.1-8b-instant",
            name="Llama 3.1 8B Instant",
            context_length="128K",
            description="Ultra-fast responses",
            is_free=True,
            pricing="Free tier available",
        ),
        ModelInfo(
            id="llama-3.2-1b-preview",
            name="Llama 3.2 1B Preview",
            context_length="128K",
            description="Fastest model, good for simple tasks",
            is_free=True,
            pricing="Free tier available",
        ),
        ModelInfo(
            id="llama-3.2-3b-preview",
            name="Llama 3.2 3B Preview",
            context_length="128K",
            description="Balanced speed and capability",
            is_free=True,
            pricing="Free tier available",
        ),
        ModelInfo(
            id="mixtral-8x7b-32768",
            name="Mixtral 8x7B",
            context_length="32K",
            description="MoE model with great quality",
            is_free=True,
            pricing="Free tier available",
        ),
        ModelInfo(
            id="gemma2-9b-it",
            name="Gemma 2 9B",
            context_length="8K",
            description="Google's efficient model",
            is_free=True,
            pricing="Free tier available",
        ),
        ModelInfo(
            id="deepseek-r1-distill-llama-70b",
            name="DeepSeek R1 Distill Llama 70B",
            context_length="128K",
            description="Reasoning model",
            is_free=True,
            pricing="Free tier available",
        ),
    ]

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for Groq API requests."""
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
        Send chat completion request to Groq.

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

        url = self.config.base_url or self.DEFAULT_BASE_URL

        return self._make_request(url, payload)

    def get_available_models(self) -> List[ModelInfo]:
        """Get all available models for Groq."""
        return self.MODELS

    def _extract_content(self, data: Dict) -> APIResponse:
        """Extract content from Groq response (OpenAI-compatible format)."""
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
        """Handle Groq API errors."""
        status_code = response.status_code

        error_mapping = {
            401: ("Invalid API key. Please check your Groq API key.", "INVALID_KEY"),
            429: ("Rate limit exceeded. Please wait a moment and try again.", "RATE_LIMIT"),
            500: ("Groq server error. Please try again later.", "SERVER_ERROR"),
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

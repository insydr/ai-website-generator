"""
OpenRouter Provider Module
==========================

Implementation for OpenRouter API provider.
"""

from typing import Dict, List, Optional

from ai_website_generator.providers.base import (
    BaseProvider,
    ProviderConfig,
    ProviderType,
    ModelInfo,
    APIResponse,
)
from ai_website_generator.constants import SYSTEM_PROMPT, API_REFERER, API_TITLE


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter API provider implementation.

    OpenRouter provides unified access to multiple LLM providers with
    competitive pricing and free tier options.

    Example:
        config = ProviderConfig(
            provider_type=ProviderType.OPENROUTER,
            api_key="sk-or-...",
            model="meta-llama/llama-3.2-3b-instruct:free"
        )
        provider = OpenRouterProvider(config)
        response = provider.chat([{"role": "user", "content": "Hello"}])
    """

    PROVIDER_NAME = "OpenRouter"
    PROVIDER_TYPE = ProviderType.OPENROUTER
    DEFAULT_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    API_KEY_PREFIX = "sk-or-"

    # Available free models on OpenRouter
    FREE_MODELS = [
        ModelInfo(
            id="meta-llama/llama-3.2-3b-instruct:free",
            name="Llama 3.2 3B (Free)",
            context_length="128K",
            description="Fast and capable for most tasks",
            is_free=True,
        ),
        ModelInfo(
            id="meta-llama/llama-3.2-1b-instruct:free",
            name="Llama 3.2 1B (Free)",
            context_length="128K",
            description="Ultra-fast, best for simple sites",
            is_free=True,
        ),
        ModelInfo(
            id="meta-llama/llama-3.1-8b-instruct:free",
            name="Llama 3.1 8B (Free)",
            context_length="128K",
            description="Balanced speed and quality",
            is_free=True,
        ),
        ModelInfo(
            id="qwen/qwen-2-7b-instruct:free",
            name="Qwen 2 7B (Free)",
            context_length="32K",
            description="Good for complex designs",
            is_free=True,
        ),
        ModelInfo(
            id="google/gemma-2-9b-it:free",
            name="Gemma 2 9B (Free)",
            context_length="8K",
            description="High quality output",
            is_free=True,
        ),
        ModelInfo(
            id="mistralai/mistral-7b-instruct:free",
            name="Mistral 7B (Free)",
            context_length="32K",
            description="Fast and capable",
            is_free=True,
        ),
        ModelInfo(
            id="deepseek/deepseek-r1:free",
            name="DeepSeek R1 (Free)",
            context_length="128K",
            description="Complex reasoning",
            is_free=True,
        ),
        ModelInfo(
            id="deepseek/deepseek-chat:free",
            name="DeepSeek Chat (Free)",
            context_length="128K",
            description="Conversational AI",
            is_free=True,
        ),
    ]

    # Popular paid models
    PAID_MODELS = [
        ModelInfo(
            id="anthropic/claude-3.5-sonnet",
            name="Claude 3.5 Sonnet",
            context_length="200K",
            description="Best for complex tasks",
            is_free=False,
            pricing="$3/M tokens",
        ),
        ModelInfo(
            id="openai/gpt-4o",
            name="GPT-4o",
            context_length="128K",
            description="OpenAI's flagship model",
            is_free=False,
            pricing="$5/M tokens",
        ),
        ModelInfo(
            id="openai/gpt-4o-mini",
            name="GPT-4o Mini",
            context_length="128K",
            description="Fast and affordable",
            is_free=False,
            pricing="$0.15/M tokens",
        ),
        ModelInfo(
            id="google/gemini-pro-1.5",
            name="Gemini Pro 1.5",
            context_length="1M",
            description="Large context window",
            is_free=False,
            pricing="$3.5/M tokens",
        ),
    ]

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for OpenRouter API requests."""
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "HTTP-Referer": API_REFERER,
            "X-Title": API_TITLE,
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> APIResponse:
        """
        Send chat completion request to OpenRouter.

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

        return self._make_request(self.DEFAULT_BASE_URL, payload)

    def get_available_models(self) -> List[ModelInfo]:
        """Get all available models for OpenRouter."""
        return self.FREE_MODELS + self.PAID_MODELS

    def get_free_models(self) -> List[ModelInfo]:
        """Get only free models."""
        return self.FREE_MODELS

    def _extract_content(self, data: Dict) -> APIResponse:
        """Extract content from OpenRouter response."""
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
        """Handle OpenRouter API errors."""
        status_code = response.status_code

        error_mapping = {
            401: ("Invalid API key. Please check your OpenRouter API key.", "INVALID_KEY"),
            402: ("Insufficient credits. Please add credits to your OpenRouter account.", "INSUFFICIENT_CREDITS"),
            429: ("Rate limit exceeded. Please wait a moment and try again.", "RATE_LIMIT"),
            503: ("Model is currently overloaded. Please try a different model.", "MODEL_OVERLOADED"),
        }

        if status_code in error_mapping:
            message, code = error_mapping[status_code]
        else:
            message = f"API Error: {status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    message = f"{message} - {error_data['error'].get('message', 'Unknown error')}"
            except Exception:
                pass
            code = f"HTTP_{status_code}"

        return APIResponse(
            success=False,
            error=message,
            error_code=code,
        )

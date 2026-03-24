"""
Custom Provider Module
======================

Implementation for custom API endpoints (BYOK - Bring Your Own Key).
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


class CustomProvider(BaseProvider):
    """
    Custom API provider for user-defined endpoints.

    Allows users to connect to any OpenAI-compatible API endpoint
    or custom implementations.

    Example:
        config = ProviderConfig(
            provider_type=ProviderType.CUSTOM,
            api_key="your-api-key",
            model="your-model-name",
            base_url="https://your-api-endpoint.com/v1/chat/completions"
        )
        provider = CustomProvider(config)
        response = provider.chat([{"role": "user", "content": "Hello"}])
    """

    PROVIDER_NAME = "Custom API"
    PROVIDER_TYPE = ProviderType.CUSTOM
    DEFAULT_BASE_URL = ""  # Must be provided by user
    API_KEY_PREFIX = ""

    def _validate_config(self) -> None:
        """Validate custom provider configuration."""
        if not self.config.model:
            raise ValueError("Model name must be specified for custom provider")

        # API key might not be required for some local deployments
        # if not self.config.api_key:
        #     raise ValueError("API key is required")

        if not self.base_url:
            raise ValueError(
                "Base URL is required for custom provider. "
                "Please provide the API endpoint URL."
            )

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for custom API requests."""
        headers = {
            "Content-Type": "application/json",
        }

        # Add authorization if API key is provided
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        # Add any extra headers from config
        headers.update(self.config.extra_headers)

        return headers

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> APIResponse:
        """
        Send chat completion request to custom endpoint.

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

        # Add any extra parameters from config
        payload.update(self.config.extra_params)

        return self._make_request(self.base_url, payload)

    def get_available_models(self) -> List[ModelInfo]:
        """
        Get available models for custom provider.

        Returns a placeholder since models are user-defined.
        """
        return [
            ModelInfo(
                id=self.config.model,
                name=f"Custom: {self.config.model}",
                context_length="Unknown",
                description="User-defined model",
                is_free=False,
            )
        ]

    def _extract_content(self, data: Dict) -> APIResponse:
        """
        Extract content from custom API response.

        Tries OpenAI-compatible format first, then falls back to common formats.
        """
        # Try OpenAI-compatible format
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            if "message" in choice:
                content = choice["message"].get("content", "")
            elif "text" in choice:
                content = choice["text"]
            else:
                content = str(choice)

            usage = data.get("usage", {})

            return APIResponse(
                success=True,
                content=content,
                raw_response=data,
                usage=usage,
            )

        # Try Anthropic-like format
        if "content" in data and len(data["content"]) > 0:
            content = data["content"][0].get("text", "")
            usage = data.get("usage", {})

            return APIResponse(
                success=True,
                content=content,
                raw_response=data,
                usage=usage,
            )

        # Try direct text response
        if "text" in data:
            return APIResponse(
                success=True,
                content=data["text"],
                raw_response=data,
            )

        # Try response field
        if "response" in data:
            return APIResponse(
                success=True,
                content=str(data["response"]),
                raw_response=data,
            )

        return APIResponse(
            success=False,
            error="Could not extract content from response. Please check the API format.",
            error_code="PARSE_ERROR",
        )

    def _handle_error(self, response) -> APIResponse:
        """Handle custom API errors."""
        status_code = response.status_code

        error_mapping = {
            401: ("Authentication failed. Please check your API key.", "INVALID_KEY"),
            403: ("Access forbidden. Please check your permissions.", "FORBIDDEN"),
            404: ("Endpoint not found. Please check the URL.", "NOT_FOUND"),
            429: ("Rate limit exceeded. Please wait and try again.", "RATE_LIMIT"),
            500: ("Server error. Please try again later.", "SERVER_ERROR"),
            502: ("Bad gateway. The server might be down.", "BAD_GATEWAY"),
            503: ("Service unavailable. Please try again later.", "SERVICE_UNAVAILABLE"),
        }

        if status_code in error_mapping:
            message, code = error_mapping[status_code]
        else:
            message = f"API Error: {status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    if isinstance(error_data["error"], str):
                        message = error_data["error"]
                    elif isinstance(error_data["error"], dict):
                        message = error_data["error"].get("message", message)
            except Exception:
                pass
            code = f"HTTP_{status_code}"

        return APIResponse(
            success=False,
            error=message,
            error_code=code,
        )

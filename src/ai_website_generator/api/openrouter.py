"""
OpenRouter API Client
=====================

Handles communication with the OpenRouter API.
"""

import requests
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum

from ai_website_generator.constants import (
    OPENROUTER_API_URL,
    SYSTEM_PROMPT,
    API_TIMEOUT,
)


class APIErrorType(Enum):
    """Types of API errors."""

    INVALID_KEY = "invalid_key"
    INSUFFICIENT_CREDITS = "insufficient_credits"
    RATE_LIMIT = "rate_limit"
    MODEL_OVERLOADED = "model_overloaded"
    TIMEOUT = "timeout"
    CONNECTION = "connection"
    UNKNOWN = "unknown"


@dataclass
class APIError(Exception):
    """Custom exception for API errors."""

    message: str
    error_type: APIErrorType
    status_code: Optional[int] = None

    def __str__(self) -> str:
        return self.message


@dataclass
class APIResponse:
    """API response data class."""

    success: bool
    content: Optional[str] = None
    error: Optional[APIError] = None
    raw_response: Optional[Dict] = None


class OpenRouterClient:
    """
    Client for OpenRouter API communication.

    Handles authentication, request formatting, and response parsing.

    Example:
        client = OpenRouterClient(api_key="sk-or-...")
        response = client.chat(messages=[...])
        if response.success:
            print(response.content)
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        timeout: int = API_TIMEOUT,
    ):
        """
        Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key
            model: Model ID to use
            temperature: Generation temperature (0.0 - 2.0)
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://ai-website-generator.streamlit.app",
            "X-Title": "AI Website Generator",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> APIResponse:
        """
        Send a chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt override

        Returns:
            APIResponse with success status and content or error
        """
        # Prepare messages with system prompt
        formatted_messages = []

        if system_prompt is None:
            system_prompt = SYSTEM_PROMPT

        formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)

        # Prepare payload
        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            response = requests.post(
                OPENROUTER_API_URL,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )

            return self._parse_response(response)

        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                error=APIError(
                    message="Request timed out. The model might be taking too long to respond.",
                    error_type=APIErrorType.TIMEOUT,
                ),
            )

        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                error=APIError(
                    message="Connection error. Please check your internet connection.",
                    error_type=APIErrorType.CONNECTION,
                ),
            )

        except Exception as e:
            return APIResponse(
                success=False,
                error=APIError(
                    message=f"Unexpected error: {str(e)}",
                    error_type=APIErrorType.UNKNOWN,
                ),
            )

    def _parse_response(self, response: requests.Response) -> APIResponse:
        """
        Parse API response and handle errors.

        Args:
            response: requests Response object

        Returns:
            APIResponse with parsed data
        """
        status_code = response.status_code

        # Success
        if status_code == 200:
            try:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    return APIResponse(
                        success=True,
                        content=content,
                        raw_response=data,
                    )
                else:
                    return APIResponse(
                        success=False,
                        error=APIError(
                            message="Invalid response format from API",
                            error_type=APIErrorType.UNKNOWN,
                            status_code=status_code,
                        ),
                    )
            except ValueError:
                return APIResponse(
                    success=False,
                    error=APIError(
                        message="Failed to parse API response",
                        error_type=APIErrorType.UNKNOWN,
                        status_code=status_code,
                    ),
                )

        # Handle error status codes
        error_mapping = {
            401: (
                "Invalid API key. Please check your OpenRouter API key.",
                APIErrorType.INVALID_KEY,
            ),
            402: (
                "Insufficient credits. Please add credits to your OpenRouter account.",
                APIErrorType.INSUFFICIENT_CREDITS,
            ),
            429: (
                "Rate limit exceeded. Please wait a moment and try again.",
                APIErrorType.RATE_LIMIT,
            ),
            503: (
                "Model is currently overloaded. Please try a different model or wait.",
                APIErrorType.MODEL_OVERLOADED,
            ),
        }

        if status_code in error_mapping:
            message, error_type = error_mapping[status_code]
        else:
            message = f"API Error: {status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    message = f"{message} - {error_data['error'].get('message', 'Unknown error')}"
            except ValueError:
                pass
            error_type = APIErrorType.UNKNOWN

        return APIResponse(
            success=False,
            error=APIError(
                message=message,
                error_type=error_type,
                status_code=status_code,
            ),
        )

    def generate_website(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> APIResponse:
        """
        Generate website from natural language prompt.

        Args:
            prompt: User's website description
            conversation_history: Previous messages for context

        Returns:
            APIResponse with generated content
        """
        messages = conversation_history or []
        messages.append({"role": "user", "content": prompt})

        return self.chat(messages)

"""
Base Provider Module
====================

Provides base class and common interfaces for AI providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import requests


class ProviderType(Enum):
    """Supported AI provider types."""

    OPENROUTER = "openrouter"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    CUSTOM = "custom"


@dataclass
class ModelInfo:
    """Information about an AI model."""

    id: str
    name: str
    context_length: str = "Unknown"
    description: str = ""
    is_free: bool = False
    pricing: str = ""


@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""

    provider_type: ProviderType
    api_key: str
    model: str
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000
    timeout: int = 120
    extra_headers: Dict[str, str] = field(default_factory=dict)
    extra_params: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_configured(self) -> bool:
        """Check if provider is properly configured."""
        return bool(self.api_key and self.model)


@dataclass
class APIResponse:
    """Standardized API response."""

    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    raw_response: Optional[Dict] = None
    usage: Optional[Dict[str, int]] = None


class BaseProvider(ABC):
    """
    Abstract base class for AI providers.

    All provider implementations must inherit from this class and implement
    the required methods.

    Example:
        class MyProvider(BaseProvider):
            def chat(self, messages: List[Dict]) -> APIResponse:
                # Implementation
                pass
    """

    # Provider metadata (override in subclass)
    PROVIDER_NAME: str = "Base Provider"
    PROVIDER_TYPE: ProviderType = ProviderType.CUSTOM
    DEFAULT_BASE_URL: str = ""
    API_KEY_PREFIX: str = ""

    def __init__(self, config: ProviderConfig):
        """
        Initialize provider with configuration.

        Args:
            config: Provider configuration
        """
        self.config = config
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate provider configuration."""
        if not self.config.api_key:
            raise ValueError(f"API key is required for {self.PROVIDER_NAME}")

        if not self.config.model:
            raise ValueError("Model must be specified")

    @property
    def base_url(self) -> str:
        """Get base URL for API requests."""
        return self.config.base_url or self.DEFAULT_BASE_URL

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Content-Type": "application/json",
            **self.config.extra_headers,
        }

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> APIResponse:
        """
        Send chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt override

        Returns:
            APIResponse with result
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[ModelInfo]:
        """
        Get list of available models for this provider.

        Returns:
            List of ModelInfo objects
        """
        pass

    def _make_request(
        self,
        url: str,
        payload: Dict,
        headers: Optional[Dict] = None,
    ) -> APIResponse:
        """
        Make HTTP request to API.

        Args:
            url: API endpoint URL
            payload: Request body
            headers: Optional custom headers

        Returns:
            APIResponse with result
        """
        request_headers = headers or self.headers

        try:
            response = requests.post(
                url,
                json=payload,
                headers=request_headers,
                timeout=self.config.timeout,
            )

            return self._parse_response(response)

        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                error="Request timed out. The model might be taking too long to respond.",
                error_code="TIMEOUT",
            )

        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                error="Connection error. Please check your internet connection.",
                error_code="CONNECTION_ERROR",
            )

        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Unexpected error: {str(e)}",
                error_code="UNKNOWN",
            )

    def _parse_response(self, response: requests.Response) -> APIResponse:
        """
        Parse API response.

        Args:
            response: requests Response object

        Returns:
            APIResponse with parsed data
        """
        status_code = response.status_code

        if status_code == 200:
            try:
                data = response.json()
                return self._extract_content(data)
            except ValueError:
                return APIResponse(
                    success=False,
                    error="Failed to parse API response",
                    error_code="PARSE_ERROR",
                )

        return self._handle_error(response)

    @abstractmethod
    def _extract_content(self, data: Dict) -> APIResponse:
        """
        Extract content from successful API response.

        Args:
            data: Parsed JSON response

        Returns:
            APIResponse with content
        """
        pass

    @abstractmethod
    def _handle_error(self, response: requests.Response) -> APIResponse:
        """
        Handle API error response.

        Args:
            response: requests Response object

        Returns:
            APIResponse with error details
        """
        pass

    def format_messages(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        Format messages for API request.

        Args:
            messages: List of message dictionaries
            system_prompt: Optional system prompt

        Returns:
            Formatted messages list
        """
        formatted = []

        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})

        formatted.extend(messages)
        return formatted

"""
Session Manager Module
======================

Manages Streamlit session state for the application.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime

from ai_website_generator.constants import DEFAULT_PROVIDER, DEFAULT_MODEL


@dataclass
class ChatMessage:
    """Represents a chat message."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


class SessionManager:
    """
    Manages application session state.

    Provides a clean interface for interacting with Streamlit's session_state.

    Example:
        session = get_session_manager()
        session.add_message("user", "Create a landing page")
        messages = session.get_messages()
    """

    # Session state keys
    KEY_CHAT_HISTORY = "chat_history"
    KEY_GENERATED_CODE = "generated_code"
    KEY_API_KEY = "api_key"
    KEY_PROVIDER_TYPE = "provider_type"
    KEY_SELECTED_MODEL = "selected_model"
    KEY_CUSTOM_BASE_URL = "custom_base_url"
    KEY_SHOW_CODE = "show_code"
    KEY_IS_LOADING = "is_loading"
    KEY_CUSTOM_MODEL_INPUT = "custom_model_input"

    def __init__(self):
        """Initialize session manager."""
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Initialize all session state variables."""
        try:
            import streamlit as st

            if self.KEY_CHAT_HISTORY not in st.session_state:
                st.session_state[self.KEY_CHAT_HISTORY] = []

            if self.KEY_GENERATED_CODE not in st.session_state:
                st.session_state[self.KEY_GENERATED_CODE] = None

            if self.KEY_API_KEY not in st.session_state:
                st.session_state[self.KEY_API_KEY] = ""

            if self.KEY_PROVIDER_TYPE not in st.session_state:
                st.session_state[self.KEY_PROVIDER_TYPE] = DEFAULT_PROVIDER

            if self.KEY_SELECTED_MODEL not in st.session_state:
                st.session_state[self.KEY_SELECTED_MODEL] = DEFAULT_MODEL

            if self.KEY_CUSTOM_BASE_URL not in st.session_state:
                st.session_state[self.KEY_CUSTOM_BASE_URL] = ""

            if self.KEY_SHOW_CODE not in st.session_state:
                st.session_state[self.KEY_SHOW_CODE] = False

            if self.KEY_IS_LOADING not in st.session_state:
                st.session_state[self.KEY_IS_LOADING] = False

            if self.KEY_CUSTOM_MODEL_INPUT not in st.session_state:
                st.session_state[self.KEY_CUSTOM_MODEL_INPUT] = ""

        except ImportError:
            # Fallback for non-Streamlit usage (e.g., tests)
            self._fallback_state = {
                self.KEY_CHAT_HISTORY: [],
                self.KEY_GENERATED_CODE: None,
                self.KEY_API_KEY: "",
                self.KEY_PROVIDER_TYPE: DEFAULT_PROVIDER,
                self.KEY_SELECTED_MODEL: DEFAULT_MODEL,
                self.KEY_CUSTOM_BASE_URL: "",
                self.KEY_SHOW_CODE: False,
                self.KEY_IS_LOADING: False,
                self.KEY_CUSTOM_MODEL_INPUT: "",
            }

    def _get_state(self, key: str, default: Any = None) -> Any:
        """Get value from session state."""
        try:
            import streamlit as st

            return st.session_state.get(key, default)
        except ImportError:
            return self._fallback_state.get(key, default)

    def _set_state(self, key: str, value: Any) -> None:
        """Set value in session state."""
        try:
            import streamlit as st

            st.session_state[key] = value
        except ImportError:
            self._fallback_state[key] = value

    # =========================================================================
    # Chat History Management
    # =========================================================================

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to chat history.

        Args:
            role: "user" or "assistant"
            content: Message content
        """
        messages = self._get_state(self.KEY_CHAT_HISTORY, [])
        messages.append(ChatMessage(role=role, content=content))
        self._set_state(self.KEY_CHAT_HISTORY, messages)

    def get_messages(self) -> List[ChatMessage]:
        """Get all chat messages."""
        return self._get_state(self.KEY_CHAT_HISTORY, [])

    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """Get messages formatted for API calls."""
        messages = self.get_messages()
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def clear_chat(self) -> None:
        """Clear all chat history."""
        self._set_state(self.KEY_CHAT_HISTORY, [])
        self._set_state(self.KEY_GENERATED_CODE, None)
        self._set_state(self.KEY_SHOW_CODE, False)

    # =========================================================================
    # Generated Code Management
    # =========================================================================

    def set_generated_code(self, code: str) -> None:
        """
        Set the generated HTML code.

        Args:
            code: HTML code string
        """
        self._set_state(self.KEY_GENERATED_CODE, code)

    def get_generated_code(self) -> Optional[str]:
        """Get the generated HTML code."""
        return self._get_state(self.KEY_GENERATED_CODE)

    def has_generated_code(self) -> bool:
        """Check if there is generated code."""
        return bool(self._get_state(self.KEY_GENERATED_CODE))

    # =========================================================================
    # Provider Configuration
    # =========================================================================

    def set_provider_type(self, provider_type: str) -> None:
        """
        Set the provider type.

        Args:
            provider_type: Provider type string (openrouter, openai, etc.)
        """
        self._set_state(self.KEY_PROVIDER_TYPE, provider_type)

    def get_provider_type(self) -> str:
        """Get the provider type."""
        return self._get_state(self.KEY_PROVIDER_TYPE, DEFAULT_PROVIDER)

    def set_api_key(self, api_key: str) -> None:
        """
        Set the API key.

        Args:
            api_key: API key for the provider
        """
        self._set_state(self.KEY_API_KEY, api_key)

    def get_api_key(self) -> Optional[str]:
        """Get the API key."""
        key = self._get_state(self.KEY_API_KEY)
        return key if key else None

    def set_selected_model(self, model_id: str) -> None:
        """
        Set the selected model.

        Args:
            model_id: Model identifier
        """
        self._set_state(self.KEY_SELECTED_MODEL, model_id)

    def get_selected_model(self) -> str:
        """Get the selected model ID."""
        return self._get_state(self.KEY_SELECTED_MODEL, DEFAULT_MODEL)

    def set_custom_model(self, model: str) -> None:
        """
        Set custom model name.

        Args:
            model: Custom model name
        """
        self._set_state(self.KEY_CUSTOM_MODEL_INPUT, model)

    def get_custom_model(self) -> str:
        """Get custom model name."""
        return self._get_state(self.KEY_CUSTOM_MODEL_INPUT, "")

    def set_custom_base_url(self, url: str) -> None:
        """
        Set custom base URL.

        Args:
            url: Custom API endpoint URL
        """
        self._set_state(self.KEY_CUSTOM_BASE_URL, url)

    def get_custom_base_url(self) -> str:
        """Get custom base URL."""
        return self._get_state(self.KEY_CUSTOM_BASE_URL, "")

    # =========================================================================
    # UI State Management
    # =========================================================================

    def toggle_show_code(self) -> None:
        """Toggle code visibility."""
        current = self._get_state(self.KEY_SHOW_CODE, False)
        self._set_state(self.KEY_SHOW_CODE, not current)

    def is_showing_code(self) -> bool:
        """Check if code is being shown."""
        return self._get_state(self.KEY_SHOW_CODE, False)

    def set_loading(self, is_loading: bool) -> None:
        """Set loading state."""
        self._set_state(self.KEY_IS_LOADING, is_loading)

    def is_loading(self) -> bool:
        """Check if app is in loading state."""
        return self._get_state(self.KEY_IS_LOADING, False)

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def get_provider_config_dict(self) -> Dict[str, Any]:
        """
        Get all provider-related settings as a dictionary.

        Returns:
            Dictionary with provider configuration
        """
        return {
            "provider_type": self.get_provider_type(),
            "api_key": self.get_api_key(),
            "model": self.get_selected_model(),
            "custom_model": self.get_custom_model(),
            "base_url": self.get_custom_base_url(),
        }


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.

    Returns:
        SessionManager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

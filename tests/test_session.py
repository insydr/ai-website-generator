"""
Tests for Session Manager Module
================================

Unit tests for the session state management.
"""

import pytest
from datetime import datetime

from ai_website_generator.utils.session import (
    SessionManager,
    ChatMessage,
    get_session_manager,
)


class TestChatMessage:
    """Tests for ChatMessage dataclass."""

    def test_create_message(self):
        """Test creating a chat message."""
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert isinstance(msg.timestamp, datetime)

    def test_message_with_timestamp(self):
        """Test creating message with specific timestamp."""
        ts = datetime(2024, 1, 1, 12, 0, 0)
        msg = ChatMessage(role="assistant", content="Hi", timestamp=ts)
        assert msg.timestamp == ts


class TestSessionManager:
    """Tests for SessionManager class."""

    def test_singleton_pattern(self):
        """Test that get_session_manager returns singleton."""
        manager1 = get_session_manager()
        manager2 = get_session_manager()
        # They should be the same instance
        assert id(manager1) == id(manager2)

    def test_add_message(self):
        """Test adding messages to history."""
        manager = SessionManager()
        manager.clear_chat()  # Start fresh

        manager.add_message("user", "Test message")
        messages = manager.get_messages()

        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Test message"

    def test_get_messages_for_api(self):
        """Test getting messages formatted for API."""
        manager = SessionManager()
        manager.clear_chat()

        manager.add_message("user", "Hello")
        manager.add_message("assistant", "Hi there!")

        api_messages = manager.get_messages_for_api()

        assert len(api_messages) == 2
        assert api_messages[0] == {"role": "user", "content": "Hello"}
        assert api_messages[1] == {"role": "assistant", "content": "Hi there!"}

    def test_clear_chat(self):
        """Test clearing chat history."""
        manager = SessionManager()
        manager.add_message("user", "Message 1")
        manager.add_message("assistant", "Message 2")

        manager.clear_chat()

        assert len(manager.get_messages()) == 0
        assert manager.get_generated_code() is None

    def test_generated_code(self):
        """Test setting and getting generated code."""
        manager = SessionManager()
        manager.clear_chat()

        html = "<html><body>Test</body></html>"
        manager.set_generated_code(html)

        assert manager.get_generated_code() == html
        assert manager.has_generated_code() is True

    def test_api_key(self):
        """Test setting and getting API key."""
        manager = SessionManager()

        manager.set_api_key("test-key-123")
        assert manager.get_api_key() == "test-key-123"

    def test_model_selection(self):
        """Test setting and getting selected model."""
        manager = SessionManager()

        manager.set_selected_model("test-model-id")
        assert manager.get_selected_model() == "test-model-id"

    def test_toggle_show_code(self):
        """Test toggling code visibility."""
        manager = SessionManager()

        initial_state = manager.is_showing_code()
        manager.toggle_show_code()
        assert manager.is_showing_code() != initial_state

        manager.toggle_show_code()
        assert manager.is_showing_code() == initial_state

    def test_loading_state(self):
        """Test loading state management."""
        manager = SessionManager()

        manager.set_loading(True)
        assert manager.is_loading() is True

        manager.set_loading(False)
        assert manager.is_loading() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
AI Website Generator - Main Application
========================================

Main entry point for the AI Website Generator application.
This module orchestrates all components and handles the main application flow.
"""

import streamlit as st
from typing import Optional

from ai_website_generator.constants import APP_TITLE, APP_ICON, DEFAULT_MODEL_ID
from ai_website_generator.config import get_config
from ai_website_generator.api.openrouter import OpenRouterClient
from ai_website_generator.utils.session import SessionManager, get_session_manager
from ai_website_generator.utils.code_extractor import extract_html_code
from ai_website_generator.ui.styles import apply_custom_css
from ai_website_generator.ui.components import (
    render_title,
    render_chat_message,
    render_example_prompts,
    render_preview_panel,
    render_sidebar,
    render_footer,
    render_error_message,
    render_success_message,
    render_warning_message,
)


class AIWebsiteGenerator:
    """
    Main application class for AI Website Generator.

    Handles the application lifecycle, user interactions, and coordination
    between different components.

    Example:
        app = AIWebsiteGenerator()
        app.run()
    """

    def __init__(self):
        """Initialize the application."""
        self.session: SessionManager = get_session_manager()
        self._setup_page_config()
        apply_custom_css()

    def _setup_page_config(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=APP_TITLE,
            page_icon=APP_ICON,
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def _get_api_key(self) -> Optional[str]:
        """Get API key from session or config."""
        # First check session state
        session_key = self.session.get_api_key()
        if session_key:
            return session_key

        # Then check config (secrets/env)
        config = get_config()
        return config.api_key

    def _has_secret_key(self) -> bool:
        """Check if API key exists in secrets."""
        try:
            import streamlit as st

            return hasattr(st, "secrets") and "openrouter_api_key" in st.secrets
        except Exception:
            return False

    def _handle_generation(self, prompt: str) -> None:
        """
        Handle website generation request.

        Args:
            prompt: User's website description
        """
        api_key = self._get_api_key()

        if not api_key:
            render_warning_message("Please enter your OpenRouter API key in the sidebar.")
            return

        if not prompt.strip():
            render_warning_message("Please enter a description for your website.")
            return

        # Add user message to history
        self.session.add_message("user", prompt)

        # Get configuration
        config = get_config(api_key)
        model_id = self.session.get_selected_model() or DEFAULT_MODEL_ID

        # Create API client
        client = OpenRouterClient(
            api_key=api_key,
            model=model_id,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

        # Show loading state
        with st.spinner("🎨 Generating your website... This may take a moment."):
            # Get conversation history for context
            history = self.session.get_messages_for_api()

            # Make API call
            response = client.generate_website(prompt, conversation_history=history)

        if response.success:
            # Extract HTML code
            html_code = extract_html_code(response.content)

            if html_code:
                # Add AI response to history
                self.session.add_message("assistant", response.content)

                # Store generated code
                self.session.set_generated_code(html_code)

                render_success_message("Website generated successfully!")
                st.rerun()
            else:
                render_error_message("Could not extract HTML code from the response. Please try again.")
                st.code(response.content, language="text")
        else:
            if response.error:
                render_error_message(response.error.message)

    def _handle_example_click(self, prompt: str) -> None:
        """Handle example prompt click."""
        st.session_state["prompt_input"] = prompt

    def _render_chat_section(self) -> None:
        """Render the chat interface section."""
        st.markdown("### 💬 Chat")

        # Chat history container
        with st.container():
            messages = self.session.get_messages()

            if messages:
                for message in messages:
                    render_chat_message(message.role, message.content)
            else:
                render_example_prompts(on_click=self._handle_example_click)

        st.markdown("---")

        # Input area
        default_prompt = st.session_state.get("prompt_input", "")
        if "prompt_input" in st.session_state:
            # Clear after use
            del st.session_state["prompt_input"]

        user_prompt = st.text_area(
            "Describe your website:",
            value=default_prompt,
            height=100,
            placeholder="E.g., Create a modern landing page for a fitness app with a hero section, features grid, testimonials, and a contact form. Use a dark theme with neon accents.",
            key="prompt_text_area",
        )

        # Buttons
        col_btn1, col_btn2 = st.columns([3, 1])

        with col_btn1:
            generate_btn = st.button("✨ Generate Website", type="primary", use_container_width=True)

        with col_btn2:
            show_code_btn = st.button("📝 Code", use_container_width=True)
            if show_code_btn:
                self.session.toggle_show_code()

        # Handle generate button
        if generate_btn:
            self._handle_generation(user_prompt)

    def _render_preview_section(self) -> None:
        """Render the preview panel section."""
        html_code = self.session.get_generated_code()
        show_code = self.session.is_showing_code()
        render_preview_panel(html_code, show_code)

    def run(self) -> None:
        """Run the main application."""
        # Render title
        render_title()

        # Create main layout
        col_chat, col_preview = st.columns([1, 1])

        # Render sidebar and get values
        api_key, selected_model, clear_clicked = render_sidebar(
            api_key=self.session.get_api_key(),
            has_secret_key=self._has_secret_key(),
            selected_model=self.session.get_selected_model(),
            on_api_key_change=self.session.set_api_key,
            on_model_change=self.session.set_selected_model,
            on_clear_chat=self.session.clear_chat,
        )

        # Handle clear chat
        if clear_clicked:
            st.rerun()

        # Render main content
        with col_chat:
            self._render_chat_section()

        with col_preview:
            self._render_preview_section()

        # Render footer
        render_footer()


def main() -> None:
    """Main entry point for the application."""
    app = AIWebsiteGenerator()
    app.run()


if __name__ == "__main__":
    main()

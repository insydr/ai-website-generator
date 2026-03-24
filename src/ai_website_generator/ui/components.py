"""
UI Components Module
====================

Provides reusable UI components for the Streamlit application.
"""

import streamlit as st
from datetime import datetime
from typing import Optional, List, Callable

from ai_website_generator.constants import (
    EXAMPLE_PROMPTS,
    AVAILABLE_MODELS,
    PREVIEW_HEIGHT,
    MAX_CHAT_PREVIEW_LENGTH,
)
from ai_website_generator.utils.code_extractor import get_code_preview


def render_chat_message(role: str, content: str, preview_length: int = MAX_CHAT_PREVIEW_LENGTH) -> None:
    """
    Render a chat message with appropriate styling.

    Args:
        role: "user" or "assistant"
        content: Message content
        preview_length: Maximum length for preview (for AI messages)
    """
    if role == "user":
        st.markdown(
            f"""
        <div class="user-message">
            <div class="message-label">👤 You</div>
            <div>{content}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        # For AI, show a preview of the code or message
        preview_text = get_code_preview(content, preview_length)
        st.markdown(
            f"""
        <div class="ai-message">
            <div class="message-label">🤖 AI</div>
            <div>{preview_text}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_example_prompts(on_click: Optional[Callable[[str], None]] = None) -> None:
    """
    Render example prompt buttons.

    Args:
        on_click: Callback function when example is clicked
    """
    st.info("👋 Start by describing the website you want to create!")
    st.markdown("**Example prompts:**")

    for i, example in enumerate(EXAMPLE_PROMPTS):
        if st.button(example, key=f"example_{i}"):
            if on_click:
                on_click(example.split(" ", 1)[1] if " " in example else example)


def render_preview_panel(html_code: Optional[str], show_code: bool = False) -> None:
    """
    Render the HTML preview panel.

    Args:
        html_code: HTML code to preview
        show_code: Whether to show the code view
    """
    st.markdown("### 👁️ Live Preview")

    if html_code:
        # Preview container
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.markdown(
            '<div class="preview-header"><span>🌐 Preview</span><span>Responsive</span></div>',
            unsafe_allow_html=True,
        )

        # Render the HTML preview
        st.components.v1.html(html_code, height=PREVIEW_HEIGHT, scrolling=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="📥 Download HTML File",
            data=html_code,
            file_name=f"website_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True,
        )

        # Show code toggle
        if show_code:
            with st.expander("📝 View Code", expanded=True):
                st.code(html_code, language="html")
    else:
        render_empty_state()


def render_empty_state() -> None:
    """Render the empty state when no preview is available."""
    st.markdown(
        """
    <div class="empty-state">
        <div class="empty-state-icon">🎨</div>
        <h4>Your preview will appear here</h4>
        <p>Enter a description and click "Generate Website" to see the magic!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar(
    api_key: Optional[str] = None,
    has_secret_key: bool = False,
    selected_model: Optional[str] = None,
    on_api_key_change: Optional[Callable[[str], None]] = None,
    on_model_change: Optional[Callable[[str], None]] = None,
    on_clear_chat: Optional[Callable[[], None]] = None,
) -> tuple:
    """
    Render the sidebar with configuration options.

    Args:
        api_key: Current API key value
        has_secret_key: Whether API key is loaded from secrets
        selected_model: Currently selected model ID
        on_api_key_change: Callback when API key changes
        on_model_change: Callback when model selection changes
        on_clear_chat: Callback when clear button is clicked

    Returns:
        Tuple of (api_key, selected_model, clear_clicked)
    """
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")

        # API Key input
        st.markdown("### 🔑 OpenRouter API Key")

        if has_secret_key:
            st.success("✅ API Key loaded from secrets")
            current_api_key = api_key
        else:
            current_api_key = st.text_input(
                "Enter your API Key:",
                type="password",
                placeholder="sk-or-...",
                help="Get your API key from openrouter.ai/keys",
                value=api_key or "",
                key="sidebar_api_key",
            )
            if on_api_key_change and current_api_key:
                on_api_key_change(current_api_key)

        st.markdown("---")

        # Model selection
        st.markdown("### 🤖 Select Model")

        model_options = {m["name"]: m["id"] for m in AVAILABLE_MODELS}
        model_names = list(model_options.keys())

        # Find default index
        default_index = 0
        if selected_model:
            for i, (name, mid) in enumerate(model_options.items()):
                if mid == selected_model:
                    default_index = i
                    break

        selected_model_name = st.selectbox(
            "Choose a model:",
            options=model_names,
            index=default_index,
            help="Free models sorted by latency (fastest first)",
        )

        new_selected_model = model_options[selected_model_name]
        if on_model_change:
            on_model_change(new_selected_model)

        # Show model info
        model_info = next((m for m in AVAILABLE_MODELS if m["id"] == new_selected_model), None)
        if model_info:
            st.caption(f"📊 Context: {model_info['context']}")
            st.caption(f"📝 {model_info['description']}")

        st.markdown("---")

        # Clear chat button
        clear_clicked = st.button("🗑️ Clear Chat", key="clear_btn", help="Clear all chat history")

        if clear_clicked and on_clear_chat:
            on_clear_chat()

        st.markdown("---")

        # Help section
        with st.expander("❓ How to use"):
            st.markdown(
                """
            1. **Enter your OpenRouter API key** (or add to secrets)
            2. **Select a model** from the dropdown
            3. **Describe your website** in natural language
            4. **View the live preview** on the right
            5. **Download the code** if satisfied

            **Tips:**
            - Be specific about design preferences
            - Mention color schemes, layouts
            - Describe interactive features
            """
            )

        with st.expander("🔗 Get API Key"):
            st.markdown(
                """
            1. Visit [openrouter.ai](https://openrouter.ai)
            2. Sign up / Log in
            3. Go to [Keys](https://openrouter.ai/keys)
            4. Create a new API key
            5. Paste it above

            **Free tier available!**
            """
            )

        return current_api_key, new_selected_model, clear_clicked


def render_footer() -> None:
    """Render the application footer."""
    st.markdown("---")
    st.markdown(
        """
    <div class="footer">
        <p>Made with ❤️ using Streamlit & OpenRouter |
        <a href="https://openrouter.ai" target="_blank">OpenRouter</a> |
        Free AI Models Available</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_title() -> None:
    """Render the application title."""
    st.markdown('<h1 class="main-title">🌐 AI Website Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform your ideas into beautiful websites with AI</p>', unsafe_allow_html=True)


def render_error_message(message: str) -> None:
    """Render an error message."""
    st.error(f"❌ {message}")


def render_success_message(message: str) -> None:
    """Render a success message."""
    st.success(f"✅ {message}")


def render_warning_message(message: str) -> None:
    """Render a warning message."""
    st.warning(f"⚠️ {message}")

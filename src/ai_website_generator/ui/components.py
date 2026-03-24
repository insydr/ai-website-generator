"""
UI Components Module
====================

Provides reusable UI components for the Streamlit application.
"""

import streamlit as st
from datetime import datetime
from typing import Optional, List, Callable, Dict, Any

from ai_website_generator.constants import (
    EXAMPLE_PROMPTS,
    PREVIEW_HEIGHT,
    MAX_CHAT_PREVIEW_LENGTH,
    API_KEY_HINTS,
    PROVIDER_DISPLAY_NAMES,
)
from ai_website_generator.utils.code_extractor import get_code_preview
from ai_website_generator.providers.registry import ProviderRegistry
from ai_website_generator.providers.base import ProviderType


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


def render_provider_selector(
    current_provider: str,
    on_change: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Render provider selection dropdown.

    Args:
        current_provider: Currently selected provider type
        on_change: Callback when selection changes

    Returns:
        Selected provider type
    """
    providers = ProviderRegistry.get_available_providers()

    # Create display names with descriptions
    options = {}
    for p in providers:
        label = f"{p['name']}"
        if p["description"]:
            label += f" - {p['description']}"
        options[p["type"]] = label

    # Find current selection
    index = list(options.keys()).index(current_provider) if current_provider in options else 0

    selected = st.selectbox(
        "🤖 AI Provider",
        options=list(options.keys()),
        format_func=lambda x: options.get(x, x),
        index=index,
        help="Select your AI provider. Each has different models and pricing.",
    )

    if on_change and selected != current_provider:
        on_change(selected)

    return selected


def render_model_selector(
    provider_type: str,
    current_model: str,
    allow_custom: bool = True,
    on_change: Optional[Callable[[str], None]] = None,
) -> tuple:
    """
    Render model selection for the chosen provider.

    Args:
        provider_type: Type of provider
        current_model: Currently selected model
        allow_custom: Whether to allow custom model input
        on_change: Callback when selection changes

    Returns:
        Tuple of (selected_model, is_custom)
    """
    try:
        provider_enum = ProviderType(provider_type)
        models = ProviderRegistry.get_provider_models(provider_enum)
    except ValueError:
        models = []

    if not models:
        # No predefined models, allow custom input
        st.info("Enter your model name below:")
        custom_model = st.text_input(
            "Model Name",
            value=current_model,
            placeholder="e.g., gpt-4, claude-3-opus, llama-3",
            help="Enter the model identifier for your API",
        )
        return custom_model, True

    # Create options with descriptions
    options = {}
    for m in models:
        label = m.name
        if m.is_free:
            label = f"🆓 {label}"
        if m.context_length != "Unknown":
            label += f" ({m.context_length})"
        options[m.id] = label

    # Add custom option if allowed
    if allow_custom:
        options["__custom__"] = "✏️ Custom model..."

    # Find current selection
    if current_model in options:
        index = list(options.keys()).index(current_model)
    else:
        # If current model not in list, default to custom
        index = len(options) - 1 if allow_custom else 0

    selected = st.selectbox(
        "📋 Select Model",
        options=list(options.keys()),
        format_func=lambda x: options.get(x, x),
        index=index,
        help="Choose a model or enter a custom one",
    )

    # Handle custom model input
    if selected == "__custom__":
        custom_model = st.text_input(
            "Enter Model ID",
            value=current_model if current_model not in options else "",
            placeholder="e.g., gpt-4-turbo, claude-3-opus-20240229",
            help="Enter the exact model identifier",
        )
        return custom_model, True

    if on_change and selected != current_model:
        on_change(selected)

    return selected, False


def render_api_key_input(
    provider_type: str,
    current_key: str = "",
    has_secret: bool = False,
    on_change: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Render API key input for the selected provider.

    Args:
        provider_type: Type of provider
        current_key: Current API key value
        has_secret: Whether key is loaded from secrets
        on_change: Callback when key changes

    Returns:
        API key value
    """
    if has_secret:
        st.success(f"✅ API Key loaded from secrets")
        return current_key

    hint = API_KEY_HINTS.get(provider_type, "Your API key")

    api_key = st.text_input(
        "🔑 API Key",
        type="password",
        value=current_key,
        placeholder=hint,
        help=f"Your {PROVIDER_DISPLAY_NAMES.get(provider_type, provider_type)} API key",
    )

    if on_change and api_key != current_key:
        on_change(api_key)

    return api_key


def render_custom_endpoint_input(
    current_url: str = "",
    visible: bool = False,
    on_change: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Render custom API endpoint input for custom provider.

    Args:
        current_url: Current endpoint URL
        visible: Whether to show this input
        on_change: Callback when URL changes

    Returns:
        Endpoint URL value
    """
    if not visible:
        return current_url

    url = st.text_input(
        "🔗 API Endpoint URL",
        value=current_url,
        placeholder="https://api.example.com/v1/chat/completions",
        help="Full URL to the chat completions endpoint",
    )

    if on_change and url != current_url:
        on_change(url)

    return url


def render_sidebar(
    provider_type: str = "openrouter",
    api_key: str = "",
    selected_model: str = "",
    has_secret_key: bool = False,
    custom_base_url: str = "",
    on_provider_change: Optional[Callable[[str], None]] = None,
    on_api_key_change: Optional[Callable[[str], None]] = None,
    on_model_change: Optional[Callable[[str], None]] = None,
    on_base_url_change: Optional[Callable[[str], None]] = None,
    on_clear_chat: Optional[Callable[[], None]] = None,
) -> Dict[str, Any]:
    """
    Render the complete sidebar with all configuration options.

    Args:
        provider_type: Current provider type
        api_key: Current API key
        selected_model: Currently selected model
        has_secret_key: Whether API key is loaded from secrets
        custom_base_url: Custom endpoint URL
        on_provider_change: Callback when provider changes
        on_api_key_change: Callback when API key changes
        on_model_change: Callback when model changes
        on_base_url_change: Callback when base URL changes
        on_clear_chat: Callback when clear button is clicked

    Returns:
        Dictionary with all current settings
    """
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")

        # Provider selection
        st.markdown("### 🏢 AI Provider")
        new_provider = render_provider_selector(provider_type, on_provider_change)

        st.markdown("---")

        # API Key
        st.markdown("### 🔑 Authentication")
        new_api_key = render_api_key_input(
            new_provider,
            api_key,
            has_secret_key,
            on_api_key_change,
        )

        st.markdown("---")

        # Model selection
        st.markdown("### 🤖 Model")
        new_model, is_custom = render_model_selector(
            new_provider,
            selected_model,
            allow_custom=True,
            on_model_change=on_model_change,
        )

        # Custom endpoint (only for custom provider)
        if new_provider == "custom":
            st.markdown("---")
            st.markdown("### 🔗 Custom Endpoint")
            new_base_url = render_custom_endpoint_input(
                custom_base_url,
                visible=True,
                on_change=on_base_url_change,
            )
        else:
            new_base_url = custom_base_url

        st.markdown("---")

        # Clear chat button
        clear_clicked = st.button("🗑️ Clear Chat", key="clear_btn", help="Clear all chat history")

        if clear_clicked and on_clear_chat:
            on_clear_chat()

        st.markdown("---")

        # Help sections
        with st.expander("❓ How to use"):
            st.markdown(
                """
            1. **Select your AI provider** from the dropdown
            2. **Enter your API key** (or add to secrets)
            3. **Choose a model** or enter custom model name
            4. **Describe your website** in natural language
            5. **View the live preview** on the right
            6. **Download the code** if satisfied

            **Tips:**
            - Be specific about design preferences
            - Mention color schemes, layouts
            - Describe interactive features
            """
            )

        with st.expander("🔗 Get API Keys"):
            st.markdown(
                """
            **OpenRouter:** [openrouter.ai/keys](https://openrouter.ai/keys)
            - Free tier available
            - Access to multiple models

            **OpenAI:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
            - GPT-4, GPT-3.5, etc.

            **Anthropic:** [console.anthropic.com](https://console.anthropic.com/)
            - Claude 3 models

            **Groq:** [console.groq.com/keys](https://console.groq.com/keys)
            - Ultra-fast inference
            - Free tier available
            """
            )

        return {
            "provider_type": new_provider,
            "api_key": new_api_key,
            "model": new_model,
            "is_custom_model": is_custom,
            "base_url": new_base_url,
            "clear_clicked": clear_clicked,
        }


def render_footer() -> None:
    """Render the application footer."""
    st.markdown("---")
    st.markdown(
        """
    <div class="footer">
        <p>Made with ❤️ using Streamlit |
        <a href="https://openrouter.ai" target="_blank">OpenRouter</a> |
        Multiple AI Providers Supported</p>
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


def render_provider_status(provider_type: str, model: str, is_configured: bool) -> None:
    """
    Render provider status indicator.

    Args:
        provider_type: Type of provider
        model: Selected model
        is_configured: Whether the provider is properly configured
    """
    provider_name = PROVIDER_DISPLAY_NAMES.get(provider_type, provider_type)

    if is_configured:
        st.caption(f"✅ {provider_name} | {model}")
    else:
        st.caption(f"⚠️ {provider_name} | Configure API key to start")

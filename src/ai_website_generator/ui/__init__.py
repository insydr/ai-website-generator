"""
UI Module
=========

Provides UI components and styling for the application.
"""

from ai_website_generator.ui.styles import apply_custom_css, CUSTOM_CSS
from ai_website_generator.ui.components import (
    render_chat_message,
    render_example_prompts,
    render_preview_panel,
    render_sidebar,
    render_empty_state,
    render_title,
    render_footer,
    render_error_message,
    render_success_message,
    render_warning_message,
    render_provider_status,
    render_provider_selector,
    render_model_selector,
    render_api_key_input,
    render_custom_endpoint_input,
)

__all__ = [
    "apply_custom_css",
    "CUSTOM_CSS",
    "render_chat_message",
    "render_example_prompts",
    "render_preview_panel",
    "render_sidebar",
    "render_empty_state",
    "render_title",
    "render_footer",
    "render_error_message",
    "render_success_message",
    "render_warning_message",
    "render_provider_status",
    "render_provider_selector",
    "render_model_selector",
    "render_api_key_input",
    "render_custom_endpoint_input",
]

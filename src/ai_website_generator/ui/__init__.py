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
)

__all__ = [
    "apply_custom_css",
    "CUSTOM_CSS",
    "render_chat_message",
    "render_example_prompts",
    "render_preview_panel",
    "render_sidebar",
    "render_empty_state",
]

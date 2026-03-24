"""
Utilities Module
================

Provides utility functions and helpers.
"""

from ai_website_generator.utils.code_extractor import (
    extract_html_code,
    clean_html_response,
    validate_html,
)
from ai_website_generator.utils.session import (
    SessionManager,
    get_session_manager,
)

__all__ = [
    "extract_html_code",
    "clean_html_response",
    "validate_html",
    "SessionManager",
    "get_session_manager",
]

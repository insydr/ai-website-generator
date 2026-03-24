"""
Code Extractor Module
=====================

Handles extraction and validation of HTML code from AI responses.
"""

import re
from typing import Optional, Tuple


def extract_html_code(response_text: str) -> Optional[str]:
    """
    Extract HTML code from AI response.

    Handles multiple code block formats and edge cases.

    Args:
        response_text: Raw text response from AI

    Returns:
        Extracted HTML code or None if not found

    Examples:
        >>> html = extract_html_code("```html\\n<!DOCTYPE html>...\\n```")
        >>> print(html)  # Full HTML code
    """
    if not response_text:
        return None

    # Patterns to match various code block formats
    patterns = [
        r"```html\s*(.*?)\s*```",  # Standard html code block
        r"```HTML\s*(.*?)\s*```",  # Uppercase HTML
        r"```\s*(<!DOCTYPE.*?)\s*```",  # Code block starting with DOCTYPE
        r"```\s*(<html.*?)\s*```",  # Code block starting with html tag
        r"```(.*?)```",  # Any code block (last resort)
    ]

    # Try each pattern
    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)
        if matches:
            code = matches[0].strip()
            # Validate it's actual HTML
            if validate_html(code):
                return code

    # If no code blocks found, check if entire response is HTML
    if validate_html(response_text):
        cleaned = clean_html_response(response_text)
        return cleaned

    return None


def clean_html_response(text: str) -> str:
    """
    Clean HTML response by removing markdown formatting.

    Args:
        text: Raw text possibly containing markdown

    Returns:
        Cleaned HTML text
    """
    cleaned = text.strip()

    # Remove leading code block markers
    cleaned = re.sub(r"^```(?:html|HTML)?\s*", "", cleaned)

    # Remove trailing code block markers
    cleaned = re.sub(r"\s*```$", "", cleaned)

    return cleaned.strip()


def validate_html(text: str) -> bool:
    """
    Check if text contains valid HTML structure.

    Args:
        text: Text to validate

    Returns:
        True if text appears to be valid HTML
    """
    if not text:
        return False

    text_upper = text.upper()

    # Check for DOCTYPE or HTML tag
    has_doctype = "<!DOCTYPE" in text_upper
    has_html_tag = "<HTML" in text_upper

    return has_doctype or has_html_tag


def extract_and_validate(response_text: str) -> Tuple[bool, Optional[str], str]:
    """
    Extract and validate HTML code from response.

    Args:
        response_text: Raw text response from AI

    Returns:
        Tuple of (success, html_code, message)
    """
    html_code = extract_html_code(response_text)

    if html_code:
        return True, html_code, "HTML code extracted successfully"

    # Check if response contains any code-like content
    if "```" in response_text:
        return False, None, "Found code block but could not extract valid HTML"

    return False, None, "No HTML code found in response"


def get_code_preview(code: str, max_length: int = 200) -> str:
    """
    Get a preview of code for display.

    Args:
        code: Full code string
        max_length: Maximum length of preview

    Returns:
        Truncated preview string
    """
    if not code:
        return ""

    # Remove extra whitespace
    preview = " ".join(code.split())

    if len(preview) > max_length:
        return preview[:max_length] + "..."

    return preview

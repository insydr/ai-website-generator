"""
Tests for Code Extractor Module
===============================

Unit tests for the code extraction and validation functions.
"""

import pytest
from ai_website_generator.utils.code_extractor import (
    extract_html_code,
    clean_html_response,
    validate_html,
    extract_and_validate,
    get_code_preview,
)


class TestValidateHTML:
    """Tests for validate_html function."""

    def test_valid_doctype(self):
        """Test validation of HTML with DOCTYPE."""
        html = "<!DOCTYPE html><html><head></head><body></body></html>"
        assert validate_html(html) is True

    def test_valid_html_tag(self):
        """Test validation of HTML with html tag."""
        html = "<html><head></head><body></body></html>"
        assert validate_html(html) is True

    def test_invalid_html(self):
        """Test validation of non-HTML content."""
        assert validate_html("This is just text") is False
        assert validate_html("<div>Some div</div>") is False

    def test_empty_string(self):
        """Test validation of empty string."""
        assert validate_html("") is False
        assert validate_html(None) is False

    def test_case_insensitive(self):
        """Test case insensitive validation."""
        html_upper = "<!DOCTYPE HTML><HTML></HTML>"
        html_lower = "<!doctype html><html></html>"
        assert validate_html(html_upper) is True
        assert validate_html(html_lower) is True


class TestExtractHTMLCode:
    """Tests for extract_html_code function."""

    def test_extract_html_block(self):
        """Test extraction from html code block."""
        response = """```html
<!DOCTYPE html>
<html><head></head><body><h1>Test</h1></body></html>
```"""
        result = extract_html_code(response)
        assert result is not None
        assert "<!DOCTYPE html>" in result
        assert "<h1>Test</h1>" in result

    def test_extract_uppercase_html(self):
        """Test extraction from uppercase HTML code block."""
        response = """```HTML
<!DOCTYPE html><html></html>
```"""
        result = extract_html_code(response)
        assert result is not None
        assert "<!DOCTYPE html>" in result

    def test_extract_doctype_block(self):
        """Test extraction from code block starting with DOCTYPE."""
        response = """```
<!DOCTYPE html>
<html><body>Content</body></html>
```"""
        result = extract_html_code(response)
        assert result is not None
        assert "Content" in result

    def test_extract_no_block_markers(self):
        """Test extraction when response is pure HTML."""
        response = "<!DOCTYPE html><html><body>Pure HTML</body></html>"
        result = extract_html_code(response)
        assert result is not None
        assert "Pure HTML" in result

    def test_extract_none_input(self):
        """Test extraction with None input."""
        assert extract_html_code(None) is None

    def test_extract_empty_input(self):
        """Test extraction with empty input."""
        assert extract_html_code("") is None

    def test_extract_no_html(self):
        """Test extraction when no HTML present."""
        response = "This is just plain text without any HTML code."
        assert extract_html_code(response) is None


class TestCleanHTMLResponse:
    """Tests for clean_html_response function."""

    def test_clean_leading_markers(self):
        """Test removal of leading code block markers."""
        text = "```html\n<!DOCTYPE html><html></html>"
        result = clean_html_response(text)
        assert result.startswith("<!DOCTYPE")

    def test_clean_trailing_markers(self):
        """Test removal of trailing code block markers."""
        text = "<!DOCTYPE html><html></html>\n```"
        result = clean_html_response(text)
        assert result.endswith("</html>")

    def test_clean_both_markers(self):
        """Test removal of both leading and trailing markers."""
        text = "```html\n<!DOCTYPE html><html></html>\n```"
        result = clean_html_response(text)
        assert result.startswith("<!DOCTYPE")
        assert result.endswith("</html>")


class TestExtractAndValidate:
    """Tests for extract_and_validate function."""

    def test_successful_extraction(self):
        """Test successful extraction."""
        response = "```html\n<!DOCTYPE html><html><body>Test</body></html>\n```"
        success, code, message = extract_and_validate(response)
        assert success is True
        assert code is not None
        assert "Test" in code

    def test_failed_extraction_no_html(self):
        """Test failed extraction with no HTML."""
        response = "Just some text without HTML"
        success, code, message = extract_and_validate(response)
        assert success is False
        assert code is None

    def test_failed_extraction_invalid_block(self):
        """Test failed extraction with invalid code block."""
        response = "```\nSome Python code\n```"
        success, code, message = extract_and_validate(response)
        assert success is False


class TestGetCodePreview:
    """Tests for get_code_preview function."""

    def test_short_code(self):
        """Test preview of short code."""
        code = "<html>Short</html>"
        result = get_code_preview(code, max_length=50)
        assert result == code

    def test_long_code(self):
        """Test preview truncation of long code."""
        code = "<html>" + "x" * 300 + "</html>"
        result = get_code_preview(code, max_length=100)
        assert len(result) == 103  # 100 + "..."
        assert result.endswith("...")

    def test_whitespace_normalization(self):
        """Test whitespace normalization."""
        code = "<html>   multiple    spaces   </html>"
        result = get_code_preview(code)
        assert "  " not in result  # No double spaces

    def test_empty_code(self):
        """Test preview of empty code."""
        assert get_code_preview("") == ""
        assert get_code_preview(None) == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

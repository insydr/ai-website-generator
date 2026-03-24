"""
AI Website Generator
====================

A Streamlit application that generates website code (HTML/CSS/JS) from natural
language descriptions using OpenRouter API.

Example usage:
    streamlit run -m ai_website_generator
"""

__version__ = "1.0.0"
__author__ = "Sydr Dev"
__email__ = "rsd.iz.rosyid@gmail.com"

from ai_website_generator.app import main

__all__ = ["main", "__version__"]

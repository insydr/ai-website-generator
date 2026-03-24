"""
Constants Module
================

Contains all constant values used throughout the application.
"""

# =============================================================================
# APPLICATION METADATA
# =============================================================================

APP_TITLE = "AI Website Generator"
APP_ICON = "🌐"
APP_VERSION = "1.1.0"

# =============================================================================
# API CONFIGURATION
# =============================================================================

API_TIMEOUT = 120  # seconds
API_REFERER = "https://ai-website-generator.streamlit.app"
API_TITLE = "AI Website Generator"

# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """You are an expert web developer AI agent specialized in creating complete, production-ready websites from natural language descriptions.

## YOUR TASK
Generate a complete, single-file HTML website with embedded CSS and JavaScript based on the user's description.

## CRITICAL RULES
1. **OUTPUT FORMAT**: You MUST return ONLY valid HTML code inside a single code block. No explanations before or after.
2. **SINGLE FILE**: All CSS must be in a `<style>` tag inside `<head>`. All JavaScript must be in a `<script>` tag before `</body>`.
3. **NO EXTERNAL DEPENDENCIES**: Do not use external CSS frameworks, CDNs, or libraries unless specifically requested. Use pure CSS and vanilla JavaScript.
4. **COMPLETE & FUNCTIONAL**: The code must be fully functional when opened in a browser. Include all necessary elements, styles, and interactivity.
5. **MODERN & RESPONSIVE**: Design must be modern, visually appealing, and responsive for mobile and desktop.
6. **NO PLACEHOLDER TEXT**: Use realistic, contextual content instead of "Lorem ipsum" or placeholder text.

## CODE STRUCTURE TEMPLATE
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Contextual Title]</title>
    <style>
        /* Reset and Base Styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        /* CSS Variables for theming */
        :root {
            --primary: #...;
            --secondary: #...;
            --background: #...;
            --text: #...;
        }

        /* All your styles here */
    </style>
</head>
<body>
    <!-- Complete HTML structure -->

    <script>
        // All JavaScript functionality here
    </script>
</body>
</html>
```

## DESIGN PRINCIPLES
- Use modern CSS features (flexbox, grid, CSS variables, animations)
- Implement smooth transitions and subtle animations
- Ensure good contrast and readability
- Create visually interesting layouts (not just centered text)
- Include hover effects and interactive elements
- Add meaningful icons using Unicode or CSS shapes

## RESPONSE FORMAT
Return ONLY the HTML code block, nothing else:
```html
[Your complete HTML/CSS/JS code here]
```"""

# =============================================================================
# EXAMPLE PROMPTS
# =============================================================================

EXAMPLE_PROMPTS = [
    "🏠 Landing page for a real estate company with property listings",
    "☕ Coffee shop website with dark theme and menu section",
    "💼 Personal portfolio for a software developer",
    "🛒 E-commerce product page with shopping cart",
    "📊 Dashboard for analytics with charts and metrics",
    "🍕 Restaurant website with online ordering system",
]

# =============================================================================
# UI SETTINGS
# =============================================================================

# Preview settings
PREVIEW_HEIGHT = 600
MAX_CODE_DISPLAY_HEIGHT = 300

# Chat settings
MAX_CHAT_PREVIEW_LENGTH = 200

# Generation settings
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4000

# =============================================================================
# PROVIDER DEFAULTS
# =============================================================================

DEFAULT_PROVIDER = "openrouter"
DEFAULT_MODEL = "meta-llama/llama-3.2-3b-instruct:free"

# Provider display names
PROVIDER_DISPLAY_NAMES = {
    "openrouter": "OpenRouter",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "groq": "Groq",
    "custom": "Custom API",
}

# API Key hints for each provider
API_KEY_HINTS = {
    "openrouter": "sk-or-v1-...",
    "openai": "sk-...",
    "anthropic": "sk-ant-...",
    "groq": "gsk_...",
    "custom": "Your API key",
}

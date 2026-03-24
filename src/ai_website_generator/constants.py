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
APP_VERSION = "1.0.0"

# =============================================================================
# API CONFIGURATION
# =============================================================================

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_TIMEOUT = 120  # seconds
API_REFERER = "https://ai-website-generator.streamlit.app"
API_TITLE = "AI Website Generator"

# =============================================================================
# AVAILABLE MODELS
# =============================================================================

# Free models from OpenRouter (sorted by latency)
AVAILABLE_MODELS = [
    {
        "id": "meta-llama/llama-3.2-3b-instruct:free",
        "name": "Llama 3.2 3B (Free)",
        "context": "128K",
        "description": "Fast and capable for most tasks"
    },
    {
        "id": "meta-llama/llama-3.2-1b-instruct:free",
        "name": "Llama 3.2 1B (Free)",
        "context": "128K",
        "description": "Ultra-fast, best for simple sites"
    },
    {
        "id": "meta-llama/llama-3.1-8b-instruct:free",
        "name": "Llama 3.1 8B (Free)",
        "context": "128K",
        "description": "Balanced speed and quality"
    },
    {
        "id": "qwen/qwen-2-7b-instruct:free",
        "name": "Qwen 2 7B (Free)",
        "context": "32K",
        "description": "Good for complex designs"
    },
    {
        "id": "google/gemma-2-9b-it:free",
        "name": "Gemma 2 9B (Free)",
        "context": "8K",
        "description": "High quality output"
    },
    {
        "id": "mistralai/mistral-7b-instruct:free",
        "name": "Mistral 7B (Free)",
        "context": "32K",
        "description": "Fast and capable"
    },
    {
        "id": "huggingfaceh4/zephyr-7b-beta:free",
        "name": "Zephyr 7B (Free)",
        "context": "4K",
        "description": "Good conversation model"
    },
    {
        "id": "openchat/openchat-7b:free",
        "name": "OpenChat 7B (Free)",
        "context": "4K",
        "description": "Optimized for chat"
    },
    {
        "id": "deepseek/deepseek-r1:free",
        "name": "DeepSeek R1 (Free)",
        "context": "128K",
        "description": "Complex reasoning"
    },
    {
        "id": "deepseek/deepseek-chat:free",
        "name": "DeepSeek Chat (Free)",
        "context": "128K",
        "description": "Conversational AI"
    },
]

# Default model selection
DEFAULT_MODEL_ID = AVAILABLE_MODELS[0]["id"]

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

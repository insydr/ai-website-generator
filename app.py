"""
AI Website Generator Agent
==========================
A Streamlit application that generates website code (HTML/CSS/JS) from natural language descriptions
using OpenRouter API. Similar to v0.dev, Replit Agent, or Emergent.

Author: Senior Full-Stack Engineer
"""

import streamlit as st
import requests
import re
import time
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import json

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
APP_TITLE = "AI Website Generator"
APP_ICON = "🌐"

# Default free models from OpenRouter (sorted by latency)
DEFAULT_MODELS = [
    {"id": "meta-llama/llama-3.2-3b-instruct:free", "name": "Llama 3.2 3B (Free)", "context": "128K"},
    {"id": "meta-llama/llama-3.2-1b-instruct:free", "name": "Llama 3.2 1B (Free)", "context": "128K"},
    {"id": "meta-llama/llama-3.1-8b-instruct:free", "name": "Llama 3.1 8B (Free)", "context": "128K"},
    {"id": "qwen/qwen-2-7b-instruct:free", "name": "Qwen 2 7B (Free)", "context": "32K"},
    {"id": "google/gemma-2-9b-it:free", "name": "Gemma 2 9B (Free)", "context": "8K"},
    {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B (Free)", "context": "32K"},
    {"id": "huggingfaceh4/zephyr-7b-beta:free", "name": "Zephyr 7B (Free)", "context": "4K"},
    {"id": "openchat/openchat-7b:free", "name": "OpenChat 7B (Free)", "context": "4K"},
    {"id": "deepseek/deepseek-r1:free", "name": "DeepSeek R1 (Free)", "context": "128K"},
    {"id": "deepseek/deepseek-chat:free", "name": "DeepSeek Chat (Free)", "context": "128K"},
]

# System prompt for the AI agent
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
# CSS STYLES FOR STREAMLIT UI
# =============================================================================

CUSTOM_CSS = """
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Chat container */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        margin-bottom: 1rem;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 1.5rem 1.5rem 0.5rem 1.5rem;
        margin: 0.5rem 0;
        margin-left: auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .ai-message {
        background: white;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 1.5rem 1.5rem 1.5rem 0.5rem;
        margin: 0.5rem 0;
        margin-right: auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #eee;
    }
    
    .message-label {
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
        opacity: 0.8;
    }
    
    /* Preview container */
    .preview-container {
        border: 2px solid #e0e0e0;
        border-radius: 1rem;
        overflow: hidden;
        background: white;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .preview-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Status indicators */
    .status-success {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-error {
        color: #ef4444;
        font-weight: 600;
    }
    
    .status-loading {
        color: #f59e0b;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Download button */
    .download-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    }
    
    /* Clear button */
    .clear-btn {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    }
    
    /* Code display */
    .code-block {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Fira Code', 'Consolas', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
        max-height: 300px;
        overflow-y: auto;
    }
    
    /* Prompt examples */
    .example-card {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-card:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateX(5px);
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-text {
        animation: pulse 1.5s infinite;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.85rem;
        margin-top: 2rem;
        border-top: 1px solid #eee;
    }
</style>
"""

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_api_key() -> Optional[str]:
    """
    Get API key from secrets or session state.
    Priority: session_state > secrets
    """
    # First check session state (user input)
    if "api_key" in st.session_state and st.session_state.api_key:
        return st.session_state.api_key
    
    # Then check secrets
    try:
        if "openrouter_api_key" in st.secrets:
            return st.secrets["openrouter_api_key"]
    except Exception:
        pass
    
    return None


def extract_html_code(response_text: str) -> Optional[str]:
    """
    Extract HTML code from AI response.
    Handles multiple code block formats and edge cases.
    """
    if not response_text:
        return None
    
    # Try multiple patterns to extract code
    patterns = [
        r'```html\s*(.*?)\s*```',  # Standard html code block
        r'```HTML\s*(.*?)\s*```',  # Uppercase HTML
        r'```\s*(<!DOCTYPE.*?)\s*```',  # Code block starting with DOCTYPE
        r'```\s*(<html.*?)\s*```',  # Code block starting with html tag
        r'```(.*?)```',  # Any code block (last resort)
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)
        if matches:
            code = matches[0].strip()
            # Verify it's valid HTML
            if '<!DOCTYPE' in code.upper() or '<HTML' in code.upper():
                return code
    
    # If no code blocks found, check if the entire response is HTML
    if '<!DOCTYPE' in response_text.upper() or '<HTML' in response_text.upper():
        # Clean up any markdown formatting
        cleaned = response_text.strip()
        if cleaned.startswith('```'):
            cleaned = re.sub(r'^```(?:html|HTML)?\s*', '', cleaned)
        if cleaned.endswith('```'):
            cleaned = re.sub(r'\s*```$', '', cleaned)
        return cleaned.strip()
    
    return None


def call_openrouter_api(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4000
) -> Tuple[bool, str]:
    """
    Make API call to OpenRouter.
    Returns (success, response_or_error_message)
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://ai-website-generator.streamlit.app",
        "X-Title": "AI Website Generator",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=120  # 2 minutes timeout
        )
        
        # Handle different response codes
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return True, content
            else:
                return False, "Invalid response format from API"
        
        elif response.status_code == 401:
            return False, "Invalid API key. Please check your OpenRouter API key."
        
        elif response.status_code == 402:
            return False, "Insufficient credits. Please add credits to your OpenRouter account."
        
        elif response.status_code == 429:
            return False, "Rate limit exceeded. Please wait a moment and try again."
        
        elif response.status_code == 503:
            return False, "Model is currently overloaded. Please try a different model or wait."
        
        else:
            error_msg = f"API Error: {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = f"{error_msg} - {error_data['error'].get('message', 'Unknown error')}"
            except Exception:
                pass
            return False, error_msg
    
    except requests.exceptions.Timeout:
        return False, "Request timed out. The model might be taking too long to respond."
    
    except requests.exceptions.ConnectionError:
        return False, "Connection error. Please check your internet connection."
    
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def initialize_session_state():
    """Initialize all session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = None
    
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = DEFAULT_MODELS[0]["id"]
    
    if "show_code" not in st.session_state:
        st.session_state.show_code = False


def clear_chat():
    """Clear all chat history and generated code."""
    st.session_state.chat_history = []
    st.session_state.generated_code = None
    st.session_state.show_code = False


def render_chat_message(role: str, content: str):
    """Render a chat message with appropriate styling."""
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="message-label">👤 You</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # For AI, show a preview of the code or message
        preview_text = content[:200] + "..." if len(content) > 200 else content
        st.markdown(f"""
        <div class="ai-message">
            <div class="message-label">🤖 AI</div>
            <div>{preview_text}</div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # ==========================================================================
    # SIDEBAR - Configuration
    # ==========================================================================
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")
        
        # API Key input
        st.markdown("### 🔑 OpenRouter API Key")
        
        # Check if key exists in secrets
        has_secret_key = False
        try:
            if "openrouter_api_key" in st.secrets:
                has_secret_key = True
        except Exception:
            pass
        
        if has_secret_key:
            st.success("✅ API Key loaded from secrets")
        else:
            api_key_input = st.text_input(
                "Enter your API Key:",
                type="password",
                placeholder="sk-or-...",
                help="Get your API key from openrouter.ai/keys"
            )
            if api_key_input:
                st.session_state.api_key = api_key_input
        
        st.markdown("---")
        
        # Model selection
        st.markdown("### 🤖 Select Model")
        
        model_options = {m["name"]: m["id"] for m in DEFAULT_MODELS}
        selected_model_name = st.selectbox(
            "Choose a model:",
            options=list(model_options.keys()),
            index=0,
            help="Free models sorted by latency (fastest first)"
        )
        st.session_state.selected_model = model_options[selected_model_name]
        
        # Show model info
        model_info = next((m for m in DEFAULT_MODELS if m["id"] == st.session_state.selected_model), None)
        if model_info:
            st.caption(f"📊 Context: {model_info['context']}")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", key="clear_btn", help="Clear all chat history"):
            clear_chat()
            st.rerun()
        
        st.markdown("---")
        
        # Help section
        with st.expander("❓ How to use"):
            st.markdown("""
            1. **Enter your OpenRouter API key** (or add to secrets)
            2. **Select a model** from the dropdown
            3. **Describe your website** in natural language
            4. **View the live preview** on the right
            5. **Download the code** if satisfied
            
            **Tips:**
            - Be specific about design preferences
            - Mention color schemes, layouts
            - Describe interactive features
            """)
        
        with st.expander("🔗 Get API Key"):
            st.markdown("""
            1. Visit [openrouter.ai](https://openrouter.ai)
            2. Sign up / Log in
            3. Go to [Keys](https://openrouter.ai/keys)
            4. Create a new API key
            5. Paste it above
            
            **Free tier available!**
            """)
    
    # ==========================================================================
    # MAIN CONTENT AREA
    # ==========================================================================
    
    # Title
    st.markdown('<h1 class="main-title">🌐 AI Website Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform your ideas into beautiful websites with AI</p>', unsafe_allow_html=True)
    
    # Create two columns: Chat (left) and Preview (right)
    col_chat, col_preview = st.columns([1, 1])
    
    # -------------------------------------------------------------------------
    # LEFT COLUMN - Chat Interface
    # -------------------------------------------------------------------------
    with col_chat:
        st.markdown("### 💬 Chat")
        
        # Chat history container
        chat_container = st.container()
        
        with chat_container:
            if st.session_state.chat_history:
                for message in st.session_state.chat_history:
                    render_chat_message(message["role"], message["content"])
            else:
                st.info("👋 Start by describing the website you want to create!")
                
                # Example prompts
                st.markdown("**Example prompts:**")
                examples = [
                    "🏠 Landing page for a real estate company with property listings",
                    "☕ Coffee shop website with dark theme and menu section",
                    "💼 Personal portfolio for a software developer",
                    "🛒 E-commerce product page with shopping cart",
                    "📊 Dashboard for analytics with charts and metrics",
                    "🍕 Restaurant website with online ordering system"
                ]
                
                for example in examples:
                    if st.button(example, key=f"example_{hash(example)}"):
                        st.session_state.example_prompt = example.split(" ", 1)[1]
                        st.rerun()
        
        st.markdown("---")
        
        # Input area
        prompt_placeholder = st.session_state.get("example_prompt", "")
        if "example_prompt" in st.session_state:
            del st.session_state.example_prompt
        
        user_prompt = st.text_area(
            "Describe your website:",
            value=prompt_placeholder,
            height=100,
            placeholder="E.g., Create a modern landing page for a fitness app with a hero section, features grid, testimonials, and a contact form. Use a dark theme with neon accents.",
            key="prompt_input"
        )
        
        # Generate button
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            generate_btn = st.button("✨ Generate Website", type="primary", use_container_width=True)
        with col_btn2:
            if st.session_state.generated_code:
                show_code_btn = st.button("📝 Code", use_container_width=True)
                if show_code_btn:
                    st.session_state.show_code = not st.session_state.show_code
        
        # Check API key before processing
        api_key = get_api_key()
        
        if generate_btn:
            if not api_key:
                st.error("⚠️ Please enter your OpenRouter API key in the sidebar.")
            elif not user_prompt.strip():
                st.warning("⚠️ Please enter a description for your website.")
            else:
                # Add user message to history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_prompt
                })
                
                # Prepare messages for API
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ]
                
                # Add chat history for context
                for msg in st.session_state.chat_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Show loading state
                with st.spinner("🎨 Generating your website... This may take a moment."):
                    # Make API call
                    success, response = call_openrouter_api(
                        api_key=api_key,
                        model=st.session_state.selected_model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=4000
                    )
                
                if success:
                    # Extract HTML code
                    html_code = extract_html_code(response)
                    
                    if html_code:
                        # Add AI response to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                        # Store generated code
                        st.session_state.generated_code = html_code
                        
                        st.success("✅ Website generated successfully!")
                        st.rerun()
                    else:
                        st.error("⚠️ Could not extract HTML code from the response. Please try again.")
                        st.code(response, language="text")
                else:
                    st.error(f"❌ {response}")
    
    # -------------------------------------------------------------------------
    # RIGHT COLUMN - Preview Panel
    # -------------------------------------------------------------------------
    with col_preview:
        st.markdown("### 👁️ Live Preview")
        
        if st.session_state.generated_code:
            # Preview container
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.markdown('<div class="preview-header"><span>🌐 Preview</span><span>Responsive</span></div>', unsafe_allow_html=True)
            
            # Render the HTML preview
            st.components.v1.html(
                st.session_state.generated_code,
                height=600,
                scrolling=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                label="📥 Download HTML File",
                data=st.session_state.generated_code,
                file_name=f"website_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
            
            # Show code toggle
            if st.session_state.show_code:
                with st.expander("📝 View Code", expanded=True):
                    st.code(st.session_state.generated_code, language="html")
        else:
            # Empty state
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #666;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎨</div>
                <h4>Your preview will appear here</h4>
                <p>Enter a description and click "Generate Website" to see the magic!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>Made with ❤️ using Streamlit & OpenRouter | 
        <a href="https://openrouter.ai" target="_blank">OpenRouter</a> | 
        Free AI Models Available</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()

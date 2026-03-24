"""
Styles Module
=============

Contains CSS styling for the Streamlit application.
"""

import streamlit as st


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

    /* Example prompts */
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

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #666;
    }

    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
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


def apply_custom_css() -> None:
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

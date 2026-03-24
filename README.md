# AI Website Generator Agent

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenRouter](https://img.shields.io/badge/Multi_Provider-6366F1?style=for-the-badge&logo=openai&logoColor=white)

**Transform your ideas into beautiful websites with AI**

A powerful Streamlit application that generates complete, production-ready websites (HTML/CSS/JS) from natural language descriptions. **Bring Your Own Key (BYOK)** - supports multiple AI providers!

[Features](#features) • [Providers](#ai-providers) • [Installation](#installation) • [Usage](#usage) • [Project Structure](#project-structure)

</div>

---

## Features

### Core Features

- **Natural Language to Website**: Describe your website in plain English and get complete, functional HTML/CSS/JS code
- **Multiple AI Providers**: Support for OpenRouter, OpenAI, Anthropic, Groq, and custom endpoints
- **Bring Your Own Key (BYOK)**: Use your own API keys from any supported provider
- **Custom Model Selection**: Choose from predefined models or enter custom model IDs
- **Live Preview**: See your generated website instantly in the built-in preview panel
- **Code Download**: Download the generated HTML file with one click
- **Chat History**: Maintain context across multiple iterations

### Technical Features

- **Modular Architecture**: Clean separation of concerns with well-organized modules
- **Provider Abstraction**: Easy to add new AI providers
- **Single-File Output**: All CSS and JavaScript are embedded in a single HTML file
- **Responsive Design**: Generated websites are mobile-friendly by default
- **Modern UI/UX**: Clean, gradient-based interface with smooth animations
- **Secure API Key Handling**: No hardcoded keys - use secrets or input field
- **Type Hints**: Full type annotations for better code quality
- **Test Coverage**: Unit tests for core functionality

---

## AI Providers

### Supported Providers

| Provider | Key Prefix | Free Tier | Description |
|----------|------------|-----------|-------------|
| **OpenRouter** | `sk-or-` | ✅ Yes | Unified access to multiple LLMs |
| **OpenAI** | `sk-` | ❌ No | GPT-4, GPT-3.5, o1 models |
| **Anthropic** | `sk-ant-` | ❌ No | Claude 3 models |
| **Groq** | `gsk_` | ✅ Yes | Ultra-fast inference |
| **Custom** | Any | - | Your own API endpoint |

### Available Models

#### OpenRouter (Free)
- Llama 3.2 3B, 1B
- Llama 3.1 8B
- Qwen 2 7B
- Gemma 2 9B
- Mistral 7B
- DeepSeek R1, Chat

#### OpenAI
- GPT-4o, GPT-4o Mini
- GPT-4 Turbo
- GPT-3.5 Turbo
- o1 Preview, o1 Mini

#### Anthropic
- Claude 3.5 Sonnet
- Claude 3.5 Haiku
- Claude 3 Opus, Sonnet, Haiku

#### Groq (Free Tier)
- Llama 3.3 70B
- Llama 3.1 8B, 3.2 1B/3B
- Mixtral 8x7B
- Gemma 2 9B

---

## Installation

### Prerequisites

- Python 3.8 or higher
- API Key from any supported provider

### Quick Start

```bash
# Clone the repository
git clone https://github.com/insydr/ai-website-generator.git
cd ai-website-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/ai_website_generator/app.py
```

### Configuration

Create a `.streamlit/secrets.toml` file to store your API keys securely:

```toml
# .streamlit/secrets.toml

# OpenRouter (recommended for free tier)
openrouter_api_key = "sk-or-v1-..."

# Or use other providers
# openai_api_key = "sk-..."
# anthropic_api_key = "sk-ant-..."
# groq_api_key = "gsk_..."

# Generic fallback
# api_key = "your-api-key"
```

---

## Usage

### Running the Application

```bash
# Method 1: Direct execution
streamlit run src/ai_website_generator/app.py

# Method 2: As a Python module
python -m ai_website_generator

# Method 3: After pip install
ai-website-generator
```

### Basic Workflow

1. **Select Provider**: Choose your AI provider from the dropdown
2. **Enter API Key**: Input your API key (or configure in secrets)
3. **Choose Model**: Select a model or enter a custom model ID
4. **Describe Website**: Enter a detailed description of the website you want
5. **Generate**: Click "Generate Website" and wait for the AI
6. **Preview**: View the live preview in the right panel
7. **Download**: Click "Download HTML File" to save the code

### Custom Provider Setup

To use a custom API endpoint:

1. Select "Custom API" from the provider dropdown
2. Enter your API key (if required)
3. Enter your model name
4. Enter the full API endpoint URL
5. Generate as normal!

### Tips for Best Results

```
❌ "Make a landing page"
✅ "Create a landing page for a SaaS product with a dark theme,
    purple accents, hero section with CTA, features grid,
    testimonials carousel, and pricing table"
```

---

## Project Structure

```
ai-website-generator/
├── src/
│   └── ai_website_generator/
│       ├── __init__.py              # Package initialization
│       ├── __main__.py              # Module entry point
│       ├── app.py                   # Main application class
│       ├── config.py                # Configuration management
│       ├── constants.py             # Application constants
│       ├── providers/               # AI provider implementations
│       │   ├── __init__.py
│       │   ├── base.py              # Base provider class
│       │   ├── registry.py          # Provider registry
│       │   ├── openrouter.py
│       │   ├── openai.py
│       │   ├── anthropic.py
│       │   ├── groq.py
│       │   └── custom.py            # Custom endpoint support
│       ├── ui/                      # UI components
│       │   ├── __init__.py
│       │   ├── components.py
│       │   └── styles.py
│       └── utils/                   # Utilities
│           ├── __init__.py
│           ├── code_extractor.py
│           └── session.py
├── tests/
│   ├── __init__.py
│   ├── test_code_extractor.py
│   └── test_session.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Programmatic Usage

```python
from ai_website_generator import (
    get_provider,
    ProviderConfig,
    ProviderType,
)

# Configure provider
config = ProviderConfig(
    provider_type=ProviderType.OPENROUTER,
    api_key="sk-or-your-key",
    model="meta-llama/llama-3.2-3b-instruct:free",
    temperature=0.7,
    max_tokens=4000,
)

# Create provider instance
provider = get_provider(config)

# Generate website
messages = [
    {"role": "user", "content": "Create a coffee shop landing page"}
]

response = provider.chat(messages)

if response.success:
    print(response.content)
else:
    print(f"Error: {response.error}")
```

---

## Getting API Keys

### OpenRouter (Recommended for Free Tier)
1. Visit [openrouter.ai](https://openrouter.ai)
2. Sign up (Google, GitHub, or Email)
3. Go to [Keys](https://openrouter.ai/keys)
4. Create a new key

### OpenAI
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up / Log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Create a new key

### Anthropic
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up / Log in
3. Create a new API key

### Groq
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to [API Keys](https://console.groq.com/keys)
4. Create a new key

---

## Development

### Running Tests

```bash
pytest

# With coverage
pytest --cov=ai_website_generator
```

### Code Quality

```bash
black src tests
isort src tests
flake8 src tests
mypy src
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid API Key | Check key format matches provider (sk-or-, sk-, sk-ant-, gsk_) |
| Rate Limit | Wait and retry, or switch to a different provider |
| Model Not Found | Check model ID is correct for your provider |
| Custom Endpoint Error | Verify URL is correct and accessible |

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ❤️ by Sydr Dev**

⭐ Star this repo if you find it useful! ⭐

</div>

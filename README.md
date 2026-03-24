# AI Website Generator Agent

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-6366F1?style=for-the-badge&logo=openai&logoColor=white)

**Transform your ideas into beautiful websites with AI**

A powerful Streamlit application that generates complete, production-ready websites (HTML/CSS/JS) from natural language descriptions using OpenRouter API.

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Project Structure](#project-structure)

</div>

---

## Features

### Core Features

- **Natural Language to Website**: Describe your website in plain English and get a complete, functional HTML/CSS/JS code
- **Live Preview**: See your generated website instantly in the built-in preview panel
- **Code Download**: Download the generated HTML file with one click
- **Chat History**: Maintain context across multiple iterations
- **Model Selection**: Choose from multiple free AI models

### Technical Features

- **Modular Architecture**: Clean separation of concerns with well-organized modules
- **Single-File Output**: All CSS and JavaScript are embedded in a single HTML file
- **Responsive Design**: Generated websites are mobile-friendly by default
- **Modern UI/UX**: Clean, gradient-based interface with smooth animations
- **Secure API Key Handling**: No hardcoded keys - use secrets or input field
- **Comprehensive Error Handling**: Clear error messages for API issues
- **Type Hints**: Full type annotations for better code quality
- **Test Coverage**: Unit tests for core functionality

---

## Demo

### Example Prompts

Here are some prompts you can try:

```
🏠 "Landing page for a real estate company with property listings, search filters, and contact form"

☕ "Coffee shop website with dark theme, menu section, location map, and online ordering"

💼 "Personal portfolio for a software developer with project showcase, skills, and contact info"

🛒 "E-commerce product page with image gallery, reviews, and add to cart functionality"

📊 "Analytics dashboard with charts, metrics cards, and data tables"

🍕 "Restaurant website with menu, reservation form, and customer testimonials"
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenRouter API Key (free tier available)

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

### Development Installation

```bash
# Install with development dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run tests
pytest

# Format code
black src tests
isort src tests

# Type check
mypy src
```

### Configuration

Create a `.streamlit/secrets.toml` file to store your API key securely:

```toml
# .streamlit/secrets.toml
openrouter_api_key = "sk-or-your-api-key-here"
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

1. **Enter API Key**: Input your OpenRouter API key in the sidebar (or configure in secrets)
2. **Select Model**: Choose an AI model from the dropdown
3. **Describe Website**: Enter a detailed description of the website you want
4. **Generate**: Click "Generate Website" and wait for the AI
5. **Preview**: View the live preview in the right panel
6. **Download**: Click "Download HTML File" to save the code

### Tips for Best Results

#### Be Specific About Design

```
❌ "Make a landing page"
✅ "Create a landing page for a SaaS product with a dark theme,
    purple accents, hero section with CTA, features grid,
    testimonials carousel, and pricing table"
```

#### Describe Interactive Elements

```
❌ "Add a menu"
✅ "Add a sticky navigation menu with smooth scroll,
    mobile hamburger menu, and hover effects"
```

---

## Project Structure

```
ai-website-generator/
├── src/
│   └── ai_website_generator/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Module entry point
│       ├── app.py               # Main application class
│       ├── config.py            # Configuration management
│       ├── constants.py         # Application constants
│       ├── api/
│       │   ├── __init__.py
│       │   └── openrouter.py    # OpenRouter API client
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── components.py    # UI components
│       │   └── styles.py        # CSS styling
│       └── utils/
│           ├── __init__.py
│           ├── code_extractor.py # Code extraction utilities
│           └── session.py        # Session state management
├── tests/
│   ├── __init__.py
│   ├── test_code_extractor.py
│   └── test_session.py
├── .streamlit/
│   └── secrets.toml.example     # Example secrets config
├── pyproject.toml               # Project metadata & build config
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

### Module Overview

| Module | Description |
|--------|-------------|
| `app.py` | Main application class and entry point |
| `config.py` | Configuration management with secrets support |
| `constants.py` | All constant values (models, prompts, etc.) |
| `api/openrouter.py` | OpenRouter API client with error handling |
| `ui/components.py` | Reusable Streamlit UI components |
| `ui/styles.py` | Custom CSS styling |
| `utils/code_extractor.py` | HTML code extraction from AI responses |
| `utils/session.py` | Session state management |

---

## Available Models

The app includes these free models (sorted by latency):

| Model | Context | Best For |
|-------|---------|----------|
| Llama 3.2 3B | 128K | Fast, general purpose |
| Llama 3.2 1B | 128K | Ultra-fast, simple sites |
| Llama 3.1 8B | 128K | Balanced speed/quality |
| Qwen 2 7B | 32K | Good for complex designs |
| Gemma 2 9B | 8K | High quality output |
| Mistral 7B | 32K | Fast and capable |
| DeepSeek R1 | 128K | Complex reasoning |
| DeepSeek Chat | 128K | Conversational |

---

## Getting OpenRouter API Key

1. **Visit OpenRouter**: Go to [openrouter.ai](https://openrouter.ai)
2. **Sign Up**: Create a free account (Google, GitHub, or Email)
3. **Navigate to Keys**: Go to [openrouter.ai/keys](https://openrouter.ai/keys)
4. **Create Key**: Click "Create Key" and give it a name
5. **Copy Key**: Copy the key (starts with `sk-or-`)
6. **Add to App**: Paste in sidebar input or add to secrets

**Free Tier**: Many models are completely free, no credit card required!

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_website_generator

# Run specific test file
pytest tests/test_code_extractor.py -v
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Lint
flake8 src tests

# Type check
mypy src
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file path: `src/ai_website_generator/app.py`
5. Add `openrouter_api_key` to secrets
6. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/ai_website_generator/app.py", \
    "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid API Key | Verify key starts with `sk-or-`, check for extra spaces |
| Rate Limit Exceeded | Wait a few minutes or try a different model |
| Model Overloaded | Switch models or wait for traffic to decrease |
| Could not extract HTML | Try regenerating with more specific prompt |
| Preview Not Loading | Check browser console, download and open locally |

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests and linting (`pytest && black src tests`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## License

This project is open source and available under the MIT License.

---

## Acknowledgments

- [Streamlit](https://streamlit.io) - The fastest way to build Python apps
- [OpenRouter](https://openrouter.ai) - Unified API for LLMs
- [Meta Llama](https://ai.meta.com/llama/) - Open source LLM
- [Mistral AI](https://mistral.ai) - Open source models

---

<div align="center">

**Made with ❤️ by Sydr Dev**

⭐ Star this repo if you find it useful! ⭐

</div>

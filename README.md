# AI Website Generator Agent

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-6366F1?style=for-the-badge&logo=openai&logoColor=white)

**Transform your ideas into beautiful websites with AI**

A powerful Streamlit application that generates complete, production-ready websites (HTML/CSS/JS) from natural language descriptions using OpenRouter API.

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration)

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

- **Single-File Output**: All CSS and JavaScript are embedded in a single HTML file
- **Responsive Design**: Generated websites are mobile-friendly by default
- **Modern UI/UX**: Clean, gradient-based interface with smooth animations
- **Secure API Key Handling**: No hardcoded keys - use secrets or input field
- **Error Handling**: Comprehensive error messages for API issues

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

### Step 1: Clone or Download

```bash
# If you have the files, navigate to the project directory
cd ai-website-generator
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key (Optional)

Create a `.streamlit/secrets.toml` file to store your API key securely:

```toml
# .streamlit/secrets.toml
openrouter_api_key = "sk-or-your-api-key-here"
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## Usage

### Basic Usage

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

#### Mention Color Schemes

```
❌ "Make it look nice"
✅ "Use a modern color palette with #667eea as primary, 
    dark background (#1a1a2e), and white text"
```

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `openrouter_api_key` | Your OpenRouter API key | Yes (via secrets or input) |

### Available Models

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

### Step-by-Step Guide

1. **Visit OpenRouter**: Go to [openrouter.ai](https://openrouter.ai)

2. **Sign Up**: Create a free account using:
   - Google
   - GitHub
   - Email

3. **Navigate to Keys**: Go to [openrouter.ai/keys](https://openrouter.ai/keys)

4. **Create Key**: Click "Create Key" and give it a name

5. **Copy Key**: Copy the key (starts with `sk-or-`)

6. **Add to App**: 
   - Paste in the sidebar input, OR
   - Add to `.streamlit/secrets.toml`

### Free Tier Limits

- Many models are completely free
- No credit card required for free models
- Rate limits apply (usually 20 requests/minute)

---

## Project Structure

```
ai-website-generator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .streamlit/
    └── secrets.toml          # API key configuration (create this)
```

---

## API Reference

### OpenRouter Integration

The app uses OpenRouter's chat completions API:

```python
# Endpoint
POST https://openrouter.ai/api/v1/chat/completions

# Headers
Authorization: Bearer {API_KEY}
HTTP-Referer: https://your-app-url.com
X-Title: AI Website Generator
Content-Type: application/json

# Body
{
    "model": "meta-llama/llama-3.2-3b-instruct:free",
    "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ],
    "temperature": 0.7,
    "max_tokens": 4000
}
```

---

## Troubleshooting

### Common Issues

#### "Invalid API Key"
- Verify your key starts with `sk-or-`
- Check for extra spaces or newlines
- Ensure key is active at openrouter.ai/keys

#### "Rate Limit Exceeded"
- Wait a few minutes before trying again
- Try a different model
- Free tier has 20 requests/minute limit

#### "Model Overloaded"
- Switch to a different model
- Wait a few minutes
- Peak hours may have more traffic

#### "Could not extract HTML"
- Try regenerating with more specific prompt
- Check if model returned an error message
- Try a larger model (Llama 3.1 8B)

#### Preview Not Loading
- Check browser console for errors
- The HTML might have embedded scripts blocked by browser
- Try downloading and opening locally

---

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use secrets.toml** for local development
3. **Use environment variables** for production deployment
4. **Regenerate keys** if accidentally exposed
5. **Monitor usage** at openrouter.ai/activity

---

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
3. Add `openrouter_api_key` to secrets
4. Deploy!

### Other Platforms

The app can be deployed to any platform supporting Python:

- **Heroku**: Add `Procfile` with `web: streamlit run app.py`
- **Railway**: Auto-detects Streamlit
- **Render**: Use Streamlit runtime
- **Docker**: See Dockerfile example below

<details>
<summary>Docker Deployment</summary>

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t ai-website-generator .
docker run -p 8501:8501 ai-website-generator
```

</details>

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

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

**Made with ❤️ by AI**

⭐ Star this repo if you find it useful! ⭐

</div>

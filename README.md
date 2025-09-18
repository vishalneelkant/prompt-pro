# 🤖 AI Prompt Engineer

An advanced AI-powered prompt engineering platform that intelligently selects and applies the best prompting strategies to transform your ideas into powerful, effective prompts for AI systems.

## ✨ Features

- **🧠 Enhanced Intent Analysis**: Deep understanding of user requirements and coding goals
- **🚀 Cursor Code Optimizer**: Specialized optimization for Cursor AI development workflows
- **🎯 Smart Strategy Selection**: Automatically identifies the best prompting strategy for your use case
- **✨ AI-Powered Engineering**: Uses GPT-4 to transform ideas into comprehensive development prompts
- **📱 Modern Interface**: Beautiful, responsive web UI with accessibility features
- **⚡ Real-time Processing**: Instant prompt optimization with detailed feedback and analysis

## 🏗️ Architecture

- **Frontend**: React.js with modern, responsive UI and accessibility features
- **Backend**: Flask API with CORS support and enhanced cursor optimization
- **AI Integration**: OpenAI GPT-4 + Pinecone vector database
- **Enhanced Features**: Advanced intent analysis, comprehensive strategy selection, and detailed planning

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Pinecone API key
- OpenAI API key

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd project_prompt_optimizer
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
# Pinecone Configuration
PINECONE=your_pinecone_api_key_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install Dependencies

**Backend (Python):**
```bash
pip install -r requirements.txt
```

**Frontend (React):**
```bash
npm install
```

### 4. Run the Application

**Start the Backend API:**
```bash
python api.py
```
The API will run at `http://localhost:5000`

**Start the Frontend (in a new terminal):**
```bash
npm start
```
The React app will open at `http://localhost:3000`

## 🔧 API Endpoints

- `GET /health` - Health check
- `POST /optimize` - Optimize a prompt
- `GET /strategies` - Get available strategies

## 📱 Usage

1. **Open the web interface** at `http://localhost:3000`
2. **Select your context** (General, Cursor Code Optimizer, Rephrase, etc.)
3. **Type your prompt or idea** in the input field
4. **Click "🚀 Optimize"** or press Enter
5. **View the enhanced prompt** with detailed analysis, intent understanding, and implementation guidance
5. **Chat history** is automatically saved during your session

## 🎯 Enhanced Capabilities

### 🚀 Cursor Code Optimizer
- **Intent Analysis**: Automatically detects user goals (new features, debugging, refactoring)
- **Technology Recognition**: Identifies mentioned technologies and frameworks
- **Comprehensive Planning**: Generates detailed implementation roadmaps
- **Strategy Selection**: Chooses optimal approach based on complexity and context

### 📝 General Optimization
- **Few-shot prompting**: Provide examples before the query
- **Chain-of-thought**: Step-by-step reasoning
- **Zero-shot prompting**: Direct queries without examples
- **Role prompting**: Assign specific roles to the AI
- **Self-consistency**: Multiple reasoning paths

## 🛠️ Development

### Project Structure
```
project_prompt_optimizer/
├── api.py              # Flask backend API
├── main.py             # Original CLI script
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
├── public/             # React public assets
├── src/                # React source code
│   ├── App.js         # Main React component
│   ├── App.css        # Component styles
│   ├── index.js       # React entry point
│   └── index.css      # Global styles
└── .env                # Environment variables
```

### Running Tests
```bash
# Backend tests
python -m pytest

# Frontend tests
npm test
```

### Building for Production
```bash
npm run build
```

## 🔒 Security Notes

- Never commit your `.env` file
- Keep API keys secure
- The `.env` file is already in `.gitignore`

## 🐛 Troubleshooting

### Common Issues

1. **"Import could not be resolved"**
   - Run `pip install -r requirements.txt`
   - Restart your IDE

2. **"Failed to resolve api.pinecone.io"**
   - Check internet connection
   - Verify API key in `.env` file
   - Check firewall/proxy settings

3. **"Module not found" errors**
   - Ensure all dependencies are installed
   - Check Python/Node.js versions

### Network Issues
- If behind corporate firewall, try mobile hotspot
- Check DNS resolution: `nslookup api.pinecone.io`
- Verify proxy settings if applicable

# Prompt Optimizer API

This project is a Flask-based API for optimizing prompts for LLMs and generative models. It supports context-aware strategies for business, technical, academic, marketing, image, and video generation.

## Features
- Context-aware prompt optimization
- Image and video generation strategies
- Text rephrasing and grammar correction
- API endpoints for health, optimization, and strategy listing

## Local Development
1. Clone the repo:
   ```sh
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
2. Install dependencies:
   ```sh
python3 -m pip install -r requirements.txt
```
3. Create a `.env` file in the project root:
   ```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENV=us-east-1
```
4. Run the API:
   ```sh
python3 api.py
```

## Deployment on Vercel
Vercel is designed for serverless Node.js/Next.js apps, but you can deploy Python APIs using [Vercel Python](https://vercel.com/docs/functions/python) serverless functions or use [Vercel's Flask template](https://github.com/vercel/examples/tree/main/python/flask-app).

### Steps:
1. Push your code to GitHub (see above).
2. Go to [vercel.com](https://vercel.com/) and import your repo.
3. Set up environment variables in Vercel dashboard (`OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_ENV`).
4. If using Flask, ensure your entry point is `api.py` and expose endpoints using Vercel's Python function conventions.
5. For production, use only environment variables for secrets. Never commit `.env` to GitHub.

## Security
- `.env` is in `.gitignore` and will NOT be published.
- Never hardcode API keys in your code.
- Use Vercel's environment variable dashboard for deployment secrets.

## API Endpoints
- `GET /health` — Health check
- `POST /optimize` — Optimize a prompt (JSON: `{ "prompt": "...", "context": "..." }`)
- `GET /strategies` — List available strategies and contexts

## License
MIT

---
For Vercel deployment help, see [Vercel Python Functions](https://vercel.com/docs/functions/python) or ask for a deployment-ready template.

---

**Happy Prompt Optimizing! 🎉**

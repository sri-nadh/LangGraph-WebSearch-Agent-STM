# 🔍 WebSearch Agent with Short-Term Memory

A modern, LangGraph-powered autonomous agent with web search capabilities, featuring a beautiful web interface and memory for conversational context.

## 🚀 Overview

This project demonstrates how to build a sophisticated web search agent using [LangGraph](https://github.com/langchain-ai/langgraph) with a FastAPI backend and modern web frontend. The agent maintains conversational memory and provides an intuitive chat interface for real-time web searches.

## 🧠 Features

* ✅ **Modern Web Interface**: Beautiful, responsive chat UI with real-time interactions
* ✅ **Web Search Integration**: Uses Tavily Search for real-time web information retrieval
* ✅ **Short-Term Memory**: Maintains conversational context across interactions
* ✅ **LangGraph Integration**: State-based agent architecture with tool routing
* ✅ **FastAPI Backend**: RESTful API with proper error handling and validation
* ✅ **Real-time Feedback**: Typing indicators and smooth message animations
* ✅ **Session Management**: Proper conversation threading and termination handling

## 🧱 Built With

* [LangGraph](https://github.com/langchain-ai/langgraph) - State machine for language model agents
* [LangChain](https://github.com/langchain-ai/langchain) - Framework for developing with LLMs
* [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
* [OpenAI](https://platform.openai.com/) - GPT-4 language model backend
* [Tavily Search](https://tavily.com/) - Web search tool for real-time queries

## 📁 Project Structure

```
├── WebSearch-Agent-Short_memory.py  # FastAPI backend with LangGraph agent
├── Static/
│   └── index.html                   # Modern web interface
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🛠️ Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd Websearch-Agent-With-Short-Term-Memory
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the project root:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Tavily Search API Key (for enhanced search)
TAVILY_API_KEY=your_tavily_api_key_here
```

> **Note**: Get your API keys from:
> - OpenAI: https://platform.openai.com/api-keys
> - Tavily: https://tavily.com/ (optional, but recommended for better search results)

### 4. Run the Application

```bash
python WebSearch-Agent-Short_memory.py
```

Or using uvicorn directly:

```bash
uvicorn WebSearch-Agent-Short_memory:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:8000
```

## 🖥️ Usage

1. **Start a Conversation**: Type your question in the chat input
2. **Web Search Queries**: Ask about current events, recent information, or any topic requiring web search
3. **Conversational Context**: The agent remembers previous messages in the conversation
4. **Session Management**: Type "quit", "exit", or "bye" to end the session
5. **Clear Chat**: Use the clear button to reset the conversation

### Example Interactions

```
User: What are the latest developments in AI technology?
Agent: [Searches web and provides current information about AI developments]

User: Tell me more about the companies mentioned
Agent: [Uses conversation context to provide details about previously mentioned companies]
```

## 🔧 API Endpoints

- `GET /` - Serves the web interface
- `POST /websearch-agent/` - Chat endpoint for agent interactions
- `GET /health` - Health check endpoint

## 🎨 Features Showcase

- **Beautiful UI**: Modern gradient design with smooth animations
- **Responsive**: Works perfectly on desktop and mobile devices
- **Real-time Feedback**: Typing indicators and loading states
- **Error Handling**: Graceful error messages and recovery
- **Session Management**: Proper conversation threading
- **Accessibility**: Keyboard shortcuts and focus management

## 🚀 Deployment

The application is ready for deployment on platforms like:
- Heroku
- Vercel
- Railway
- DigitalOcean App Platform
- Any Docker-compatible platform

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).


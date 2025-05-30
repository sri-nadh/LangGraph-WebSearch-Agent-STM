# 🔍 WebSearch Agent with Short-Term Memory

A modern, LangGraph-powered autonomous agent with web search capabilities, featuring a beautiful web interface, dynamic session management, and isolated conversation memory.

## 🚀 Overview

This project demonstrates how to build a sophisticated web search agent using [LangGraph](https://github.com/langchain-ai/langgraph) with a FastAPI backend and modern web frontend. The agent maintains conversational memory through dynamic session management, ensuring each conversation is completely isolated with its own memory context.

## 🧠 Features

* ✅ **Modern Web Interface**: Beautiful, responsive chat UI with real-time interactions
* ✅ **Dynamic Session Management**: Automatic thread ID generation for isolated conversations
* ✅ **Web Search Integration**: Uses Tavily Search for real-time web information retrieval
* ✅ **Isolated Memory**: Each session maintains separate conversational context
* ✅ **LangGraph Integration**: State-based agent architecture with tool routing
* ✅ **FastAPI Backend**: RESTful API with proper error handling and validation
* ✅ **Real-time Feedback**: Typing indicators and smooth message animations
* ✅ **Session Control**: Fresh sessions on page refresh or manual chat clearing
* ✅ **Multi-Tab Support**: Different browser tabs maintain separate conversations

## 🧱 Built With

* [LangGraph](https://github.com/langchain-ai/langgraph) - State machine for language model agents
* [LangChain](https://github.com/langchain-ai/langchain) - Framework for developing with LLMs
* [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
* [OpenAI](https://platform.openai.com/) - GPT-4 language model backend
* [Tavily Search](https://tavily.com/) - Web search tool for real-time queries

## 📁 Project Structure

```
├── main.py                          # FastAPI application and routes
├── agent.py                         # LangGraph agent logic and session management
├── models.py                        # Pydantic models, schemas, and configuration
├── Static/
│   └── index.html                   # Modern web interface
├── requirements.txt                 # Python dependencies
├── __init__.py                      # Package initialization
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
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:8000
```

## 🖥️ Usage

1. **Automatic Session**: Each page load automatically creates a new conversation session
2. **Web Search Queries**: Ask about current events, recent information, or any topic requiring web search
3. **Conversational Context**: The agent remembers previous messages within the same session
4. **Session Management**: 
   - Type "quit", "exit", or "bye" to end the current session
   - Click "Clear" button to start a fresh session
   - Refresh the page for a completely new conversation
5. **Multi-Tab Support**: Open multiple tabs for parallel conversations

### Example Interactions

```
User: What are the latest developments in AI technology?
Agent: [Searches web and provides current information about AI developments]

User: Tell me more about the companies mentioned
Agent: [Uses conversation context to provide details about previously mentioned companies]

User: [Clicks Clear button - starts fresh session with no memory of previous conversation]
```


### Key Components

#### **File Structure & Responsibilities:**
- **`main.py`**: FastAPI application, HTTP routes, and server configuration
- **`agent.py`**: WebSearchAgent class with LangGraph logic and session management
- **`models.py`**: Pydantic schemas, TypedDict definitions, and utility functions
- **`Static/index.html`**: Frontend interface with session management

#### **Core Components:**
- **Session Generator**: Creates unique thread IDs for conversation isolation
- **WebSearchAgent Class**: Encapsulates chatbot node, tool node, and graph management
- **Chatbot Node**: Processes user messages and determines when to use tools
- **Tool Node**: Handles web search operations via Tavily
- **State Graph**: Manages conversation flow and tool routing with thread-specific memory
- **FastAPI Routes**: Provides HTTP endpoints and serves the web interface
- **Frontend Session Manager**: Handles session creation, management, and cleanup

### Memory Management
- **Isolated Conversations**: Each thread ID maintains separate conversation history
- **Automatic Cleanup**: Old sessions naturally expire without manual intervention
- **Multi-Tab Support**: Different browser tabs/windows maintain independent sessions
- **Session Recovery**: Automatic session creation if current session becomes invalid

## 🔄 Session Flow Example

1. **User opens page** → Frontend calls `/new-session/`
2. **Backend generates** → `thread_20241215_143022_a7b3c4d5`
3. **User sends message** → `{"message": "Hello", "thread_id": "thread_20241215_143022_a7b3c4d5"}`
4. **Backend processes** → Uses thread-specific memory context
5. **User clears chat** → Frontend creates new session with different thread ID
6. **Fresh conversation** → No memory of previous interactions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas for potential improvement:
- Session persistence across browser sessions
- Conversation export/import functionality
- Enhanced memory management options
- Additional search providers

## 📄 License

This project is open source and available under the [MIT License](LICENSE).


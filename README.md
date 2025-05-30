# 🔍 WebSearch Agent with Short-Term Memory

A modern, LangGraph-powered autonomous agent with web search capabilities, featuring a beautiful web interface, dynamic session management, and isolated conversation memory.

## 🚀 Overview

This project demonstrates how to build a sophisticated web search agent using [LangGraph](https://github.com/langchain-ai/langgraph) with a FastAPI backend and modern web frontend. The agent maintains conversational memory through dynamic session management, ensuring each conversation is completely isolated with its own memory context.

## 🎨 Features Showcase

- **Beautiful UI**: Modern gradient design with smooth animations
- **Responsive**: Works perfectly on desktop and mobile devices
- **Real-time Feedback**: Typing indicators and loading states
- **Error Handling**: Graceful error messages and recovery
- **Session Isolation**: Each conversation is completely independent
- **Function-Based Design**: Clean, maintainable codebase with simple functions
- **Rich Text Formatting**: Automatic formatting for numbered lists, bold text, and structured content
- **Single Welcome Message**: Clean UI with no duplicate messages
- **Accessibility**: Keyboard shortcuts and focus management

## 🧠 Features

* ✅ **Modern Web Interface**: Beautiful, responsive chat UI with real-time interactions
* ✅ **Dynamic Session Management**: Automatic thread ID generation for isolated conversations
* ✅ **Function-Based Architecture**: Clean, maintainable function-based agent design
* ✅ **Web Search Integration**: Uses Tavily Search for real-time web information retrieval
* ✅ **Isolated Memory**: Each session maintains separate conversational context
* ✅ **LangGraph Integration**: State-based agent architecture with tool routing
* ✅ **FastAPI Backend**: RESTful API with proper error handling and validation
* ✅ **Real-time Feedback**: Typing indicators and smooth message animations
* ✅ **Session Control**: Fresh sessions on page refresh or manual chat clearing
* ✅ **Multi-Tab Support**: Different browser tabs maintain separate conversations
* ✅ **Rich Message Formatting**: Structured responses with numbered lists, bold text, and proper spacing
* ✅ **Clean UI Experience**: Single welcome message with proper session isolation

## 🧱 Built With

* [LangGraph](https://github.com/langchain-ai/langgraph) - State machine for language model agents
* [LangChain](https://github.com/langchain-ai/langchain) - Framework for developing with LLMs
* [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
* [OpenAI](https://platform.openai.com/) - GPT-4 language model backend
* [Tavily Search](https://tavily.com/) - Web search tool for real-time queries

## 📁 Project Structure

```
├── main.py                          # FastAPI application and routes
├── agent.py                         # LangGraph agent functions and session management  
├── models.py                        # Pydantic models, schemas, and configuration
├── Static/
│   └── index.html                   # Modern web interface with session management
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
- **`agent.py`**: Function-based agent logic with LangGraph components and session management
- **`models.py`**: Pydantic schemas, TypedDict definitions, and utility functions
- **`Static/index.html`**: Frontend interface with dynamic session management and message formatting

#### **Core Functions:**
- **`process_message()`**: Main function to process user messages through the agent
- **`chatbot_node()`**: Processes user messages and determines when to use tools
- **`build_graph()`**: Creates and compiles the LangGraph state graph
- **`initialize_agent()`**: Sets up the agent components on module import
- **Session Generator**: Creates unique thread IDs for conversation isolation
- **FastAPI Routes**: Provides HTTP endpoints and serves the web interface
- **Frontend Session Manager**: Handles session creation, management, and cleanup


## 🤝 Contributing

Contributions are welcome! The function-based architecture makes it easy to contribute. Please feel free to submit a Pull Request. 

### **Development Guidelines:**
- **Function-First**: Keep the function-based approach for simplicity
- **Type Hints**: Use proper type hints for all functions
- **Documentation**: Add docstrings for new functions
- **Testing**: Consider adding unit tests for individual functions

### **Areas for Potential Improvement:**
- **Session Persistence**: Save sessions across browser restarts
- **Conversation Export**: Add functionality to export chat history
- **Enhanced Memory**: Implement configurable memory management options
- **Additional Search Providers**: Support for multiple search engines
- **Advanced Formatting**: Enhanced message formatting options
- **Performance**: Optimize for high-concurrency scenarios
- **Authentication**: Add user authentication and personal sessions

## 📄 License

This project is open source and available under the [MIT License](LICENSE).





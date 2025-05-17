# 🔍 WebSearch Agent with Short-Term Memory

A lightweight, LangGraph-powered autonomous agent capable of performing web searches and maintaining short-term memory for more effective multi-turn information retrieval.

## 🚀 Overview

This project demonstrates how to build a simple web search agent using [LangGraph](https://github.com/langchain-ai/langgraph), with a memory mechanism to retain the context of recent searches. It's ideal for lightweight use cases such as:

* Topic research
* Summarizing multi-step queries
* Conversational web search bots

## 🧠 Features

* ✅ **Web Search Integration**: Uses a tool abstraction to perform real-time web searches.
* ✅ **Short-Term Memory**: Retains recent messages (configurable buffer) to provide conversational context.
* ✅ **LangGraph Integration**: Simple graph with branching behavior based on tool use.
* ✅ **Multi-turn Support**: Capable of carrying out multi-step interactions with memory awareness.

## 🧱 Built With

* [LangGraph](https://github.com/langchain-ai/langgraph) - State machine for language model agents
* [LangChain](https://github.com/langchain-ai/langchain) - Framework for developing with LLMs
* [OpenAI](https://platform.openai.com/) - Language model backend (can be swapped)
* `TavilySearchResults` - Web search tool for real-time queries

## 📁 File Structure

```
WebSearch-Agent-Short_memory.py  # Main implementation
```

## 🛠️ Setup

### 1. Install Requirements

```bash
pip install langchain langgraph openai tavily-python
```

> ✅ Ensure you have API keys set for OpenAI and Tavily (or your web search provider).

### 2. Set API Keys

```bash
export OPENAI_API_KEY=your-openai-key
export TAVILY_API_KEY=your-tavily-key
```

### 3. Run the Script

```bash
python WebSearch-Agent-Short_memory.py
```


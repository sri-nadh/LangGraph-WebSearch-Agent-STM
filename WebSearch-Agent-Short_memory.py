from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import uuid
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

app = FastAPI(title="WebSearch Agent", description="AI Agent with web search capabilities")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# Mount static files
app.mount("/static", StaticFiles(directory="Static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("Static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Index file not found")


# Request Schema for input validation
class RequestSchema(BaseModel):
    message: str
    thread_id: str

# Response Schema
class ResponseSchema(BaseModel):
    response: str
    status: str = "success"

# New Session Response Schema
class NewSessionResponse(BaseModel):
    thread_id: str
    status: str = "success"

# state management for state graph
class State(TypedDict):
    messages: Annotated[list, add_messages]


# In-memory temporary storage for conversations
memory = MemorySaver()

graph_builder = StateGraph(State)

# Initialize search tool
search_tool = TavilySearch(max_results=2, topic="news")

tools = [search_tool]

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

llm_with_tools = llm.bind_tools(tools)

# Chatbot node
def chatbot(state: State) -> State:
    try:
        
        system_message = """
You are a helpful AI assistant with access to real-time web data via the [TavilySearch] tool. Use it effectively by following these principles:

Use [TavilySearch] when:
    a. Information may be current, dynamic, or time-sensitive.

    b. Your built-in knowledge is uncertain, outdated, or incomplete.

    c. The user explicitly asks for up-to-date or verified web content.
    
How to use it:
    a. Formulate a precise search query.

    b. Extract the most relevant and credible insights.

    c. Combine search results with your reasoning to provide a clear, accurate, and helpful answer.

Only use [TavilySearch] when necessary—prioritize efficiency, accuracy, and trust in every response.
"""

        
        response = llm_with_tools.invoke([("system", system_message)] + state["messages"])
        
        return {"messages": [response]}
    
    except Exception as e:
    
        logger.error(f"Error in chatbot node: {e}")        
        error_response = AIMessage(content="I apologize, but I encountered an error while processing your request. Please try again.")
        
        return {"messages": [error_response]}

# Tool node
tool_node = ToolNode(tools=[search_tool])

# Build the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

graph = graph_builder.compile(checkpointer=memory)

# Thread management with dynamic IDs
terminated_threads: set[str] = set()

def generate_thread_id():
    """Generate a unique thread ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"thread_{timestamp}_{unique_id}"


# New session endpoint
@app.post("/new-session/", response_model=NewSessionResponse)
async def create_new_session():
    """Create a new session with a unique thread ID"""
    try:
        new_thread_id = generate_thread_id()
        logger.info(f"Created new session with thread ID: {new_thread_id}")
        return NewSessionResponse(thread_id=new_thread_id, status="success")
    except Exception as e:
        logger.error(f"Error creating new session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create new session")


# WebSearch Agent endpoint
@app.post("/websearch-agent/", response_model=ResponseSchema)
async def websearch_agent(request: RequestSchema):
    try:
        user_message = request.message.strip()
        thread_id = request.thread_id

        if not user_message:
            raise HTTPException(status_code=400, detail="Empty message is not allowed")

        if not thread_id:
            raise HTTPException(status_code=400, detail="Thread ID is required")

        if thread_id in terminated_threads:
            return ResponseSchema(
                response="This session has ended. Please refresh or start a new session to chat again.",
                status="session_ended"
            )
        
        if user_message.lower() in ["quit", "exit", "bye"]:
            terminated_threads.add(thread_id)
            return ResponseSchema(
                response="Ok bye, it was nice chatting with you. Have a good rest of the day!",
                status="session_ended"
            )
        
        # Create config with the dynamic thread ID
        config = {"configurable": {"thread_id": thread_id}}
        
        # Process the message through the graph
        result = graph.invoke({"messages": [("user", user_message)]}, config)
        response = result["messages"][-1].content
        return ResponseSchema(response=response, status="success")
        
    except Exception as e:
        logger.error(f"Error in websearch_agent: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

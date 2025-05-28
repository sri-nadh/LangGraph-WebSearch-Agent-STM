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

# Response Schema
class ResponseSchema(BaseModel):
    response: str
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
        system_message = (
            "You are a helpful AI assistant with access to web search capabilities via TavilySearch. "
            "If you don't know the answer to a question or need current information, use the search tool "
            "to find relevant information and provide a comprehensive answer based on the search results."
        )
        
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


# Thread management 
Thread_Id = "First_Thread"
config = {"configurable": {"thread_id": Thread_Id}}
terminated_threads: set[str] = set()


# WebSearch Agent endpoint
@app.post("/websearch-agent/", response_model=ResponseSchema)
async def websearch_agent(request: RequestSchema):
    try:
        user_message = request.message.strip()

        if not user_message:
            raise HTTPException(status_code=400, detail="Empty message is not allowed")

        if Thread_Id in terminated_threads:
            return ResponseSchema(
                response="This session has ended. Please refresh or start a new session to chat again.",
                status="session_ended"
            )
        
        if user_message.lower() in ["quit", "exit", "bye"]:
            terminated_threads.add(Thread_Id)
            return ResponseSchema(
                response="Ok bye, it was nice chatting with you. Have a good rest of the day!",
                status="session_ended"
            )
        
        # Process the message through the graph
        for event in graph.stream({"messages": [("user", user_message)]}, config):
            for value in event.values():
                return ResponseSchema(
                    response=value["messages"][-1].content,
                    status="success"
                )
        
        # Fallback response if no events are generated
        return ResponseSchema(
            response="I apologize, but I couldn't process your request at this time.",
            status="error"
        )
        
    except Exception as e:
        logger.error(f"Error in websearch_agent: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

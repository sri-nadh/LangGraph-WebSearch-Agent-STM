from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from fastapi import FastAPI,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

api_key= os.getenv("OPENAI-API-KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"]
)


app.mount("/Static",StaticFiles(directory="Static"),name="Static")

@app.get("/",response_class= HTMLResponse)
async def read_index():
    with open("/static/index.html","r",encoding= "utf-8") as f:
        return f.read()



class RequestSchema(BaseModel):
    message: str


# Class for Stategraph to manage State across the graph nodes.
class State(TypedDict):
    messages: Annotated[list, add_messages]



# in-memory temporory storage for a single long conv
memory=MemorySaver()

graph_builder = StateGraph(State)

search_tool=TavilySearch(max_results=2,topic="news")

tools = [search_tool]

llm = ChatOpenAI(model="gpt-4o",api_key=api_key)

llm_with_tools = llm.bind_tools(tools)


#chat bot node
def chatbot(state: State)-> State:
    
    response= llm_with_tools.invoke([("system","you are a chatbot, with acces to [TavilySearch] Tool. so if you dont know the answer to question , use the tool to websearch and then use its result to come up with a better answer ")]+state["messages"])
    
    return {"messages": [response]}


# Tavily Search Node
tool_node = ToolNode(tools=[search_tool])


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)


graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)


# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

graph = graph_builder.compile(checkpointer=memory)

Thread_Id = "First_Thread"

# Writing the memory to thread with id "1"
config = {"configurable": {"thread_id": Thread_Id}}

terminated_threads : set[str] = set()


@app.post("/websearch-agent/", response_class= JSONResponse)
async def WebSearch_Agent(request : RequestSchema):
    
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="Empty Message is not Allowed")

    if Thread_Id in terminated_threads :
        return JSONResponse(content="This session has ended. Please refresh or start a new session to chat again.")
    
    if user_message.lower() in ["quit", "exit", "bye"]:
        
        terminated_threads.add(Thread_Id)
        return JSONResponse(content="Ok bye, it was nice chatting with you. Have a good rest of the day!")
        

    # Process user input through the LangGraph
    for event in graph.stream({"messages": [("user", user_message)]}, config):
        for value in event.values():
            return JSONResponse(content={"response" : value["messages"][-1].content})

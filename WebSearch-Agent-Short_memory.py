from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict
import os
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]


# in-memory temporory storage for a single long conv
memory=MemorySaver()

api_key= os.getenv("OPENAI-API-KEY")

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


# Writing the memory to thread with id "1"
config = {"configurable": {"thread_id": "1"}}


# Defining Loop to have a continuous conversation
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    # Process user input through the LangGraph
    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

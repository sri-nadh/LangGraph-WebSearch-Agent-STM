from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from models import State, OPENAI_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

memory = MemorySaver()
terminated_threads: set[str] = set()
graph = None
llm_with_tools = None


def chatbot_node(state: State) -> State:
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


def build_graph():
    global graph, llm_with_tools
    
    graph_builder = StateGraph(State)
    
    search_tool = TavilySearch(max_results=2, topic="news")
    tools = [search_tool]
    
    llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)
    
    tool_node = ToolNode(tools=[search_tool])
    
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_node("tools", tool_node)
    
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.set_entry_point("chatbot")
    
    graph = graph_builder.compile(checkpointer=memory)
    
    return graph


def process_message(user_message: str, thread_id: str):
    global graph, terminated_threads
    
    # Initialize graph if not already built
    if graph is None:
        build_graph()
    
    try:
        # Check if thread is terminated
        if thread_id in terminated_threads:
            return {
                "response": "This session has ended. Please refresh or start a new session to chat again.",
                "status": "session_ended"
            }
        
        if user_message.lower() in ["quit", "exit", "bye"]:
            terminated_threads.add(thread_id)
            return {
                "response": "Ok bye, it was nice chatting with you. Have a good rest of the day!",
                "status": "session_ended"
            }
        
        # Create config with the dynamic thread ID
        config = {"configurable": {"thread_id": thread_id}}
        
        # Process the message through the graph
        result = graph.invoke({"messages": [("user", user_message)]}, config)
        response = result["messages"][-1].content
        
        return {"response": response, "status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {
            "response": "I apologize, but I encountered an error while processing your request. Please try again.",
            "status": "error"
        }


def initialize_agent():
    """Initialize the agent by building the graph"""
    logger.info("Initializing WebSearch Agent...")
    build_graph()
    logger.info("WebSearch Agent initialized successfully")


# Initialize the agent when module is imported
initialize_agent() 
from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

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

# State management for state graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

def generate_thread_id():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"thread_{timestamp}_{unique_id}" 
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from models import RequestSchema, ResponseSchema, NewSessionResponse, generate_thread_id
from agent import process_message
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="Static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve the main web interface"""
    try:
        with open("Static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Index file not found")


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


@app.post("/websearch-agent/", response_model=ResponseSchema)
async def websearch_agent_endpoint(request: RequestSchema):
    """Chat endpoint for agent interactions"""
    try:
        user_message = request.message.strip()
        thread_id = request.thread_id

        if not user_message:
            raise HTTPException(status_code=400, detail="Empty message is not allowed")

        if not thread_id:
            raise HTTPException(status_code=400, detail="Thread ID is required")

        # Process message through the agent
        result = process_message(user_message, thread_id)
        
        return ResponseSchema(
            response=result["response"],
            status=result["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in websearch_agent endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
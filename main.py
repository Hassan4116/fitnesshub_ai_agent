from fastapi import FastAPI, Depends
from app.memory import save_state, load_state
from pydantic import BaseModel
from app.auth import get_current_user
from app.session import get_or_create_session
from app.agent.build_agent import build_agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Fitness Hub AI Agent")

class ChatRequest(BaseModel):
    message: str

# Build agent
agent = build_agent()


@app.post("/chat")
async def chat(req: ChatRequest, user=Depends(get_current_user)):
    session_id = get_or_create_session(user["id"])

    state = load_state(session_id) or {
        "history": [],
        "query": ""
    }

    state["query"] = req.message

    # Call the agent function directly (no longer using langgraph)
    result = agent(state)

    save_state(session_id, result)

    return {
        "session_id": session_id,
        "response": result["response"],
    }


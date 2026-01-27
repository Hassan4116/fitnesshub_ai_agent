import json
import redis
from app.config import REDIS_URL
from langchain_core.messages import AIMessage, HumanMessage

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def load_state(session_id: str):
    data = redis_client.get(session_id)
    if not data:
        return None
    state_dict = json.loads(data)
    new_history = []
    for m in state_dict.get("history", []):
        if m["type"] == "human":
            new_history.append(HumanMessage(content=m["content"]))
        elif m["type"] == "ai":
            new_history.append(AIMessage(content=m["content"]))

    return {
        **state_dict,
        "history": new_history
    }


def save_state(session_id: str, state: dict):
    to_store = {
        **state,
        "history": [
            {"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in state.get("history", [])
        ]
    }
    redis_client.set(session_id, json.dumps(to_store))
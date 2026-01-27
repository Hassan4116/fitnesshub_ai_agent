import uuid
import redis
from .config import REDIS_URL, SESSION_TTL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def get_or_create_session(user_id: str) -> str:
    key = f"support_session:{user_id}"
    session_id = redis_client.get(key)
    if session_id is None:
        session_id = str(user_id)
        redis_client.setex(key, SESSION_TTL, session_id)
    return session_id
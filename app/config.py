import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
SESSION_TTL = int(os.getenv("SESSION_TTL", 3600))

# Lazy load LLMs to avoid Windows multiprocessing issues
_llm_main = None
_llm_fallback = None

def get_llm_main():
    global _llm_main
    if _llm_main is None:
        _llm_main = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300,
        )
    return _llm_main

def get_llm_fallback():
    global _llm_fallback
    if _llm_fallback is None:
        _llm_fallback = ChatOpenAI(
            model="gpt-4o-nano",
            temperature=0.7,
            max_tokens=300,
        )
    return _llm_fallback

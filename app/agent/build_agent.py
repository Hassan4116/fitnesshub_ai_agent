from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.state import AgentState
from app.config import llm_main, llm_fallback
# System prompt that goes to LLM
PROMPT = """
You are a professional gym, fitness, and nutrition assistant.

Rules:
- ONLY answer gym, workout, fitness, or nutrition related questions.
- If user asks anything outside these topics, politely refuse.
- Give practical, safe, beginner-friendly advice.
- No medical diagnosis.
"""


def fitness_assistant_node(state: AgentState):
    """
    Single node that:
    - reads history
    - enforces system prompt
    - appends new messages
    """
    
    messages = [
        SystemMessage(content=PROMPT),
        *state.get("history", []),
        HumanMessage(content=state["query"]),
    ]
    
    try:

        response = llm_main.invoke(messages)
    except Exception as e:
        print("[fitness_assistant_node] Primary LLM failed, using fallback:", e)
        response = llm_fallback.invoke(messages)


    # Step 2: Summarize history if too long
    history = state.get("history", [])
    if len(history) > 20:  # Keep last 20 messages fully
        try:
            summary_response = llm_main.invoke([
                SystemMessage(content="Summarize the following chat history concisely, keeping context:"),
                *history[:-20]
            ])
            # Replace old history with summarized + last 20 messages
            history = [AIMessage(content=summary_response.content)] + history[-20:]
        except Exception as e:
            print("[fitness_assistant_node] Failed to summarize history:", e)

    new_history = [
        *history,
        HumanMessage(content=state["query"]),
        AIMessage(content=response.content)
    ]

    return {
        "response": response.content,
        "history": new_history
    }

def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("fitness_assistant", fitness_assistant_node)
    graph.add_edge(START, "fitness_assistant")
    graph.add_edge("fitness_assistant", END)


    return graph.compile()


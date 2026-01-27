

# Fitness Hub AI Agent

A FastAPI-based AI assistant for fitness, gym, and nutrition guidance. This agent uses LangChain with LangGraph to provide intelligent, domain-focused responses to fitness-related queries.

## Features

- **Domain-Focused AI Assistant**: Specialized in gym, fitness, and nutrition topics with built-in safeguards
- **JWT Authentication**: Secure user authentication with JWT tokens
- **Session Management**: Redis-based session persistence and state management
- **LangGraph Integration**: Modern agent architecture using LangGraph for reliable workflows
- **OpenAI GPT Integration**: Powered by OpenAI's GPT-4o model
- **Message History**: Maintains conversation history for contextual responses

## System Architecture

```
FastAPI Server
    ├── Authentication (JWT)
    ├── Session Management (Redis)
    └── AI Agent (LangGraph)
        └── LLM (OpenAI GPT-4o-mini)
```

## Installation

### Prerequisites

- Python 3.10+
- Redis server
- OpenAI API key

### Setup

1. **Clone the repository and navigate to the project**:
   ```bash
   cd fitness_hub_aiagent
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   JWT_SECRET=your_jwt_secret_key
   REDIS_URL=redis://localhost:6379
   SESSION_TTL=3600
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `JWT_SECRET` | Secret key for JWT tokens | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `SESSION_TTL` | Session time-to-live (seconds) | `3600` |

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST `/chat`

Send a message to the fitness assistant.

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "message": "What's a good beginner workout routine?"
}
```

**Response**:
```json
{
  "session_id": "user123",
  "response": "Here's a beginner-friendly workout routine..."
}
```

**Headers**:
```
Authorization: Bearer <jwt_token>
```

## Project Structure

```
fitness_hub_aiagent/
├── main.py                 # FastAPI application entry point
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── app/
    ├── __init__.py
    ├── agent/
    │   └── build_agent.py    # LangGraph agent configuration
    ├── auth.py               # JWT authentication logic
    ├── config.py             # Configuration and LLM setup
    ├── history.py            # Chat history management
    ├── memory.py             # Session state persistence
    ├── session.py            # Session creation and management
    ├── state.py              # Agent state schema
    ├── middlewares/
    │   ├── model_router.py
    │   └── summarize.py
    └── tools/                # Custom tools (extensible)
```

## Agent Behavior

The fitness assistant is configured with the following rules:

- ✅ Answers gym, workout, fitness, and nutrition questions
- ✅ Provides practical, beginner-friendly advice
- ✅ Gives safe recommendations
- ❌ Refuses to provide medical diagnoses
- ❌ Redirects non-fitness queries politely

## Dependencies

Key dependencies:
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **LangChain**: AI framework
- **LangGraph**: Agent orchestration
- **LangChain OpenAI**: OpenAI integration
- **Redis**: Session storage
- **PyJWT**: JWT authentication
- **Pydantic**: Data validation

See `requirements.txt` for the complete list.

## Development

### Adding Custom Tools

Extend the agent with custom fitness tools in `app/tools/`:

```python
from langchain.tools import tool

@tool
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI from weight and height."""
    return weight_kg / (height_m ** 2)
```

### Modifying Agent Behavior

Edit the `PROMPT` variable in `app/agent/build_agent.py` to adjust the assistant's behavior and instructions.

### Managing Session State

Session state is persisted in Redis using the schema defined in `app/state.py`.

## Troubleshooting

### Redis Connection Error
Ensure Redis is running:
```bash
redis-cli ping  # Should return "PONG"
```

### OpenAI API Key Error
Verify your API key is set in the `.env` file and is valid.

### JWT Authentication Error
Ensure the `Authorization` header is provided with a valid JWT token.



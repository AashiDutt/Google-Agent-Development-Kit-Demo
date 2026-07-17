# ADK-Powered Travel Planner 🌍🛫

This project is a multi-agent AI-powered travel planner built using Google's Agent Development Kit (ADK). It showcases how intelligent agents can coordinate to plan a complete trip: flights, stays, and activities. A simple Streamlit UI wraps everything for an intuitive end-user experience.

## 📚 What is ADK?

ADK (Agent Development Kit) is Google's open-source framework designed to help developers build modular, production-ready multi-agent systems powered by LLMs. It supports:

Hierarchical, parallel, or sequential agent orchestration

Integration with models via LiteLLM: GPT-4o, Claude, Gemini, DeepSeek, etc.

Streaming conversations, callbacks, session memory

Deployment in any environment (local, container, or cloud)

Each agent in ADK is self-contained, exposing a /run endpoint and metadata for discovery using the A2A (Agent-to-Agent) protocol.

## 🎨 Project Overview

This travel planner demonstrates a modular, orchestrated agent workflow:

User Input → Streamlit UI → Host Agent → [Flight Agent, Stay Agent, Activities Agent]

host_agent: Coordinates the planning process

flight_agent: Suggests flights

stay_agent: Recommends hotels

activities_agent: Suggests local experiences

Agents communicate over REST using FastAPI and respond with structured JSON outputs.

## 📂 Project Structure

ADK_demo/

├── agents/

│   ├── host_agent/         # Orchestrator — calls sub-agents over HTTP

│   ├── flight_agent/       # Flight suggestions via DeepSeek LLM

│   ├── stay_agent/         # Hotel/stay suggestions

│   └── activities_agent/   # Activity suggestions

├── shared/                 # Shared Pydantic models (unused)

├── common/                 # A2A client/server logic

│   ├── a2a_client.py       # HTTP client for agent-to-agent calls

│   └── a2a_server.py       # FastAPI server factory

├── travel_ui.py            # Streamlit frontend

├── research_notebook.ipynb  # Jupyter notebook for experimentation

├── requirements.txt

├── docker-compose.yml

├── Dockerfile

└── README.md

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- A DeepSeek API key (or any LiteLLM-compatible provider)

### Local Setup

1. Clone the Repo
```
git clone https://github.com/AashiDutt/Google-Agent-Development-Kit-Demo.git
cd Google-Agent-Development-Kit-Demo
```

2. Create virtual environment and install dependencies
```
python3 -m venv adk_demo
source adk_demo/bin/activate
pip install -r requirements.txt
```

3. Set your API key
```
export DEEPSEEK_API_KEY="your-api-key"
```

### Run with Docker (recommended)

```
docker compose up --build
```

- Streamlit UI: http://localhost:8501
- Host agent API: http://localhost:8000/run

### Run Locally (without Docker)

Start each agent in separate terminals:

```
uvicorn agents.host_agent.__main__:app --host 0.0.0.0 --port 8000
uvicorn agents.flight_agent.__main__:app --host 0.0.0.0 --port 8001
uvicorn agents.stay_agent.__main__:app --host 0.0.0.0 --port 8002
uvicorn agents.activities_agent.__main__:app --host 0.0.0.0 --port 8003
```

Launch the UI:

```
streamlit run travel_ui.py --server.port 8501 --server.address 0.0.0.0
```

## 🔧 What's Been Done

### Agent Alignment

The Jupyter notebook (`research_notebook.ipynb`) was updated to match the production agents in the `agents/` folder:

- **flight_agent** — instruction/prompt aligned with `agents/flight_agent/agent.py`: now uses all request fields (origin, destination, start_date, end_date, budget), asks for airline/departure time/return time/price/layover info
- **stay_agent** — instruction/prompt aligned with `agents/stay_agent/agent.py`: now includes date range, asks for hotel name/price per night/location
- **activities_agent** — instruction/prompt aligned with `agents/activities_agent/agent.py`: asks for name/description/price/duration

All three agents preserve the mock fallback (when no API key is set) as a notebook convenience.

### Docker Setup

- Fully functional `docker-compose.yml` with 5 services (host, flight, stay, activities, streamlit-ui)
- Each agent runs as an independent uvicorn process
- Host agent orchestrates sub-agents via A2A HTTP protocol
- Verified working with a real DeepSeek API key

### Documentation

- **`common/a2a_client.py`** — Added docstrings explaining the A2A client and function parameters
- **`.notes/PYTHON_README.md`** — Python reference guide for Node.js developers covering imports, async/await, FastAPI, type hints, and common patterns used in this project
- **`.notes/DOCKER_README.md`** — Docker usage reference

## 🔄 API

All agents expose a single `POST /run` endpoint:

**Request:**
```json
{
  "origin": "Dublin",
  "destination": "Bangkok",
  "start_date": "2026-11-01",
  "end_date": "2026-11-14",
  "budget": 2500
}
```

**Response (from host agent):**
```json
{
  "flights": "text with flight options...",
  "stay": "text with hotel options...",
  "activities": "text or JSON array with activities..."
}
```

## 🗑️ Known Dead Code

- **`agents/host_agent/agent.py`** — Defines a `host_agent` ADK agent and `execute()`, but is never imported. Host orchestration lives in `task_manager.py`.
- **`shared/schemas.py`** — Defines `TravelRequest` (Pydantic model), but is never imported anywhere. Already out of sync with the actual request fields used.

## 🤖 Contributing

Contributions are welcome! Please open issues or submit PRs with improvements.

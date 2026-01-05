# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**OxyGent** is a Python framework for building production-ready multi-agent systems. It unifies tools, models, and agents into modular "Oxy" components with transparent, end-to-end pipelines.

- **Python**: 3.10+
- **Package**: Available on PyPI as `oxygent`
- **License**: Apache 2.0

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest                                          # All tests
pytest test/unittest/test_react_agent.py        # Single file
pytest test/unittest/test_react_agent.py::test_function_name  # Single test
pytest -v                                       # Verbose output

# Run demo application
python demo.py

# Run examples
python -m examples.agents.demo_single_agent
python -m examples.ecommerce.app
```

## Environment Variables

Required in `.env` or exported:
```bash
DEFAULT_LLM_API_KEY="your_api_key"
DEFAULT_LLM_BASE_URL="https://api.openai.com/v1"
DEFAULT_LLM_MODEL_NAME="gpt-4"
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MAS (Multi-Agent System)                 │
│            Agent registration, routing, lifecycle           │
├─────────────────────────────────────────────────────────────┤
│               Core Oxy Components (Agents & Tools)          │
│  Agents: ReActAgent, ChatAgent, RAGAgent, WorkflowAgent     │
│  Tools: FunctionTools, MCPTools, HttpTools, BankTools       │
│  LLMs: HttpLLM, OpenAILLM, LocalLLM, MockLLM               │
├─────────────────────────────────────────────────────────────┤
│                Execution Flows & Paradigms                  │
│  Workflow, Reflexion, PlanAndSolve, MathReflexion          │
├─────────────────────────────────────────────────────────────┤
│              Data Persistence & Knowledge Layer             │
│  Elasticsearch (history), Redis (caching), Vearch (vectors) │
├─────────────────────────────────────────────────────────────┤
│                   FastAPI Web Service Layer                 │
│  HTTP endpoints, WebSocket SSE streaming, Live prompts      │
└─────────────────────────────────────────────────────────────┘
```

### Core Concept: Oxy

**Oxy** is the atomic unit - an abstract base class for agents and tools. All components inherit from `Oxy` and implement the async `_execute(oxy_request) -> oxy_response` pattern.

### Key Files by Complexity

| Component | Location | Size |
|-----------|----------|------|
| MAS Orchestrator | `oxygent/mas.py` | 61KB |
| Routes/Web API | `oxygent/routes.py` | 49KB |
| Base Oxy | `oxygent/oxy/base_oxy.py` | 29KB |
| Config | `oxygent/config.py` | 22KB |
| ReAct Agent | `oxygent/oxy/agents/react_agent.py` | 18KB |
| Live Prompt Manager | `oxygent/live_prompt/manager.py` | 32KB |

## Request/Response Lifecycle

```python
OxyRequest:
  ├── request_id: str              # Client trace ID
  ├── current_trace_id: str        # Node's unique ID
  ├── caller / callee: str         # Agent names
  ├── call_stack: List[str]        # Execution chain
  ├── arguments: dict              # Input parameters
  ├── shared_data: dict            # Session-scoped data
  └── mas: MAS                     # Runtime reference

OxyResponse:
  ├── state: OxyState             # COMPLETED, FAILED, RUNNING
  ├── output: Any                 # Execution result
  ├── error: str                  # Error if failed
  └── observations: List          # Tool call observations
```

## Agent Hierarchy

```
BaseAgent (abstract)
├── LocalAgent (local execution base)
│   ├── ReActAgent (reasoning + acting loops) ← Most common
│   ├── ChatAgent (simple conversation)
│   ├── RAGAgent (retrieval-augmented)
│   ├── WorkflowAgent (task-based)
│   ├── ParallelAgent (concurrent execution)
│   └── SSEOxyGent (streaming)
└── RemoteAgent (proxy to remote agents)
```

## Tool Types

- **FunctionTool**: Wraps Python async/sync functions with auto-schema extraction
- **MCPTool**: Wraps MCP servers (StdioMCPClient, SSEMCPClient, StreamableMCPClient)
- **HttpTool**: Generic HTTP requests
- **BankTool**: External service integration

## Common Patterns

### Creating a ReActAgent
```python
agent = oxy.ReActAgent(
    name="my_agent",
    desc="Agent description",
    tools=["tool_1", "tool_2"],
    max_react_rounds=10,
)
```

### Creating a FunctionTool
```python
from oxygent.oxy.function_tools import FunctionTool

async def calculate(x: int, y: int) -> int:
    return x + y

tool = FunctionTool(name="calc", func_process=calculate)
```

### Running MAS
```python
async with MAS(oxy_space=[...agents...]) as mas:
    await mas.start_web_service(first_query="Hello!")
    # or: response = await mas.execute(oxy_request)
```

## Testing Patterns

- Use `MockLLM` for isolated agent testing
- Mock LLM responses to test agent logic without API calls
- Tests in `test/unittest/` (43+ test files)
- Some tests require external services (ES, Redis) - mock-based tests don't

## Configuration

`config.json` structure with environment variable substitution (`${VAR_NAME}`):
- `llm`: LLM parameters (temperature, max_tokens, timeout)
- `agent`: Agent defaults (llm_model, memory_size, prompts)
- `server`: Web server (host, port, workers)
- `databases`: ES, Redis, Vearch configs

## Web Service Endpoints

- `GET /` → Web UI
- `POST /chat` → Query the MAS
- `WebSocket /sse` → Real-time streaming
- `GET /nodes` → Execution trace visualization
- `GET /prompts` → Live prompt management

## Extension Points

### Custom Agent
```python
class CustomAgent(LocalAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom execution logic
        pass
```

### Custom Tool
```python
class MyCustomTool(BaseTool):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom tool logic
        pass
```

## MCP Integration

Requires Node.js. Create MCP server implementations and wrap with:
- `StdioMCPClient` for stdio-based
- `SSEMCPClient` for Server-Sent Events
- `StreamableMCPClient` for streaming

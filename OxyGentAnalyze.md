# OxyGent Project Overview

## What is OxyGent?

OxyGent is an advanced Python framework developed by JD.com for building production-ready multi-agent systems. It's an enterprise-grade alternative to LangChain/LangGraph with a focus on modularity, scalability, and distributed agent orchestration.

## Core Architecture

### 1. Oxy Components (Universal Building Blocks)

All components in OxyGent inherit from the base `Oxy` class located in `oxygent/oxy/base_oxy.py`:

- **Agents**: ReAct, Chat, Workflow, Parallel, Remote agents
- **Tools**: Function tools, MCP tools, HTTP API tools
- **LLMs**: HTTP LLM, OpenAI LLM, Remote LLM connectors
- **Flows**: Parallel Flow, Plan-and-Solve, Reflexion, Workflow

### 2. MAS (Multi-Agent System)

The central orchestrator located in `oxygent/mas.py` that:

- Manages agent registration and organization
- Handles distributed execution and coordination  
- Provides web UI and SSE streaming capabilities
- Manages database connections (ES, Redis, Vector DBs)
- Supports CLI, web service, and batch processing modes

### 3. Database Integration

Enterprise-grade persistence through:

- **Elasticsearch**: Trace storage, message logging, node execution history
- **Redis**: Real-time message streaming for SSE
- **Vector Databases**: Tool similarity search and retrieval

## Key Differences vs LangChain/LangGraph

| Aspect                  | OxyGent                   | LangChain           | LangGraph       |
| ----------------------- | ------------------------- | ------------------- | --------------- |
| **Primary Focus**       | Multi-agent orchestration | Single-agent chains | Graph workflows |
| **Architecture**        | Modular Oxy components    | Chain composition   | State graphs    |
| **Execution Model**     | Async-first, distributed  | Sync/async hybrid   | State-based     |
| **Persistence**         | Built-in ES/Redis         | Limited             | Memory-based    |
| **Web Interface**       | Included web UI + SSE     | External            | External        |
| **Agent Communication** | Native multi-agent        | Add-on              | Possible        |

## Development Commands

Based on the project structure, common development commands include:

### Installation

```bash
# Development setup
pip install -r requirements.txt

# Production install  
pip install oxygent
```

### Running Examples

```bash
# Basic demo
python demo.py

# CLI mode
python examples/agents/single_demo.py

# Web service mode (with UI)
python demo.py  # Opens web interface at http://localhost:8000
```

### Testing

```bash
# Unit tests
pytest test/unittest/

# Integration tests  
pytest test/integration/
```

## Project Structure

```
oxygent/
    oxy/                    # Core Oxy components
    agents/            # Agent implementations
    tools/             # Tool implementations
    llms/              # LLM connectors
    flows/             # Workflow patterns
    base_oxy.py        # Universal base class
    mas.py                 # Multi-Agent System orchestrator
    config.py              # Configuration management
    schemas/               # Data models and schemas
    databases/             # Database integrations
    web/                   # Web UI assets
    preset_tools/          # Built-in tool implementations
```

## Key Features

1. **Modular Design**: LEGO-like component assembly
2. **Hot-swappable Components**: Runtime component replacement
3. **Distributed Execution**: Elastic scaling across machines
4. **Built-in UI**: Web interface with real-time streaming
5. **MCP Integration**: Model Context Protocol support
6. **Enterprise Persistence**: Full audit trails and data retention
7. **Multiple Execution Modes**: CLI, Web, Batch processing

## Usage Patterns

### Basic Agent Setup

```python
from oxygent import MAS, oxy
import os

oxy_space = [
    oxy.HttpLLM(name="default_llm", api_key=os.getenv("API_KEY")),
    oxy.ReActAgent(name="assistant", tools=["time_tools"]),
]

async def main():
    async with MAS(oxy_space=oxy_space) as mas:
        await mas.start_web_service()
```

### Multi-Agent Coordination

```python
oxy_space = [
    oxy.ReActAgent(name="master", sub_agents=["time_agent", "file_agent"], is_master=True),
    oxy.ReActAgent(name="time_agent", tools=["time_tools"]),
    oxy.ReActAgent(name="file_agent", tools=["file_tools"]),
]
```

## Development Tips

1. **Agent Development**: Extend `BaseAgent` for custom agents
2. **Tool Creation**: Use `@fh.tool` decorator or extend `BaseTool`
3. **Custom Flows**: Implement workflow logic in `Workflow` class
4. **Database Setup**: Configure ES/Redis in config for persistence
5. **Testing**: Use integration tests for multi-agent scenarios

## Architecture Benefits

- **Scalability**: Linear cost growth with exponential intelligence gains
- **Modularity**: Components can be mixed and matched
- **Observability**: Full execution tracing and debugging
- **Production-Ready**: Enterprise-grade persistence and monitoring
- **Flexibility**: Support for various agent patterns and workflows

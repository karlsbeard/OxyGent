# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**OxyGent** is an open-source Python framework for building production-ready multi-agent AI systems. It provides a modular architecture where tools, models, and agents are unified into modular "Oxy" components that can be assembled like building blocks.

## Core Architecture

### Framework Structure

- **Oxy**: Base abstract class for all agents and tools (`oxygent/oxy/base_oxy.py`)
- **MAS (Multi-Agent System)**: Core orchestrator for managing agent interactions (`oxygent/mas.py`)
- **Agents**: Different agent types in `oxygent/oxy/agents/`
  - `ReActAgent`: Reasoning and acting agent
  - `ChatAgent`: Conversational agent
  - `ParallelAgent`: Concurrent execution agent
  - `WorkflowAgent`: Workflow-based agent
  - `SSEOxyGent`: Server-sent events agent
- **Tools**: Various tool implementations
  - `HttpTool`: HTTP request tool
  - `MCPTool`: MCP (Model Context Protocol) tool
  - `FunctionTool`: Python function wrapper
- **LLMs**: Language model integrations (`oxygent/oxy/llms/`)
  - `HttpLLM`: Generic HTTP LLM client
  - `OpenAILLM`: OpenAI-specific implementation
- **Flows**: Execution patterns (`oxygent/oxy/flows/`)
  - `Workflow`: Sequential workflow execution
  - `PlanAndSolve`: Planning-based execution
  - `Reflexion`: Self-reflective execution

### Key Components

- **Config**: Global configuration management (`oxygent/config.py`)
- **Database Support**: Redis, Elasticsearch, and Vector databases (`oxygent/databases/`)
- **Preset Tools**: Common utilities (`oxygent/preset_tools/`)
- **Web Interface**: Built-in web UI (`oxygent/web/`)

## Development Commands

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run unit tests
pytest test/unittest

# Run integration tests (optional)
pytest test/integration

# Run specific test
pytest test/unittest/test_base_agent.py
```

### Code Formatting

```bash
# Format code
ruff format .

# Format docstrings
docformatter -r -i --wrap-summaries 88 --wrap-descriptions 88 oxygent/
```

### Running Examples

```bash
# Basic demo
python demo.py

# Single agent example
python -m examples.agents.single_demo

# Other examples in examples/ directory
python examples/agents/batch_demo.py
python examples/advanced/parallel_demo.py
```

### Web Service

The framework includes a built-in web interface. Start it by running any demo with `start_web_service()`.

## Project Structure Highlights

### Core Modules

- `oxygent/oxy/`: Core framework components (agents, tools, flows, LLMs)
- `oxygent/databases/`: Database abstraction layer
- `oxygent/preset_tools/`: Ready-to-use tools (time, file, math, etc.)
- `oxygent/utils/`: Utility functions
- `oxygent/schemas/`: Pydantic models for data structures

### Configuration

- Environment variables loaded from `.env` file
- Global configuration via `Config` class
- Test configuration in `pytest.ini`

### MCP Integration

The framework supports Model Context Protocol (MCP) for tool integration:

- `mcp_servers/`: Custom MCP server implementations
- MCP tools in `oxygent/oxy/mcp_tools/`

### Multi-Agent Examples

- `examples/distributed/`: Distributed agent examples
- `examples/ecommerce/`: E-commerce system example

## Key Patterns

### Agent Creation

```python
from oxygent import oxy, MAS, Config

# Create agents using the oxy module
agent = oxy.ReActAgent(
    name="my_agent",
    desc="Agent description",
    tools=["tool_name"]
)
```

### Multi-Agent System

```python
async with MAS(oxy_space=oxy_space) as mas:
    await mas.start_web_service()
```

### Tool Registration

Tools are registered in the `oxy_space` list alongside agents and LLMs.

## Dependencies

Key dependencies include FastAPI, Pydantic, OpenAI SDK, MCP, Redis, Elasticsearch, and various async libraries. See `requirements.txt` for complete list.

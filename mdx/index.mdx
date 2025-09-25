---
title: Agent System Overview
description: Comprehensive guide to the OxyGent agent architecture, types, and capabilities
---

# OxyGent Agent System

The OxyGent agent system provides a comprehensive framework for building intelligent, autonomous agents that can reason, act, communicate, and collaborate. This system supports everything from simple conversational agents to complex reasoning systems that can use tools, delegate tasks, and work in teams.

## Architecture Overview

The OxyGent agent system is built on a hierarchical architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        BaseAgent                                │
│  • Trace Management    • Data Persistence    • Request Lifecycle│
└─────────────────┬───────────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
   ┌────▼─────┐        ┌────▼──────┐
   │LocalAgent│        │RemoteAgent│
   └────┬─────┘        └────┬──────┘
        │                   │
 ┌──────┴───────┐          │
 │              │     ┌────▼────────┐
┌▼──────┐ ┌─────▼┐    │ SSEOxyGent  │
│ChatAg │ │ReAct │    └─────────────┘
│ParAll │ │Work  │
└───────┘ └──────┘
```

### Core Principles

1. **Hierarchical Design**: Each agent type builds upon lower-level capabilities
2. **Separation of Concerns**: Different aspects handled by specialized classes
3. **Extensibility**: Easy to create new agent types by extending existing ones
4. **Interoperability**: All agents work together seamlessly
5. **Distributed Support**: Local and remote agents integrate transparently

## Agent Types

### Foundation Agents

#### [BaseAgent](./base-agent)
The foundation class for all agents in the OxyGent system.

**Key Capabilities**:
- Request/response lifecycle management
- Trace management and data persistence
- Elasticsearch integration for history
- Group data management

**Use Cases**:
- Foundation for all other agent types
- Custom agent implementations
- Trace management requirements

```python
from oxygent.oxy.agents import BaseAgent

class CustomAgent(BaseAgent):
    async def _execute(self, oxy_request):
        return OxyResponse(output="Custom processing complete")
```

#### [LocalAgent](./local-agent)
Base class for agents that execute locally with tool and memory management.

**Key Capabilities**:
- Dynamic tool discovery and management
- Sub-agent delegation and hierarchy
- Conversation memory management
- LLM integration with prompt templating
- Team-based parallel execution
- Multimodal content support

**Use Cases**:
- Foundation for tool-using agents
- Complex memory management needs
- Multi-modal interactions
- Team-based processing

```python
class ToolUsingAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.tools = ["web_search", "calculator"]
```

#### [RemoteAgent](./remote-agent)
Foundation for agents that communicate with remote OxyGent systems.

**Key Capabilities**:
- HTTP/HTTPS endpoint validation
- Organization structure management
- Remote system integration
- Call stack preservation

**Use Cases**:
- Distributed OxyGent architectures
- Microservices integration
- Cloud-based agent systems
- Load balancing scenarios

```python
remote_agent = RemoteAgent(
    name="remote_processor",
    server_url="https://remote-oxygent.company.com"
)
```

### Specialized Agents

#### [ChatAgent](./chat-agent)
Conversational agent optimized for dialogue interactions.

**Key Capabilities**:
- Natural conversation flow management
- Automatic memory integration
- Simple query processing interface
- Default conversational prompts

**Best For**:
- Chatbots and virtual assistants
- Customer service applications
- Simple Q&A interactions
- Conversational interfaces

```python
chat_agent = ChatAgent(
    name="customer_service",
    llm_model="gpt-4",
    prompt="You are a helpful customer service representative."
)
```

#### [ReActAgent](./react-agent)
Advanced reasoning agent implementing the ReAct (Reasoning and Acting) paradigm.

**Key Capabilities**:
- Iterative reasoning and action cycles
- Sophisticated memory management
- Multiple tool retrieval strategies
- Trust mode for direct tool results
- Error recovery and reflexion
- Custom response parsing

**Best For**:
- Complex problem solving
- Multi-step reasoning tasks
- Research and analysis
- Autonomous decision making
- Tool-heavy workflows

```python
react_agent = ReActAgent(
    name="problem_solver",
    llm_model="gpt-4",
    max_react_rounds=16,
    tools=["web_search", "calculator", "python_executor"]
)
```

#### [ParallelAgent](./parallel-agent)
Team coordination agent for concurrent task execution.

**Key Capabilities**:
- Concurrent execution across team members
- Result aggregation and summarization
- Team coordination with unique identifiers
- Diverse perspective gathering

**Best For**:
- Team-based problem solving
- Multiple solution generation
- Cross-validation of results
- Load distribution
- Consensus building

```python
# Automatically created when LocalAgent.team_size > 1
team_agent = LocalAgent(
    name="brainstorm_team",
    team_size=3,  # Creates ParallelAgent with 3 members
    llm_model="gpt-4"
)
```

#### [WorkflowAgent](./workflow-agent)
Custom workflow execution agent for integrating existing functions.

**Key Capabilities**:
- Custom function integration
- OxyRequest context access
- Legacy system bridging
- Flexible workflow implementation

**Best For**:
- Wrapping existing business logic
- Custom data processing pipelines
- Rapid prototyping
- Domain-specific algorithms
- Legacy integration

```python
async def custom_workflow(oxy_request):
    data = oxy_request.arguments.get("data", [])
    return {"processed": len(data), "status": "complete"}

workflow_agent = WorkflowAgent(
    name="data_processor",
    func_workflow=custom_workflow
)
```

#### [SSEOxyGent](./sse-oxy-agent)
Real-time communication agent using Server-Sent Events.

**Key Capabilities**:
- Real-time streaming communication
- Live updates and progress reporting
- Event stream processing
- Distributed architecture support

**Best For**:
- Real-time applications
- Streaming responses
- Distributed agent systems
- Live collaboration
- Progress monitoring

```python
sse_agent = SSEOxyGent(
    name="remote_stream",
    server_url="https://remote-oxygent.company.com",
    is_share_call_stack=True
)
```

## Agent Selection Guide

### Simple Conversations → ChatAgent
```python
# Perfect for basic Q&A and conversations
ChatAgent(llm_model="gpt-4", prompt="You are a helpful assistant")
```

### Tool Usage → LocalAgent or ReActAgent
```python
# LocalAgent for simple tool use
LocalAgent(tools=["web_search"], llm_model="gpt-4")

# ReActAgent for complex reasoning with tools  
ReActAgent(tools=["web_search", "calculator"], max_react_rounds=10)
```

### Team Work → ParallelAgent (via LocalAgent)
```python
# Automatic team creation
LocalAgent(team_size=3, llm_model="gpt-4")  # Becomes ParallelAgent
```

### Custom Logic → WorkflowAgent
```python
# Wrap existing functions
WorkflowAgent(func_workflow=my_custom_function)
```

### Remote Systems → SSEOxyGent
```python
# Connect to remote OxyGent instances
SSEOxyGent(server_url="https://remote.example.com")
```

### Custom Foundation → BaseAgent
```python
# Build completely custom agents
class MyAgent(BaseAgent):
    async def _execute(self, request):
        # Custom implementation
        pass
```

## Common Patterns

### Hierarchical Agent Systems

```python
# Master coordinator
master = ReActAgent(
    name="master_coordinator",
    llm_model="gpt-4",
    sub_agents=["research_specialist", "analysis_expert", "report_writer"],
    tools=["web_search", "data_analyzer"]
)

# Specialized sub-agents
research_agent = ChatAgent(
    name="research_specialist", 
    prompt="You specialize in research and information gathering."
)

analysis_agent = ReActAgent(
    name="analysis_expert",
    tools=["statistical_analyzer", "python_executor"]
)

report_agent = WorkflowAgent(
    name="report_writer",
    func_workflow=generate_formatted_report
)
```

### Distributed Processing

```python
# Local coordinator
local_coordinator = ParallelAgent(
    name="distributed_processor",
    permitted_tool_name_list=["remote_node_1", "remote_node_2", "remote_node_3"]
)

# Remote processing nodes
node_1 = SSEOxyGent(name="remote_node_1", server_url="https://node1.company.com")
node_2 = SSEOxyGent(name="remote_node_2", server_url="https://node2.company.com") 
node_3 = SSEOxyGent(name="remote_node_3", server_url="https://node3.company.com")
```

### Multi-Modal Pipeline

```python
# Multi-modal processing agent
multimodal_agent = LocalAgent(
    name="multimodal_processor",
    llm_model="gpt-4-vision",
    tools=["image_analyzer", "ocr_tool", "audio_transcriber"],
    is_attachment_processing_enabled=True
)

# Can handle text, images, audio, and documents
```

## Configuration Patterns

### Development vs Production

```python
# Development configuration
dev_agent = ChatAgent(
    name="dev_assistant",
    llm_model="gpt-3.5-turbo",  # Cost-effective
    short_memory_size=5,        # Smaller context
    tools=["debug_tools"]
)

# Production configuration  
prod_agent = ReActAgent(
    name="prod_assistant",
    llm_model="gpt-4-turbo",     # High performance
    short_memory_size=20,        # Larger context
    max_react_rounds=16,         # More reasoning steps
    tools=["production_tools"]
)
```

### Resource Optimization

```python
# Memory-optimized agent
memory_efficient = ChatAgent(
    llm_model="gpt-3.5-turbo",
    short_memory_size=3,
    is_retain_master_short_memory=False
)

# Performance-optimized agent
high_performance = ReActAgent(
    llm_model="gpt-4-turbo", 
    memory_max_tokens=32000,
    is_discard_react_memory=False,  # Keep detailed memory
    max_react_rounds=24
)
```

### Security Configuration

```python
# Secure remote agent
secure_agent = SSEOxyGent(
    server_url="https://secure-endpoint.com",  # HTTPS only
    is_share_call_stack=False  # Minimal context sharing
)

# Restricted local agent
restricted_agent = LocalAgent(
    tools=["safe_tool_1", "safe_tool_2"],
    except_tools=["dangerous_tool"],  # Explicitly forbidden
    llm_model="gpt-4"
)
```

## Integration Examples

### Web Application Integration

```python
from fastapi import FastAPI
from oxygent.oxy.agents import ChatAgent, ReActAgent

app = FastAPI()

# Simple chat endpoint
chat_agent = ChatAgent(name="web_chat", llm_model="gpt-4")

@app.post("/chat")
async def chat_endpoint(message: str):
    request = OxyRequest(arguments={"query": message})
    response = await chat_agent.execute(request)
    return {"response": response.output}

# Complex processing endpoint  
processor = ReActAgent(
    name="web_processor",
    tools=["web_search", "data_analyzer"],
    max_react_rounds=10
)

@app.post("/process")
async def process_endpoint(task: dict):
    request = OxyRequest(arguments=task)
    response = await processor.execute(request) 
    return {"result": response.output}
```

### Microservices Architecture

```python
# Service A: User Interface
ui_agent = ChatAgent(
    name="ui_agent",
    sub_agents=["analytics_service", "recommendation_service"]
)

# Service B: Analytics (Remote)
analytics_agent = SSEOxyGent(
    name="analytics_service",
    server_url="https://analytics.company.com"
)

# Service C: Recommendations (Remote)
recommendation_agent = SSEOxyGent(
    name="recommendation_service", 
    server_url="https://ml.company.com"
)
```

### Batch Processing System

```python
# Batch coordinator
batch_coordinator = ParallelAgent(
    name="batch_processor",
    permitted_tool_name_list=["worker_1", "worker_2", "worker_3", "worker_4"]
)

# Worker agents (can be different types)
workers = [
    WorkflowAgent(name=f"worker_{i}", func_workflow=process_batch_item)
    for i in range(1, 5)
]
```

## Best Practices

### 1. Choose the Right Agent Type

- **ChatAgent**: Simple conversations, Q&A, basic interactions
- **LocalAgent**: Custom tool integration, memory management
- **ReActAgent**: Complex reasoning, multi-step problem solving  
- **ParallelAgent**: Team coordination, multiple perspectives
- **WorkflowAgent**: Custom business logic, existing function integration
- **SSEOxyGent**: Real-time remote communication, distributed systems

### 2. Configure Memory Appropriately

```python
# For conversations: moderate memory
chat_agent.short_memory_size = 10

# For complex reasoning: larger memory
react_agent.memory_max_tokens = 32000
react_agent.is_discard_react_memory = False

# For performance: minimal memory
fast_agent.short_memory_size = 3
```

### 3. Handle Errors Gracefully

```python
class RobustAgent(LocalAgent):
    async def _execute(self, oxy_request):
        try:
            return await super()._execute(oxy_request)
        except Exception as e:
            return OxyResponse(
                state=OxyState.ERROR,
                output=f"Processing failed: {e}"
            )
```

### 4. Monitor Performance

```python
import time

class MonitoredAgent(ReActAgent):
    async def _execute(self, oxy_request):
        start_time = time.time()
        response = await super()._execute(oxy_request)
        execution_time = time.time() - start_time
        
        response.extra["execution_time"] = execution_time
        return response
```

### 5. Use Appropriate Security

```python
# Production security
production_agent = SSEOxyGent(
    server_url="https://secure-endpoint.com",  # HTTPS only
    is_share_call_stack=False  # Minimal context sharing
)

# Development flexibility
dev_agent = LocalAgent(
    server_url="http://localhost:8000",  # HTTP OK for dev
    is_share_call_stack=True  # Full context sharing
)
```

## Getting Started

### 1. Simple Chat Agent

```python
from oxygent.oxy.agents import ChatAgent

# Create and use a basic chat agent
agent = ChatAgent(
    name="assistant",
    llm_model="gpt-4",
    prompt="You are a helpful assistant."
)

# Process a request
request = OxyRequest(arguments={"query": "Hello, how are you?"})
response = await agent.execute(request)
print(response.output)
```

### 2. Tool-Using Agent

```python
from oxygent.oxy.agents import LocalAgent

# Create an agent with tools
agent = LocalAgent(
    name="helper",
    llm_model="gpt-4", 
    tools=["web_search", "calculator"],
    prompt="You can search the web and do calculations to help users."
)
```

### 3. Reasoning Agent

```python
from oxygent.oxy.agents import ReActAgent

# Create a reasoning agent
agent = ReActAgent(
    name="solver",
    llm_model="gpt-4",
    max_react_rounds=10,
    tools=["web_search", "python_executor"],
    prompt="You are a problem solver. Think step by step and use tools as needed."
)
```

## Next Steps

- **[BaseAgent](./base-agent)**: Learn about the foundation class
- **[LocalAgent](./local-agent)**: Understand tool and memory management  
- **[ReActAgent](./react-agent)**: Master reasoning and acting patterns
- **[ChatAgent](./chat-agent)**: Create conversational interfaces
- **[RemoteAgent](./remote-agent) & [SSEOxyGent](./sse-oxy-agent)**: Build distributed systems

## Advanced Topics

- **Tool Management**: Dynamic tool discovery and retrieval
- **Memory Systems**: Conversation history and context management
- **Distributed Architecture**: Multi-instance and remote communication
- **Performance Optimization**: Memory, token, and execution optimization
- **Security**: Authentication, authorization, and secure communication
- **Monitoring**: Logging, tracing, and performance monitoring
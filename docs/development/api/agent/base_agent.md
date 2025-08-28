# BaseAgent Class

## Overview

The `BaseAgent` class serves as the foundation for all agent implementations in the OxyGent system. It extends the `BaseFlow` class and provides common functionality for agent implementations including permission management, trace handling, and data persistence operations.

## Class Definition

```python
class BaseAgent(BaseFlow)
```

**Module**: `oxygent.oxy.agents.base_agent`  
**Inherits from**: `BaseFlow`

## Core Attributes

### Agent Configuration

- `category` (str): The category of this tool/agent (default: "agent")
- `input_schema` (dict[str, Any]): Input schema configuration for the agent (auto-configured from Config)

## Key Methods

### Trace Management

#### `async def _pre_process(self, oxy_request: OxyRequest) -> OxyRequest`

Pre-processes the request before handling with enhanced trace management for user requests.

**Functionality:**

- Calls parent `_pre_process` method
- Handles trace hierarchy for user-originated requests
- Retrieves historical trace information from Elasticsearch
- Sets up root trace IDs for request tracking

**Trace Handling Logic:**

```python
if oxy_request.caller_category == "user":
    if oxy_request.from_trace_id:
        # Query ES for parent trace information
        es_response = await self.mas.es_client.search(
            Config.get_app_name() + "_trace",
            {"query": {"term": {"_id": oxy_request.from_trace_id}}}
        )
        
        # Extract and update root trace IDs
        if es_response and es_response["hits"]["hits"]:
            oxy_request.root_trace_ids = es_response["hits"]["hits"][0]["_source"]["root_trace_ids"]
        else:
            oxy_request.root_trace_ids = []
        
        # Add current trace to root trace IDs
        oxy_request.root_trace_ids.append(oxy_request.from_trace_id)
```

### Data Persistence

#### `async def _pre_save_data(self, oxy_request: OxyRequest)`

Saves preliminary trace data before processing the request.

**Functionality:**

- Calls parent `_pre_save_data` method
- Persists initial trace information to Elasticsearch for user requests
- Creates a record in the `{app_name}_trace` index

**Saved Data Structure:**

```python
{
    "request_id": oxy_request.request_id,
    "trace_id": oxy_request.current_trace_id,
    "group_id": oxy_request.group_id,
    "from_trace_id": oxy_request.from_trace_id,
    "root_trace_ids": oxy_request.root_trace_ids,
    "input": to_json(oxy_request.arguments),
    "callee": oxy_request.callee,
    "output": "",  # Filled in post_save_data
    "create_time": get_format_time(),
}
```

#### `async def _post_save_data(self, oxy_response: OxyResponse)`

Saves complete trace and history data after processing the request.

**Functionality:**

- Calls parent `_post_save_data` method
- Updates trace record with response output
- Optionally saves conversation history for user requests

**History Data Management:**

- Creates unique sub-session identifiers
- Stores query-answer pairs with metadata
- Supports conversation context preservation
- Integration with extra response data

**History Data Structure:**

```python
{
    "sub_session_id": current_sub_session_id,
    "session_name": oxy_request.session_name,
    "trace_id": oxy_request.current_trace_id,
    "memory": to_json({
        "query": oxy_request.get_query(),
        "answer": oxy_response.output,
        **oxy_response.extra  # Additional metadata
    }),
    "create_time": get_format_time(),
}
```

## Database Integration

### Elasticsearch Indices

BaseAgent integrates with two primary Elasticsearch indices:

#### 1. Trace Index (`{app_name}_trace`)

**Purpose**: Tracks individual request-response cycles

- Stores request metadata and arguments
- Captures response outputs and execution state
- Maintains trace hierarchy and relationships
- Supports conversation threading

#### 2. History Index (`{app_name}_history`)

**Purpose**: Maintains conversation history

- Stores query-answer pairs
- Preserves session context
- Enables memory retrieval for agents
- Supports conversation continuity

### Error Handling

Both data persistence methods include error handling:

```python
if self.mas and self.mas.es_client:
    # Perform Elasticsearch operations
    await self.mas.es_client.index(...)
else:
    logger.warning(f"Save {oxy_request.callee} trace data error")
```

## Usage Patterns

### Basic Agent Implementation

```python
from oxygent.oxy.agents.base_agent import BaseAgent
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class MyAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="my_agent",
            desc="Custom agent implementation",
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom agent logic
        result = await self.process_request(oxy_request)
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=result,
            extra={"processing_metadata": self.get_metadata()}
        )
```

### Conversation History Integration

```python
class ConversationalAgent(BaseAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Access conversation history through trace system
        # History is automatically saved when is_save_history=True
        
        # Process with awareness of conversation context
        result = await self.generate_contextual_response(oxy_request)
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=result
        )
```

## Configuration

BaseAgent uses several configuration options from the global Config:

- `Config.get_agent_input_schema()`: Default input schema
- `Config.get_app_name()`: Application name for index naming
- Trace and history data retention policies

## Best Practices

1. **Trace Management**: Rely on automatic trace handling for user requests
2. **Data Persistence**: Use the built-in ES integration for consistency
3. **History Preservation**: Enable `is_save_history` for conversational agents
4. **Error Handling**: Let the base class handle ES connection issues
5. **Session Management**: Use appropriate session naming strategies
6. **Memory Efficiency**: Consider trace data size for high-volume applications

## Integration with MAS

BaseAgent is fully integrated with the Multi-Agent System:

- Automatic registration with ES client
- Seamless trace ID propagation
- Background task management for data persistence
- Integration with global configuration system

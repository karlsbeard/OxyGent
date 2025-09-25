---
title: BaseAgent
description: Foundation class for all agents in the OxyGent framework with trace management and data persistence capabilities
---

# BaseAgent

The `BaseAgent` class serves as the foundation for all agent implementations in the OxyGent system. It extends the `BaseFlow` class and provides essential functionality for trace management, data persistence, and common agent lifecycle operations.

## Overview

`BaseAgent` is an abstract base class that handles the core infrastructure required by all agents in the OxyGent framework. It manages:

- **Trace Management**: Tracks request flows and maintains trace hierarchies
- **Data Persistence**: Stores trace data and conversation history in Elasticsearch
- **Request Lifecycle**: Handles pre-processing, execution, and post-processing phases
- **Permission Management**: Controls access to tools and resources

## Class Definition

```python
from oxygent.oxy.agents import BaseAgent
from oxygent.schemas import OxyRequest, OxyResponse

class MyCustomAgent(BaseAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Your agent implementation here
        pass
```

## Attributes

### category
- **Type**: `str`
- **Default**: `"agent"`
- **Description**: The category classification for this agent/tool

### input_schema
- **Type**: `dict[str, Any]`
- **Default**: Retrieved from `Config.get_agent_input_schema()`
- **Description**: Input parameters schema defining expected request structure

## Key Methods

### async _pre_process(oxy_request: OxyRequest) -> OxyRequest

Handles request preprocessing including trace management and root trace ID setup.

**Key Functionality**:
- Retrieves historical trace information from Elasticsearch for user requests
- Establishes trace hierarchy by setting root trace IDs
- Prepares the request context for execution

```python
# The method automatically handles trace setup:
# 1. Queries Elasticsearch for parent trace information
# 2. Extracts and sets root_trace_ids from parent trace
# 3. Appends current from_trace_id to root trace IDs
```

**Parameters**:
- `oxy_request`: The incoming request to preprocess

**Returns**: The preprocessed request with trace information populated

### async _pre_save_data(oxy_request: OxyRequest)

Saves preliminary trace data before processing the request.

**Key Functionality**:
- Persists initial trace information to Elasticsearch
- Creates a record of the request before processing begins
- Handles group data schema validation and filtering

```python
# Example of trace data saved:
{
    "request_id": "req_123",
    "trace_id": "trace_456", 
    "group_id": "group_789",
    "group_data": {...},
    "from_trace_id": "parent_trace",
    "root_trace_ids": ["root1", "root2"],
    "input": {...},
    "callee": "agent_name",
    "output": "",  # Will be filled in post_save_data
    "create_time": "2024-09-01T12:00:00"
}
```

**Parameters**:
- `oxy_request`: The request containing trace data to save

### async _post_save_data(oxy_response: OxyResponse)

Updates trace records with response output and saves conversation history.

**Key Functionality**:
- Updates the trace record with the complete response output
- Optionally saves conversation history for user requests
- Handles group data persistence with schema validation

```python
# Example conversation history saved:
{
    "sub_session_id": "trace_456__session_name",
    "session_name": "default_session",
    "trace_id": "trace_456",
    "memory": {
        "query": "User's question",
        "answer": "Agent's response",
        # Additional fields from oxy_response.extra
    },
    "create_time": "2024-09-01T12:05:00"
}
```

**Parameters**:
- `oxy_response`: The response containing processed results and request data

## Usage Examples

### Basic Agent Implementation

```python
from oxygent.oxy.agents import BaseAgent
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class SimpleAgent(BaseAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Simple echo agent
        user_input = oxy_request.arguments.get("query", "No input provided")
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=f"Echo: {user_input}"
        )
```

### Agent with Custom Pre-processing

```python
class CustomPreprocessAgent(BaseAgent):
    async def _pre_process(self, oxy_request: OxyRequest) -> OxyRequest:
        # Call parent preprocessing first
        oxy_request = await super()._pre_process(oxy_request)
        
        # Add custom preprocessing logic
        if "query" in oxy_request.arguments:
            # Transform query to uppercase
            oxy_request.arguments["query"] = oxy_request.arguments["query"].upper()
            
        return oxy_request
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        processed_query = oxy_request.arguments.get("query")
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=f"Processed: {processed_query}"
        )
```

### Agent with History Management

```python
class HistoryAwareAgent(BaseAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # This agent automatically benefits from trace management
        # The BaseAgent handles all trace persistence
        
        current_query = oxy_request.arguments.get("query")
        trace_id = oxy_request.current_trace_id
        
        # Your processing logic here
        result = f"Processing '{current_query}' with trace {trace_id}"
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=result,
            # BaseAgent will automatically save this to history if requested
        )
```

## Architecture Integration

### Elasticsearch Integration

`BaseAgent` seamlessly integrates with Elasticsearch for:

- **Trace Storage**: All request-response pairs are stored with trace metadata
- **History Retrieval**: Historical conversations can be retrieved for context
- **Group Data Management**: Supports storing and filtering group-specific data

### Trace Hierarchy

The trace system supports hierarchical request tracking:

```
Root Trace ID → Parent Trace ID → Current Trace ID
     ↓               ↓                 ↓
  Initial         Delegated         Current
  Request         Request           Request
```

### Configuration Integration

BaseAgent relies on the Config system for:

- Input schema definitions (`Config.get_agent_input_schema()`)
- Application naming (`Config.get_app_name()`)
- Elasticsearch schema configuration (`Config.get_es_schema_group_data()`)

## Error Handling

The BaseAgent includes robust error handling:

```python
# Warning logs for save failures
if not self.mas or not self.mas.es_client:
    logger.warning(f"Save {oxy_request.callee} pre trace data error")
```

## Best Practices

1. **Always Call Super Methods**: When overriding lifecycle methods, call the parent implementation first:
   ```python
   async def _pre_process(self, oxy_request: OxyRequest) -> OxyRequest:
       oxy_request = await super()._pre_process(oxy_request)
       # Your custom logic here
       return oxy_request
   ```

2. **Handle Trace Context**: Use the trace information for debugging and monitoring:
   ```python
   logger.info("Processing request", extra={
       "trace_id": oxy_request.current_trace_id,
       "node_id": oxy_request.node_id,
   })
   ```

3. **Leverage History**: For conversational agents, the automatic history management provides context for multi-turn conversations.

## Related Classes

- **[LocalAgent](./local-agent)**: Extends BaseAgent with local execution and tool management
- **[RemoteAgent](./remote-agent)**: Extends BaseAgent for remote system communication
- **OxyRequest**: Request object handled by all methods
- **OxyResponse**: Response object returned by agent execution

## See Also

- [Agent System Overview](./index)
- [Local Agent Documentation](./local-agent)
- [Configuration Management](../config)
- [Schema Definitions](../schemas)
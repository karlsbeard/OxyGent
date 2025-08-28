# SSEOxyGent Class

## Overview

The `SSEOxyGent` class provides Server-Sent Events (SSE) based communication with remote OxyGent systems. It enables real-time streaming of agent interactions and responses, making it ideal for building responsive user interfaces and real-time applications.

## Class Definition

```python
class SSEOxyGent(RemoteAgent)
```

**Module**: `oxygent.oxy.agents.sse_oxy_agent`  
**Inherits from**: `RemoteAgent`

## Key Features

- **Real-time Streaming**: Continuous data flow via Server-Sent Events
- **Live Progress Updates**: Real-time tool calls and observations
- **Remote Agent Integration**: Seamless connection to remote OxyGent systems
- **Call Stack Management**: Configurable call stack sharing
- **Organization Structure**: Dynamic organization discovery
- **Message Filtering**: Intelligent message filtering and forwarding
- **Connection Management**: Automatic connection handling and cleanup

## Core Attributes

### SSE Configuration

- `is_share_call_stack` (bool): Whether to share the call stack with the agent (default: True)

## Key Methods

### Initialization

#### `async def init(self)`

Initializes the SSE agent by discovering the remote organization structure.

**Implementation:**

```python
async def init(self):
    await super().init()
    
    # Discover remote organization structure
    async with httpx.AsyncClient() as client:
        response = await client.get(build_url(self.server_url, "/get_organization"))
        self.org = response.json()["data"]["organization"]
```

**Process:**

1. Calls parent initialization
2. Fetches organization structure from remote server
3. Stores organization data for team coordination

### Core Execution

#### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`

Executes the request through SSE streaming connection.

**Execution Flow:**

1. **Connection Setup**: Establishes SSE connection to remote server
2. **Payload Preparation**: Transforms request for remote compatibility
3. **Streaming Processing**: Handles real-time message stream
4. **Message Filtering**: Processes and forwards relevant messages
5. **Response Assembly**: Collects final response from stream

**Implementation Details:**

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    logger.info(
        f"Initiating SSE connection. {self.server_url}",
        extra={
            "trace_id": oxy_request.current_trace_id,
            "node_id": oxy_request.node_id,
        },
    )
    
    # Prepare payload for remote system
    payload = oxy_request.model_dump(
        exclude={"mas", "parallel_id", "latest_node_ids"}
    )
    payload.update(payload["arguments"])
    payload["caller_category"] = "user"
    
    # Configure call stack sharing
    if self.is_share_call_stack:
        payload["call_stack"] = payload["call_stack"][:-1]
        payload["node_id_stack"] = payload["node_id_stack"][:-1]
    else:
        del payload["call_stack"]
        del payload["node_id_stack"]
        payload["caller"] = "user"
    
    del payload["arguments"]
    
    # Establish SSE connection
    url = build_url(self.server_url, "/sse/chat")
    answer = ""
    
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, data=json.dumps(payload), headers=headers
        ) as resp:
            # Process streaming events
            async for line in resp.content:
                if line:
                    decoded_line = line.decode("utf-8").strip()
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]
                        
                        # Handle termination signal
                        if data == "done":
                            logger.info(f"SSE connection terminated: {self.server_url}")
                            await resp.release()
                            break
                        
                        # Process JSON messages
                        data = json.loads(data)
                        
                        if data["type"] == "answer":
                            answer = data.get("content")
                        elif data["type"] in ["tool_call", "observation"]:
                            # Filter user-category messages
                            if (
                                data["content"]["caller_category"] == "user"
                                or data["content"]["callee_category"] == "user"
                            ):
                                continue
                            else:
                                # Adjust call stack for forwarded messages
                                if not self.is_share_call_stack:
                                    data["content"]["call_stack"] = (
                                        oxy_request.call_stack
                                        + data["content"]["call_stack"][2:]
                                    )
                                await oxy_request.send_message(data)
                        else:
                            # Forward other message types
                            await oxy_request.send_message(data)
    
    return OxyResponse(state=OxyState.COMPLETED, output=answer)
```

## Usage Examples

### Basic SSE Agent

```python
from oxygent.oxy.agents.sse_oxy_agent import SSEOxyGent

# Create SSE agent for remote system
sse_agent = SSEOxyGent(
    name="remote_assistant",
    desc="Remote OxyGent system via SSE",
    server_url="https://remote-oxygent.example.com",
    is_share_call_stack=True
)

# Usage - streams real-time responses
response = await oxy_request.call(
    callee="remote_assistant",
    arguments={
        "query": "Analyze the current market trends",
        "domain": "technology"
    }
)
```

### Multi-Service SSE Integration

```python
# SSE agent for comprehensive remote services
multi_service_agent = SSEOxyGent(
    name="enterprise_brain",
    desc="Enterprise AI system with multiple specialized services",
    server_url="https://enterprise-ai.company.com",
    is_share_call_stack=False,  # Clean call stack for external integration
)

# Initialize to discover available services
await multi_service_agent.init()

# Access discovered organization
available_services = multi_service_agent.get_org()
print("Available remote services:", available_services)

# Usage for complex business process
response = await oxy_request.call(
    callee="enterprise_brain",
    arguments={
        "query": "Process quarterly financial analysis",
        "department": "finance",
        "quarter": "Q3_2024",
        "include_forecasting": True
    }
)
```

### Real-time Progress Monitoring

```python
class ProgressMonitoringSSE(SSEOxyGent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress_callback = None
    
    def set_progress_callback(self, callback):
        """Set callback function for progress updates"""
        self.progress_callback = callback
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Override to add custom progress monitoring
        if self.progress_callback:
            await self.progress_callback("Starting remote execution...")
        
        # Use parent implementation with custom message handling
        original_send_message = oxy_request.send_message
        
        async def enhanced_send_message(message):
            # Custom progress tracking
            if message.get("type") == "tool_call":
                tool_name = message.get("content", {}).get("callee", "unknown")
                if self.progress_callback:
                    await self.progress_callback(f"Executing tool: {tool_name}")
            elif message.get("type") == "observation":
                if self.progress_callback:
                    await self.progress_callback("Tool execution completed")
            
            # Forward to original handler
            return await original_send_message(message)
        
        # Temporarily replace message handler
        oxy_request.send_message = enhanced_send_message
        
        try:
            result = await super()._execute(oxy_request)
            if self.progress_callback:
                await self.progress_callback("Remote execution completed")
            return result
        finally:
            # Restore original handler
            oxy_request.send_message = original_send_message

# Usage with progress monitoring
async def progress_handler(message):
    print(f"[PROGRESS] {message}")

progress_agent = ProgressMonitoringSSE(
    name="monitored_remote",
    server_url="https://slow-processing.example.com"
)
progress_agent.set_progress_callback(progress_handler)
```

## Message Types and Handling

### Supported Message Types

#### 1. Answer Messages

Final responses from the remote system.

```python
{
    "type": "answer",
    "content": "Final response content"
}
```

#### 2. Tool Call Messages  

Real-time tool execution notifications.

```python
{
    "type": "tool_call",
    "content": {
        "node_id": "abc123",
        "caller": "agent_name",
        "callee": "tool_name", 
        "call_stack": ["user", "agent_name"],
        "arguments": {"param": "value"}
    }
}
```

#### 3. Observation Messages

Tool execution results.

```python
{
    "type": "observation", 
    "content": {
        "node_id": "abc123",
        "output": "Tool execution result",
        "call_stack": ["user", "agent_name", "tool_name"]
    }
}
```

#### 4. Custom Messages

Application-specific message types.

```python
{
    "type": "progress",
    "content": {
        "stage": "processing", 
        "progress": 45,
        "message": "Processing data..."
    }
}
```

### Message Filtering Logic

The SSE agent implements intelligent message filtering:

```python
# User-category messages are filtered out (not forwarded)
if (
    data["content"]["caller_category"] == "user"
    or data["content"]["callee_category"] == "user"
):
    continue

# Other messages are forwarded with call stack adjustment
if not self.is_share_call_stack:
    data["content"]["call_stack"] = (
        oxy_request.call_stack + data["content"]["call_stack"][2:]
    )
await oxy_request.send_message(data)
```

## Call Stack Management

### Shared Call Stack Mode (`is_share_call_stack=True`)

- Maintains original call stack from local system
- Enables end-to-end tracing across systems
- Better for integrated environments

```python
# Local call stack: ["user", "local_agent", "sse_agent"]  
# Remote receives: ["user", "local_agent"]
# Messages maintain: original call stack structure
```

### Independent Call Stack Mode (`is_share_call_stack=False`)

- Creates clean separation between systems
- Better for external integrations
- Simplified remote system interface

```python
# Local call stack: ["user", "local_agent", "sse_agent"]
# Remote receives: caller="user" (simplified)
# Messages adjusted: local_stack + remote_stack[2:]
```

## Advanced Patterns

### Connection Resilience

```python
class ResilientSSEAgent(SSEOxyGent):
    def __init__(self, max_retries: int = 3, retry_delay: float = 5.0, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        for attempt in range(self.max_retries + 1):
            try:
                return await super()._execute(oxy_request)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == self.max_retries:
                    return OxyResponse(
                        state=OxyState.FAILED,
                        output=f"SSE connection failed after {self.max_retries} attempts: {str(e)}"
                    )
                
                logger.warning(f"SSE connection failed (attempt {attempt + 1}), retrying in {self.retry_delay}s")
                await asyncio.sleep(self.retry_delay)
```

### Event Filtering and Routing

```python
class CustomEventSSEAgent(SSEOxyGent):
    def __init__(self, event_filter: callable = None, **kwargs):
        super().__init__(**kwargs)
        self.event_filter = event_filter or (lambda x: True)
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Override message processing with custom filtering
        original_implementation = await self._get_base_execution_logic(oxy_request)
        
        # Custom event processing would go here
        # This is a simplified example - actual implementation would
        # need to intercept the SSE stream processing
        
        return original_implementation

    async def _process_custom_event(self, event_data, oxy_request):
        """Process custom event types"""
        if event_data.get("type") == "progress":
            # Handle progress events
            await oxy_request.send_message({
                "type": "progress_update",
                "content": event_data["content"]
            })
        elif event_data.get("type") == "error":
            # Handle error events
            logger.error(f"Remote error: {event_data['content']}")
```

## Performance Considerations

### Connection Management

- **Persistent Connections**: SSE maintains long-lived connections
- **Resource Usage**: Monitor memory usage for long-running streams
- **Timeout Handling**: Implement appropriate timeout strategies

### Streaming Efficiency

- **Buffer Management**: Handle streaming data efficiently
- **Message Processing**: Process messages asynchronously
- **Connection Cleanup**: Ensure proper connection cleanup

### Error Recovery

```python
# Implement timeout and error recovery
async with aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=3600)  # 1 hour timeout
) as session:
    try:
        async with session.post(url, **kwargs) as resp:
            # Process SSE stream
            pass
    except asyncio.TimeoutError:
        # Handle timeout
        logger.error("SSE stream timeout")
    except aiohttp.ClientError as e:
        # Handle connection errors
        logger.error(f"SSE connection error: {e}")
```

## Best Practices

1. **Connection Management**: Implement proper timeout and cleanup
2. **Error Handling**: Handle network errors and connection drops
3. **Message Filtering**: Filter unnecessary messages for performance
4. **Call Stack Strategy**: Choose appropriate call stack sharing mode
5. **Progress Monitoring**: Implement progress callbacks for long operations
6. **Resource Monitoring**: Monitor memory usage for long-running streams
7. **Authentication**: Implement proper authentication for secure connections
8. **Logging**: Log connection events and errors for debugging
9. **Retry Logic**: Implement exponential backoff for connection failures
10. **Performance Testing**: Test with various message volumes and types

## Common Use Cases

1. **Real-time Dashboards**: Live updates for monitoring systems
2. **Progress Tracking**: Long-running task progress visualization
3. **Collaborative Systems**: Multi-user real-time collaboration
4. **Live Analytics**: Real-time data processing and visualization
5. **Chat Applications**: Interactive conversational interfaces
6. **Remote Processing**: Distributed computation with live feedback
7. **Monitoring Systems**: Real-time system health and alerts
8. **Data Streaming**: Continuous data processing pipelines
9. **Interactive Workflows**: Step-by-step process execution
10. **Multi-system Integration**: Real-time integration between systems

## Security Considerations

- **Authentication**: Secure SSE endpoints with proper authentication
- **Data Validation**: Validate incoming SSE messages
- **Rate Limiting**: Implement rate limiting for SSE connections  
- **SSL/TLS**: Use HTTPS for all SSE connections
- **Message Sanitization**: Sanitize message content before forwarding

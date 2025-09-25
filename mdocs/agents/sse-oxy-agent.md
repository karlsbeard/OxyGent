---
title: SSEOxyGent
description: Remote agent for real-time communication with OxyGent systems via Server-Sent Events (SSE)
---

# SSEOxyGent

The `SSEOxyGent` class extends `RemoteAgent` to provide real-time communication with remote OxyGent systems using Server-Sent Events (SSE). This agent enables streaming communication, live updates, and seamless integration with remote OxyGent instances while maintaining full context and call stack information.

## Overview

`SSEOxyGent` is designed for scenarios requiring:

- **Real-time Communication**: Streaming responses from remote OxyGent systems
- **Live Updates**: Receive intermediate results and progress updates
- **Remote Integration**: Seamless connection to distributed OxyGent instances
- **Context Preservation**: Maintain call stack and trace information across remote boundaries
- **Event Streaming**: Handle tool calls, observations, and answers in real-time
- **Distributed Architecture**: Enable multi-instance OxyGent deployments

This agent is particularly useful for:
- Distributed agent architectures across multiple servers
- Real-time collaborative agent systems
- Live dashboard updates and monitoring
- Streaming responses for better user experience
- Load balancing across OxyGent instances

## Architecture

### SSE Communication Flow

```
Local OxyGent Instance
         ↓
   ┌─────────────┐
   │ SSEOxyGent  │
   └─────────────┘
         ↓ HTTP POST /sse/chat
┌─────────────────────────┐
│   Remote OxyGent        │
│   ┌─────────────────┐   │
│   │   Agent/Tool    │   │ ← Processes request
│   └─────────────────┘   │
│          ↓              │
│   ┌─────────────────┐   │
│   │  SSE Stream     │   │ ← Streams events
│   └─────────────────┘   │
└─────────────────────────┘
         ↓ Server-Sent Events
   ┌─────────────┐
   │ Local Agent │ ← Receives stream
   └─────────────┘
```

### Event Types

SSEOxyGent handles multiple event types in the SSE stream:

- **answer**: Final response from the remote system
- **tool_call**: Tool execution request from remote agent
- **observation**: Tool execution results
- **progress**: Intermediate progress updates
- **error**: Error messages and exceptions

## Class Definition

```python
from oxygent.oxy.agents import SSEOxyGent
from oxygent.schemas import OxyRequest, OxyResponse

# Basic SSE agent
sse_agent = SSEOxyGent(
    name="remote_assistant",
    server_url="https://remote-oxygent.example.com",
    is_share_call_stack=True
)
```

## Key Attributes

### is_share_call_stack
- **Type**: `bool`
- **Default**: `True`
- **Description**: Whether to share the call stack with the remote agent

**When True** (default):
- Remote agent receives partial call stack (excluding current agent)
- Enables proper trace and context management across instances
- Allows remote agent to understand the calling context

**When False**:
- Call stack is not shared with remote system
- Remote agent sees request as coming directly from "user"
- Simplified context but loses hierarchical information

## Key Methods

### async init()

Initializes the agent and fetches the remote system's organization structure.

```python
await sse_agent.init()
# Fetches organization from: {server_url}/get_organization
# Populates self.org with remote system capabilities
```

### async _execute(oxy_request: OxyRequest) -> OxyResponse

Executes the SSE communication with the remote OxyGent system.

**Process Flow**:
1. Prepare payload by serializing the request
2. Configure call stack sharing based on settings
3. Establish SSE connection to remote endpoint
4. Stream events and handle different event types
5. Forward relevant events to local message handlers
6. Return final answer when stream completes

## Usage Examples

### Basic Remote Communication

```python
from oxygent.oxy.agents import SSEOxyGent

# Connect to remote OxyGent instance
remote_assistant = SSEOxyGent(
    name="remote_assistant",
    server_url="https://oxygent-instance.company.com",
    is_share_call_stack=True
)

# Initialize to fetch remote organization
await remote_assistant.init()

# Now the agent can be used like any other agent
# Requests will be streamed to the remote system
```

### Multi-Instance Architecture

```python
class DistributedOxyGent:
    def __init__(self):
        self.instances = {}
    
    async def add_remote_instance(self, name: str, url: str):
        """Add a remote OxyGent instance"""
        
        remote_agent = SSEOxyGent(
            name=f"remote_{name}",
            server_url=url,
            is_share_call_stack=True
        )
        
        await remote_agent.init()
        self.instances[name] = remote_agent
        
        # Check remote capabilities
        org = remote_agent.get_org()
        print(f"Connected to {name}: {len(org)} capabilities available")
    
    def get_instance(self, name: str) -> SSEOxyGent:
        return self.instances.get(name)

# Usage
distributed = DistributedOxyGent()
await distributed.add_remote_instance("analytics", "https://analytics.company.com")
await distributed.add_remote_instance("research", "https://research.company.com")

# Route requests to appropriate instances
analytics_agent = distributed.get_instance("analytics")
research_agent = distributed.get_instance("research")
```

### Load Balancing with SSE Agents

```python
import random
from typing import List

class LoadBalancedSSECluster:
    def __init__(self, server_urls: List[str]):
        self.agents = []
        self.current_index = 0
    
    async def initialize(self, server_urls: List[str]):
        """Initialize all remote agents in the cluster"""
        
        for i, url in enumerate(server_urls):
            agent = SSEOxyGent(
                name=f"cluster_node_{i+1}",
                server_url=url,
                is_share_call_stack=True
            )
            
            try:
                await agent.init()
                self.agents.append(agent)
                print(f"✓ Connected to {url}")
            except Exception as e:
                print(f"✗ Failed to connect to {url}: {e}")
    
    def get_next_agent(self) -> SSEOxyGent:
        """Round-robin load balancing"""
        if not self.agents:
            raise Exception("No healthy agents available")
        
        agent = self.agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.agents)
        return agent
    
    def get_random_agent(self) -> SSEOxyGent:
        """Random load balancing"""
        if not self.agents:
            raise Exception("No healthy agents available")
        
        return random.choice(self.agents)

# Usage
cluster = LoadBalancedSSECluster()
await cluster.initialize([
    "https://node1.oxygent.com",
    "https://node2.oxygent.com", 
    "https://node3.oxygent.com"
])

# Get agent for request processing
agent = cluster.get_next_agent()
```

### Development and Production Configuration

```python
from oxygent.oxy.agents import SSEOxyGent
from oxygent.config import Config

class ConfigurableSSEAgent(SSEOxyGent):
    def __init__(self, environment="development", **kwargs):
        
        # Environment-specific configurations
        if environment == "development":
            server_url = "http://localhost:8000"
            is_share_call_stack = True
        elif environment == "staging":
            server_url = "https://staging.oxygent.company.com"
            is_share_call_stack = True
        elif environment == "production":
            server_url = "https://oxygent.company.com"
            is_share_call_stack = False  # Simplified for production
        else:
            raise ValueError(f"Unknown environment: {environment}")
        
        super().__init__(
            server_url=server_url,
            is_share_call_stack=is_share_call_stack,
            **kwargs
        )
        
        self.environment = environment

# Usage
dev_agent = ConfigurableSSEAgent(name="dev_remote", environment="development")
prod_agent = ConfigurableSSEAgent(name="prod_remote", environment="production")
```

### Custom Event Handling

```python
class CustomSSEOxyGent(SSEOxyGent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_handlers = {
            "custom_event": self.handle_custom_event,
            "progress_update": self.handle_progress_update,
            "metrics": self.handle_metrics
        }
    
    async def handle_custom_event(self, event_data):
        """Handle custom event types from remote system"""
        print(f"Custom event received: {event_data}")
    
    async def handle_progress_update(self, event_data):
        """Handle progress updates"""
        progress = event_data.get("progress", 0)
        status = event_data.get("status", "unknown")
        print(f"Progress: {progress}% - {status}")
    
    async def handle_metrics(self, event_data):
        """Handle metrics data"""
        metrics = event_data.get("metrics", {})
        print(f"Metrics: {metrics}")
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Extended execution with custom event handling"""
        
        # Add custom event handling to the SSE processing
        # This would require extending the SSE processing loop
        # to handle additional event types
        
        return await super()._execute(oxy_request)

custom_agent = CustomSSEOxyGent(
    name="custom_remote",
    server_url="https://custom-oxygent.example.com"
)
```

## Event Stream Processing

### Event Types and Handling

```python
# SSE Event Stream Format:
# data: {"type": "answer", "content": "Final response text"}
# data: {"type": "tool_call", "content": {...}}
# data: {"type": "observation", "content": {...}}
# data: done

# Event processing in _execute method:
async for line in resp.content:
    if line:
        decoded_line = line.decode("utf-8").strip()
        if decoded_line.startswith("data: "):
            data = decoded_line[6:]  # Remove "data: " prefix
            
            if data == "done":
                # Stream completed
                break
            
            event = json.loads(data)
            event_type = event["type"]
            
            if event_type == "answer":
                # Final answer from remote system
                answer = event.get("content")
            
            elif event_type == "tool_call":
                # Remote agent is calling a tool
                await self.handle_tool_call_event(event, oxy_request)
            
            elif event_type == "observation":
                # Tool execution result
                await self.handle_observation_event(event, oxy_request)
```

### Message Forwarding

```python
# SSEOxyGent forwards relevant events to local message handlers
# while filtering out user-to-user communications

if data["type"] in ["tool_call", "observation"]:
    content = data["content"]
    
    # Skip user-to-user communications
    if (content["caller_category"] == "user" or 
        content["callee_category"] == "user"):
        continue
    
    # Reconstruct call stack for local context
    if not self.is_share_call_stack:
        content["call_stack"] = (
            oxy_request.call_stack + 
            content["call_stack"][2:]  # Skip remote user context
        )
    
    # Forward to local message handler
    await oxy_request.send_message(data)
```

## Advanced Configuration

### Call Stack Management

```python
class CallStackAwareSSEAgent(SSEOxyGent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_stack_strategy = "partial"  # "full", "partial", "none"
    
    def prepare_payload(self, oxy_request: OxyRequest) -> dict:
        """Customize payload based on call stack strategy"""
        
        payload = oxy_request.model_dump(
            exclude={"mas", "parallel_id", "latest_node_ids"}
        )
        payload.update(payload["arguments"])
        payload["caller_category"] = "user"
        
        if self.call_stack_strategy == "full":
            # Share complete call stack
            pass  # Keep original call stack
        
        elif self.call_stack_strategy == "partial":
            # Share partial call stack (default behavior)
            if self.is_share_call_stack:
                payload["call_stack"] = payload["call_stack"][:-1]
                payload["node_id_stack"] = payload["node_id_stack"][:-1]
        
        elif self.call_stack_strategy == "none":
            # Don't share call stack
            del payload["call_stack"]
            del payload["node_id_stack"]
            payload["caller"] = "user"
        
        del payload["arguments"]
        return payload
```

### Connection Management

```python
class ResilientSSEAgent(SSEOxyGent):
    def __init__(self, max_retries=3, retry_delay=1.0, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with connection retry logic"""
        
        for attempt in range(self.max_retries + 1):
            try:
                return await super()._execute(oxy_request)
            
            except aiohttp.ClientError as e:
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                else:
                    return OxyResponse(
                        state=OxyState.ERROR,
                        output=f"Failed to connect to remote system after {self.max_retries} attempts: {e}"
                    )
            
            except Exception as e:
                # Non-network errors should not be retried
                return OxyResponse(
                    state=OxyState.ERROR,
                    output=f"Remote execution error: {e}"
                )

resilient_agent = ResilientSSEAgent(
    name="resilient_remote",
    server_url="https://remote.example.com",
    max_retries=3,
    retry_delay=2.0
)
```

## Monitoring and Debugging

### Connection Monitoring

```python
class MonitoredSSEAgent(SSEOxyGent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0
        }
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        start_time = time.time()
        self.connection_stats["total_requests"] += 1
        
        try:
            response = await super()._execute(oxy_request)
            
            if response.state == OxyState.COMPLETED:
                self.connection_stats["successful_requests"] += 1
            else:
                self.connection_stats["failed_requests"] += 1
            
            # Update average response time
            response_time = time.time() - start_time
            current_avg = self.connection_stats["average_response_time"]
            total_requests = self.connection_stats["total_requests"]
            
            self.connection_stats["average_response_time"] = (
                (current_avg * (total_requests - 1) + response_time) / total_requests
            )
            
            return response
        
        except Exception as e:
            self.connection_stats["failed_requests"] += 1
            raise
    
    def get_connection_stats(self) -> dict:
        return self.connection_stats.copy()

monitored_agent = MonitoredSSEAgent(
    name="monitored_remote",
    server_url="https://remote.example.com"
)

# Check stats
stats = monitored_agent.get_connection_stats()
print(f"Success rate: {stats['successful_requests'] / stats['total_requests'] * 100:.1f}%")
```

## Security Considerations

### HTTPS Enforcement

```python
class SecureSSEAgent(SSEOxyGent):
    def __init__(self, **kwargs):
        if not kwargs.get("server_url", "").startswith("https://"):
            raise ValueError("Only HTTPS connections are allowed")
        super().__init__(**kwargs)
```

### Authentication and Headers

```python
class AuthenticatedSSEAgent(SSEOxyGent):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Add authentication headers to the SSE request
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "OxyGent-SSEClient/1.0"
        }
        
        # Custom execution with auth headers
        # (Would require modifying the SSE connection setup)
        
        return await super()._execute(oxy_request)
```

## Best Practices

1. **Use HTTPS in Production**: Always use secure connections for production systems
   ```python
   server_url = "https://secure-oxygent.company.com"  # Preferred
   server_url = "http://localhost:8000"               # Only for development
   ```

2. **Handle Connection Failures**: Implement retry logic and graceful degradation
   ```python
   try:
       response = await sse_agent.execute(request)
   except ConnectionError:
       # Fallback to local processing or error handling
   ```

3. **Monitor Performance**: Track connection statistics and response times
   ```python
   # Monitor success rates, response times, and error patterns
   ```

4. **Configure Call Stack Sharing**: Choose appropriate level for your architecture
   ```python
   # For hierarchical systems: is_share_call_stack=True
   # For simplified remote calls: is_share_call_stack=False
   ```

5. **Initialize Before Use**: Always call `init()` to fetch remote organization
   ```python
   await sse_agent.init()  # Fetch remote capabilities
   ```

## Common Use Cases

- **Microservices Architecture**: Connect OxyGent instances across services
- **Cloud Distribution**: Load balance across cloud instances
- **Real-time Collaboration**: Multiple users working with distributed agents
- **Hybrid Deployments**: Mix of local and remote agent capabilities
- **Development/Testing**: Connect to development instances from local environment

## Performance Considerations

- **Streaming**: Responses stream in real-time for better user experience
- **Network Latency**: Consider network delays for remote communications
- **Connection Pooling**: Reuse connections when possible
- **Timeout Management**: Set appropriate timeouts for remote calls

## Related Classes

- **[RemoteAgent](./remote-agent)**: Parent class providing remote communication foundation
- **[LocalAgent](./local-agent)**: Local execution alternative
- **[BaseAgent](./base-agent)**: Foundation class with trace management

## See Also

- [Agent System Overview](./index)
- [Remote Agent Documentation](./remote-agent)
- [Distributed Architecture Guide](../architecture/distributed)
- [Network Configuration](../config/network)
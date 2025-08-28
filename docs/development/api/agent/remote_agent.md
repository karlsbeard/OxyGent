# RemoteAgent Class

## Overview

The `RemoteAgent` class provides the foundation for connecting to and interacting with remote agent systems over HTTP/HTTPS. It serves as the base class for agents that communicate with external systems while maintaining integration with the local OxyGent framework.

## Class Definition

```python
class RemoteAgent(BaseAgent)
```

**Module**: `oxygent.oxy.agents.remote_agent`  
**Inherits from**: `BaseAgent`

## Core Attributes

### Remote Connection

- `server_url` (AnyUrl, required): The URL of the remote agent server
- `org` (dict): Organization structure from the remote system (default: empty dict)

## Validation

### URL Validation

#### `@field_validator("server_url")`

Validates that the server URL uses supported protocols.

**Supported Protocols:**

- `http://`
- `https://`

**Validation Logic:**

```python
@field_validator("server_url")
def check_protocol(cls, v):
    if v.scheme not in ("http", "https"):
        raise ValueError("server_url must start with http:// or https://")
    return v
```

**Example:**

```python
# Valid URLs
RemoteAgent(server_url="https://api.example.com")
RemoteAgent(server_url="http://localhost:8080")

# Invalid URL - raises ValueError
RemoteAgent(server_url="ftp://example.com")
```

## Key Methods

### Organization Management

#### `def get_org(self)`

Returns the organization structure with remote marking for all child nodes.

**Functionality:**

- Creates a deep copy of the organization structure
- Recursively marks all nodes as remote
- Preserves the original organization hierarchy

**Implementation:**

```python
def get_org(self):
    def update_children(children):
        for node in children:
            node["is_remote"] = True
            if "children" in node and isinstance(node["children"], list):
                update_children(node["children"])
        return children
    
    # Create deep copy and mark as remote
    children_copy = copy.deepcopy(self.org["children"])
    return update_children(children_copy)
```

**Return Structure:**

```python
{
    "children": [
        {
            "name": "remote_service",
            "is_remote": True,
            "children": [
                {
                    "name": "sub_service",
                    "is_remote": True,
                    # ... nested structure
                }
            ]
        }
    ]
}
```

### Abstract Methods

#### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`

**Status**: Not implemented (raises `NotImplementedError`)

This method must be overridden by concrete remote agent implementations to define the specific communication protocol with the remote system.

**Implementation Requirements:**

- Handle HTTP/HTTPS communication with the remote server
- Transform OxyRequest to remote-compatible format
- Process remote responses back to OxyResponse format
- Manage authentication and connection handling
- Implement error recovery and retry logic

## Usage Examples

### Basic Remote Agent Implementation

```python
from oxygent.oxy.agents.remote_agent import RemoteAgent
import httpx

class HTTPRemoteAgent(RemoteAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="http_agent",
            desc="HTTP-based remote agent",
            server_url="https://api.example.com",
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Transform request for remote system
        payload = {
            "query": oxy_request.get_query(),
            "arguments": oxy_request.arguments,
            "trace_id": oxy_request.current_trace_id
        }
        
        # Send HTTP request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server_url}/execute",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            return OxyResponse(
                state=OxyState.COMPLETED,
                output=result["output"],
                extra=result.get("metadata", {})
            )
```

### Organization Structure Handling

```python
class OrganizationAwareRemoteAgent(RemoteAgent):
    def __init__(self, **kwargs):
        super().__init__(
            server_url="https://multi-agent.example.com",
            org={
                "children": [
                    {
                        "name": "nlp_service",
                        "children": [
                            {"name": "tokenizer"},
                            {"name": "classifier"}
                        ]
                    },
                    {
                        "name": "ml_service", 
                        "children": [
                            {"name": "predictor"},
                            {"name": "trainer"}
                        ]
                    }
                ]
            },
            **kwargs
        )
    
    def get_available_services(self):
        """Get list of available remote services"""
        org_structure = self.get_org()
        services = []
        
        def collect_services(nodes):
            for node in nodes:
                services.append(node["name"])
                if "children" in node:
                    collect_services(node["children"])
        
        collect_services(org_structure["children"])
        return services
```

### Authentication Integration

```python
class AuthenticatedRemoteAgent(RemoteAgent):
    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = self._prepare_request(oxy_request)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server_url}/api/execute",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                return OxyResponse(
                    state=OxyState.FAILED,
                    output="Authentication failed"
                )
            
            response.raise_for_status()
            return self._process_response(response.json())
```

## Integration Patterns

### With Local MAS

RemoteAgent maintains full integration with the local Multi-Agent System:

```python
# Remote agent registration
remote_agent = HTTPRemoteAgent(
    name="external_processor",
    server_url="https://processing.example.com"
)

# Integration with local MAS
mas.register_agent(remote_agent)

# Usage in local workflows
local_result = await oxy_request.call(
    callee="external_processor",
    arguments={"data": processing_data}
)
```

### Error Handling Patterns

```python
class ResilientRemoteAgent(RemoteAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        for attempt in range(self.retries):
            try:
                return await self._try_execute(oxy_request)
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                if attempt == self.retries - 1:
                    return OxyResponse(
                        state=OxyState.FAILED,
                        output=f"Remote service unavailable: {str(e)}"
                    )
                await asyncio.sleep(self.delay * (attempt + 1))  # Exponential backoff
            except httpx.HTTPError as e:
                return OxyResponse(
                    state=OxyState.FAILED,
                    output=f"HTTP error: {str(e)}"
                )
```

## Advanced Features

### Connection Pooling

```python
class PooledRemoteAgent(RemoteAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = None
    
    async def init(self):
        await super().init()
        self._client = httpx.AsyncClient(
            base_url=str(self.server_url),
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        response = await self._client.post("/execute", json=payload)
        # Process response
    
    async def cleanup(self):
        if self._client:
            await self._client.aclose()
```

### Protocol Abstraction

```python
class MultiProtocolRemoteAgent(RemoteAgent):
    def __init__(self, protocol: str = "http", **kwargs):
        super().__init__(**kwargs)
        self.protocol = protocol
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        if self.protocol == "http":
            return await self._http_execute(oxy_request)
        elif self.protocol == "websocket":
            return await self._websocket_execute(oxy_request)
        elif self.protocol == "grpc":
            return await self._grpc_execute(oxy_request)
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")
```

## Best Practices

1. **URL Validation**: Always use HTTPS in production environments
2. **Error Handling**: Implement comprehensive error handling for network issues
3. **Timeout Management**: Set appropriate timeouts for remote calls
4. **Authentication**: Secure remote communications with proper authentication
5. **Connection Pooling**: Use connection pooling for high-frequency communications
6. **Organization Structure**: Maintain clear organization hierarchies for complex remote systems
7. **Retry Logic**: Implement exponential backoff for transient failures
8. **Monitoring**: Add logging and monitoring for remote service health
9. **Data Transformation**: Handle data format differences between local and remote systems
10. **Security**: Validate and sanitize data exchanged with remote systems

## Configuration

RemoteAgent inherits all configuration from BaseAgent and adds:

- Network timeout configuration
- Connection retry policies
- Authentication configuration
- Protocol-specific settings

## Common Use Cases

1. **External API Integration**: Connect to third-party services
2. **Distributed Computing**: Leverage remote computational resources
3. **Microservice Architecture**: Integrate with microservice ecosystems
4. **Cloud Service Integration**: Connect to cloud-based AI services
5. **Legacy System Integration**: Interface with existing remote systems
6. **Load Distribution**: Distribute processing across remote nodes

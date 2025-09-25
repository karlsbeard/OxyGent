---
title: RemoteAgent
description: Foundation class for agents that communicate with remote agent systems over HTTP/HTTPS
---

# RemoteAgent

The `RemoteAgent` class extends `BaseAgent` to provide the foundation for connecting to and interacting with remote agent systems over HTTP/HTTPS protocols. It serves as the base class for agents that need to communicate with external OxyGent instances or other compatible remote systems.

## Overview

`RemoteAgent` is designed for distributed agent architectures where agents need to:

- **Connect to Remote Systems**: Establish communication with remote OxyGent instances
- **Manage Organization Structure**: Handle remote system organization hierarchies
- **Validate Connection Parameters**: Ensure proper HTTP/HTTPS endpoint configuration
- **Provide Remote Context**: Mark remote operations for proper routing and handling

## Class Definition

```python
from oxygent.oxy.agents import RemoteAgent
from oxygent.schemas import OxyRequest, OxyResponse

class MyRemoteAgent(RemoteAgent):
    def __init__(self, **kwargs):
        super().__init__(
            server_url="https://remote-oxygent.example.com",
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Your remote communication implementation
        pass
```

## Attributes

### server_url
- **Type**: `AnyUrl`
- **Required**: Yes
- **Description**: The URL of the remote agent server
- **Validation**: Must start with `http://` or `https://`

```python
# Valid examples:
server_url = "https://api.example.com"
server_url = "http://localhost:8000"
server_url = "https://remote-agent.company.com:8443"

# Invalid examples (will raise ValueError):
server_url = "ftp://example.com"      # Wrong protocol
server_url = "example.com"            # Missing protocol
server_url = "tcp://example.com"      # Wrong protocol
```

### org
- **Type**: `dict`
- **Default**: `{}`
- **Description**: Organization structure retrieved from the remote system

```python
# Example organization structure:
{
    "name": "Remote OxyGent Instance",
    "version": "1.0.0", 
    "children": [
        {
            "name": "data_agent",
            "type": "agent",
            "description": "Handles data processing tasks"
        },
        {
            "name": "analysis_agent", 
            "type": "agent",
            "description": "Performs data analysis"
        }
    ]
}
```

## Key Methods

### URL Validation

The `RemoteAgent` includes automatic URL validation using Pydantic:

```python
@field_validator("server_url")
def check_protocol(cls, v):
    if v.scheme not in ("http", "https"):
        raise ValueError("server_url must start with http:// or https://")
    return v
```

**Supported Protocols**:
- `http://` - For development and internal networks
- `https://` - For production and secure communication

### get_org() -> list

Returns the organization structure with remote markings applied.

```python
# Original organization structure is modified to include remote markers
remote_org = agent.get_org()

# Each node in the structure will have:
{
    "name": "agent_name",
    "type": "agent", 
    "description": "Agent description",
    "is_remote": True  # Added by get_org()
}
```

**Functionality**:
- Creates a deep copy of the organization structure
- Recursively marks all nodes with `is_remote: True`
- Preserves the original hierarchy and metadata
- Returns the modified structure for integration with local systems

## Usage Examples

### Basic Remote Agent

```python
from oxygent.oxy.agents import RemoteAgent
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class SimpleRemoteAgent(RemoteAgent):
    def __init__(self, **kwargs):
        super().__init__(
            server_url="https://remote-system.example.com",
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Basic remote communication example
        query = oxy_request.get_query()
        
        # Your remote communication logic here
        # This is where you'd implement the actual HTTP/HTTPS communication
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=f"Processed remotely: {query}"
        )
```

### Configuration-Based Remote Agent

```python
class ConfigurableRemoteAgent(RemoteAgent):
    def __init__(self, remote_config: dict, **kwargs):
        """Initialize with configuration dictionary"""
        super().__init__(
            server_url=remote_config["endpoint"],
            **kwargs
        )
        self.api_key = remote_config.get("api_key")
        self.timeout = remote_config.get("timeout", 30)
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Implementation with configuration
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Your remote execution logic
        return OxyResponse(
            state=OxyState.COMPLETED,
            output="Remote execution completed"
        )

# Usage:
config = {
    "endpoint": "https://api.remote-system.com",
    "api_key": "your-api-key",
    "timeout": 60
}
agent = ConfigurableRemoteAgent(remote_config=config, name="remote_processor")
```

### Organization-Aware Remote Agent

```python
class OrgAwareRemoteAgent(RemoteAgent):
    async def init(self):
        """Initialize and fetch organization structure"""
        await super().init()
        # Fetch organization structure from remote system
        # (Implementation depends on your specific remote protocol)
        self.org = await self.fetch_remote_organization()
    
    async def fetch_remote_organization(self) -> dict:
        """Fetch organization structure from remote system"""
        # Example implementation
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server_url}/api/organization")
            return response.json()
    
    def list_remote_capabilities(self) -> list[str]:
        """Get list of available remote capabilities"""
        remote_org = self.get_org()
        capabilities = []
        
        def extract_capabilities(nodes):
            for node in nodes:
                if node.get("type") == "agent":
                    capabilities.append(node["name"])
                if "children" in node:
                    extract_capabilities(node["children"])
        
        extract_capabilities(remote_org)
        return capabilities

# Usage:
agent = OrgAwareRemoteAgent(server_url="https://remote.example.com")
await agent.init()
capabilities = agent.list_remote_capabilities()
# Returns: ["data_agent", "analysis_agent", ...]
```

### Load-Balanced Remote Agent

```python
import random
from typing import List

class LoadBalancedRemoteAgent(RemoteAgent):
    def __init__(self, server_urls: List[str], **kwargs):
        """Initialize with multiple server endpoints for load balancing"""
        # Start with the first server
        super().__init__(server_url=server_urls[0], **kwargs)
        self.all_servers = server_urls
        self.current_server_index = 0
    
    def get_next_server(self) -> str:
        """Round-robin server selection"""
        self.current_server_index = (self.current_server_index + 1) % len(self.all_servers)
        return self.all_servers[self.current_server_index]
    
    def get_random_server(self) -> str:
        """Random server selection"""
        return random.choice(self.all_servers)
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Try current server first, fallback to others if needed
        max_retries = len(self.all_servers)
        
        for attempt in range(max_retries):
            try:
                # Your remote execution logic here
                result = await self.execute_on_server(self.server_url, oxy_request)
                return result
            except Exception as e:
                if attempt < max_retries - 1:
                    # Switch to next server and retry
                    self.server_url = self.get_next_server()
                    continue
                else:
                    # All servers failed
                    raise e

# Usage:
servers = [
    "https://server1.example.com",
    "https://server2.example.com", 
    "https://server3.example.com"
]
agent = LoadBalancedRemoteAgent(server_urls=servers, name="load_balanced_remote")
```

## Integration Patterns

### With Local Agent System

RemoteAgent integrates seamlessly with local agent hierarchies:

```python
class HybridAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add remote agents as sub-agents
        self.sub_agents = ["local_processor", "remote_analyzer"]
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        task_type = oxy_request.arguments.get("task_type")
        
        if task_type == "local":
            return await oxy_request.call(
                callee="local_processor",
                arguments=oxy_request.arguments
            )
        elif task_type == "remote":
            return await oxy_request.call(
                callee="remote_analyzer",  # This could be a RemoteAgent
                arguments=oxy_request.arguments
            )
```

### Organization Structure Integration

```python
def merge_remote_organizations(local_org: dict, remote_agents: List[RemoteAgent]) -> dict:
    """Merge multiple remote organizations with local structure"""
    merged_org = local_org.copy()
    
    for remote_agent in remote_agents:
        remote_org = remote_agent.get_org()
        # Add remote capabilities to merged structure
        merged_org["children"].extend(remote_org)
    
    return merged_org
```

## Error Handling

RemoteAgent includes validation and error handling:

### URL Validation Errors

```python
try:
    agent = RemoteAgent(server_url="invalid-url")
except ValueError as e:
    # Handle validation error
    print(f"Invalid server URL: {e}")
```

### Connection Error Handling

```python
class RobustRemoteAgent(RemoteAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        try:
            # Remote execution logic
            return await self.execute_remotely(oxy_request)
        except ConnectionError:
            # Handle connection failures
            return OxyResponse(
                state=OxyState.ERROR,
                output="Remote system unavailable"
            )
        except TimeoutError:
            # Handle timeouts
            return OxyResponse(
                state=OxyState.ERROR,
                output="Remote request timed out"
            )
```

## Security Considerations

### HTTPS Enforcement

```python
class SecureRemoteAgent(RemoteAgent):
    @field_validator("server_url")
    def enforce_https(cls, v):
        if v.scheme != "https":
            raise ValueError("Only HTTPS connections are allowed in production")
        return v
```

### Authentication Headers

```python
class AuthenticatedRemoteAgent(RemoteAgent):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key
    
    def get_auth_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "OxyGent-RemoteAgent/1.0"
        }
```

## Best Practices

1. **Use HTTPS in Production**: Always use secure connections for production systems
   ```python
   server_url = "https://secure-endpoint.com"  # Preferred
   server_url = "http://localhost:8000"        # Only for development
   ```

2. **Implement Retry Logic**: Handle temporary connection failures gracefully
   ```python
   async def _execute_with_retry(self, oxy_request: OxyRequest) -> OxyResponse:
       for attempt in range(3):
           try:
               return await self._execute(oxy_request)
           except ConnectionError:
               if attempt < 2:
                   await asyncio.sleep(2 ** attempt)  # Exponential backoff
               else:
                   raise
   ```

3. **Validate Organization Structure**: Ensure remote capabilities match expectations
   ```python
   def validate_remote_org(self, required_agents: List[str]):
       available = self.list_remote_capabilities()
       missing = set(required_agents) - set(available)
       if missing:
           raise ValueError(f"Missing remote agents: {missing}")
   ```

4. **Handle Network Timeouts**: Set appropriate timeout values
   ```python
   self.timeout = 30  # seconds
   self.retry_attempts = 3
   ```

## Related Classes

- **[BaseAgent](./base-agent)**: Parent class providing trace management
- **[SSEOxyGent](./sse-oxy-agent)**: Concrete implementation for SSE communication
- **[LocalAgent](./local-agent)**: Local execution alternative

## See Also

- [Agent System Overview](./index)
- [SSE OxyGent Documentation](./sse-oxy-agent)
- [Network Configuration](../config/network)
- [Security Guidelines](../security)
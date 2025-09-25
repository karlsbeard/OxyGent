---
title: StreamableMCPClient
description: Streamable HTTP MCP client for bidirectional streaming communication in OxyGent
---

# StreamableMCPClient

The `StreamableMCPClient` implements MCP communication over streamable HTTP transport. This method provides bidirectional streaming capabilities over HTTP, combining the reliability of HTTP with real-time streaming features.

## Class Overview

```python
from oxygent.oxy.mcp_tools import StreamableMCPClient
from oxygent.oxy.mcp_tools.base_mcp_client import BaseMCPClient

class StreamableMCPClient(BaseMCPClient):
    """MCP client implementation using Streamable-HTTP transport."""
```

## Core Attributes

### `server_url: AnyUrl`
The HTTP endpoint URL for the streamable MCP server.

### `headers: Dict[str, str]`
Extra HTTP headers for the connection.

### `middlewares: List[Any]`
Client-side MCP middlewares for request processing.

## Quick Start

### Basic HTTP Streaming Server

```python
from oxygent.oxy.mcp_tools import StreamableMCPClient

# HTTP streaming MCP server
client = StreamableMCPClient(
    name="http_stream",
    desc="HTTP streaming server",
    server_url="https://mcp-server.example.com/stream"
)

await client.init()
```

### Authenticated Connection

```python
# Secure HTTP streaming with authentication
secure_client = StreamableMCPClient(
    name="secure_stream",
    server_url="https://secure-mcp.example.com/stream",
    headers={
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
)
```

## Configuration Examples

### Production Setup

```python
prod_client = StreamableMCPClient(
    name="production_http",
    desc="Production HTTP streaming server",
    server_url="https://api.company.com/mcp/stream",
    headers={
        "Authorization": f"Bearer {os.getenv('MCP_TOKEN')}",
        "User-Agent": "OxyGent/1.0",
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    middlewares=[
        AuthenticationMiddleware(),
        LoggingMiddleware()
    ],
    is_keep_alive=True,
    timeout=120.0
)
```

### Load Balancing

```python
# Multiple endpoints for load balancing
endpoints = [
    "https://mcp-1.example.com/stream",
    "https://mcp-2.example.com/stream",
    "https://mcp-3.example.com/stream"
]

clients = []
for i, endpoint in enumerate(endpoints):
    client = StreamableMCPClient(
        name=f"http_server_{i}",
        server_url=endpoint,
        headers=common_headers
    )
    clients.append(client)

# Initialize all clients
for client in clients:
    await client.init()
```

## Integration Examples

### Web Service Integration

```python
# RESTful API integration via HTTP streaming
api_client = StreamableMCPClient(
    name="api_gateway",
    server_url="https://api.company.com/mcp/stream",
    headers={
        "Authorization": f"Bearer {api_key}",
        "X-API-Version": "v1"
    }
)

# Use with agents for API operations
api_agent = ChatAgent(name="api_specialist")
api_agent.add_oxy(api_client)
```

### Microservices Communication

```python
# Multiple microservice endpoints
services = {
    "user_service": "https://users.company.com/mcp/stream",
    "order_service": "https://orders.company.com/mcp/stream",
    "payment_service": "https://payments.company.com/mcp/stream"
}

service_clients = {}
for service_name, url in services.items():
    client = StreamableMCPClient(
        name=service_name,
        server_url=url,
        headers={"Authorization": f"Bearer {service_tokens[service_name]}"}
    )
    service_clients[service_name] = client
    await client.init()
```

## Advanced Features

### Connection Health Monitoring

```python
class HealthMonitoredStreamableClient(StreamableMCPClient):
    """Streamable client with health monitoring."""
    
    async def health_check(self) -> bool:
        """Check server health via HTTP ping."""
        try:
            # Simple health check request
            await self.call_tool("health_check", {})
            return True
        except Exception:
            return False
    
    async def ensure_healthy(self):
        """Ensure client connection is healthy."""
        if not await self.health_check():
            await self.cleanup()
            await self.init(is_fetch_tools=False)
```

### Request/Response Caching

```python
class CachedStreamableClient(StreamableMCPClient):
    """Streamable client with response caching."""
    
    def __init__(self, cache_size=1000, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}
        self.cache_size = cache_size
    
    async def _execute(self, oxy_request):
        """Execute with caching support."""
        cache_key = f"{oxy_request.callee}:{hash(str(oxy_request.arguments))}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = await super()._execute(oxy_request)
        
        # Cache successful responses
        if response.state == OxyState.COMPLETED:
            if len(self.cache) >= self.cache_size:
                # Remove oldest entry
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            
            self.cache[cache_key] = response
        
        return response
```

## Security Features

### HTTPS Enforcement

```python
def ensure_https_url(url: str) -> str:
    """Ensure URL uses HTTPS in production."""
    if not url.startswith(('https://', 'http://localhost', 'http://127.0.0.1')):
        raise ValueError(f"HTTPS required for production: {url}")
    return url

# Production client with HTTPS enforcement
secure_client = StreamableMCPClient(
    name="secure_http",
    server_url=ensure_https_url("https://secure-api.company.com/stream"),
    headers={"Authorization": f"Bearer {secure_token}"}
)
```

### Certificate Validation

```python
import ssl
import httpx

class SecureStreamableClient(StreamableMCPClient):
    """Streamable client with enhanced security."""
    
    def __init__(self, verify_ssl=True, **kwargs):
        super().__init__(**kwargs)
        self.verify_ssl = verify_ssl
    
    async def init(self, is_fetch_tools=True):
        """Initialize with SSL verification."""
        # Configure SSL context if needed
        if self.verify_ssl:
            ssl_context = ssl.create_default_context()
            # Additional SSL configuration
        
        await super().init(is_fetch_tools)
```

## Performance Optimization

### Connection Pooling

```python
class PooledStreamableManager:
    """Manager for pooled streamable HTTP connections."""
    
    def __init__(self, server_url: str, pool_size: int = 5):
        self.server_url = server_url
        self.pool_size = pool_size
        self.available_clients = asyncio.Queue()
        self.all_clients = []
    
    async def initialize_pool(self):
        """Initialize connection pool."""
        for i in range(self.pool_size):
            client = StreamableMCPClient(
                name=f"pooled_http_{i}",
                server_url=self.server_url,
                is_keep_alive=True
            )
            await client.init(is_fetch_tools=False)
            self.all_clients.append(client)
            await self.available_clients.put(client)
    
    async def get_client(self) -> StreamableMCPClient:
        """Get client from pool."""
        return await self.available_clients.get()
    
    async def return_client(self, client: StreamableMCPClient):
        """Return client to pool."""
        await self.available_clients.put(client)
    
    async def cleanup_pool(self):
        """Cleanup all pooled clients."""
        for client in self.all_clients:
            await client.cleanup()
```

### Batch Request Processing

```python
class BatchStreamableClient(StreamableMCPClient):
    """Streamable client with batch processing."""
    
    async def execute_batch(self, requests: list[OxyRequest]) -> list[OxyResponse]:
        """Execute multiple requests efficiently."""
        # Process requests in parallel
        tasks = [self._execute(req) for req in requests]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_responses = []
        for response in responses:
            if isinstance(response, Exception):
                processed_responses.append(
                    OxyResponse(state=OxyState.FAILED, output=str(response))
                )
            else:
                processed_responses.append(response)
        
        return processed_responses
```

## Error Handling

### Retry Logic

```python
class ResilientStreamableClient(StreamableMCPClient):
    """Streamable client with retry logic."""
    
    def __init__(self, max_retries=3, retry_delay=1.0, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def _execute_with_retry(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with exponential backoff retry."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await self._execute(oxy_request)
            except httpx.HTTPError as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(f"HTTP request failed (attempt {attempt + 1}), retrying in {delay}s")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Max retries exceeded for {oxy_request.callee}")
            except Exception as e:
                # Don't retry for non-HTTP errors
                return OxyResponse(state=OxyState.FAILED, output=str(e))
        
        return OxyResponse(state=OxyState.FAILED, output=str(last_exception))
```

## Best Practices

### Configuration Management

```python
# ✅ Good: Centralized configuration
@dataclass
class StreamableConfig:
    server_url: str
    auth_token: str
    timeout: float = 60.0
    keep_alive: bool = True
    
    @classmethod
    def from_env(cls, prefix: str = "STREAMABLE_"):
        """Load from environment variables."""
        return cls(
            server_url=os.getenv(f"{prefix}URL"),
            auth_token=os.getenv(f"{prefix}TOKEN"),
            timeout=float(os.getenv(f"{prefix}TIMEOUT", "60.0")),
            keep_alive=os.getenv(f"{prefix}KEEP_ALIVE", "true").lower() == "true"
        )

# Usage
config = StreamableConfig.from_env("API_")
client = StreamableMCPClient(
    name="configured_client",
    server_url=config.server_url,
    headers={"Authorization": f"Bearer {config.auth_token}"},
    timeout=config.timeout,
    is_keep_alive=config.keep_alive
)
```

### Resource Cleanup

```python
# ✅ Good: Automatic cleanup
async def use_streamable_client():
    client = None
    try:
        client = StreamableMCPClient(
            name="temp_client",
            server_url="https://api.example.com/stream"
        )
        await client.init()
        
        # Use client
        response = await client._execute(request)
        return response
    finally:
        if client:
            await client.cleanup()
```

## API Reference

### Complete Class Definition

```python
class StreamableMCPClient(BaseMCPClient):
    """MCP client implementation using Streamable-HTTP transport."""
    
    server_url: AnyUrl = Field("")
    headers: Dict[str, str] = Field(default_factory=dict, description="Extra HTTP headers")
    middlewares: List[Any] = Field(default_factory=list, description="Client-side MCP middlewares")
    
    async def init(self, is_fetch_tools=True) -> None:
        """Initialize HTTP streaming connection to MCP server."""
        
    async def call_tool(self, tool_name, arguments):
        """Execute tool with one-shot HTTP connection."""
```

### Configuration Schema

```python
{
    "server_url": "https://server.com/stream",  # HTTP endpoint URL
    "headers": {                                # HTTP headers
        "Authorization": "Bearer token",
        "Content-Type": "application/json"
    },
    "middlewares": [middleware_instance],       # Middleware list
    "is_keep_alive": True,                      # Connection persistence  
    "timeout": 60.0                             # Request timeout
}
```

## See Also

- [BaseMCPClient](./base-mcp-client) - Base MCP client functionality
- [StdioMCPClient](./stdio-mcp-client) - Standard I/O transport
- [SSEMCPClient](./sse-mcp-client) - Server-Sent Events transport
- [MCPTool](./mcp-tool) - Individual MCP tool proxy
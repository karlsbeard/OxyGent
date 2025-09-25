---
title: SSEMCPClient
description: Server-Sent Events MCP client for real-time streaming communication in OxyGent
---

# SSEMCPClient

The `SSEMCPClient` implements MCP communication over Server-Sent Events (SSE). This transport enables real-time, unidirectional communication from MCP servers to clients, making it ideal for streaming responses, live updates, and real-time data processing.

## Class Overview

```python
from oxygent.oxy.mcp_tools import SSEMCPClient
from oxygent.oxy.mcp_tools.base_mcp_client import BaseMCPClient

class SSEMCPClient(BaseMCPClient):
    """MCP client implementation using Server-Sent Events transport."""
```

## Core Attributes

### `sse_url: AnyUrl`
The Server-Sent Events endpoint URL for the MCP server.

```python
client = SSEMCPClient(
    name="realtime_server",
    sse_url="https://mcp-server.example.com/sse"
)
```

### `headers: Dict[str, str]`
Extra HTTP headers to include in SSE connection requests.

```python
client = SSEMCPClient(
    name="authenticated_server",
    sse_url="https://secure-mcp.example.com/sse",
    headers={
        "Authorization": "Bearer your-api-token",
        "User-Agent": "OxyGent/1.0",
        "Accept": "text/event-stream"
    }
)
```

### `middlewares: List[Any]`
Client-side MCP middlewares for request/response processing.

```python
client = SSEMCPClient(
    name="middleware_server",
    sse_url="https://mcp-server.example.com/sse",
    middlewares=[
        AuthenticationMiddleware(),
        LoggingMiddleware(),
        RetryMiddleware(max_attempts=3)
    ]
)
```

## Key Features

- **Real-time Streaming**: Unidirectional server-to-client communication
- **HTTP-based**: Works over standard HTTP/HTTPS infrastructure
- **Middleware Support**: Extensible middleware system for custom processing
- **Automatic Reconnection**: Built-in connection recovery for network issues
- **Authentication**: Full support for HTTP headers and authentication
- **Keep-Alive Options**: Persistent vs. one-shot connection modes

## Quick Start

### Basic SSE Server Connection

```python
from oxygent.oxy.mcp_tools import SSEMCPClient

# Simple SSE MCP server
client = SSEMCPClient(
    name="data_stream",
    desc="Real-time data streaming server",
    sse_url="https://mcp-server.example.com/sse"
)

# Initialize and discover tools
await client.init()
# Server pushes tool definitions via SSE
```

### Authenticated Connection

```python
# Secure SSE server with authentication
secure_client = SSEMCPClient(
    name="secure_stream",
    desc="Authenticated streaming server", 
    sse_url="https://secure-mcp.example.com/sse",
    headers={
        "Authorization": f"Bearer {get_auth_token()}",
        "X-Client-ID": "oxygent-client-123"
    }
)

await secure_client.init()
```

### With Middleware

```python
# Custom middleware for logging and retry
import logging

class LoggingMiddleware:
    async def __call__(self, request, call_next):
        logging.info(f"SSE Request: {request}")
        response = await call_next(request)
        logging.info(f"SSE Response: {response}")
        return response

client = SSEMCPClient(
    name="logged_server",
    sse_url="https://mcp-server.example.com/sse",
    middlewares=[LoggingMiddleware()]
)
```

## Methods

### `async init(is_fetch_tools=True) -> None`

Initialize the SSE connection to the MCP server with proper error handling and middleware setup.

**Process:**
1. Establishes SSE connection using provided URL and headers
2. Creates MCP ClientSession over SSE transport
3. Configures and applies client-side middlewares
4. Initializes MCP protocol handshake
5. Discovers available tools (if requested)

```python
await client.init()
# SSE connection established, tools discovered and registered
```

**Keep-Alive vs One-Shot:**

```python
# Persistent connection (default)
persistent_client = SSEMCPClient(is_keep_alive=True, sse_url=url)
await persistent_client.init()  # Connection maintained

# One-shot connections
oneshot_client = SSEMCPClient(is_keep_alive=False, sse_url=url) 
await oneshot_client.init()  # Tools discovered, connection closed
```

### `async call_tool(tool_name, arguments)`

Execute tool with one-shot SSE connection for non-persistent mode.

```python
# One-shot execution
response = await client.call_tool("stream_data", {
    "query": "real-time metrics",
    "duration": 60
})
```

## Configuration Examples

### Development Setup

```python
# Local development SSE server
dev_client = SSEMCPClient(
    name="dev_stream",
    sse_url="http://localhost:8080/sse",
    headers={
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache"
    }
)
```

### Production Configuration

```python
# Production SSE server with full configuration
prod_client = SSEMCPClient(
    name="production_stream",
    desc="Production real-time data server",
    sse_url="https://mcp-api.company.com/sse/v1",
    headers={
        "Authorization": f"Bearer {os.getenv('MCP_API_TOKEN')}",
        "User-Agent": "OxyGent/1.0",
        "Accept": "text/event-stream",
        "X-Client-Version": "1.0.0",
        "X-Request-ID": str(uuid.uuid4())
    },
    middlewares=[
        AuthenticationMiddleware(),
        RequestIdMiddleware(),
        MetricsMiddleware()
    ],
    is_keep_alive=True,  # Maintain connection for real-time updates
    timeout=300.0  # 5-minute timeout for long-running streams
)
```

### Multi-Environment Setup

```python
import os

def create_sse_client(environment: str) -> SSEMCPClient:
    """Create environment-specific SSE client."""
    
    configs = {
        "development": {
            "sse_url": "http://localhost:8080/sse",
            "headers": {"Accept": "text/event-stream"}
        },
        "staging": {
            "sse_url": "https://staging-mcp.example.com/sse",
            "headers": {
                "Authorization": f"Bearer {os.getenv('STAGING_TOKEN')}",
                "Accept": "text/event-stream"
            }
        },
        "production": {
            "sse_url": "https://mcp-api.company.com/sse",
            "headers": {
                "Authorization": f"Bearer {os.getenv('PROD_TOKEN')}",
                "Accept": "text/event-stream",
                "User-Agent": "OxyGent-Production/1.0"
            }
        }
    }
    
    config = configs[environment]
    return SSEMCPClient(
        name=f"sse_server_{environment}",
        **config
    )

# Usage
client = create_sse_client("production")
```

## Integration Examples

### Real-time Data Processing

```python
from oxygent.agents import ChatAgent

# Real-time market data agent
market_client = SSEMCPClient(
    name="market_stream",
    sse_url="https://market-data.example.com/sse",
    headers={"Authorization": f"Bearer {market_api_key}"}
)

# Agent for processing streaming market data
market_agent = ChatAgent(name="market_analyzer")
market_agent.add_oxy(market_client)

await market_agent.init()

# Agent can now use real-time market tools
response = await market_agent.execute(OxyRequest(
    callee="stream_stock_prices",
    arguments={
        "symbols": ["AAPL", "GOOGL", "MSFT"],
        "duration": 300  # 5 minutes of streaming
    }
))
```

### Live Dashboard Integration

```python
# Multiple SSE streams for dashboard
dashboard_clients = [
    SSEMCPClient(
        name="metrics_stream",
        sse_url="https://metrics.company.com/sse",
        headers={"Authorization": f"Bearer {metrics_token}"}
    ),
    SSEMCPClient(
        name="logs_stream", 
        sse_url="https://logs.company.com/sse",
        headers={"Authorization": f"Bearer {logs_token}"}
    ),
    SSEMCPClient(
        name="alerts_stream",
        sse_url="https://alerts.company.com/sse", 
        headers={"Authorization": f"Bearer {alerts_token}"}
    )
]

# Initialize all streams
for client in dashboard_clients:
    client.set_mas(mas)
    await client.init()

# Dashboard agent can access all real-time streams
dashboard_agent = ChatAgent(name="dashboard_manager")
for client in dashboard_clients:
    dashboard_agent.add_oxy(client)
```

### Event-Driven Workflows

```python
from oxygent.flows import WorkflowFlow

# Event-driven workflow using SSE streams
event_client = SSEMCPClient(
    name="event_stream",
    sse_url="https://events.company.com/sse"
)

# Workflow that responds to real-time events
workflow = WorkflowFlow(name="event_processor")
workflow.add_oxy(event_client)

# Workflow steps triggered by events
workflow_config = {
    "triggers": [
        {
            "event": "user_action",
            "tool": "process_user_event",
            "response_tool": "send_notification"
        },
        {
            "event": "system_alert",
            "tool": "analyze_system_health",
            "response_tool": "trigger_remediation"
        }
    ]
}
```

## Advanced Features

### Middleware Development

```python
class CustomSSEMiddleware:
    """Custom middleware for SSE request/response processing."""
    
    def __init__(self, config: dict):
        self.config = config
    
    async def __call__(self, request, call_next):
        # Pre-process request
        request.headers["X-Custom-Header"] = self.config.get("custom_value")
        
        # Execute request
        start_time = time.time()
        try:
            response = await call_next(request)
            # Post-process successful response
            response.metadata["processing_time"] = time.time() - start_time
            return response
        except Exception as e:
            # Handle errors
            logger.error(f"SSE middleware error: {e}")
            raise

# Usage
client = SSEMCPClient(
    name="custom_server",
    sse_url="https://mcp-server.example.com/sse",
    middlewares=[CustomSSEMiddleware({"custom_value": "oxygent-client"})]
)
```

### Connection Monitoring

```python
class MonitoredSSEClient(SSEMCPClient):
    """SSE client with connection monitoring."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection_stats = {
            "connect_time": None,
            "last_activity": None,
            "reconnect_count": 0,
            "message_count": 0
        }
    
    async def init(self, is_fetch_tools=True):
        """Initialize with connection monitoring."""
        try:
            self.connection_stats["connect_time"] = time.time()
            await super().init(is_fetch_tools)
            self.connection_stats["last_activity"] = time.time()
        except Exception as e:
            self.connection_stats["reconnect_count"] += 1
            raise
    
    async def _execute(self, oxy_request):
        """Execute with activity tracking."""
        response = await super()._execute(oxy_request)
        self.connection_stats["message_count"] += 1
        self.connection_stats["last_activity"] = time.time()
        return response
    
    def get_connection_health(self) -> dict:
        """Get connection health metrics."""
        current_time = time.time()
        return {
            "connected_duration": current_time - self.connection_stats["connect_time"] if self.connection_stats["connect_time"] else 0,
            "time_since_last_activity": current_time - self.connection_stats["last_activity"] if self.connection_stats["last_activity"] else None,
            "reconnect_count": self.connection_stats["reconnect_count"],
            "message_count": self.connection_stats["message_count"],
            "is_healthy": self._session is not None
        }
```

### Automatic Reconnection

```python
class ResilientSSEClient(SSEMCPClient):
    """SSE client with automatic reconnection."""
    
    def __init__(self, max_retries=5, retry_delay=1.0, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_count = 0
    
    async def init_with_retry(self, is_fetch_tools=True):
        """Initialize with automatic retry on failure."""
        while self.retry_count < self.max_retries:
            try:
                await self.init(is_fetch_tools)
                self.retry_count = 0  # Reset on success
                return
            except Exception as e:
                self.retry_count += 1
                if self.retry_count >= self.max_retries:
                    logger.error(f"Max retries ({self.max_retries}) exceeded for {self.name}")
                    raise
                
                delay = self.retry_delay * (2 ** (self.retry_count - 1))  # Exponential backoff
                logger.warning(f"SSE connection failed (attempt {self.retry_count}), retrying in {delay}s: {e}")
                await asyncio.sleep(delay)
    
    async def _execute(self, oxy_request):
        """Execute with automatic reconnection on failure."""
        try:
            return await super()._execute(oxy_request)
        except anyio.ClosedResourceError:
            logger.warning(f"SSE connection lost for {self.name}, attempting reconnection")
            await self.init_with_retry(is_fetch_tools=False)
            return await super()._execute(oxy_request)
```

## Performance Optimization

### Connection Pooling

```python
class PooledSSEClientManager:
    """Manager for pooled SSE connections."""
    
    def __init__(self, sse_url: str, pool_size: int = 3):
        self.sse_url = sse_url
        self.pool_size = pool_size
        self.pool = asyncio.Queue(maxsize=pool_size)
        self.created_clients = 0
    
    async def get_client(self) -> SSEMCPClient:
        """Get client from pool or create new one."""
        try:
            # Try to get existing client
            client = self.pool.get_nowait()
            return client
        except asyncio.QueueEmpty:
            # Create new client if pool not full
            if self.created_clients < self.pool_size:
                client = SSEMCPClient(
                    name=f"pooled_client_{self.created_clients}",
                    sse_url=self.sse_url,
                    is_keep_alive=True
                )
                await client.init(is_fetch_tools=False)
                self.created_clients += 1
                return client
            else:
                # Wait for available client
                return await self.pool.get()
    
    async def return_client(self, client: SSEMCPClient):
        """Return client to pool."""
        await self.pool.put(client)
    
    async def cleanup(self):
        """Cleanup all pooled clients."""
        while not self.pool.empty():
            client = await self.pool.get()
            await client.cleanup()
```

### Caching for Frequent Requests

```python
import hashlib
import json

class CachedSSEClient(SSEMCPClient):
    """SSE client with response caching."""
    
    def __init__(self, cache_ttl=60, **kwargs):
        super().__init__(**kwargs)
        self.cache_ttl = cache_ttl
        self.cache = {}
    
    def _get_cache_key(self, tool_name: str, arguments: dict) -> str:
        """Generate cache key for request."""
        content = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def _execute(self, oxy_request):
        """Execute with caching for non-streaming requests."""
        cache_key = self._get_cache_key(oxy_request.callee, oxy_request.arguments)
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_response = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                logger.debug(f"Cache hit for {oxy_request.callee}")
                return cached_response
        
        # Execute and cache
        response = await super()._execute(oxy_request)
        
        # Only cache successful, non-streaming responses
        if response.state == OxyState.COMPLETED and not self._is_streaming_response(response):
            self.cache[cache_key] = (time.time(), response)
        
        return response
    
    def _is_streaming_response(self, response) -> bool:
        """Check if response indicates streaming data."""
        # Implement logic to detect streaming responses
        return False
```

## Security Considerations

### Secure Headers Configuration

```python
# Production security headers
secure_headers = {
    "Authorization": f"Bearer {os.getenv('SSE_API_TOKEN')}",
    "User-Agent": "OxyGent/1.0",
    "Accept": "text/event-stream",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://your-domain.com",  # CORS origin
    "Referer": "https://your-domain.com/dashboard"
}

secure_client = SSEMCPClient(
    name="secure_sse",
    sse_url="https://secure-sse.example.com/stream",
    headers=secure_headers
)
```

### Token Refresh Middleware

```python
class TokenRefreshMiddleware:
    """Middleware for automatic token refresh."""
    
    def __init__(self, token_provider):
        self.token_provider = token_provider
        self.last_refresh = 0
        self.refresh_interval = 3600  # 1 hour
    
    async def __call__(self, request, call_next):
        # Refresh token if needed
        if time.time() - self.last_refresh > self.refresh_interval:
            new_token = await self.token_provider.get_fresh_token()
            request.headers["Authorization"] = f"Bearer {new_token}"
            self.last_refresh = time.time()
        
        return await call_next(request)

# Usage
class TokenProvider:
    async def get_fresh_token(self):
        # Implement token refresh logic
        return await refresh_api_token()

client = SSEMCPClient(
    name="auto_refresh_client",
    sse_url="https://api.example.com/sse",
    middlewares=[TokenRefreshMiddleware(TokenProvider())]
)
```

## Error Handling

### Comprehensive Error Management

```python
async def robust_sse_execution(client, request):
    """Robust SSE execution with comprehensive error handling."""
    try:
        return await client._execute(request)
    
    except anyio.ClosedResourceError:
        # SSE connection closed
        logger.warning("SSE connection closed, attempting reconnection")
        await client.init(is_fetch_tools=False)
        return await client._execute(request)
    
    except httpx.HTTPError as e:
        # HTTP-related errors
        if e.response.status_code == 401:
            logger.error("SSE authentication failed")
            # Implement token refresh logic
            return OxyResponse(state=OxyState.FAILED, output="Authentication failed")
        elif e.response.status_code == 503:
            logger.error("SSE service unavailable")
            return OxyResponse(state=OxyState.FAILED, output="Service temporarily unavailable")
        else:
            logger.error(f"SSE HTTP error: {e}")
            return OxyResponse(state=OxyState.FAILED, output=f"HTTP error: {e}")
    
    except asyncio.TimeoutError:
        # Timeout handling
        logger.error("SSE request timeout")
        return OxyResponse(state=OxyState.FAILED, output="Request timeout")
    
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected SSE error: {e}")
        return OxyResponse(state=OxyState.FAILED, output=f"Execution error: {str(e)}")
```

### Health Monitoring

```python
class HealthMonitoredSSEClient(SSEMCPClient):
    """SSE client with health monitoring."""
    
    async def health_check(self) -> dict:
        """Comprehensive health check."""
        health_status = {
            "connection_status": "unknown",
            "last_successful_request": None,
            "error_count": 0,
            "uptime": 0
        }
        
        try:
            # Test connection with lightweight request
            if self._session:
                await self._session.list_tools()
                health_status["connection_status"] = "healthy"
            else:
                health_status["connection_status"] = "disconnected"
                
        except Exception as e:
            health_status["connection_status"] = "error"
            health_status["last_error"] = str(e)
        
        return health_status
    
    async def periodic_health_check(self, interval=60):
        """Run periodic health checks."""
        while True:
            health = await self.health_check()
            if health["connection_status"] != "healthy":
                logger.warning(f"SSE client {self.name} health check failed: {health}")
                # Implement recovery logic
                try:
                    await self.cleanup()
                    await self.init(is_fetch_tools=False)
                except Exception as e:
                    logger.error(f"Failed to recover SSE client {self.name}: {e}")
            
            await asyncio.sleep(interval)
```

## Best Practices

### Configuration Management

```python
# ✅ Good: Environment-based configuration
class SSEConfig:
    """SSE client configuration management."""
    
    @classmethod
    def from_environment(cls, env_prefix="SSE_"):
        """Create configuration from environment variables."""
        return {
            "sse_url": os.getenv(f"{env_prefix}URL"),
            "headers": {
                "Authorization": f"Bearer {os.getenv(f'{env_prefix}TOKEN')}",
                "User-Agent": os.getenv(f"{env_prefix}USER_AGENT", "OxyGent/1.0")
            },
            "timeout": float(os.getenv(f"{env_prefix}TIMEOUT", "60.0")),
            "is_keep_alive": os.getenv(f"{env_prefix}KEEP_ALIVE", "true").lower() == "true"
        }

# Usage
client = SSEMCPClient(
    name="env_configured_client",
    **SSEConfig.from_environment("MARKET_DATA_")
)
```

### Resource Management

```python
# ✅ Good: Proper cleanup with context manager
class SSEClientManager:
    """Context manager for SSE client lifecycle."""
    
    def __init__(self, **client_kwargs):
        self.client_kwargs = client_kwargs
        self.client = None
    
    async def __aenter__(self):
        self.client = SSEMCPClient(**self.client_kwargs)
        await self.client.init()
        return self.client
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.cleanup()

# Usage
async with SSEClientManager(
    name="managed_client",
    sse_url="https://api.example.com/sse"
) as client:
    response = await client._execute(request)
    # Automatic cleanup on exit
```

## API Reference

### Complete Class Definition

```python
class SSEMCPClient(BaseMCPClient):
    """MCP client implementation using Server-Sent Events transport."""
    
    sse_url: AnyUrl = Field("")
    headers: Dict[str, str] = Field(default_factory=dict, description="Extra HTTP headers")
    middlewares: List[Any] = Field(default_factory=list, description="Client-side MCP middlewares")
    
    async def init(self, is_fetch_tools=True) -> None:
        """Initialize SSE connection to MCP server."""
        
    async def call_tool(self, tool_name, arguments):
        """Execute tool with one-shot SSE connection."""
```

### Configuration Schema

```python
{
    "sse_url": "https://server.com/sse",     # SSE endpoint URL
    "headers": {                             # HTTP headers
        "Authorization": "Bearer token",
        "Accept": "text/event-stream"
    },
    "middlewares": [middleware_instance],    # Middleware list
    "is_keep_alive": True,                   # Connection persistence
    "timeout": 60.0                          # Request timeout
}
```

## See Also

- [BaseMCPClient](./base-mcp-client) - Base MCP client functionality
- [StdioMCPClient](./stdio-mcp-client) - Standard I/O transport
- [StreamableMCPClient](./streamable-mcp-client) - Streamable HTTP transport
- [MCPTool](./mcp-tool) - Individual MCP tool proxy
---
title: BaseMCPClient
description: Abstract base class for Model Context Protocol (MCP) client implementations in OxyGent
---

# BaseMCPClient

The `BaseMCPClient` class provides the foundational implementation for communicating with MCP servers. It handles server lifecycle management, tool discovery, dynamic tool registration, and tool execution through the Model Context Protocol standard.

## Class Overview

```python
from oxygent.oxy.mcp_tools import BaseMCPClient
from oxygent.oxy.base_tool import BaseTool

class BaseMCPClient(BaseTool):
    """Base client for Model Context Protocol (MCP) servers."""
```

### Inheritance Hierarchy
```
BaseMCPClient → BaseTool → Oxy
```

## Core Attributes

### `included_tool_name_list: list`
List of tool names discovered from the MCP server during initialization.

```python
client = StdioMCPClient(name="test_server", params=params)
await client.init()

print(client.included_tool_name_list)
# Output: ['read_file', 'write_file', 'list_directory', 'create_directory']
```

### `is_keep_alive: bool`
Controls connection persistence behavior. Defaults to configuration value `Config.get_tool_mcp_is_keep_alive()`.

- `True`: Maintains persistent connection for better performance
- `False`: Creates new connection for each tool execution

```python
# Persistent connection for frequent operations
persistent_client = BaseMCPClient(is_keep_alive=True)

# One-shot connection for occasional use
occasional_client = BaseMCPClient(is_keep_alive=False)
```

## Private Attributes

### Connection Management
- `_session: ClientSession`: Active MCP client session
- `_cleanup_lock: asyncio.Lock`: Prevents concurrent cleanup operations
- `_exit_stack: AsyncExitStack`: Manages resource lifecycle
- `_stdio_context: Any`: Context for stdio-based connections

## Core Methods

### `async list_tools() -> None`

Discover and register tools from the MCP server.

**Process:**
1. Validates that server session is initialized
2. Sends `list_tools` request to MCP server
3. Processes response and registers discovered tools

```python
client = StdioMCPClient(name="filesystem", params=fs_params)
await client.init()  # Initializes connection
await client.list_tools()  # Discovers and registers tools

# Tools are now available in client.included_tool_name_list
print(f"Available tools: {client.included_tool_name_list}")
```

**Implementation Details:**
```python
async def list_tools(self) -> None:
    if not self._session:
        raise RuntimeError(f"Server {self.name} not initialized")
    
    tools_response = await self._session.list_tools()
    self.add_tools(tools_response)
```

### `add_tools(tools_response) -> None`

Process tool discovery response and create MCPTool instances.

**Process:**
1. Extracts common parameters from client configuration
2. Iterates through discovered tools in response
3. Creates `MCPTool` instances for each tool
4. Registers tools with the Multi-Agent System (MAS)

```python
# tools_response format from MCP server:
# [
#   ("tools", [
#     Tool(name="read_file", description="Read file contents", inputSchema={...}),
#     Tool(name="write_file", description="Write to file", inputSchema={...})
#   ])
# ]

client.add_tools(tools_response)
# Creates MCPTool instances and registers with MAS
```

**Implementation Details:**
```python
def add_tools(self, tools_response) -> None:
    # Extract parameters excluding client-specific fields
    params = self.model_dump(exclude={
        "sse_url", "server_url", "headers", "middlewares",
        "included_tool_name_list", "name", "desc", "mcp_client", 
        "server_name", "input_schema"
    })
    
    for item in tools_response:
        if isinstance(item, tuple) and item[0] == "tools":
            for tool in item[1]:
                # Track discovered tool names
                self.included_tool_name_list.append(tool.name)
                
                # Create MCPTool proxy
                mcp_tool = MCPTool(
                    name=tool.name,
                    desc=tool.description,
                    mcp_client=self,
                    server_name=self.name,
                    input_schema=tool.inputSchema,
                    **params
                )
                
                # Register with MAS
                mcp_tool.set_mas(self.mas)
                self.mas.add_oxy(mcp_tool)
```

### `async _execute(oxy_request: OxyRequest) -> OxyResponse`

Execute a tool call through the MCP server.

**Parameters:**
- `oxy_request`: Request containing tool name and arguments

**Returns:**
- `OxyResponse`: Response with execution results or error information

**Process:**
1. Extracts tool name from request
2. Handles persistent vs. one-shot connection modes
3. Sends tool execution request to MCP server
4. Processes response and returns formatted result

```python
request = OxyRequest(
    callee="read_file",
    arguments={"path": "/tmp/example.txt"}
)

response = await client._execute(request)
if response.state == OxyState.COMPLETED:
    print(f"File contents: {response.output}")
```

**Implementation Details:**
```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    tool_name = oxy_request.callee
    
    if self.is_keep_alive:
        # Use persistent connection
        if not self._session:
            raise RuntimeError(f"Server {self.name} not initialized")
        
        try:
            mcp_response = await self._session.call_tool(
                tool_name, oxy_request.arguments
            )
        except anyio.ClosedResourceError:
            # Reconnect and retry
            await self.init(is_fetch_tools=False)
            mcp_response = await self._session.call_tool(
                tool_name, oxy_request.arguments
            )
    else:
        # Create one-shot connection
        mcp_response = await self.call_tool(tool_name, oxy_request.arguments)
    
    # Process response content
    results = [content.text.strip() for content in mcp_response.content]
    return OxyResponse(
        state=OxyState.COMPLETED,
        output=results[0] if len(results) == 1 else results
    )
```

### `async cleanup() -> None`

Clean up MCP server resources and connections.

**Features:**
- Thread-safe cleanup with async lock
- Graceful handling of cancellation and exceptions
- Comprehensive resource disposal

```python
try:
    # Use MCP client
    await client.init()
    # ... perform operations
finally:
    # Always cleanup resources
    await client.cleanup()
```

**Implementation Details:**
```python
async def cleanup(self) -> None:
    async with self._cleanup_lock:
        try:
            await self._exit_stack.aclose()
        except asyncio.CancelledError:
            logger.error("cleanup(): Operation was cancelled")
        except Exception:
            # Suppress cleanup exceptions to prevent cascading failures
            pass
        finally:
            self._session = None
            self._stdio_context = None
```

## Usage Patterns

### Basic Implementation Pattern

```python
class CustomMCPClient(BaseMCPClient):
    """Custom MCP client implementation."""
    
    async def init(self, is_fetch_tools=True) -> None:
        """Initialize connection to MCP server."""
        # 1. Establish connection (transport-specific)
        # 2. Create ClientSession
        # 3. Initialize MCP protocol
        # 4. Discover tools (if requested)
        pass
    
    async def call_tool(self, tool_name, arguments):
        """Execute tool with one-shot connection."""
        # Implementation for non-persistent connections
        pass
```

### Connection Lifecycle Management

```python
# Proper lifecycle management
async def use_mcp_client():
    client = None
    try:
        # Initialize
        client = CustomMCPClient(name="example", is_keep_alive=True)
        await client.init()
        
        # Use tools
        response = await client._execute(OxyRequest(
            callee="example_tool",
            arguments={"param": "value"}
        ))
        
        return response
    finally:
        # Always cleanup
        if client:
            await client.cleanup()
```

### Error Handling Patterns

```python
class RobustMCPClient(BaseMCPClient):
    async def init(self, is_fetch_tools=True) -> None:
        try:
            # Connection establishment logic
            await self.establish_connection()
            
            if is_fetch_tools:
                await self.list_tools()
                
        except ConnectionError as e:
            logger.error(f"Failed to connect to {self.name}: {e}")
            await self.cleanup()
            raise Exception(f"Server {self.name} connection error")
        except Exception as e:
            logger.error(f"Unexpected error initializing {self.name}: {e}")
            await self.cleanup()
            raise Exception(f"Server {self.name} initialization error")
```

## Configuration Examples

### Keep-Alive Configuration

```python
# High-frequency usage - persistent connection
frequent_client = BaseMCPClient(
    name="frequent_server",
    desc="Frequently used MCP server",
    is_keep_alive=True,  # Maintain connection
    timeout=30.0  # Shorter timeout for responsive operations
)

# Occasional usage - one-shot connections  
occasional_client = BaseMCPClient(
    name="occasional_server", 
    desc="Occasionally used MCP server",
    is_keep_alive=False,  # Create connection per request
    timeout=120.0  # Longer timeout for complex operations
)
```

### Permission Control

```python
# Secure operations requiring permission
secure_client = BaseMCPClient(
    name="secure_operations",
    desc="Sensitive MCP operations", 
    is_permission_required=True  # Require explicit permission
)
```

## Integration Examples

### With Multi-Agent System

```python
from oxygent.mas import MAS

# Setup MAS and MCP client
mas = MAS()
client = CustomMCPClient(name="tools_server")

# Register and initialize
client.set_mas(mas)
await client.init()

# Tools are automatically registered with MAS
available_tools = [oxy.name for oxy in mas.oxys if isinstance(oxy, MCPTool)]
print(f"MCP tools registered: {available_tools}")
```

### With Agents

```python
from oxygent.agents import ChatAgent

# Create agent with MCP tools
agent = ChatAgent(name="mcp_agent")
agent.add_oxy(client)

# Agent can now use MCP tools
response = await agent.execute(OxyRequest(
    callee="mcp_discovered_tool",
    arguments={"input": "data"}
))
```

### Multi-Server Setup

```python
async def setup_multi_server_environment():
    servers = [
        StdioMCPClient(name="filesystem", params=fs_params),
        SSEMCPClient(name="realtime", sse_url="https://sse.example.com"),
        StreamableMCPClient(name="http", server_url="https://http.example.com")
    ]
    
    # Initialize all servers
    for server in servers:
        server.set_mas(mas)
        await server.init()
    
    # All tools from all servers are now available
    total_tools = sum(len(server.included_tool_name_list) for server in servers)
    print(f"Total tools available: {total_tools}")
```

## Advanced Features

### Automatic Reconnection

```python
async def _execute_with_retry(self, oxy_request: OxyRequest) -> OxyResponse:
    """Execute with automatic reconnection on connection loss."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            return await self._execute(oxy_request)
        except anyio.ClosedResourceError:
            if attempt < max_retries - 1:
                logger.warning(f"Connection lost, retrying {attempt + 1}/{max_retries}")
                await self.init(is_fetch_tools=False)
            else:
                raise
```

### Tool Filtering

```python
class FilteredMCPClient(BaseMCPClient):
    def __init__(self, tool_filter=None, **kwargs):
        super().__init__(**kwargs)
        self.tool_filter = tool_filter or []
    
    def add_tools(self, tools_response):
        """Only register tools matching filter criteria."""
        # Filter tools before registration
        if self.tool_filter:
            original_response = tools_response
            filtered_tools = []
            
            for item in original_response:
                if isinstance(item, tuple) and item[0] == "tools":
                    tools = [t for t in item[1] if t.name in self.tool_filter]
                    if tools:
                        filtered_tools.append(("tools", tools))
            
            super().add_tools(filtered_tools)
        else:
            super().add_tools(tools_response)

# Usage
filtered_client = FilteredMCPClient(
    name="filtered_server",
    tool_filter=["read_file", "write_file"]  # Only allow these tools
)
```

### Custom Tool Processing

```python
class ProcessingMCPClient(BaseMCPClient):
    def add_tools(self, tools_response):
        """Add custom processing before tool registration."""
        # Process tools before registration
        processed_response = []
        
        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                processed_tools = []
                for tool in item[1]:
                    # Add custom description prefix
                    tool.description = f"[MCP] {tool.description}"
                    processed_tools.append(tool)
                processed_response.append(("tools", processed_tools))
        
        super().add_tools(processed_response)
```

## Performance Optimization

### Connection Pooling

```python
class PooledMCPClient(BaseMCPClient):
    """MCP client with connection pooling for high-load scenarios."""
    
    def __init__(self, pool_size=5, **kwargs):
        super().__init__(**kwargs)
        self.pool_size = pool_size
        self.connection_pool = asyncio.Queue(maxsize=pool_size)
    
    async def init(self, is_fetch_tools=True):
        """Initialize connection pool."""
        for _ in range(self.pool_size):
            connection = await self.create_connection()
            await self.connection_pool.put(connection)
        
        if is_fetch_tools:
            # Use one connection for tool discovery
            connection = await self.connection_pool.get()
            try:
                await self.discover_tools_with_connection(connection)
            finally:
                await self.connection_pool.put(connection)
```

### Caching

```python
from functools import lru_cache
import json

class CachedMCPClient(BaseMCPClient):
    """MCP client with response caching."""
    
    def __init__(self, cache_ttl=300, **kwargs):
        super().__init__(**kwargs)
        self.cache_ttl = cache_ttl
        self.cache = {}
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Create cache key
        cache_key = f"{oxy_request.callee}:{json.dumps(oxy_request.arguments, sort_keys=True)}"
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_response = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_response
        
        # Execute and cache
        response = await super()._execute(oxy_request)
        self.cache[cache_key] = (time.time(), response)
        
        return response
```

## Error Handling

### Common Error Scenarios

```python
async def robust_mcp_execution(client, request):
    """Robust MCP tool execution with comprehensive error handling."""
    try:
        return await client._execute(request)
    
    except RuntimeError as e:
        if "not initialized" in str(e):
            # Server not initialized
            logger.error(f"MCP server {client.name} not initialized")
            await client.init()
            return await client._execute(request)
        else:
            raise
    
    except anyio.ClosedResourceError:
        # Connection closed unexpectedly
        logger.warning(f"Connection to {client.name} closed, reconnecting...")
        await client.init(is_fetch_tools=False)
        return await client._execute(request)
    
    except TimeoutError:
        # Operation timeout
        logger.error(f"Timeout executing {request.callee} on {client.name}")
        return OxyResponse(
            state=OxyState.FAILED,
            output=f"Timeout executing {request.callee}"
        )
    
    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected error in MCP execution: {e}")
        return OxyResponse(
            state=OxyState.FAILED,
            output=f"Execution error: {str(e)}"
        )
```

### Health Checking

```python
class HealthCheckedMCPClient(BaseMCPClient):
    """MCP client with health checking capabilities."""
    
    async def health_check(self) -> bool:
        """Check if MCP server is healthy and responsive."""
        try:
            if not self._session:
                return False
            
            # Try to list tools as health check
            await self._session.list_tools()
            return True
        except Exception as e:
            logger.warning(f"Health check failed for {self.name}: {e}")
            return False
    
    async def ensure_healthy(self):
        """Ensure client is healthy, reconnect if necessary."""
        if not await self.health_check():
            logger.info(f"Reconnecting unhealthy client {self.name}")
            await self.cleanup()
            await self.init(is_fetch_tools=False)
```

## Best Practices

### Resource Management

```python
# ✅ Good: Proper resource management
async def good_usage():
    client = CustomMCPClient(name="example")
    try:
        await client.init()
        response = await client._execute(request)
        return response
    finally:
        await client.cleanup()

# ❌ Bad: No cleanup
async def bad_usage():
    client = CustomMCPClient(name="example") 
    await client.init()
    return await client._execute(request)  # Resources not cleaned up
```

### Error Handling

```python
# ✅ Good: Comprehensive error handling
async def robust_init(client):
    try:
        await client.init()
    except Exception as e:
        logger.error(f"Failed to initialize {client.name}: {e}")
        await client.cleanup()  # Cleanup even on failure
        raise

# ❌ Bad: No error handling
async def fragile_init(client):
    await client.init()  # May fail without cleanup
```

### Connection Strategy

```python
# ✅ Good: Choose appropriate connection strategy
high_frequency_client = BaseMCPClient(is_keep_alive=True)  # Frequent use
low_frequency_client = BaseMCPClient(is_keep_alive=False)   # Occasional use

# ❌ Bad: Always keeping connections alive
all_clients_persistent = BaseMCPClient(is_keep_alive=True)  # Wastes resources
```

## Troubleshooting

### Connection Issues

```python
# Debug connection problems
import logging

# Enable detailed logging
logging.getLogger("oxygent.oxy.mcp_tools").setLevel(logging.DEBUG)

# Test connection
try:
    await client.init()
    logger.info(f"Successfully connected to {client.name}")
    logger.info(f"Discovered tools: {client.included_tool_name_list}")
except Exception as e:
    logger.error(f"Connection failed: {e}")
```

### Tool Discovery Problems

```python
# Verify tool discovery
client = CustomMCPClient(name="test")
await client.init()

if not client.included_tool_name_list:
    logger.warning("No tools discovered - check MCP server implementation")
else:
    logger.info(f"Tools available: {client.included_tool_name_list}")
    
    # Test tool execution
    for tool_name in client.included_tool_name_list:
        try:
            # Try with minimal arguments
            response = await client._execute(OxyRequest(
                callee=tool_name,
                arguments={}
            ))
            logger.info(f"Tool {tool_name} is accessible")
        except Exception as e:
            logger.warning(f"Tool {tool_name} failed: {e}")
```

## API Reference

### Complete Class Definition

```python
class BaseMCPClient(BaseTool):
    """Base client for Model Context Protocol (MCP) servers."""
    
    included_tool_name_list: list = Field(default_factory=list)
    is_keep_alive: bool = Field(default_factory=Config.get_tool_mcp_is_keep_alive)
    
    def __init__(self, **kwargs):
        """Initialize MCP client with resource management."""
        
    async def list_tools(self) -> None:
        """Discover and register tools from MCP server."""
        
    def add_tools(self, tools_response) -> None:
        """Process tool discovery response and create MCPTool instances."""
        
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute tool call through MCP server."""
        
    async def cleanup(self) -> None:
        """Clean up MCP server resources and connections."""
```

### Abstract Methods (to be implemented by subclasses)
- `async def init(self, is_fetch_tools=True) -> None`
- `async def call_tool(self, tool_name, arguments)` (for non-persistent connections)

### Inherited Properties

From `BaseTool`:
- `is_permission_required: bool = True`
- `category: str = "tool"`
- `timeout: float = 60`

From `Oxy`:
- `name: str`
- `desc: str`
- `mas: Optional[MAS] = None`

## See Also

- [StdioMCPClient](./stdio-mcp-client) - Standard I/O transport implementation
- [SSEMCPClient](./sse-mcp-client) - Server-Sent Events transport implementation
- [StreamableMCPClient](./streamable-mcp-client) - Streamable HTTP transport implementation
- [MCPTool](./mcp-tool) - Individual tool proxy for MCP server tools
---
title: StdioMCPClient
description: Standard I/O MCP client for local process communication in OxyGent
---

# StdioMCPClient

The `StdioMCPClient` implements MCP communication over standard input/output streams. This transport method is ideal for local process communication, allowing MCP servers to run as separate processes that communicate through stdin/stdout pipes.

## Class Overview

```python
from oxygent.oxy.mcp_tools import StdioMCPClient
from oxygent.oxy.mcp_tools.base_mcp_client import BaseMCPClient

class StdioMCPClient(BaseMCPClient):
    """MCP client implementation using standard I/O transport."""
```

## Core Attributes

### `params: dict[str, Any]`
Configuration parameters for the MCP server process, including command, arguments, and environment variables.

**Structure:**
```python
{
    "command": "npx",  # Command to execute
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],  # Command arguments
    "env": {"NODE_ENV": "production"}  # Environment variables
}
```

## Key Features

- **Process Management**: Spawns and manages external MCP server processes
- **Directory Validation**: Ensures required directories exist before server startup
- **Environment Control**: Full control over environment variables
- **NPX Integration**: Special handling for npm/npx-based MCP servers
- **File System Validation**: Validates file paths for directory-based operations

## Quick Start

### Basic Filesystem Server

```python
from oxygent.oxy.mcp_tools import StdioMCPClient

# Configure filesystem MCP server
fs_client = StdioMCPClient(
    name="filesystem",
    desc="File system operations",
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
        "env": {}
    }
)

# Initialize and discover tools
await fs_client.init()
# Discovers: read_file, write_file, list_directory, create_directory, etc.
```

### Custom Node.js Server

```python
# Custom MCP server
custom_client = StdioMCPClient(
    name="custom_server",
    desc="Custom MCP server functionality",
    params={
        "command": "node",
        "args": ["./custom-mcp-server.js"],
        "env": {
            "NODE_ENV": "production",
            "LOG_LEVEL": "info",
            "API_KEY": os.getenv("API_KEY")
        }
    }
)

await custom_client.init()
```

## Methods

### `async init(is_fetch_tools=True) -> None`

Initialize the stdio connection to the MCP server process with comprehensive validation.

**Validation Steps:**
1. Resolves command path (with special handling for 'npx')
2. Validates required files exist for directory-based commands
3. Creates necessary directories if they don't exist
4. Sets up environment variables
5. Establishes stdio transport and session

```python
await client.init()
# Process spawned, tools discovered, and registered with MAS
```

### `async call_tool(tool_name, arguments)`

Execute tool with one-shot connection for non-persistent mode.

```python
# One-shot execution (when is_keep_alive=False)
response = await client.call_tool("read_file", {"path": "/tmp/test.txt"})
```

### `async get_server_params()`

Generate `StdioServerParameters` for MCP server initialization.

**Process:**
1. Resolves command path (handles npx specially)
2. Validates command exists and is executable
3. Performs directory validation for filesystem servers
4. Sets up environment variables

```python
server_params = await client.get_server_params()
# Returns StdioServerParameters with resolved command, args, and environment
```

### `async _ensure_directories_exist(args: list[str]) -> None`

Ensure required directories exist before starting MCP server.

**Special Cases:**
- **Filesystem Server**: Creates target directory if it doesn't exist
- **Directory-based Commands**: Validates MCP tool files exist

```python
# For filesystem server with /workspace target
args = ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
await client._ensure_directories_exist(args)
# Creates /workspace directory if it doesn't exist
```

## Configuration Examples

### NPX-based Servers

```python
# Official MCP filesystem server
filesystem_config = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/workspace"],
    "env": {}
}

# MCP memory server
memory_config = {
    "command": "npx", 
    "args": ["-y", "@modelcontextprotocol/server-memory"],
    "env": {"MEMORY_SIZE": "1000"}
}

# MCP GitHub server
github_config = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")}
}
```

### Local Node.js Servers

```python
# Local development server
local_config = {
    "command": "node",
    "args": ["./servers/my-mcp-server.js"],
    "env": {
        "NODE_ENV": "development",
        "DEBUG": "mcp:*",
        "PORT": "8080"
    }
}

# Production server with PM2
production_config = {
    "command": "node",
    "args": ["./dist/server.js"],
    "env": {
        "NODE_ENV": "production",
        "LOG_LEVEL": "error",
        "DATABASE_URL": os.getenv("DATABASE_URL")
    }
}
```

### Directory-based Execution

```python
# Execute MCP server from specific directory
directory_config = {
    "command": "npx",
    "args": ["--directory", "/path/to/mcp/server", "run", "start:mcp"],
    "env": {"NODE_ENV": "production"}
}
```

### Python-based MCP Servers

```python
# Python MCP server
python_config = {
    "command": "python",
    "args": ["-m", "my_mcp_server"],
    "env": {
        "PYTHONPATH": "/path/to/server",
        "MCP_CONFIG": "/path/to/config.json"
    }
}

# Uvicorn-based MCP server
uvicorn_config = {
    "command": "uvicorn",
    "args": ["mcp_server:app", "--host", "127.0.0.1", "--port", "8000"],
    "env": {"UVICORN_LOG_LEVEL": "info"}
}
```

## Integration Examples

### With Multi-Agent System

```python
from oxygent.mas import MAS

# Setup multiple stdio-based MCP servers
mas = MAS()

servers = [
    StdioMCPClient(
        name="filesystem",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
        }
    ),
    StdioMCPClient(
        name="memory",
        params={
            "command": "npx", 
            "args": ["-y", "@modelcontextprotocol/server-memory"]
        }
    ),
    StdioMCPClient(
        name="custom_tools",
        params={
            "command": "node",
            "args": ["./custom-server.js"],
            "env": {"API_KEY": os.getenv("API_KEY")}
        }
    )
]

# Initialize all servers
for server in servers:
    server.set_mas(mas)
    await server.init()

print(f"Total tools available: {sum(len(s.included_tool_name_list) for s in servers)}")
```

### With Workflow Integration

```python
from oxygent.flows import WorkflowFlow

# Create workflow using stdio MCP tools
workflow = WorkflowFlow(name="file_processing_workflow")
workflow.add_oxy(fs_client)

# Define workflow steps using MCP tools
steps = [
    {
        "name": "list_files",
        "tool": "list_directory", 
        "arguments": {"path": "/input"}
    },
    {
        "name": "process_files",
        "tool": "read_file",
        "arguments": {"path": "{list_files.output[0]}"}
    },
    {
        "name": "save_result",
        "tool": "write_file",
        "arguments": {
            "path": "/output/result.txt",
            "content": "{process_files.output}"
        }
    }
]
```

## Performance Optimization

### Keep-Alive vs One-Shot

```python
# High-frequency usage - keep persistent connection
frequent_client = StdioMCPClient(
    name="frequent_fs",
    is_keep_alive=True,  # Maintain process and connection
    params=fs_params
)

# Occasional usage - spawn process per request
occasional_client = StdioMCPClient(
    name="occasional_fs",
    is_keep_alive=False,  # Spawn process for each execution
    params=fs_params
)
```

### Resource Management

```python
# Proper resource cleanup
class ManagedStdioClient:
    def __init__(self, **params):
        self.client = StdioMCPClient(**params)
    
    async def __aenter__(self):
        await self.client.init()
        return self.client
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.cleanup()

# Usage
async with ManagedStdioClient(name="fs", params=fs_params) as client:
    response = await client._execute(request)
    # Automatic cleanup on exit
```

## Error Handling

### Common Error Scenarios

```python
async def robust_stdio_init(client):
    """Robust initialization with comprehensive error handling."""
    try:
        await client.init()
    except FileNotFoundError as e:
        # Command or file not found
        if "does not exist" in str(e):
            logger.error(f"MCP server file missing: {e}")
        else:
            logger.error(f"Command not found: {e}")
        raise
    except ValueError as e:
        # Invalid command configuration
        logger.error(f"Invalid configuration: {e}")
        raise
    except Exception as e:
        # Server initialization failed
        logger.error(f"Server {client.name} failed to start: {e}")
        await client.cleanup()
        raise Exception(f"Server {client.name} error")
```

### Process Management

```python
import psutil

class MonitoredStdioClient(StdioMCPClient):
    """Stdio client with process monitoring."""
    
    async def init(self, is_fetch_tools=True):
        await super().init(is_fetch_tools)
        self.process_info = self.get_process_info()
    
    def get_process_info(self):
        """Get information about the spawned MCP server process."""
        # Implementation depends on access to process handle
        return {"pid": None, "memory": 0, "cpu": 0}
    
    async def health_check(self):
        """Check if MCP server process is still running."""
        try:
            # Check if process is alive and responsive
            await self._session.list_tools()
            return True
        except Exception:
            return False
```

## Security Considerations

### Environment Variables

```python
# ✅ Secure: Use environment variables for secrets
secure_config = {
    "command": "node",
    "args": ["secure-server.js"],
    "env": {
        "NODE_ENV": "production",
        "API_KEY": os.getenv("API_KEY"),  # From environment
        "DATABASE_URL": os.getenv("DATABASE_URL")  # From environment
    }
}

# ❌ Insecure: Hardcoded secrets
insecure_config = {
    "command": "node",
    "args": ["server.js"],
    "env": {
        "API_KEY": "secret-key-123",  # Exposed in code
        "DATABASE_URL": "postgresql://user:pass@host/db"  # Credentials exposed
    }
}
```

### Command Validation

```python
class SecureStdioClient(StdioMCPClient):
    """Stdio client with command validation."""
    
    ALLOWED_COMMANDS = ["node", "python", "npx"]
    
    async def get_server_params(self):
        """Validate command before execution."""
        params = await super().get_server_params()
        
        # Validate command is in allowed list
        command_name = os.path.basename(params.command)
        if command_name not in self.ALLOWED_COMMANDS:
            raise SecurityError(f"Command {command_name} not allowed")
        
        # Validate arguments don't contain dangerous patterns
        for arg in params.args:
            if any(dangerous in arg for dangerous in ["../", "$(", "`"]):
                raise SecurityError(f"Dangerous argument pattern: {arg}")
        
        return params
```

### File Path Validation

```python
def validate_workspace_path(path: str, allowed_base: str = "/workspace") -> bool:
    """Validate that file paths are within allowed workspace."""
    real_path = os.path.realpath(path)
    real_base = os.path.realpath(allowed_base)
    return real_path.startswith(real_base)

# Usage in filesystem server configuration
safe_fs_config = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/safe/workspace"],
    "env": {}
}
```

## Advanced Features

### Dynamic Configuration

```python
class ConfigurableStdioClient(StdioMCPClient):
    """Stdio client with dynamic configuration updates."""
    
    async def update_environment(self, new_env: dict):
        """Update environment variables for MCP server."""
        self.params["env"].update(new_env)
        
        # Restart if currently running with keep-alive
        if self.is_keep_alive and self._session:
            await self.cleanup()
            await self.init(is_fetch_tools=False)
    
    async def restart_server(self):
        """Restart MCP server with current configuration."""
        await self.cleanup()
        await self.init()
```

### Multi-Server Management

```python
class StdioServerManager:
    """Manager for multiple stdio-based MCP servers."""
    
    def __init__(self):
        self.servers = {}
    
    async def add_server(self, name: str, params: dict) -> StdioMCPClient:
        """Add and initialize new MCP server."""
        client = StdioMCPClient(name=name, params=params)
        await client.init()
        self.servers[name] = client
        return client
    
    async def remove_server(self, name: str):
        """Remove and cleanup MCP server."""
        if name in self.servers:
            await self.servers[name].cleanup()
            del self.servers[name]
    
    async def restart_all(self):
        """Restart all managed servers."""
        for server in self.servers.values():
            await server.cleanup()
            await server.init(is_fetch_tools=False)
    
    async def cleanup_all(self):
        """Cleanup all servers."""
        for server in self.servers.values():
            await server.cleanup()
        self.servers.clear()
```

## Best Practices

### Configuration Management

```python
# ✅ Good: Structured configuration
class MCPServerConfig:
    FILESYSTEM = {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
        "base_env": {}
    }
    
    MEMORY = {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "base_env": {"MEMORY_SIZE": "1000"}
    }
    
    @classmethod
    def filesystem(cls, workspace_path: str) -> dict:
        config = cls.FILESYSTEM.copy()
        config["args"] = config["args"] + [workspace_path]
        return config

# Usage
fs_client = StdioMCPClient(
    name="filesystem",
    params=MCPServerConfig.filesystem("/workspace")
)
```

### Error Recovery

```python
# ✅ Good: Automatic recovery
class ResilientStdioClient(StdioMCPClient):
    def __init__(self, max_retries=3, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
    
    async def init_with_retry(self):
        """Initialize with automatic retry on failure."""
        for attempt in range(self.max_retries):
            try:
                await self.init()
                return
            except Exception as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Init attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
```

## Troubleshooting

### Process Validation

```python
# Debug process startup issues
async def debug_stdio_client(client):
    """Debug stdio client initialization."""
    try:
        # Test command resolution
        server_params = await client.get_server_params()
        logger.info(f"Command: {server_params.command}")
        logger.info(f"Args: {server_params.args}")
        logger.info(f"Env keys: {list(server_params.env.keys())}")
        
        # Test initialization
        await client.init()
        logger.info(f"Tools discovered: {client.included_tool_name_list}")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        # Check if command exists
        import shutil
        command = client.params["command"]
        if command == "npx":
            command = shutil.which("npx")
        logger.info(f"Command path: {command}")
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        await client.cleanup()
```

### Directory Issues

```python
# Debug directory validation
def debug_directory_setup(args):
    """Debug directory-related issues."""
    if len(args) >= 2 and "server-filesystem" in " ".join(args):
        target_dir = args[-1]
        logger.info(f"Target directory: {target_dir}")
        logger.info(f"Directory exists: {os.path.exists(target_dir)}")
        logger.info(f"Directory is writable: {os.access(target_dir, os.W_OK)}")
    
    if args[0] == "--directory" and len(args) >= 4:
        work_dir = args[1]
        mcp_file = os.path.join(work_dir, args[3])
        logger.info(f"Working directory: {work_dir}")
        logger.info(f"MCP file: {mcp_file}")
        logger.info(f"MCP file exists: {os.path.exists(mcp_file)}")
```

## API Reference

### Complete Class Definition

```python
class StdioMCPClient(BaseMCPClient):
    """MCP client implementation using standard I/O transport."""
    
    params: dict[str, Any] = Field(default_factory=dict)
    
    async def init(self, is_fetch_tools=True) -> None:
        """Initialize stdio connection to MCP server process."""
        
    async def call_tool(self, tool_name, arguments):
        """Execute tool with one-shot connection."""
        
    async def get_server_params(self):
        """Generate StdioServerParameters for server initialization."""
        
    async def _ensure_directories_exist(self, args: list[str]) -> None:
        """Ensure required directories exist before starting server."""
```

### Configuration Schema

```python
params = {
    "command": str,           # Executable command
    "args": list[str],        # Command arguments
    "env": dict[str, str]     # Environment variables
}
```

## See Also

- [BaseMCPClient](./base-mcp-client) - Base MCP client functionality
- [SSEMCPClient](./sse-mcp-client) - Server-Sent Events transport
- [StreamableMCPClient](./streamable-mcp-client) - Streamable HTTP transport
- [MCPTool](./mcp-tool) - Individual MCP tool proxy
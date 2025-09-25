---
title: FunctionHub
description: Central registry for dynamic Python function registration and management in OxyGent
---

# FunctionHub

The `FunctionHub` class serves as a central registry for converting Python functions into executable tools within the OxyGent system. It provides a decorator-based interface for dynamic function registration with automatic type conversion and schema generation.

## Class Overview

```python
from oxygent.oxy.function_tools import FunctionHub
from oxygent.oxy.base_tool import BaseTool

class FunctionHub(BaseTool):
    """Central hub for registering and managing Python functions as tools."""
```

### Inheritance Hierarchy
```
FunctionHub → BaseTool → Oxy
```

## Core Attributes

### `func_dict: dict`
Registry dictionary that maps function names to their metadata and execution functions.

**Format**: `{name: (description, async_func)}`
- `name`: Function name as string key
- `description`: Human-readable description of the function
- `async_func`: Asynchronous version of the function

```python
hub = FunctionHub()
# After registration, func_dict contains:
# {"add_numbers": ("Add two numbers", async_add_numbers)}
```

## Methods

### `__init__(**kwargs)`

Initialize a new FunctionHub instance.

```python
hub = FunctionHub(
    name="math_functions",
    desc="Mathematical utility functions",
    is_permission_required=True
)
```

### `async init()`

Initialize the hub by creating `FunctionTool` instances for all registered functions.

**Process:**
1. Calls parent `BaseTool.init()`
2. Iterates through `func_dict`
3. Creates `FunctionTool` instances for each registered function
4. Registers tools with the Multi-Agent System (MAS)

```python
await hub.init()
# Converts all registered functions to tools
# Registers them with MAS for agent access
```

**Implementation Details:**
```python
async def init(self):
    await super().init()
    params = self.model_dump(exclude={"func_dict", "name", "desc"})
    
    for tool_name, (tool_desc, tool_func) in self.func_dict.items():
        function_tool = FunctionTool(
            name=tool_name, 
            desc=tool_desc, 
            func_process=tool_func, 
            **params
        )
        function_tool.set_mas(self.mas)
        self.mas.add_oxy(function_tool)
```

### `tool(description: str)`

Decorator for registering functions as tools with automatic async conversion.

**Parameters:**
- `description` (str): Human-readable description of the tool's functionality

**Returns:**
- `Callable`: Decorator function that processes and registers the function

```python
@hub.tool("Calculate the sum of two numbers")
def add_numbers(a: int, b: int) -> int:
    return a + b

@hub.tool("Fetch data asynchronously")
async def fetch_data(url: str) -> dict:
    # Already async - no conversion needed
    return await httpx.get(url).json()
```

**Decorator Behavior:**

#### Synchronous Function Conversion
```python
# Original sync function
def sync_function(x: int) -> int:
    return x * 2

# Automatically wrapped as:
@functools.wraps(func)
async def async_func(*args, **kwargs):
    return func(*args, **kwargs)  # TODO: Use thread pool for blocking operations
```

#### Asynchronous Function Handling
```python
# Already async functions are used directly
if asyncio.iscoroutinefunction(func):
    async_func = func
```

## Usage Patterns

### Basic Registration

```python
from oxygent.oxy.function_tools import FunctionHub

hub = FunctionHub(name="utilities")

@hub.tool("Convert temperature from Celsius to Fahrenheit")
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert temperature from Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

@hub.tool("Generate unique identifier")
def generate_id() -> str:
    """Generate a unique identifier string."""
    import uuid
    return str(uuid.uuid4())
```

### Advanced Registration with Types

```python
from typing import List, Dict, Optional
from pydantic import Field

@hub.tool("Process user data with validation")
def process_users(
    users: List[Dict[str, str]], 
    filter_active: bool = Field(True, description="Filter only active users"),
    limit: Optional[int] = Field(None, description="Maximum number of users")
) -> List[Dict[str, str]]:
    """Process and filter user data."""
    result = users
    if filter_active:
        result = [u for u in result if u.get('status') == 'active']
    if limit:
        result = result[:limit]
    return result
```

### Context-Aware Functions

```python
from oxygent.schemas import OxyRequest

@hub.tool("Get request context information")
def get_context_info(message: str, oxy_request: OxyRequest) -> dict:
    """Extract information from request context."""
    return {
        "message": message,
        "trace_id": oxy_request.trace_id,
        "caller": oxy_request.caller,
        "timestamp": oxy_request.created_at
    }
```

### Async I/O Operations

```python
import httpx
import asyncio

@hub.tool("Fetch multiple URLs concurrently")
async def fetch_urls(urls: List[str]) -> List[dict]:
    """Fetch data from multiple URLs concurrently."""
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## Integration Examples

### With Multi-Agent System

```python
from oxygent.mas import MAS

# Create MAS and function hub
mas = MAS()
hub = FunctionHub(name="data_tools")

# Register functions
@hub.tool("Clean data format")
def clean_data(raw_data: str) -> str:
    return raw_data.strip().lower()

# Initialize and register
hub.set_mas(mas)
await hub.init()

# Functions are now available as tools in MAS
```

### With Agents

```python
from oxygent.agents import ChatAgent

# Create agent and function hub
agent = ChatAgent(name="data_processor")
hub = FunctionHub(name="processing_tools")

@hub.tool("Analyze text sentiment")
def analyze_sentiment(text: str) -> dict:
    # Sentiment analysis implementation
    return {"sentiment": "positive", "confidence": 0.8}

# Register hub with agent
agent.add_oxy(hub)
await agent.init()
```

## Best Practices

### Function Design

```python
# ✅ Good: Clear, focused functionality
@hub.tool("Calculate compound interest")
def calculate_compound_interest(
    principal: float,
    rate: float,
    time: int,
    compounds_per_year: int = 12
) -> float:
    """Calculate compound interest using standard formula."""
    return principal * (1 + rate/compounds_per_year) ** (compounds_per_year * time)

# ❌ Avoid: Overly complex, multiple responsibilities
@hub.tool("Do everything with data")
def process_everything(data: dict) -> dict:
    # Too many responsibilities in one function
    pass
```

### Error Handling

```python
@hub.tool("Safe division operation")
def safe_divide(dividend: float, divisor: float) -> dict:
    """Perform division with error handling."""
    try:
        if divisor == 0:
            return {"error": "Division by zero"}
        result = dividend / divisor
        return {"result": result, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}
```

### Type Annotations

```python
from typing import Union, List, Optional
from datetime import datetime

@hub.tool("Process timestamps")
def process_timestamps(
    timestamps: List[str],
    format_string: str = "%Y-%m-%d %H:%M:%S",
    timezone: Optional[str] = None
) -> List[datetime]:
    """Convert string timestamps to datetime objects."""
    # Implementation with proper type handling
    pass
```

## Configuration Options

### Permission Control

```python
# Require permission for sensitive operations
secure_hub = FunctionHub(
    name="secure_operations",
    is_permission_required=True
)

@secure_hub.tool("Delete user account")
def delete_account(user_id: str) -> dict:
    """Delete a user account - requires permission."""
    # Sensitive operation implementation
    pass
```

### Timeout Configuration

```python
# Set custom timeout for long-running operations
long_running_hub = FunctionHub(
    name="batch_operations",
    timeout=300.0  # 5 minutes
)

@long_running_hub.tool("Process large dataset")
async def process_large_dataset(data_path: str) -> dict:
    """Process large dataset - may take several minutes."""
    # Long-running operation implementation
    pass
```

## Troubleshooting

### Common Issues

#### Functions Not Appearing as Tools

**Problem**: Functions registered but not available in MAS

**Solution**:
```python
# Ensure proper initialization sequence
hub = FunctionHub(name="my_tools")

# Register functions first
@hub.tool("My function")
def my_function():
    pass

# Then set MAS and initialize
hub.set_mas(mas)
await hub.init()  # This step is crucial!
```

#### Async Conversion Issues

**Problem**: Sync functions with blocking I/O causing performance issues

**Current Limitation**: Sync functions are not yet executed in thread pools

**Workaround**:
```python
# Convert blocking operations to async manually
@hub.tool("File operation")
async def read_file_async(filename: str) -> str:
    import aiofiles
    async with aiofiles.open(filename, 'r') as f:
        return await f.read()
```

#### Schema Generation Problems

**Problem**: Complex types not properly recognized

**Solution**:
```python
from pydantic import Field, BaseModel

class UserData(BaseModel):
    name: str
    age: int

@hub.tool("Process structured data")
def process_user(
    user: dict,  # Use dict instead of custom models
    options: dict = Field(default_factory=dict, description="Processing options")
) -> dict:
    # Process as dictionary internally
    pass
```

## Performance Considerations

### Memory Usage
- Function dictionaries are stored in memory
- Consider function lifetime and cleanup
- Monitor memory usage with large numbers of functions

### Execution Overhead
- Minimal overhead for function registration
- Efficient lookup using dictionary keys
- Async conversion adds minimal performance cost

### Scaling Considerations
```python
# For large numbers of functions, consider multiple hubs
math_hub = FunctionHub(name="math_functions")
string_hub = FunctionHub(name="string_functions")
io_hub = FunctionHub(name="io_functions")

# Register each with MAS
for hub in [math_hub, string_hub, io_hub]:
    hub.set_mas(mas)
    await hub.init()
```

## API Reference

### Complete Class Definition

```python
class FunctionHub(BaseTool):
    """Central hub for registering and managing Python functions as tools."""
    
    func_dict: dict = Field(
        default_factory=dict, 
        description="Registry of functions and their metadata"
    )
    
    async def init(self) -> None:
        """Initialize hub and create FunctionTool instances."""
        
    def tool(self, description: str) -> Callable:
        """Decorator for registering functions as tools."""
```

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

- [FunctionTool](./function-tool) - Individual function wrapper implementation
- [BaseTool](/agents/base-agent) - Base class for all tools
- [MAS Integration](/flows/workflow-flow) - Multi-Agent System integration patterns
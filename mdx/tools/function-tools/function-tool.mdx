---
title: FunctionTool
description: Individual function wrapper that provides tool interface and execution environment for Python functions in OxyGent
---

# FunctionTool

The `FunctionTool` class wraps individual Python functions to make them executable within the OxyGent system. It automatically extracts input schemas from function signatures, handles parameter mapping, and provides a standardized tool execution interface.

## Class Overview

```python
from oxygent.oxy.function_tools import FunctionTool
from oxygent.oxy.base_tool import BaseTool

class FunctionTool(BaseTool):
    """Tool that wraps Python functions for execution within the OxyGent system."""
```

### Inheritance Hierarchy
```
FunctionTool → BaseTool → Oxy
```

## Core Attributes

### `func_process: Optional[Callable]`
The Python function to execute. Should be an async function or will be treated as async during execution.

```python
async def my_function(a: int, b: str) -> dict:
    return {"result": f"{a}_{b}"}

tool = FunctionTool(
    name="my_tool",
    desc="Example tool",
    func_process=my_function
)
```

### `is_permission_required: bool`
Whether permission is required for execution. Defaults to `True` for security.

### `needs_oxy_request: bool`
Automatically detected flag indicating whether the function requires `OxyRequest` parameter injection.

### `input_schema: dict`
Automatically generated schema describing the function's input parameters, extracted from the function signature.

**Schema Format:**
```json
{
    "properties": {
        "param_name": {
            "type": "type_name",
            "description": "parameter description"
        }
    },
    "required": ["required_param_names"]
}
```

## Constructor

### `__init__(**kwargs)`

Initialize the FunctionTool and extract the input schema from the function signature.

```python
def example_function(
    name: str,
    age: int,
    email: str = Field("", description="User email address"),
    oxy_request: OxyRequest = None
) -> dict:
    return {"name": name, "age": age, "email": email}

tool = FunctionTool(
    name="user_processor",
    desc="Process user information",
    func_process=example_function
)

# Automatically generated input_schema:
# {
#     "properties": {
#         "name": {"type": "str", "description": ""},
#         "age": {"type": "int", "description": ""},
#         "email": {"type": "str", "description": "User email address"}
#     },
#     "required": ["name", "age"]
# }
# needs_oxy_request: True
```

## Methods

### `_extract_input_schema(func: Callable) -> dict`

Extract input schema from function signature with support for type annotations and Pydantic Fields.

**Parameter Analysis:**
1. **Type Annotations**: Extracts parameter types from function annotations
2. **Pydantic Fields**: Handles `Field()` with descriptions and required/optional settings
3. **OxyRequest Detection**: Identifies parameters that need request context injection
4. **Default Values**: Determines required vs optional parameters

**Implementation Details:**

```python
def _extract_input_schema(self, func):
    sig = signature(func)
    schema = {"properties": {}, "required": []}
    needs_oxy_request = False
    
    for name, param in sig.parameters.items():
        param_type = param.annotation
        
        # Handle OxyRequest parameters
        if param_type != Parameter.empty:
            type_name = getattr(param_type, "__name__", str(param_type))
            if type_name == "OxyRequest":
                needs_oxy_request = True
                continue  # Don't include in schema
        
        # Extract type information
        if param_type is Parameter.empty:
            type_name = None
        else:
            type_name = getattr(param_type, "__name__", str(param_type))
        
        # Handle Pydantic Field annotations
        if isinstance(param.default, FieldInfo):
            desc = param.default.description or ""
            schema["properties"][name] = {"description": desc, "type": type_name}
            if param.default.is_required():
                schema["required"].append(name)
        # Handle parameters without defaults (required)
        elif param.default is Parameter.empty:
            schema["properties"][name] = {"description": "", "type": type_name}
            schema["required"].append(name)
    
    self.needs_oxy_request = needs_oxy_request
    return schema
```

### `async _execute(oxy_request: OxyRequest) -> OxyResponse`

Execute the wrapped function with provided arguments and proper parameter mapping.

**Execution Process:**

1. **Parameter Mapping**: Maps `OxyRequest.arguments` to function parameters
2. **Context Injection**: Injects `OxyRequest` for functions that need it
3. **Function Execution**: Calls the wrapped function with mapped parameters
4. **Response Generation**: Wraps result in `OxyResponse` with appropriate state

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    try:
        func_kwargs = {}
        sig = signature(self.func_process)
        
        # Map parameters from request to function arguments
        for param_name, param in sig.parameters.items():
            if param.annotation != Parameter.empty:
                param_type = param.annotation
                type_name = getattr(param_type, "__name__", str(param_type))
                
                # Inject OxyRequest for functions that need it
                if type_name == "OxyRequest":
                    func_kwargs[param_name] = oxy_request
                # Map regular parameters from request arguments
                elif param_name in oxy_request.arguments:
                    func_kwargs[param_name] = oxy_request.arguments[param_name]
            # Handle untyped parameters
            elif param_name in oxy_request.arguments:
                func_kwargs[param_name] = oxy_request.arguments[param_name]
        
        # Execute function and return result
        result = await self.func_process(**func_kwargs)
        return OxyResponse(state=OxyState.COMPLETED, output=result)
        
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.error(f"Error in function tool {self.name}: {error_msg}")
        return OxyResponse(state=OxyState.FAILED, output=str(e))
```

## Usage Examples

### Basic Function Wrapping

```python
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# Create FunctionTool instance
add_tool = FunctionTool(
    name="add_numbers",
    desc="Add two numbers together",
    func_process=add_numbers
)

# Execute through OxyRequest
from oxygent.schemas import OxyRequest
request = OxyRequest(
    callee="add_numbers",
    arguments={"a": 5, "b": 3}
)

response = await add_tool._execute(request)
# response.output = 8
# response.state = OxyState.COMPLETED
```

### Advanced Parameter Handling

```python
from pydantic import Field
from typing import Optional, List

def process_data(
    data: List[dict],
    filter_key: str,
    filter_value: Optional[str] = Field(None, description="Value to filter by"),
    limit: int = Field(10, description="Maximum number of results"),
    oxy_request: OxyRequest = None
) -> dict:
    """Process and filter data with request context."""
    
    # Access request metadata if needed
    trace_id = oxy_request.trace_id if oxy_request else None
    
    # Filter data
    if filter_value:
        filtered_data = [item for item in data if item.get(filter_key) == filter_value]
    else:
        filtered_data = data
    
    # Apply limit
    result = filtered_data[:limit]
    
    return {
        "count": len(result),
        "data": result,
        "trace_id": trace_id
    }

# Create tool with automatic schema extraction
process_tool = FunctionTool(
    name="process_data",
    desc="Process and filter data",
    func_process=process_data
)

# Generated schema:
# {
#     "properties": {
#         "data": {"type": "List[dict]", "description": ""},
#         "filter_key": {"type": "str", "description": ""},
#         "filter_value": {"type": "Optional[str]", "description": "Value to filter by"},
#         "limit": {"type": "int", "description": "Maximum number of results"}
#     },
#     "required": ["data", "filter_key"]
# }
# needs_oxy_request: True
```

### Async Function Support

```python
import httpx

async def fetch_user_data(user_id: str, include_posts: bool = False) -> dict:
    """Fetch user data from external API."""
    async with httpx.AsyncClient() as client:
        # Fetch user info
        user_response = await client.get(f"/api/users/{user_id}")
        user_data = user_response.json()
        
        # Optionally fetch posts
        if include_posts:
            posts_response = await client.get(f"/api/users/{user_id}/posts")
            user_data["posts"] = posts_response.json()
        
        return user_data

# Async functions work seamlessly
fetch_tool = FunctionTool(
    name="fetch_user_data",
    desc="Fetch user data from API",
    func_process=fetch_user_data
)
```

## Integration Patterns

### With FunctionHub

```python
# FunctionHub creates FunctionTool instances automatically
hub = FunctionHub(name="utilities")

@hub.tool("Convert units")
def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    # Conversion logic
    return converted_value

await hub.init()
# Creates FunctionTool instance internally and registers with MAS
```

### Direct Usage

```python
# Create FunctionTool directly for fine-grained control
tool = FunctionTool(
    name="custom_processor",
    desc="Custom data processor",
    func_process=my_custom_function,
    timeout=120.0,  # Custom timeout
    is_permission_required=False  # Override permission requirement
)

# Register with MAS
tool.set_mas(mas)
await tool.init()
```

### With Agents

```python
# Add to agent directly
agent = ChatAgent(name="data_agent")
agent.add_oxy(tool)

# Tool becomes available for agent execution
response = await agent.execute(OxyRequest(
    callee="custom_processor",
    arguments={"data": sample_data}
))
```

## Schema Generation Details

### Supported Type Annotations

```python
from typing import List, Dict, Optional, Union
from datetime import datetime

def typed_function(
    # Basic types
    name: str,
    age: int,
    height: float,
    is_active: bool,
    
    # Complex types
    tags: List[str],
    metadata: Dict[str, any],
    optional_field: Optional[str],
    union_field: Union[str, int],
    
    # Datetime
    created_at: datetime,
    
    # With descriptions
    email: str = Field("", description="User email address"),
    
    # Optional with defaults
    status: str = "active",
    
    # Context injection
    oxy_request: OxyRequest = None
) -> dict:
    pass
```

**Generated Schema:**
```json
{
    "properties": {
        "name": {"type": "str", "description": ""},
        "age": {"type": "int", "description": ""},
        "height": {"type": "float", "description": ""},
        "is_active": {"type": "bool", "description": ""},
        "tags": {"type": "List[str]", "description": ""},
        "metadata": {"type": "Dict[str, any]", "description": ""},
        "optional_field": {"type": "Optional[str]", "description": ""},
        "union_field": {"type": "Union[str, int]", "description": ""},
        "created_at": {"type": "datetime", "description": ""},
        "email": {"type": "str", "description": "User email address"}
    },
    "required": ["name", "age", "height", "is_active", "tags", "metadata", "optional_field", "union_field", "created_at"]
}
```

### Pydantic Field Integration

```python
from pydantic import Field

def advanced_function(
    # Required field with description
    user_id: str = Field(description="Unique user identifier"),
    
    # Optional field with default and description
    page_size: int = Field(20, description="Number of items per page"),
    
    # Required field (no default, but Field used for description)
    query: str = Field(..., description="Search query string"),
    
    # Optional field with complex validation
    email: Optional[str] = Field(None, description="Email address", regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
) -> dict:
    pass
```

## Error Handling

### Exception Management

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    try:
        # Function execution logic
        result = await self.func_process(**func_kwargs)
        return OxyResponse(state=OxyState.COMPLETED, output=result)
    except Exception as e:
        # Comprehensive error logging
        import traceback
        error_msg = traceback.format_exc()
        logger.error(f"Error in function tool {self.name}: {error_msg}")
        
        # Return failed response with error message
        return OxyResponse(state=OxyState.FAILED, output=str(e))
```

### Custom Error Handling in Functions

```python
def robust_function(data: dict) -> dict:
    """Function with built-in error handling."""
    try:
        # Main processing logic
        result = process_data(data)
        return {"status": "success", "data": result}
    except ValidationError as e:
        # Return structured error response
        return {"status": "error", "error_type": "validation", "message": str(e)}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error_type": "unknown", "message": str(e)}

# Tool will receive structured error response instead of exception
tool = FunctionTool(name="robust_tool", func_process=robust_function)
```

## Performance Considerations

### Memory Usage
- Input schema is generated once during initialization
- Function reference is stored, not copied
- Minimal memory overhead per tool instance

### Execution Performance
- Direct function call with parameter mapping
- Minimal overhead for argument processing
- Async execution maintains performance benefits

### Optimization Tips

```python
# Pre-compile complex operations
import re

# Compile regex patterns at module level
EMAIL_PATTERN = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

def validate_email(email: str) -> dict:
    """Use pre-compiled patterns for better performance."""
    if EMAIL_PATTERN.match(email):
        return {"valid": True}
    return {"valid": False, "error": "Invalid email format"}
```

## Best Practices

### Function Design

```python
# ✅ Good: Clear interface, proper types, error handling
def calculate_distance(
    lat1: float = Field(description="Starting latitude"),
    lon1: float = Field(description="Starting longitude"),
    lat2: float = Field(description="Ending latitude"),
    lon2: float = Field(description="Ending longitude"),
    unit: str = Field("km", description="Distance unit: 'km' or 'miles'")
) -> dict:
    """Calculate distance between two geographic points."""
    try:
        # Haversine formula implementation
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        if unit == "miles":
            distance = distance * 0.621371
        return {"distance": distance, "unit": unit}
    except Exception as e:
        return {"error": str(e)}

# ❌ Avoid: Unclear interface, no error handling
def calc_dist(p1, p2):
    return some_calculation(p1, p2)  # May raise exceptions
```

### Parameter Validation

```python
from typing import Literal

def process_order(
    order_id: str = Field(description="Order identifier"),
    action: Literal["approve", "reject", "hold"] = Field(description="Action to take"),
    reason: Optional[str] = Field(None, description="Reason for action")
) -> dict:
    """Process order with validated action types."""
    # Implementation with guaranteed valid action values
    pass
```

## Troubleshooting

### Schema Generation Issues

**Problem**: Complex types not recognized properly

```python
# ❌ Problem: Custom class not in schema
class CustomData:
    pass

def process_custom(data: CustomData) -> dict:
    pass

# ✅ Solution: Use dict or basic types
def process_custom(data: dict) -> dict:
    # Validate and convert internally
    pass
```

**Problem**: Optional parameters not handled correctly

```python
# ❌ Problem: Ambiguous optional handling
def ambiguous_function(param=None):
    pass

# ✅ Solution: Explicit typing and Field usage
def clear_function(
    param: Optional[str] = Field(None, description="Optional parameter")
) -> dict:
    pass
```

### Execution Issues

**Problem**: Parameter mapping failures

```python
# Check parameter names match exactly
request = OxyRequest(
    callee="my_function",
    arguments={
        "param_name": "value",  # Must match function parameter name exactly
        "another_param": 42
    }
)
```

**Problem**: Missing required parameters

```python
# Ensure all required parameters are provided
def my_function(required_param: str, optional_param: str = "default"):
    pass

# Required: must provide required_param
request = OxyRequest(
    arguments={"required_param": "value"}  # optional_param will use default
)
```

## API Reference

### Complete Class Definition

```python
class FunctionTool(BaseTool):
    """Tool that wraps Python functions for execution within the OxyGent system."""
    
    is_permission_required: bool = Field(True, description="")
    func_process: Optional[Callable] = Field(None, exclude=True, description="")
    needs_oxy_request: bool = Field(False, description="Whether this tool needs oxy_request parameter")
    
    def __init__(self, **kwargs):
        """Initialize the function tool and extract input schema."""
        
    def _extract_input_schema(self, func: Callable) -> dict:
        """Extract input schema from function signature."""
        
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute the wrapped function with provided arguments."""
```

### Inherited Properties

From `BaseTool`:
- `category: str = "tool"`
- `timeout: float = 60`

From `Oxy`:
- `name: str`
- `desc: str`
- `mas: Optional[MAS] = None`

## See Also

- [FunctionHub](./function-hub) - Central registry for function management
- [BaseTool](/agents/base-agent) - Base class for all tools
- [Schemas](/flows/workflow-flow) - OxyRequest and OxyResponse details
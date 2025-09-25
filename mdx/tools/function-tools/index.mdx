---
title: Function Tools Overview
description: Comprehensive guide to OxyGent's Function Tools system for dynamic function registration and execution
---

# Function Tools Overview

The Function Tools system is a core component of OxyGent that enables dynamic registration and execution of Python functions as tools within the framework. It provides a decorator-based interface for converting regular Python functions into executable tools with automatic schema generation and type safety.

## Architecture Overview

The Function Tools system consists of two main components:

- **[FunctionHub](./function-hub)**: Central registry for managing and converting Python functions into tools
- **[FunctionTool](./function-tool)**: Individual function wrapper that provides tool interface and execution environment

```mermaid
graph TD
    A[Python Function] -->|@hub.tool()| B[FunctionHub]
    B -->|init()| C[FunctionTool Instance]
    C -->|register| D[Multi-Agent System]
    D -->|execute| E[OxyRequest/OxyResponse]
```

## Quick Start

### Basic Function Registration

```python
from oxygent.oxy.function_tools import FunctionHub

# Create a function hub
hub = FunctionHub(name="my_functions", desc="Custom function collection")

@hub.tool("Calculate the sum of two numbers")
def add_numbers(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b

@hub.tool("Fetch user information from database")
async def get_user(user_id: str, oxy_request: OxyRequest) -> dict:
    """Retrieve user data with request context."""
    # Access request context through oxy_request
    return {"user_id": user_id, "status": "active"}
```

### Integration with MAS

```python
from oxygent.mas import MAS

# Initialize Multi-Agent System
mas = MAS()

# Register function hub
hub.set_mas(mas)
await hub.init()  # This converts functions to tools and registers them
```

## Key Features

### 🎯 Decorator-Based Registration
- Simple `@hub.tool("description")` decorator
- Automatic conversion of sync functions to async
- Preserves function metadata and signatures

### 📋 Automatic Schema Generation
- Extracts input schemas from function signatures
- Supports type annotations and Pydantic Fields
- Automatic parameter validation

### 🔗 Smart Parameter Injection
- Automatic injection of `OxyRequest` parameters
- Flexible argument mapping from requests
- Support for both positional and keyword arguments

### ⚡ Performance Optimization
- Efficient function registration and lookup
- Minimal overhead for function execution
- Thread-safe operations

### 🛡️ Security & Error Handling
- Permission-based execution control
- Comprehensive error logging
- Graceful failure handling

## Use Cases

### Custom Business Logic
```python
@hub.tool("Process customer order")
def process_order(customer_id: str, items: list, discount: float = 0.0):
    # Custom business logic implementation
    total = calculate_total(items, discount)
    return {"order_id": generate_order_id(), "total": total}
```

### System Integration
```python
@hub.tool("Send notification via external service")
async def send_notification(message: str, channel: str):
    # Integration with external notification service
    return await external_service.send(message, channel)
```

### Data Processing
```python
@hub.tool("Transform data format")
def transform_data(input_data: dict, format_type: str):
    # Data transformation logic
    if format_type == "json":
        return json.dumps(input_data)
    elif format_type == "xml":
        return dict_to_xml(input_data)
```

## Best Practices

### Function Design
- Keep functions focused on single responsibilities
- Use descriptive function names and docstrings
- Implement proper error handling
- Use type annotations for better schema generation

### Performance Considerations
- Avoid blocking operations in sync functions
- Use async functions for I/O operations
- Consider thread pool execution for CPU-intensive tasks

### Security Guidelines
- Validate input parameters
- Implement proper authentication checks
- Use `is_permission_required` for sensitive operations
- Sanitize outputs to prevent data leakage

## Advanced Configuration

### Custom Parameter Handling
```python
from pydantic import Field

@hub.tool("Advanced parameter handling")
def advanced_function(
    required_param: str,
    optional_param: str = Field("default", description="Optional parameter"),
    oxy_request: OxyRequest = None
):
    # Access request metadata
    if oxy_request:
        trace_id = oxy_request.trace_id
        caller = oxy_request.caller
    
    return {"result": f"Processed {required_param}"}
```

### Error Handling Strategies
```python
@hub.tool("Function with error handling")
async def robust_function(data: dict):
    try:
        # Main processing logic
        result = process_data(data)
        return {"status": "success", "data": result}
    except ValidationError as e:
        # Specific error handling
        return {"status": "error", "message": str(e)}
    except Exception as e:
        # Generic error handling
        logger.error(f"Unexpected error: {e}")
        raise
```

## Integration Examples

### With Agents
```python
# Function hub setup
hub = FunctionHub(name="agent_tools")

@hub.tool("Analyze text sentiment")
def analyze_sentiment(text: str) -> dict:
    return {"sentiment": "positive", "confidence": 0.85}

# Agent integration
agent = ChatAgent(name="sentiment_analyzer")
agent.add_oxy(hub)
```

### With Workflows
```python
# Workflow integration
workflow = WorkflowFlow(name="data_processing")
workflow.add_oxy(hub)

# Functions become available as workflow steps
workflow.add_step("transform_data", {"input_data": "{prev_output}"})
```

## Troubleshooting

### Common Issues

#### Function Not Registered
- Ensure `@hub.tool()` decorator is applied
- Check that `hub.init()` is called
- Verify MAS registration

#### Schema Generation Problems
- Use proper type annotations
- Check Pydantic Field usage
- Validate function signatures

#### Execution Failures
- Review error logs for details
- Check parameter mapping
- Verify function implementation

## Next Steps

- Explore [FunctionHub](./function-hub) for detailed registration patterns
- Learn [FunctionTool](./function-tool) internals for advanced usage
- Check out integration examples in the [Agents](/agents) section
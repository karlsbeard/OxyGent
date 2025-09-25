---
title: "Workflow Flow"
description: "Custom workflow execution flow for the OxyGent framework"
---

# Workflow Flow

The Workflow class provides a bridge between the OxyGent flow framework and user-defined workflow logic, enabling execution of custom workflow functions within the flow system.

## Overview

The Workflow flow serves as an adapter that allows you to integrate custom workflow functions into the OxyGent framework. It extends the BaseFlow class and provides a simple way to execute arbitrary workflow logic while maintaining compatibility with the OxyGent request/response pattern.

## Class Definition

```python
from oxygent.oxy.flows import Workflow
```

### Inheritance Hierarchy

```
BaseFlow
└── Workflow
```

## Attributes

### func_workflow
- **Type**: `Optional[Callable]`
- **Default**: `None`
- **Description**: The custom workflow function to execute
- **Requirements**: Must accept an `OxyRequest` parameter and return a result
- **Field Options**: `exclude=True` (excluded from serialization)

## Methods

### _execute(oxy_request: OxyRequest) → OxyResponse

The core execution method that runs the custom workflow function.

**Parameters:**
- `oxy_request` (`OxyRequest`): The incoming request containing the workflow parameters

**Returns:**
- `OxyResponse`: Response with execution state and workflow output

**Behavior:**
1. Calls the configured `func_workflow` with the provided request
2. Wraps the result in an `OxyResponse` with `COMPLETED` state
3. Returns the response containing the workflow output

## Usage Examples

### Basic Workflow Function

```python
from oxygent.oxy.flows import Workflow
from oxygent.schemas import OxyRequest

async def simple_workflow(oxy_request: OxyRequest):
    """A simple workflow that processes the input query."""
    query = oxy_request.get_query()
    return f"Processed: {query}"

# Create workflow flow
workflow_flow = Workflow(
    name="simple_workflow",
    desc="Simple data processing workflow",
    func_workflow=simple_workflow
)
```

### Data Processing Workflow

```python
async def data_processing_workflow(oxy_request: OxyRequest):
    """A workflow that performs complex data processing."""
    
    # Extract data from request
    data = oxy_request.arguments.get("data", [])
    operation = oxy_request.arguments.get("operation", "sum")
    
    # Process data based on operation
    if operation == "sum":
        result = sum(data)
    elif operation == "average":
        result = sum(data) / len(data) if data else 0
    elif operation == "max":
        result = max(data) if data else None
    elif operation == "min":
        result = min(data) if data else None
    else:
        result = f"Unknown operation: {operation}"
    
    return {
        "operation": operation,
        "input_data": data,
        "result": result,
        "processed_count": len(data)
    }

# Create workflow flow
data_workflow = Workflow(
    name="data_processor",
    desc="Data processing workflow with multiple operations",
    func_workflow=data_processing_workflow
)
```

### Multi-step Workflow

```python
async def multi_step_workflow(oxy_request: OxyRequest):
    """A workflow with multiple processing steps."""
    
    input_text = oxy_request.get_query()
    
    # Step 1: Text preprocessing
    cleaned_text = input_text.strip().lower()
    
    # Step 2: Analysis
    word_count = len(cleaned_text.split())
    char_count = len(cleaned_text)
    
    # Step 3: Generate report
    report = {
        "original_text": input_text,
        "cleaned_text": cleaned_text,
        "statistics": {
            "word_count": word_count,
            "character_count": char_count,
            "average_word_length": char_count / word_count if word_count > 0 else 0
        },
        "processing_steps": [
            "Text normalization",
            "Statistical analysis", 
            "Report generation"
        ]
    }
    
    return report

# Create workflow flow
analysis_workflow = Workflow(
    name="text_analyzer",
    desc="Multi-step text analysis workflow",
    func_workflow=multi_step_workflow
)
```

### Workflow with External API Calls

```python
import aiohttp
from typing import Dict, Any

async def api_integration_workflow(oxy_request: OxyRequest) -> Dict[str, Any]:
    """Workflow that integrates with external APIs."""
    
    endpoint = oxy_request.arguments.get("endpoint")
    method = oxy_request.arguments.get("method", "GET")
    headers = oxy_request.arguments.get("headers", {})
    
    if not endpoint:
        return {"error": "No endpoint specified"}
    
    try:
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(endpoint, headers=headers) as response:
                    data = await response.json()
            elif method.upper() == "POST":
                payload = oxy_request.arguments.get("payload", {})
                async with session.post(endpoint, json=payload, headers=headers) as response:
                    data = await response.json()
            else:
                return {"error": f"Unsupported method: {method}"}
                
        return {
            "success": True,
            "status_code": response.status,
            "data": data,
            "endpoint": endpoint,
            "method": method
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "endpoint": endpoint,
            "method": method
        }

# Create API integration workflow
api_workflow = Workflow(
    name="api_integrator",
    desc="Workflow for external API integration",
    func_workflow=api_integration_workflow
)
```

## Integration with OxyGent Framework

### In OxySpace Configuration

```python
# In your oxy_space configuration
def create_workflow_flows():
    return [
        Workflow(
            name="custom_processor",
            desc="Custom data processing workflow",
            func_workflow=your_custom_function,
            permitted_tool_name_list=["data_tool", "api_tool"]
        ),
        Workflow(
            name="business_logic",
            desc="Business-specific workflow implementation",
            func_workflow=business_workflow_function
        )
    ]
```

### Request Execution

```python
# Execute workflow through OxyGent framework
oxy_request = OxyRequest(
    callee="custom_processor",
    arguments={
        "data": [1, 2, 3, 4, 5],
        "operation": "average"
    }
)

response = await oxy_request.call()
print(response.output)  # Workflow result
```

## Best Practices

### 1. Error Handling

```python
async def robust_workflow(oxy_request: OxyRequest):
    """Workflow with proper error handling."""
    try:
        # Workflow logic here
        result = perform_complex_operation(oxy_request)
        return {"success": True, "result": result}
        
    except ValidationError as e:
        return {"success": False, "error": f"Validation error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
```

### 2. Input Validation

```python
async def validated_workflow(oxy_request: OxyRequest):
    """Workflow with input validation."""
    
    # Validate required parameters
    required_fields = ["input_data", "operation_type"]
    for field in required_fields:
        if field not in oxy_request.arguments:
            return {"error": f"Missing required field: {field}"}
    
    # Validate data types
    input_data = oxy_request.arguments["input_data"]
    if not isinstance(input_data, list):
        return {"error": "input_data must be a list"}
    
    # Proceed with workflow
    return process_validated_data(input_data)
```

### 3. Logging and Monitoring

```python
import logging

logger = logging.getLogger(__name__)

async def monitored_workflow(oxy_request: OxyRequest):
    """Workflow with logging and monitoring."""
    
    start_time = time.time()
    logger.info(f"Starting workflow with request: {oxy_request.arguments}")
    
    try:
        result = await perform_workflow_logic(oxy_request)
        
        duration = time.time() - start_time
        logger.info(f"Workflow completed successfully in {duration:.2f}s")
        
        return {
            "result": result,
            "execution_time": duration,
            "status": "success"
        }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Workflow failed after {duration:.2f}s: {str(e)}")
        
        return {
            "error": str(e),
            "execution_time": duration,
            "status": "failed"
        }
```

### 4. Async Best Practices

```python
async def async_workflow(oxy_request: OxyRequest):
    """Properly structured async workflow."""
    
    # Use async operations for I/O
    async with aiofiles.open('data.json', 'r') as f:
        data = json.loads(await f.read())
    
    # Use asyncio.gather for concurrent operations
    results = await asyncio.gather(
        process_data_chunk(data[:100]),
        process_data_chunk(data[100:200]),
        process_data_chunk(data[200:])
    )
    
    return {"processed_chunks": len(results), "total_items": len(data)}
```

## Common Use Cases

1. **Data Processing Pipelines**: Transform and analyze data through multiple steps
2. **API Integration**: Connect with external services and APIs
3. **Business Logic Implementation**: Execute domain-specific business rules
4. **File Processing**: Read, process, and write files with custom logic
5. **Notification Systems**: Send alerts and notifications based on conditions
6. **Custom Analytics**: Generate reports and insights from data

## Technical Notes

- The `func_workflow` attribute is excluded from serialization (`exclude=True`)
- Workflow functions must be async and accept an `OxyRequest` parameter
- Return values are automatically wrapped in `OxyResponse` objects
- The flow inherits all capabilities from `BaseFlow`, including permission management
- Workflow functions should handle their own error cases and return appropriate responses

## Related Documentation

- [BaseFlow](/base-flow) - Base class for all flows
- [ParallelFlow](/parallel-flow) - Concurrent execution flow
- [PlanAndSolve](/plan-and-solve-flow) - Planning and execution flow
- [Reflexion](/reflexion-flow) - Iterative improvement flow
- [OxyRequest](/oxy-request) - Request object structure
- [OxyResponse](/oxy-response) - Response object structure
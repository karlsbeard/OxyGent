---
title: WorkflowAgent
description: Agent that executes custom workflow functions within the OxyGent framework
---

# WorkflowAgent

The `WorkflowAgent` class extends `LocalAgent` to provide a flexible bridge between the OxyGent agent system and custom workflow logic. It enables the execution of user-defined functions within the agent framework while maintaining all the benefits of trace management, memory, and tool integration.

## Overview

`WorkflowAgent` is designed for scenarios where you need to:

- **Integrate Custom Logic**: Execute existing Python functions within the agent framework
- **Rapid Prototyping**: Quickly convert functions to agents without complex refactoring
- **Legacy Integration**: Wrap existing business logic or algorithms as agents
- **Flexible Workflows**: Implement complex, multi-step processes as single agent calls
- **Bridge Pattern**: Connect traditional Python functions with the agent ecosystem

This agent is particularly useful for:
- Wrapping existing business logic functions
- Creating custom data processing pipelines
- Implementing domain-specific algorithms
- Rapid prototyping of agent behaviors
- Testing custom logic within the agent framework

## Architecture

### Execution Flow

```
OxyRequest
     ↓
┌─────────────────────────┐
│     WorkflowAgent       │
│                         │
│  ┌─────────────────┐   │
│  │  func_workflow   │   │  ← Custom Function
│  └─────────────────┘   │
│                         │
└─────────────────────────┘
     ↓
OxyResponse
```

### Function Integration

WorkflowAgent provides a simple interface for function integration:

1. Define your custom workflow function
2. Assign it to `func_workflow` attribute
3. The agent handles request/response conversion automatically
4. Full access to OxyRequest context and capabilities

## Class Definition

```python
from oxygent.oxy.agents import WorkflowAgent
from oxygent.schemas import OxyRequest, OxyResponse

# Define your workflow function
async def my_workflow(oxy_request: OxyRequest):
    # Your custom logic here
    query = oxy_request.get_query()
    result = f"Processed: {query}"
    return result

# Create the workflow agent
workflow_agent = WorkflowAgent(
    name="custom_processor",
    func_workflow=my_workflow
)
```

## Key Attribute

### func_workflow
- **Type**: `Optional[Callable]`
- **Default**: `None`
- **Description**: The workflow function to execute
- **Signature**: `async def func_workflow(oxy_request: OxyRequest) -> Any`
- **Excluded**: From serialization (marked with `exclude=True`)

## Usage Examples

### Basic Data Processing Workflow

```python
from oxygent.oxy.agents import WorkflowAgent
from oxygent.schemas import OxyRequest

async def data_processing_workflow(oxy_request: OxyRequest):
    """Custom data processing pipeline"""
    
    # Extract input data
    data = oxy_request.arguments.get("data", [])
    operation = oxy_request.arguments.get("operation", "process")
    
    if operation == "analyze":
        # Perform data analysis
        result = {
            "total_items": len(data),
            "average": sum(data) / len(data) if data else 0,
            "max_value": max(data) if data else None,
            "min_value": min(data) if data else None
        }
        return f"Data Analysis Complete: {result}"
    
    elif operation == "transform":
        # Transform data
        multiplier = oxy_request.arguments.get("multiplier", 2)
        transformed = [x * multiplier for x in data]
        return f"Data transformed: {transformed}"
    
    else:
        return "Unknown operation. Supported: analyze, transform"

# Create the workflow agent
data_processor = WorkflowAgent(
    name="data_processor",
    func_workflow=data_processing_workflow
)
```

### Business Logic Integration

```python
import asyncio
from datetime import datetime
from oxygent.oxy.agents import WorkflowAgent

async def order_processing_workflow(oxy_request: OxyRequest):
    """E-commerce order processing workflow"""
    
    order_data = oxy_request.arguments.get("order", {})
    
    # Step 1: Validate order
    if not order_data.get("items") or not order_data.get("customer_id"):
        return {"status": "error", "message": "Invalid order data"}
    
    # Step 2: Check inventory (simulated)
    await asyncio.sleep(0.1)  # Simulate database call
    inventory_available = True  # Simulated result
    
    if not inventory_available:
        return {"status": "error", "message": "Items not available"}
    
    # Step 3: Calculate total
    items = order_data["items"]
    total = sum(item["price"] * item["quantity"] for item in items)
    
    # Step 4: Apply discounts
    discount_rate = oxy_request.arguments.get("discount", 0)
    final_total = total * (1 - discount_rate)
    
    # Step 5: Generate order confirmation
    order_id = f"ORD-{int(datetime.now().timestamp())}"
    
    return {
        "status": "success",
        "order_id": order_id,
        "total": final_total,
        "estimated_delivery": "3-5 business days",
        "items_count": len(items)
    }

order_processor = WorkflowAgent(
    name="order_processor",
    func_workflow=order_processing_workflow
)
```

### Multi-Tool Workflow

```python
async def research_workflow(oxy_request: OxyRequest):
    """Complex research workflow using multiple tools"""
    
    research_topic = oxy_request.get_query()
    
    # Step 1: Web search for initial information
    search_result = await oxy_request.call(
        callee="web_search",
        arguments={"query": f"{research_topic} latest research 2024"}
    )
    
    # Step 2: Extract key points
    key_points = await oxy_request.call(
        callee="text_analyzer",
        arguments={"text": search_result.output, "task": "extract_key_points"}
    )
    
    # Step 3: Generate detailed analysis
    analysis_result = await oxy_request.call(
        callee="gpt-4",
        arguments={
            "messages": [
                {"role": "system", "content": "You are a research analyst."},
                {"role": "user", "content": f"Analyze this research on {research_topic}: {key_points.output}"}
            ]
        }
    )
    
    # Step 4: Create summary report
    report = {
        "topic": research_topic,
        "sources_found": search_result.output.count("http"),
        "key_findings": key_points.output,
        "detailed_analysis": analysis_result.output,
        "generated_at": datetime.now().isoformat()
    }
    
    return report

research_agent = WorkflowAgent(
    name="research_agent",
    func_workflow=research_workflow
)
```

### State Machine Workflow

```python
class OrderStateMachine:
    def __init__(self):
        self.states = {
            "pending": self.process_pending,
            "confirmed": self.process_confirmed,
            "shipped": self.process_shipped,
            "delivered": self.process_delivered
        }
    
    async def process_pending(self, order_data):
        # Validate and confirm order
        return {"new_state": "confirmed", "message": "Order confirmed"}
    
    async def process_confirmed(self, order_data):
        # Prepare for shipping
        return {"new_state": "shipped", "message": "Order shipped"}
    
    async def process_shipped(self, order_data):
        # Track delivery
        return {"new_state": "delivered", "message": "Order delivered"}
    
    async def process_delivered(self, order_data):
        # Complete order
        return {"new_state": "completed", "message": "Order completed"}

state_machine = OrderStateMachine()

async def state_machine_workflow(oxy_request: OxyRequest):
    """State machine workflow implementation"""
    
    current_state = oxy_request.arguments.get("state", "pending")
    order_data = oxy_request.arguments.get("order_data", {})
    
    if current_state not in state_machine.states:
        return {"error": f"Invalid state: {current_state}"}
    
    # Execute state-specific logic
    result = await state_machine.states[current_state](order_data)
    
    return {
        "previous_state": current_state,
        "current_state": result["new_state"],
        "message": result["message"],
        "timestamp": datetime.now().isoformat()
    }

state_agent = WorkflowAgent(
    name="order_state_machine",
    func_workflow=state_machine_workflow
)
```

### File Processing Workflow

```python
import json
import csv
from io import StringIO

async def file_processing_workflow(oxy_request: OxyRequest):
    """Advanced file processing workflow"""
    
    file_content = oxy_request.arguments.get("file_content", "")
    file_type = oxy_request.arguments.get("file_type", "auto")
    operation = oxy_request.arguments.get("operation", "analyze")
    
    # Auto-detect file type if needed
    if file_type == "auto":
        if file_content.strip().startswith("{"):
            file_type = "json"
        elif "," in file_content and "\n" in file_content:
            file_type = "csv"
        else:
            file_type = "text"
    
    # Process based on file type
    if file_type == "json":
        try:
            data = json.loads(file_content)
            if operation == "analyze":
                return {
                    "file_type": "json",
                    "keys": list(data.keys()) if isinstance(data, dict) else "array",
                    "size": len(data),
                    "structure": type(data).__name__
                }
            elif operation == "transform":
                # Custom transformation logic
                transformed = {k: v for k, v in data.items() if v is not None}
                return {"transformed_data": transformed}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
    
    elif file_type == "csv":
        try:
            csv_data = list(csv.DictReader(StringIO(file_content)))
            if operation == "analyze":
                return {
                    "file_type": "csv",
                    "rows": len(csv_data),
                    "columns": list(csv_data[0].keys()) if csv_data else [],
                    "sample": csv_data[:3] if csv_data else []
                }
        except Exception as e:
            return {"error": f"CSV processing error: {str(e)}"}
    
    else:  # text
        if operation == "analyze":
            return {
                "file_type": "text",
                "characters": len(file_content),
                "words": len(file_content.split()),
                "lines": file_content.count("\n") + 1
            }
    
    return {"error": "Unsupported operation"}

file_processor = WorkflowAgent(
    name="file_processor",
    func_workflow=file_processing_workflow
)
```

## Advanced Integration Patterns

### Workflow with Memory Access

```python
async def memory_aware_workflow(oxy_request: OxyRequest):
    """Workflow that uses conversation memory"""
    
    # Access conversation history
    short_memory = oxy_request.get_short_memory()
    current_query = oxy_request.get_query()
    
    # Analyze conversation context
    if short_memory:
        last_interaction = short_memory[-1] if short_memory else None
        context = f"Previous context: {last_interaction.get('content', 'None')}"
    else:
        context = "No previous context"
    
    # Process with context awareness
    result = f"Processing '{current_query}' with context: {context}"
    
    return result

context_agent = WorkflowAgent(
    name="context_aware_processor",
    func_workflow=memory_aware_workflow
)
```

### Error Handling Workflow

```python
async def robust_workflow(oxy_request: OxyRequest):
    """Workflow with comprehensive error handling"""
    
    try:
        # Main processing logic
        data = oxy_request.arguments.get("data")
        
        if not data:
            raise ValueError("No data provided")
        
        # Simulate processing
        result = {"processed": True, "data_length": len(str(data))}
        
        return result
    
    except ValueError as e:
        return {"error": "validation", "message": str(e)}
    except TypeError as e:
        return {"error": "type", "message": str(e)}
    except Exception as e:
        return {"error": "general", "message": f"Unexpected error: {str(e)}"}

robust_agent = WorkflowAgent(
    name="robust_processor",
    func_workflow=robust_workflow
)
```

### Async Integration with External Services

```python
import httpx

async def api_integration_workflow(oxy_request: OxyRequest):
    """Workflow integrating with external APIs"""
    
    service = oxy_request.arguments.get("service", "default")
    endpoint = oxy_request.arguments.get("endpoint", "/api/data")
    method = oxy_request.arguments.get("method", "GET")
    
    base_urls = {
        "service_a": "https://api.service-a.com",
        "service_b": "https://api.service-b.com",
        "default": "https://api.default.com"
    }
    
    base_url = base_urls.get(service, base_urls["default"])
    
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(f"{base_url}{endpoint}")
            elif method == "POST":
                payload = oxy_request.arguments.get("payload", {})
                response = await client.post(f"{base_url}{endpoint}", json=payload)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            return {
                "status_code": response.status_code,
                "data": response.json(),
                "service": service
            }
    
    except httpx.RequestError as e:
        return {"error": "request", "message": str(e)}
    except Exception as e:
        return {"error": "general", "message": str(e)}

api_agent = WorkflowAgent(
    name="api_integrator",
    func_workflow=api_integration_workflow
)
```

## Configuration and Customization

### Workflow with Configuration

```python
class ConfigurableWorkflow:
    def __init__(self, config: dict):
        self.config = config
    
    async def __call__(self, oxy_request: OxyRequest):
        # Access configuration
        max_items = self.config.get("max_items", 100)
        timeout = self.config.get("timeout", 30)
        
        # Use configuration in processing
        data = oxy_request.arguments.get("items", [])[:max_items]
        
        # Simulate timeout-aware processing
        await asyncio.sleep(min(0.1, timeout / 1000))
        
        return {
            "processed_items": len(data),
            "max_allowed": max_items,
            "config_used": self.config
        }

# Create configured workflow
workflow_config = {"max_items": 50, "timeout": 10, "debug": True}
configured_workflow = ConfigurableWorkflow(workflow_config)

configured_agent = WorkflowAgent(
    name="configured_processor",
    func_workflow=configured_workflow
)
```

## Best Practices

1. **Keep Functions Focused**: Each workflow should have a single, clear purpose
   ```python
   # Good: Focused on specific task
   async def calculate_metrics(oxy_request):
       return calculate_business_metrics(oxy_request.arguments["data"])
   
   # Avoid: Too many responsibilities
   async def do_everything(oxy_request):
       # Don't mix unrelated operations
   ```

2. **Use Async/Await Properly**: Leverage asynchronous capabilities
   ```python
   async def async_workflow(oxy_request: OxyRequest):
       # Use await for I/O operations
       result = await external_api_call()
       return result
   ```

3. **Handle Errors Gracefully**: Provide meaningful error responses
   ```python
   async def safe_workflow(oxy_request: OxyRequest):
       try:
           return process_data(oxy_request.arguments)
       except Exception as e:
           return {"error": str(e), "status": "failed"}
   ```

4. **Leverage OxyRequest Capabilities**: Use the full request context
   ```python
   async def context_aware_workflow(oxy_request: OxyRequest):
       # Access memory, call other agents, get trace info
       memory = oxy_request.get_short_memory()
       trace_id = oxy_request.current_trace_id
       
       # Delegate to other agents if needed
       result = await oxy_request.call("other_agent", {"data": "value"})
       return result
   ```

5. **Return Structured Data**: Provide consistent response formats
   ```python
   async def structured_workflow(oxy_request: OxyRequest):
       return {
           "status": "success",
           "data": processed_data,
           "metadata": {"timestamp": datetime.now().isoformat()}
       }
   ```

## Performance Considerations

- **Memory Usage**: WorkflowAgent has minimal overhead
- **Execution Speed**: Direct function execution without additional layers
- **Scalability**: Functions can be as simple or complex as needed
- **Integration**: Full access to OxyGent ecosystem capabilities

## Common Use Cases

- **Legacy System Integration**: Wrap existing functions as agents
- **Data Processing Pipelines**: Multi-step data transformation workflows
- **Business Logic Implementation**: Custom domain-specific processing
- **API Integration**: External service interaction workflows
- **Rapid Prototyping**: Quick agent behavior testing
- **State Machine Implementation**: Complex stateful workflows

## Related Classes

- **[LocalAgent](./local-agent)**: Parent class providing tool and memory management
- **[BaseAgent](./base-agent)**: Foundation class with trace management
- **[ChatAgent](./chat-agent)**: Alternative for conversational workflows

## See Also

- [Agent System Overview](./index)
- [Custom Function Integration](../integration/functions)
- [Workflow Patterns](../patterns/workflows)
- [Error Handling Strategies](../error-handling)
# WorkflowAgent Class

## Overview

The `WorkflowAgent` class provides a flexible way to integrate custom workflow functions into the OxyGent system. It serves as a bridge between the agent framework and user-defined workflow logic, allowing developers to implement custom business logic while leveraging the full OxyGent infrastructure.

## Class Definition

```python
class WorkflowAgent(LocalAgent)
```

**Module**: `oxygent.oxy.agents.workflow_agent`  
**Inherits from**: `LocalAgent`

## Core Attributes

### Workflow Function

- `func_workflow` (Optional[Callable]): The workflow function to execute (default: None)

## Key Features

- **Custom Logic Integration**: Execute any custom Python function within the agent framework
- **Full LocalAgent Capabilities**: Access to all LocalAgent features (tools, memory, LLM integration)
- **Flexible Function Signatures**: Support for various function signatures and return types
- **Error Handling**: Automatic integration with OxyGent error handling and retry mechanisms
- **Data Persistence**: Automatic trace and history management
- **Message Flow**: Integration with frontend messaging system

## Core Method

### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`

Executes the custom workflow function with the provided request.

**Implementation:**

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    return OxyResponse(
        state=OxyState.COMPLETED, 
        output=await self.func_workflow(oxy_request)
    )
```

**Execution Flow:**

1. Receives OxyRequest with arguments and context
2. Calls the custom workflow function with the request
3. Wraps the result in an OxyResponse
4. Returns the response with COMPLETED state

## Usage Examples

### Basic Workflow Agent

```python
from oxygent.oxy.agents.workflow_agent import WorkflowAgent
from oxygent.schemas import OxyRequest

async def simple_calculator(oxy_request: OxyRequest):
    """Simple calculation workflow"""
    expression = oxy_request.arguments.get("expression", "")
    try:
        result = eval(expression)  # Note: Use safely in production
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# Create workflow agent
calc_agent = WorkflowAgent(
    name="calculator_workflow",
    desc="Custom calculator with workflow logic",
    func_workflow=simple_calculator
)

# Usage
response = await oxy_request.call(
    callee="calculator_workflow",
    arguments={"expression": "2 + 3 * 4"}
)
# Returns: "The result of 2 + 3 * 4 is 14"
```

### Data Processing Workflow

```python
import pandas as pd

async def data_analysis_workflow(oxy_request: OxyRequest):
    """Complex data analysis workflow"""
    data_source = oxy_request.arguments.get("data_source")
    analysis_type = oxy_request.arguments.get("analysis_type", "summary")
    
    # Load data
    if data_source.endswith('.csv'):
        df = pd.read_csv(data_source)
    elif data_source.endswith('.json'):
        df = pd.read_json(data_source)
    else:
        return "Unsupported data source format"
    
    # Perform analysis based on type
    if analysis_type == "summary":
        result = {
            "rows": len(df),
            "columns": len(df.columns),
            "summary": df.describe().to_dict()
        }
    elif analysis_type == "correlation":
        result = df.corr().to_dict()
    else:
        result = "Unknown analysis type"
    
    return result

# Create data analysis agent
data_agent = WorkflowAgent(
    name="data_analyzer",
    desc="Custom data analysis workflow agent",
    func_workflow=data_analysis_workflow
)
```

### Multi-Step Business Workflow

```python
async def order_processing_workflow(oxy_request: OxyRequest):
    """E-commerce order processing workflow"""
    order_data = oxy_request.arguments.get("order", {})
    
    steps_completed = []
    
    try:
        # Step 1: Validate order
        if not order_data.get("customer_id") or not order_data.get("items"):
            return {"status": "error", "message": "Invalid order data"}
        steps_completed.append("validation")
        
        # Step 2: Check inventory
        inventory_response = await oxy_request.call(
            callee="inventory_checker",
            arguments={"items": order_data["items"]}
        )
        if inventory_response.output.get("available") != True:
            return {"status": "error", "message": "Items not available"}
        steps_completed.append("inventory_check")
        
        # Step 3: Calculate pricing
        pricing_response = await oxy_request.call(
            callee="price_calculator",
            arguments={
                "items": order_data["items"],
                "customer_id": order_data["customer_id"]
            }
        )
        total_price = pricing_response.output.get("total")
        steps_completed.append("pricing")
        
        # Step 4: Process payment
        payment_response = await oxy_request.call(
            callee="payment_processor",
            arguments={
                "customer_id": order_data["customer_id"],
                "amount": total_price,
                "payment_method": order_data.get("payment_method")
            }
        )
        if payment_response.output.get("status") != "success":
            return {"status": "error", "message": "Payment failed"}
        steps_completed.append("payment")
        
        # Step 5: Create shipment
        shipment_response = await oxy_request.call(
            callee="shipment_creator",
            arguments={
                "order": order_data,
                "payment_id": payment_response.output.get("payment_id")
            }
        )
        steps_completed.append("shipment")
        
        return {
            "status": "success",
            "order_id": shipment_response.output.get("order_id"),
            "tracking_number": shipment_response.output.get("tracking_number"),
            "total_amount": total_price,
            "steps_completed": steps_completed
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "steps_completed": steps_completed
        }

# Create order processing agent
order_agent = WorkflowAgent(
    name="order_processor",
    desc="Complete order processing workflow",
    func_workflow=order_processing_workflow,
    tools=["inventory_checker", "price_calculator", "payment_processor", "shipment_creator"]
)
```

### Conditional Workflow with LLM Integration

```python
async def smart_content_workflow(oxy_request: OxyRequest):
    """Intelligent content processing workflow"""
    content = oxy_request.arguments.get("content", "")
    content_type = oxy_request.arguments.get("type", "unknown")
    
    # Determine content type if not provided
    if content_type == "unknown":
        classification_response = await oxy_request.call(
            callee="content_classifier",
            arguments={"text": content[:500]}  # First 500 chars for classification
        )
        content_type = classification_response.output.get("type", "text")
    
    # Process based on content type
    if content_type == "code":
        # Code analysis workflow
        analysis_response = await oxy_request.call(
            callee="code_analyzer",
            arguments={"code": content}
        )
        
        optimization_response = await oxy_request.call(
            callee="code_optimizer", 
            arguments={
                "code": content,
                "issues": analysis_response.output.get("issues", [])
            }
        )
        
        return {
            "type": "code",
            "analysis": analysis_response.output,
            "optimized_code": optimization_response.output.get("optimized_code"),
            "improvements": optimization_response.output.get("improvements", [])
        }
    
    elif content_type == "article":
        # Article processing workflow
        summary_response = await oxy_request.call(
            callee="text_summarizer",
            arguments={"text": content}
        )
        
        keywords_response = await oxy_request.call(
            callee="keyword_extractor",
            arguments={"text": content}
        )
        
        return {
            "type": "article",
            "summary": summary_response.output,
            "keywords": keywords_response.output.get("keywords", []),
            "word_count": len(content.split())
        }
    
    else:
        # Generic text processing
        return {
            "type": content_type,
            "character_count": len(content),
            "word_count": len(content.split()),
            "processed": True
        }

# Create smart content agent
content_agent = WorkflowAgent(
    name="smart_content_processor",
    desc="Intelligent content processing with conditional logic",
    func_workflow=smart_content_workflow,
    tools=["content_classifier", "code_analyzer", "code_optimizer", 
           "text_summarizer", "keyword_extractor"]
)
```

## Advanced Patterns

### Workflow with State Management

```python
class StatefulWorkflow:
    def __init__(self):
        self.state = {}
    
    async def __call__(self, oxy_request: OxyRequest):
        session_id = oxy_request.arguments.get("session_id", "default")
        action = oxy_request.arguments.get("action", "status")
        
        # Initialize session state if needed
        if session_id not in self.state:
            self.state[session_id] = {
                "step": 0,
                "data": {},
                "completed_steps": []
            }
        
        session_state = self.state[session_id]
        
        if action == "start":
            session_state["step"] = 1
            session_state["data"] = oxy_request.arguments.get("initial_data", {})
            return {"status": "started", "current_step": 1}
        
        elif action == "next":
            return await self._execute_step(oxy_request, session_state)
        
        elif action == "status":
            return {
                "current_step": session_state["step"],
                "completed_steps": session_state["completed_steps"],
                "data": session_state["data"]
            }
        
        elif action == "reset":
            del self.state[session_id]
            return {"status": "reset"}
    
    async def _execute_step(self, oxy_request: OxyRequest, session_state):
        current_step = session_state["step"]
        
        if current_step == 1:
            # Process step 1
            result = await self._step_1_logic(oxy_request, session_state)
            session_state["completed_steps"].append(1)
            session_state["step"] = 2
            return result
        
        elif current_step == 2:
            # Process step 2
            result = await self._step_2_logic(oxy_request, session_state)
            session_state["completed_steps"].append(2)
            session_state["step"] = 3
            return result
        
        else:
            return {"status": "completed", "final_result": session_state["data"]}

# Create stateful workflow agent
stateful_agent = WorkflowAgent(
    name="stateful_processor",
    desc="Workflow with persistent state management",
    func_workflow=StatefulWorkflow()
)
```

### Integration with LocalAgent Features

```python
async def hybrid_workflow(oxy_request: OxyRequest):
    """Workflow that combines custom logic with LocalAgent features"""
    
    # Access conversation history (inherited from LocalAgent)
    short_memory = oxy_request.get_short_memory()
    conversation_context = len(short_memory) > 0
    
    # Get user query
    user_query = oxy_request.get_query()
    
    # Custom business logic
    if conversation_context:
        context_summary = f"Continuing conversation with {len(short_memory)} previous messages"
    else:
        context_summary = "Starting new conversation"
    
    # Use tools (inherited from LocalAgent)
    if "calculate" in user_query.lower():
        calc_response = await oxy_request.call(
            callee="calculator",
            arguments={"expression": extract_expression(user_query)}
        )
        return f"{context_summary}. Calculation result: {calc_response.output}"
    
    elif "search" in user_query.lower():
        search_response = await oxy_request.call(
            callee="web_search",
            arguments={"query": user_query}
        )
        return f"{context_summary}. Search results: {search_response.output}"
    
    else:
        # Use LLM (inherited from LocalAgent)
        llm_response = await oxy_request.call(
            callee="gpt-4",
            arguments={
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_query}
                ]
            }
        )
        return f"{context_summary}. AI response: {llm_response.output}"

def extract_expression(text):
    """Extract mathematical expression from text"""
    import re
    pattern = r'[\d\+\-\*\/\(\)\.\s]+'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "0"

# Create hybrid workflow agent
hybrid_agent = WorkflowAgent(
    name="hybrid_assistant",
    desc="Workflow combining custom logic with LocalAgent features",
    func_workflow=hybrid_workflow,
    llm_model="gpt-4",
    tools=["calculator", "web_search"],
    short_memory_size=10
)
```

## Function Signature Requirements

The workflow function should follow these patterns:

### Async Function (Recommended)

```python
async def my_workflow(oxy_request: OxyRequest):
    # Async workflow logic
    result = await some_async_operation()
    return result
```

### Sync Function (Supported)

```python
def my_workflow(oxy_request: OxyRequest):
    # Synchronous workflow logic
    result = some_sync_operation()
    return result
```

### Return Value Handling

The workflow function can return various types:

- **String**: Direct text response
- **Dict**: Structured data response
- **List**: Array response
- **Custom Objects**: Serializable objects
- **None**: Empty response

## Best Practices

1. **Error Handling**: Implement comprehensive error handling within workflow functions
2. **Resource Management**: Properly manage resources like database connections
3. **Async Operations**: Use async/await for I/O operations
4. **Tool Integration**: Leverage LocalAgent's tool capabilities via `oxy_request.call()`
5. **Memory Usage**: Access conversation history through `oxy_request.get_short_memory()`
6. **State Management**: Consider external state storage for complex workflows
7. **Logging**: Use appropriate logging within workflow functions
8. **Testing**: Unit test workflow functions independently
9. **Documentation**: Document workflow function parameters and return values
10. **Performance**: Optimize for the expected workload and usage patterns

## Common Use Cases

1. **Business Process Automation**: Order processing, approval workflows
2. **Data Pipeline Orchestration**: ETL processes, data validation
3. **Content Processing**: Document analysis, content generation
4. **System Integration**: API orchestration, service coordination
5. **Custom Algorithms**: Specialized computation, analysis workflows
6. **Notification Systems**: Event-driven messaging, alerts
7. **File Processing**: Batch processing, format conversion
8. **Workflow Orchestration**: Multi-step business processes
9. **Custom Analytics**: Specialized reporting, metrics calculation
10. **Integration Bridges**: Legacy system integration, protocol translation

## Error Handling

WorkflowAgent inherits all error handling from LocalAgent:

- Automatic retry logic for transient failures
- Exception logging with trace information
- Graceful degradation for workflow errors
- Integration with the MAS error handling system

## Performance Considerations

- **Async Operations**: Use async functions for better concurrency
- **Resource Pooling**: Share expensive resources across workflow calls
- **Caching**: Implement caching for repeated operations
- **Batch Processing**: Process multiple items together when possible
- **Memory Management**: Be mindful of memory usage in long-running workflows

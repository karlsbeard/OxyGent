# BaseFlow Class

## Overview

The `BaseFlow` class serves as the abstract base class for all flows in the OxyGent system. Flows are specialized Oxy instances that orchestrate complex workflows and coordinate multiple agents or tools.

## Class Definition

```python
class BaseFlow(Oxy)
```

**Module**: `oxygent.oxy.base_flow`  
**Inherits from**: `Oxy`

## Core Attributes

### Flow Configuration
- `is_permission_required` (bool): Whether this flow requires permission (default: True)
- `category` (str): Flow category identifier (default: "agent")
- `is_master` (bool): Whether this flow is a 'MASTER' (central controller) (default: False)

## Abstract Methods

### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`
**Status**: Not implemented (raises `NotImplementedError`)

This method must be overridden by concrete flow implementations to define the specific workflow logic.

**Parameters:**
- `oxy_request` (OxyRequest): The request containing workflow parameters and context

**Returns:**
- `OxyResponse`: The workflow execution result

**Raises:**
- `NotImplementedError`: Always raised in the base class

## Key Differences from Oxy

The BaseFlow class differs from the base Oxy class in the following ways:

1. **Default Permission**: Flows require permission by default (`is_permission_required=True`)
2. **Category**: Flows are categorized as "agent" rather than "tool"
3. **Master Role**: Flows can be designated as master controllers in complex systems

## Usage Pattern

BaseFlow is designed to be subclassed for implementing specific workflow patterns:

```python
from oxygent.oxy.base_flow import BaseFlow
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class MyWorkflow(BaseFlow):
    def __init__(self, **kwargs):
        super().__init__(
            name="my_workflow",
            desc="Custom workflow implementation",
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Implement workflow logic
        # This might involve:
        # 1. Parsing workflow parameters
        # 2. Coordinating multiple agents/tools
        # 3. Managing workflow state
        # 4. Handling branching logic
        # 5. Aggregating results
        
        result = await self.execute_workflow_steps(oxy_request)
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=result,
            extra={"workflow_metadata": self.get_execution_metadata()}
        )
    
    async def execute_workflow_steps(self, oxy_request: OxyRequest):
        # Custom workflow implementation
        pass
```

## Common Flow Implementations

The OxyGent framework provides several concrete flow implementations:

- **Workflow**: Sequential workflow execution
- **PlanAndSolve**: Planning-based execution flow
- **Reflexion**: Self-reflective execution flow
- **ParallelFlow**: Concurrent execution flow

## Integration with MAS

BaseFlow instances are fully integrated with the Multi-Agent System (MAS):

- Inherit all Oxy lifecycle methods and data persistence
- Support for permission management and tool access
- Integration with Elasticsearch for workflow tracking
- Message passing capabilities for frontend communication

## Master Flow Pattern

When `is_master=True`, the flow acts as a central controller:

```python
master_flow = MyWorkflow(
    name="orchestrator",
    desc="Master workflow controller",
    is_master=True,
    is_permission_required=True
)
```

Master flows typically:
- Coordinate multiple sub-workflows
- Manage global workflow state
- Handle complex decision making
- Serve as entry points for complex multi-step processes

## Error Handling

BaseFlow inherits all error handling capabilities from Oxy:
- Automatic retry logic
- Exception logging with trace information
- Graceful failure handling
- Integration with friendly error messages

## Best Practices

1. **Override _execute**: Always implement the `_execute` method in concrete flows
2. **State Management**: Use the `extra` field in OxyResponse for workflow state
3. **Error Propagation**: Let exceptions bubble up for automatic retry handling
4. **Tool Coordination**: Use `oxy_request.call()` for coordinating with other agents/tools
5. **Logging**: Leverage inherited logging capabilities for workflow tracking
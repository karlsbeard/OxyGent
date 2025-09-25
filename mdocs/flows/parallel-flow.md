---
title: "Parallel Flow"
description: "Concurrent execution flow for orchestrating multiple tools and agents simultaneously"
---

# Parallel Flow

The ParallelFlow class enables concurrent execution of multiple tools or agents, distributing the same request across all permitted tools and aggregating their results into a unified response.

## Overview

ParallelFlow is designed for scenarios where you need to execute the same operation across multiple tools or agents simultaneously, then combine their outputs. This pattern is useful for:

- Consensus building across multiple AI models
- Parallel data processing with different tools  
- Comparing outputs from different agents
- Load distribution and redundancy
- Multi-perspective analysis

## Class Definition

```python
from oxygent.oxy.flows import ParallelFlow
```

### Inheritance Hierarchy

```
BaseFlow
└── ParallelFlow
```

## Core Functionality

### _execute(oxy_request: OxyRequest) → OxyResponse

The main execution method that orchestrates concurrent execution across all permitted tools.

**Parameters:**
- `oxy_request` (`OxyRequest`): The request to be distributed to all tools

**Returns:**
- `OxyResponse`: Aggregated response containing outputs from all tools

**Execution Flow:**
1. Distributes the same request to all tools in `permitted_tool_name_list`
2. Executes all requests concurrently using `asyncio.gather`
3. Aggregates all outputs into a single unified response
4. Returns the combined result with `COMPLETED` state

## Usage Examples

### Basic Parallel Execution

```python
from oxygent.oxy.flows import ParallelFlow

# Create parallel flow with multiple AI models
consensus_flow = ParallelFlow(
    name="ai_consensus",
    desc="Get consensus from multiple AI models",
    permitted_tool_name_list=[
        "gpt4_agent",
        "claude_agent", 
        "gemini_agent"
    ]
)

# Execute request across all models
request = OxyRequest(
    callee="ai_consensus",
    arguments={
        "query": "What are the pros and cons of renewable energy?"
    }
)

response = await request.call()
# Output contains responses from all three models
```

### Data Processing Pipeline

```python
# Parallel data processing with different tools
data_processor = ParallelFlow(
    name="parallel_processor",
    desc="Process data with multiple analysis tools",
    permitted_tool_name_list=[
        "statistical_analyzer",
        "ml_processor",
        "visualization_tool"
    ]
)

# Process same dataset with different approaches
request = OxyRequest(
    callee="parallel_processor", 
    arguments={
        "dataset": "sales_data.csv",
        "analysis_type": "comprehensive"
    }
)

response = await request.call()
# Receives statistical analysis, ML insights, and visualizations
```

### Multi-Language Translation

```python
# Translate text using multiple translation services
translation_flow = ParallelFlow(
    name="multi_translator",
    desc="Translate using multiple services for comparison",
    permitted_tool_name_list=[
        "google_translate",
        "deepl_translate", 
        "azure_translate"
    ]
)

request = OxyRequest(
    callee="multi_translator",
    arguments={
        "text": "Hello, how are you today?",
        "target_language": "Spanish"
    }
)

response = await request.call()
# Compare translations from different services
```

### Code Review System

```python
# Parallel code review with multiple reviewers
code_review_flow = ParallelFlow(
    name="code_reviewer",
    desc="Multi-perspective code review",
    permitted_tool_name_list=[
        "security_reviewer",
        "performance_reviewer",
        "style_reviewer", 
        "logic_reviewer"
    ]
)

request = OxyRequest(
    callee="code_reviewer",
    arguments={
        "code": """
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)
        """,
        "language": "python"
    }
)

response = await request.call()
# Get security, performance, style, and logic reviews
```

## Advanced Usage Patterns

### Weighted Consensus Building

```python
async def weighted_consensus_workflow(oxy_request: OxyRequest):
    """Custom workflow that builds weighted consensus from parallel results."""
    
    # Use ParallelFlow for initial processing
    parallel_flow = ParallelFlow(
        permitted_tool_name_list=[
            "expert_agent_1",
            "expert_agent_2", 
            "expert_agent_3"
        ]
    )
    
    # Get all responses
    parallel_response = await parallel_flow._execute(oxy_request)
    
    # Parse individual responses
    responses = parallel_response.output.split("The following are the results from multiple executions:")[1].strip().split("\n")
    
    # Apply weighting logic
    weights = {"expert_agent_1": 0.5, "expert_agent_2": 0.3, "expert_agent_3": 0.2}
    
    # Build weighted consensus (implementation specific to use case)
    consensus = build_weighted_response(responses, weights)
    
    return {
        "individual_responses": responses,
        "weighted_consensus": consensus,
        "confidence_score": calculate_confidence(responses)
    }
```

### Failure Resilience

```python
class ResilientParallelFlow(ParallelFlow):
    """ParallelFlow with failure handling."""
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with failure handling."""
        
        successful_responses = []
        failed_tools = []
        
        # Execute all tools, collecting successes and failures
        for tool_name in self.permitted_tool_name_list:
            try:
                response = await oxy_request.call(
                    callee=tool_name,
                    arguments=oxy_request.arguments
                )
                successful_responses.append(f"[{tool_name}]: {response.output}")
                
            except Exception as e:
                failed_tools.append(f"[{tool_name}]: Failed - {str(e)}")
        
        # Build combined output
        output_parts = []
        
        if successful_responses:
            output_parts.append("Successful executions:")
            output_parts.extend(successful_responses)
        
        if failed_tools:
            output_parts.append("\nFailed executions:")
            output_parts.extend(failed_tools)
        
        return OxyResponse(
            state=OxyState.COMPLETED if successful_responses else OxyState.FAILED,
            output="\n".join(output_parts),
            extra={
                "successful_count": len(successful_responses),
                "failed_count": len(failed_tools),
                "success_rate": len(successful_responses) / len(self.permitted_tool_name_list)
            }
        )
```

### Performance Monitoring

```python
import time
from typing import Dict, List

class MonitoredParallelFlow(ParallelFlow):
    """ParallelFlow with performance monitoring."""
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with performance monitoring."""
        
        start_time = time.time()
        
        # Track individual tool performance
        tool_performance: Dict[str, Dict] = {}
        
        # Execute with timing
        async def timed_execution(tool_name: str):
            tool_start = time.time()
            try:
                response = await oxy_request.call(
                    callee=tool_name,
                    arguments=oxy_request.arguments
                )
                duration = time.time() - tool_start
                tool_performance[tool_name] = {
                    "duration": duration,
                    "status": "success",
                    "output_length": len(response.output)
                }
                return response
                
            except Exception as e:
                duration = time.time() - tool_start
                tool_performance[tool_name] = {
                    "duration": duration,
                    "status": "failed",
                    "error": str(e)
                }
                raise e
        
        # Execute all tools with monitoring
        responses = await asyncio.gather(
            *[timed_execution(tool) for tool in self.permitted_tool_name_list],
            return_exceptions=True
        )
        
        # Filter successful responses
        successful_responses = [
            r for r in responses 
            if not isinstance(r, Exception)
        ]
        
        total_duration = time.time() - start_time
        
        # Build performance report
        performance_report = {
            "total_duration": total_duration,
            "tool_count": len(self.permitted_tool_name_list),
            "successful_count": len(successful_responses),
            "tool_performance": tool_performance,
            "average_tool_duration": sum(
                p["duration"] for p in tool_performance.values()
            ) / len(tool_performance),
            "parallelization_efficiency": (
                max(p["duration"] for p in tool_performance.values()) / total_duration
            ) if tool_performance else 0
        }
        
        # Aggregate outputs
        output = "The following are the results from multiple executions:\n" + \
                "\n".join([res.output for res in successful_responses])
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=output,
            extra={"performance": performance_report}
        )
```

## Integration Patterns

### With Other Flows

```python
from oxygent.oxy.flows import Workflow, ParallelFlow

async def hybrid_workflow(oxy_request: OxyRequest):
    """Combine ParallelFlow with custom workflow logic."""
    
    # Step 1: Use ParallelFlow for initial processing
    parallel_flow = ParallelFlow(
        permitted_tool_name_list=["analyzer_1", "analyzer_2", "analyzer_3"]
    )
    
    parallel_result = await parallel_flow._execute(oxy_request)
    
    # Step 2: Process parallel results with custom logic
    individual_results = parse_parallel_output(parallel_result.output)
    
    # Step 3: Apply business logic
    final_decision = make_decision_from_results(individual_results)
    
    return {
        "parallel_analysis": individual_results,
        "final_decision": final_decision,
        "confidence": calculate_confidence(individual_results)
    }

# Create hybrid flow
hybrid_flow = Workflow(
    name="hybrid_analyzer",
    desc="Parallel analysis with decision logic",
    func_workflow=hybrid_workflow
)
```

### Dynamic Tool Selection

```python
class DynamicParallelFlow(ParallelFlow):
    """ParallelFlow with dynamic tool selection."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tool_selector = kwargs.get("tool_selector")
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with dynamic tool selection."""
        
        # Dynamically select tools based on request
        if self.tool_selector:
            selected_tools = await self.tool_selector(oxy_request)
            # Temporarily override permitted tools
            original_tools = self.permitted_tool_name_list.copy()
            self.permitted_tool_name_list = selected_tools
        
        try:
            # Execute with selected tools
            result = await super()._execute(oxy_request)
            return result
        finally:
            # Restore original tools
            if self.tool_selector:
                self.permitted_tool_name_list = original_tools

async def smart_tool_selector(oxy_request: OxyRequest) -> List[str]:
    """Select tools based on request content."""
    query = oxy_request.get_query().lower()
    
    if "code" in query or "programming" in query:
        return ["code_analyzer", "syntax_checker", "performance_optimizer"]
    elif "translate" in query or "language" in query:
        return ["google_translate", "deepl_translate", "azure_translate"]
    elif "math" in query or "calculate" in query:
        return ["math_solver", "calculator", "statistics_tool"]
    else:
        return ["general_ai_1", "general_ai_2", "general_ai_3"]

# Create dynamic flow
dynamic_flow = DynamicParallelFlow(
    name="smart_parallel",
    desc="Dynamically selects appropriate tools",
    tool_selector=smart_tool_selector
)
```

## Best Practices

### 1. Tool Selection Strategy

```python
# Choose tools that complement each other
complementary_flow = ParallelFlow(
    name="complementary_analysis",
    permitted_tool_name_list=[
        "quantitative_analyzer",  # Numbers and statistics
        "qualitative_analyzer",   # Text and sentiment  
        "visual_analyzer"         # Images and charts
    ]
)
```

### 2. Timeout Handling

```python
import asyncio

class TimeoutParallelFlow(ParallelFlow):
    """ParallelFlow with timeout handling."""
    
    def __init__(self, timeout_seconds: float = 30.0, **kwargs):
        super().__init__(**kwargs)
        self.timeout_seconds = timeout_seconds
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with timeout protection."""
        
        try:
            # Execute with timeout
            responses = await asyncio.wait_for(
                asyncio.gather(*[
                    oxy_request.call(
                        callee=tool_name,
                        arguments=oxy_request.arguments
                    ) for tool_name in self.permitted_tool_name_list
                ]),
                timeout=self.timeout_seconds
            )
            
            # Process successful responses
            output = "The following are the results from multiple executions:\n" + \
                    "\n".join([res.output for res in responses])
            
            return OxyResponse(
                state=OxyState.COMPLETED,
                output=output
            )
            
        except asyncio.TimeoutError:
            return OxyResponse(
                state=OxyState.FAILED,
                output=f"Parallel execution timed out after {self.timeout_seconds} seconds"
            )
```

### 3. Resource Management

```python
import asyncio

class ResourceManagedParallelFlow(ParallelFlow):
    """ParallelFlow with resource management."""
    
    def __init__(self, max_concurrent: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with concurrency limits."""
        
        async def limited_execution(tool_name: str):
            async with self.semaphore:
                return await oxy_request.call(
                    callee=tool_name,
                    arguments=oxy_request.arguments
                )
        
        # Execute with resource limits
        responses = await asyncio.gather(*[
            limited_execution(tool_name) 
            for tool_name in self.permitted_tool_name_list
        ])
        
        output = "The following are the results from multiple executions:\n" + \
                "\n".join([res.output for res in responses])
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=output
        )
```

## Common Use Cases

1. **Multi-Model Consensus**: Get responses from multiple AI models and compare
2. **Parallel Data Processing**: Process data with different algorithms simultaneously  
3. **Load Distribution**: Distribute work across multiple identical tools
4. **A/B Testing**: Compare different versions of tools or models
5. **Redundancy and Reliability**: Execute critical tasks across multiple systems
6. **Multi-Perspective Analysis**: Get different viewpoints on the same problem

## Performance Considerations

- **Concurrency Benefits**: Significant speedup when tools have I/O operations
- **Resource Usage**: Monitor CPU, memory, and network usage with multiple concurrent executions
- **Tool Response Times**: Overall execution time limited by slowest tool
- **Error Handling**: Consider partial success scenarios
- **Output Size**: Aggregated outputs can be large with many tools

## Technical Notes

- Uses `asyncio.gather` for concurrent execution
- All tools receive identical request parameters
- Response aggregation is simple concatenation with headers
- Inherits permission management from BaseFlow
- No built-in result deduplication or filtering
- Exception handling affects all parallel executions

## Related Documentation

- [BaseFlow](/base-flow) - Base class for all flows
- [Workflow](/workflow-flow) - Custom workflow execution
- [PlanAndSolve](/plan-and-solve-flow) - Planning and execution flow  
- [Reflexion](/reflexion-flow) - Iterative improvement flow
- [OxyRequest](/oxy-request) - Request object structure
- [OxyResponse](/oxy-response) - Response object structure
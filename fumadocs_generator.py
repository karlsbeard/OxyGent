#!/usr/bin/env python3
"""
Fumadocs Generator for OxyGent Flows
====================================

This script generates fumadocs-compliant documentation for the oxygent/oxy/flows directory
and related components (agents, llms). It creates a structured documentation directory with
proper meta.json configuration and detailed MDX content based on actual Python code.

Usage:
    python fumadocs_generator.py

Output:
    Creates mdocs-flows-new/ directory with complete fumadocs structure
"""

import ast
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import importlib.util
import sys


class CodeAnalyzer:
    """Analyzes Python code to extract documentation-relevant information."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a Python file and extract relevant information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            info = {
                'path': str(file_path),
                'filename': file_path.name,
                'module_docstring': ast.get_docstring(tree),
                'classes': [],
                'functions': [],
                'imports': [],
                'constants': [],
                'raw_content': content
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._extract_class_info(node)
                    info['classes'].append(class_info)
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):  # Skip private functions
                        func_info = self._extract_function_info(node)
                        info['functions'].append(func_info)
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    import_info = self._extract_import_info(node)
                    info['imports'].extend(import_info)
                elif isinstance(node, ast.Assign):
                    const_info = self._extract_constants(node)
                    if const_info:
                        info['constants'].extend(const_info)
            
            return info
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {'path': str(file_path), 'filename': file_path.name, 'error': str(e)}
    
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Extract information from a class definition."""
        methods = []
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if not item.name.startswith('_') or item.name in ['__init__']:
                    method_info = self._extract_function_info(item)
                    methods.append(method_info)
            elif isinstance(item, ast.AnnAssign) or isinstance(item, ast.Assign):
                attr_info = self._extract_attribute_info(item)
                if attr_info:
                    attributes.extend(attr_info)
        
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'bases': [ast.unparse(base) for base in node.bases],
            'methods': methods,
            'attributes': attributes,
            'decorators': [ast.unparse(d) for d in node.decorator_list]
        }
    
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Extract information from a function definition."""
        args = []
        for arg in node.args.args:
            arg_info = {'name': arg.arg}
            if arg.annotation:
                arg_info['type'] = ast.unparse(arg.annotation)
            args.append(arg_info)
        
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'args': args,
            'return_type': return_type,
            'decorators': [ast.unparse(d) for d in node.decorator_list],
            'is_async': isinstance(node, ast.AsyncFunctionDef)
        }
    
    def _extract_import_info(self, node) -> List[Dict[str, str]]:
        """Extract import information."""
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'type': 'import',
                    'module': alias.name,
                    'alias': alias.asname
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append({
                    'type': 'from_import',
                    'module': module,
                    'name': alias.name,
                    'alias': alias.asname
                })
        return imports
    
    def _extract_constants(self, node: ast.Assign) -> List[Dict[str, Any]]:
        """Extract constant definitions."""
        constants = []
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.isupper():
                try:
                    value = ast.unparse(node.value)
                    constants.append({
                        'name': target.id,
                        'value': value
                    })
                except:
                    pass
        return constants
    
    def _extract_attribute_info(self, node) -> List[Dict[str, Any]]:
        """Extract class attribute information."""
        attributes = []
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            attr_info = {
                'name': node.target.id,
                'type': ast.unparse(node.annotation) if node.annotation else None
            }
            if node.value:
                try:
                    attr_info['default'] = ast.unparse(node.value)
                except:
                    pass
            attributes.append(attr_info)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        attributes.append({
                            'name': target.id,
                            'default': ast.unparse(node.value)
                        })
                    except:
                        pass
        return attributes


class FumadocsGenerator:
    """Generates fumadocs-compliant documentation structure."""
    
    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.analyzer = CodeAnalyzer(source_dir)
        
    def generate_all(self):
        """Generate complete documentation structure."""
        self.output_dir.mkdir(exist_ok=True)
        
        # Generate main index
        self._generate_main_index()
        
        # Generate flows documentation
        flows_dir = self.source_dir / "oxygent" / "oxy" / "flows"
        if flows_dir.exists():
            self._generate_flows_docs(flows_dir)
        
        # Generate agents documentation
        agents_dir = self.source_dir / "oxygent" / "oxy" / "agents"
        if agents_dir.exists():
            self._generate_agents_docs(agents_dir)
        
        # Generate LLMs documentation
        llms_dir = self.source_dir / "oxygent" / "oxy" / "llms"
        if llms_dir.exists():
            self._generate_llms_docs(llms_dir)
        
        # Generate meta.json
        self._generate_meta_json()
        
        print(f"Documentation generated successfully in {self.output_dir}")
    
    def _generate_main_index(self):
        """Generate main index.mdx file."""
        content = """---
title: OxyGent Flows Documentation
description: Comprehensive documentation for OxyGent's flow system, agents, and LLM integrations
---

# OxyGent Flows Documentation

Welcome to the comprehensive documentation for OxyGent's flow system. This documentation covers all aspects of the flow framework including core workflows, agents, and LLM integrations.

## What is OxyGent Flows?

OxyGent Flows is a powerful workflow orchestration framework that enables:

- **Custom Workflows**: Execute user-defined workflow functions
- **Parallel Processing**: Concurrent execution of multiple tools or agents  
- **Plan-and-Solve**: Advanced planning and execution strategies
- **Reflexion**: Self-reflective reasoning capabilities
- **Agent Integration**: Seamless integration with various AI agents
- **LLM Support**: Multiple LLM provider integrations

## Getting Started

Choose a section below to explore:

<Cards>
  <Card title="Flows" href="/flows" icon="workflow">
    Core workflow execution engines and strategies
  </Card>
  <Card title="Agents" href="/agents" icon="robot"> 
    AI agents for different use cases and environments
  </Card>
  <Card title="LLMs" href="/llms" icon="brain">
    Language model integrations and configurations
  </Card>
</Cards>

## Architecture Overview

The OxyGent flow system is built around these core concepts:

### BaseFlow
All flows inherit from `BaseFlow` and implement the `_execute` method to define their specific execution logic.

### OxyRequest/OxyResponse
Standardized request/response objects that flow through the system, enabling consistent communication between components.

### Tool Orchestration
Flows can orchestrate multiple tools, agents, or other flows through the permitted tool system.

## Key Features

- **Asynchronous Execution**: Built for high-performance async operations
- **Type Safety**: Comprehensive type hints and Pydantic models
- **Extensibility**: Easy to extend with custom flows and agents
- **Error Handling**: Robust error handling and state management
- **Logging**: Comprehensive logging for debugging and monitoring
"""

        self._write_file(self.output_dir / "index.mdx", content)
    
    def _generate_flows_docs(self, flows_dir: Path):
        """Generate flows documentation."""
        flows_output_dir = self.output_dir / "flows"
        flows_output_dir.mkdir(exist_ok=True)
        
        # Generate flows index
        flows_index = """---
title: Flows
description: Core workflow execution engines and orchestration strategies
---

# Flows

OxyGent flows are the core execution engines that orchestrate complex workflows. Each flow type serves specific use cases and execution patterns.

## Available Flows

<Cards>
  <Card title="Workflow" href="/flows/workflow" icon="play">
    Execute custom workflow functions with full flexibility
  </Card>
  <Card title="Parallel Flow" href="/flows/parallel-flow" icon="parallel">
    Concurrent execution of multiple tools or agents
  </Card>
  <Card title="Plan and Solve" href="/flows/plan-and-solve" icon="strategy">
    Advanced planning and step-by-step execution strategy
  </Card>
  <Card title="Reflexion" href="/flows/reflexion" icon="reflect">
    Self-reflective reasoning and iterative improvement
  </Card>
</Cards>

## Base Flow Architecture

All flows inherit from the `BaseFlow` class and implement the `_execute` method:

```python
from oxygent.schemas import OxyRequest, OxyResponse
from oxygent.oxy.base_flow import BaseFlow

class CustomFlow(BaseFlow):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom execution logic
        return OxyResponse(...)
```

## Common Patterns

### Tool Orchestration
Flows can orchestrate multiple tools through the permitted tool system:

```python
# Add tools to the permitted list
self.add_permitted_tools(["tool1", "tool2"])

# Call tools during execution
response = await oxy_request.call(
    callee="tool1", 
    arguments={"param": "value"}
)
```

### State Management
Flows track execution state through the `OxyState` enum:

- `PENDING`: Flow is ready to execute
- `IN_PROGRESS`: Flow is currently executing  
- `COMPLETED`: Flow has completed successfully
- `FAILED`: Flow encountered an error

### Error Handling
Flows should handle errors gracefully and return appropriate response states:

```python
try:
    result = await some_operation()
    return OxyResponse(state=OxyState.COMPLETED, output=result)
except Exception as e:
    logger.error(f"Flow execution failed: {e}")
    return OxyResponse(state=OxyState.FAILED, output=str(e))
```
"""
        
        self._write_file(flows_output_dir / "index.mdx", flows_index)
        
        # Generate individual flow documentation
        for py_file in flows_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            
            file_info = self.analyzer.parse_file(py_file)
            if 'error' in file_info:
                continue
                
            flow_name = py_file.stem
            if flow_name == "workflow":
                self._generate_workflow_doc(flows_output_dir, file_info)
            elif flow_name == "parallel_flow":
                self._generate_parallel_flow_doc(flows_output_dir, file_info)
            elif flow_name == "plan_and_solve":
                self._generate_plan_and_solve_doc(flows_output_dir, file_info)
            elif flow_name == "reflexion":
                self._generate_reflexion_doc(flows_output_dir, file_info)
    
    def _generate_workflow_doc(self, output_dir: Path, file_info: Dict):
        """Generate workflow-specific documentation."""
        content = f"""---
title: Workflow
description: Execute custom workflow functions with full flexibility
---

# Workflow

{file_info.get('module_docstring', 'Custom workflow execution flow.')}

## Overview

The Workflow flow serves as a bridge between the OxyGent flow framework and user-defined workflow logic. It enables execution of custom workflow functions within the structured flow system.

## Class Definition

```python
class Workflow(BaseFlow):
    \"\"\"Flow that executes custom workflow functions.\"\"\"
    
    func_workflow: Optional[Callable] = Field(None, exclude=True, description="")
```

## Usage

### Basic Usage

```python
from oxygent.oxy.flows import Workflow
from oxygent.schemas import OxyRequest, OxyResponse

# Define a custom workflow function
async def my_workflow(request: OxyRequest) -> str:
    # Custom workflow logic
    return f"Processed: {{request.get_query()}}"

# Create and configure the workflow
workflow = Workflow(func_workflow=my_workflow)

# Execute the workflow
request = OxyRequest(query="Hello, World!")
response = await workflow._execute(request)
print(response.output)  # Processed: Hello, World!
```

### Advanced Usage with Tool Integration

```python
async def advanced_workflow(request: OxyRequest) -> str:
    # Access tools through the request
    tool_response = await request.call(
        callee="some_tool",
        arguments={{"input": request.get_query()}}
    )
    
    # Process the tool response
    result = f"Tool output: {{tool_response.output}}"
    return result

workflow = Workflow(func_workflow=advanced_workflow)
```

## Key Features

- **Flexibility**: Execute any custom workflow function
- **Integration**: Seamless integration with the flow framework
- **Async Support**: Full support for asynchronous operations
- **Tool Access**: Access to all permitted tools through OxyRequest

## Configuration

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `func_workflow` | `Optional[Callable]` | The custom workflow function to execute | `None` |

## Implementation Details

The Workflow flow is intentionally simple - it delegates all execution logic to the provided workflow function:

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    return OxyResponse(
        state=OxyState.COMPLETED, 
        output=await self.func_workflow(oxy_request)
    )
```

## Best Practices

1. **Error Handling**: Implement proper error handling in your workflow function
2. **Type Hints**: Use proper type hints for better IDE support
3. **Documentation**: Document your workflow functions clearly
4. **Testing**: Write unit tests for your workflow functions

### Example with Error Handling

```python
async def robust_workflow(request: OxyRequest) -> str:
    try:
        # Your workflow logic here
        result = process_request(request)
        return result
    except Exception as e:
        logger.error(f"Workflow error: {{e}}")
        raise  # Re-raise to let the flow handle it
```

## Related Flows

- [Parallel Flow](/flows/parallel-flow): For concurrent execution
- [Plan and Solve](/flows/plan-and-solve): For structured planning workflows
"""
        
        self._write_file(output_dir / "workflow.mdx", content)
    
    def _generate_parallel_flow_doc(self, output_dir: Path, file_info: Dict):
        """Generate parallel flow documentation."""
        content = f"""---
title: Parallel Flow  
description: Concurrent execution of multiple tools or agents with result aggregation
---

# Parallel Flow

{file_info.get('module_docstring', 'Parallel execution flow for concurrent operations.')}

## Overview

The ParallelFlow executes the same request across multiple tools or agents concurrently and aggregates their results into a unified response. This is ideal for scenarios where you want to:

- Compare outputs from different agents
- Gather multiple perspectives on the same problem
- Implement consensus mechanisms
- Improve reliability through redundancy

## Class Definition

```python
class ParallelFlow(BaseFlow):
    \"\"\"Flow that executes multiple tools or agents concurrently.\"\"\"
```

## Usage

### Basic Setup

```python
from oxygent.oxy.flows import ParallelFlow
from oxygent.schemas import OxyRequest

# Create a parallel flow
parallel_flow = ParallelFlow()

# Add multiple tools to execute in parallel
parallel_flow.add_permitted_tools([
    "agent1", 
    "agent2", 
    "agent3",
    "llm_model_a",
    "llm_model_b"
])

# Execute the request across all tools
request = OxyRequest(query="Analyze this data")
response = await parallel_flow._execute(request)
```

### Example Output

When executed, the ParallelFlow aggregates all responses:

```
The following are the results from multiple executions:
Agent1 Response: Data shows increasing trend...
Agent2 Response: Statistical analysis reveals...  
Agent3 Response: Pattern recognition indicates...
LLM Model A Response: Based on the data...
LLM Model B Response: The analysis suggests...
```

## Execution Flow

1. **Distribution**: The same `OxyRequest` is sent to all tools in `permitted_tool_name_list`
2. **Concurrent Execution**: All tools execute simultaneously using `asyncio.gather`
3. **Aggregation**: Results are combined into a single response string
4. **Return**: Unified response with `OxyState.COMPLETED`

## Implementation Details

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    # Execute the same request concurrently across all permitted tools
    oxy_responses = await asyncio.gather(
        *[
            oxy_request.call(
                callee=permitted_tool_name, 
                arguments=oxy_request.arguments
            )
            for permitted_tool_name in self.permitted_tool_name_list
        ]
    )

    # Aggregate all outputs into a single response
    oxy_response = OxyResponse(
        state=OxyState.COMPLETED,
        output="The following are the results from multiple executions:"
        + "\\n".join([res.output for res in oxy_responses]),
    )
    return oxy_response
```

## Use Cases

### Multi-Agent Consensus

```python
# Set up agents for consensus
consensus_flow = ParallelFlow()
consensus_flow.add_permitted_tools([
    "expert_agent_1",
    "expert_agent_2", 
    "expert_agent_3"
])

# Get multiple expert opinions
request = OxyRequest(query="Should we invest in this technology?")
response = await consensus_flow._execute(request)
# Response contains all expert opinions for comparison
```

### Model Comparison

```python
# Compare different LLM models
comparison_flow = ParallelFlow()
comparison_flow.add_permitted_tools([
    "gpt4_model",
    "claude_model",
    "gemini_model"
])

request = OxyRequest(query="Explain quantum computing")
response = await comparison_flow._execute(request)
# Compare how different models explain the same concept
```

### Redundant Processing

```python
# Ensure reliability through redundancy
redundant_flow = ParallelFlow()
redundant_flow.add_permitted_tools([
    "primary_processor",
    "backup_processor_1",
    "backup_processor_2"
])

request = OxyRequest(query="Process critical data")
response = await redundant_flow._execute(request)
# Get multiple processing results for verification
```

## Performance Considerations

- **Concurrency**: All tools execute simultaneously, reducing total execution time
- **Resource Usage**: Higher resource consumption due to parallel execution
- **Error Handling**: If one tool fails, others continue (using `asyncio.gather`)
- **Timeout**: Individual tool timeouts don't affect other executions

## Configuration Tips

1. **Tool Selection**: Choose tools that provide valuable different perspectives
2. **Performance Balance**: Consider the trade-off between speed and resource usage
3. **Error Resilience**: Ensure individual tool failures don't break the entire flow
4. **Result Processing**: Consider post-processing to analyze aggregated results

## Custom Result Processing

You can extend ParallelFlow to implement custom result aggregation:

```python
class CustomParallelFlow(ParallelFlow):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Get parallel results
        responses = await asyncio.gather(
            *[oxy_request.call(callee=tool, arguments=oxy_request.arguments)
              for tool in self.permitted_tool_name_list]
        )
        
        # Custom aggregation logic
        processed_results = self.custom_aggregation(responses)
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=processed_results
        )
    
    def custom_aggregation(self, responses):
        # Implement your custom logic here
        # e.g., voting, averaging, consensus detection
        pass
```

## Related Flows

- [Workflow](/flows/workflow): For custom sequential logic
- [Plan and Solve](/flows/plan-and-solve): For structured planning approaches
"""
        
        self._write_file(output_dir / "parallel-flow.mdx", content)
    
    def _generate_plan_and_solve_doc(self, output_dir: Path, file_info: Dict):
        """Generate plan and solve documentation."""
        content = f"""---
title: Plan and Solve
description: Advanced planning and step-by-step execution strategy with optional replanning
---

# Plan and Solve

{file_info.get('module_docstring', 'Plan-and-Solve Prompting Workflow.')}

## Overview

The PlanAndSolve flow implements a sophisticated planning and execution strategy where:

1. **Planning Phase**: A planner agent creates a step-by-step plan
2. **Execution Phase**: An executor agent executes each step sequentially  
3. **Replanning Phase** (optional): A replanner agent updates the plan based on execution results

This approach is particularly effective for complex, multi-step problems that benefit from structured decomposition and adaptive planning.

## Class Definition

```python
class PlanAndSolve(BaseFlow):
    \"\"\"Plan-and-Solve Prompting Workflow.\"\"\"
    
    max_replan_rounds: int = Field(30, description="Maximum retries for operations.")
    planner_agent_name: str = Field("planner_agent", description="planner agent name")
    pre_plan_steps: List[str] = Field(None, description="pre plan steps")
    enable_replanner: bool = Field(False, description="enable replanner")
    executor_agent_name: str = Field("executor_agent", description="executor agent name")
    llm_model: str = Field("default_llm", description="LLM model name for fallback")
```

## Usage

### Basic Configuration

```python
from oxygent.oxy.flows import PlanAndSolve
from oxygent.schemas import OxyRequest

# Create and configure the flow
plan_solve = PlanAndSolve(
    planner_agent_name="my_planner",
    executor_agent_name="my_executor", 
    max_replan_rounds=10,
    enable_replanner=True
)

# Execute with a complex query
request = OxyRequest(query="Create a comprehensive marketing strategy for a new product")
response = await plan_solve._execute(request)
```

### With Pre-defined Steps

```python
# Use pre-defined plan steps
predefined_steps = [
    "Analyze the target market",
    "Research competitor strategies", 
    "Define unique value proposition",
    "Create marketing channels plan",
    "Set budget and timeline"
]

plan_solve = PlanAndSolve(
    pre_plan_steps=predefined_steps,
    executor_agent_name="marketing_executor"
)
```

### Advanced Configuration with Custom Parsers

```python
from oxygent.utils.llm_pydantic_parser import PydanticOutputParser

# Custom plan structure
class CustomPlan(BaseModel):
    title: str = Field(description="Plan title")
    steps: List[str] = Field(description="Execution steps")
    priority: int = Field(description="Priority level")

# Configure with custom parser
plan_solve = PlanAndSolve(
    pydantic_parser_planner=PydanticOutputParser(output_cls=CustomPlan),
    enable_replanner=True
)
```

## Execution Flow

### Phase 1: Planning

If no pre-plan steps are provided, the planner agent creates a plan:

```python
# Planner receives the original query
query = "How can I improve my website's SEO?"

# Planner generates structured plan
plan_response = await planner_agent(query)
# Example output:
# 1. Analyze current website SEO performance
# 2. Research relevant keywords and competition  
# 3. Optimize on-page elements (meta tags, headers, content)
# 4. Improve technical SEO (site speed, mobile-friendliness)
# 5. Build high-quality backlinks
```

### Phase 2: Sequential Execution

Each plan step is executed by the executor agent:

```python
for step in plan_steps:
    task_formatted = f'''
    We have finished the following steps: {{past_steps}}
    The current step to execute is: {{step}}
    You should only execute the current step, and do not execute other steps.
    '''
    
    result = await executor_agent(task_formatted)
    past_steps += f"task: {{step}}, result: {{result.output}}"
```

### Phase 3: Replanning (Optional)

If enabled, the replanner evaluates progress and updates the plan:

```python
replanner_query = f'''
The target of user is: {{original_query}}
The origin plan is: {{plan}}
We have finished the following steps: {{past_steps}}

Please update the plan considering the mentioned information.
If no more operation is supposed, use Response to answer the user.
Otherwise, please update the plan.
'''

updated_plan = await replanner_agent(replanner_query)
```

## Configuration Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `max_replan_rounds` | `int` | Maximum execution rounds | `30` |
| `planner_agent_name` | `str` | Name of the planning agent | `"planner_agent"` |
| `executor_agent_name` | `str` | Name of the execution agent | `"executor_agent"` |
| `pre_plan_steps` | `List[str]` | Pre-defined plan steps | `None` |
| `enable_replanner` | `bool` | Enable adaptive replanning | `False` |
| `llm_model` | `str` | Fallback LLM model | `"default_llm"` |

## Pydantic Models

The flow uses structured models for parsing responses:

### Plan Model

```python
class Plan(BaseModel):
    \"\"\"Plan to follow in future.\"\"\"
    
    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )
```

### Action Model (for Replanning)

```python
class Action(BaseModel):
    \"\"\"Action to perform.\"\"\"
    
    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )
```

## Use Cases

### Project Management

```python
project_planner = PlanAndSolve(
    planner_agent_name="project_planner",
    executor_agent_name="task_executor",
    enable_replanner=True,
    max_replan_rounds=20
)

request = OxyRequest(query="Plan and execute a software development project")
response = await project_planner._execute(request)
```

### Research Tasks

```python
research_flow = PlanAndSolve(
    planner_agent_name="research_planner", 
    executor_agent_name="research_executor",
    enable_replanner=True
)

request = OxyRequest(query="Research the impact of AI on healthcare")
response = await research_flow._execute(request)
```

### Problem Solving

```python
problem_solver = PlanAndSolve(
    pre_plan_steps=[
        "Identify the core problem",
        "Gather relevant information", 
        "Generate potential solutions",
        "Evaluate and select best solution",
        "Implement the solution"
    ],
    executor_agent_name="problem_executor"
)
```

## Best Practices

### 1. Agent Specialization

- **Planner**: Should be optimized for strategic thinking and decomposition
- **Executor**: Should be optimized for task execution and tool usage
- **Replanner**: Should be optimized for evaluation and adaptation

### 2. Step Granularity

- Make steps specific and actionable
- Avoid steps that are too broad or too narrow
- Consider dependencies between steps

### 3. Error Handling

```python
class RobustPlanAndSolve(PlanAndSolve):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        try:
            return await super()._execute(oxy_request)
        except Exception as e:
            logger.error(f"Plan and solve execution failed: {{e}}")
            return OxyResponse(
                state=OxyState.FAILED,
                output=f"Execution failed: {{str(e)}}"
            )
```

### 4. Progress Tracking

Monitor execution progress through logging:

```python
logger.info(f"Starting plan execution for: {{original_query}}")
logger.info(f"Generated plan with {{len(plan_steps)}} steps")
logger.info(f"Executing step {{current_step}}: {{step}}")
logger.info(f"Completed execution with final result: {{final_output}}")
```

## Advanced Features

### Custom Response Parsing

```python
def custom_planner_parser(response: str) -> Plan:
    # Custom parsing logic
    lines = response.strip().split('\n')
    steps = [line.strip('123456789. ') for line in lines if line.strip()]
    return Plan(steps=steps)

plan_solve = PlanAndSolve(
    func_parse_planner_response=custom_planner_parser
)
```

### Conditional Replanning

```python
class ConditionalPlanAndSolve(PlanAndSolve):
    def should_replan(self, past_steps: str, remaining_steps: List[str]) -> bool:
        # Custom logic to determine if replanning is needed
        if "error" in past_steps.lower():
            return True
        if len(remaining_steps) > 10:
            return True
        return False
```

## Performance Considerations

- **Planning Overhead**: Initial planning takes time but improves execution efficiency
- **Sequential Execution**: Steps execute sequentially, not in parallel
- **Replanning Cost**: Adaptive replanning adds computational overhead
- **Agent Performance**: Overall performance depends on the quality of planner/executor agents

## Related Flows

- [Workflow](/flows/workflow): For custom sequential workflows
- [Parallel Flow](/flows/parallel-flow): For concurrent execution
- [Reflexion](/flows/reflexion): For self-reflective reasoning
"""
        
        self._write_file(output_dir / "plan-and-solve.mdx", content)
    
    def _generate_reflexion_doc(self, output_dir: Path, file_info: Dict):
        """Generate reflexion flow documentation.""" 
        reflexion_classes = [cls for cls in file_info.get('classes', []) if 'reflexion' in cls['name'].lower()]
        
        content = f"""---
title: Reflexion
description: Self-reflective reasoning and iterative improvement flows
---

# Reflexion

{file_info.get('module_docstring', 'Reflexion flows for self-reflective reasoning.')}

## Overview

The Reflexion flows implement self-reflective reasoning patterns where the system can:

- Reflect on its own outputs and reasoning
- Iteratively improve responses through self-criticism
- Learn from mistakes and adjust strategies
- Implement sophisticated reasoning loops

## Available Reflexion Flows

"""

        # Add documentation for each Reflexion class found
        for cls_info in reflexion_classes:
            class_name = cls_info['name']
            docstring = cls_info.get('docstring', f'The {class_name} flow.')
            
            content += f"""
### {class_name}

{docstring}

#### Class Definition

```python
class {class_name}(BaseFlow):
"""
            
            # Add attributes if available
            if cls_info.get('attributes'):
                content += "    # Configuration attributes:\n"
                for attr in cls_info['attributes']:
                    attr_name = attr['name']
                    attr_type = attr.get('type', 'Any')
                    attr_default = attr.get('default', '')
                    content += f"    {attr_name}: {attr_type}"
                    if attr_default:
                        content += f" = {attr_default}"
                    content += "\n"
            
            content += "```\n"
            
            # Add methods documentation
            if cls_info.get('methods'):
                content += "\n#### Key Methods\n\n"
                for method in cls_info['methods']:
                    if method['name'] in ['__init__', '_execute']:
                        method_name = method['name']
                        method_doc = method.get('docstring', f'{method_name} method')
                        content += f"**{method_name}**\n{method_doc}\n\n"

        # Add general usage examples
        content += """
## Usage Patterns

### Basic Reflexion Loop

```python
from oxygent.oxy.flows import Reflexion
from oxygent.schemas import OxyRequest

# Create reflexion flow
reflexion_flow = Reflexion()

# Configure for iterative improvement
request = OxyRequest(query="Solve this complex problem step by step")
response = await reflexion_flow._execute(request)
```

### Mathematical Reflexion

```python
from oxygent.oxy.flows import MathReflexion

# Specialized for mathematical reasoning
math_flow = MathReflexion()

request = OxyRequest(query="Prove that the square root of 2 is irrational")
response = await math_flow._execute(request)
```

## Core Concepts

### Self-Reflection Loop

1. **Initial Response**: Generate an initial response to the query
2. **Self-Criticism**: Analyze the response for potential issues
3. **Improvement**: Generate an improved response based on the criticism
4. **Iteration**: Repeat the process until satisfactory or max iterations reached

### Reflection Strategies

#### Error Detection
- Identify logical inconsistencies
- Spot computational errors
- Recognize incomplete reasoning

#### Quality Assessment  
- Evaluate response completeness
- Check reasoning validity
- Assess evidence quality

#### Iterative Improvement
- Refine arguments based on reflection
- Add missing information
- Correct identified errors

## Configuration Options

Common configuration parameters for reflexion flows:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `max_iterations` | `int` | Maximum reflection iterations | `3` |
| `reflection_threshold` | `float` | Quality threshold for stopping | `0.8` |
| `critic_agent_name` | `str` | Name of critic agent | `"critic"` |
| `improver_agent_name` | `str` | Name of improver agent | `"improver"` |

## Example Implementation

```python
class CustomReflexion(BaseFlow):
    max_iterations: int = 3
    quality_threshold: float = 0.8
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        current_response = await self.initial_response(oxy_request)
        
        for iteration in range(self.max_iterations):
            # Get self-criticism
            criticism = await self.reflect_on_response(
                oxy_request, current_response
            )
            
            # Check if improvement is needed
            if self.is_satisfactory(criticism):
                break
                
            # Improve the response
            current_response = await self.improve_response(
                oxy_request, current_response, criticism
            )
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=current_response
        )
    
    async def initial_response(self, request: OxyRequest) -> str:
        # Generate initial response
        pass
    
    async def reflect_on_response(self, request: OxyRequest, response: str) -> str:
        # Self-criticism logic
        pass
    
    async def improve_response(self, request: OxyRequest, response: str, criticism: str) -> str:
        # Improvement logic
        pass
    
    def is_satisfactory(self, criticism: str) -> bool:
        # Quality assessment logic
        pass
```

## Use Cases

### Academic Writing

```python
# Iteratively improve academic arguments
academic_reflexion = Reflexion(
    critic_agent_name="academic_critic",
    improver_agent_name="academic_writer"
)

request = OxyRequest(query="Write a literature review on machine learning")
response = await academic_reflexion._execute(request)
```

### Code Review and Improvement

```python
# Self-reviewing code solutions
code_reflexion = Reflexion(
    critic_agent_name="code_reviewer", 
    improver_agent_name="code_improver"
)

request = OxyRequest(query="Implement a binary search algorithm")
response = await code_reflexion._execute(request)
```

### Mathematical Problem Solving

```python
# Mathematical reasoning with self-correction
math_reflexion = MathReflexion()

request = OxyRequest(query="Solve this calculus problem with detailed steps")
response = await math_reflexion._execute(request)
```

## Best Practices

### 1. Effective Criticism

- Focus on specific, actionable feedback
- Identify concrete improvement areas
- Avoid overly harsh or vague criticism

### 2. Quality Metrics

```python
def assess_response_quality(response: str, criteria: Dict[str, float]) -> float:
    \"\"\"Assess response quality against multiple criteria.\"\"\"
    scores = []
    
    # Completeness score
    if criteria.get("completeness"):
        scores.append(assess_completeness(response))
    
    # Accuracy score  
    if criteria.get("accuracy"):
        scores.append(assess_accuracy(response))
    
    # Clarity score
    if criteria.get("clarity"):
        scores.append(assess_clarity(response))
    
    return sum(scores) / len(scores) if scores else 0.0
```

### 3. Stopping Conditions

- Set reasonable iteration limits
- Use quality thresholds appropriately
- Implement early stopping for satisfactory responses

### 4. Agent Specialization

- **Critic Agent**: Trained for identifying flaws and areas for improvement
- **Improver Agent**: Trained for generating better versions based on feedback

## Performance Considerations

- **Computational Cost**: Multiple iterations increase processing time
- **Quality vs Speed**: Balance improvement quality with execution speed  
- **Convergence**: Ensure iterations lead to meaningful improvements
- **Resource Usage**: Monitor memory and computational resource consumption

## Advanced Techniques

### Multi-Aspect Reflection

```python
class MultiAspectReflexion(Reflexion):
    reflection_aspects = ["accuracy", "completeness", "clarity", "creativity"]
    
    async def comprehensive_reflection(self, response: str) -> Dict[str, str]:
        reflections = {}
        for aspect in self.reflection_aspects:
            criticism = await self.aspect_specific_criticism(response, aspect)
            reflections[aspect] = criticism
        return reflections
```

### Confidence-Based Iteration

```python
class ConfidenceBasedReflexion(Reflexion):
    async def should_continue_reflecting(self, response: str, iteration: int) -> bool:
        confidence = await self.assess_confidence(response)
        return confidence < self.confidence_threshold and iteration < self.max_iterations
```

## Related Flows

- [Plan and Solve](/flows/plan-and-solve): For structured planning with potential replanning
- [Workflow](/flows/workflow): For custom sequential workflows
"""
        
        self._write_file(output_dir / "reflexion.mdx", content)
    
    def _generate_agents_docs(self, agents_dir: Path):
        """Generate agents documentation."""
        agents_output_dir = self.output_dir / "agents"
        agents_output_dir.mkdir(exist_ok=True)
        
        # Generate agents index
        agents_index = """---
title: Agents
description: AI agents for different use cases and environments
---

# Agents

OxyGent agents are specialized AI components designed for specific use cases and environments. Each agent type offers unique capabilities and integration patterns.

## Available Agents

<Cards>
  <Card title="Base Agent" href="/agents/base-agent" icon="foundation">
    Foundation class for all OxyGent agents
  </Card>
  <Card title="React Agent" href="/agents/react-agent" icon="react">
    Reasoning and Acting agent with tool integration
  </Card>
  <Card title="Chat Agent" href="/agents/chat-agent" icon="chat">
    Conversational agent for interactive dialogues
  </Card>
  <Card title="Local Agent" href="/agents/local-agent" icon="local">
    Local execution agent for on-premise operations
  </Card>
  <Card title="Remote Agent" href="/agents/remote-agent" icon="cloud">
    Remote execution agent for distributed operations
  </Card>
  <Card title="Parallel Agent" href="/agents/parallel-agent" icon="parallel">
    Multi-threaded agent for concurrent processing
  </Card>
  <Card title="Workflow Agent" href="/agents/workflow-agent" icon="workflow">
    Agent specialized for workflow orchestration
  </Card>
  <Card title="SSE Oxy Agent" href="/agents/sse-oxy-agent" icon="stream">
    Server-sent events agent for real-time streaming
  </Card>
</Cards>

## Agent Architecture

All agents inherit from the `BaseAgent` class and follow common patterns:

```python
from oxygent.oxy.agents import BaseAgent
from oxygent.schemas import OxyRequest, OxyResponse

class CustomAgent(BaseAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom agent logic
        return OxyResponse(...)
```

## Common Features

- **Async Operations**: All agents support asynchronous execution
- **Type Safety**: Comprehensive type hints and Pydantic models  
- **Tool Integration**: Seamless integration with external tools
- **State Management**: Built-in state tracking and error handling
- **Logging**: Comprehensive logging for debugging and monitoring
"""
        
        self._write_file(agents_output_dir / "index.mdx", agents_index)
        
        # Generate individual agent docs (simplified for brevity)
        for py_file in agents_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            file_info = self.analyzer.parse_file(py_file)
            if 'error' in file_info:
                continue
                
            agent_name = py_file.stem.replace('_', '-')
            self._generate_agent_doc(agents_output_dir, agent_name, file_info)
    
    def _generate_agent_doc(self, output_dir: Path, agent_name: str, file_info: Dict):
        """Generate documentation for a specific agent."""
        title = agent_name.replace('-', ' ').title()
        
        content = f"""---
title: {title}
description: {file_info.get('module_docstring', f'{title} agent documentation')}
---

# {title}

{file_info.get('module_docstring', f'Documentation for the {title} agent.')}

## Overview

The {title} provides specialized functionality for specific use cases within the OxyGent system.

"""
        
        # Add class information
        for cls_info in file_info.get('classes', []):
            if 'agent' in cls_info['name'].lower():
                content += f"""
## Class Definition

```python
class {cls_info['name']}(BaseAgent):
    \"\"\"{cls_info.get('docstring', f'{cls_info["name"]} implementation.')}\"\"\"""
                
                # Add attributes
                if cls_info.get('attributes'):
                    content += "\n    # Configuration attributes:\n"
                    for attr in cls_info['attributes']:
                        attr_name = attr['name']
                        attr_type = attr.get('type', 'Any')
                        content += f"    {attr_name}: {attr_type}\n"
                
                content += "```\n"
                
                # Add methods
                if cls_info.get('methods'):
                    content += "\n## Key Methods\n\n"
                    for method in cls_info['methods']:
                        if not method['name'].startswith('_') or method['name'] in ['__init__', '_execute']:
                            content += f"### {method['name']}\n\n"
                            if method.get('docstring'):
                                content += f"{method['docstring']}\n\n"
                            
                            # Add method signature
                            args_str = ", ".join([f"{arg['name']}: {arg.get('type', 'Any')}" for arg in method.get('args', [])])
                            return_type = method.get('return_type', 'Any')
                            async_prefix = "async " if method.get('is_async') else ""
                            
                            content += f"```python\n{async_prefix}def {method['name']}({args_str}) -> {return_type}:\n    ...\n```\n\n"
        
        # Get the main class name
        main_class_name = 'Agent'
        if file_info.get('classes'):
            main_class_name = file_info['classes'][0].get('name', 'Agent')
        
        content += "\n## Usage Example\n\n"
        content += "```python\n"
        content += f"from oxygent.oxy.agents import {main_class_name}\n"
        content += "from oxygent.schemas import OxyRequest\n\n"
        content += "# Create and configure the agent\n"
        content += f"agent = {main_class_name}()\n\n"
        content += "# Execute a request\n"
        content += 'request = OxyRequest(query="Your query here")\n'
        content += "response = await agent._execute(request)\n"
        content += "print(response.output)\n"
        content += "```\n\n"
        content += "## Configuration

Refer to the class attributes above for configuration options.

## Best Practices

1. **Error Handling**: Implement proper error handling for robust operation
2. **Resource Management**: Monitor resource usage for optimal performance  
3. **Logging**: Use appropriate logging levels for debugging
4. **Testing**: Write comprehensive tests for agent functionality

## Related Components

- [Base Agent](/agents/base-agent): Foundation class for all agents
- [Flows](/flows): Workflow orchestration components
"""
        
        self._write_file(output_dir / f"{agent_name}.mdx", content)
    
    def _generate_llms_docs(self, llms_dir: Path):
        """Generate LLMs documentation."""
        llms_output_dir = self.output_dir / "llms"  
        llms_output_dir.mkdir(exist_ok=True)
        
        # Generate LLMs index
        llms_index = """---
title: LLMs
description: Language model integrations and configurations
---

# LLMs

OxyGent provides comprehensive support for various Large Language Model (LLM) providers and configurations. The LLM system is designed to be flexible, extensible, and easy to integrate.

## Available LLM Integrations

<Cards>
  <Card title="Base LLM" href="/llms/base-llm" icon="foundation">
    Foundation class for all LLM integrations
  </Card>
  <Card title="OpenAI LLM" href="/llms/openai-llm" icon="openai">
    Integration with OpenAI GPT models
  </Card>
  <Card title="HTTP LLM" href="/llms/http-llm" icon="http">
    Generic HTTP-based LLM integration
  </Card>
  <Card title="Remote LLM" href="/llms/remote-llm" icon="cloud">
    Remote LLM service integration
  </Card>
</Cards>

## LLM Architecture

All LLM integrations inherit from the `BaseLLM` class:

```python
from oxygent.oxy.llms import BaseLLM
from oxygent.schemas import LLMResponse, Message

class CustomLLM(BaseLLM):
    async def generate_response(self, messages: List[Message]) -> LLMResponse:
        # Custom LLM integration logic
        return LLMResponse(...)
```

## Common Features

- **Async Operations**: All LLMs support asynchronous operations
- **Message Handling**: Standardized message format for conversations
- **Error Handling**: Robust error handling and retry mechanisms
- **Rate Limiting**: Built-in rate limiting and throttling
- **Logging**: Comprehensive logging for debugging and monitoring
- **Configuration**: Flexible configuration options for each provider
"""
        
        self._write_file(llms_output_dir / "index.mdx", llms_index)
        
        # Generate individual LLM docs
        for py_file in llms_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            file_info = self.analyzer.parse_file(py_file)
            if 'error' in file_info:
                continue
                
            llm_name = py_file.stem.replace('_', '-')
            self._generate_llm_doc(llms_output_dir, llm_name, file_info)
    
    def _generate_llm_doc(self, output_dir: Path, llm_name: str, file_info: Dict):
        """Generate documentation for a specific LLM."""
        title = llm_name.replace('-', ' ').title()
        
        content = f"""---
title: {title}
description: {file_info.get('module_docstring', f'{title} integration documentation')}
---

# {title}

{file_info.get('module_docstring', f'Documentation for the {title} integration.')}

## Overview

The {title} provides integration with specific LLM services, enabling seamless communication and response generation.

"""
        
        # Add class information
        for cls_info in file_info.get('classes', []):
            if 'llm' in cls_info['name'].lower():
                content += f"""
## Class Definition

```python
class {cls_info['name']}(BaseLLM):
    \"\"\"{cls_info.get('docstring', f'{cls_info["name"]} implementation.')}\"\"\"""
                
                # Add attributes
                if cls_info.get('attributes'):
                    content += "\n    # Configuration attributes:\n"
                    for attr in cls_info['attributes']:
                        attr_name = attr['name']
                        attr_type = attr.get('type', 'Any')
                        content += f"    {attr_name}: {attr_type}\n"
                
                content += "```\n"
        
        # Get the main class name
        main_class_name = 'LLM'
        if file_info.get('classes'):
            main_class_name = file_info['classes'][0].get('name', 'LLM')
        
        content += "\n## Usage Example\n\n"
        content += "```python\n"
        content += f"from oxygent.oxy.llms import {main_class_name}\n"
        content += "from oxygent.schemas import Message\n\n"
        content += "# Create and configure the LLM\n"
        content += f"llm = {main_class_name}(\n"
        content += "    # Configuration parameters\n"
        content += ")\n\n"
        content += "# Generate a response\n"
        content += 'messages = [Message.user_message("Hello, how are you?")]\n'
        content += "response = await llm.generate_response(messages)\n"
        content += "print(response.content)\n"
        content += "```\n\n"
        content += "## Configuration

Refer to the class definition above for available configuration options.

## Best Practices

1. **API Key Management**: Store API keys securely using environment variables
2. **Rate Limiting**: Respect provider rate limits and implement backoff strategies
3. **Error Handling**: Handle API errors gracefully with retry logic
4. **Cost Monitoring**: Monitor API usage and costs
5. **Response Validation**: Validate responses for expected format and content

## Related Components

- [Base LLM](/llms/base-llm): Foundation class for all LLM integrations
- [Agents](/agents): Agent components that use LLMs
"""
        
        self._write_file(output_dir / f"{llm_name}.mdx", content)
    
    def _generate_meta_json(self):
        """Generate meta.json configuration file."""
        meta_config = {
            "title": "OxyGent Flows Documentation",
            "description": "Comprehensive documentation for OxyGent's flow system",
            "icon": "workflow",
            "pages": [
                "index",
                {
                    "title": "Flows",
                    "pages": [
                        "flows/index",
                        "flows/workflow",
                        "flows/parallel-flow", 
                        "flows/plan-and-solve",
                        "flows/reflexion"
                    ]
                },
                {
                    "title": "Agents", 
                    "pages": [
                        "agents/index",
                        "agents/base-agent",
                        "agents/react-agent",
                        "agents/chat-agent",
                        "agents/local-agent",
                        "agents/remote-agent",
                        "agents/parallel-agent",
                        "agents/workflow-agent",
                        "agents/sse-oxy-agent"
                    ]
                },
                {
                    "title": "LLMs",
                    "pages": [
                        "llms/index",
                        "llms/base-llm",
                        "llms/openai-llm", 
                        "llms/http-llm",
                        "llms/remote-llm"
                    ]
                }
            ]
        }
        
        self._write_file(self.output_dir / "meta.json", json.dumps(meta_config, indent=2))
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file, creating directories as needed."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {file_path}")


def main():
    """Main execution function."""
    # Configuration
    source_directory = "/Users/chengkai48/Documents/aicoding/OxyGent"
    output_directory = "/Users/chengkai48/Documents/aicoding/OxyGent/mdocs-flows-new"
    
    print("Starting OxyGent Flows Documentation Generation...")
    print(f"Source Directory: {source_directory}")
    print(f"Output Directory: {output_directory}")
    
    # Create generator and run
    generator = FumadocsGenerator(source_directory, output_directory)
    generator.generate_all()
    
    print("\nDocumentation generation completed successfully!")
    print(f"Generated files in: {output_directory}")
    print("\nNext steps:")
    print("1. Review the generated documentation")
    print("2. Customize content as needed") 
    print("3. Integrate with your fumadocs project")


if __name__ == "__main__":
    main()
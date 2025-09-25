---
title: "Plan and Solve Flow"
description: "Strategic planning and execution flow that breaks down complex problems into manageable steps"
---

# Plan and Solve Flow

The PlanAndSolve flow implements a strategic approach to problem-solving by breaking complex tasks into sequential steps, executing them systematically, and optionally re-planning based on intermediate results.

## Overview

The Plan-and-Solve prompting methodology enhances problem-solving capabilities by:

1. **Planning Phase**: Analyzing the problem and creating a step-by-step execution plan
2. **Execution Phase**: Systematically executing each planned step
3. **Monitoring Phase**: Tracking progress and results from each step
4. **Re-planning Phase** (optional): Dynamically updating the plan based on execution results

This approach is particularly effective for complex, multi-step problems that benefit from structured decomposition and systematic execution.

## Class Definition

```python
from oxygent.oxy.flows import PlanAndSolve
```

### Inheritance Hierarchy

```
BaseFlow
└── PlanAndSolve
```

## Core Attributes

### Planning Configuration

- **`planner_agent_name`** (`str`): Name of the agent responsible for creating execution plans
  - Default: `"planner_agent"`
  - Role: Analyzes problems and generates step-by-step plans

- **`pre_plan_steps`** (`Optional[List[str]]`): Pre-defined steps to execute
  - Default: `None` 
  - When provided, skips initial planning phase

### Execution Configuration

- **`executor_agent_name`** (`str`): Name of the agent that executes individual steps
  - Default: `"executor_agent"`
  - Role: Performs the actual work for each planned step

- **`max_replan_rounds`** (`int`): Maximum number of execution iterations
  - Default: `30`
  - Prevents infinite loops in complex problems

### Re-planning Configuration

- **`enable_replanner`** (`bool`): Whether to enable dynamic re-planning
  - Default: `False`
  - When enabled, updates plans based on execution results

- **`llm_model`** (`str`): LLM model for fallback operations
  - Default: `"default_llm"`
  - Used for final answer generation when needed

### Response Parsing

- **`func_parse_planner_response`** (`Optional[Callable]`): Custom planner response parser
- **`pydantic_parser_planner`** (`PydanticOutputParser`): Structured planner output parser
- **`func_parse_replanner_response`** (`Optional[Callable]`): Custom replanner response parser  
- **`pydantic_parser_replanner`** (`PydanticOutputParser`): Structured replanner output parser

## Data Models

### Plan

```python
class Plan(BaseModel):
    """Plan to follow in future."""
    
    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )
```

### Response

```python
class Response(BaseModel):
    """Response to user."""
    
    response: str
```

### Action

```python
class Action(BaseModel):
    """Action to perform."""
    
    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )
```

## Usage Examples

### Basic Plan and Solve

```python
from oxygent.oxy.flows import PlanAndSolve

# Create basic plan-and-solve flow
plan_solve_flow = PlanAndSolve(
    name="problem_solver",
    desc="Systematic problem solver with planning",
    planner_agent_name="strategic_planner",
    executor_agent_name="task_executor",
    max_replan_rounds=10
)

# Execute complex problem
request = OxyRequest(
    callee="problem_solver",
    arguments={
        "query": "How can I optimize the performance of my web application?"
    }
)

response = await request.call()
```

### With Re-planning Enabled

```python
# Create flow with dynamic re-planning
adaptive_flow = PlanAndSolve(
    name="adaptive_solver",
    desc="Adaptive problem solver with re-planning",
    planner_agent_name="adaptive_planner", 
    executor_agent_name="flexible_executor",
    enable_replanner=True,
    max_replan_rounds=15
)

# Handle dynamic problem-solving
request = OxyRequest(
    callee="adaptive_solver",
    arguments={
        "query": "Develop a machine learning model for customer churn prediction"
    }
)

response = await request.call()
# Flow adapts plan based on intermediate results
```

### Pre-defined Plan Execution

```python
# Create flow with pre-defined steps
structured_flow = PlanAndSolve(
    name="structured_processor",
    desc="Execute predefined workflow steps",
    pre_plan_steps=[
        "Analyze the input data structure and format",
        "Validate data quality and identify missing values", 
        "Apply data cleaning and preprocessing steps",
        "Generate statistical summary and insights",
        "Create visualization and export results"
    ],
    executor_agent_name="data_processor"
)

# Execute with predefined plan
request = OxyRequest(
    callee="structured_processor",
    arguments={
        "query": "Process the customer survey dataset",
        "dataset_path": "/data/survey_responses.csv"
    }
)

response = await request.call()
```

### Software Development Workflow

```python
# Software development planning flow
dev_flow = PlanAndSolve(
    name="dev_workflow",
    desc="Software development planning and execution",
    planner_agent_name="architect_agent",
    executor_agent_name="developer_agent", 
    enable_replanner=True,
    max_replan_rounds=20
)

# Plan and implement feature
request = OxyRequest(
    callee="dev_workflow",
    arguments={
        "query": "Implement user authentication system with JWT tokens",
        "requirements": [
            "User registration and login",
            "Password hashing and validation", 
            "JWT token generation and validation",
            "Protected route middleware",
            "User session management"
        ]
    }
)

response = await request.call()
```

## Advanced Usage Patterns

### Custom Response Parsers

```python
from oxygent.schemas import LLMResponse

def custom_plan_parser(response_text: str) -> LLMResponse:
    """Custom parser for plan responses."""
    
    # Extract steps from response text
    lines = response_text.strip().split('\n')
    steps = []
    
    for line in lines:
        line = line.strip()
        if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
            # Clean step text
            step = re.sub(r'^[\d\-\•\.\)\s]+', '', line).strip()
            if step:
                steps.append(step)
    
    return LLMResponse(steps=steps)

# Create flow with custom parser
custom_flow = PlanAndSolve(
    name="custom_planner",
    desc="Plan and solve with custom parsing",
    func_parse_planner_response=custom_plan_parser,
    planner_agent_name="custom_planner_agent",
    executor_agent_name="custom_executor_agent"
)
```

### Progress Monitoring

```python
class MonitoredPlanAndSolve(PlanAndSolve):
    """PlanAndSolve with detailed progress monitoring."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execution_log = []
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with progress monitoring."""
        
        original_query = oxy_request.get_query()
        self.execution_log = [{
            "timestamp": time.time(),
            "phase": "initialization",
            "query": original_query
        }]
        
        plan_str = ""
        past_steps = ""
        plan_steps = self.pre_plan_steps
        
        for current_round in range(self.max_replan_rounds + 1):
            round_start = time.time()
            
            # Planning phase monitoring
            if (current_round == 0) and (self.pre_plan_steps is None):
                self.execution_log.append({
                    "timestamp": time.time(),
                    "phase": "planning",
                    "round": current_round
                })
                
                # Execute planning logic
                if self.pydantic_parser_planner:
                    query = self.pydantic_parser_planner.format(original_query)
                else:
                    query = original_query.copy()

                oxy_response = await oxy_request.call(
                    callee=self.planner_agent_name,
                    arguments={"query": query},
                )
                
                if self.pydantic_parser_planner:
                    plan_response = self.pydantic_parser_planner.parse(oxy_response.output)
                else:
                    plan_response = self.func_parse_planner_response(oxy_response.output)
                    
                plan_steps = plan_response.steps
                plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan_steps))
                
                self.execution_log.append({
                    "timestamp": time.time(),
                    "phase": "planning_complete",
                    "plan": plan_steps,
                    "step_count": len(plan_steps)
                })
            
            # Execution phase monitoring
            current_task = plan_steps[0]
            
            self.execution_log.append({
                "timestamp": time.time(),
                "phase": "execution",
                "round": current_round,
                "current_task": current_task,
                "remaining_steps": len(plan_steps)
            })
            
            task_formatted = f"""
                We have finished the following steps: {past_steps}
                The current step to execute is:{current_task}
                You should only execute the current step, and do not execute other steps in our plan.
            """.strip()
            
            executor_response = await oxy_request.call(
                callee=self.executor_agent_name,
                arguments={"query": task_formatted},
            )
            
            past_steps = past_steps + "\n" + f"task:{current_task}, result:{executor_response.output}"
            
            self.execution_log.append({
                "timestamp": time.time(),
                "phase": "execution_complete", 
                "round": current_round,
                "task": current_task,
                "result_length": len(executor_response.output),
                "round_duration": time.time() - round_start
            })
            
            # Re-planning phase (if enabled)
            if self.enable_replanner:
                self.execution_log.append({
                    "timestamp": time.time(),
                    "phase": "replanning",
                    "round": current_round
                })
                
                # Execute re-planning logic...
                # (Implementation continues with monitoring)
            
            else:
                plan_steps = plan_steps[1:]
                if len(plan_steps) == 0:
                    self.execution_log.append({
                        "timestamp": time.time(),
                        "phase": "completion",
                        "total_rounds": current_round + 1,
                        "total_duration": time.time() - self.execution_log[0]["timestamp"]
                    })
                    
                    return OxyResponse(
                        state=OxyState.COMPLETED,
                        output=executor_response.output,
                        extra={"execution_log": self.execution_log}
                    )
        
        # Return with execution log
        return OxyResponse(
            state=OxyState.COMPLETED,
            output="Maximum rounds reached",
            extra={"execution_log": self.execution_log}
        )
```

### Specialized Domain Flows

```python
class ResearchPlanAndSolve(PlanAndSolve):
    """Specialized flow for research tasks."""
    
    def __init__(self, **kwargs):
        # Set research-specific defaults
        kwargs.setdefault("planner_agent_name", "research_planner")
        kwargs.setdefault("executor_agent_name", "research_executor") 
        kwargs.setdefault("enable_replanner", True)
        kwargs.setdefault("max_replan_rounds", 25)
        
        super().__init__(**kwargs)
        
        # Add research-specific tools
        self.add_permitted_tools([
            "literature_search",
            "data_collector", 
            "statistical_analyzer",
            "citation_manager"
        ])

class ProjectManagementFlow(PlanAndSolve):
    """Flow optimized for project management tasks."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault("planner_agent_name", "project_planner")
        kwargs.setdefault("executor_agent_name", "task_manager")
        kwargs.setdefault("enable_replanner", True)
        
        super().__init__(**kwargs)
        
        # Add project management tools
        self.add_permitted_tools([
            "resource_allocator",
            "timeline_optimizer",
            "risk_assessor",
            "progress_tracker"
        ])
```

## Integration with OxyGent Framework

### In OxySpace Configuration

```python
def create_planning_flows():
    """Create various plan-and-solve flows."""
    
    return [
        # General problem solving
        PlanAndSolve(
            name="general_planner",
            desc="General purpose planning and execution flow",
            planner_agent_name="strategic_planner",
            executor_agent_name="general_executor",
            max_replan_rounds=15
        ),
        
        # Adaptive problem solving  
        PlanAndSolve(
            name="adaptive_planner", 
            desc="Adaptive planning with dynamic re-planning",
            planner_agent_name="adaptive_planner",
            executor_agent_name="flexible_executor", 
            enable_replanner=True,
            max_replan_rounds=20
        ),
        
        # Pre-structured workflows
        PlanAndSolve(
            name="data_processing_workflow",
            desc="Structured data processing workflow",
            pre_plan_steps=[
                "Load and validate input data",
                "Perform data cleaning and preprocessing", 
                "Apply analysis algorithms",
                "Generate visualizations and reports",
                "Export results and summary"
            ],
            executor_agent_name="data_processor"
        )
    ]
```

### Custom Workflow Integration

```python
from oxygent.oxy.flows import Workflow, PlanAndSolve

async def hybrid_planning_workflow(oxy_request: OxyRequest):
    """Combine planning with custom logic."""
    
    # Step 1: Use PlanAndSolve for initial planning
    planner = PlanAndSolve(
        planner_agent_name="strategic_planner",
        executor_agent_name="task_executor",
        enable_replanner=False  # We'll handle adaptation manually
    )
    
    initial_result = await planner._execute(oxy_request)
    
    # Step 2: Apply custom business logic 
    if requires_special_handling(initial_result):
        # Custom processing
        enhanced_result = apply_domain_expertise(initial_result)
        return enhanced_result
    
    # Step 3: Return original result if no special handling needed
    return initial_result

# Create hybrid flow
hybrid_flow = Workflow(
    name="hybrid_planner",
    desc="Planning flow with custom domain logic",
    func_workflow=hybrid_planning_workflow
)
```

## Best Practices

### 1. Agent Selection

```python
# Use specialized agents for better results
specialized_flow = PlanAndSolve(
    name="code_development_flow",
    desc="Software development planning and execution",
    
    # Use architect for high-level planning
    planner_agent_name="software_architect",
    
    # Use developer for implementation
    executor_agent_name="senior_developer",
    
    # Enable re-planning for iterative development
    enable_replanner=True,
    max_replan_rounds=30
)
```

### 2. Error Handling and Validation

```python
class RobustPlanAndSolve(PlanAndSolve):
    """PlanAndSolve with robust error handling."""
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with comprehensive error handling."""
        
        try:
            # Validate input parameters
            if not self._validate_request(oxy_request):
                return OxyResponse(
                    state=OxyState.FAILED,
                    output="Invalid request parameters"
                )
            
            # Execute with error tracking
            return await super()._execute(oxy_request)
            
        except Exception as e:
            logger.error(f"PlanAndSolve execution failed: {str(e)}")
            
            # Fallback to simple execution
            return await self._fallback_execution(oxy_request)
    
    def _validate_request(self, oxy_request: OxyRequest) -> bool:
        """Validate request parameters."""
        
        query = oxy_request.get_query()
        if not query or len(query.strip()) < 10:
            return False
            
        # Additional validation logic
        return True
    
    async def _fallback_execution(self, oxy_request: OxyRequest) -> OxyResponse:
        """Fallback execution strategy."""
        
        # Simple direct execution without planning
        fallback_messages = [
            Message.system_message("Please provide a direct answer to the user's question."),
            Message.user_message(oxy_request.get_query())
        ]
        
        fallback_response = await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": [msg.to_dict() for msg in fallback_messages]}
        )
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=f"Direct response (planning failed): {fallback_response.output}",
            extra={"fallback_used": True}
        )
```

### 3. Performance Optimization

```python
class OptimizedPlanAndSolve(PlanAndSolve):
    """Performance-optimized PlanAndSolve."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plan_cache = {}  # Cache for similar plans
        self.execution_cache = {}  # Cache for repeated executions
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with caching optimizations."""
        
        query_hash = hash(oxy_request.get_query())
        
        # Check plan cache
        if query_hash in self.plan_cache:
            cached_plan = self.plan_cache[query_hash]
            logger.info("Using cached plan")
            # Execute with cached plan
            return await self._execute_cached_plan(oxy_request, cached_plan)
        
        # Execute normally and cache result
        result = await super()._execute(oxy_request)
        
        # Cache successful plans
        if result.state == OxyState.COMPLETED:
            self.plan_cache[query_hash] = self._extract_plan_from_result(result)
        
        return result
```

## Common Use Cases

1. **Software Development**: Planning features, implementing code, testing, deployment
2. **Research Projects**: Literature review, data collection, analysis, report writing
3. **Business Analysis**: Market research, competitor analysis, strategy formulation
4. **Data Science Workflows**: Data preparation, model training, evaluation, deployment
5. **Project Management**: Task breakdown, resource allocation, timeline planning
6. **Content Creation**: Research, outline creation, writing, editing, publishing

## Performance Considerations

- **Planning Overhead**: Initial planning adds latency but improves execution quality
- **Re-planning Cost**: Dynamic re-planning increases execution time but improves adaptability
- **Agent Selection**: Specialized agents improve results but may have higher latency
- **Step Granularity**: Fine-grained steps provide better control but increase execution rounds
- **Cache Utilization**: Plan caching can significantly improve performance for similar queries

## Technical Notes

- Maximum execution rounds prevent infinite loops
- Each step builds on results from previous steps
- Re-planning updates the entire remaining plan based on current progress
- Pydantic parsers provide structured output handling
- Custom parsers allow flexibility in response interpretation
- Execution state is maintained throughout the entire flow

## Related Documentation

- [BaseFlow](/base-flow) - Base class for all flows
- [Workflow](/workflow-flow) - Custom workflow execution
- [ParallelFlow](/parallel-flow) - Concurrent execution flow
- [Reflexion](/reflexion-flow) - Iterative improvement flow
- [PydanticOutputParser](/pydantic-parser) - Structured output parsing
- [OxyRequest](/oxy-request) - Request object structure
- [OxyResponse](/oxy-response) - Response object structure
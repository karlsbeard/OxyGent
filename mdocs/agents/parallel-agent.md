---
title: ParallelAgent
description: Agent that executes tasks concurrently across multiple team members and aggregates their results
---

# ParallelAgent

The `ParallelAgent` class extends `LocalAgent` to provide concurrent task execution across multiple team members. It distributes the same task to all available team members simultaneously and combines their responses into a unified, summarized result.

## Overview

`ParallelAgent` is designed for scenarios where you need:

- **Concurrent Execution**: Run the same task across multiple agent instances simultaneously
- **Result Aggregation**: Combine multiple responses into a coherent summary
- **Team Coordination**: Manage parallel processing with unique identifiers
- **Scalable Processing**: Leverage multiple instances for improved throughput
- **Diverse Perspectives**: Gather different approaches to the same problem

This agent is particularly useful for:
- Generating multiple solutions and selecting the best one
- Cross-validation of results across different agent instances
- Load distribution across team members
- Consensus building from multiple perspectives

## Architecture

### Execution Flow

```
Input Task
     ↓
┌────────────────────────────────────────┐
│        ParallelAgent Coordinator       │
└────────┬───────────┬───────────┬──────┘
         ↓           ↓           ↓
    Team Member 1  Team Member 2  Team Member N
         ↓           ↓           ↓
    Response 1    Response 2    Response N
         ↓           ↓           ↓
         └───────────┴───────────┘
                     ↓
            LLM Summarization
                     ↓
              Final Response
```

### Team Structure

ParallelAgent automatically creates team members when a LocalAgent has `team_size > 1`:

1. Original agent becomes the coordinator (ParallelAgent)
2. Team members are created as `{name}_1`, `{name}_2`, etc.
3. Each member inherits the original agent's configuration
4. Parallel execution uses unique parallel_id for coordination

## Class Definition

```python
from oxygent.oxy.agents import ParallelAgent
from oxygent.schemas import OxyRequest, OxyResponse

# ParallelAgent is typically created automatically by LocalAgent
# when team_size > 1, but can be instantiated directly:

parallel_agent = ParallelAgent(
    name="team_coordinator",
    llm_model="gpt-4",
    permitted_tool_name_list=["member_1", "member_2", "member_3"]
)
```

## Key Method

### async _execute(oxy_request: OxyRequest) -> OxyResponse

Executes the request in parallel across all team members and summarizes results.

**Process Flow**:
1. Generate unique parallel execution ID
2. Distribute task to all team members concurrently
3. Collect all responses using `asyncio.gather`
4. Create summary prompt with user question and all results
5. Use LLM to generate coherent summary of parallel execution

```python
# Parallel execution with asyncio.gather:
parallel_id = shortuuid.ShortUUID().random(length=16)
oxy_responses = await asyncio.gather(*[
    oxy_request.call(
        callee=team_member_name,
        arguments=oxy_request.arguments,
        parallel_id=parallel_id,
    )
    for team_member_name in self.permitted_tool_name_list
])
```

## Usage Examples

### Basic Parallel Execution

```python
from oxygent.oxy.agents import LocalAgent

# Create a base agent with team_size > 1
# This automatically becomes a ParallelAgent with team members
class BrainstormingAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.team_size = 3  # Creates 3 team members
        self.prompt = """
        You are a creative brainstorming assistant.
        Generate innovative ideas and solutions for the given problem.
        Be creative and think outside the box.
        """

# When initialized, this becomes:
# - ParallelAgent (coordinator): "brainstorm_coordinator" 
# - Team members: "brainstorm_coordinator_1", "brainstorm_coordinator_2", "brainstorm_coordinator_3"

brainstorm_agent = BrainstormingAgent(name="brainstorm_coordinator")
```

### Problem-Solving Team

```python
class ProblemSolvingTeam(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.team_size = 4  # 4 different approaches
        self.tools = ["web_search", "calculator", "python_executor"]
        
        self.prompt = """
        You are part of a problem-solving team. Approach the given problem
        from your unique perspective and provide a comprehensive solution.
        
        Consider:
        - Different solution strategies
        - Alternative approaches
        - Potential edge cases
        - Implementation details
        
        Use available tools as needed to support your analysis.
        """

# This creates 4 parallel problem-solving agents that will:
# 1. Each tackle the problem independently
# 2. Use tools as needed for their approach
# 3. Results get combined into a comprehensive solution
```

### Code Review Team

```python
class CodeReviewTeam(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.team_size = 3
        self.tools = ["static_analyzer", "security_scanner", "performance_profiler"]
        
        self.prompt = """
        You are a code reviewer focusing on different aspects:
        - Code quality and best practices
        - Security vulnerabilities
        - Performance optimization opportunities
        - Maintainability and readability
        
        Provide constructive feedback and specific recommendations.
        """

# Each team member reviews code from different perspectives
# Results are combined into comprehensive review feedback
```

### Direct ParallelAgent Usage

```python
from oxygent.oxy.agents import ParallelAgent

# Create team members first (could be different agent types)
class AnalysisAgent(LocalAgent):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.llm_model = "gpt-4"
        self.prompt = f"You are {name}, providing analysis from your specialized perspective."

# Create specialized team members
market_analyst = AnalysisAgent(name="market_analyst")
technical_analyst = AnalysisAgent(name="technical_analyst") 
risk_analyst = AnalysisAgent(name="risk_analyst")

# Create ParallelAgent coordinator
analysis_team = ParallelAgent(
    name="analysis_coordinator",
    llm_model="gpt-4",
    permitted_tool_name_list=["market_analyst", "technical_analyst", "risk_analyst"]
)

# The coordinator will distribute tasks to all three analysts
# and summarize their different perspectives
```

### Advanced Team Configuration

```python
class AdaptiveTeam(LocalAgent):
    def __init__(self, team_size=3, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.team_size = team_size
        
        # Each team member gets slightly different instructions
        self.prompt = """
        You are team member ${member_id} out of ${total_members}.
        Your role: ${role_description}
        
        Focus on: ${focus_area}
        
        Collaborate with your team by providing unique insights
        from your specialized perspective.
        """

    def customize_team_member(self, member_id: int, total_members: int):
        """Customize individual team member configurations"""
        roles = {
            1: {"role": "Creative Thinker", "focus": "innovative solutions"},
            2: {"role": "Critical Analyst", "focus": "potential problems and risks"},
            3: {"role": "Practical Implementer", "focus": "feasibility and execution"}
        }
        
        role_config = roles.get(member_id, {"role": "General Analyst", "focus": "comprehensive analysis"})
        
        return {
            "member_id": member_id,
            "total_members": total_members,
            "role_description": role_config["role"],
            "focus_area": role_config["focus"]
        }

# This creates a team where each member has a specialized role
```

## Response Aggregation

### Default Summarization

ParallelAgent uses built-in summarization:

```python
# Automatic summary generation:
temp_memory = Memory()
temp_memory.add_message(
    Message.system_message(
        f"""You are a helpful assistant, the user's question is: {oxy_request.get_query()}.
Please summarize the results of the parallel execution of the above tasks."""
    )
)
temp_memory.add_message(
    Message.user_message(
        "The parallel results are as following:\n" +
        "\n".join([
            str(i + 1) + ". " + res.output
            for i, res in enumerate(oxy_responses)
        ])
    )
)
```

### Custom Aggregation Strategy

```python
class CustomAggregationAgent(ParallelAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Get parallel results
        parallel_id = shortuuid.ShortUUID().random(length=16)
        oxy_responses = await asyncio.gather(*[
            oxy_request.call(
                callee=permitted_tool_name,
                arguments=oxy_request.arguments,
                parallel_id=parallel_id,
            )
            for permitted_tool_name in self.permitted_tool_name_list
        ])
        
        # Custom aggregation logic
        return await self.custom_aggregate(oxy_request, oxy_responses)
    
    async def custom_aggregate(self, oxy_request: OxyRequest, responses: list) -> OxyResponse:
        """Custom aggregation strategy"""
        
        # Analyze response quality
        scored_responses = []
        for i, response in enumerate(responses):
            score = self.evaluate_response_quality(response.output)
            scored_responses.append((score, i+1, response.output))
        
        # Sort by quality score
        scored_responses.sort(reverse=True)
        
        # Create custom summary
        best_response = scored_responses[0]
        summary_prompt = f"""
        Based on {len(responses)} parallel analyses, here are the results ranked by quality:
        
        Best Response (Score: {best_response[0]}):
        {best_response[2]}
        
        Alternative Perspectives:
        {self.format_alternatives(scored_responses[1:3])}
        
        Provide a synthesized final answer combining the best insights.
        """
        
        return await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": [{"role": "user", "content": summary_prompt}]}
        )
```

## Performance Considerations

### Parallel Execution Benefits

- **Throughput**: Multiple agents process simultaneously
- **Redundancy**: Multiple solutions provide backup options
- **Diversity**: Different perspectives on the same problem
- **Quality**: Best ideas surface through comparison

### Resource Management

```python
class ResourceOptimizedTeam(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.team_size = 2  # Smaller teams for resource constraints
        
        # Optimize for efficiency
        self.short_memory_size = 5
        self.max_react_rounds = 8  # If using ReAct-based members
```

### Cost Optimization

```python
class CostEffectiveTeam(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.team_size = 3
        
        # Use cost-effective models for team members
        # Coordinator uses premium model for final summary
        self.llm_model = "gpt-4"  # Premium for coordination
        self.member_llm_model = "gpt-3.5-turbo"  # Cost-effective for members
```

## Error Handling

### Robust Parallel Execution

```python
class FaultTolerantParallelAgent(ParallelAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        parallel_id = shortuuid.ShortUUID().random(length=16)
        
        # Execute with error handling
        results = []
        for team_member in self.permitted_tool_name_list:
            try:
                response = await oxy_request.call(
                    callee=team_member,
                    arguments=oxy_request.arguments,
                    parallel_id=parallel_id,
                )
                results.append(response)
            except Exception as e:
                # Log error but continue with other team members
                logger.warning(f"Team member {team_member} failed: {e}")
                results.append(OxyResponse(
                    state=OxyState.ERROR,
                    output=f"Team member {team_member} encountered an error"
                ))
        
        # Filter out failed responses for summarization
        successful_responses = [r for r in results if r.state != OxyState.ERROR]
        
        if not successful_responses:
            return OxyResponse(
                state=OxyState.ERROR,
                output="All team members failed to process the request"
            )
        
        # Summarize successful responses
        return await self.summarize_responses(oxy_request, successful_responses)
```

## Monitoring and Analytics

### Team Performance Tracking

```python
class MonitoredParallelAgent(ParallelAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        start_time = time.time()
        
        # Execute parallel processing
        response = await super()._execute(oxy_request)
        
        # Track performance metrics
        total_time = time.time() - start_time
        team_size = len(self.permitted_tool_name_list)
        
        # Add metrics to response
        response.extra.update({
            "team_size": team_size,
            "execution_time": total_time,
            "parallel_efficiency": total_time / team_size,
            "parallel_id": oxy_request.parallel_id
        })
        
        return response
```

## Best Practices

1. **Optimal Team Size**: Balance quality and resource usage
   ```python
   self.team_size = 3  # Good balance for most use cases
   self.team_size = 5  # For complex problems requiring diverse perspectives
   ```

2. **Meaningful Differentiation**: Ensure team members provide unique value
   ```python
   # Good: Different specialized roles
   # Bad: Identical agents producing duplicate results
   ```

3. **Resource Management**: Consider computational costs
   ```python
   # Use smaller models for team members, premium for coordination
   member_model = "gpt-3.5-turbo"
   coordinator_model = "gpt-4"
   ```

4. **Error Resilience**: Handle individual member failures gracefully
   ```python
   # Always implement fallback strategies for failed team members
   ```

5. **Result Validation**: Quality-check parallel results
   ```python
   def validate_team_results(self, responses):
       # Implement validation logic for team outputs
       pass
   ```

## Common Use Cases

- **Content Generation**: Multiple creative approaches to writing tasks
- **Problem Solving**: Different solution strategies for complex problems
- **Code Review**: Multiple reviewers focusing on different aspects
- **Research Tasks**: Parallel research from different angles
- **Decision Making**: Gathering diverse perspectives for better decisions
- **Quality Assurance**: Cross-validation through multiple evaluations

## Related Classes

- **[LocalAgent](./local-agent)**: Parent class and source of team members
- **[ReActAgent](./react-agent)**: Can be used as team members for complex reasoning
- **[ChatAgent](./chat-agent)**: Can be used as team members for conversational tasks

## See Also

- [Agent System Overview](./index)
- [Team Coordination Patterns](../patterns/team-coordination)
- [Performance Optimization](../optimization)
- [Error Handling Strategies](../error-handling)
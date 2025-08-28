# ParallelAgent Class

## Overview

The `ParallelAgent` class executes tasks concurrently across multiple team members and aggregates their results into a unified response. This agent enables parallel processing by distributing the same task to all available team members simultaneously and then summarizing their combined outputs.

## Class Definition

```python
class ParallelAgent(LocalAgent)
```

**Module**: `oxygent.oxy.agents.parallel_agent`  
**Inherits from**: `LocalAgent`

## Key Features

- **Concurrent Execution**: Runs tasks in parallel across multiple team members
- **Result Aggregation**: Combines outputs from all team members
- **LLM-powered Summarization**: Uses language models to create coherent summaries
- **Fault Tolerance**: Continues execution even if some team members fail
- **Load Distribution**: Distributes computational load across multiple instances
- **Automatic Team Management**: Works with team configurations from LocalAgent

## Core Method

### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`

Executes the request in parallel across all team members and summarizes results.

**Execution Flow:**

1. **Parallel Execution**: Distributes task to all permitted team members
2. **Result Collection**: Gathers responses from all team members
3. **Response Aggregation**: Combines individual responses
4. **LLM Summarization**: Uses language model to create unified summary
5. **Final Response**: Returns comprehensive result

**Implementation Details:**

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    # Generate unique parallel execution ID
    parallel_id = shortuuid.ShortUUID().random(length=16)
    
    # Execute across all team members concurrently
    oxy_responses = await asyncio.gather(*[
        oxy_request.call(
            callee=permitted_tool_name,
            arguments=oxy_request.arguments,
            parallel_id=parallel_id,
        )
        for permitted_tool_name in self.permitted_tool_name_list
    ])
    
    # Build summarization prompt
    temp_memory = Memory()
    temp_memory.add_message(
        Message.system_message(
            f"""You are a helpful assistant, the user's question is: {oxy_request.get_query()}.
Please summarize the results of the parallel execution of the above tasks."""
        )
    )
    
    # Format parallel results
    result_text = "The parallel results are as following:\n" + "\n".join([
        str(i + 1) + ". " + res.output
        for i, res in enumerate(oxy_responses)
    ])
    temp_memory.add_message(Message.user_message(result_text))
    
    # Generate unified summary using LLM
    return await oxy_request.call(
        callee=self.llm_model,
        arguments={
            "messages": temp_memory.to_dict_list(
                short_memory_size=self.short_memory_size
            )
        },
    )
```

## Usage Examples

### Basic Parallel Processing

```python
from oxygent.oxy.agents.parallel_agent import ParallelAgent

# Create team members (these would be created automatically by LocalAgent with team_size > 1)
team_members = ["researcher_1", "researcher_2", "researcher_3"]

# Create parallel coordinator
parallel_agent = ParallelAgent(
    name="research_team",
    desc="Parallel research team for comprehensive analysis",
    llm_model="gpt-4",
    permitted_tool_name_list=team_members,
    short_memory_size=10
)

# Usage
response = await oxy_request.call(
    callee="research_team",
    arguments={
        "query": "What are the latest developments in quantum computing?"
    }
)
# Returns summarized insights from all three researchers
```

### Created via LocalAgent Team Configuration

```python
from oxygent.oxy.agents.local_agent import LocalAgent

# Original agent with team configuration
base_agent = LocalAgent(
    name="analyst",
    desc="Data analysis agent",
    llm_model="gpt-4",
    tools=["data_reader", "calculator", "chart_generator"],
    team_size=4  # Creates 4 parallel instances
)

# After initialization, this automatically creates:
# - analyst_1, analyst_2, analyst_3, analyst_4 (individual agents)
# - analyst (ParallelAgent coordinator)

# Usage distributes work across all team members
response = await oxy_request.call(
    callee="analyst",  # Uses the ParallelAgent coordinator
    arguments={
        "query": "Analyze sales data from Q1-Q4",
        "data_file": "sales_2024.csv"
    }
)
```

### Custom Parallel Processing with Different Agent Types

```python
# Create specialized agents for different aspects
agents_config = [
    {
        "name": "speed_optimizer",
        "desc": "Focuses on performance optimization",
        "llm_model": "gpt-4",
        "prompt": "You are an expert in performance optimization. Focus on speed improvements."
    },
    {
        "name": "security_auditor", 
        "desc": "Focuses on security analysis",
        "llm_model": "gpt-4",
        "prompt": "You are a security expert. Focus on security vulnerabilities and best practices."
    },
    {
        "name": "maintainability_reviewer",
        "desc": "Focuses on code maintainability",
        "llm_model": "gpt-4", 
        "prompt": "You are a software architect. Focus on maintainability and clean code."
    }
]

# Create parallel coordinator for code review
code_review_team = ParallelAgent(
    name="code_review_team",
    desc="Comprehensive code review team with multiple specializations",
    llm_model="gpt-4",
    permitted_tool_name_list=["speed_optimizer", "security_auditor", "maintainability_reviewer"]
)

# Usage for comprehensive code review
response = await oxy_request.call(
    callee="code_review_team",
    arguments={
        "query": "Review this Python function for optimization opportunities",
        "code": """
        def process_data(data_list):
            result = []
            for item in data_list:
                if item > 0:
                    result.append(item * 2)
            return result
        """
    }
)
```

## Advanced Patterns

### Error Handling and Partial Results

```python
class ResilientParallelAgent(ParallelAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        parallel_id = shortuuid.ShortUUID().random(length=16)
        
        # Execute with individual error handling
        tasks = [
            oxy_request.call(
                callee=agent_name,
                arguments=oxy_request.arguments,
                parallel_id=parallel_id,
            )
            for agent_name in self.permitted_tool_name_list
        ]
        
        # Gather results with error handling
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        successful_results = []
        failed_agents = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_agents.append(self.permitted_tool_name_list[i])
                logger.warning(f"Agent {self.permitted_tool_name_list[i]} failed: {str(result)}")
            else:
                successful_results.append(result)
        
        if not successful_results:
            return OxyResponse(
                state=OxyState.FAILED,
                output="All team members failed to execute the task"
            )
        
        # Build summary with failure information
        temp_memory = Memory()
        summary_prompt = f"""
        User question: {oxy_request.get_query()}
        
        Results from {len(successful_results)} out of {len(self.permitted_tool_name_list)} team members:
        """
        if failed_agents:
            summary_prompt += f"\nNote: {len(failed_agents)} team members failed: {', '.join(failed_agents)}"
        
        temp_memory.add_message(Message.system_message(summary_prompt))
        
        result_text = "\n".join([
            f"{i + 1}. {res.output}"
            for i, res in enumerate(successful_results)
        ])
        temp_memory.add_message(Message.user_message(result_text))
        
        return await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": temp_memory.to_dict_list()}
        )
```

### Weighted Result Aggregation

```python
class WeightedParallelAgent(ParallelAgent):
    def __init__(self, agent_weights: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.agent_weights = agent_weights or {}
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        parallel_id = shortuuid.ShortUUID().random(length=16)
        
        # Execute in parallel
        oxy_responses = await asyncio.gather(*[
            oxy_request.call(
                callee=agent_name,
                arguments=oxy_request.arguments,
                parallel_id=parallel_id,
            )
            for agent_name in self.permitted_tool_name_list
        ])
        
        # Build weighted summary
        temp_memory = Memory()
        temp_memory.add_message(
            Message.system_message(
                f"""You are summarizing parallel execution results for: {oxy_request.get_query()}
                Some results have higher weights indicating their importance in the final summary."""
            )
        )
        
        weighted_results = []
        for i, (agent_name, response) in enumerate(zip(self.permitted_tool_name_list, oxy_responses)):
            weight = self.agent_weights.get(agent_name, 1.0)
            weight_label = f" (Weight: {weight})" if weight != 1.0 else ""
            weighted_results.append(f"{i + 1}. {agent_name}{weight_label}: {response.output}")
        
        result_text = "Weighted parallel results:\n" + "\n".join(weighted_results)
        temp_memory.add_message(Message.user_message(result_text))
        
        return await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": temp_memory.to_dict_list()}
        )

# Usage with weights
weighted_team = WeightedParallelAgent(
    name="weighted_analysis_team",
    desc="Analysis team with weighted expertise",
    llm_model="gpt-4",
    permitted_tool_name_list=["senior_analyst", "junior_analyst", "specialist"],
    agent_weights={
        "senior_analyst": 2.0,    # Higher weight
        "specialist": 1.5,        # Medium weight  
        "junior_analyst": 1.0     # Standard weight
    }
)
```

### Consensus-Based Decision Making

```python
class ConsensusParallelAgent(ParallelAgent):
    def __init__(self, consensus_threshold: float = 0.6, **kwargs):
        super().__init__(**kwargs)
        self.consensus_threshold = consensus_threshold
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        parallel_id = shortuuid.ShortUUID().random(length=16)
        
        # Execute in parallel
        oxy_responses = await asyncio.gather(*[
            oxy_request.call(
                callee=agent_name,
                arguments=oxy_request.arguments,
                parallel_id=parallel_id,
            )
            for agent_name in self.permitted_tool_name_list
        ])
        
        # Analyze consensus
        responses_text = [resp.output for resp in oxy_responses]
        consensus_analysis = await self._analyze_consensus(
            oxy_request, responses_text
        )
        
        # Build final summary with consensus information
        temp_memory = Memory()
        temp_memory.add_message(
            Message.system_message(
                f"""Analyze the consensus among team members for: {oxy_request.get_query()}
                Consensus threshold: {self.consensus_threshold}
                Provide a summary highlighting areas of agreement and disagreement."""
            )
        )
        
        result_with_consensus = f"""
        Team Responses:
        {chr(10).join([f"{i+1}. {resp}" for i, resp in enumerate(responses_text)])}
        
        Consensus Analysis:
        {consensus_analysis}
        """
        
        temp_memory.add_message(Message.user_message(result_with_consensus))
        
        return await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": temp_memory.to_dict_list()}
        )
    
    async def _analyze_consensus(self, oxy_request: OxyRequest, responses: list) -> str:
        consensus_prompt = f"""
        Analyze the following {len(responses)} responses for consensus:
        
        {chr(10).join([f"Response {i+1}: {resp}" for i, resp in enumerate(responses)])}
        
        Identify:
        1. Areas of strong agreement (consensus >= {self.consensus_threshold})
        2. Areas of disagreement or uncertainty
        3. Overall consensus level
        """
        
        analysis_response = await oxy_request.call(
            callee=self.llm_model,
            arguments={
                "messages": [
                    {"role": "system", "content": "You are an expert at analyzing consensus among multiple viewpoints."},
                    {"role": "user", "content": consensus_prompt}
                ]
            }
        )
        
        return analysis_response.output
```

## Integration with Team Management

ParallelAgent is typically created automatically when a LocalAgent is configured with `team_size > 1`:

```python
# This configuration...
original_agent = LocalAgent(
    name="processor",
    desc="Data processing agent",
    llm_model="gpt-4",
    tools=["data_reader", "calculator"],
    team_size=3
)

# Automatically creates:
# 1. processor_1, processor_2, processor_3 (individual agents)
# 2. processor (ParallelAgent that coordinates the team)

# The MAS registration process:
mas.register_agent(original_agent)  # Registers all team members and coordinator
```

## Performance Considerations

### Concurrency Benefits

- **Parallel Processing**: Multiple agents process simultaneously
- **Reduced Latency**: Overall processing time limited by slowest agent
- **Increased Throughput**: Handle more requests concurrently

### Resource Usage

- **Memory**: Multiple agent instances consume more memory
- **CPU**: Parallel processing utilizes multiple cores
- **Network**: Concurrent API calls to language models

### Optimization Strategies

```python
# Optimize for specific use cases
fast_parallel = ParallelAgent(
    name="speed_team",
    llm_model="gpt-3.5-turbo",  # Faster, cost-effective model
    permitted_tool_name_list=["agent_1", "agent_2"],  # Smaller team
    short_memory_size=5  # Reduced context for speed
)

# Optimize for quality
quality_parallel = ParallelAgent(
    name="quality_team", 
    llm_model="gpt-4",  # High-quality model
    permitted_tool_name_list=["expert_1", "expert_2", "expert_3", "expert_4"],  # Larger team
    short_memory_size=20  # More context for better results
)
```

## Best Practices

1. **Team Composition**: Choose complementary team members for diverse perspectives
2. **Error Handling**: Implement robust error handling for partial failures
3. **Resource Management**: Monitor resource usage with large teams
4. **Result Quality**: Balance team size with result quality needs
5. **Timeout Management**: Set appropriate timeouts for parallel operations
6. **Logging**: Track individual agent performance and failures
7. **Consensus Mechanisms**: Implement consensus logic for critical decisions
8. **Load Balancing**: Consider agent capabilities when forming teams
9. **Cost Optimization**: Balance quality needs with computational costs
10. **Testing**: Test with various team sizes and failure scenarios

## Common Use Cases

1. **Multi-perspective Analysis**: Get diverse viewpoints on complex topics
2. **Redundancy**: Ensure reliability through parallel execution
3. **Performance Scaling**: Distribute load across multiple instances
4. **Consensus Building**: Combine multiple expert opinions
5. **Quality Assurance**: Cross-validation through parallel processing
6. **Research Tasks**: Comprehensive information gathering
7. **Decision Support**: Multi-criteria evaluation
8. **Content Generation**: Multiple creative approaches
9. **Code Review**: Different expertise areas (security, performance, style)
10. **Data Analysis**: Parallel processing of large datasets

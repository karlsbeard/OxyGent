---
title: ReActAgent
description: Advanced agent implementing the ReAct (Reasoning and Acting) paradigm for autonomous tool-based problem solving
---

# ReActAgent

The `ReActAgent` class implements the ReAct (Reasoning and Acting) paradigm, enabling autonomous agent behavior through iterative cycles of reasoning and tool execution. This advanced agent combines language model reasoning with dynamic tool usage to solve complex problems that require multiple steps and tool interactions.

## Overview

ReActAgent represents the most sophisticated agent type in the OxyGent framework, providing:

- **Autonomous Reasoning**: Iterative thought process with language model reasoning
- **Dynamic Tool Execution**: Intelligent selection and execution of tools based on reasoning
- **Sophisticated Memory Management**: Advanced memory strategies with token-based optimization
- **Multiple Tool Retrieval Modes**: Flexible tool discovery and retrieval strategies
- **Trust Mode Support**: Direct tool result usage when appropriate
- **Error Recovery**: Robust error handling and correction mechanisms
- **Reflexion Capabilities**: Self-evaluation and response improvement

## Architecture

### ReAct Loop

The core ReAct loop follows this pattern:

```
1. Reason: Analyze current situation and plan next action
2. Act: Execute selected tools based on reasoning
3. Observe: Process tool execution results
4. Repeat: Continue until satisfactory answer is reached
```

### Memory Structure

ReActAgent maintains multiple memory layers:

- **System Memory**: Instructions and prompts
- **Short Memory**: Recent conversation history
- **ReAct Memory**: Detailed reasoning and tool execution trace
- **Master Memory**: Cross-session user history (optional)

## Class Definition

```python
from oxygent.oxy.agents import ReActAgent
from oxygent.schemas import OxyRequest, OxyResponse

# Basic ReAct agent
react_agent = ReActAgent(
    name="problem_solver",
    llm_model="gpt-4",
    max_react_rounds=16,
    tools=["web_search", "calculator", "file_manager"]
)
```

## Key Attributes

### Execution Control

#### max_react_rounds
- **Type**: `int`
- **Default**: `16`
- **Description**: Maximum number of reasoning-acting iterations before fallback

#### trust_mode
- **Type**: `bool`
- **Default**: `False`
- **Description**: Enable direct tool result usage without additional reasoning

### Memory Management

#### is_discard_react_memory
- **Type**: `bool`
- **Default**: `True`
- **Description**: Whether to discard detailed ReAct memory in conversation history

#### memory_max_tokens
- **Type**: `int`
- **Default**: `24800`
- **Description**: Maximum tokens for memory management

#### weight_short_memory
- **Type**: `int`
- **Default**: `5`
- **Description**: Priority weight for short-term memory

#### weight_react_memory
- **Type**: `int`
- **Default**: `1`
- **Description**: Priority weight for detailed ReAct memory

## Tool Retrieval Modes

ReActAgent supports multiple tool retrieval strategies:

### Mode 1: No Retrieval (Return All Tools)
```python
agent = ReActAgent(
    name="all_tools_agent",
    llm_model="gpt-4",
    top_k_tools=float('inf'),
    is_retrieve_even_if_tools_scarce=False
)
```

### Mode 2: Query-Based Retrieval
```python
agent = ReActAgent(
    name="smart_retrieval_agent", 
    llm_model="gpt-4",
    top_k_tools=5  # Retrieve 5 most relevant tools
)
```

### Mode 3: Active Sourcing
```python
agent = ReActAgent(
    name="autonomous_agent",
    llm_model="gpt-4", 
    is_sourcing_tools=True,
    top_k_tools=5
)
```

## Key Methods

### LLM Response Parsing

#### _parse_llm_response(ori_response: str, oxy_request: OxyRequest = None) -> LLMResponse

Parses LLM output to determine next action in the ReAct loop.

**Response Types**:
- **TOOL_CALL**: LLM wants to execute a tool
- **ANSWER**: LLM provides final answer
- **ERROR_PARSE**: Response format error requiring correction

```python
# Expected JSON format from LLM:
{
    "tool_name": "web_search",
    "arguments": {
        "query": "latest AI research 2024"
    }
}

# Or for final answer (no JSON structure):
"Based on my research, here is the answer to your question..."
```

### Advanced Memory Management

#### async _get_history(oxy_request: OxyRequest, is_get_user_master_session=False) -> Memory

Implements sophisticated memory management with weighted scoring and token limits.

**Simple Mode** (`is_discard_react_memory=True`):
- Only keeps query-answer pairs
- Optimal for most conversation scenarios
- Reduces memory overhead

**Advanced Mode** (`is_discard_react_memory=False`):
- Retains detailed reasoning traces
- Uses weighted scoring for memory prioritization
- Applies token limits with intelligent filtering

### Reflexion System

#### _default_reflexion(response: str, oxy_request: OxyRequest) -> str

Evaluates agent responses for quality and provides feedback for improvement.

```python
# Custom reflexion function example:
def custom_reflexion(self, response: str, oxy_request: OxyRequest) -> str:
    if len(response.strip()) == 0:
        return "Response should not be empty."
    
    if "sorry" in response.lower() and "cannot" in response.lower():
        return "Try to be more helpful and provide alternative solutions."
    
    return None  # Response is acceptable
```

## Usage Examples

### Basic Problem-Solving Agent

```python
from oxygent.oxy.agents import ReActAgent

class ProblemSolver(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.max_react_rounds = 10
        self.tools = [
            "web_search",
            "calculator", 
            "python_executor",
            "file_reader"
        ]
        self.prompt = """
        You are an expert problem solver. Use the available tools to research, 
        calculate, and analyze information to provide comprehensive answers.
        
        Available tools:
        - web_search: Search for current information
        - calculator: Perform mathematical calculations
        - python_executor: Run Python code for complex analysis
        - file_reader: Read and analyze files
        
        Think step by step and use tools as needed.
        """

# Usage
solver = ProblemSolver(name="problem_solver")

# Example request:
request = OxyRequest(
    arguments={
        "query": "What's the compound annual growth rate of Tesla stock over the last 5 years?"
    }
)

# The agent will:
# 1. Search for Tesla stock data
# 2. Calculate CAGR using the calculator or Python
# 3. Provide a comprehensive answer with reasoning
```

### Research Assistant Agent

```python
class ResearchAssistant(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4-turbo"
        self.max_react_rounds = 20  # Allow for thorough research
        self.is_sourcing_tools = True  # Enable autonomous tool discovery
        self.tools = ["retrieve_tools"]  # Start with tool retrieval capability
        
        self.prompt = """
        You are a thorough research assistant. For each query:
        
        1. Break down the research question into components
        2. Gather information from multiple sources
        3. Analyze and synthesize findings
        4. Present well-structured, evidence-based answers
        
        Use tools strategically to gather comprehensive information.
        Always cite sources when possible.
        """

# This agent can autonomously discover and use research tools
```

### Data Analysis Agent

```python
class DataAnalyst(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.max_react_rounds = 15
        self.tools = [
            "python_executor",
            "csv_reader",
            "chart_generator",
            "statistical_analyzer"
        ]
        self.trust_mode = True  # Trust tool results for data operations
        
        self.prompt = """
        You are a data analyst. When given data analysis tasks:
        
        1. Examine the data structure and quality
        2. Apply appropriate statistical methods
        3. Generate visualizations when helpful
        4. Provide insights and recommendations
        
        Use Python for complex calculations and data manipulation.
        """

# Trust mode allows direct use of data analysis results
```

### Advanced Memory Configuration

```python
class MemoryOptimizedAgent(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.is_discard_react_memory = False  # Keep detailed memory
        self.memory_max_tokens = 32000  # Large context window
        self.weight_short_memory = 10  # Prioritize conversation history
        self.weight_react_memory = 3   # Moderate weight for tool traces
        
        # Custom memory scoring function
        self.func_map_memory_order = lambda x: 1.0 / (x ** 0.5)
        
        self.prompt = """
        You are an AI assistant with access to detailed conversation history.
        Use context from previous interactions to provide consistent, 
        context-aware responses.
        """

# This configuration provides sophisticated memory management
# with weighted importance scoring
```

## Advanced Features

### Custom Response Parser

```python
class CustomParserAgent(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_parse_llm_response = self.custom_parser
    
    def custom_parser(self, ori_response: str, oxy_request=None):
        """Custom LLM response parser"""
        
        # Handle special think tags
        if "<think>" in ori_response and "</think>" in ori_response:
            # Extract thinking and action separately
            think_section = ori_response.split("<think>")[1].split("</think>")[0]
            action_section = ori_response.split("</think>")[1].strip()
            
            # Process action section normally
            return self._parse_llm_response(action_section, oxy_request)
        
        # Handle multiple tool calls
        if "MULTIPLE_TOOLS:" in ori_response:
            # Custom handling for multiple simultaneous tool calls
            tool_calls = self.extract_multiple_tools(ori_response)
            return LLMResponse(
                state=LLMState.TOOL_CALL,
                output=tool_calls,
                ori_response=ori_response
            )
        
        # Fall back to default parser
        return self._parse_llm_response(ori_response, oxy_request)
```

### Custom Reflexion Logic

```python
class QualityAssuredAgent(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_reflexion = self.quality_check
    
    def quality_check(self, response: str, oxy_request: OxyRequest) -> str:
        """Advanced response quality checking"""
        
        # Check for completeness
        if len(response) < 10:
            return "Please provide a more detailed and complete answer."
        
        # Check for uncertainty without tool use
        uncertainty_phrases = ["i don't know", "not sure", "maybe", "possibly"]
        if any(phrase in response.lower() for phrase in uncertainty_phrases):
            available_tools = oxy_request.arguments.get("tools_description", "")
            if available_tools and "search" in available_tools:
                return "If you're uncertain, consider using available tools to find accurate information."
        
        # Check for generic responses
        if response.lower().startswith("i'm sorry, i cannot"):
            return "Try to provide helpful alternatives or use available tools to assist the user."
        
        return None  # Response passes quality check
```

### Multi-Modal ReAct Agent

```python
class MultiModalReActAgent(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4-vision"
        self.is_multimodal_supported = True
        self.tools = [
            "image_analyzer",
            "ocr_tool", 
            "chart_reader",
            "visual_qa"
        ]
        
        self.prompt = """
        You are a multi-modal AI agent capable of processing text, images, and other media.
        
        When analyzing visual content:
        1. Describe what you observe
        2. Use appropriate tools for detailed analysis
        3. Combine visual and textual information
        4. Provide comprehensive insights
        """

# This agent can handle images, documents, and other visual content
# in addition to text-based reasoning and tool usage
```

## Error Handling and Recovery

### Graceful Degradation

```python
class RobustReActAgent(ReActAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        try:
            return await super()._execute(oxy_request)
        except Exception as e:
            # Log the error
            logger.error(f"ReAct execution failed: {e}")
            
            # Provide fallback response
            fallback_prompt = """
            I encountered an issue during my reasoning process. 
            Let me try to provide a direct response based on my knowledge.
            """
            
            messages = [
                {"role": "system", "content": fallback_prompt},
                {"role": "user", "content": oxy_request.get_query()}
            ]
            
            return await oxy_request.call(
                callee=self.llm_model,
                arguments={"messages": messages}
            )
```

### Tool Error Recovery

```python
class RecoveryReActAgent(ReActAgent):
    async def handle_tool_error(self, tool_name: str, error: str, oxy_request: OxyRequest):
        """Handle tool execution errors with recovery strategies"""
        
        recovery_strategies = {
            "web_search": "Try rephrasing the search query or use alternative search terms.",
            "calculator": "Check the mathematical expression format and try again.",
            "file_reader": "Verify the file path exists and is accessible.",
            "default": f"The {tool_name} tool encountered an error. Consider using alternative approaches."
        }
        
        recovery_message = recovery_strategies.get(tool_name, recovery_strategies["default"])
        return f"Tool Error: {error}\n\nSuggestion: {recovery_message}"
```

## Performance Optimization

### Token Management

```python
class TokenOptimizedAgent(ReActAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Optimize for token efficiency
        self.memory_max_tokens = 16000  # Conservative limit
        self.short_memory_size = 8      # Fewer conversation turns
        self.max_react_rounds = 8       # Shorter reasoning cycles
        
        # Prioritize recent interactions
        self.func_map_memory_order = lambda x: 2.0 / x
```

### Batch Tool Execution

```python
# ReActAgent automatically supports parallel tool execution
# When LLM requests multiple tools:

llm_output = [
    {"tool_name": "web_search", "arguments": {"query": "AI news"}},
    {"tool_name": "calculator", "arguments": {"expression": "100 * 1.05"}}
]

# Both tools execute concurrently with asyncio.gather()
# Results are combined in the observation
```

## Monitoring and Debugging

### Execution Tracing

```python
class TracingReActAgent(ReActAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        trace_data = {
            "rounds": [],
            "tool_calls": [],
            "memory_usage": []
        }
        
        # Add tracing to the execution loop
        for round_num in range(self.max_react_rounds + 1):
            trace_data["rounds"].append({
                "round": round_num,
                "timestamp": time.time(),
                "query": oxy_request.get_query()
            })
            
            # Continue with normal execution...
            # Add trace data to response
            
        response = await super()._execute(oxy_request)
        response.extra["execution_trace"] = trace_data
        return response
```

## Best Practices

1. **Set Appropriate Round Limits**: Balance thoroughness with efficiency
   ```python
   self.max_react_rounds = 8   # For simple tasks
   self.max_react_rounds = 16  # For complex problem-solving
   self.max_react_rounds = 24  # For research and analysis tasks
   ```

2. **Choose Memory Strategy**: Match memory configuration to use case
   ```python
   # For conversational agents:
   self.is_discard_react_memory = True
   
   # For complex problem-solving:
   self.is_discard_react_memory = False
   self.memory_max_tokens = 32000
   ```

3. **Use Trust Mode Appropriately**: Enable for reliable tools
   ```python
   # For data processing tools:
   self.trust_mode = True
   
   # For unreliable or experimental tools:
   self.trust_mode = False
   ```

4. **Implement Custom Reflexion**: Improve response quality
   ```python
   self.func_reflexion = self.domain_specific_quality_check
   ```

5. **Monitor Performance**: Track token usage and execution time
   ```python
   # Add performance monitoring to your agent implementation
   start_time = time.time()
   response = await super()._execute(oxy_request)
   execution_time = time.time() - start_time
   ```

## Related Classes

- **[LocalAgent](./local-agent)**: Parent class providing tool and memory management
- **[ChatAgent](./chat-agent)**: Simpler conversational agent
- **[ParallelAgent](./parallel-agent)**: Team-based execution agent

## See Also

- [Agent System Overview](./index)
- [Tool Management](../tools)
- [Memory Systems](../memory)
- [LLM Integration](../llm)
- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Original ReAct research
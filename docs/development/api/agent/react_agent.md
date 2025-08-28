# ReActAgent Class

## Overview

The `ReActAgent` class implements the ReAct (Reasoning and Acting) paradigm for autonomous agent behavior. It combines language model reasoning with tool execution in an iterative loop, enabling agents to break down complex problems, reason about solutions, and take actions to achieve goals.

## Class Definition

```python
class ReActAgent(LocalAgent)
```

**Module**: `oxygent.oxy.agents.react_agent`  
**Inherits from**: `LocalAgent`

## Core Concept

The ReAct paradigm alternates between two phases:
1. **Reasoning**: LLM analyzes the problem and decides on the next action
2. **Acting**: Execute tools based on the reasoning decision

This creates an autonomous loop: **Reason → Act → Observe → Reason → Act → ...**

## Key Attributes

### Execution Control
- `max_react_rounds` (int): Maximum number of reasoning-acting iterations (default: 16)
- `trust_mode` (bool): Enable trust mode for direct tool results (default: False)

### Memory Management
- `is_discard_react_memory` (bool): Whether to discard detailed ReAct memory (default: True)
- `memory_max_tokens` (int): Maximum tokens for memory management (default: 24800)
- `weight_short_memory` (int): Weight for short-term memory (default: 5)
- `weight_react_memory` (int): Weight for ReAct memory (default: 1)
- `func_map_memory_order` (Callable): Function to map order to score (default: identity function)

### Custom Functions
- `func_parse_llm_response` (Optional[Callable]): Function to parse LLM output
- `func_reflexion` (Optional[Callable]): Function to perform reflexion on responses

## Tool Retrieval Modes

ReActAgent supports multiple tool retrieval strategies:

### Mode 1: No Retrieval
Return all available tools regardless of query.
```python
agent = ReActAgent(
    top_k_tools=float('inf'),
    is_retrieve_even_if_tools_scarce=False
)
```

### Mode 2: Query-based Retrieval
Automatically retrieve N most relevant tools based on query.
```python
agent = ReActAgent(
    top_k_tools=5,
    is_retrieve_even_if_tools_scarce=True
)
```

### Mode 3: Active Sourcing
Provide sourcing tool for agent-driven retrieval.
```python
agent = ReActAgent(
    is_sourcing_tools=True,
    top_k_tools=5
)
```

## Key Methods

### Initialization

#### `def __init__(self, **kwargs)`
Initializes the ReAct agent with appropriate configuration.

**Automatic Setup:**
- Sets prompt based on tool sourcing configuration
- Configures LLM response parser
- Sets up reflexion function
- Adds tool retrieval capability if vector search is configured

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
    # Auto-select prompt based on tool sourcing
    if not self.prompt:
        self.prompt = (
            SYSTEM_PROMPT_RETRIEVAL if self.is_sourcing_tools else SYSTEM_PROMPT
        )
    
    # Set default functions if not provided
    if self.func_parse_llm_response is None:
        self.func_parse_llm_response = self._parse_llm_response
    
    if self.func_reflexion is None:
        self.func_reflexion = self._default_reflexion
    
    # Add retrieve_tools if vector search is configured
    if Config.get_vearch_config():
        self.tools.append("retrieve_tools")
```

### Response Processing

#### `def _parse_llm_response(self, ori_response: str, oxy_request: OxyRequest = None) -> LLMResponse`
Parses LLM response to determine the next action.

**Supported Response Types:**

1. **Tool Call**: JSON format with tool_name and arguments
```json
{
    "tool_name": "calculator",
    "arguments": {"expression": "2 + 2"}
}
```

2. **Final Answer**: Natural language response without JSON
```text
The answer is 4 based on my calculation.
```

3. **Think Model Format**: Response with thinking process
```text
<think>Let me calculate this step by step...</think>
The calculation shows that 2 + 2 = 4.
```

**Return States:**
- `LLMState.TOOL_CALL`: Valid tool call detected
- `LLMState.ANSWER`: Final answer provided
- `LLMState.ERROR_PARSE`: Parsing error or formatting issue

### Reflexion System

#### `def _default_reflexion(self, response: str, oxy_request: OxyRequest) -> str`
Default reflexion function that validates response quality.

**Validation Checks:**
- Empty or whitespace-only responses
- Response quality assessment
- Custom validation logic (override for specific needs)

**Usage:**
```python
# Custom reflexion function
def custom_reflexion(self, response: str, oxy_request: OxyRequest) -> str:
    if len(response) < 10:
        return "Please provide a more detailed explanation."
    if "I don't know" in response.lower():
        return "Try to provide more specific information or use available tools."
    return None  # Response is acceptable
```

### Memory Management

#### `async def _get_history(self, oxy_request: OxyRequest, is_get_user_master_session=False) -> Memory`
Sophisticated memory management with two modes:

**Simple Mode** (`is_discard_react_memory=True`):
- Only keeps query-answer pairs
- Faster processing
- Reduced context size

**Advanced Mode** (`is_discard_react_memory=False`):
- Weighted memory scoring
- Token-based filtering
- Preserves reasoning traces
- Complex conversation flow reconstruction

**Advanced Mode Implementation:**
```python
# Collect all QA pairs with metadata
qa_list = []
for short_i, history in enumerate(historys):
    memory = json.loads(history["_source"]["memory"])
    qa_list.append((memory["query"], memory["answer"], short_i, "short"))
    
    # Add ReAct reasoning steps
    for react_q, react_a in chunk_list(memory["react_memory"]):
        qa_list.append((react_q["content"], react_a["content"], short_i, "react"))

# Calculate weighted scores
scores = []
for i, (q, a, short_i, memory_type) in enumerate(qa_list):
    weight = (
        self.weight_short_memory if memory_type == "short" 
        else self.weight_react_memory
    )
    scores.append(self.func_map_memory_order(i + 1) * weight)

# Token-based filtering with priority preservation
count_token = 0
retained_index = set()
for index in sorted_scores:
    q, a, short_i, memory_type = qa_list[index]
    count_token += len(q) + len(a)
    if count_token > self.memory_max_tokens:
        break
    retained_index.add(index)
```

### Core Execution

#### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`
Implements the main ReAct reasoning-acting loop.

**Execution Flow:**

```
1. Initialize ReAct memory
2. For each round (up to max_react_rounds):
   a. Build complete message context
   b. Call LLM for reasoning
   c. Parse LLM response
   d. If ANSWER: return final response
   e. If TOOL_CALL: execute tools and add observations
   f. If ERROR: add correction prompt
   g. Continue to next round
3. Fallback: Generate summary from tool results
```

**Detailed Implementation:**
```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    react_memory = Memory()
    
    for current_round in range(self.max_react_rounds + 1):
        # Build complete context
        temp_memory = Memory()
        temp_memory.add_message(
            Message.system_message(self._build_instruction(oxy_request.arguments))
        )
        temp_memory.add_messages(
            Message.dict_list_to_messages(oxy_request.get_short_memory())
        )
        temp_memory.add_message(Message.user_message(user_query_content))
        temp_memory.add_messages(react_memory.messages)
        
        # Get LLM reasoning
        oxy_response = await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": temp_memory.to_dict_list()}
        )
        
        llm_response = self.func_parse_llm_response(
            oxy_response.output, oxy_request
        )
        
        # Process based on LLM decision
        if llm_response.state is LLMState.ANSWER:
            return OxyResponse(
                state=OxyState.COMPLETED,
                output=llm_response.output,
                extra={"react_memory": react_memory.to_dict_list()}
            )
        
        elif llm_response.state is LLMState.TOOL_CALL:
            # Execute tool calls (parallel execution supported)
            parallel_id = shortuuid.ShortUUID().random(length=16)
            oxy_responses = await asyncio.gather(*[
                oxy_request.call(
                    callee=tool_call_dict["tool_name"],
                    arguments=tool_call_dict["arguments"],
                    parallel_id=parallel_id
                )
                for tool_call_dict in tool_call_dict_list
            ])
            
            # Build observation
            observation = Observation()
            for tool_call_dict, oxy_response in zip(tool_call_dict_list, oxy_responses):
                observation.add_exec_result(
                    ExecResult(
                        executor=tool_call_dict["tool_name"],
                        oxy_response=oxy_response
                    )
                )
            
            # Check for trust mode
            if self.trust_mode or (
                isinstance(llm_response.output, dict) and
                llm_response.output.get("trust_mode") == 1
            ):
                # Return tool results directly
                return OxyResponse(
                    state=OxyState.COMPLETED,
                    output=observation.to_content(self.is_multimodal_supported),
                    extra={"react_memory": react_memory.to_dict_list()}
                )
            
            # Add to ReAct memory for next iteration
            react_memory.add_message(
                Message.assistant_message(llm_response.ori_response)
            )
            react_memory.add_message(
                Message.user_message(
                    observation.to_content(self.is_multimodal_supported)
                )
            )
        
        else:
            # Error handling - add correction prompt
            react_memory.add_message(
                Message.assistant_message(llm_response.ori_response)
            )
            react_memory.add_message(Message.user_message(llm_response.output))
    
    # Fallback: Generate final answer from tool results
    return await self._generate_fallback_response(oxy_request, react_memory)
```

## Usage Examples

### Basic ReAct Agent

```python
from oxygent.oxy.agents.react_agent import ReActAgent

# Create a ReAct agent with tools
react_agent = ReActAgent(
    name="problem_solver",
    desc="Agent that can reason about problems and use tools to solve them",
    llm_model="gpt-4",
    tools=["calculator", "web_search", "file_reader"],
    max_react_rounds=10,
    trust_mode=False
)

# Usage
response = await oxy_request.call(
    callee="problem_solver",
    arguments={
        "query": "What is the current population of Tokyo and how does it compare to New York?"
    }
)
```

### Advanced Memory Configuration

```python
# ReAct agent with sophisticated memory management
advanced_react = ReActAgent(
    name="research_agent",
    desc="Research agent with advanced memory",
    llm_model="gpt-4",
    tools=["web_search", "document_analyzer", "data_calculator"],
    is_discard_react_memory=False,  # Keep detailed reasoning traces
    memory_max_tokens=32000,        # Large context window
    weight_short_memory=3,          # Prefer recent conversations
    weight_react_memory=2,          # Include reasoning steps
    max_react_rounds=20,            # More reasoning rounds
    func_map_memory_order=lambda x: 1.0 / x  # Recent items weighted higher
)
```

### Trust Mode Configuration

```python
# Agent with trust mode for direct tool results
trusted_agent = ReActAgent(
    name="trusted_executor",
    desc="Agent that can return tool results directly",
    llm_model="gpt-4",
    tools=["database_query", "api_caller"],
    trust_mode=True,  # Return tool results without further reasoning
    max_react_rounds=5
)

# Or selective trust mode via tool response
response_with_trust = {
    "tool_name": "database_query",
    "arguments": {"query": "SELECT * FROM users"},
    "trust_mode": 1  # This specific call uses trust mode
}
```

### Custom Response Parser

```python
class CustomReActAgent(ReActAgent):
    def _parse_llm_response(self, ori_response: str, oxy_request: OxyRequest = None) -> LLMResponse:
        # Handle custom response formats
        if ori_response.startswith("ACTION:"):
            # Parse custom action format
            action_line = ori_response.split("\n")[0]
            tool_name = action_line.replace("ACTION:", "").strip()
            
            # Extract arguments from subsequent lines
            args_text = "\n".join(ori_response.split("\n")[1:])
            try:
                arguments = json.loads(args_text)
                return LLMResponse(
                    state=LLMState.TOOL_CALL,
                    output={"tool_name": tool_name, "arguments": arguments},
                    ori_response=ori_response
                )
            except:
                return LLMResponse(
                    state=LLMState.ERROR_PARSE,
                    output="Invalid action format",
                    ori_response=ori_response
                )
        
        # Fall back to default parsing
        return super()._parse_llm_response(ori_response, oxy_request)
```

## Advanced Features

### Tool Sourcing Integration

When `is_sourcing_tools=True`, the agent can dynamically retrieve tools:

```python
sourcing_agent = ReActAgent(
    name="adaptive_agent",
    desc="Agent that can find and use tools dynamically",
    llm_model="gpt-4",
    is_sourcing_tools=True,
    top_k_tools=3,  # Retrieve top 3 most relevant tools
    tools=["retrieve_tools"]  # Automatically added
)
```

### Multimodal ReAct

```python
multimodal_react = ReActAgent(
    name="vision_reasoner",
    desc="ReAct agent with multimodal capabilities",
    llm_model="gpt-4-vision",
    tools=["image_analyzer", "text_extractor"],
    is_multimodal_supported=True
)

# Usage with images
response = await oxy_request.call(
    callee="vision_reasoner",
    arguments={
        "query": [
            {"type": "text", "text": "Analyze this image and extract key information"},
            {"type": "image_url", "image_url": {"url": "https://example.com/chart.png"}}
        ]
    }
)
```

### Parallel Tool Execution

ReActAgent automatically executes multiple tools in parallel when the LLM requests multiple actions:

```python
# LLM response requesting parallel tool calls
llm_output = [
    {"tool_name": "web_search", "arguments": {"query": "Tokyo population 2024"}},
    {"tool_name": "web_search", "arguments": {"query": "New York population 2024"}},
    {"tool_name": "calculator", "arguments": {"expression": "comparison formula"}}
]
```

## Best Practices

1. **Tool Selection**: Provide relevant, well-documented tools
2. **Round Limits**: Set appropriate `max_react_rounds` for problem complexity
3. **Memory Management**: Choose memory mode based on use case requirements
4. **Prompt Design**: Use clear, structured prompts that encourage reasoning
5. **Error Handling**: Implement robust reflexion functions for quality control
6. **Trust Mode**: Use judiciously for performance vs. reasoning trade-offs
7. **Tool Descriptions**: Ensure tools have clear, LLM-friendly descriptions
8. **Context Management**: Monitor token usage in complex reasoning chains
9. **Fallback Strategy**: Always provide fallback mechanisms for edge cases
10. **Testing**: Test with various problem types and complexities

## Common Patterns

### Problem-Solving Agent
```python
problem_solver = ReActAgent(
    name="general_solver",
    llm_model="gpt-4",
    tools=["calculator", "web_search", "code_executor"],
    prompt="You are a problem-solving agent. Break down complex problems into steps and use available tools to find solutions."
)
```

### Research Agent
```python
researcher = ReActAgent(
    name="researcher",
    llm_model="gpt-4",
    tools=["web_search", "document_reader", "data_analyzer"],
    is_discard_react_memory=False,  # Keep research process
    max_react_rounds=15,
    prompt="You are a research agent. Gather information systematically and synthesize findings."
)
```

### Data Analysis Agent
```python
analyst = ReActAgent(
    name="data_analyst",
    llm_model="gpt-4",
    tools=["database_query", "python_executor", "chart_generator"],
    trust_mode=True,  # Direct data results
    prompt="You are a data analyst. Use tools to query, analyze, and visualize data effectively."
)
```

## Performance Considerations

- **Memory Usage**: Advanced memory mode uses more tokens but provides better context
- **Round Optimization**: Higher round limits enable more thorough reasoning but increase latency
- **Tool Efficiency**: Parallel tool execution reduces overall response time
- **Trust Mode**: Reduces reasoning overhead for direct tool results
- **Context Size**: Monitor total context size including memory and tool descriptions
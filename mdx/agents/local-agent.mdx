---
title: LocalAgent
description: Base class for agents that execute locally with tool management, memory, and LLM integration capabilities
---

# LocalAgent

The `LocalAgent` class extends `BaseAgent` to provide comprehensive local execution capabilities. It serves as the foundation for agents that need to interact with tools, manage conversation memory, integrate with language models, and support team-based parallel execution.

## Overview

`LocalAgent` is a powerful base class that adds significant functionality beyond `BaseAgent`:

- **Dynamic Tool Discovery**: Automatically retrieves and manages available tools
- **Sub-agent Delegation**: Hierarchical support for delegating tasks to other agents
- **Conversation Memory**: Manages short-term and long-term conversation history
- **LLM Integration**: Seamless integration with language model services
- **Team Execution**: Support for parallel execution across multiple agent instances
- **Multimodal Support**: Handles text, images, and other content types

## Class Definition

```python
from oxygent.oxy.agents import LocalAgent
from oxygent.schemas import OxyRequest, OxyResponse

class MyLocalAgent(LocalAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Your local agent implementation
        pass
```

## Core Attributes

### LLM Configuration

#### llm_model
- **Type**: `str`
- **Default**: From `Config.get_agent_llm_model()`
- **Description**: The language model to use for this agent
- **Required**: Yes

#### prompt
- **Type**: `str`
- **Default**: From `Config.get_agent_prompt()`
- **Description**: System prompt template for agent behavior

#### additional_prompt
- **Type**: `str`
- **Default**: `""`
- **Description**: User-added prompt that extends the original prompt

### Tool Management

#### sub_agents
- **Type**: `list`
- **Default**: `[]`
- **Description**: Names of other agents this agent can delegate to (hierarchy support)

#### tools
- **Type**: `list`
- **Default**: `[]`
- **Description**: Tools available to this agent

#### except_tools
- **Type**: `list`
- **Default**: `[]`
- **Description**: Tools explicitly forbidden to this agent

#### is_sourcing_tools
- **Type**: `bool`
- **Default**: `False`
- **Description**: When enabled, agent actively retrieves tools instead of direct tool recall

#### top_k_tools
- **Type**: `int`
- **Default**: `10`
- **Description**: Number of tools to retrieve during dynamic tool discovery

### Memory Management

#### short_memory_size
- **Type**: `int`
- **Default**: From `Config.get_agent_short_memory_size()`
- **Description**: Number of short-term memory entries to retain

#### is_retain_master_short_memory
- **Type**: `bool`
- **Default**: `False`
- **Description**: Whether to retrieve user history from master session

### Multimodal Support

#### is_multimodal_supported
- **Type**: `bool`
- **Default**: `False`
- **Description**: Whether to support multimodal input (automatically detected from LLM)

#### is_attachment_processing_enabled
- **Type**: `bool`
- **Default**: `True`
- **Description**: Whether to inject attachments into query

### Team Execution

#### team_size
- **Type**: `int`
- **Default**: `1`
- **Description**: Number of instances for team execution (creates parallel execution when > 1)

## Key Methods

### Tool Management Methods

#### _init_available_tool_name_list()

Initializes the list of tools available to this agent, including sub-agents, MCP tools, function tools, and function hubs.

```python
# Automatically called during initialization
# Validates and registers:
# - Sub-agents from self.sub_agents
# - Tools from self.tools (excluding self.except_tools)
# - MCP tools and function hubs with their individual functions
```

**Raises**:
- `Exception`: If referenced agent or tool doesn't exist
- `Exception`: If referenced item is not a valid tool

### Memory Management Methods

#### async _get_history(oxy_request: OxyRequest, is_get_user_master_session=False) -> Memory

Retrieves conversation history from Elasticsearch with intelligent filtering.

```python
# Example usage in your agent
history = await self._get_history(oxy_request)
messages = history.to_dict_list()

# For master session history
master_history = await self._get_history(oxy_request, is_get_user_master_session=True)
```

**Parameters**:
- `oxy_request`: Current request containing trace information
- `is_get_user_master_session`: Whether to get master session history

**Returns**: Memory object with conversation history as alternating user/assistant messages

### Tool Retrieval Methods

#### async _get_llm_tool_desc_list(oxy_request: OxyRequest, query: str) -> list[str]

Retrieves tool descriptions for LLM context based on configuration and query relevance.

**Tool Retrieval Strategies**:

1. **No Vector Search**: Returns all permitted tools
2. **Dynamic Retrieval**: Uses query similarity to retrieve relevant tools
3. **Tool Scarcity Handling**: Provides all tools when count is below threshold
4. **Sub-agent Retention**: Keeps sub-agents in toolset regardless of retrieval

```python
# Example of tool retrieval based on query
tools_desc = await self._get_llm_tool_desc_list(oxy_request, "create a chart")
# Returns descriptions of chart-related tools
```

### Instruction Building

#### _build_instruction(arguments) -> str

Builds instruction prompt by substituting template variables.

```python
# Template example: "You are a ${role} assistant specialized in ${domain}"
# Arguments: {"role": "helpful", "domain": "data analysis"}
# Result: "You are a helpful assistant specialized in data analysis"

instruction = self._build_instruction({"task": "summarize", "format": "bullet points"})
```

**Parameters**:
- `arguments`: Dictionary containing variable values for substitution

**Returns**: Formatted instruction string with variables substituted

### Lifecycle Methods

#### async _before_execute(oxy_request: OxyRequest) -> OxyRequest

Prepares the request for execution by:
- Setting up tool descriptions for LLM context
- Processing multimodal content
- Handling attachments
- Optionally using intent understanding for query rewriting

```python
# Automatic multimodal content processing:
# Text content → {"type": "text", "text": "content"}
# URLs/Paths → Processed attachment objects
# Fallback → Text representation
```

## Usage Examples

### Basic Local Agent

```python
from oxygent.oxy.agents import LocalAgent
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class SimpleLocalAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"  # Required
        self.prompt = "You are a helpful assistant."
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Access processed tools descriptions
        tools_desc = oxy_request.arguments.get("tools_description", "")
        
        # Process with LLM
        response = await oxy_request.call(
            callee=self.llm_model,
            arguments={
                "messages": [
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": oxy_request.get_query()}
                ]
            }
        )
        
        return response
```

### Agent with Tool Management

```python
class ToolManagedAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.tools = ["web_search", "calculator", "file_manager"]
        self.except_tools = ["dangerous_tool"]  # Explicitly forbidden
        self.top_k_tools = 5  # Limit tool retrieval
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Tools are automatically managed and described
        # Available in oxy_request.arguments["tools_description"]
        return await super()._execute(oxy_request)
```

### Agent with Sub-agents

```python
class HierarchicalAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.sub_agents = ["data_analyst", "report_writer"]
        self.prompt = """
        You can delegate tasks to specialized agents:
        - data_analyst: For data processing and analysis
        - report_writer: For generating formatted reports
        """
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        query = oxy_request.get_query()
        
        if "analyze data" in query.lower():
            # Delegate to data analyst
            return await oxy_request.call(
                callee="data_analyst",
                arguments=oxy_request.arguments
            )
        elif "write report" in query.lower():
            # Delegate to report writer
            return await oxy_request.call(
                callee="report_writer", 
                arguments=oxy_request.arguments
            )
        
        # Handle directly
        return OxyResponse(
            state=OxyState.COMPLETED,
            output="Please specify whether you want data analysis or report writing."
        )
```

### Team Execution Agent

```python
class TeamAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.team_size = 3  # Creates 3 parallel instances
        self.prompt = "You are part of a team working on the same task."
    
    # When team_size > 1, this agent is automatically converted to ParallelAgent
    # The original agent becomes the coordinator
    # Individual team members are created as {name}_1, {name}_2, etc.
```

### Memory-Aware Agent

```python
class ConversationalAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.short_memory_size = 10  # Remember last 10 exchanges
        self.is_retain_master_short_memory = True  # Access user's main session
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Short memory is automatically loaded in _pre_process
        short_memory = oxy_request.get_short_memory()
        
        # Master memory (if enabled) is in arguments
        master_memory = oxy_request.arguments.get("master_short_memory", [])
        
        # Build full context
        messages = []
        messages.append({"role": "system", "content": self.prompt})
        messages.extend(master_memory[-5:])  # Last 5 from master session
        messages.extend(short_memory)  # Current session memory
        messages.append({"role": "user", "content": oxy_request.get_query()})
        
        return await oxy_request.call(
            callee=self.llm_model,
            arguments={"messages": messages}
        )
```

### Multimodal Agent

```python
class MultimodalAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4-vision"  # Multimodal model
        self.is_attachment_processing_enabled = True
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Query is automatically processed for multimodal content
        # Images, URLs, and attachments are handled automatically
        query = oxy_request.arguments.get("query")
        
        # query might be:
        # - String for text-only input
        # - List of content objects for multimodal input:
        #   [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": {...}}]
        
        return await oxy_request.call(
            callee=self.llm_model,
            arguments={
                "messages": [
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": query}
                ]
            }
        )
```

## Configuration Patterns

### Dynamic Tool Retrieval

```python
class DynamicToolAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_sourcing_tools = True  # Enable autonomous tool retrieval
        self.top_k_tools = 5
        self.tools = ["retrieve_tools"]  # Include tool retrieval capability
```

### Intent Understanding

```python
class IntentAwareAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.intent_understanding_agent = "intent_classifier"
        # This agent will rewrite queries before tool retrieval
```

### Tool Retention Strategies

```python
class StrategyAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Always keep sub-agents available regardless of retrieval
        self.is_retain_subagent_in_toolset = True  
        # Retrieve tools even when we have fewer than k tools
        self.is_retrieve_even_if_tools_scarce = True
        self.top_k_tools = 10
```

## Advanced Features

### Prompt Template Variables

LocalAgent supports dynamic prompt templating:

```python
self.prompt = """
You are a ${role} assistant working on ${task_type} tasks.
Your expertise level is ${expertise_level}.
Current context: ${context}
"""

# Variables are substituted from oxy_request.arguments
```

### Team Initialization

When `team_size > 1`, LocalAgent automatically:

1. Creates multiple agent instances (`{name}_1`, `{name}_2`, etc.)
2. Replaces itself with a `ParallelAgent` coordinator
3. Preserves all custom functions and configurations
4. Enables parallel task execution

### Memory Token Management

For advanced memory management (used in ReActAgent):

```python
self.memory_max_tokens = 24800  # Token limit for memory
self.weight_short_memory = 5    # Priority for short memory
self.weight_react_memory = 1    # Priority for detailed memory
```

## Error Handling

LocalAgent includes comprehensive error handling:

```python
# LLM model validation
if not self.llm_model:
    raise Exception(f"agent {self.name} not set llm_model")

# Tool existence validation  
if tool_name not in self.mas.oxy_name_to_oxy:
    raise Exception(f"Tool [{tool_name}] not exists.")

# Tool type validation
if not isinstance(oxy, BaseTool):
    raise Exception(f"[{oxy_name}] is not a tool.")
```

## Best Practices

1. **Always Set LLM Model**: The `llm_model` attribute is required
   ```python
   self.llm_model = "gpt-4"  # Required in __init__
   ```

2. **Use Tool Validation**: Let the framework validate tool availability
   ```python
   self.tools = ["existing_tool"]  # Will raise exception if not found
   ```

3. **Leverage Memory Management**: Use the built-in memory system
   ```python
   short_memory = oxy_request.get_short_memory()  # Automatic history loading
   ```

4. **Handle Multimodal Content**: Design prompts for mixed content types
   ```python
   if self.is_multimodal_supported:
       # Handle list-based content
   else:
       # Handle text-only content
   ```

5. **Implement Team Coordination**: Use team_size for parallel processing
   ```python
   self.team_size = 3  # Automatically creates parallel execution
   ```

## Related Classes

- **[BaseAgent](./base-agent)**: Parent class providing trace management
- **[ChatAgent](./chat-agent)**: Conversational agent extending LocalAgent
- **[ReActAgent](./react-agent)**: Reasoning and acting agent extending LocalAgent
- **[ParallelAgent](./parallel-agent)**: Team execution agent extending LocalAgent

## See Also

- [Agent System Overview](./index)
- [Tool Management](../tools)
- [Memory System](../memory)
- [Configuration Guide](../config)
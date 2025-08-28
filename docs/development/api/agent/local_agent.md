# LocalAgent Class

## Overview

The `LocalAgent` class serves as the base class for agents that execute locally with access to tools, sub-agents, and memory management capabilities. It handles tool retrieval, conversation history, and instruction building for LLM interactions.

## Class Definition

```python
class LocalAgent(BaseAgent)
```

**Module**: `oxygent.oxy.agents.local_agent`  
**Inherits from**: `BaseAgent`

## Core Attributes

### LLM Integration
- `llm_model` (str): The language model to use for this agent (required)
- `prompt` (Optional[str]): System prompt template for agent behavior
- `additional_prompt` (Optional[str]): User-added prompt text (default: "")

### Agent Hierarchy
- `sub_agents` (Optional[list]): Names of delegatable sub-agents
- `intent_understanding_agent` (Optional[str]): Agent for query rewriting and tool retrieval

### Tool Management
- `tools` (Optional[list]): Available tools for this agent
- `except_tools` (Optional[list]): Tools explicitly forbidden for this agent
- `is_sourcing_tools` (bool): Whether to use dynamic tool retrieval (default: False)
- `is_retain_subagent_in_toolset` (bool): Whether sub-agents remain in toolset (default: False)
- `top_k_tools` (int): Maximum number of tools to retrieve (default: 10)
- `is_retrieve_even_if_tools_scarce` (bool): Retrieve even with few tools (default: True)

### Memory Management
- `short_memory_size` (int): Number of conversation turns to retain
- `is_retain_master_short_memory` (bool): Whether to retrieve user history (default: False)

### Multimodal Support
- `is_multimodal_supported` (bool): Whether to support multimodal input (default: False, auto-detected)
- `is_attachment_processing_enabled` (bool): Whether to inject attachments into query (default: True)

### Team Execution
- `team_size` (int): Number of parallel instances for team execution (default: 1)

## Key Methods

### Initialization

#### `def __init__(self, **kwargs)`
Initializes the local agent and validates LLM model configuration.

**Validation:**
```python
if not self.llm_model:
    raise Exception(f"agent {self.name} not set llm_model")
```

#### `async def init(self)`
Performs comprehensive agent initialization including:
- Tool setup and validation
- Team-based execution configuration
- Multimodal capability detection
- Sub-agent registration

**Team Setup Logic:**
```python
if self.team_size > 1:
    # Create team member instances
    for i in range(self.team_size):
        new_instance = copy.deepcopy(self)
        new_instance.name = f"{self.name}_{i + 1}"
        # Register with MAS
    
    # Replace with ParallelAgent for coordination
    parallel_agent = ParallelAgent(...)
```

### Tool Management

#### `def _init_available_tool_name_list(self)`
Initializes the comprehensive list of available tools including:
- Sub-agents
- MCP tools
- Function tools
- Function hubs

**Tool Registration Logic:**
```python
# Sub-agents
for sub_agent in self.sub_agents:
    if sub_agent not in self.mas.oxy_name_to_oxy:
        raise Exception(f"Agent [{sub_agent}] not exists.")
    self.add_permitted_tool(sub_agent)

# Tools with type-specific handling
for oxy_name in self.tools:
    oxy = self.mas.oxy_name_to_oxy[oxy_name]
    if isinstance(oxy, (MCPTool, FunctionTool)):
        self.add_permitted_tool(oxy_name)
    elif isinstance(oxy, BaseMCPClient):
        # Register all included tools
        for tool_name in oxy.included_tool_name_list:
            if tool_name not in self.except_tools:
                self.add_permitted_tool(tool_name)
    # ... additional tool types
```

#### `async def _get_llm_tool_desc_list(self, oxy_request: OxyRequest, query: str) -> str`
Retrieves and formats tool descriptions for LLM context based on configuration.

**Tool Retrieval Strategies:**

1. **Direct Listing** (No vector search):
```python
if not Config.get_vearch_config():
    for tool_name in self.permitted_tool_name_list:
        tool_desc = oxy_request.get_oxy(tool_name).desc_for_llm
        llm_tool_desc_list.append(tool_desc)
```

2. **Dynamic Retrieval** (With vector search):
```python
if self.is_sourcing_tools:
    # Add autonomous retrieval capability
    tool_desc = oxy_request.get_oxy("retrieve_tools").desc_for_llm
    llm_tool_desc_list.append(tool_desc)
else:
    # Query-based tool retrieval
    oxy_response = await oxy_request.call(
        callee="retrieve_tools", 
        arguments={"query": query}
    )
```

### Memory Management

#### `async def _get_history(self, oxy_request: OxyRequest, is_get_user_master_session=False) -> Memory`
Retrieves conversation history from Elasticsearch with intelligent session management.

**Query Structure:**
```python
es_response = await self.mas.es_client.search(
    Config.get_app_name() + "_history",
    {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"trace_id": oxy_request.root_trace_ids}},
                    {"term": {"session_name": session_name}},
                ]
            }
        },
        "size": self.short_memory_size,
        "sort": [{"create_time": {"order": "desc"}}],
    }
)
```

**Memory Processing:**
```python
for history in historys:
    memory = json.loads(history["_source"]["memory"])
    short_memory.add_message(Message.user_message(memory["query"]))
    short_memory.add_message(Message.assistant_message(memory["answer"]))
```

### Instruction Building

#### `def _build_instruction(self, arguments) -> str`
Builds instruction prompts by substituting template variables.

**Template Variable Substitution:**
```python
pattern = re.compile(r"\$\{(\w+)\}")

def replacer(match):
    key = match.group(1)
    return str(arguments.get(key, match.group(0)))

return pattern.sub(replacer, self.prompt.strip())
```

### Lifecycle Hooks

#### `async def _pre_process(self, oxy_request: OxyRequest) -> OxyRequest`
Pre-processes requests with memory loading:
- Loads conversation history if not present
- Optionally loads master session history
- Calls parent pre-processing

#### `async def _before_execute(self, oxy_request: OxyRequest) -> OxyRequest`
Prepares execution context with:
- Tool description generation
- Intent understanding (optional)
- Multimodal content processing
- Attachment handling

**Multimodal Processing:**
```python
# Process query parts for multimodal support
for part in query_parts:
    ctype = part.get("content_type", "text/plain")
    data = str(part.get("data", ""))
    
    if ctype.startswith("text"):
        multimodal_content.append({"type": "text", "text": data})
    elif ctype in ("url", "path"):
        multimodal_content.extend(process_attachments([data]))
    
# Apply based on LLM capabilities
if self.is_multimodal_supported:
    oxy_request.arguments["query"] = multimodal_content
else:
    oxy_request.arguments["query"] = "\n".join(plain_text_lines)
```

## Usage Examples

### Basic Local Agent

```python
from oxygent.oxy.agents.local_agent import LocalAgent

class MyLocalAgent(LocalAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="my_agent",
            desc="Custom local agent",
            llm_model="gpt-4",
            prompt="You are a helpful assistant that ${task}",
            tools=["calculator", "web_search"],
            sub_agents=["specialist_agent"],
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Access pre-loaded tools and memory
        tools_desc = oxy_request.arguments.get("tools_description", "")
        short_memory = oxy_request.get_short_memory()
        
        # Implement agent-specific logic
        result = await self.process_with_tools(oxy_request)
        
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=result
        )
```

### Tool Retrieval Configuration

```python
# Mode 1: No Retrieval - Return all tools
agent = MyLocalAgent(
    top_k_tools=float('inf'),
    is_retrieve_even_if_tools_scarce=False
)

# Mode 2: Query-based Retrieval - Auto-retrieve N tools
agent = MyLocalAgent(
    top_k_tools=5,
    is_retrieve_even_if_tools_scarce=True
)

# Mode 3: Active Sourcing - Agent-driven retrieval
agent = MyLocalAgent(
    is_sourcing_tools=True,
    top_k_tools=5
)
```

### Team-based Execution

```python
team_agent = MyLocalAgent(
    name="team_leader",
    team_size=3,  # Creates 3 parallel instances
    llm_model="gpt-4"
)
# Automatically converts to ParallelAgent for coordination
```

## Advanced Features

### Deep Copy Support
LocalAgent implements `__deepcopy__` for safe instance cloning while preserving MAS connectivity:

```python
def __deepcopy__(self, memo):
    fields = self.model_dump()
    fields["mas"] = self.mas  # Keep MAS reference shared
    # Deep copy all other fields
    return self.__class__(**fields)
```

### Intent Understanding Integration
When configured with an intent understanding agent:
```python
agent = MyLocalAgent(
    intent_understanding_agent="intent_analyzer",
    # Agent will rewrite queries for better tool retrieval
)
```

### Attachment Processing
Supports various attachment types with multimodal conversion:
- URL references
- File paths
- Direct content injection
- Multimodal LLM integration

## Configuration Dependencies

LocalAgent relies on several configuration options:
- `Config.get_agent_llm_model()`: Default LLM model
- `Config.get_agent_prompt()`: Default system prompt
- `Config.get_agent_short_memory_size()`: Default memory size
- `Config.get_vearch_config()`: Vector search configuration

## Best Practices

1. **LLM Model**: Always specify a valid LLM model
2. **Tool Organization**: Use clear tool categorization and exception lists
3. **Memory Management**: Configure appropriate memory sizes for context
4. **Team Execution**: Use team_size > 1 for parallel processing needs
5. **Multimodal Support**: Enable attachment processing for rich content
6. **Tool Retrieval**: Choose appropriate retrieval strategy based on tool count
7. **Session Management**: Use descriptive session naming for history tracking
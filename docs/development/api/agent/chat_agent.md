# ChatAgent Class

## Overview

The `ChatAgent` class provides a conversational agent that manages chat interactions with language models. It handles conversation memory, processes user queries, and coordinates with language models to generate contextually aware responses.

## Class Definition

```python
class ChatAgent(LocalAgent)
```

**Module**: `oxygent.oxy.agents.chat_agent`  
**Inherits from**: `LocalAgent`

## Key Features

- **Conversational Memory Management**: Automatically handles conversation history and context
- **Multi-turn Conversations**: Supports continuous dialogue with context preservation
- **LLM Integration**: Seamless coordination with language models
- **Simple Interface**: Straightforward implementation for chat-based interactions
- **Memory Size Control**: Configurable conversation history limits
- **Parameter Passing**: Support for LLM-specific parameters

## Initialization

### `def __init__(self, **kwargs)`

Initializes the chat agent with a default conversational prompt.

**Default Behavior:**

```python
if not self.prompt:
    self.prompt = "You are a helpful assistant."
```

**Configuration Options:**

```python
chat_agent = ChatAgent(
    name="assistant",
    desc="Conversational AI assistant",
    llm_model="gpt-4",
    prompt="You are a knowledgeable assistant specialized in ${domain}",
    short_memory_size=10,  # Keep last 10 conversation turns
    **kwargs
)
```

## Core Method

### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`

Executes a chat interaction with the language model.

**Process Flow:**

1. **Memory Initialization**: Creates temporary memory container
2. **Instruction Building**: Builds system prompt with variable substitution
3. **History Loading**: Loads recent conversation history
4. **Query Addition**: Adds current user query to conversation
5. **LLM Call**: Sends complete conversation to language model
6. **Response Return**: Returns the generated response

**Implementation Details:**

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    # Create temporary memory container
    temp_memory = Memory()
    
    # Add system instruction
    temp_memory.add_message(
        Message.system_message(self._build_instruction(oxy_request.arguments))
    )
    
    # Load conversation history
    temp_memory.add_messages(
        Message.dict_list_to_messages(oxy_request.get_short_memory())
    )
    
    # Add current user query
    temp_memory.add_message(Message.user_message(oxy_request.get_query()))
    
    # Prepare LLM arguments
    arguments = {
        "messages": temp_memory.to_dict_list(
            short_memory_size=self.short_memory_size
        )
    }
    
    # Add optional LLM parameters
    llm_params = oxy_request.arguments.get("llm_params", dict())
    arguments.update(llm_params)
    
    # Call language model
    return await oxy_request.call(callee=self.llm_model, arguments=arguments)
```

## Message Flow

### Conversation Structure

The ChatAgent maintains a structured conversation flow:

```
System Message: [Agent Instructions]
User Message: [Previous Query 1]
Assistant Message: [Previous Response 1]
User Message: [Previous Query 2]
Assistant Message: [Previous Response 2]
...
User Message: [Current Query]
```

### Memory Management

- **Automatic History Loading**: Retrieves conversation history via `oxy_request.get_short_memory()`
- **Size Limiting**: Respects `short_memory_size` for token management
- **Context Preservation**: Maintains conversation continuity across interactions

## Usage Examples

### Basic Chat Agent

```python
from oxygent.oxy.agents.chat_agent import ChatAgent

# Create a simple conversational agent
chat_agent = ChatAgent(
    name="assistant",
    desc="General purpose chat assistant",
    llm_model="gpt-3.5-turbo",
    prompt="You are a helpful and friendly assistant."
)

# Usage in conversation
response = await oxy_request.call(
    callee="assistant",
    arguments={
        "query": "What is the weather like today?",
        "llm_params": {
            "temperature": 0.7,
            "max_tokens": 150
        }
    }
)
```

### Specialized Chat Agent

```python
# Domain-specific chat agent with template variables
specialized_agent = ChatAgent(
    name="coding_assistant",
    desc="Programming and software development assistant",
    llm_model="gpt-4",
    prompt="""You are an expert ${language} programmer and software architect.
    
    Your expertise includes:
    - Writing clean, efficient ${language} code
    - Following best practices and design patterns
    - Debugging and troubleshooting
    - Code review and optimization
    
    Always provide practical, working solutions with clear explanations.""",
    short_memory_size=20  # Longer memory for complex coding discussions
)

# Usage with template variables
response = await oxy_request.call(
    callee="coding_assistant",
    arguments={
        "query": "How do I implement a singleton pattern?",
        "language": "Python",  # Template variable substitution
        "llm_params": {
            "temperature": 0.3,  # Lower temperature for more consistent code
        }
    }
)
```

### Multi-Modal Chat Agent

```python
# Chat agent with multimodal support
multimodal_chat = ChatAgent(
    name="vision_assistant",
    desc="Chat assistant with image understanding",
    llm_model="gpt-4-vision",
    prompt="You are a helpful assistant that can analyze images and answer questions about them.",
    is_multimodal_supported=True,
    is_attachment_processing_enabled=True
)

# Usage with image attachments
response = await oxy_request.call(
    callee="vision_assistant",
    arguments={
        "query": [
            {"type": "text", "text": "What do you see in this image?"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
    }
)
```

## Advanced Configuration

### Conversation Memory Control

```python
# Fine-tuned memory management
chat_agent = ChatAgent(
    name="memory_aware_assistant",
    llm_model="gpt-4",
    short_memory_size=15,  # Keep last 15 turns
    is_retain_master_short_memory=True,  # Access broader conversation history
    memory_max_tokens=8000  # Token-based memory limiting (inherited from parent)
)
```

### LLM Parameter Integration

```python
# Agent with default LLM parameters
chat_agent = ChatAgent(
    name="configured_assistant",
    llm_model="gpt-4",
    prompt="You are a creative writing assistant."
)

# Usage with dynamic LLM parameters
response = await oxy_request.call(
    callee="configured_assistant",
    arguments={
        "query": "Write a short story about space exploration",
        "llm_params": {
            "temperature": 0.8,      # High creativity
            "max_tokens": 500,       # Longer response
            "top_p": 0.9,           # Diverse vocabulary
            "frequency_penalty": 0.2 # Reduce repetition
        }
    }
)
```

## Integration Patterns

### With Other Agents

```python
# Chat agent that can delegate to specialists
delegating_chat = ChatAgent(
    name="smart_assistant",
    desc="Chat assistant with specialist delegation",
    llm_model="gpt-4",
    prompt="""You are a smart assistant that can help with various tasks.
    
    When users ask about specific domains, consider whether to:
    1. Answer directly if the question is simple
    2. Delegate to specialist agents for complex queries
    
    Available specialists: ${available_tools}""",
    sub_agents=["code_specialist", "math_specialist", "research_specialist"],
    tools=["web_search", "calculator"]
)
```

### Session Management

```python
# Session-aware chat agent
session_chat = ChatAgent(
    name="session_assistant",
    desc="Session-aware conversational agent",
    llm_model="gpt-4",
    prompt="You are a helpful assistant. Remember our conversation context.",
    is_retain_master_short_memory=True
)

# Usage with session context
response = await oxy_request.call(
    callee="session_assistant",
    arguments={
        "query": "Continue our previous discussion about machine learning",
        "session_name": "ml_study_session",
        "is_save_history": True  # Persist conversation
    }
)
```

## Performance Considerations

### Memory Optimization

- **Token Management**: Use `short_memory_size` to control context length
- **History Pruning**: Automatic pruning of old conversation turns
- **Selective Loading**: Load only relevant conversation history

### Efficient LLM Usage

```python
# Optimized for cost and performance
efficient_chat = ChatAgent(
    name="efficient_assistant",
    llm_model="gpt-3.5-turbo",  # Cost-effective model
    short_memory_size=5,        # Limited context for faster processing
    prompt="You are a concise and helpful assistant."
)
```

## Error Handling

ChatAgent inherits comprehensive error handling from LocalAgent:

- **Network Errors**: Automatic retry with exponential backoff
- **LLM Errors**: Graceful handling of API failures
- **Memory Errors**: Fallback for memory loading issues
- **Timeout Handling**: Configurable timeout for LLM calls

## Best Practices

1. **Prompt Design**: Craft clear, specific prompts for intended behavior
2. **Memory Size**: Balance context preservation with performance
3. **Temperature Control**: Use appropriate temperature for use case
4. **Token Management**: Monitor token usage for cost control
5. **Session Names**: Use descriptive session names for history tracking
6. **Error Recovery**: Implement graceful degradation for failures
7. **Parameter Tuning**: Experiment with LLM parameters for optimal results
8. **Context Awareness**: Design prompts that leverage conversation history
9. **Multimodal Support**: Enable when working with images or rich content
10. **Performance Monitoring**: Track response times and error rates

## Common Use Cases

1. **Customer Support**: Automated customer service interactions
2. **Educational Tutoring**: Interactive learning and question answering
3. **Creative Writing**: Story generation and creative collaboration
4. **Technical Q&A**: Programming and technical support
5. **Personal Assistant**: Task management and information retrieval
6. **Content Generation**: Blog posts, articles, and marketing copy
7. **Language Learning**: Conversation practice and language tutoring
8. **Research Assistant**: Information gathering and analysis
9. **Code Review**: Programming assistance and code explanation
10. **Brainstorming**: Idea generation and creative problem solving

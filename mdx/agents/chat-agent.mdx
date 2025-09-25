---
title: ChatAgent
description: Conversational agent that manages chat interactions with language models and conversation memory
---

# ChatAgent

The `ChatAgent` class extends `LocalAgent` to provide a streamlined interface for conversational AI interactions. It specializes in managing conversation flows, processing user queries, and maintaining dialogue continuity through intelligent memory management.

## Overview

`ChatAgent` is designed specifically for chat-based interactions and provides:

- **Conversational Flow Management**: Maintains natural dialogue progression
- **Automatic Memory Integration**: Seamlessly incorporates conversation history  
- **Simple Query Processing**: Streamlined interface for chat interactions
- **Default Conversation Prompts**: Built-in helpful assistant behavior
- **Multi-turn Dialogue Support**: Maintains context across conversation turns

This agent is ideal for creating chatbots, conversational assistants, and any application requiring natural dialogue capabilities.

## Class Definition

```python
from oxygent.oxy.agents import ChatAgent
from oxygent.schemas import OxyRequest, OxyResponse

# Basic usage
chat_agent = ChatAgent(
    name="assistant",
    llm_model="gpt-4",
    prompt="You are a helpful assistant."
)
```

## Key Features

### Automatic Prompt Initialization

ChatAgent provides a default conversational prompt if none is specified:

```python
# If no prompt is provided, defaults to:
self.prompt = "You are a helpful assistant."
```

### Built-in Conversation Memory

The agent automatically manages conversation context by:

1. Loading conversation history from previous interactions
2. Combining system instructions with historical context
3. Adding the current user query to continue the dialogue
4. Maintaining proper message flow (system → history → user query)

## Core Method

### async _execute(oxy_request: OxyRequest) -> OxyResponse

Executes a chat interaction with the configured language model.

**Process Flow**:
1. Creates temporary memory container
2. Adds system message with built instruction
3. Loads and adds conversation history (short-term memory)
4. Adds current user query
5. Calls the LLM with complete conversation context

```python
# Message structure sent to LLM:
[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Previous user message 1"},
    {"role": "assistant", "content": "Previous assistant response 1"}, 
    {"role": "user", "content": "Previous user message 2"},
    {"role": "assistant", "content": "Previous assistant response 2"},
    {"role": "user", "content": "Current user query"}
]
```

## Usage Examples

### Basic Chat Agent

```python
from oxygent.oxy.agents import ChatAgent

# Simple conversational agent
chat_agent = ChatAgent(
    name="basic_chat",
    llm_model="gpt-4",
    prompt="You are a friendly and helpful assistant."
)

# The agent is now ready to handle conversational requests
# Memory management and conversation flow are handled automatically
```

### Specialized Chat Agent

```python
class CustomerServiceAgent(ChatAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.prompt = """
        You are a professional customer service representative for TechCorp.
        
        Guidelines:
        - Be polite and helpful
        - Provide accurate information about our products
        - Escalate complex issues to human agents when needed
        - Always maintain a professional tone
        
        If you don't know something, say so rather than guessing.
        """
        self.short_memory_size = 15  # Remember longer conversations

# Usage
service_agent = CustomerServiceAgent(name="customer_service")
```

### Domain-Specific Chat Agent

```python
class TechnicalSupportAgent(ChatAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4-turbo"
        self.prompt = """
        You are a technical support specialist with expertise in:
        - Software troubleshooting
        - Hardware diagnostics  
        - Network configuration
        - System administration
        
        Provide step-by-step solutions and ask clarifying questions when needed.
        Use technical terminology appropriately based on the user's apparent skill level.
        """
        # Enable tools for technical tasks
        self.tools = ["system_diagnostics", "log_analyzer", "network_scanner"]

# Usage
tech_agent = TechnicalSupportAgent(name="tech_support")
```

### Multi-Language Chat Agent

```python
class MultiLingualChatAgent(ChatAgent):
    def __init__(self, default_language="en", **kwargs):
        super().__init__(**kwargs)
        self.default_language = default_language
        self.llm_model = "gpt-4"
        
    @property  
    def prompt(self):
        prompts = {
            "en": "You are a helpful assistant. Respond in English unless the user writes in another language.",
            "es": "Eres un asistente útil. Responde en español a menos que el usuario escriba en otro idioma.",
            "fr": "Vous êtes un assistant utile. Répondez en français sauf si l'utilisateur écrit dans une autre langue.",
            "de": "Sie sind ein hilfreicher Assistent. Antworten Sie auf Deutsch, es sei denn, der Benutzer schreibt in einer anderen Sprache."
        }
        return prompts.get(self.default_language, prompts["en"])

# Usage
english_agent = MultiLingualChatAgent(name="chat_en", default_language="en")
spanish_agent = MultiLingualChatAgent(name="chat_es", default_language="es")
```

### Memory-Optimized Chat Agent

```python
class ContextAwareChatAgent(ChatAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.short_memory_size = 20  # Keep more conversation history
        self.is_retain_master_short_memory = True  # Access user's main session
        
        self.prompt = """
        You are an intelligent assistant with access to our conversation history.
        
        Use the conversation context to:
        - Provide relevant and coherent responses
        - Remember user preferences and previous discussions
        - Build upon earlier topics when appropriate
        - Maintain consistency in your responses
        """

# This agent will have access to both:
# - Current session memory (last 20 exchanges)
# - Master session memory (from user's main conversation thread)
```

## Integration Examples

### With Tool Management

```python
class ToolEnabledChatAgent(ChatAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.tools = [
            "web_search",
            "calculator", 
            "weather_api",
            "calendar_manager"
        ]
        self.prompt = """
        You are a helpful assistant with access to various tools.
        
        Available capabilities:
        - Web search for current information
        - Mathematical calculations
        - Weather information
        - Calendar management
        
        Use tools when appropriate to provide accurate and helpful responses.
        """

# The ChatAgent will automatically include tool descriptions in the conversation
# Users can ask questions that trigger tool usage naturally
```

### With Sub-Agent Delegation

```python
class CoordinatorChatAgent(ChatAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm_model = "gpt-4"
        self.sub_agents = [
            "technical_specialist",
            "creative_writer", 
            "data_analyst"
        ]
        self.prompt = """
        You are a coordinator assistant that can delegate tasks to specialists.
        
        Available specialists:
        - Technical Specialist: For programming and technical questions
        - Creative Writer: For writing and creative tasks  
        - Data Analyst: For data processing and analysis
        
        For complex or specialized requests, delegate to the appropriate specialist.
        For general conversation, handle directly.
        """

# This agent can seamlessly switch between direct conversation and specialist delegation
```

## Request Processing

### Input Format

ChatAgent expects standard OxyRequest format:

```python
# Typical request structure:
{
    "query": "Hello, can you help me with Python programming?",
    "short_memory": [
        {"role": "user", "content": "Hi there"},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
}
```

### Response Format

Returns standard OxyResponse with conversational output:

```python
# Typical response:
{
    "state": "COMPLETED",
    "output": "Hello! I'd be happy to help you with Python programming. What specific aspect would you like to learn about or what problem are you trying to solve?"
}
```

## Advanced Configuration

### Custom Memory Management

```python
class CustomMemoryChatAgent(ChatAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom memory processing before standard chat execution
        
        # Filter sensitive information from history
        filtered_memory = self.filter_sensitive_content(
            oxy_request.get_short_memory()
        )
        
        # Override the memory in the request
        temp_memory = Memory()
        temp_memory.add_message(
            Message.system_message(self._build_instruction(oxy_request.arguments))
        )
        temp_memory.add_messages(Message.dict_list_to_messages(filtered_memory))
        temp_memory.add_message(Message.user_message(oxy_request.get_query()))
        
        # Custom LLM parameters
        arguments = {
            "messages": temp_memory.to_dict_list(short_memory_size=self.short_memory_size),
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        return await oxy_request.call(callee=self.llm_model, arguments=arguments)
    
    def filter_sensitive_content(self, memory_list):
        # Custom filtering logic
        return [msg for msg in memory_list if not self.contains_sensitive_info(msg)]
```

### Dynamic Prompt Adaptation

```python
class AdaptiveChatAgent(ChatAgent):
    def _build_instruction(self, arguments) -> str:
        base_prompt = super()._build_instruction(arguments)
        
        # Adapt prompt based on conversation context
        user_query = arguments.get("query", "")
        
        if "technical" in user_query.lower():
            return base_prompt + "\n\nFocus on providing detailed technical explanations."
        elif "creative" in user_query.lower():
            return base_prompt + "\n\nBe creative and imaginative in your responses."
        else:
            return base_prompt
```

## Error Handling

ChatAgent inherits robust error handling from LocalAgent:

```python
class RobustChatAgent(ChatAgent):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        try:
            return await super()._execute(oxy_request)
        except Exception as e:
            # Graceful fallback for chat interactions
            return OxyResponse(
                state=OxyState.COMPLETED,
                output="I apologize, but I'm having trouble processing your request right now. Could you please try rephrasing your question?"
            )
```

## Best Practices

1. **Set Clear Conversation Boundaries**: Define the agent's role and capabilities clearly
   ```python
   self.prompt = "I am a customer service agent. I can help with orders, returns, and product questions."
   ```

2. **Use Appropriate Memory Size**: Balance context retention with performance
   ```python
   self.short_memory_size = 10  # Good for most chat scenarios
   self.short_memory_size = 20  # For complex, context-heavy conversations
   ```

3. **Handle Multimodal Input**: Consider image and file inputs in conversations
   ```python
   # ChatAgent automatically handles multimodal content through LocalAgent
   self.is_multimodal_supported = True  # Set by LLM capability
   ```

4. **Design for Conversation Flow**: Create prompts that encourage natural dialogue
   ```python
   self.prompt = """
   You are a conversational assistant. 
   Ask follow-up questions when helpful.
   Acknowledge previous messages when relevant.
   Maintain a consistent personality throughout the conversation.
   """
   ```

## Performance Considerations

- **Memory Management**: ChatAgent automatically manages conversation history
- **Token Usage**: Monitor token consumption for long conversations
- **Response Time**: Simple structure ensures fast response times
- **Scalability**: Lightweight design suitable for high-volume chat applications

## Related Classes

- **[LocalAgent](./local-agent)**: Parent class providing tool and memory management
- **[ReActAgent](./react-agent)**: More complex reasoning agent for tool-heavy tasks
- **[BaseAgent](./base-agent)**: Foundation class with trace management

## See Also

- [Agent System Overview](./index)
- [Conversation Memory](../memory)
- [LLM Integration](../llm)
- [Tool Management](../tools)
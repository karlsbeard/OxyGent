---
title: OpenAILLM - Official OpenAI Integration
description: Official OpenAI client implementation with advanced features like reasoning content and streaming support
---

# OpenAILLM - Official OpenAI Integration

The `OpenAILLM` class provides a production-ready implementation of the RemoteLLM interface specifically designed for OpenAI's language models. It leverages the official `AsyncOpenAI` client for optimal performance, compatibility, and access to the latest OpenAI features including reasoning content (o1 models) and advanced streaming capabilities.

## Class Overview

```python
from oxygent.oxy.llms.openai_llm import OpenAILLM
from oxygent.oxy.llms.remote_llm import RemoteLLM
from openai import AsyncOpenAI
```

`OpenAILLM` extends `RemoteLLM` to provide OpenAI-specific functionality while maintaining full compatibility with the OxyGent LLM system.

## Class Definition

```python
class OpenAILLM(RemoteLLM):
    """OpenAI Large Language Model implementation.
    
    This class provides a concrete implementation of RemoteLLM specifically designed
    for OpenAI's language models. It uses the official AsyncOpenAI client for
    optimal performance and compatibility with OpenAI's API standards.
    """
```

## Supported Models

### GPT-4o Series (Recommended)
- **gpt-4o**: Latest multimodal model with vision, code, and reasoning capabilities
- **gpt-4o-mini**: Faster, more cost-effective version of GPT-4o
- **gpt-4o-2024-08-06**: Specific snapshot version

### GPT-4 Series
- **gpt-4-turbo**: Latest GPT-4 Turbo with 128K context window
- **gpt-4**: Original GPT-4 model with 8K context window
- **gpt-4-32k**: Extended context version (32K tokens)
- **gpt-4-vision-preview**: GPT-4 with vision capabilities

### GPT-3.5 Series
- **gpt-3.5-turbo**: Fast, cost-effective model for most use cases
- **gpt-3.5-turbo-16k**: Extended context version
- **gpt-3.5-turbo-instruct**: Instruction-following variant

### O1 Series (Reasoning Models)
- **o1-preview**: Advanced reasoning model with chain-of-thought
- **o1-mini**: Smaller, faster reasoning model

## Configuration

### Environment Setup

```bash
# Required environment variables
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Optional configuration
OPENAI_ORG_ID=your-organization-id
OPENAI_PROJECT_ID=your-project-id
```

### Configuration Examples

#### Basic Configuration
```python
from oxygent.oxy.llms import OpenAILLM

llm = OpenAILLM(
    api_key="${OPENAI_API_KEY}",
    base_url="https://api.openai.com/v1",
    model_name="gpt-4o",
    timeout=120,
    llm_params={
        "temperature": 0.7,
        "max_tokens": 4096,
        "top_p": 0.9
    }
)
```

#### Advanced Configuration
```python
llm = OpenAILLM(
    api_key="${OPENAI_API_KEY}",
    base_url="https://api.openai.com/v1", 
    model_name="gpt-4o",
    timeout=300,
    is_send_think=True,
    is_multimodal_supported=True,
    is_convert_url_to_base64=True,
    max_image_pixels=20000000,
    llm_params={
        "temperature": 0.8,
        "max_tokens": 8192,
        "top_p": 0.95,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1,
        "stop": ["Human:", "AI:"]
    }
)
```

#### Streaming Configuration
```python
streaming_llm = OpenAILLM(
    api_key="${OPENAI_API_KEY}",
    base_url="https://api.openai.com/v1",
    model_name="gpt-4o",
    llm_params={
        "stream": True,
        "temperature": 0.9
    }
)
```

## Core Implementation

### `async _execute(self, oxy_request: OxyRequest) -> OxyResponse`

The main execution method handles both streaming and non-streaming requests with full OpenAI feature support.

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    """Execute a request using the OpenAI API.
    
    Creates a chat completion request using the official AsyncOpenAI client.
    The method handles payload construction, configuration merging, and
    response processing for OpenAI's chat completion API.
    """
```

#### Request Processing Pipeline

1. **Configuration Merging**
```python
# Global LLM configuration
llm_config = Config.get_llm_config()
excluded_keys = {"cls", "base_url", "api_key", "name", "model_name"}
base_config = {k: v for k, v in llm_config.items() if k not in excluded_keys}

# Build request payload
payload = {
    "messages": await self._get_messages(oxy_request),
    "model": self.model_name,
    "stream": False
}

# Apply configurations in order of precedence
payload.update(base_config)          # Global config
payload.update(self.llm_params)      # Instance config  
payload.update(oxy_request.arguments) # Request-specific config
```

2. **Client Initialization**
```python
client = AsyncOpenAI(
    api_key=self.api_key,
    base_url=self.base_url
)
```

3. **API Request Execution**
```python
completion = await client.chat.completions.create(**payload)
```

## Advanced Features

### Streaming Support

OpenAILLM provides sophisticated streaming capabilities with automatic message forwarding:

```python
if payload.get("stream", False):
    answer = ""
    think_start = True
    think_end = False
    
    async for chunk in completion:
        # Handle reasoning content (o1 models)
        if hasattr(chunk.choices[0].delta, "reasoning_content"):
            if think_start:
                await oxy_request.send_message({
                    "type": "stream", 
                    "content": {"delta": "<think>"}
                })
                answer += "<think>"
                think_start = False
                think_end = True
            
            reasoning_char = chunk.choices[0].delta.reasoning_content
            if reasoning_char:
                answer += reasoning_char
                await oxy_request.send_message({
                    "type": "stream",
                    "content": {"delta": reasoning_char}
                })
        
        # Handle regular content
        elif hasattr(chunk.choices[0].delta, "content"):
            if think_end:
                await oxy_request.send_message({
                    "type": "stream",
                    "content": {"delta": "</think>"}
                })
                answer += "</think>"
                think_end = False
            
            content_char = chunk.choices[0].delta.content
            if content_char:
                answer += content_char
                await oxy_request.send_message({
                    "type": "stream",
                    "content": {"delta": content_char}
                })
    
    return OxyResponse(state=OxyState.COMPLETED, output=answer)
```

### Reasoning Content Support

For OpenAI's o1 models, the implementation automatically handles reasoning content:

```python
# Example response structure for o1 models
{
    "choices": [{
        "delta": {
            "reasoning_content": "Let me think about this step by step...",
            "content": "The answer is..."
        }
    }]
}
```

The reasoning content is automatically wrapped in `<think>` tags and streamed to the frontend.

### Multimodal Support

Full support for vision and multimodal inputs:

```python
multimodal_request = OxyRequest(
    arguments={
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                        "detail": "high"  # OpenAI-specific parameter
                    }
                }
            ]
        }]
    }
)
```

## Usage Examples

### Basic Text Generation

```python
from oxygent.oxy.llms import OpenAILLM
from oxygent.schemas import OxyRequest, OxyState

# Initialize
llm = OpenAILLM(
    api_key="${OPENAI_API_KEY}",
    base_url="https://api.openai.com/v1",
    model_name="gpt-4o"
)

# Simple text generation
request = OxyRequest(
    arguments={
        "messages": [
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
)

response = await llm.execute(request)
print(response.output)
```

### Conversation with System Prompt

```python
conversation_request = OxyRequest(
    arguments={
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful AI assistant specialized in software development."
            },
            {
                "role": "user", 
                "content": "How do I implement a binary search algorithm in Python?"
            }
        ],
        "temperature": 0.3,  # Lower temperature for code generation
        "max_tokens": 2000
    }
)

response = await llm.execute(conversation_request)
```

### Function Calling

```python
function_calling_request = OxyRequest(
    arguments={
        "messages": [
            {"role": "user", "content": "What's the weather like in San Francisco?"}
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ],
        "tool_choice": "auto"
    }
)

response = await llm.execute(function_calling_request)
```

### Vision Analysis

```python
vision_request = OxyRequest(
    arguments={
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this chart and provide key insights"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
                        "detail": "high"
                    }
                }
            ]
        }],
        "max_tokens": 1500
    }
)

response = await llm.execute(vision_request)
```

### Streaming Response

```python
streaming_request = OxyRequest(
    arguments={
        "messages": [
            {"role": "user", "content": "Write a detailed story about space exploration"}
        ],
        "stream": True,
        "temperature": 0.8
    }
)

# The streaming response is automatically handled
# Chunks are sent via websocket to frontend
response = await llm.execute(streaming_request)
print("Final response:", response.output)
```

## Error Handling

### Common OpenAI Errors

```python
from openai import OpenAIError, AuthenticationError, RateLimitError

async def execute_with_error_handling(self, oxy_request):
    try:
        return await self._execute(oxy_request)
    
    except AuthenticationError:
        return OxyResponse(
            state=OxyState.FAILED,
            output="Authentication failed. Please check your OpenAI API key."
        )
    
    except RateLimitError:
        return OxyResponse(
            state=OxyState.FAILED,
            output="Rate limit exceeded. Please try again later."
        )
    
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return OxyResponse(
            state=OxyState.FAILED,
            output=self.friendly_error_text
        )
```

### Token Limit Handling

```python
def validate_token_limits(self, messages: list, model_name: str):
    """Validate that the request doesn't exceed model token limits"""
    token_limits = {
        "gpt-4o": 128000,
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384
    }
    
    estimated_tokens = self.estimate_tokens(messages)
    limit = token_limits.get(model_name, 4096)
    
    if estimated_tokens > limit * 0.8:  # 80% safety margin
        raise ValueError(
            f"Request may exceed token limit for {model_name}. "
            f"Estimated: {estimated_tokens}, Limit: {limit}"
        )
```

## Performance Optimization

### Connection Pooling

```python
from openai import AsyncOpenAI
import asyncio

class OptimizedOpenAILLM(OpenAILLM):
    _client_pool = {}
    _lock = asyncio.Lock()
    
    async def get_client(self):
        """Get or create a pooled client"""
        key = (self.api_key, self.base_url)
        
        async with self._lock:
            if key not in self._client_pool:
                self._client_pool[key] = AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            return self._client_pool[key]
```

### Response Caching

```python
import hashlib
import json
from typing import Optional

class CachedOpenAILLM(OpenAILLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}  # Use Redis in production
    
    def get_cache_key(self, payload: dict) -> str:
        cache_data = {
            "model": payload["model"],
            "messages": payload["messages"],
            "temperature": payload.get("temperature", 1.0),
            "max_tokens": payload.get("max_tokens")
        }
        return hashlib.sha256(
            json.dumps(cache_data, sort_keys=True).encode()
        ).hexdigest()
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        payload = self.build_payload(oxy_request)
        
        # Skip caching for streaming requests
        if payload.get("stream", False):
            return await super()._execute(oxy_request)
        
        cache_key = self.get_cache_key(payload)
        
        if cache_key in self.cache:
            return OxyResponse(
                state=OxyState.COMPLETED,
                output=self.cache[cache_key]
            )
        
        response = await super()._execute(oxy_request)
        
        if response.state == OxyState.COMPLETED:
            self.cache[cache_key] = response.output
        
        return response
```

## Testing Strategies

### Unit Testing

```python
import pytest
from unittest.mock import AsyncMock, patch
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types import CompletionUsage

class TestOpenAILLM:
    @pytest.fixture
    def llm(self):
        return OpenAILLM(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            model_name="gpt-4o"
        )
    
    @pytest.mark.asyncio
    @patch('openai.AsyncOpenAI.chat.completions.create')
    async def test_non_streaming_execution(self, mock_create, llm):
        # Mock OpenAI response
        mock_response = ChatCompletion(
            id="chatcmpl-test",
            choices=[{
                "index": 0,
                "message": ChatCompletionMessage(
                    role="assistant",
                    content="Test response"
                ),
                "finish_reason": "stop"
            }],
            created=1234567890,
            model="gpt-4o",
            usage=CompletionUsage(
                completion_tokens=10,
                prompt_tokens=5,
                total_tokens=15
            )
        )
        mock_create.return_value = mock_response
        
        request = OxyRequest(
            arguments={
                "messages": [{"role": "user", "content": "Test"}]
            }
        )
        
        response = await llm.execute(request)
        
        assert response.state == OxyState.COMPLETED
        assert response.output == "Test response"
        mock_create.assert_called_once()
```

### Integration Testing

```python
@pytest.mark.integration 
class TestOpenAIIntegration:
    @pytest.mark.asyncio
    async def test_real_openai_api(self):
        """Test with real OpenAI API (requires valid API key)"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OpenAI API key not available")
        
        llm = OpenAILLM(
            api_key=api_key,
            base_url="https://api.openai.com/v1",
            model_name="gpt-3.5-turbo"  # Use cheaper model for tests
        )
        
        request = OxyRequest(
            arguments={
                "messages": [{"role": "user", "content": "Say 'Hello, World!'"}],
                "max_tokens": 10
            }
        )
        
        response = await llm.execute(request)
        
        assert response.state == OxyState.COMPLETED
        assert "Hello" in response.output
```

## Security Considerations

### API Key Protection

```python
import os
from typing import Optional

class SecureOpenAILLM(OpenAILLM):
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        # Use environment variable if not provided
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        # Validate API key format
        if not api_key.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
        
        super().__init__(api_key=api_key, **kwargs)
    
    def __repr__(self):
        # Don't expose API key in string representation
        return f"OpenAILLM(model={self.model_name}, base_url={self.base_url})"
```

### Input Sanitization

```python
def sanitize_messages(self, messages: list) -> list:
    """Sanitize input messages to prevent prompt injection"""
    sanitized = []
    
    for message in messages:
        if isinstance(message.get("content"), str):
            # Remove potentially dangerous patterns
            content = message["content"]
            content = re.sub(r'<\|.*?\|>', '', content)  # Remove special tokens
            content = content.strip()
            
            sanitized.append({
                "role": message["role"],
                "content": content
            })
        else:
            sanitized.append(message)  # Preserve multimodal content
    
    return sanitized
```

## Monitoring and Observability

### Request Logging

```python
import logging
import time

logger = logging.getLogger(__name__)

class ObservableOpenAILLM(OpenAILLM):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        start_time = time.time()
        
        try:
            # Log request start
            logger.info(
                "OpenAI request started",
                extra={
                    "trace_id": oxy_request.current_trace_id,
                    "node_id": oxy_request.node_id,
                    "model": self.model_name,
                    "message_count": len(oxy_request.arguments.get("messages", []))
                }
            )
            
            response = await super()._execute(oxy_request)
            
            # Log successful completion
            logger.info(
                "OpenAI request completed",
                extra={
                    "trace_id": oxy_request.current_trace_id,
                    "node_id": oxy_request.node_id,
                    "model": self.model_name,
                    "response_length": len(response.output) if response.output else 0,
                    "duration_seconds": time.time() - start_time,
                    "state": response.state.name
                }
            )
            
            return response
            
        except Exception as e:
            # Log errors
            logger.error(
                f"OpenAI request failed: {e}",
                extra={
                    "trace_id": oxy_request.current_trace_id,
                    "node_id": oxy_request.node_id,
                    "model": self.model_name,
                    "duration_seconds": time.time() - start_time,
                    "error_type": type(e).__name__
                }
            )
            raise
```

### Usage Tracking

```python
class MetricsTrackingOpenAILLM(OpenAILLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_count = 0
        self.total_tokens = 0
        self.error_count = 0
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        self.request_count += 1
        
        try:
            response = await super()._execute(oxy_request)
            
            # Track token usage (if available in response)
            if hasattr(response, 'extra') and 'usage' in response.extra:
                self.total_tokens += response.extra['usage'].total_tokens
            
            return response
            
        except Exception as e:
            self.error_count += 1
            raise
    
    def get_metrics(self) -> dict:
        return {
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1)
        }
```

## Best Practices

### Production Configuration

1. **Environment Variables**: Use environment variables for sensitive configuration
2. **Error Handling**: Implement comprehensive error handling and user-friendly messages
3. **Logging**: Add structured logging with trace IDs for debugging
4. **Monitoring**: Track usage, performance, and error rates
5. **Security**: Sanitize inputs and protect API keys

### Performance Tuning

1. **Model Selection**: Choose appropriate models for your use case (cost vs. capability)
2. **Token Management**: Monitor and optimize token usage
3. **Caching**: Implement response caching for repeated queries
4. **Streaming**: Use streaming for long responses to improve user experience
5. **Connection Pooling**: Reuse HTTP connections for better performance

### Development Guidelines

1. **Testing**: Write comprehensive tests including integration tests with real API
2. **Mocking**: Use proper mocking for unit tests to avoid API costs
3. **Configuration**: Use flexible configuration that works in different environments
4. **Documentation**: Document model-specific features and limitations

## Next Steps

- [HttpLLM](./http-llm) - Generic HTTP client for other providers
- [LLM Configuration Guide](../configuration/openai-config) - Detailed OpenAI configuration
- [Streaming Implementation](../guides/streaming-setup) - Set up real-time streaming
- [Function Calling Guide](../guides/function-calling) - Implement tool use with OpenAI
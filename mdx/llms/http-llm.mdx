---
title: HttpLLM - Universal HTTP Client
description: Generic HTTP client implementation supporting multiple LLM providers with automatic API format detection
---

# HttpLLM - Universal HTTP Client

The `HttpLLM` class provides a flexible, universal HTTP client implementation that can work with multiple Large Language Model providers over HTTP. It features intelligent API format detection, automatic endpoint configuration, and comprehensive support for OpenAI-compatible APIs, Google Gemini, Ollama, and custom LLM services.

## Class Overview

```python
from oxygent.oxy.llms.http_llm import HttpLLM
from oxygent.oxy.llms.remote_llm import RemoteLLM
import httpx
```

`HttpLLM` extends `RemoteLLM` to provide a generic HTTP client that can adapt to different API formats and authentication schemes automatically.

## Class Definition

```python
class HttpLLM(RemoteLLM):
    """HTTP-based Large Language Model implementation.
    
    This class provides a concrete implementation of RemoteLLM for communicating
    with remote LLM APIs over HTTP. It handles API authentication, request
    formatting, and response parsing for OpenAI-compatible APIs.
    """
```

## Supported Providers

### OpenAI-Compatible APIs
- **OpenAI**: Official OpenAI API
- **Azure OpenAI**: Microsoft's OpenAI service
- **Anthropic**: Claude models via OpenAI-compatible wrapper
- **Custom APIs**: Any service following OpenAI chat completions format

### Google Gemini
- **Gemini Pro**: Google's large language model
- **Gemini Pro Vision**: Multimodal capabilities
- **Vertex AI**: Google Cloud AI integration

### Ollama
- **Local Models**: Self-hosted model serving
- **Docker Deployments**: Containerized model instances
- **Custom Models**: Fine-tuned and specialized models

### Other Providers
- **Hugging Face Inference API**: Hosted model serving
- **Together AI**: Multiple model hosting
- **Replicate**: Cloud-based model serving
- **Custom Endpoints**: Any HTTP-based LLM service

## API Format Detection

HttpLLM automatically detects and adapts to different API formats based on the base URL:

```python
def detect_api_format(self, url: str) -> tuple[str, bool]:
    """
    Detect API format based on URL patterns
    Returns: (format_type, uses_openai_format)
    """
    url_lower = url.lower()
    
    if "generativelanguage.googleapis.com" in url_lower:
        return ("gemini", False)
    elif self.api_key and "ollama" not in url_lower:
        return ("openai", True)  
    else:
        return ("ollama", True)
```

### Automatic Endpoint Configuration

```python
def build_endpoint_url(self, base_url: str, format_type: str) -> str:
    """Build appropriate endpoint URL based on API format"""
    url = base_url.rstrip("/")
    
    if format_type == "gemini":
        if not url.endswith(":generateContent"):
            url = f"{url}/models/{self.model_name}:generateContent"
    elif format_type == "openai":
        if not url.endswith("/chat/completions"):
            url = f"{url}/chat/completions"
    elif format_type == "ollama":
        if not url.endswith("/api/chat"):
            url = f"{url}/api/chat"
    
    return url
```

## Authentication Methods

### Bearer Token Authentication (OpenAI-compatible)
```python
headers = {
    "Authorization": f"Bearer {self.api_key}",
    "Content-Type": "application/json"
}
```

### API Key Header (Google Gemini)
```python
headers = {
    "X-goog-api-key": self.api_key,
    "Content-Type": "application/json"
}
```

### No Authentication (Local Ollama)
```python
headers = {
    "Content-Type": "application/json"
}
```

## Core Implementation

### `async _execute(self, oxy_request: OxyRequest) -> OxyResponse`

The main execution method handles multiple API formats with automatic adaptation:

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    """Execute an HTTP request to the remote LLM API.
    
    Sends a formatted request to the remote LLM API and processes the response.
    The method handles authentication, payload construction, and response parsing
    for OpenAI-compatible APIs.
    """
```

#### Request Processing Pipeline

1. **URL and Format Detection**
```python
url = self.base_url.rstrip("/")
is_gemini = "generativelanguage.googleapis.com" in url
use_openai = (self.api_key is not None) and (not is_gemini)

# Configure endpoint URLs
if is_gemini:
    if not url.endswith(":generateContent"):
        url = f"{url}/models/{self.model_name}:generateContent"
elif use_openai:
    if not url.endswith("/chat/completions"):
        url = f"{url}/chat/completions"
else:  # Ollama
    if not url.endswith("/api/chat"):
        url = f"{url}/api/chat"
```

2. **Authentication Header Setup**
```python
headers = {"Content-Type": "application/json"}

if is_gemini:
    headers["X-goog-api-key"] = self.api_key
elif use_openai:
    headers["Authorization"] = f"Bearer {self.api_key}"
# No additional auth needed for local Ollama
```

3. **Payload Format Adaptation**
```python
if is_gemini:
    # Convert to Gemini format
    raw_msgs = await self._get_messages(oxy_request)
    contents = [
        {
            "role": ("user" if m["role"] == "user" else "model"),
            "parts": [{"text": m["content"]}]
        }
        for m in raw_msgs if m.get("content")
    ]
    payload = {"contents": contents}
else:
    # Use OpenAI format (works for OpenAI and Ollama)
    payload = {
        "messages": await self._get_messages(oxy_request),
        "model": self.model_name,
        "stream": False
    }
```

## Configuration Examples

### OpenAI-Compatible API Configuration

```python
from oxygent.oxy.llms import HttpLLM

# OpenAI
openai_llm = HttpLLM(
    api_key="${OPENAI_API_KEY}",
    base_url="https://api.openai.com/v1",
    model_name="gpt-4o",
    llm_params={
        "temperature": 0.7,
        "max_tokens": 4096
    }
)

# Azure OpenAI
azure_llm = HttpLLM(
    api_key="${AZURE_OPENAI_KEY}",
    base_url="https://your-resource.openai.azure.com",
    model_name="gpt-4",
    llm_params={
        "temperature": 0.8,
        "max_tokens": 2048
    }
)

# Anthropic via OpenAI-compatible proxy
anthropic_llm = HttpLLM(
    api_key="${ANTHROPIC_API_KEY}",
    base_url="https://api.anthropic.com/v1",
    model_name="claude-3-sonnet",
    llm_params={
        "temperature": 0.6,
        "max_tokens": 8192
    }
)
```

### Google Gemini Configuration

```python
# Google Gemini Pro
gemini_llm = HttpLLM(
    api_key="${GOOGLE_API_KEY}",
    base_url="https://generativelanguage.googleapis.com/v1beta",
    model_name="gemini-pro",
    llm_params={
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
)

# Gemini Pro Vision (multimodal)
gemini_vision_llm = HttpLLM(
    api_key="${GOOGLE_API_KEY}",
    base_url="https://generativelanguage.googleapis.com/v1beta",
    model_name="gemini-pro-vision",
    is_multimodal_supported=True,
    is_convert_url_to_base64=True,
    llm_params={
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 4096
        }
    }
)
```

### Ollama Configuration

```python
# Local Ollama instance
ollama_llm = HttpLLM(
    api_key=None,  # No API key needed for local Ollama
    base_url="http://localhost:11434",
    model_name="llama2:7b",
    llm_params={
        "temperature": 0.8,
        "num_predict": 2048,
        "top_p": 0.9
    }
)

# Remote Ollama instance
remote_ollama_llm = HttpLLM(
    api_key=None,
    base_url="http://your-ollama-server:11434",
    model_name="codellama:13b",
    llm_params={
        "temperature": 0.2,  # Lower for code generation
        "num_predict": 4096
    }
)
```

## Streaming Support

HttpLLM provides comprehensive streaming support with automatic format detection:

```python
async def handle_streaming_request(self, oxy_request: OxyRequest) -> OxyResponse:
    """Handle streaming responses from various API formats"""
    payload = await self.build_payload(oxy_request)
    
    if not payload.get("stream", False):
        return await self.handle_non_streaming_request(oxy_request)
    
    result_parts = []
    
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST", 
            self.build_endpoint_url(),
            headers=self.build_headers(),
            json=payload
        ) as resp:
            async for line in resp.aiter_lines():
                if not line or not line.startswith("data:"):
                    continue
                    
                line = line[5:].strip()  # Remove "data:" prefix
                
                if line == "[DONE]":
                    break
                
                try:
                    chunk = json.loads(line)
                    delta_content = self.extract_delta_content(chunk)
                    
                    if delta_content:
                        result_parts.append(delta_content)
                        await oxy_request.send_message({
                            "type": "stream",
                            "content": {"delta": delta_content}
                        })
                        
                except json.JSONDecodeError:
                    continue
    
    return OxyResponse(
        state=OxyState.COMPLETED,
        output="".join(result_parts)
    )

def extract_delta_content(self, chunk: dict, api_format: str) -> str:
    """Extract content from streaming chunk based on API format"""
    if api_format == "openai":
        return (
            chunk.get("choices", [{}])[0]
            .get("delta", {})
            .get("content", "") or
            chunk.get("choices", [{}])[0]
            .get("delta", {})
            .get("reasoning_content", "")
        )
    elif api_format == "ollama":
        return chunk.get("message", {}).get("content", "")
    else:
        return ""
```

## Usage Examples

### Basic Text Generation

```python
from oxygent.oxy.llms import HttpLLM
from oxygent.schemas import OxyRequest

# Configure for any OpenAI-compatible API
llm = HttpLLM(
    api_key="${API_KEY}",
    base_url="https://api.example.com/v1",
    model_name="your-model-name"
)

request = OxyRequest(
    arguments={
        "messages": [
            {"role": "user", "content": "Explain machine learning in simple terms"}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
)

response = await llm.execute(request)
print(response.output)
```

### Multi-Provider Setup

```python
# Configure multiple providers
providers = {
    "openai": HttpLLM(
        api_key="${OPENAI_API_KEY}",
        base_url="https://api.openai.com/v1",
        model_name="gpt-4o"
    ),
    "gemini": HttpLLM(
        api_key="${GOOGLE_API_KEY}",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        model_name="gemini-pro"
    ),
    "ollama": HttpLLM(
        base_url="http://localhost:11434",
        model_name="llama2:7b"
    )
}

async def query_all_providers(query: str):
    request = OxyRequest(arguments={"query": query})
    
    results = {}
    for name, llm in providers.items():
        try:
            response = await llm.execute(request)
            results[name] = response.output
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results
```

### Multimodal Processing with Gemini

```python
gemini_vision = HttpLLM(
    api_key="${GOOGLE_API_KEY}",
    base_url="https://generativelanguage.googleapis.com/v1beta",
    model_name="gemini-pro-vision",
    is_multimodal_supported=True
)

multimodal_request = OxyRequest(
    arguments={
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe what you see in this image"},
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."}
                }
            ]
        }]
    }
)

response = await gemini_vision.execute(multimodal_request)
```

### Streaming Example

```python
streaming_llm = HttpLLM(
    api_key="${API_KEY}",
    base_url="https://api.example.com/v1",
    model_name="your-model"
)

streaming_request = OxyRequest(
    arguments={
        "messages": [{"role": "user", "content": "Write a short story"}],
        "stream": True,
        "temperature": 0.8
    }
)

# Streaming chunks are automatically sent to frontend
response = await streaming_llm.execute(streaming_request)
print("Complete response:", response.output)
```

## Error Handling and Recovery

### Provider-Specific Error Handling

```python
class RobustHttpLLM(HttpLLM):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        try:
            return await super()._execute(oxy_request)
            
        except httpx.HTTPStatusError as e:
            return self.handle_http_error(e)
        except httpx.TimeoutException:
            return OxyResponse(
                state=OxyState.FAILED,
                output="Request timed out. Please try again."
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return OxyResponse(
                state=OxyState.FAILED,
                output=self.friendly_error_text
            )
    
    def handle_http_error(self, error: httpx.HTTPStatusError) -> OxyResponse:
        status = error.response.status_code
        
        if status == 401:
            return OxyResponse(
                state=OxyState.FAILED,
                output="Authentication failed. Please check your API key."
            )
        elif status == 429:
            return OxyResponse(
                state=OxyState.FAILED,
                output="Rate limit exceeded. Please try again later."
            )
        elif status >= 500:
            return OxyResponse(
                state=OxyState.FAILED,
                output="Server error. Please try again."
            )
        else:
            try:
                error_data = error.response.json()
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                return OxyResponse(
                    state=OxyState.FAILED,
                    output=f"API Error: {error_message}"
                )
            except:
                return OxyResponse(
                    state=OxyState.FAILED,
                    output=f"HTTP {status} Error"
                )
```

### Automatic Failover

```python
class FailoverHttpLLM(HttpLLM):
    def __init__(self, primary_config: dict, fallback_configs: list, **kwargs):
        super().__init__(**primary_config, **kwargs)
        self.fallback_llms = [HttpLLM(**config, **kwargs) for config in fallback_configs]
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Try primary LLM
        try:
            return await super()._execute(oxy_request)
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}, trying fallbacks")
            
            # Try fallback LLMs
            for i, fallback_llm in enumerate(self.fallback_llms):
                try:
                    logger.info(f"Attempting fallback LLM {i+1}")
                    return await fallback_llm._execute(oxy_request)
                except Exception as fallback_error:
                    logger.warning(f"Fallback LLM {i+1} failed: {fallback_error}")
                    continue
            
            # All LLMs failed
            return OxyResponse(
                state=OxyState.FAILED,
                output="All LLM providers failed. Please try again later."
            )
```

## Performance Optimization

### Connection Pooling and Reuse

```python
import httpx
from contextlib import asynccontextmanager

class OptimizedHttpLLM(HttpLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = None
    
    async def get_client(self):
        if self.client is None:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100,
                    keepalive_expiry=30.0
                ),
                headers=self.build_default_headers()
            )
        return self.client
    
    async def __aenter__(self):
        await self.get_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
            self.client = None
```

### Request Batching

```python
class BatchingHttpLLM(HttpLLM):
    def __init__(self, max_batch_size: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.max_batch_size = max_batch_size
        self.pending_requests = []
    
    async def execute_batch(self, requests: list[OxyRequest]) -> list[OxyResponse]:
        """Execute multiple requests in a single API call (if supported)"""
        if not self.supports_batching():
            # Execute individually if batching not supported
            tasks = [self.execute(req) for req in requests]
            return await asyncio.gather(*tasks)
        
        # Combine requests into batch payload
        batch_payload = self.create_batch_payload(requests)
        
        # Execute batch request
        response = await self.execute_http_request(batch_payload)
        
        # Split response back into individual responses
        return self.split_batch_response(response, requests)
```

### Response Caching

```python
import hashlib
import json
from typing import Optional
import time

class CachingHttpLLM(HttpLLM):
    def __init__(self, cache_ttl: int = 3600, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    def get_cache_key(self, oxy_request: OxyRequest) -> str:
        """Generate cache key from request parameters"""
        cache_data = {
            "base_url": self.base_url,
            "model_name": self.model_name,
            "messages": oxy_request.arguments.get("messages", []),
            "temperature": oxy_request.arguments.get("temperature", 1.0),
            "max_tokens": oxy_request.arguments.get("max_tokens")
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Skip caching for streaming requests
        if oxy_request.arguments.get("stream", False):
            return await super()._execute(oxy_request)
        
        cache_key = self.get_cache_key(oxy_request)
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return OxyResponse(
                    state=OxyState.COMPLETED,
                    output=cached_data
                )
        
        # Execute request
        response = await super()._execute(oxy_request)
        
        # Cache successful responses
        if response.state == OxyState.COMPLETED:
            self.cache[cache_key] = (response.output, time.time())
        
        return response
```

## Testing Strategies

### Mock Testing

```python
import pytest
from unittest.mock import AsyncMock, patch
import httpx

class TestHttpLLM:
    @pytest.fixture
    def llm(self):
        return HttpLLM(
            api_key="test-key",
            base_url="https://api.test.com/v1",
            model_name="test-model"
        )
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_openai_format_request(self, mock_post, llm):
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        request = OxyRequest(
            arguments={"messages": [{"role": "user", "content": "Test"}]}
        )
        
        response = await llm.execute(request)
        
        assert response.state == OxyState.COMPLETED
        assert response.output == "Test response"
        
        # Verify request format
        call_args = mock_post.call_args
        assert "chat/completions" in call_args[1]["url"]
        assert "Bearer test-key" in call_args[1]["headers"]["Authorization"]
    
    @pytest.mark.asyncio
    async def test_gemini_format_detection(self, llm):
        llm.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {
                "candidates": [{"content": {"parts": [{"text": "Gemini response"}]}}]
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            request = OxyRequest(
                arguments={"messages": [{"role": "user", "content": "Test"}]}
            )
            
            response = await llm.execute(request)
            
            # Verify Gemini-specific formatting
            call_args = mock_post.call_args
            assert ":generateContent" in call_args[1]["url"]
            assert "X-goog-api-key" in call_args[1]["headers"]
            payload = call_args[1]["json"]
            assert "contents" in payload
```

### Integration Testing

```python
@pytest.mark.integration
class TestHttpLLMIntegration:
    @pytest.mark.asyncio
    async def test_ollama_integration(self):
        """Test with local Ollama instance"""
        llm = HttpLLM(
            base_url="http://localhost:11434",
            model_name="llama2:7b"
        )
        
        # Check if Ollama is running
        try:
            async with httpx.AsyncClient() as client:
                await client.get("http://localhost:11434/api/tags", timeout=5.0)
        except:
            pytest.skip("Ollama not running locally")
        
        request = OxyRequest(
            arguments={
                "messages": [{"role": "user", "content": "Say hello"}],
                "temperature": 0.1
            }
        )
        
        response = await llm.execute(request)
        assert response.state == OxyState.COMPLETED
        assert len(response.output) > 0
```

## Security Best Practices

### API Key Protection

```python
import os
from typing import Optional

def secure_api_key_loading(provider: str) -> Optional[str]:
    """Securely load API key from environment"""
    key_mappings = {
        "openai": "OPENAI_API_KEY",
        "google": "GOOGLE_API_KEY", 
        "anthropic": "ANTHROPIC_API_KEY",
        "azure": "AZURE_OPENAI_KEY"
    }
    
    env_var = key_mappings.get(provider)
    if not env_var:
        return None
    
    api_key = os.getenv(env_var)
    if api_key and len(api_key) > 10:  # Basic validation
        return api_key
    
    raise ValueError(f"Invalid or missing API key for {provider}")
```

### Input Sanitization

```python
def sanitize_request_payload(self, payload: dict) -> dict:
    """Sanitize payload to prevent injection attacks"""
    sanitized = payload.copy()
    
    # Sanitize messages
    if "messages" in sanitized:
        sanitized["messages"] = [
            self.sanitize_message(msg) for msg in sanitized["messages"]
        ]
    
    # Remove potentially dangerous parameters
    dangerous_params = ["eval", "exec", "system", "shell"]
    for param in dangerous_params:
        sanitized.pop(param, None)
    
    return sanitized

def sanitize_message(self, message: dict) -> dict:
    """Sanitize individual message content"""
    sanitized = message.copy()
    
    if isinstance(message.get("content"), str):
        content = message["content"]
        # Remove potential command injection patterns
        content = re.sub(r'[`${}]', '', content)
        sanitized["content"] = content
    
    return sanitized
```

## Monitoring and Observability

### Request/Response Logging

```python
import logging
import time

logger = logging.getLogger(__name__)

class ObservableHttpLLM(HttpLLM):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        start_time = time.time()
        
        # Log request details
        logger.info(
            "HTTP LLM request started",
            extra={
                "trace_id": oxy_request.current_trace_id,
                "node_id": oxy_request.node_id,
                "base_url": self.base_url,
                "model_name": self.model_name,
                "api_format": self.detect_api_format(self.base_url)[0]
            }
        )
        
        try:
            response = await super()._execute(oxy_request)
            
            # Log successful completion
            logger.info(
                "HTTP LLM request completed",
                extra={
                    "trace_id": oxy_request.current_trace_id,
                    "node_id": oxy_request.node_id,
                    "duration_seconds": time.time() - start_time,
                    "response_length": len(response.output) if response.output else 0,
                    "state": response.state.name
                }
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"HTTP LLM request failed: {e}",
                extra={
                    "trace_id": oxy_request.current_trace_id,
                    "node_id": oxy_request.node_id,
                    "duration_seconds": time.time() - start_time,
                    "error_type": type(e).__name__,
                    "base_url": self.base_url
                }
            )
            raise
```

### Metrics Collection

```python
from collections import defaultdict
import time

class MetricsHttpLLM(HttpLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metrics = {
            "requests_total": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "total_response_time": 0.0,
            "provider_metrics": defaultdict(lambda: {
                "requests": 0,
                "successes": 0,
                "failures": 0
            })
        }
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        provider = self.detect_api_format(self.base_url)[0]
        start_time = time.time()
        
        self.metrics["requests_total"] += 1
        self.metrics["provider_metrics"][provider]["requests"] += 1
        
        try:
            response = await super()._execute(oxy_request)
            
            self.metrics["requests_successful"] += 1
            self.metrics["provider_metrics"][provider]["successes"] += 1
            
            response_time = time.time() - start_time
            self.metrics["total_response_time"] += response_time
            
            return response
            
        except Exception as e:
            self.metrics["requests_failed"] += 1
            self.metrics["provider_metrics"][provider]["failures"] += 1
            raise
    
    def get_metrics(self) -> dict:
        total_requests = self.metrics["requests_total"]
        return {
            "total_requests": total_requests,
            "success_rate": self.metrics["requests_successful"] / max(total_requests, 1),
            "average_response_time": self.metrics["total_response_time"] / max(
                self.metrics["requests_successful"], 1
            ),
            "provider_breakdown": dict(self.metrics["provider_metrics"])
        }
```

## Best Practices

### Configuration Management

1. **Environment Variables**: Use environment variables for sensitive configuration
2. **Provider Detection**: Implement robust provider detection logic
3. **Fallback Configuration**: Set up fallback providers for reliability
4. **Timeout Management**: Configure appropriate timeouts for different providers

### Performance Optimization

1. **Connection Pooling**: Reuse HTTP connections for better performance
2. **Request Batching**: Batch multiple requests when supported
3. **Response Caching**: Cache responses for identical requests
4. **Streaming**: Use streaming for long responses

### Error Handling

1. **Graceful Degradation**: Handle provider failures gracefully
2. **Retry Logic**: Implement exponential backoff for transient failures
3. **Error Classification**: Distinguish between different error types
4. **User-Friendly Messages**: Provide clear error messages to users

### Security

1. **API Key Security**: Never log or expose API keys
2. **Input Validation**: Sanitize all input data
3. **Rate Limiting**: Implement client-side rate limiting
4. **HTTPS Only**: Always use HTTPS for API communications

## Next Steps

- [LLM Configuration Guide](../configuration/http-llm-config) - Detailed HTTP LLM configuration
- [Provider Integration Guide](../guides/provider-integration) - Add new LLM providers
- [Error Handling Guide](../guides/error-handling) - Comprehensive error handling strategies
- [Performance Tuning](../guides/performance-tuning) - Optimize LLM performance
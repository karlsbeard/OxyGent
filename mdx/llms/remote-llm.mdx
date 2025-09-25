---
title: RemoteLLM - Remote API Base Class
description: Abstract base class for remote LLM API integrations with authentication and configuration validation
---

# RemoteLLM - Remote API Base Class

The `RemoteLLM` class serves as an intermediate abstract base class between `BaseLLM` and specific remote LLM provider implementations. It provides essential infrastructure for communicating with remote LLM APIs, including authentication management, configuration validation, and standardized error handling.

## Class Overview

```python
from oxygent.oxy.llms.remote_llm import RemoteLLM
from oxygent.oxy.llms.base_llm import BaseLLM
from pydantic import Field, field_validator
```

`RemoteLLM` extends `BaseLLM` to add remote API-specific functionality while maintaining the unified LLM interface.

## Class Definition

```python
class RemoteLLM(BaseLLM):
    """Large Language Model implementation for remote APIs.
    
    This class provides a concrete implementation of BaseLLM for communicating
    with remote LLM APIs. It handles API authentication, request
    formatting, and response parsing for OpenAI-compatible APIs.
    """
```

## Attributes

### Authentication & Connection

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `Optional[str]` | `None` | The API key for authentication with the LLM service |
| `base_url` | `Optional[str]` | `""` | The base URL endpoint for the LLM API |
| `model_name` | `Optional[str]` | `""` | The specific model name to use for requests |

### Configuration Requirements

All remote LLM implementations require three essential configuration parameters:

1. **API Key**: Authentication credentials for the remote service
2. **Base URL**: The endpoint URL for API requests  
3. **Model Name**: The specific model identifier to use

## Field Validation

The `RemoteLLM` class implements strict field validation to ensure proper configuration:

### `@field_validator("base_url", "model_name")`

```python
@field_validator("base_url", "model_name")
@classmethod
def not_empty(cls, value, info):
    key = info.field_name
    
    # Check for None values
    if value is None:
        raise ValueError(
            f"Environment variable '{key}' is not set and no default value provided. "
            f"Please check your .env or system env."
        )
    
    # Check for correct type
    if not isinstance(value, str):
        raise ValueError(
            f"Environment variable '{key}' type error: "
            f"expected str, got {type(value).__name__}."
        )
    
    # Check for empty or whitespace-only strings
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    
    return value
```

This validator ensures:
- **Non-null values**: Prevents None values from being assigned
- **Type safety**: Ensures values are strings
- **Non-empty validation**: Prevents empty or whitespace-only strings
- **Environment variable guidance**: Provides clear error messages for missing configuration

## Configuration Examples

### Environment Variable Configuration

The most secure and recommended approach is using environment variables:

```bash
# .env file or system environment
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-3-sonnet

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b
```

### Direct Configuration

```python
from oxygent.oxy.llms import OpenAILLM

# Direct instantiation (not recommended for production)
llm = OpenAILLM(
    api_key="sk-your-api-key",
    base_url="https://api.openai.com/v1", 
    model_name="gpt-4o"
)
```

### Config System Integration

```python
from oxygent.config import Config

# Configuration through Config system
Config.set_llm_config({
    "api_key": "${OPENAI_API_KEY}",     # Environment variable reference
    "base_url": "${OPENAI_BASE_URL}",   # Environment variable reference  
    "model_name": "${OPENAI_MODEL}"     # Environment variable reference
})

# Usage
llm_config = Config.get_llm_config()
llm = OpenAILLM(**llm_config)
```

## Abstract Method Implementation

### `async _execute(self, oxy_request: OxyRequest) -> OxyResponse`

`RemoteLLM` declares but does not implement the `_execute` method, leaving it as abstract for concrete implementations:

```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    raise NotImplementedError("This method is not yet implemented")
```

Concrete implementations must provide the actual LLM API integration logic:

```python
class MyRemoteLLM(RemoteLLM):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # 1. Extract and process messages
        messages = await self._get_messages(oxy_request)
        
        # 2. Build API request payload
        payload = {
            "messages": messages,
            "model": self.model_name,
            **self.llm_params,
            **oxy_request.arguments
        }
        
        # 3. Make authenticated API request
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = await self.make_api_request(payload, headers)
        
        # 4. Process and return response
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=response.get("content", "")
        )
```

## Common Implementation Patterns

### Authentication Patterns

#### Bearer Token Authentication
```python
headers = {
    "Authorization": f"Bearer {self.api_key}",
    "Content-Type": "application/json"
}
```

#### API Key Header Authentication
```python
headers = {
    "X-API-Key": self.api_key,
    "Content-Type": "application/json" 
}
```

#### Provider-Specific Authentication
```python
# Google APIs
headers = {"X-goog-api-key": self.api_key}

# Custom header schemes
headers = {"API-Token": self.api_key}
```

### URL Construction Patterns

#### OpenAI-Compatible APIs
```python
def build_url(self):
    base = self.base_url.rstrip("/")
    if not base.endswith("/chat/completions"):
        return f"{base}/chat/completions"
    return base
```

#### Provider-Specific Endpoints
```python
def build_url(self):
    base = self.base_url.rstrip("/")
    if "generativelanguage.googleapis.com" in base:
        return f"{base}/models/{self.model_name}:generateContent"
    elif "ollama" in base:
        return f"{base}/api/chat"
    else:
        return f"{base}/chat/completions"
```

### Request Payload Construction

#### Standard OpenAI Format
```python
async def build_payload(self, oxy_request: OxyRequest) -> dict:
    # Get processed messages
    messages = await self._get_messages(oxy_request)
    
    # Base payload
    payload = {
        "messages": messages,
        "model": self.model_name,
        "stream": False
    }
    
    # Add global LLM configuration
    llm_config = Config.get_llm_config()
    excluded_keys = {"cls", "base_url", "api_key", "name", "model_name"}
    for key, value in llm_config.items():
        if key not in excluded_keys:
            payload[key] = value
    
    # Add instance-specific parameters
    payload.update(self.llm_params)
    
    # Add request-specific parameters
    for key, value in oxy_request.arguments.items():
        if key != "messages":
            payload[key] = value
    
    return payload
```

#### Provider-Specific Format Adaptation
```python
def adapt_payload_for_provider(self, base_payload: dict) -> dict:
    if self.is_gemini_api():
        # Convert OpenAI format to Gemini format
        return {
            "contents": [
                {
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [{"text": msg["content"]}]
                }
                for msg in base_payload["messages"]
            ]
        }
    elif self.is_ollama_api():
        # Ollama-specific adaptations
        return base_payload
    else:
        # Standard OpenAI format
        return base_payload
```

## Error Handling Strategies

### Configuration Validation Errors

```python
try:
    llm = MyRemoteLLM(
        base_url="",  # This will trigger validation error
        model_name="gpt-4o"
    )
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    # Handle configuration error - perhaps load from fallback config
```

### API Authentication Errors

```python
async def handle_auth_errors(self, response):
    if response.status_code == 401:
        raise ValueError(
            f"Authentication failed for {self.__class__.__name__}. "
            f"Please check your API key configuration."
        )
    elif response.status_code == 403:
        raise ValueError(
            f"Access forbidden. Please check your API key permissions."
        )
```

### Connection and Timeout Errors

```python
import asyncio
import httpx

async def make_request_with_retry(self, payload: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.build_url(),
                    json=payload,
                    headers=self.build_headers()
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            if attempt == max_retries - 1:
                raise ValueError("Request timed out after multiple retries")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500 and attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Retry server errors
                continue
            else:
                raise ValueError(f"API request failed: {e.response.text}")
```

## Testing Remote LLM Implementations

### Configuration Validation Testing

```python
import pytest
from pydantic import ValidationError

class TestRemoteLLMValidation:
    def test_empty_base_url_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            MyRemoteLLM(
                base_url="",
                model_name="test-model"
            )
        assert "base_url must be a non-empty string" in str(exc_info.value)
    
    def test_none_model_name_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            MyRemoteLLM(
                base_url="https://api.example.com",
                model_name=None
            )
        assert "Environment variable 'model_name' is not set" in str(exc_info.value)
```

### Mock API Testing

```python
from unittest.mock import AsyncMock, patch

class TestRemoteLLMExecution:
    @pytest.fixture
    def llm(self):
        return MyRemoteLLM(
            api_key="test-key",
            base_url="https://api.example.com",
            model_name="test-model"
        )
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_successful_execution(self, mock_post, llm):
        # Mock successful API response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        request = OxyRequest(arguments={"query": "Test query"})
        response = await llm.execute(request)
        
        assert response.state == OxyState.COMPLETED
        assert "Test response" in response.output
        mock_post.assert_called_once()
```

### Integration Testing

```python
@pytest.mark.integration
class TestRemoteLLMIntegration:
    @pytest.mark.asyncio
    async def test_real_api_integration(self):
        """Test with actual API (requires valid credentials)"""
        llm = MyRemoteLLM(
            api_key=os.getenv("TEST_API_KEY"),
            base_url=os.getenv("TEST_BASE_URL"),
            model_name=os.getenv("TEST_MODEL")
        )
        
        if not all([llm.api_key, llm.base_url, llm.model_name]):
            pytest.skip("Integration test requires API credentials")
        
        request = OxyRequest(
            arguments={
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        
        response = await llm.execute(request)
        assert response.state == OxyState.COMPLETED
        assert isinstance(response.output, str)
        assert len(response.output) > 0
```

## Security Best Practices

### API Key Management

1. **Environment Variables**: Always use environment variables for API keys
2. **Key Rotation**: Implement regular key rotation procedures
3. **Access Scoping**: Use API keys with minimal required permissions
4. **Monitoring**: Log API key usage and monitor for anomalies

```python
import os
from cryptography.fernet import Fernet

class SecureRemoteLLM(RemoteLLM):
    def __init__(self, **kwargs):
        # Decrypt API key if encrypted
        encrypted_key = kwargs.get("api_key")
        if encrypted_key and encrypted_key.startswith("encrypted:"):
            key_data = encrypted_key.replace("encrypted:", "")
            kwargs["api_key"] = self.decrypt_api_key(key_data)
        
        super().__init__(**kwargs)
    
    def decrypt_api_key(self, encrypted_data: str) -> str:
        encryption_key = os.getenv("API_KEY_ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("Encryption key not found in environment")
        
        f = Fernet(encryption_key.encode())
        return f.decrypt(encrypted_data.encode()).decode()
```

### Request Security

```python
def sanitize_payload(self, payload: dict) -> dict:
    """Remove sensitive information from request payload before logging"""
    safe_payload = payload.copy()
    
    # Remove or mask sensitive fields
    sensitive_fields = ["api_key", "authorization", "password"]
    for field in sensitive_fields:
        if field in safe_payload:
            safe_payload[field] = "***REDACTED***"
    
    return safe_payload
```

## Performance Optimization

### Connection Pooling

```python
import httpx

class OptimizedRemoteLLM(RemoteLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(max_keepalive_connections=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
```

### Request Caching

```python
import hashlib
import json
from typing import Optional

class CachedRemoteLLM(RemoteLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}  # In production, use Redis or similar
    
    def get_cache_key(self, payload: dict) -> str:
        """Generate cache key from request payload"""
        cache_data = {
            "model": self.model_name,
            "messages": payload.get("messages", []),
            "temperature": payload.get("temperature", 0.7)
        }
        return hashlib.md5(json.dumps(cache_data, sort_keys=True).encode()).hexdigest()
    
    async def _execute_with_cache(self, oxy_request: OxyRequest) -> OxyResponse:
        payload = await self.build_payload(oxy_request)
        cache_key = self.get_cache_key(payload)
        
        # Check cache first
        if cache_key in self.cache:
            cached_response = self.cache[cache_key]
            return OxyResponse(
                state=OxyState.COMPLETED,
                output=cached_response
            )
        
        # Execute request
        response = await self._execute(oxy_request)
        
        # Cache successful responses
        if response.state == OxyState.COMPLETED:
            self.cache[cache_key] = response.output
        
        return response
```

## Next Steps

Learn about specific remote LLM implementations:

- [OpenAILLM](./openai-llm) - Official OpenAI client with advanced features
- [HttpLLM](./http-llm) - Generic HTTP client for various providers
- [Configuration Guide](../configuration/remote-llm-config) - Detailed configuration options
- [Security Best Practices](../security/api-key-management) - Secure API key management
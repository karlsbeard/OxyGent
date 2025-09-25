---
title: BaseLLM - Core LLM Interface
description: Abstract base class providing the foundation for all LLM implementations in OxyGent
---

# BaseLLM - Core LLM Interface

The `BaseLLM` class serves as the abstract foundation for all Large Language Model implementations in the OxyGent system. It provides essential functionality including multimodal input processing, think message extraction, error handling, and a unified interface for different LLM providers.

## Class Overview

```python
from oxygent.oxy.llms.base_llm import BaseLLM
from oxygent.oxy.base_oxy import Oxy
from pydantic import Field
```

`BaseLLM` inherits from the `Oxy` base class and implements the core LLM interface that all specific implementations must follow.

## Class Definition

```python
class BaseLLM(Oxy):
    """Base class for Large Language Model implementations.
    
    This class provides common functionality for all LLM implementations including:
    - Multimodal input processing (images, videos)
    - Think message extraction and forwarding
    - Base64 conversion for media URLs
    - Error handling with user-friendly messages
    """
```

## Attributes

### Core Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | `str` | `"llm"` | The category type, always "llm" for LLM implementations |
| `timeout` | `float` | `300` | Maximum execution time in seconds |
| `llm_params` | `dict` | `{}` | Additional parameters specific to the LLM implementation |

### Behavior Control

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `is_send_think` | `bool` | `True` | Whether to send think messages to the frontend |
| `friendly_error_text` | `str` | `"Sorry, I seem to have encountered a problem. Please try again."` | User-friendly error message for exceptions |

### Multimodal Processing

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `is_multimodal_supported` | `bool` | `False` | Whether to support multimodal input |
| `is_convert_url_to_base64` | `bool` | `False` | Whether to convert media URLs to base64 format |
| `max_image_pixels` | `int` | `10000000` | Maximum pixel count allowed per image (10M pixels) |
| `max_video_size` | `int` | `12582912` | Maximum video file size in bytes (12MB) |
| `max_file_size_bytes` | `int` | `2097152` | Maximum non-media file size in bytes (2MB) |

## Core Methods

### Message Processing

#### `async _get_messages(self, oxy_request: OxyRequest) -> list`

Preprocesses messages for multimodal input processing.

**Parameters:**
- `oxy_request` (`OxyRequest`): The request object containing input data

**Returns:**
- `list`: Processed messages in OpenAI-compatible format

**Functionality:**

1. **Query-to-Messages Conversion**: Automatically converts various query formats to standard message format:

```python
# String query -> Messages
query = "Hello, world!"
# Converts to:
messages = [{"role": "user", "content": "Hello, world!"}]

# Dict query -> Messages  
query = {"type": "text", "text": "Hello"}
# Converts to:
messages = [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]

# List query -> Messages (preserved)
query = [{"role": "user", "content": "Hello"}]
# Preserved as-is
```

2. **URL-to-Base64 Conversion**: When `is_convert_url_to_base64` is enabled:

```python
# Image URL processing
{
    "type": "image_url",
    "image_url": {"url": "https://example.com/image.jpg"}
}
# Converts to:
{
    "type": "image_url", 
    "image_url": {"url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."}
}
```

3. **Supported Content Types**:

| Content Type | Processing Function | Size Limit |
|-------------|-------------------|------------|
| `image_url` | `image_to_base64()` | `max_image_pixels` |
| `video_url` | `video_to_base64()` | `max_video_size` |
| `table_file` | `file_to_base64()` | `max_file_size_bytes` |
| `doc_file` | `file_to_base64()` | `max_file_size_bytes` |
| `pdf_file` | `file_to_base64()` | `max_file_size_bytes` |
| `code_file` | `file_to_base64()` | `max_file_size_bytes` |
| `file` | `file_to_base64()` | `max_file_size_bytes` |

### Execution Methods

#### `async _execute(self, oxy_request: OxyRequest) -> OxyResponse`

**Abstract method** that must be implemented by all concrete LLM classes.

**Parameters:**
- `oxy_request` (`OxyRequest`): The request object containing LLM parameters

**Returns:**
- `OxyResponse`: The response object with LLM output

**Implementation Requirements:**
```python
class MyLLM(BaseLLM):
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # 1. Extract messages using _get_messages()
        messages = await self._get_messages(oxy_request)
        
        # 2. Build LLM request payload
        payload = {
            "messages": messages,
            "model": self.model_name,
            # ... other parameters
        }
        
        # 3. Call LLM API
        response = await llm_api_call(payload)
        
        # 4. Return structured response
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=response.content
        )
```

### Post-Processing Methods

#### `async _post_send_message(self, oxy_response: OxyResponse)`

Handles think message extraction and forwarding after response generation.

**Parameters:**
- `oxy_response` (`OxyResponse`): The response object containing LLM output

**Think Message Extraction Modes:**

1. **XML-Style Extraction**:
```python
response_text = """
<think>
Let me analyze this step by step...
The user is asking about quantum computing.
</think>

Quantum computing is a revolutionary technology...
"""
# Extracts: "Let me analyze this step by step...\nThe user is asking about quantum computing."
```

2. **JSON-Style Extraction**:
```python
response_text = """
{
    "think": "I need to consider the technical complexity...",
    "answer": "Quantum computing uses quantum mechanical phenomena..."
}
"""
# Extracts: "I need to consider the technical complexity..."
```

**Message Forwarding:**
```python
await oxy_request.send_message({
    "type": "think", 
    "content": extracted_thinking_content
})
```

## Multimodal Processing Deep Dive

### Image Processing Pipeline

```python
async def process_image_content(self, image_url: str) -> str:
    """
    Image processing workflow:
    1. Download/read image from URL or file path
    2. Validate image format and size
    3. Resize if exceeds max_image_pixels
    4. Convert to base64 with appropriate MIME type
    5. Return data URI format
    """
    
    # Size validation
    if current_pixels > self.max_image_pixels:
        scale = (self.max_image_pixels / current_pixels) ** 0.5
        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Return data URI
    return f"data:image;base64,{base64_content}"
```

### Video Processing Pipeline

```python
async def process_video_content(self, video_url: str) -> str:
    """
    Video processing workflow:
    1. Download/read video from URL or file path
    2. Check file size against max_video_size limit
    3. If within limits, convert to base64
    4. If exceeds limits, return original URL
    """
    
    video_bytes = await source_to_bytes(video_url)
    if len(video_bytes) > self.max_video_size:
        return video_url  # Return original URL
    else:
        return f"data:video;base64,{base64.b64encode(video_bytes).decode('utf-8')}"
```

### Document Processing Pipeline

```python
async def process_document_content(self, file_url: str, content_type: str) -> str:
    """
    Document processing workflow:
    1. Determine content type (table_file, doc_file, pdf_file, etc.)
    2. Download/read file from URL or path
    3. Validate file size against limits
    4. Convert to base64 with proper MIME type
    5. Handle errors gracefully with logging
    """
    
    try:
        file_bytes = await source_to_bytes(file_url)
        if len(file_bytes) > self.max_file_size_bytes:
            return file_url  # Return original URL
        
        mime_type = self._get_mime_type(file_url, content_type)
        return f"data:{mime_type};base64,{base64_content}"
    except Exception as e:
        logger.warning(f"Failed to process {content_type}: {e}")
        return file_url  # Fallback to original URL
```

## Configuration Examples

### Basic LLM Configuration

```python
from oxygent.oxy.llms import BaseLLM

class MyCustomLLM(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    async def _execute(self, oxy_request):
        # Implementation here
        pass

# Usage
llm = MyCustomLLM(
    timeout=120,                    # 2 minute timeout
    is_send_think=True,            # Enable think message forwarding
    is_multimodal_supported=True,   # Enable multimodal processing
    is_convert_url_to_base64=True, # Enable URL-to-base64 conversion
    max_image_pixels=5000000,      # 5M pixel limit
    max_video_size=20*1024*1024,   # 20MB video limit
    max_file_size_bytes=5*1024*1024, # 5MB file limit
    llm_params={
        "temperature": 0.7,
        "max_tokens": 4096
    }
)
```

### Multimodal Configuration

```python
multimodal_llm = MyCustomLLM(
    is_multimodal_supported=True,
    is_convert_url_to_base64=True,
    max_image_pixels=15000000,     # Higher limit for detailed images
    max_video_size=50*1024*1024,   # 50MB for longer videos
    max_file_size_bytes=10*1024*1024, # 10MB for larger documents
    friendly_error_text="Multimodal processing failed. Please try with smaller files."
)
```

## Error Handling

### Exception Management

```python
try:
    response = await llm.execute(oxy_request)
except asyncio.TimeoutError:
    # Timeout handling
    response = OxyResponse(
        state=OxyState.FAILED,
        output=llm.friendly_error_text
    )
except ValueError as e:
    # Validation errors
    logger.error(f"Validation error: {e}")
    response = OxyResponse(
        state=OxyState.FAILED, 
        output="Invalid input format"
    )
except Exception as e:
    # General error handling
    logger.error(f"Unexpected error: {e}")
    response = OxyResponse(
        state=OxyState.FAILED,
        output=llm.friendly_error_text
    )
```

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# Structured logging with trace information
logger.warning(
    f"Failed to process {content_type}: {error_message}",
    extra={
        "trace_id": oxy_request.current_trace_id,
        "node_id": oxy_request.node_id,
        "content_type": content_type,
        "file_size": len(content_bytes),
        "error_type": type(error).__name__
    }
)
```

## Testing Strategies

### Unit Testing

```python
import pytest
from unittest.mock import AsyncMock, patch

class TestBaseLLM:
    @pytest.fixture
    def llm(self):
        return MyTestLLM(
            is_convert_url_to_base64=True,
            max_image_pixels=1000000
        )
    
    @pytest.mark.asyncio
    async def test_message_processing(self, llm):
        request = OxyRequest(arguments={"query": "Test query"})
        messages = await llm._get_messages(request)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Test query"
    
    @pytest.mark.asyncio
    @patch('oxygent.utils.common_utils.image_to_base64')
    async def test_multimodal_processing(self, mock_image_to_base64, llm):
        mock_image_to_base64.return_value = "data:image;base64,fake_data"
        
        request = OxyRequest(
            arguments={
                "messages": [{
                    "role": "user",
                    "content": [{
                        "type": "image_url",
                        "image_url": {"url": "http://example.com/image.jpg"}
                    }]
                }]
            }
        )
        
        messages = await llm._get_messages(request)
        mock_image_to_base64.assert_called_once()
        assert "base64" in messages[0]["content"][0]["image_url"]["url"]
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_end_to_end_processing():
    llm = MyTestLLM(is_send_think=True)
    
    request = OxyRequest(
        arguments={
            "messages": [{"role": "user", "content": "Test question"}]
        }
    )
    
    response = await llm.execute(request)
    
    assert response.state == OxyState.COMPLETED
    assert isinstance(response.output, str)
    assert len(response.output) > 0
```

## Performance Considerations

### Memory Management
- Process media files in streaming mode for large files
- Clean up temporary files after base64 conversion
- Use lazy loading for optional multimodal features

### Optimization Strategies
- Cache frequently accessed configuration values
- Use connection pooling for HTTP requests
- Implement request batching where possible

### Monitoring Metrics
- Track message processing time
- Monitor media conversion success rates
- Log memory usage for large file processing

## Next Steps

- [RemoteLLM](./remote-llm) - Remote API base implementation
- [OpenAILLM](./openai-llm) - OpenAI-specific implementation  
- [HttpLLM](./http-llm) - Generic HTTP client implementation
- [LLM Configuration Guide](../configuration/llm-config) - Detailed configuration options
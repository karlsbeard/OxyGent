---
title: LLM System Overview
description: Complete guide to OxyGent's Large Language Model integration system
---

# LLM System Overview

OxyGent's LLM system provides a unified, extensible interface for integrating with various Large Language Model providers. The system is designed with a multi-layered architecture that supports everything from local models to cloud-based AI services.

## Architecture Overview

The LLM system follows a hierarchical inheritance design pattern:

```
BaseLLM (Abstract Base Class)
└── RemoteLLM (Remote API Abstract Class)
    ├── OpenAILLM (Official OpenAI Client)
    └── HttpLLM (Generic HTTP Client)
```

### Core Design Principles

- **Unified Interface**: All LLM implementations share the same base interface
- **Configuration-Driven**: Centralized configuration through the Config system
- **Multimodal Support**: Built-in handling for images, videos, and documents
- **Streaming Ready**: Real-time streaming response support
- **Error Resilient**: Comprehensive retry and error handling mechanisms
- **Think Processing**: Advanced reasoning chain extraction and display

## Supported LLM Providers

### OpenAI Ecosystem
- **Official Client**: Uses AsyncOpenAI for optimal performance
- **Model Support**: GPT-4o, GPT-4, GPT-3.5 Turbo, and all OpenAI models
- **Advanced Features**: Reasoning content, function calling, vision
- **Streaming**: Full streaming support with thinking process display

### HTTP-Compatible APIs
- **Google Gemini**: Direct integration via Google's API
- **Ollama**: Local model deployment support
- **Custom APIs**: Any OpenAI-compatible endpoint
- **Auto-Detection**: Intelligent API format detection and adaptation

### Local Models
Through Ollama integration, support for:
- **Llama Series**: Llama 2, Code Llama, Llama Pro
- **Mistral Models**: Mistral 7B, Mixtral 8x7B
- **Code Models**: CodeLlama, StarCoder, WizardCoder
- **Specialized Models**: Dolphin, Orca, Vicuna

## Key Features

### Multimodal Processing

The system provides comprehensive multimodal input processing:

```python
# Supported media types
SUPPORTED_TYPES = {
    "images": ["image_url"],           # JPG, PNG, GIF, WebP
    "videos": ["video_url"],           # MP4, AVI, MOV, WebM
    "documents": ["doc_file", "pdf_file"],  # DOC, PDF
    "tables": ["table_file"],          # XLSX, CSV, TSV
    "code": ["code_file"],             # PY, JS, TS, MD
    "generic": ["file"]                # Any file type
}
```

#### Media Processing Features
- **Automatic URL-to-Base64 conversion** for offline processing
- **Intelligent resizing** with configurable pixel limits
- **Size validation** and optimization
- **Format detection** and MIME type handling
- **Error handling** with graceful fallbacks

### Message Processing

Advanced message formatting and processing capabilities:

```python
# Query format conversion
query_formats = {
    "string": "Plain text query",
    "dict": "Single message object", 
    "list": "Message array (OpenAI format)"
}

# Automatic message structure conversion
message_structure = {
    "role": "user|assistant|system",
    "content": "string|array[content_parts]"
}
```

### Think Message Extraction

Sophisticated reasoning process extraction:

```python
# XML-style extraction
xml_pattern = r"<think>(.*?)</think>"

# JSON-style extraction  
json_pattern = r'"think"\s*:\s*"([^"]*)"'

# Automatic forwarding to frontend
await oxy_request.send_message({
    "type": "think", 
    "content": extracted_thinking
})
```

## Configuration Management

### LLM Configuration Structure

```python
llm_config = {
    "cls": "oxygent.oxy.llms.OpenAILLM",  # Implementation class
    "base_url": "https://api.openai.com/v1",  # API endpoint
    "api_key": "${OPENAI_API_KEY}",       # Environment variable
    "model_name": "gpt-4o",               # Model identifier
    "temperature": 0.7,                   # Creativity control
    "max_tokens": 4096,                   # Response length limit
    "top_p": 1.0,                        # Nucleus sampling
    "timeout": 300                        # Request timeout
}
```

### Environment Variable Support

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Anthropic Configuration  
ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-3-sonnet

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b
```

### Runtime Configuration

```python
from oxygent.config import Config

# Dynamic configuration updates
Config.set_llm_config({
    "temperature": 0.8,
    "max_tokens": 8192,
    "top_p": 0.9
})

# Per-request parameter override
llm_params = {
    "temperature": 0.5,
    "stream": True
}
```

## Performance Optimizations

### Connection Management
- **Async HTTP Clients**: Non-blocking request handling
- **Connection Pooling**: Efficient resource utilization  
- **Request Queuing**: Controlled concurrent processing
- **Timeout Management**: Configurable timeout strategies

### Caching Strategies
- **Response Caching**: Optional LLM response caching
- **Configuration Caching**: Hot configuration reloading
- **Media Processing Cache**: Processed media content caching

### Memory Management
- **Streaming Processing**: Large file streaming support
- **Lazy Loading**: On-demand resource loading
- **Garbage Collection**: Automatic cleanup of processed media

## Security Features

### API Key Management
- **Environment Variable Support**: Secure key storage
- **Runtime Key Rotation**: Dynamic key updates
- **Key Validation**: Automatic key format verification

### Input Validation
- **Content Filtering**: Malicious content detection
- **Size Limits**: File and request size restrictions
- **Format Validation**: Input format verification
- **Sanitization**: Automatic content sanitization

### Output Security
- **Response Filtering**: Sensitive information removal
- **Content Validation**: Output format verification
- **Error Sanitization**: Safe error message display

## Error Handling

### Retry Mechanisms
```python
retry_config = {
    "max_retries": 3,
    "initial_delay": 1.0,
    "backoff_multiplier": 2.0,
    "max_delay": 60.0,
    "retry_on_timeout": True,
    "retry_on_rate_limit": True
}
```

### Graceful Degradation
- **Fallback Models**: Automatic model switching on failure
- **Partial Response Handling**: Processing incomplete responses
- **Service Health Monitoring**: Provider availability tracking

### Comprehensive Logging
```python
import logging

logger = logging.getLogger("oxygent.llms")

# Structured logging with trace IDs
logger.info(
    "LLM request completed", 
    extra={
        "trace_id": request.current_trace_id,
        "node_id": request.node_id,
        "model": "gpt-4o",
        "tokens_used": 1250,
        "response_time": 2.3
    }
)
```

## Integration Examples

### Basic Usage

```python
from oxygent.oxy.llms import OpenAILLM
from oxygent.schemas import OxyRequest

# Initialize LLM
llm = OpenAILLM(
    api_key="${OPENAI_API_KEY}",
    base_url="https://api.openai.com/v1", 
    model_name="gpt-4o"
)

# Create request
request = OxyRequest(
    arguments={
        "messages": [
            {"role": "user", "content": "Explain quantum computing"}
        ]
    }
)

# Execute request
response = await llm.execute(request)
print(response.output)
```

### Multimodal Usage

```python
# Image and text processing
multimodal_request = OxyRequest(
    arguments={
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url", 
                        "image_url": {
                            "url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
                        }
                    }
                ]
            }
        ]
    }
)

response = await llm.execute(multimodal_request)
```

### Streaming Usage

```python
# Enable streaming
streaming_request = OxyRequest(
    arguments={
        "messages": [{"role": "user", "content": "Write a story"}],
        "stream": True
    }
)

# Process streaming response
response = await llm.execute(streaming_request)
# Streaming chunks are automatically sent via websocket
```

## Best Practices

### Production Deployment

1. **Configuration Management**
   - Use environment variables for sensitive data
   - Implement configuration validation
   - Set up configuration monitoring

2. **Performance Tuning**
   - Configure appropriate timeouts
   - Implement request rate limiting
   - Set up response caching where appropriate

3. **Monitoring & Observability**
   - Log all LLM interactions with trace IDs
   - Monitor token usage and costs
   - Set up alerts for failures and performance issues

4. **Security Hardening**
   - Regularly rotate API keys
   - Implement input sanitization
   - Set up output content filtering

### Development Guidelines

1. **Testing Strategy**
   - Mock LLM responses for unit tests
   - Test with multiple model providers
   - Validate multimodal input processing

2. **Error Handling**
   - Always implement timeout handling
   - Provide meaningful error messages
   - Log errors with sufficient context

3. **Resource Management**
   - Clean up processed media files
   - Monitor memory usage for large files
   - Implement proper async context management

## Next Steps

Explore the specific LLM implementations:

- [BaseLLM](./base-llm) - Core LLM interface and functionality
- [RemoteLLM](./remote-llm) - Remote API base implementation  
- [OpenAILLM](./openai-llm) - OpenAI official client integration
- [HttpLLM](./http-llm) - Generic HTTP client for various providers

For configuration details, see the [Configuration Guide](../configuration) and [Environment Setup](../environment-setup).
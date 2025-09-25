---
title: HttpTool
description: HTTP request tool for API integration and web service connectivity in OxyGent
---

# HttpTool

The `HttpTool` class enables making HTTP requests to external APIs and services within the OxyGent system. It supports configurable HTTP methods, headers, and parameters with proper timeout handling and async execution.

## Class Overview

```python
from oxygent.oxy.api_tools import HttpTool
from oxygent.oxy.base_tool import BaseTool

class HttpTool(BaseTool):
    """Tool for making HTTP requests to external APIs and services."""
```

### Inheritance Hierarchy
```
HttpTool → BaseTool → Oxy
```

## Core Attributes

### `method: str`
HTTP method to use for requests. Defaults to "GET".

**Supported Methods:**
- GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS

```python
get_tool = HttpTool(method="GET", url="https://api.example.com/data")
post_tool = HttpTool(method="POST", url="https://api.example.com/create")
```

### `url: str`
Target URL for the HTTP request.

```python
tool = HttpTool(
    name="api_endpoint",
    url="https://jsonplaceholder.typicode.com/posts"
)
```

### `headers: dict`
HTTP headers to include in the request.

```python
authenticated_tool = HttpTool(
    name="secure_api",
    url="https://api.example.com/data",
    headers={
        "Authorization": "Bearer your-token",
        "Content-Type": "application/json",
        "User-Agent": "OxyGent/1.0"
    }
)
```

### `default_params: dict`
Default parameters that will be merged with request arguments.

```python
tool = HttpTool(
    name="weather_api",
    url="https://api.weather.com/v1/current",
    default_params={
        "format": "json",
        "units": "metric",
        "lang": "en"
    }
)
```

## Methods

### `async _execute(oxy_request: OxyRequest) -> OxyResponse`

Execute the HTTP request with parameter merging and timeout handling.

**Process:**
1. Merges `default_params` with `oxy_request.arguments`
2. Creates async HTTP client with configured timeout
3. Makes HTTP request using specified method, URL, and headers
4. Returns response wrapped in `OxyResponse`

```python
request = OxyRequest(
    callee="weather_api",
    arguments={"location": "New York", "detailed": "true"}
)

response = await tool._execute(request)
# Merged parameters: {"format": "json", "units": "metric", "lang": "en", "location": "New York", "detailed": "true"}
```

**Implementation Details:**
```python
async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
    # Merge default parameters with request arguments
    params = self.default_params.copy()
    params.update(oxy_request.arguments)
    
    # Make HTTP request with timeout handling
    async with httpx.AsyncClient(timeout=self.timeout) as client:
        http_response = await client.get(
            self.url, params=params, headers=self.headers
        )
        return OxyResponse(state=OxyState.COMPLETED, output=http_response.text)
```

## Usage Examples

### Basic GET Request

```python
# Simple API data fetching
api_tool = HttpTool(
    name="fetch_posts",
    desc="Fetch blog posts from API",
    method="GET",
    url="https://jsonplaceholder.typicode.com/posts"
)

# Execute request
response = await api_tool._execute(OxyRequest(
    callee="fetch_posts",
    arguments={"userId": 1}
))

if response.state == OxyState.COMPLETED:
    posts_data = response.output
    print(f"Fetched posts: {posts_data}")
```

### Authenticated API Access

```python
# API with authentication
secure_tool = HttpTool(
    name="user_profile",
    desc="Get user profile information",
    method="GET",
    url="https://api.company.com/v1/user/profile",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
)

# Fetch user data
user_response = await secure_tool._execute(OxyRequest(
    callee="user_profile",
    arguments={"include": "preferences,settings"}
))
```

### POST Request with JSON Data

```python
# API data submission
create_tool = HttpTool(
    name="create_user",
    desc="Create new user account",
    method="POST", 
    url="https://api.company.com/v1/users",
    headers={
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
)

# Create user
creation_response = await create_tool._execute(OxyRequest(
    callee="create_user",
    arguments={
        "name": "John Doe",
        "email": "john@example.com",
        "role": "user"
    }
))
```

### File Upload

```python
# File upload tool
upload_tool = HttpTool(
    name="upload_file",
    desc="Upload file to storage service",
    method="POST",
    url="https://storage.company.com/v1/upload",
    headers={
        "Authorization": f"Bearer {storage_token}"
        # Content-Type will be set automatically for multipart
    }
)

# Upload file
upload_response = await upload_tool._execute(OxyRequest(
    callee="upload_file",
    arguments={
        "file": file_content,
        "filename": "document.pdf",
        "folder": "documents"
    }
))
```

## Configuration Examples

### Environment-Based Configuration

```python
import os

# Production API configuration
production_tool = HttpTool(
    name="production_api",
    desc="Production API endpoint",
    method="POST",
    url=os.getenv("API_URL"),
    headers={
        "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
        "Content-Type": "application/json",
        "X-Client-Version": os.getenv("CLIENT_VERSION", "1.0")
    },
    timeout=float(os.getenv("API_TIMEOUT", "30.0"))
)
```

### Multiple Environment Setup

```python
def create_api_tool(environment: str) -> HttpTool:
    """Create environment-specific API tool."""
    
    configs = {
        "development": {
            "url": "http://localhost:3000/api",
            "headers": {"Content-Type": "application/json"},
            "timeout": 10.0
        },
        "staging": {
            "url": "https://staging-api.company.com/v1",
            "headers": {
                "Authorization": f"Bearer {os.getenv('STAGING_TOKEN')}",
                "Content-Type": "application/json"
            },
            "timeout": 30.0
        },
        "production": {
            "url": "https://api.company.com/v1",
            "headers": {
                "Authorization": f"Bearer {os.getenv('PROD_TOKEN')}",
                "Content-Type": "application/json",
                "X-Environment": "production"
            },
            "timeout": 60.0
        }
    }
    
    config = configs[environment]
    return HttpTool(
        name=f"{environment}_api",
        desc=f"API tool for {environment} environment",
        method="POST",
        **config
    )

# Usage
dev_tool = create_api_tool("development")
prod_tool = create_api_tool("production")
```

### Service-Specific Tools

```python
# Payment service integration
payment_tools = {
    "process_payment": HttpTool(
        name="process_payment",
        desc="Process credit card payment",
        method="POST",
        url="https://payments.company.com/v1/process",
        headers={
            "Authorization": f"Bearer {payment_token}",
            "Content-Type": "application/json",
            "Idempotency-Key": lambda: str(uuid.uuid4())  # For idempotent requests
        },
        default_params={"currency": "USD"}
    ),
    
    "refund_payment": HttpTool(
        name="refund_payment", 
        desc="Refund payment transaction",
        method="POST",
        url="https://payments.company.com/v1/refund",
        headers={
            "Authorization": f"Bearer {payment_token}",
            "Content-Type": "application/json"
        }
    ),
    
    "get_payment_status": HttpTool(
        name="get_payment_status",
        desc="Check payment transaction status",
        method="GET",
        url="https://payments.company.com/v1/status",
        headers={"Authorization": f"Bearer {payment_token}"}
    )
}
```

## Integration Examples

### With Agents

```python
from oxygent.agents import ChatAgent

# Create API-focused agent
api_agent = ChatAgent(name="api_specialist")

# Add multiple HTTP tools
api_tools = [
    HttpTool(name="get_user", method="GET", url="https://api.com/users"),
    HttpTool(name="create_user", method="POST", url="https://api.com/users"), 
    HttpTool(name="update_user", method="PUT", url="https://api.com/users"),
    HttpTool(name="delete_user", method="DELETE", url="https://api.com/users")
]

for tool in api_tools:
    api_agent.add_oxy(tool)

# Agent can now perform CRUD operations
response = await api_agent.execute(OxyRequest(
    callee="create_user",
    arguments={"name": "Alice", "email": "alice@example.com"}
))
```

### With Workflows

```python
from oxygent.flows import WorkflowFlow

# Data processing workflow using HTTP tools
data_workflow = WorkflowFlow(name="data_pipeline")

# Add HTTP tools for different stages
fetch_tool = HttpTool(
    name="fetch_data",
    method="GET",
    url="https://data-source.com/api/export"
)

process_tool = HttpTool(
    name="process_data",
    method="POST",
    url="https://processor.com/api/transform"
)

store_tool = HttpTool(
    name="store_data",
    method="POST", 
    url="https://storage.com/api/save"
)

# Add tools to workflow
for tool in [fetch_tool, process_tool, store_tool]:
    data_workflow.add_oxy(tool)

# Define workflow steps
workflow_config = {
    "steps": [
        {
            "name": "extract",
            "tool": "fetch_data",
            "arguments": {"format": "json", "limit": 1000}
        },
        {
            "name": "transform", 
            "tool": "process_data",
            "arguments": {"data": "{extract.output}", "format": "normalized"}
        },
        {
            "name": "load",
            "tool": "store_data",
            "arguments": {"processed_data": "{transform.output}"}
        }
    ]
}
```

### Multi-Service Orchestration

```python
# Microservices orchestration
services = {
    "user_service": HttpTool(
        name="user_api",
        url="https://users.company.com/api/v1",
        headers={"Authorization": f"Bearer {user_service_token}"}
    ),
    "order_service": HttpTool(
        name="order_api", 
        url="https://orders.company.com/api/v1",
        headers={"Authorization": f"Bearer {order_service_token}"}
    ),
    "inventory_service": HttpTool(
        name="inventory_api",
        url="https://inventory.company.com/api/v1", 
        headers={"Authorization": f"Bearer {inventory_service_token}"}
    ),
    "notification_service": HttpTool(
        name="notification_api",
        url="https://notifications.company.com/api/v1",
        headers={"Authorization": f"Bearer {notification_service_token}"}
    )
}

# Orchestration agent
orchestrator = ChatAgent(name="service_orchestrator")
for service_tool in services.values():
    orchestrator.add_oxy(service_tool)

# Complex business operation
async def process_order(order_data):
    # 1. Validate user
    user_response = await orchestrator.execute(OxyRequest(
        callee="user_api",
        arguments={"action": "validate", "user_id": order_data["user_id"]}
    ))
    
    # 2. Check inventory
    inventory_response = await orchestrator.execute(OxyRequest(
        callee="inventory_api", 
        arguments={"action": "check", "items": order_data["items"]}
    ))
    
    # 3. Create order
    order_response = await orchestrator.execute(OxyRequest(
        callee="order_api",
        arguments={"action": "create", "order": order_data}
    ))
    
    # 4. Send confirmation
    notification_response = await orchestrator.execute(OxyRequest(
        callee="notification_api",
        arguments={
            "action": "send",
            "user_id": order_data["user_id"],
            "message": f"Order {order_response.output['order_id']} confirmed"
        }
    ))
    
    return order_response
```

## Advanced Features

### Request/Response Transformation

```python
class TransformingHttpTool(HttpTool):
    """HttpTool with request/response transformation."""
    
    def __init__(self, request_transformer=None, response_transformer=None, **kwargs):
        super().__init__(**kwargs)
        self.request_transformer = request_transformer
        self.response_transformer = response_transformer
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with transformation support."""
        # Transform request if needed
        if self.request_transformer:
            transformed_args = self.request_transformer(oxy_request.arguments)
            oxy_request = OxyRequest(
                callee=oxy_request.callee,
                arguments=transformed_args,
                caller=oxy_request.caller,
                trace_id=oxy_request.trace_id
            )
        
        # Execute original request
        response = await super()._execute(oxy_request)
        
        # Transform response if needed
        if self.response_transformer and response.state == OxyState.COMPLETED:
            transformed_output = self.response_transformer(response.output)
            response = OxyResponse(
                state=response.state,
                output=transformed_output
            )
        
        return response

# Usage with transformers
def normalize_user_data(data):
    """Transform user data for API compatibility."""
    return {
        "full_name": f"{data['first_name']} {data['last_name']}",
        "email_address": data["email"],
        "user_role": data.get("role", "user")
    }

def parse_api_response(response_text):
    """Parse and extract relevant data from API response."""
    import json
    data = json.loads(response_text)
    return {
        "user_id": data["id"],
        "status": data["status"],
        "created_at": data["created_timestamp"]
    }

user_tool = TransformingHttpTool(
    name="create_user_normalized",
    method="POST",
    url="https://api.company.com/users",
    request_transformer=normalize_user_data,
    response_transformer=parse_api_response
)
```

### Retry and Circuit Breaker

```python
import asyncio
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class ResilientHttpTool(HttpTool):
    """HttpTool with retry logic and circuit breaker."""
    
    def __init__(
        self, 
        max_retries=3,
        retry_delay=1.0,
        circuit_breaker_threshold=5,
        circuit_breaker_timeout=60.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_timeout = circuit_breaker_timeout
        
        # Circuit breaker state
        self.circuit_state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with resilience patterns."""
        # Check circuit breaker
        if not self._can_execute():
            return OxyResponse(
                state=OxyState.FAILED,
                output="Circuit breaker is open"
            )
        
        # Retry logic
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await super()._execute(oxy_request)
                
                # Success - reset circuit breaker
                self._record_success()
                return response
                
            except Exception as e:
                last_exception = e
                self._record_failure()
                
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay}s")
                    await asyncio.sleep(delay)
        
        return OxyResponse(
            state=OxyState.FAILED,
            output=f"Failed after {self.max_retries} retries: {last_exception}"
        )
    
    def _can_execute(self) -> bool:
        """Check if request can be executed based on circuit breaker state."""
        current_time = time.time()
        
        if self.circuit_state == CircuitState.CLOSED:
            return True
        elif self.circuit_state == CircuitState.OPEN:
            if current_time - self.last_failure_time > self.circuit_breaker_timeout:
                self.circuit_state = CircuitState.HALF_OPEN
                return True
            return False
        elif self.circuit_state == CircuitState.HALF_OPEN:
            return True
        
        return False
    
    def _record_success(self):
        """Record successful request."""
        self.failure_count = 0
        self.circuit_state = CircuitState.CLOSED
    
    def _record_failure(self):
        """Record failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.circuit_breaker_threshold:
            self.circuit_state = CircuitState.OPEN
```

### Response Caching

```python
import hashlib
import json
import time

class CachedHttpTool(HttpTool):
    """HttpTool with intelligent response caching."""
    
    def __init__(self, cache_ttl=300, cache_size=1000, **kwargs):
        super().__init__(**kwargs)
        self.cache_ttl = cache_ttl
        self.cache_size = cache_size
        self.cache = {}
        self.access_times = {}
    
    def _get_cache_key(self, oxy_request: OxyRequest) -> str:
        """Generate cache key for request."""
        cache_data = {
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "default_params": self.default_params,
            "arguments": oxy_request.arguments
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _is_cacheable(self, oxy_request: OxyRequest) -> bool:
        """Determine if request should be cached."""
        # Only cache GET requests by default
        return self.method.upper() == "GET"
    
    def _cleanup_cache(self):
        """Remove expired entries and enforce size limit."""
        current_time = time.time()
        
        # Remove expired entries
        expired_keys = [
            key for key, (timestamp, _) in self.cache.items()
            if current_time - timestamp > self.cache_ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.access_times[key]
        
        # Enforce size limit (LRU eviction)
        if len(self.cache) > self.cache_size:
            # Sort by access time, remove oldest
            sorted_items = sorted(self.access_times.items(), key=lambda x: x[1])
            keys_to_remove = [key for key, _ in sorted_items[:len(self.cache) - self.cache_size]]
            
            for key in keys_to_remove:
                del self.cache[key]
                del self.access_times[key]
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with caching support."""
        if not self._is_cacheable(oxy_request):
            return await super()._execute(oxy_request)
        
        cache_key = self._get_cache_key(oxy_request)
        current_time = time.time()
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_response = self.cache[cache_key]
            if current_time - cached_time < self.cache_ttl:
                # Cache hit
                self.access_times[cache_key] = current_time
                logger.debug(f"Cache hit for {self.name}")
                return cached_response
        
        # Cache miss - execute request
        response = await super()._execute(oxy_request)
        
        # Cache successful responses
        if response.state == OxyState.COMPLETED:
            self.cache[cache_key] = (current_time, response)
            self.access_times[cache_key] = current_time
            
            # Cleanup cache
            self._cleanup_cache()
        
        return response
```

## Security Considerations

### Input Validation

```python
class SecureHttpTool(HttpTool):
    """HttpTool with security validations."""
    
    def __init__(self, allowed_params=None, param_validators=None, **kwargs):
        super().__init__(**kwargs)
        self.allowed_params = allowed_params or []
        self.param_validators = param_validators or {}
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with security validations."""
        # Validate URL scheme
        if not self.url.startswith(('https://', 'http://localhost', 'http://127.0.0.1')):
            return OxyResponse(
                state=OxyState.FAILED,
                output="Only HTTPS URLs are allowed (except localhost)"
            )
        
        # Validate parameters
        validation_error = self._validate_parameters(oxy_request.arguments)
        if validation_error:
            return OxyResponse(state=OxyState.FAILED, output=validation_error)
        
        # Sanitize parameters
        sanitized_request = self._sanitize_request(oxy_request)
        
        return await super()._execute(sanitized_request)
    
    def _validate_parameters(self, arguments: dict) -> str:
        """Validate request parameters."""
        # Check allowed parameters
        if self.allowed_params:
            invalid_params = set(arguments.keys()) - set(self.allowed_params)
            if invalid_params:
                return f"Invalid parameters: {invalid_params}"
        
        # Run custom validators
        for param, validator in self.param_validators.items():
            if param in arguments:
                try:
                    if not validator(arguments[param]):
                        return f"Validation failed for parameter: {param}"
                except Exception as e:
                    return f"Validation error for {param}: {e}"
        
        return None
    
    def _sanitize_request(self, oxy_request: OxyRequest) -> OxyRequest:
        """Sanitize request parameters."""
        sanitized_args = {}
        
        for key, value in oxy_request.arguments.items():
            if isinstance(value, str):
                # Basic string sanitization
                sanitized_value = value.strip()
                # Remove potentially dangerous characters
                sanitized_value = ''.join(c for c in sanitized_value if c.isprintable())
                sanitized_args[key] = sanitized_value
            else:
                sanitized_args[key] = value
        
        return OxyRequest(
            callee=oxy_request.callee,
            arguments=sanitized_args,
            caller=oxy_request.caller,
            trace_id=oxy_request.trace_id
        )

# Usage with validation
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

secure_tool = SecureHttpTool(
    name="secure_user_api",
    method="POST",
    url="https://api.company.com/users",
    allowed_params=["name", "email", "role"],
    param_validators={
        "email": validate_email,
        "role": lambda role: role in ["admin", "user", "guest"]
    }
)
```

### Authentication Management

```python
class AuthenticatedHttpTool(HttpTool):
    """HttpTool with dynamic authentication."""
    
    def __init__(self, auth_provider=None, **kwargs):
        super().__init__(**kwargs)
        self.auth_provider = auth_provider
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with dynamic authentication."""
        # Refresh authentication if needed
        if self.auth_provider:
            await self._refresh_auth()
        
        return await super()._execute(oxy_request)
    
    async def _refresh_auth(self):
        """Refresh authentication headers."""
        try:
            token = await self.auth_provider.get_token()
            self.headers["Authorization"] = f"Bearer {token}"
        except Exception as e:
            logger.error(f"Failed to refresh auth token: {e}")
            raise

class TokenProvider:
    """Token provider for dynamic authentication."""
    
    def __init__(self, token_url: str, client_id: str, client_secret: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.cached_token = None
        self.token_expires_at = 0
    
    async def get_token(self) -> str:
        """Get valid access token."""
        current_time = time.time()
        
        if self.cached_token and current_time < self.token_expires_at:
            return self.cached_token
        
        # Refresh token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            
            token_data = response.json()
            self.cached_token = token_data["access_token"]
            self.token_expires_at = current_time + token_data.get("expires_in", 3600) - 60  # 1 minute buffer
            
            return self.cached_token

# Usage
token_provider = TokenProvider(
    token_url="https://auth.company.com/oauth/token",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

auth_tool = AuthenticatedHttpTool(
    name="authenticated_api",
    method="GET",
    url="https://api.company.com/data",
    auth_provider=token_provider
)
```

## Performance Optimization

### Connection Pooling

```python
import httpx

class PooledHttpTool(HttpTool):
    """HttpTool with connection pooling."""
    
    _client_pool = {}
    
    @classmethod
    def get_client(cls, timeout: float) -> httpx.AsyncClient:
        """Get or create shared HTTP client."""
        if timeout not in cls._client_pool:
            limits = httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30.0
            )
            cls._client_pool[timeout] = httpx.AsyncClient(
                limits=limits,
                timeout=timeout
            )
        
        return cls._client_pool[timeout]
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute using pooled HTTP client."""
        # Merge parameters
        params = self.default_params.copy()
        params.update(oxy_request.arguments)
        
        # Use pooled client
        client = self.get_client(self.timeout)
        
        try:
            http_response = await client.request(
                method=self.method,
                url=self.url,
                params=params if self.method == "GET" else None,
                json=params if self.method != "GET" else None,
                headers=self.headers
            )
            
            return OxyResponse(state=OxyState.COMPLETED, output=http_response.text)
        except Exception as e:
            return OxyResponse(state=OxyState.FAILED, output=str(e))
```

## Error Handling

### Comprehensive Error Management

```python
import httpx

async def robust_http_execution(tool: HttpTool, request: OxyRequest) -> OxyResponse:
    """Execute HttpTool with comprehensive error handling."""
    try:
        return await tool._execute(request)
    
    except httpx.TimeoutException:
        logger.error(f"HTTP timeout for {tool.name} after {tool.timeout}s")
        return OxyResponse(
            state=OxyState.FAILED,
            output=f"Request timeout after {tool.timeout}s"
        )
    
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        error_messages = {
            400: "Bad request - invalid parameters",
            401: "Authentication required",
            403: "Access forbidden", 
            404: "Resource not found",
            429: "Rate limit exceeded",
            500: "Internal server error",
            502: "Bad gateway",
            503: "Service unavailable",
            504: "Gateway timeout"
        }
        
        error_msg = error_messages.get(status_code, f"HTTP {status_code} error")
        logger.error(f"HTTP {status_code} for {tool.name}: {error_msg}")
        
        return OxyResponse(state=OxyState.FAILED, output=error_msg)
    
    except httpx.NetworkError as e:
        logger.error(f"Network error for {tool.name}: {e}")
        return OxyResponse(state=OxyState.FAILED, output="Network connectivity error")
    
    except Exception as e:
        logger.error(f"Unexpected error for {tool.name}: {e}")
        return OxyResponse(state=OxyState.FAILED, output=f"Execution error: {str(e)}")
```

## Best Practices

### Configuration Management

```python
# ✅ Good: Centralized configuration
@dataclass
class HttpToolConfig:
    name: str
    method: str
    url: str
    auth_token: str = None
    timeout: float = 30.0
    default_params: dict = None
    
    def to_tool(self) -> HttpTool:
        """Convert to HttpTool instance."""
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        return HttpTool(
            name=self.name,
            method=self.method,
            url=self.url,
            headers=headers,
            timeout=self.timeout,
            default_params=self.default_params or {}
        )

# Usage
configs = [
    HttpToolConfig(
        name="user_api",
        method="GET",
        url="https://api.company.com/users",
        auth_token=os.getenv("USER_API_TOKEN")
    ),
    HttpToolConfig(
        name="order_api", 
        method="POST",
        url="https://api.company.com/orders",
        auth_token=os.getenv("ORDER_API_TOKEN"),
        default_params={"currency": "USD"}
    )
]

tools = [config.to_tool() for config in configs]
```

### Error Handling Strategy

```python
# ✅ Good: Standardized error handling
class StandardHttpTool(HttpTool):
    """HttpTool with standardized error handling and logging."""
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with standard error handling."""
        start_time = time.time()
        
        try:
            response = await super()._execute(oxy_request)
            
            # Log successful execution
            execution_time = time.time() - start_time
            logger.info(
                f"HTTP tool {self.name} succeeded",
                extra={
                    "tool_name": self.name,
                    "method": self.method,
                    "url": self.url,
                    "execution_time": execution_time,
                    "response_length": len(response.output) if isinstance(response.output, str) else 0
                }
            )
            
            return response
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Log error with context
            logger.error(
                f"HTTP tool {self.name} failed",
                extra={
                    "tool_name": self.name,
                    "method": self.method,
                    "url": self.url,
                    "execution_time": execution_time,
                    "arguments": oxy_request.arguments,
                    "error": str(e)
                }
            )
            
            return OxyResponse(
                state=OxyState.FAILED,
                output={
                    "error": str(e),
                    "tool": self.name,
                    "method": self.method,
                    "url": self.url,
                    "execution_time": execution_time
                }
            )
```

## API Reference

### Complete Class Definition

```python
class HttpTool(BaseTool):
    """Tool for making HTTP requests to external APIs and services."""
    
    method: str = Field("GET", description="HTTP method to use")
    url: str = Field("", description="Target URL for the HTTP request")
    headers: dict = Field(default_factory=dict, description="HTTP headers to include")
    default_params: dict = Field(default_factory=dict, description="Default request parameters")
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute the HTTP request."""
```

### Inherited Properties

From `BaseTool`:
- `is_permission_required: bool = True`
- `category: str = "tool"`
- `timeout: float = 60`

From `Oxy`:
- `name: str`
- `desc: str`
- `mas: Optional[MAS] = None`

### Configuration Schema

```python
{
    "name": str,              # Tool identifier
    "desc": str,              # Tool description
    "method": str,            # HTTP method (GET, POST, etc.)
    "url": str,               # Target URL
    "headers": dict,          # HTTP headers
    "default_params": dict,   # Default parameters
    "timeout": float,         # Request timeout in seconds
    "is_permission_required": bool  # Permission requirement
}
```

## See Also

- [Function Tools](/tools/function-tools) - For custom HTTP processing functions
- [MCP Tools](/tools/mcp-tools) - For MCP server integration
- [BaseTool](/agents/base-agent) - Base tool interface
- [Agents](/agents) - Agent integration patterns
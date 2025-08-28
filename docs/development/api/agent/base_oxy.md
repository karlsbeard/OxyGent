# Base Oxy Class

## Overview

The `Oxy` class is the abstract base class for all agents and tools in the OxyGent system. It provides the core execution lifecycle, permission management, message handling, and data persistence patterns.

## Class Definition

```python
class Oxy(BaseModel, ABC)
```

**Module**: `oxygent.oxy.base_oxy`

## Core Attributes

### Identity & Description

- `name` (str, required): Unique identifier for the agent/tool
- `desc` (str): Human-readable description of functionality
- `category` (str): Category classification (default: "tool")
- `class_name` (Optional[str]): Class name (auto-generated)

### Schema & LLM Integration

- `input_schema` (dict[str, Any]): Input schema definition
- `desc_for_llm` (str): LLM-friendly description (auto-generated from schema)

### Permissions & Access Control

- `is_entrance` (bool): Whether this is a MAS entry point (default: False)
- `is_permission_required` (bool): Whether permission is needed for execution (default: False)
- `permitted_tool_name_list` (list): List of tools this entity can call
- `extra_permitted_tool_name_list` (list): Additional tool permissions

### Data Management

- `is_save_data` (bool): Whether to save execution data (default: True)

### Message Control

- `is_send_tool_call` (bool): Whether to send tool_call messages
- `is_send_observation` (bool): Whether to send observation messages
- `is_send_answer` (bool): Whether to send answer messages

### Logging Control

- `is_detailed_tool_call` (bool): Whether to show detailed tool_call logs
- `is_detailed_observation` (bool): Whether to show detailed observation logs

### Execution Control

- `semaphore` (int): Maximum concurrent executions (default: 16)
- `timeout` (float): Execution timeout in seconds (default: 3600)
- `retries` (int): Number of retry attempts on failure (default: 2)
- `delay` (float): Delay between retries (default: 1.0)

### Processing Functions

- `func_process_input` (Callable): Input processing function
- `func_process_output` (Callable): Output processing function
- `func_format_input` (Optional[Callable]): Input formatting for callee
- `func_format_output` (Optional[Callable]): Output formatting for caller
- `func_execute` (Optional[Callable]): Custom execution function
- `func_interceptor` (Optional[Callable]): Request interceptor function

### System Integration

- `mas` (Optional[Any]): MAS instance reference (excluded from serialization)
- `friendly_error_text` (Optional[str]): User-friendly error message

## Core Methods

### Abstract Methods

#### `async def _execute(self, oxy_request: OxyRequest) -> OxyResponse`

Main execution method that must be implemented by subclasses.

**Parameters:**

- `oxy_request` (OxyRequest): The request to execute

**Returns:**

- `OxyResponse`: The execution result

### Lifecycle Methods

#### `async def execute(self, oxy_request: OxyRequest) -> OxyResponse`

Complete execution lifecycle orchestrator. Handles:

- Pre-processing
- Logging and data saving
- Input formatting and validation
- Permission checks
- Execution with retry logic
- Post-processing
- Output formatting

**Parameters:**

- `oxy_request` (OxyRequest): The request to execute

**Returns:**

- `OxyResponse`: The formatted execution result

#### `async def init(self)`

Initialize the Oxy instance. Override for custom initialization.

### Hook Methods

#### `async def _pre_process(self, oxy_request: OxyRequest) -> OxyRequest`

Pre-process the request before execution.

#### `async def _pre_log(self, oxy_request: OxyRequest)`

Log the tool call information before execution.

#### `async def _pre_save_data(self, oxy_request: OxyRequest)`

Save preliminary execution data.

#### `async def _pre_send_message(self, oxy_request: OxyRequest)`

Send tool call message to frontend if enabled.

#### `async def _before_execute(self, oxy_request: OxyRequest) -> OxyRequest`

Final preparation before execution.

#### `async def _after_execute(self, oxy_response: OxyResponse) -> OxyResponse`

Process response after execution.

#### `async def _post_process(self, oxy_response: OxyResponse) -> OxyResponse`

Post-process the response.

#### `async def _post_log(self, oxy_response: OxyResponse)`

Log the execution result.

#### `async def _post_save_data(self, oxy_response: OxyResponse)`

Save complete execution data to Elasticsearch.

#### `async def _post_send_message(self, oxy_response: OxyResponse)`

Send observation and answer messages to frontend if enabled.

#### `async def _handle_exception(self, e)`

Handle execution exceptions. Override for custom error handling.

### Utility Methods

#### `def set_mas(self, mas)`

Set the MAS (Multi-Agent System) reference.

#### `def add_permitted_tool(self, tool_name: str)`

Add a tool to the permitted tools list.

#### `def add_permitted_tools(self, tool_names: list)`

Add multiple tools to the permitted tools list.

## Data Persistence

The Oxy class automatically saves execution data to Elasticsearch when `is_save_data=True`:

- **Pre-execution**: Saves request metadata to `{app_name}_node` index
- **Post-execution**: Updates with complete execution data including input, output, and execution state

## Error Handling & Retries

The class provides built-in retry logic:

1. Attempts execution up to `retries` times
2. Waits `delay` seconds between retries
3. Handles `asyncio.CancelledError` specially
4. Logs all exceptions with trace information
5. Returns FAILED state response on final failure

## Message Flow

The execution lifecycle sends messages to frontend when enabled:

1. **tool_call**: Before execution (if `is_send_tool_call=True`)
2. **observation**: After execution (if `is_send_observation=True`)
3. **answer**: For user-originated calls (if `is_send_answer=True`)

## Usage Example

```python
from oxygent.oxy.base_oxy import Oxy
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class MyCustomTool(Oxy):
    def __init__(self, **kwargs):
        super().__init__(
            name="my_tool",
            desc="A custom tool implementation",
            category="tool",
            **kwargs
        )
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # Custom execution logic
        result = self.process_input(oxy_request.arguments)
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=result
        )
```

## Thread Safety

The Oxy class uses `asyncio.Semaphore` for concurrency control, limiting simultaneous executions to the `semaphore` value.

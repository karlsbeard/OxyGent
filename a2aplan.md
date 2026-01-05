# Google A2A Protocol Integration Plan for OxyGent

**Version**: 1.1
**Date**: January 5, 2026
**Status**: Revised (Aligned to A2A v1.0 spec; ready for implementation)
**Branch**: feature_a2a

**Protocol Baseline**:
- A2A Protocol Specification: v1.0 (draft, `latest`)
- Primary binding for OxyGent implementation: **JSON-RPC 2.0 over HTTP(S)** + **SSE** (`text/event-stream`)
- Notes:
  - JSON-RPC binding method names are **PascalCase** (e.g., `SendMessage`, `GetTask`), matching the spec.
  - Agent Card discovery uses the **well-known root path**: `GET /.well-known/agent-card.json`.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Background & Motivation](#2-background--motivation)
3. [A2A Protocol Overview](#3-a2a-protocol-overview)
4. [Architecture Design](#4-architecture-design)
5. [Module Structure](#5-module-structure)
6. [Detailed Component Design](#6-detailed-component-design)
7. [Implementation Phases](#7-implementation-phases)
8. [Testing Strategy](#8-testing-strategy)
9. [Configuration](#9-configuration)
10. [Usage Examples](#10-usage-examples)
11. [Appendix](#11-appendix)

---

## 1. Executive Summary

### 1.1 Objective

Integrate Google's Agent-to-Agent (A2A) protocol into the OxyGent framework, enabling:

- **OxyGent as A2A Client**: Discover and invoke external A2A-compliant agents
- **OxyGent as A2A Server**: Expose OxyGent agents as A2A-compliant endpoints

### 1.2 Key Decisions

| Aspect | Decision |
|--------|----------|
| **Direction** | Bidirectional (Client + Server) |
| **Transport** | JSON-RPC (HTTP) + SSE + Webhooks |
| **Agent Hierarchy** | Hybrid (A2AAgent + A2ATool) |
| **Authentication** | Pluggable (API Key, OAuth 2.0, Bearer) |

### 1.3 Timeline

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1 | 3-4 days | Foundation (Schemas + Basic Client) |
| Phase 2 | 3-4 days | Full Client (A2AAgent + Streaming) |
| Phase 3 | 4-5 days | Server Implementation |
| Phase 4 | 2-3 days | Webhook Support |
| Phase 5 | 2-3 days | Polish & Documentation |
| **Total** | **14-19 days** | |

---

## 2. Background & Motivation

### 2.1 Why A2A?

Google's Agent-to-Agent (A2A) protocol is an open standard (Apache 2.0, Linux Foundation) for AI agent interoperability. With 50+ industry partners (Salesforce, SAP, LangChain, Cohere), A2A is becoming the de facto standard for agent-to-agent communication.

**A2A vs MCP:**
- **MCP** (Model Context Protocol): Agent ↔ Tool communication
- **A2A**: Agent ↔ Agent communication (peer-level)

### 2.2 Benefits for OxyGent

1. **Ecosystem Access**: Connect with any A2A-compliant agent (Google, Salesforce, etc.)
2. **Federation**: OxyGent systems can interoperate with each other via standard protocol
3. **Enterprise Adoption**: A2A compliance signals enterprise-readiness
4. **Future-Proofing**: Early adoption of emerging industry standard

### 2.3 Current OxyGent Capabilities

OxyGent already has strong foundations for A2A integration:

| Capability | Existing Implementation | A2A Analog |
|------------|------------------------|------------|
| Remote Agents | `SSEOxyGent`, `RemoteAgent` | A2A Client |
| Service Discovery | `BankClient` pattern | Agent Card fetching |
| Protocol Clients | `BaseMCPClient` hierarchy | `BaseA2AClient` |
| Streaming | SSE in `sse_oxy_agent.py` | `SendStreamingMessage` / `SubscribeToTask` |
| Web Endpoints | `routes.py` FastAPI | A2A JSON-RPC routes |

---

## 3. A2A Protocol Overview

### 3.1 Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                     A2A Protocol Stack                       │
├─────────────────────────────────────────────────────────────┤
│  Discovery Layer                                             │
│  └─ Agent Card: /.well-known/agent-card.json                │
│     ├─ protocolVersion, name, description, version          │
│     ├─ supportedInterfaces (JSONRPC / HTTP+JSON / GRPC)     │
│     ├─ capabilities (streaming, pushNotifications, ...)     │
│     ├─ securitySchemes + security requirements              │
│     └─ skills[] (id, name, description, inputModes, ...)    │
├─────────────────────────────────────────────────────────────┤
│  Communication Layer                                         │
│  └─ JSON-RPC 2.0 over HTTPS (primary for OxyGent)            │
│     ├─ SendMessage (sync; returns SendMessageResponse)       │
│     ├─ SendStreamingMessage (SSE; streams StreamResponse)    │
│     ├─ GetTask / ListTasks / CancelTask                      │
│     ├─ SubscribeToTask (SSE; streams StreamResponse)         │
│     └─ *TaskPushNotificationConfig methods                   │
│                                                             │
│  └─ HTTP+JSON/REST (optional compatibility)                  │
│     ├─ POST /v1/message:send / POST /v1/message:stream       │
│     └─ GET /v1/tasks / POST /v1/tasks/{id}:subscribe/...     │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                  │
│  ├─ Message: {role, parts[], metadata}                      │
│  ├─ Part: TextPart | FilePart | DataPart                    │
│  ├─ Task: {id, contextId, status, artifacts[], history}     │
│  └─ Artifact: {artifactId, name, description, parts[]}      │
├─────────────────────────────────────────────────────────────┤
│  Task Lifecycle                                              │
│  submitted → working → completed|failed|canceled|input-required │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Key Operations & Bindings

> A2A defines binding-independent operations (Send Message / Stream / Task ops). Concrete names differ per binding.
> This plan targets **JSON-RPC binding** as the primary interoperability surface.

| Operation | JSON-RPC Method (spec) | HTTP+JSON/REST Endpoint (spec) | Response |
|---|---|---|---|
| Get Agent Card | *(not JSON-RPC)* | `GET /.well-known/agent-card.json` | `AgentCard` |
| Send Message | `SendMessage` | `POST /v1/message:send` | `SendMessageResponse` (`task` or `message`) |
| Send Streaming Message | `SendStreamingMessage` | `POST /v1/message:stream` (SSE) | SSE stream of `StreamResponse` |
| Get Task | `GetTask` | `GET /v1/tasks/{id}` | `Task` |
| List Tasks | `ListTasks` | `GET /v1/tasks` | `ListTasksResponse` (paging + tasks) |
| Cancel Task | `CancelTask` | `POST /v1/tasks/{id}:cancel` | `Task` |
| Subscribe to Task | `SubscribeToTask` | `POST /v1/tasks/{id}:subscribe` (SSE) | SSE stream of `StreamResponse` |

### 3.3 Agent Card Example (Spec-shaped)

```json
{
  "protocolVersion": "1.0",
  "name": "OxyGent Multi-Agent System",
  "description": "Production-ready multi-agent framework",
  "version": "1.0.0",
  "provider": {
    "organization": "JD.com",
    "url": "https://oxygent.jd.com"
  },
  "supportedInterfaces": [
    {"url": "https://oxygent.example.com/a2a/rpc", "protocolBinding": "JSONRPC"},
    {"url": "https://oxygent.example.com/a2a/v1", "protocolBinding": "HTTP+JSON"}
  ],
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "securitySchemes": {
    "api_key": {
      "apiKeySecurityScheme": {
        "location": "header",
        "name": "X-API-Key",
        "description": "OxyGent A2A API key"
      }
    }
  },
  "security": [{"api_key": []}],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"],
  "skills": [
    {
      "id": "time_agent",
      "name": "Time Agent",
      "description": "Query and manipulate time information",
      "tags": ["time", "datetime"],
      "inputModes": ["text/plain"],
      "outputModes": ["text/plain"]
    }
  ]
}
```

---

## 4. Architecture Design

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         OxyGent MAS                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Agent Layer                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │  │
│  │  │ LocalAgent  │  │ A2AAgent    │  │ SSEOxyGent      │   │  │
│  │  │ (ReAct,Chat)│  │ (NEW)       │  │ (existing)      │   │  │
│  │  └─────────────┘  └──────┬──────┘  └─────────────────┘   │  │
│  └──────────────────────────┼────────────────────────────────┘  │
│                              │                                    │
│  ┌──────────────────────────┼────────────────────────────────┐  │
│  │                    A2A Module (NEW)                        │  │
│  │  ┌─────────────────┐     │     ┌─────────────────────┐   │  │
│  │  │  A2A Client     │◄────┴────►│  A2A Server         │   │  │
│  │  │  ├─BaseA2AClient│           │  ├─AgentCardGen     │   │  │
│  │  │  ├─A2AAgent     │           │  ├─A2ARoutes        │   │  │
│  │  │  └─A2ATool      │           │  ├─MessageHandler   │   │  │
│  │  └─────────────────┘           │  └─TaskStore        │   │  │
│  │           │                     └──────────┬──────────┘   │  │
│  │           │                                │               │  │
│  │  ┌────────┴────────┐           ┌──────────┴──────────┐   │  │
│  │  │  Auth Layer     │           │  Webhook Layer      │   │  │
│  │  │  ├─APIKeyAuth   │           │  ├─WebhookHandler   │   │  │
│  │  │  ├─OAuth2Auth   │           │  └─WebhookSender    │   │  │
│  │  │  └─BearerAuth   │           │                     │   │  │
│  │  └─────────────────┘           └─────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    External A2A Agents                     │  │
│  │  Google Agents │ Salesforce │ LangChain │ Other OxyGent   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Data Flow

#### Client Flow (OxyGent → External A2A Agent)

```
User Query
    │
    ▼
OxyGent Master Agent
    │
    ▼ (delegates to A2AAgent)
A2AAgent._execute()
    │
    ├─► Convert OxyRequest → A2A Message
    │
    ├─► Auth: Get headers from AuthHandler
    │
    ├─► Fetch `GET /.well-known/agent-card.json` (root) and select JSONRPC interface URL
    ├─► HTTP POST (JSON-RPC)
    │   ├─ SendMessage (sync)
    │   └─ SendStreamingMessage (SSE)
    ├─► Receive Task/Events
    │
    └─► Convert A2A Task/Events → OxyResponse
```

#### Server Flow (External A2A Client → OxyGent)

```
External A2A Client
    │
    ▼
/.well-known/agent-card.json → AgentCardGenerator
    │
    ▼
POST /a2a/rpc (JSON-RPC)
    │
    ▼
A2ARoutes.handle_jsonrpc()
    │
    ├─► Validate Auth
    │
    ├─► Route by method (JSON-RPC binding):
    │   ├─ SendMessage / SendStreamingMessage
    │   ├─ GetTask / ListTasks / CancelTask
    │   └─ SubscribeToTask
    │
    ├─► MessageHandler:
    │   ├─ Convert A2A Message → OxyRequest
    │   ├─ Execute via MAS
    │   └─ Convert OxyResponse → A2A Task
    │
    └─► Return JSON-RPC Response / SSE Stream
```

### 4.3 Hybrid Hierarchy Design

**A2AAgent** (Full Agent Semantics):
- Multi-turn conversation support via `contextId`
- Streaming responses via SSE
- Task lifecycle management
- Appears as remote agent in MAS hierarchy

**A2ATool** (Simple Tool Access):
- Single-shot invocations
- Lightweight, no conversation context
- Appears as tool in MAS hierarchy

```python
# Usage as Agent (full capabilities)
oxy_space = [
    oxy.A2AAgent(
        name="external_assistant",
        base_url="https://assistant.example.com",
        auth_config={"type": "api_key", "key": "xxx"}
    ),
    oxy.ReActAgent(
        is_master=True,
        sub_agents=["external_assistant"]  # A2A agent as sub-agent
    )
]

# Usage as Tool (lightweight)
oxy_space = [
    oxy.BaseA2AClient(
        name="weather_service",
        base_url="https://weather.example.com"
        # Auto-creates A2ATool for each skill
    ),
    oxy.ReActAgent(
        is_master=True,
        tools=["weather_service"]  # A2A skills as tools
    )
]
```

---

## 5. Module Structure

### 5.1 Directory Layout

```
oxygent/
└── oxy/
    └── a2a/                              # NEW MODULE
        ├── __init__.py                   # Public exports
        │
        ├── schemas/                      # Pydantic models
        │   ├── __init__.py
        │   ├── agent_card.py            # AgentCard, AgentSkill, AgentCapabilities
        │   ├── messages.py              # Message, Part (Text/File/Data)
        │   ├── tasks.py                 # Task, TaskState, TaskStatus, Artifact
        │   ├── jsonrpc.py               # JSONRPCRequest, JSONRPCResponse
        │   └── auth.py                  # AuthConfig schemas
        │
        ├── client/                       # Client components
        │   ├── __init__.py
        │   ├── base_a2a_client.py       # BaseA2AClient (discovers skills)
        │   ├── a2a_agent.py             # A2AAgent (full agent semantics)
        │   ├── a2a_tool.py              # A2ATool (wraps single skill)
        │   ├── discovery.py             # AgentCardFetcher, cache
        │   └── task_manager.py          # Client-side task tracking
        │
        ├── server/                       # Server components
        │   ├── __init__.py
        │   ├── agent_card_generator.py  # Generate Agent Card from MAS
        │   ├── a2a_routes.py            # FastAPI router for A2A
        │   ├── message_handler.py       # Process A2A messages
        │   ├── task_store.py            # ES-backed task persistence
        │   └── sse_broadcaster.py       # Stream task updates
        │
        ├── auth/                         # Authentication layer
        │   ├── __init__.py
        │   ├── base_auth.py             # BaseA2AAuth (abstract)
        │   ├── api_key_auth.py          # API key authentication
        │   ├── bearer_auth.py           # Bearer token authentication
        │   ├── oauth2_auth.py           # OAuth 2.0 with refresh
        │   └── auth_factory.py          # Create handler from config
        │
        ├── webhooks/                     # Push notification support
        │   ├── __init__.py
        │   ├── webhook_handler.py       # Process incoming webhooks
        │   ├── webhook_sender.py        # Send push notifications
        │   └── webhook_config.py        # PushNotificationConfig
        │
        └── utils/                        # Utilities
            ├── __init__.py
            ├── jsonrpc_utils.py         # JSON-RPC 2.0 helpers
            └── streaming_utils.py       # SSE utilities
```

### 5.2 Public API (`__init__.py`)

```python
# oxygent/oxy/a2a/__init__.py

from .client.base_a2a_client import BaseA2AClient
from .client.a2a_agent import A2AAgent
from .client.a2a_tool import A2ATool
from .server.a2a_routes import a2a_router
from .server.agent_card_generator import AgentCardGenerator
from .auth.api_key_auth import APIKeyAuth
from .auth.oauth2_auth import OAuth2Auth
from .auth.bearer_auth import BearerAuth
from .schemas.agent_card import AgentCard, AgentSkill
from .schemas.tasks import Task, TaskState

__all__ = [
    # Client
    "BaseA2AClient",
    "A2AAgent",
    "A2ATool",
    # Server
    "a2a_router",
    "AgentCardGenerator",
    # Auth
    "APIKeyAuth",
    "OAuth2Auth",
    "BearerAuth",
    # Schemas
    "AgentCard",
    "AgentSkill",
    "Task",
    "TaskState",
]
```

---

## 6. Detailed Component Design

### 6.1 Schemas

#### Agent Card (`schemas/agent_card.py`) — aligned to A2A v1.0

```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AgentProvider(BaseModel):
    organization: str
    url: Optional[str] = None

class AgentCapabilities(BaseModel):
    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False

class AgentInterface(BaseModel):
    url: str
    protocolBinding: str  # e.g. "JSONRPC" | "HTTP+JSON" | "GRPC"
    tenant: Optional[str] = None

class SecurityScheme(BaseModel):
    # Discriminated union in spec; here we model it as a thin dict-shaped object
    apiKeySecurityScheme: Optional[Dict[str, Any]] = None
    httpAuthSecurityScheme: Optional[Dict[str, Any]] = None
    oauth2SecurityScheme: Optional[Dict[str, Any]] = None
    openIdConnectSecurityScheme: Optional[Dict[str, Any]] = None
    mtlsSecurityScheme: Optional[Dict[str, Any]] = None

class AgentSkill(BaseModel):
    id: str
    name: str
    description: str
    tags: List[str] = []
    examples: List[str] = []
    inputModes: List[str] = ["text/plain"]
    outputModes: List[str] = ["text/plain"]
    security: Optional[List[Dict[str, List[str]]]] = None

class AgentCard(BaseModel):
    protocolVersion: Optional[str] = "1.0"
    name: str
    description: str
    version: str = "1.0.0"
    documentationUrl: Optional[str] = None
    provider: Optional[AgentProvider] = None
    capabilities: AgentCapabilities = AgentCapabilities()
    supportedInterfaces: Optional[List[AgentInterface]] = None
    # Deprecated fields retained for backward compatibility if needed:
    url: Optional[str] = None
    preferredTransport: Optional[str] = None
    additionalInterfaces: Optional[List[AgentInterface]] = None
    securitySchemes: Optional[Dict[str, SecurityScheme]] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    defaultInputModes: List[str] = ["text/plain"]
    defaultOutputModes: List[str] = ["text/plain"]
    skills: List[AgentSkill] = []
```

#### Messages (`schemas/messages.py`)

```python
from pydantic import BaseModel
from typing import Literal, Union, List, Dict, Any, Optional

class PartBase(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

class TextPart(PartBase):
    # Spec: Part.text is a string
    text: str

class FilePart(BaseModel):
    # Spec: FilePart has exactly one of fileWithUri / fileWithBytes
    fileWithUri: Optional[str] = None
    fileWithBytes: Optional[str] = None  # base64
    mediaType: Optional[str] = None
    name: Optional[str] = None

class FileContainerPart(PartBase):
    file: FilePart

class DataPart(BaseModel):
    data: Dict[str, Any]

class DataContainerPart(PartBase):
    # Spec: Part.data is a DataPart object
    data: DataPart

Part = Union[TextPart, FileContainerPart, DataContainerPart]

class Message(BaseModel):
    role: Literal["user", "agent"]
    messageId: str
    contextId: Optional[str] = None
    taskId: Optional[str] = None
    parts: List[Part]
    metadata: Optional[Dict[str, Any]] = None
    extensions: Optional[List[str]] = None
    referenceTaskIds: Optional[List[str]] = None
```

#### Tasks (`schemas/tasks.py`)

```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

class TaskStatus(BaseModel):
    state: TaskState
    message: Optional[Message] = None
    timestamp: Optional[str] = None

class Artifact(BaseModel):
    artifactId: str
    name: Optional[str] = None
    description: Optional[str] = None
    parts: List[Part]
    metadata: Optional[Dict[str, Any]] = None

class Task(BaseModel):
    id: str
    contextId: Optional[str] = None
    status: TaskStatus
    artifacts: List[Artifact] = []
    history: Optional[List[TaskStatus]] = None
    metadata: Optional[Dict[str, Any]] = None

class ListTasksResponse(BaseModel):
    tasks: List[Task]
    nextPageToken: str = ""
    pageSize: int = 50
    totalSize: int = 0
```

### 6.2 Client Components

#### BaseA2AClient (`client/base_a2a_client.py`)

```python
from oxygent.oxy.base_tool import BaseTool
from oxygent.schemas import OxyRequest, OxyResponse, OxyState
from typing import Optional, List, Dict, Any
from pydantic import AnyUrl
import aiohttp

class BaseA2AClient(BaseTool):
    """Base client for A2A protocol.

    Notes:
    - Agent Card MUST be fetched from `GET /.well-known/agent-card.json` on the server origin.
    - RPC URL is selected from AgentCard.supportedInterfaces (prefer protocolBinding == "JSONRPC").
    """

    base_url: AnyUrl  # server origin, e.g. https://agent.example.com
    rpc_url: Optional[AnyUrl] = None  # resolved from AgentCard.supportedInterfaces
    auth_config: Optional[Dict[str, Any]] = None
    agent_card: Optional[AgentCard] = None
    included_skill_ids: List[str] = []
    timeout: float = 60.0

    _auth_handler: Optional[BaseA2AAuth] = None
    _http_client: Optional[aiohttp.ClientSession] = None

    async def init(self, is_fetch_skills: bool = True):
        """Initialize client: fetch Agent Card and register skills."""
        # Create auth handler
        if self.auth_config:
            self._auth_handler = AuthFactory.create(self.auth_config)

        # Fetch Agent Card
        self.agent_card = await self._fetch_agent_card()

        # Register skills as tools
        if is_fetch_skills:
            await self._register_skills()

    async def _fetch_agent_card(self) -> AgentCard:
        """Fetch Agent Card from /.well-known/agent-card.json (root path)."""
        url = f"{self.base_url}/.well-known/agent-card.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return AgentCard(**data)

    def _select_jsonrpc_interface(self) -> str:
        if not self.agent_card or not self.agent_card.supportedInterfaces:
            # Backward compat: fall back to deprecated `url`
            if self.agent_card and self.agent_card.url:
                return self.agent_card.url
            raise ValueError("AgentCard.supportedInterfaces is missing; cannot resolve JSON-RPC endpoint")

        for itf in self.agent_card.supportedInterfaces:
            if (itf.protocolBinding or "").upper() == "JSONRPC":
                return itf.url
        raise ValueError("No JSONRPC interface found in AgentCard.supportedInterfaces")

    async def _register_skills(self):
        """Create A2ATool for each skill in Agent Card."""
        for skill in self.agent_card.skills:
            if self.included_skill_ids and skill.id not in self.included_skill_ids:
                continue

            tool = A2ATool(
                name=f"{self.name}_{skill.id}",
                desc=skill.description,
                skill_id=skill.id,
                a2a_client=self,
                input_modes=skill.inputModes,
                output_modes=skill.outputModes,
            )
            self.mas.add_oxy(tool)
            self.add_permitted_tool(tool.name)

    async def send_message(
        self,
        message: Message,
        context_id: Optional[str] = None,
        stream: bool = False
    ) -> Union[Task, AsyncIterator]:
        """Send message to A2A agent (JSON-RPC binding)."""
        if context_id and not getattr(message, "contextId", None):
            # Prefer Message.contextId for conversation continuity.
            message.contextId = context_id

        headers = {"Content-Type": "application/json"}
        if self._auth_handler:
            headers.update(await self._auth_handler.get_auth_headers())

        payload = {
            "jsonrpc": "2.0",
            "id": generate_uuid(),
            "method": "SendStreamingMessage" if stream else "SendMessage",
            "params": {
                "message": message.model_dump(),
                # Optional: pass routing hints / vendor extensions here.
                # Example: {"skillId": "weather"}
                "metadata": None,
                # Optional: SendMessageConfiguration may be added here (acceptedOutputModes, blocking, ...)
            }
        }

        if stream:
            return self._stream_response(payload, headers)
        else:
            return await self._sync_response(payload, headers)

    async def _sync_response(self, payload: dict, headers: dict) -> Task:
        """Synchronous SendMessage.

        Spec: JSON-RPC result is a SendMessageResponse which contains one of {task, message}.
        """
        if not self.rpc_url:
            self.rpc_url = self._select_jsonrpc_interface()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                str(self.rpc_url),
                json=payload,
                headers=headers,
                timeout=self.timeout
            ) as response:
                data = await response.json()
                result = data.get("result") or {}
                if "task" in result:
                    return Task(**result["task"])
                raise ValueError("SendMessage returned Message (no task); handle this branch in client")

    async def _stream_response(self, payload: dict, headers: dict) -> AsyncIterator:
        """Streaming message/stream via SSE."""
        # Implementation follows SSEOxyGent pattern
        ...
```

#### A2AAgent (`client/a2a_agent.py`)

```python
from oxygent.oxy.agents.remote_agent import RemoteAgent
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class A2AAgent(RemoteAgent):
    """Full-featured A2A agent with multi-turn conversation support."""

    base_url: AnyUrl
    auth_config: Optional[Dict[str, Any]] = None
    context_id: Optional[str] = None  # Current conversation

    _a2a_client: Optional[BaseA2AClient] = None

    async def init(self):
        """Initialize A2A client and build organization."""
        self._a2a_client = BaseA2AClient(
            name=f"{self.name}_client",
            base_url=self.base_url,
            auth_config=self.auth_config,
            mas=self.mas
        )
        await self._a2a_client.init(is_fetch_skills=False)
        self.org = self._build_org_from_agent_card()

    def _build_org_from_agent_card(self) -> dict:
        """Convert Agent Card skills to OxyGent organization format."""
        children = []
        for skill in self._a2a_client.agent_card.skills:
            children.append({
                "name": skill.id,
                "type": "tool",
                "is_remote": True,
                "children": []
            })
        return {"name": self.name, "type": "agent", "children": children}

    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute via A2A protocol."""
        # Convert OxyRequest to A2A Message
        message = self._convert_to_a2a_message(oxy_request)

        # Use streaming if available
        if self._a2a_client.agent_card.capabilities.streaming:
            return await self._execute_streaming(message, oxy_request)
        else:
            return await self._execute_sync(message, oxy_request)

    def _convert_to_a2a_message(self, oxy_request: OxyRequest) -> Message:
        """Convert OxyRequest to A2A Message."""
        query = oxy_request.arguments.get("query", "")
        return Message(
            role="user",
            messageId=generate_uuid(),
            contextId=self.context_id,
            parts=[TextPart(text=query)],
            metadata={"oxy_trace_id": oxy_request.current_trace_id}
        )

    async def _execute_streaming(self, message: Message, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with streaming.

        JSON-RPC streaming returns an SSE stream of JSON-RPC envelopes.
        Each envelope's result SHOULD be a StreamResponse object with exactly one of:
        {task, message, statusUpdate, artifactUpdate}.
        """
        async for event in self._a2a_client.send_message(
            message=message,
            context_id=self.context_id,
            stream=True
        ):
            # Forward intermediate events (pseudo-structure)
            result = event.get("result") if isinstance(event, dict) else None
            if not isinstance(result, dict):
                continue
            if "statusUpdate" in result:
                await oxy_request.send_message({"type": "a2a_status", "payload": result["statusUpdate"]})
            elif "artifactUpdate" in result:
                await oxy_request.send_message({"type": "a2a_artifact", "payload": result["artifactUpdate"]})
            elif "task" in result and result["task"].get("status", {}).get("state") in ("completed", "failed", "canceled", "cancelled", "rejected"):
                return self._convert_task_to_response(Task(**result["task"]))

        raise RuntimeError("Streaming ended without terminal Task")
```

### 6.3 Server Components

#### A2A Routes (`server/a2a_routes.py`)

```python
from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

a2a_router = APIRouter(prefix="/a2a", tags=["A2A Protocol"])

"""IMPORTANT:

Spec requires the public Agent Card to be available at the ROOT well-known path:
`GET /.well-known/agent-card.json`.

Implementation plan:
- Add a root FastAPI route (outside this router) that calls AgentCardGenerator.
- Optionally keep this `/a2a/.well-known/...` route as a backward-compatible alias.
"""

@a2a_router.post("/rpc")
async def handle_jsonrpc(request: Request):
    """Main JSON-RPC 2.0 endpoint (JSON-RPC binding)."""
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    handler = A2AMessageHandler(request.app.state.mas)

    try:
        if method == "SendMessage":
            result = await handler.handle_send_message(params)
        elif method == "SendStreamingMessage":
            return EventSourceResponse(handler.handle_send_streaming_message(params, request_id=request_id))
        elif method == "GetTask":
            result = await handler.handle_get_task(params)
        elif method == "ListTasks":
            result = await handler.handle_list_tasks(params)
        elif method == "CancelTask":
            result = await handler.handle_cancel_task(params)
        elif method == "SubscribeToTask":
            return EventSourceResponse(handler.handle_subscribe_to_task(params, request_id=request_id))
        else:
            raise ValueError(f"Unknown method: {method}")

        return {"jsonrpc": "2.0", "id": request_id, "result": result.model_dump() if hasattr(result, "model_dump") else result}
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32000, "message": str(e)}
        }
```

#### Agent Card Generator (`server/agent_card_generator.py`)

```python
class AgentCardGenerator:
    """Generate A2A Agent Card from OxyGent MAS configuration."""

    def __init__(self, mas: MAS):
        self.mas = mas

    def generate(self) -> AgentCard:
        """Build Agent Card from registered agents."""
        skills = []

        for oxy_name, oxy in self.mas.oxy_name_to_oxy.items():
            if isinstance(oxy, (LocalAgent, BaseAgent)):
                if oxy.is_entrance or oxy.is_master:
                    skill = self._oxy_to_skill(oxy)
                    skills.append(skill)

        return AgentCard(
            protocolVersion="1.0",
            name=Config.get_app_name(),
            description=f"OxyGent Multi-Agent System",
            version=Config.get_app_version(),
            provider=AgentProvider(
                organization="OxyGent",
                url="https://oxygent.jd.com"
            ),
            supportedInterfaces=[
                {"url": f"{Config.get_server_url()}/a2a/rpc", "protocolBinding": "JSONRPC"},
                # Optional compatibility surface:
                {"url": f"{Config.get_server_url()}/a2a/v1", "protocolBinding": "HTTP+JSON"},
            ],
            capabilities=AgentCapabilities(
                streaming=True,
                pushNotifications=Config.get_a2a_push_enabled(),
                stateTransitionHistory=True
            ),
            # Spec-shaped security declaration (details depend on deployment).
            securitySchemes={
                "api_key": {"apiKeySecurityScheme": {"location": "header", "name": "X-API-Key"}}
            },
            security=[{"api_key": []}],
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain"],
            skills=skills
        )

    def _oxy_to_skill(self, oxy: Oxy) -> AgentSkill:
        """Convert Oxy instance to AgentSkill."""
        return AgentSkill(
            id=oxy.name,
            name=oxy.name,
            description=oxy.desc,
            tags=getattr(oxy, 'tags', []),
            inputModes=["text/plain"],
            outputModes=["text/plain"]
        )
```

### 6.4 Authentication Layer

#### Base Auth (`auth/base_auth.py`)

```python
from abc import ABC, abstractmethod
from typing import Dict
from fastapi import Request

class BaseA2AAuth(ABC):
    """Abstract base for A2A authentication handlers."""

    @abstractmethod
    async def get_auth_headers(self) -> Dict[str, str]:
        """Return headers for outgoing requests."""
        pass

    @abstractmethod
    async def validate_request(self, request: Request) -> bool:
        """Validate incoming request authentication."""
        pass
```

#### API Key Auth (`auth/api_key_auth.py`)

```python
class APIKeyAuth(BaseA2AAuth):
    """API Key authentication."""

    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    async def get_auth_headers(self) -> Dict[str, str]:
        return {self.header_name: self.api_key}

    async def validate_request(self, request: Request) -> bool:
        key = request.headers.get(self.header_name)
        return key == self.api_key
```

#### OAuth2 Auth (`auth/oauth2_auth.py`)

```python
class OAuth2Auth(BaseA2AAuth):
    """OAuth 2.0 authentication with automatic token refresh."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        scopes: List[str] = []
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scopes = scopes
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    async def get_auth_headers(self) -> Dict[str, str]:
        token = await self._ensure_valid_token()
        return {"Authorization": f"Bearer {token}"}

    async def _ensure_valid_token(self) -> str:
        if self._access_token and self._token_expiry > datetime.now():
            return self._access_token

        # Refresh token
        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": " ".join(self.scopes)
            }) as response:
                data = await response.json()
                self._access_token = data["access_token"]
                self._token_expiry = datetime.now() + timedelta(seconds=data["expires_in"])
                return self._access_token
```

---

## 7. Implementation Phases

### Phase 1: Foundation (3-4 days)

**Goal**: Core schemas and basic client functionality.

**Tasks**:
- [x] Create `oxygent/oxy/a2a/` directory structure
- [ ] Implement all Pydantic schemas
- [ ] Implement `BaseA2AClient` with Agent Card fetching
- [ ] Implement `A2ATool` for simple skill invocation
- [ ] Add `APIKeyAuth` authentication
- [ ] Unit tests for schemas and basic client

**Files Created**:
```
oxygent/oxy/a2a/__init__.py
oxygent/oxy/a2a/schemas/__init__.py
oxygent/oxy/a2a/schemas/agent_card.py
oxygent/oxy/a2a/schemas/messages.py
oxygent/oxy/a2a/schemas/tasks.py
oxygent/oxy/a2a/schemas/jsonrpc.py
oxygent/oxy/a2a/client/__init__.py
oxygent/oxy/a2a/client/base_a2a_client.py
oxygent/oxy/a2a/client/a2a_tool.py
oxygent/oxy/a2a/auth/__init__.py
oxygent/oxy/a2a/auth/base_auth.py
oxygent/oxy/a2a/auth/api_key_auth.py
test/unittest/a2a/test_schemas.py
test/unittest/a2a/test_base_client.py
```

### Phase 2: Full Client (3-4 days)

**Goal**: Complete client with streaming and multi-turn support.

**Tasks**:
- [ ] Implement `A2AAgent` with full agent semantics
- [ ] Add SSE streaming support (following `sse_oxy_agent.py` pattern)
- [ ] Implement `TaskManager` for task lifecycle
- [ ] Add `OAuth2Auth` and `BearerAuth`
- [ ] Implement `AuthFactory`
- [ ] Multi-turn conversation via `contextId`
- [ ] Integration tests with mock A2A server

**Files Created**:
```
oxygent/oxy/a2a/client/a2a_agent.py
oxygent/oxy/a2a/client/task_manager.py
oxygent/oxy/a2a/client/discovery.py
oxygent/oxy/a2a/auth/oauth2_auth.py
oxygent/oxy/a2a/auth/bearer_auth.py
oxygent/oxy/a2a/auth/auth_factory.py
oxygent/oxy/a2a/utils/__init__.py
oxygent/oxy/a2a/utils/streaming_utils.py
test/unittest/a2a/test_a2a_agent.py
test/unittest/a2a/mock_a2a_server.py
```

### Phase 3: Server (4-5 days)

**Goal**: Expose OxyGent as A2A-compliant endpoint.

**Tasks**:
- [ ] Implement `AgentCardGenerator`
- [ ] Create A2A FastAPI routes
- [ ] Implement `A2AMessageHandler`
- [ ] Implement `TaskStore` with ES persistence
- [ ] Add `SSEBroadcaster` for streaming
- [ ] Integrate with MAS initialization
- [ ] Server-side authentication validation

**Files Created**:
```
oxygent/oxy/a2a/server/__init__.py
oxygent/oxy/a2a/server/agent_card_generator.py
oxygent/oxy/a2a/server/a2a_routes.py
oxygent/oxy/a2a/server/message_handler.py
oxygent/oxy/a2a/server/task_store.py
oxygent/oxy/a2a/server/sse_broadcaster.py
test/unittest/a2a/test_server.py
```

**Files Modified**:
```
oxygent/mas.py          # Add A2A initialization
oxygent/routes.py       # Include A2A router + add ROOT well-known agent-card route
oxygent/config.py       # Add A2A config methods
oxygent/__init__.py     # Export A2A components
```

### Phase 4: Webhooks (2-3 days)

**Goal**: Push notification support for long-running tasks.

**Tasks**:
- [ ] Implement `WebhookHandler` for incoming notifications
- [ ] Implement `WebhookSender` for outgoing notifications
- [ ] Add `tasks/pushNotificationConfig/*` methods
- [ ] Webhook authentication support

**Files Created**:
```
oxygent/oxy/a2a/webhooks/__init__.py
oxygent/oxy/a2a/webhooks/webhook_handler.py
oxygent/oxy/a2a/webhooks/webhook_sender.py
oxygent/oxy/a2a/webhooks/webhook_config.py
test/unittest/a2a/test_webhooks.py
```

### Phase 5: Polish (2-3 days)

**Goal**: Production readiness.

**Tasks**:
- [ ] Comprehensive integration testing
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Usage examples
- [ ] Documentation updates

**Files Created**:
```
examples/a2a/__init__.py
examples/a2a/a2a_client_example.py
examples/a2a/a2a_server_example.py
examples/a2a/a2a_federation_example.py
docs/a2a_integration.md
```

**Files Modified**:
```
CLAUDE.md    # Add A2A section
README.md    # Add A2A feature mention
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```
test/unittest/a2a/
├── test_schemas.py              # Pydantic model validation
├── test_auth.py                 # Authentication handlers
├── test_base_client.py          # BaseA2AClient
├── test_a2a_agent.py            # A2AAgent
├── test_a2a_tool.py             # A2ATool
├── test_agent_card_gen.py       # AgentCardGenerator
├── test_message_handler.py      # Message processing
├── test_task_store.py           # Task persistence
└── test_webhooks.py             # Webhook handlers
```

### 8.2 Integration Tests

```
test/integration/a2a/
├── test_client_integration.py   # Client against mock server
├── test_server_integration.py   # Server endpoint testing
└── test_e2e_flow.py             # OxyGent ↔ OxyGent via A2A
```

### 8.3 Mock A2A Server

```python
# test/unittest/a2a/mock_a2a_server.py
from fastapi import FastAPI
from fastapi.testclient import TestClient

class MockA2AServer:
    """Mock A2A server for testing."""

    def __init__(self):
        self.app = FastAPI()
        self._setup_routes()
        self.client = TestClient(self.app)

    def _setup_routes(self):
        @self.app.get("/.well-known/agent-card.json")
        def agent_card():
            return {
                "name": "Mock A2A Agent",
                "protocolVersion": "1.0",
                "supportedInterfaces": [{"url": "http://localhost:8000/a2a/rpc", "protocolBinding": "JSONRPC"}],
                "skills": [...]
            }

        @self.app.post("/a2a/rpc")
        def jsonrpc(request: dict):
            # Handle JSON-RPC methods
            ...
```

---

## 9. Configuration

### 9.1 Config Additions (`config.json`)

```json
{
  "default": {
    "a2a": {
      "server_enabled": true,
      "push_notifications_enabled": false,
      "auth_schemes": ["apiKey"],
      "default_timeout": 60,
      "task_store_index": "${APP_NAME}_a2a_tasks"
    }
  }
}
```

### 9.2 Config Methods (`config.py`)

```python
@staticmethod
def get_a2a_server_enabled() -> bool:
    return Config._config.get("a2a", {}).get("server_enabled", False)

@staticmethod
def get_a2a_push_enabled() -> bool:
    return Config._config.get("a2a", {}).get("push_notifications_enabled", False)

@staticmethod
def get_a2a_auth_schemes() -> List[str]:
    return Config._config.get("a2a", {}).get("auth_schemes", ["apiKey"])

@staticmethod
def get_a2a_task_store_index() -> str:
    return Config._config.get("a2a", {}).get("task_store_index", f"{Config.get_app_name()}_a2a_tasks")
```

---

## 10. Usage Examples

### 10.1 Client: Calling External A2A Agent

```python
import asyncio
from oxygent import MAS, Config, oxy

Config.set_agent_llm_model("default_llm")

oxy_space = [
    oxy.HttpLLM(
        name="default_llm",
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_name=os.getenv("LLM_MODEL_NAME"),
    ),
    # A2A Agent (full capabilities)
    oxy.A2AAgent(
        name="external_assistant",
        base_url="https://assistant.example.com",
        auth_config={
            "type": "api_key",
            "api_key": os.getenv("EXTERNAL_API_KEY")
        }
    ),
    # Master agent with A2A sub-agent
    oxy.ReActAgent(
        is_master=True,
        name="master",
        sub_agents=["external_assistant"],
    ),
]

async def main():
    async with MAS(oxy_space=oxy_space) as mas:
        await mas.start_web_service(
            first_query="Ask the external assistant to help with this task"
        )

asyncio.run(main())
```

### 10.2 Client: Using A2A Skills as Tools

```python
oxy_space = [
    oxy.HttpLLM(name="default_llm", ...),

    # A2A Client (discovers skills as tools)
    oxy.BaseA2AClient(
        name="weather_service",
        base_url="https://weather-agent.example.com",
        auth_config={"type": "bearer", "token": os.getenv("WEATHER_TOKEN")}
    ),

    # Local agent using A2A tools
    oxy.ReActAgent(
        is_master=True,
        name="master",
        tools=["weather_service"],  # Auto-discovered skills
    ),
]
```

### 10.3 Server: Exposing OxyGent as A2A Endpoint

```python
from oxygent import MAS, Config, oxy

# Enable A2A server
Config.set("a2a.server_enabled", True)
Config.set("a2a.auth_schemes", ["apiKey"])

oxy_space = [
    oxy.HttpLLM(name="default_llm", ...),
    preset_tools.time_tools,
    oxy.ReActAgent(
        name="time_agent",
        desc="Query time information",
        tools=["time_tools"],
        is_entrance=True,  # Expose as A2A skill
    ),
    oxy.ReActAgent(
        is_master=True,
        name="master",
        sub_agents=["time_agent"],
    ),
]

async def main():
    async with MAS(oxy_space=oxy_space) as mas:
        # A2A endpoints available at:
        # GET  /.well-known/agent-card.json
        # POST /a2a/rpc (JSON-RPC)
        await mas.start_web_service()

asyncio.run(main())
```

### 10.4 Federation: OxyGent ↔ OxyGent via A2A

```python
# System A (Server)
oxy_space_a = [
    oxy.HttpLLM(name="llm", ...),
    preset_tools.math_tools,
    oxy.ReActAgent(
        name="math_agent",
        tools=["math_tools"],
        is_entrance=True,
    ),
]

# System B (Client)
oxy_space_b = [
    oxy.HttpLLM(name="llm", ...),
    oxy.A2AAgent(
        name="remote_math",
        base_url="http://system-a:8000",
    ),
    oxy.ReActAgent(
        is_master=True,
        sub_agents=["remote_math"],
    ),
]
```

---

## 11. Appendix

### 11.1 State Mapping

| OxyGent OxyState | A2A TaskState | Notes |
|------------------|---------------|-------|
| `CREATED` | `submitted` | Initial state |
| `RUNNING` | `working` | In progress |
| `COMPLETED` | `completed` | Success |
| `FAILED` | `failed` | Error |
| `CANCELED` | `canceled` / `cancelled` | User cancelled (string varies by binding/version; treat both as terminal) |
| `PAUSED` | `input-required` | Needs user input |
| `SKIPPED` | `rejected` | Prefer `rejected` for “refused/not performed” semantics |

### 11.2 Error Codes

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid request | Not valid JSON-RPC |
| -32601 | Method not found | Unknown method |
| -32602 | Invalid params | Invalid method params |
| -32603 | Internal error | Server error |
| -32000 | Task not found | Unknown task ID |
| -32001 | Auth failed | Authentication error |

### 11.3 References

- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A GitHub Repository](https://github.com/a2aproject/A2A)
- [Google A2A Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [OxyGent Documentation](http://oxygent.jd.com/docs/)

---

**Document Version**: 1.1
**Last Updated**: January 5, 2026
**Author**: Claude Code + OxyGent Team

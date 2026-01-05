# PRD: OxyGent Agent Skills System

## Product Requirements Document
**Version**: 2.0
**Date**: 2025-12-28
**Author**: Claude Code Analysis
**Status**: Draft for Review

---

## Executive Summary

OxyGent is a production-ready multi-agent framework for rapid agent development. This PRD proposes adding an **Agent Skills** system following the Claude Agent SDK pattern: **Markdown-based declarative instructions** that are dynamically loaded and injected into the agent's context through **LLM reasoning**.

### Core Design Philosophy

| Concept | Definition |
|---------|------------|
| **Skills** | Markdown-based instructions that extend agent capabilities through prompt injection |
| **Tools** | Code-based functions (FunctionHub, HttpTool, MCP) that execute specific operations |
| **Key Difference** | Skills = LLM-interpreted prompts; Tools = Code-executed functions |

### Architecture Summary: Progressive Disclosure + Context Modification

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SKILL EXECUTION FLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │  Startup │ -> │ Metadata     │ -> │ System       │ -> │ Agent     │ │
│  │          │    │ Index Only   │    │ Prompt       │    │ Ready     │ │
│  └──────────┘    │ (name+desc)  │    │ Preloaded    │    └───────────┘ │
│                  └──────────────┘    └──────────────┘                   │
│                                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │  User    │ -> │ LLM Semantic │ -> │ Match Skill  │ -> │ Invoke    │ │
│  │  Request │    │ Reasoning    │    │ Description  │    │ Skill Tool│ │
│  └──────────┘    └──────────────┘    └──────────────┘    └───────────┘ │
│                                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │  Load    │ -> │ Inject Full  │ -> │ Modify Exec  │ -> │ Continue  │ │
│  │  SKILL.md│    │ Instructions │    │ Environment  │    │ Task      │ │
│  └──────────┘    └──────────────┘    └──────────────┘    └───────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Problem Statement

### Current OxyGent Capabilities

OxyGent has a robust **Tool** system:
- `FunctionHub` for Python functions
- `HttpTool` for HTTP APIs
- `MCPClient` for MCP servers
- `BaseTool` for custom implementations

### What's Missing: Skills

Modern agent frameworks (Claude Agent SDK) distinguish between:

| Aspect | Tools | Skills |
|--------|-------|--------|
| **Definition** | Code (Python/API) | Markdown (SKILL.md) |
| **Registration** | Explicit code import | Filesystem auto-discovery |
| **Execution** | Direct function call | LLM prompt injection |
| **Invocation** | Agent explicitly calls | LLM decides when relevant |
| **Composition** | Code orchestration | LLM reasoning chains |
| **Loading** | All at startup | Progressive (metadata first) |

---

## Goals & Non-Goals

### Goals

| Priority | Goal | Success Metric |
|----------|------|----------------|
| P0 | SKILL.md file format (Claude Agent SDK compatible) | Skills defined in markdown |
| P0 | Progressive disclosure (metadata → full content) | < 10ms metadata load |
| P0 | LLM-based skill selection via semantic matching | > 85% correct skill selection |
| P0 | Dynamic prompt injection mechanism | Skills modify agent context |
| P1 | Execution environment modification (tool permissions) | Skills can restrict/grant tools |
| P1 | Filesystem auto-discovery | Skills from `.oxygent/skills/` |
| P2 | Skill marketplace/sharing | Skills installable from registry |

### Non-Goals (v1.0)

- ❌ Pipeline/Parallel code-based composition (skills use LLM reasoning)
- ❌ Wrapping tools as skills (they remain separate concepts)
- ❌ Concurrent skill execution (one active skill at a time)
- ❌ Visual skill builder UI
- ❌ Skill awareness for non-ReAct agents (v1.0 only ReActAgent is skill-aware to avoid context bloat)
- ❌ Sub-agent skill support (explicitly out of scope for v1.0)

---

## Architecture Design

### Core Principle: Skills ≠ Tools

```
┌─────────────────────────────────────────────────────────────────┐
│                        OxyGent Agent                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐ │
│  │       TOOLS             │    │         SKILLS              │ │
│  │  (Code Execution)       │    │  (Prompt Injection)         │ │
│  ├─────────────────────────┤    ├─────────────────────────────┤ │
│  │ • FunctionHub           │    │ • SKILL.md files            │ │
│  │ • HttpTool              │    │ • Markdown instructions     │ │
│  │ • MCPClient             │    │ • LLM-interpreted           │ │
│  │ • BaseTool subclasses   │    │ • Context modification      │ │
│  ├─────────────────────────┤    ├─────────────────────────────┤ │
│  │ Registration: Code      │    │ Registration: Filesystem    │ │
│  │ Execution: Direct call  │    │ Execution: Prompt inject    │ │
│  │ Loading: All at startup │    │ Loading: Progressive        │ │
│  └─────────────────────────┘    └─────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Progressive Disclosure Architecture

```
Phase 1: STARTUP (Lightweight)
┌─────────────────────────────────────────────────────────────────┐
│  Scan .oxygent/skills/*/SKILL.md                                │
│  Extract ONLY: name, description (from frontmatter)             │
│  Build: SkillMetadataIndex { name → description }               │
│  DO NOT load: Full markdown content, resources                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 2: SYSTEM PROMPT INJECTION
┌─────────────────────────────────────────────────────────────────┐
│  Inject skill catalog into agent's system prompt:               │
│                                                                  │
│  ## Available Skills                                             │
│  You have access to the following skills. When a user request   │
│  matches a skill's description, invoke it using the Skill tool. │
│                                                                  │
│  - **code-reviewer**: Review code for quality and security      │
│  - **web-researcher**: Research topics on the web               │
│  - **summarizer**: Summarize long documents                     │
│                                                                  │
│  To use a skill: Skill(name="skill-name")                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 3: LLM REASONING (Runtime)
┌─────────────────────────────────────────────────────────────────┐
│  User: "Review this Python file for security issues"            │
│                                                                  │
│  LLM Chain of Thought:                                          │
│  - User wants code review with security focus                   │
│  - Available skill: "code-reviewer" matches                     │
│  - Decision: Invoke Skill(name="code-reviewer")                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 4: SKILL LOADING (On-Demand)
┌─────────────────────────────────────────────────────────────────┐
│  Load full SKILL.md content from filesystem                     │
│  Load associated resources (templates, examples)                 │
│  Parse: instructions, allowed-tools, model preferences           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 5: CONTEXT INJECTION
┌─────────────────────────────────────────────────────────────────┐
│  Inject full skill instructions into conversation context:      │
│                                                                  │
│  [SKILL ACTIVATED: code-reviewer]                               │
│  ## Instructions                                                 │
│  When reviewing code:                                            │
│  1. Read the file(s) using the Read tool                        │
│  2. Analyze for security vulnerabilities...                     │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 6: ENVIRONMENT MODIFICATION
┌─────────────────────────────────────────────────────────────────┐
│  Modify agent's execution environment:                          │
│  - Tool permissions: allowed-tools: [Read, Glob, Grep]          │
│  - Model selection:  (if specified)         │
│  - Timeout adjustment: timeout: 300                              │
│  - Memory context: inject skill-specific memory                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 7: CONTINUE EXECUTION
┌─────────────────────────────────────────────────────────────────┐
│  Agent continues with:                                           │
│  - Enriched context (skill instructions)                        │
│  - Modified permissions (skill-allowed tools)                   │
│  - Task completion following skill guidance                     │
│                                                                  │
│  NOTE: One skill active at a time (non-concurrent)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## LLM-Based Skill Selection Mechanism

### How Agent Decides When to Use Skills

```
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL SELECTION PROCESS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SYSTEM PROMPT PRELOADING                                    │
│     ├─ Skill catalog injected at agent initialization           │
│     └─ Format: name + description pairs                         │
│                                                                  │
│  2. USER REQUEST ARRIVES                                        │
│     └─ "Help me review this code for security issues"           │
│                                                                  │
│  3. LLM SEMANTIC MATCHING                                       │
│     ├─ LLM reads user request                                   │
│     ├─ LLM scans skill descriptions in system prompt            │
│     └─ LLM identifies semantic overlap                          │
│                                                                  │
│  4. CHAIN-OF-THOUGHT REASONING                                  │
│     ├─ "User wants code review with security focus"             │
│     ├─ "Skill 'code-reviewer' handles code quality/security"    │
│     └─ "This skill is highly relevant to the request"           │
│                                                                  │
│  5. SKILL INVOCATION DECISION                                   │
│     ├─ LLM decides to invoke skill (autonomous)                 │
│     └─ Calls: Skill(name="code-reviewer")                       │
│                                                                  │
│  6. DYNAMIC FILTERING (Optional)                                │
│     ├─ If multiple skills match, LLM reasons about best fit     │
│     └─ Considers: specificity, context, user intent             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Characteristics

| Aspect | Implementation |
|--------|----------------|
| **Selection Method** | Pure LLM reasoning (no code-based matching) |
| **Matching Algorithm** | Semantic similarity via LLM understanding |
| **Decision Authority** | LLM autonomously decides when to use skills |
| **Fallback** | If no skill matches, agent uses base capabilities |
| **Concurrency** | One active skill at a time |

---

## SKILL.md File Format

### Standard Format (Claude Agent SDK Compatible)

```markdown
---
name: code-reviewer
description: Review code for quality, security, and best practices

# Optional metadata
version: "1.0.0"
author: "OxyGent Team"

# Tool permissions (modify agent's allowed tools when skill active)
allowed-tools:
  - Read
  - Glob
  - Grep

# Model preference (optional)


# Resource files (loaded with skill)
resources:
  - templates/review-template.md
  - examples/security-checklist.md
---

# Code Reviewer Skill

## Overview

This skill reviews code files for quality issues, security vulnerabilities,
and adherence to best practices.

## Instructions

When this skill is activated, follow these steps:

### Step 1: Understand the Request
- Identify which files need review
- Determine the focus area (security, quality, performance)
- Check the programming language

### Step 2: Read the Code
Use the Read tool to examine the target files:
- Read the main file(s) specified by the user
- If needed, use Glob to find related files
- Use Grep to search for specific patterns

### Step 3: Analyze for Issues

Check for these categories:

**Security Issues (Critical)**
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization flaws
- Sensitive data exposure
- Insecure dependencies

**Code Quality Issues**
- Code complexity (cyclomatic complexity)
- Readability and maintainability
- DRY violations
- SOLID principle violations

**Performance Issues**
- Inefficient algorithms (O(n²) when O(n) possible)
- Memory leaks
- Unnecessary database queries
- Missing caching opportunities

### Step 4: Generate Report

Produce a structured review report:

```markdown
# Code Review Report

## Executive Summary
[Brief overview: files reviewed, major findings, risk level]

## Critical Issues (Must Fix)
- [ ] Issue 1: [description]
  - **File**: [path:line]
  - **Risk**: High/Medium/Low
  - **Fix**: [suggested solution]

## Warnings (Should Fix)
[List of warnings...]

## Suggestions (Nice to Have)
[List of improvements...]

## Positive Observations
[What the code does well]
```

## Language-Specific Guidelines

### Python
- Check for type hints
- Verify docstring completeness
- Review exception handling
- Check import organization
- Verify dependency pinning (requirements/pyproject)

### JavaScript/TypeScript
- Review async/await patterns
- Check error boundaries
- Verify type safety (TS)
- Review module organization

### Java
- Review exception handling
- Check thread safety and concurrency
- Verify resource management (try-with-resources)
- Review dependency versions (Maven/Gradle)

### Go
- Check error handling patterns
- Review goroutine safety
- Verify interface usage
- Check context propagation/cancellation

## Examples

### Example 1: Security Review
User: "Review auth.py for security issues"
→ Focus on authentication logic, password handling, session management

### Example 2: Full Review
User: "Review the entire src/ directory"
→ Comprehensive review of all files, prioritize by risk
```

### Skill Directory Layout (Claude Code Compatible)

Each skill may include additional files beyond `SKILL.md` for progressive disclosure:

```
my-skill/
├── SKILL.md          # required - overview and navigation
├── reference.md      # detailed docs - loaded on demand
├── examples.md       # usage examples - loaded on demand
└── scripts/
    └── helper.py     # utility script - executed, not loaded
```

### Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | ✅ | string | Unique skill identifier |
| `description` | ✅ | string | Short description for LLM matching |
| `version` | ❌ | string | Semantic version |
| `author` | ❌ | string | Skill author |
| `allowed-tools` | ❌ | list | Tools available when skill active |
| `model` | ❌ | string | Preferred LLM model |
| `resources` | ❌ | list | Additional files to load |

### Markdown Body

The markdown body contains detailed instructions that are injected into the agent's context when the skill is activated. This can include:

- Step-by-step instructions
- Decision trees
- Output format templates
- Language-specific guidelines
- Examples

---

## Core Components

### 1. SkillMetadata (Lightweight Index)

```python
# oxygent/oxy/skills/skill_metadata.py

from pydantic import BaseModel, Field
from typing import Optional, List
from pathlib import Path

class SkillMetadata(BaseModel):
    """
    Lightweight skill metadata for indexing.
    Loaded at startup, injected into system prompt.
    """

    name: str = Field(..., description="Unique skill identifier")
    description: str = Field(..., description="Short description for LLM matching")

    # Location (for on-demand loading)
    skill_path: Path = Field(..., description="Path to SKILL.md file")

    # Optional metadata (loaded from frontmatter)
    version: Optional[str] = None
    author: Optional[str] = None

    def to_prompt_entry(self) -> str:
        """Format for system prompt injection."""
        return f"- **{self.name}**: {self.description}"
```

### 2. SkillContent (Full Content)

```python
# oxygent/oxy/skills/skill_content.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from pathlib import Path

class SkillContent(BaseModel):
    """
    Full skill content, loaded on-demand when skill is invoked.
    """

    # Metadata (same as SkillMetadata)
    name: str
    description: str
    version: Optional[str] = None
    author: Optional[str] = None

    # Full content
    instructions: str = Field(..., description="Full markdown instructions")

    # Execution environment modifications
    allowed_tools: List[str] = Field(
        default_factory=list,
        description="Tools available when skill is active"
    )
    model: Optional[str] = Field(
        default=None,
        description="Preferred LLM model for this skill"
    )

    # Resources
    resources: Dict[str, str] = Field(
        default_factory=dict,
        description="Loaded resource files: filename → content"
    )

    def to_context_injection(self) -> str:
        """Format for conversation context injection."""
        injection = f"""
[SKILL ACTIVATED: {self.name}]

{self.instructions}
"""

        # Add resources if any
        if self.resources:
            injection += "\n## Skill Resources\n"
            for name, content in self.resources.items():
                injection += f"\n### {name}\n{content}\n"

        return injection
```

### 3. SkillRegistry (Discovery & Index)

```python
# oxygent/oxy/skills/skill_registry.py

from pathlib import Path
from typing import Dict, List, Optional
import yaml

class SkillRegistry:
    """
    Manages skill discovery, metadata indexing, and on-demand loading.

    Two-phase loading:
    1. Startup: Load metadata only (name + description)
    2. Runtime: Load full content when skill is invoked
    """

    def __init__(
        self,
        skill_dirs: List[str] = None,
        auto_discover: bool = True
    ):
        self.skill_dirs = skill_dirs or [
            ".oxygent/skills/",      # Project skills
            "~/.oxygent/skills/",    # User skills
        ]

        # Metadata index (lightweight, always in memory)
        self.metadata_index: Dict[str, SkillMetadata] = {}

        # Content cache (loaded on-demand)
        self._content_cache: Dict[str, SkillContent] = {}

        if auto_discover:
            self.discover_all()

    def discover_all(self) -> List[str]:
        """
        Phase 1: Discover all skills and load metadata ONLY.
        Does NOT load full content.
        """
        discovered = []

        for skill_dir in self.skill_dirs:
            path = Path(skill_dir).expanduser()
            if not path.exists():
                continue

            for skill_file in path.rglob("SKILL.md"):
                metadata = self._load_metadata_only(skill_file)
                if metadata:
                    self.metadata_index[metadata.name] = metadata
                    discovered.append(metadata.name)

        return discovered

    def _load_metadata_only(self, skill_path: Path) -> Optional[SkillMetadata]:
        """
        Load ONLY the frontmatter metadata from a SKILL.md file.
        Does not read the full markdown body.
        """
        try:
            content = skill_path.read_text()

            # Parse frontmatter only
            if not content.startswith("---"):
                return None

            parts = content.split("---", 2)
            if len(parts) < 3:
                return None

            frontmatter = yaml.safe_load(parts[1])

            return SkillMetadata(
                name=frontmatter["name"],
                description=frontmatter["description"],
                version=frontmatter.get("version"),
                author=frontmatter.get("author"),
                skill_path=skill_path,
            )
        except Exception as e:
            print(f"Warning: Failed to load skill metadata from {skill_path}: {e}")
            return None

    def load_full_content(self, skill_name: str) -> Optional[SkillContent]:
        """
        Phase 2: Load full skill content on-demand.
        Called when skill is invoked.
        """
        # Check cache first
        if skill_name in self._content_cache:
            return self._content_cache[skill_name]

        # Get metadata
        metadata = self.metadata_index.get(skill_name)
        if not metadata:
            return None

        # Load full content
        try:
            content = metadata.skill_path.read_text()
            parts = content.split("---", 2)
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()

            # Load resources if specified
            resources = {}
            if "resources" in frontmatter:
                skill_dir = metadata.skill_path.parent
                for resource_path in frontmatter["resources"]:
                    resource_file = skill_dir / resource_path
                    if resource_file.exists():
                        resources[resource_path] = resource_file.read_text()

            skill_content = SkillContent(
                name=frontmatter["name"],
                description=frontmatter["description"],
                version=frontmatter.get("version"),
                author=frontmatter.get("author"),
                instructions=body,
                allowed_tools=frontmatter.get("allowed-tools", []),
                model=frontmatter.get("model"),
                resources=resources,
            )

            # Cache for future use
            self._content_cache[skill_name] = skill_content

            return skill_content

        except Exception as e:
            print(f"Error loading skill content for {skill_name}: {e}")
            return None

    def generate_system_prompt_section(self) -> str:
        """
        Generate the skill catalog section for the agent's system prompt.
        """
        if not self.metadata_index:
            return ""

        lines = [
            "## Available Skills",
            "",
            "You have access to the following skills. When a user request",
            "matches a skill's description, invoke it using the Skill tool.",
            "",
        ]

        for metadata in self.metadata_index.values():
            lines.append(metadata.to_prompt_entry())

        lines.extend([
            "",
            "To use a skill: Call the Skill tool with the skill name.",
            "Example: Skill(name=\"code-reviewer\")",
            "",
        ])

        return "\n".join(lines)

    def list_skills(self) -> List[SkillMetadata]:
        """Return all registered skill metadata."""
        return list(self.metadata_index.values())
```

### 4. SkillTool (The Bridge)

```python
# oxygent/oxy/skills/skill_tool.py

from pydantic import Field
from oxygent.oxy import BaseTool, OxyRequest, OxyResponse, OxyState

class SkillTool(BaseTool):
    """
    The Skill tool that agents use to invoke skills.

    When invoked:
    1. Loads full skill content from registry
    2. Injects instructions into conversation context
    3. Modifies execution environment (tool permissions)
    4. Returns control to agent with enriched context
    """

    name: str = "Skill"
    desc: str = "Invoke a skill to get specialized instructions and capabilities"

    input_schema: dict = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the skill to invoke"
            }
        },
        "required": ["name"]
    }

    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """
        Execute skill invocation.

        This does NOT execute the skill's task directly.
        Instead, it loads the skill and modifies the agent's context.
        """
        skill_name = oxy_request.arguments.get("name")

        if not skill_name:
            return OxyResponse(
                state=OxyState.FAILED,
                output="Skill name is required"
            )

        # Get skill registry from MAS
        registry = self.mas.skill_registry
        if not registry:
            return OxyResponse(
                state=OxyState.FAILED,
                output="Skill registry not initialized"
            )

        # Load full skill content (on-demand)
        skill_content = registry.load_full_content(skill_name)
        if not skill_content:
            return OxyResponse(
                state=OxyState.FAILED,
                output=f"Skill '{skill_name}' not found"
            )

        # Build response with context injection
        context_injection = skill_content.to_context_injection()

        # Build execution environment modifications
        env_mods = {}
        if skill_content.allowed_tools:
            env_mods["allowed_tools"] = skill_content.allowed_tools
        if skill_content.model:
            env_mods["model"] = skill_content.model

        return OxyResponse(
            state=OxyState.COMPLETED,
            output=context_injection,
            extra={
                "skill_name": skill_name,
                "environment_modifications": env_mods,
                "context_type": "skill_injection",
            }
        )
```

### 5. Agent Integration (ReActAgent-Only in v1.0)

**Note**: v1.0 integrates skills only in `ReActAgent` to avoid context bloat. A shared mixin for non-ReAct agents is **deferred (TODO)**.

```python
# oxygent/oxy/agents/skill_aware_agent.py (Deferred: future non-ReAct support)

class SkillAwareAgentMixin:
    """
    Mixin to add skill awareness to agents.

    Responsibilities:
    1. Inject skill catalog into system prompt
    2. Handle Skill tool responses (context injection)
    3. Apply execution environment modifications
    """

    def _build_system_prompt_with_skills(self, base_prompt: str) -> str:
        """
        Enhance system prompt with skill catalog.
        Called during agent initialization.
        """
        if not self.mas or not self.mas.skill_registry:
            return base_prompt

        skill_section = self.mas.skill_registry.generate_system_prompt_section()

        if not skill_section:
            return base_prompt

        return f"{base_prompt}\n\n{skill_section}"

    def _handle_skill_response(
        self,
        skill_response: OxyResponse,
        current_context: list
    ) -> tuple:
        """
        Handle response from Skill tool invocation.

        Returns:
            (updated_context, environment_modifications)
        """
        if skill_response.extra.get("context_type") != "skill_injection":
            return current_context, {}

        # Inject skill instructions into conversation context
        context_injection = skill_response.output
        current_context.append({
            "role": "system",
            "content": context_injection
        })

        # Extract environment modifications
        env_mods = skill_response.extra.get("environment_modifications", {})

        return current_context, env_mods

    def _apply_environment_modifications(self, env_mods: dict):
        """
        Apply execution environment modifications from skill.
        """
        if "allowed_tools" in env_mods:
            # Temporarily restrict agent's tool access
            self._skill_allowed_tools = env_mods["allowed_tools"]

        if "model" in env_mods:
            # Switch to skill-preferred model
            self._skill_model = env_mods["model"]
```

---

## Integration with OxyGent

### MAS Integration

```python
# oxygent/mas.py (additions)

class MAS(BaseModel):
    # ... existing fields ...

    # Skill system
    skill_registry: Optional[SkillRegistry] = None
    skill_dirs: List[str] = Field(default_factory=lambda: [
        ".oxygent/skills/",
        "~/.oxygent/skills/",
    ])
    auto_discover_skills: bool = True

    async def __aenter__(self):
        # ... existing initialization ...

        # Initialize skill registry (metadata only)
        if self.auto_discover_skills:
            self.skill_registry = SkillRegistry(
                skill_dirs=self.skill_dirs,
                auto_discover=True
            )

            # Register the Skill tool
            skill_tool = SkillTool()
            self.add_oxy(skill_tool)

        return self

    def get_skill_catalog_prompt(self) -> str:
        """Get skill catalog for system prompt injection."""
        if not self.skill_registry:
            return ""
        return self.skill_registry.generate_system_prompt_section()
```

### ReActAgent Integration

```python
# oxygent/oxy/agents/react_agent.py (modifications)

class ReActAgent(LocalAgent):
    # ... existing fields ...

    # Skill support
    enable_skills: bool = True
    _active_skill: Optional[str] = None
    _skill_allowed_tools: Optional[List[str]] = None

    async def _build_system_prompt(self) -> str:
        """Build system prompt with skill catalog."""
        base_prompt = self.system_prompt or SYSTEM_PROMPT

        if self.enable_skills and self.mas and self.mas.skill_registry:
            skill_section = self.mas.skill_registry.generate_system_prompt_section()
            return f"{base_prompt}\n\n{skill_section}"

        return base_prompt

    async def _process_tool_response(
        self,
        tool_name: str,
        response: OxyResponse,
        messages: list
    ) -> list:
        """Process tool response, handling skill activation specially."""

        if tool_name == "Skill" and response.state == OxyState.COMPLETED:
            # Skill was invoked - inject context
            context_injection = response.output
            self._active_skill = response.extra.get("skill_name")

            # Apply environment modifications
            env_mods = response.extra.get("environment_modifications", {})
            if "allowed_tools" in env_mods:
                self._skill_allowed_tools = env_mods["allowed_tools"]

            # Inject skill instructions as system message
            messages.append({
                "role": "system",
                "content": context_injection
            })
        else:
            # Normal tool response
            messages.append({
                "role": "assistant",
                "content": f"Tool {tool_name} returned: {response.output}"
            })

        return messages

    def _get_permitted_tools(self) -> List[str]:
        """Get currently permitted tools (may be modified by active skill)."""
        if self._skill_allowed_tools:
            # Skill has restricted tool access
            return self._skill_allowed_tools
        return self.permitted_tool_name_list
```

### Sub-Agent Considerations (Deferred)

Sub-agents are **not** skill-aware in v1.0. Reserve a design hook for future work, with two candidate approaches:

- **Explicit injection**: parent agent passes selected skill context into sub-agent system prompt.
- **Shared inheritance**: sub-agent inherits a shared `SkillRegistry` and applies skill context locally.

This is intentionally deferred to avoid context bloat and performance regressions in the initial release.
**TODO**: decide between explicit injection vs shared inheritance when sub-agent support is scheduled.

---

## Skill Composition: LLM-Driven Chaining

### NOT Pipeline/Parallel - LLM Reasoning

Skills do NOT compose through code-based pipelines. Instead, composition happens through:

1. **Sequential Reasoning**: LLM naturally chains skill invocations
2. **Context Accumulation**: Each skill's output enriches context for next steps
3. **One Active Skill**: Only one skill active at a time (non-concurrent)

### Example: Multi-Skill Task

```
User: "Research AI frameworks, then write a comparison document"

Agent Reasoning:
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Match user intent to skills                              │
│         - "Research" → matches "web-researcher" skill            │
│         - "Write comparison" → matches "technical-writer" skill  │
├─────────────────────────────────────────────────────────────────┤
│ Step 2: Invoke first skill                                       │
│         Skill(name="web-researcher")                             │
│         → Context injected with research instructions            │
│         → Agent performs research using skill guidance           │
│         → Stores research results in context                     │
├─────────────────────────────────────────────────────────────────┤
│ Step 3: Skill completes, agent reasons about next step           │
│         - Research complete                                       │
│         - Now need to write comparison                           │
│         - Invoke next skill                                      │
├─────────────────────────────────────────────────────────────────┤
│ Step 4: Invoke second skill                                      │
│         Skill(name="technical-writer")                           │
│         → Context injected with writing instructions             │
│         → Agent writes document using skill guidance             │
│         → Previous research results still in context             │
├─────────────────────────────────────────────────────────────────┤
│ Step 5: Task complete                                            │
│         Both skills contributed through sequential invocation    │
└─────────────────────────────────────────────────────────────────┘
```

### Key Principle: LLM Decides Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  SKILL COMPOSITION MODEL                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ NOT THIS (Code-Based Pipeline):                              │
│     pipeline(skill1, skill2, skill3)                             │
│     parallel([skill1, skill2])                                   │
│                                                                  │
│  ✅ THIS (LLM-Driven Reasoning):                                 │
│     User Request                                                 │
│         ↓                                                        │
│     LLM Reasoning: "This needs skill A first"                    │
│         ↓                                                        │
│     Skill(name="A") → Context enriched                           │
│         ↓                                                        │
│     LLM Reasoning: "Now I need skill B"                          │
│         ↓                                                        │
│     Skill(name="B") → Context further enriched                   │
│         ↓                                                        │
│     LLM Reasoning: "Task complete"                               │
│         ↓                                                        │
│     Final Response                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
oxygent/
├── oxy/
│   ├── skills/                      # NEW: Skills module
│   │   ├── __init__.py
│   │   ├── skill_metadata.py        # Lightweight metadata class
│   │   ├── skill_content.py         # Full content class
│   │   ├── skill_registry.py        # Discovery & on-demand loading
│   │   └── skill_tool.py            # The Skill tool
│   │
│   ├── agents/
│   │   ├── react_agent.py           # MODIFIED: Skill-aware
│   │   └── local_agent.py           # Unchanged in v1.0 (skills are ReAct-only)
│   │
│   └── ...
│
├── preset_skills/                   # NEW: Built-in skills
│   ├── code-reviewer/
│   │   ├── SKILL.md
│   │   ├── reference.md
│   │   ├── examples.md
│   │   └── scripts/
│   │       └── helper.py
│   ├── web-researcher/
│   │   ├── SKILL.md
│   │   ├── reference.md
│   │   ├── examples.md
│   │   └── scripts/
│   │       └── helper.py
│   ├── summarizer/
│   │   ├── SKILL.md
│   │   ├── reference.md
│   │   ├── examples.md
│   │   └── scripts/
│   │       └── helper.py
│   └── technical-writer/
│       ├── SKILL.md
│       ├── reference.md
│       ├── examples.md
│       └── scripts/
│           └── helper.py
│
└── .oxygent/                        # Project-level configuration
    └── skills/                      # Project-specific skills
        └── custom-skill/
            ├── SKILL.md
            ├── reference.md
            ├── examples.md
            └── scripts/
                └── helper.py
```

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| SkillMetadata class | P0 | 1d | Lightweight metadata for indexing |
| SkillContent class | P0 | 1d | Full content with environment mods |
| SkillRegistry (discovery) | P0 | 2d | Metadata-only discovery at startup |
| SkillRegistry (on-demand loading) | P0 | 1d | Load full content when invoked |
| SkillTool implementation | P0 | 2d | The Skill tool for agents |
| Basic tests | P0 | 1d | Unit tests for core components |

**Deliverable**: Skills discoverable and loadable on-demand

### Phase 2: Agent Integration (Week 3-4)

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| System prompt injection | P0 | 1d | Inject skill catalog into agent prompt |
| ReActAgent skill handling | P0 | 2d | Handle Skill tool responses |
| Context injection | P0 | 1d | Inject skill instructions into context |
| Environment modification | P0 | 2d | Apply tool permissions, model selection |
| MAS integration | P0 | 1d | Initialize registry, register Skill tool |
| Integration tests | P0 | 1d | End-to-end skill invocation |

**Deliverable**: ReActAgent can invoke skills and receive context injection

**Scope note**: v1.0 is ReActAgent-only. **TODO**: evaluate non-ReAct agent and sub-agent support in a future phase.

### Phase 3: Preset Skills (Week 5-6)

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| code-reviewer skill | P1 | 2d | Code review with security focus |
| web-researcher skill | P1 | 2d | Web research and synthesis |
| summarizer skill | P1 | 1d | Document summarization |
| technical-writer skill | P1 | 2d | Technical documentation |
| Skill testing framework | P1 | 1d | Utilities for testing skills |
| Documentation | P1 | 1d | Skill authoring guide |

**Deliverable**: 4+ production-ready preset skills

### Phase 4: Polish (Week 7-8)

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| Skill caching optimization | P2 | 1d | Intelligent content caching |
| Skill versioning | P2 | 1d | Version compatibility checks |
| CLI commands | P2 | 2d | `oxygent skill list/create/test` |
| Marketplace API (design) | P2 | 2d | Skill sharing specification |
| Performance optimization | P2 | 1d | Startup time, memory usage |
| Final testing | P1 | 1d | Comprehensive test suite |

**Deliverable**: Production-ready skills system

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Metadata load time | < 50ms | Time to load all skill metadata at startup |
| Skill match accuracy | > 85% | LLM correctly selects relevant skill |
| Context injection latency | < 100ms | Time from skill invocation to context ready |
| Developer adoption | 50% | New capabilities added as skills vs tools |
| Preset skill coverage | 4+ | Number of built-in skills |

---

## Comparison: OxyGent Skills vs Claude Agent SDK

| Aspect | OxyGent Skills | Claude Agent SDK |
|--------|---------------|------------------|
| File Format | SKILL.md (compatible) | SKILL.md |
| Discovery Location | `.oxygent/skills/` | `.claude/skills/` |
| Loading Strategy | Progressive (metadata → full) | Progressive |
| Selection Mechanism | LLM semantic reasoning | LLM semantic reasoning |
| Context Injection | System message injection | Context modification |
| Environment Mods | allowed-tools, model | allowed-tools |
| Composition | LLM-driven chaining | LLM-driven |
| Concurrency | One active skill | One active skill |

---

## Appendix: Key Design Decisions

### Decision 1: Skills ≠ Tools

**Rationale**: Skills and tools serve fundamentally different purposes:
- Tools execute code (deterministic, fast)
- Skills guide behavior (LLM-interpreted, flexible)

Keeping them separate maintains clarity and allows each to evolve independently.

### Decision 2: Progressive Disclosure

**Rationale**: Loading full skill content at startup wastes memory and slows initialization. By loading metadata first and full content on-demand:
- Startup is fast (metadata only)
- Memory is conserved (load only active skills)
- Scaling is better (100s of skills possible)

### Decision 3: LLM-Driven Composition

**Rationale**: Code-based pipelines (skill1 → skill2) are rigid and require developer anticipation of all workflows. LLM-driven composition:
- Adapts to user intent dynamically
- Handles novel combinations
- Requires no new code for new workflows

### Decision 4: One Active Skill

**Rationale**: Concurrent skills would create conflicting contexts and tool permissions. Sequential activation:
- Keeps context clean
- Prevents permission conflicts
- Matches natural task flow

---

*Document generated by Claude Code Analysis*
*Version 2.0 - Corrected Architecture*
*Last updated: 2024-12-28*

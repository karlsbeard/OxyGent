"""Integration tests for the Skills system with MAS and ReActAgent.

These tests verify end-to-end skill functionality including:
- MAS initialization with skill registry
- ReActAgent skill invocation
- Context injection and environment modifications
"""

import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from oxygent.oxy.agents.react_agent import ReActAgent
from oxygent.oxy.llms import MockLLM
from oxygent.oxy.skills import SkillRegistry, SkillTool
from oxygent.schemas import Memory, Message, OxyRequest, OxyState


# ──────────────────────────────────────────────────────────────────────────────
# ❶ Fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def skill_files():
    """Create a temporary directory with test skill files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = Path(tmpdir) / "skills"
        skill_dir.mkdir()

        # Create a simple test skill
        test_skill_dir = skill_dir / "test-skill"
        test_skill_dir.mkdir()
        (test_skill_dir / "SKILL.md").write_text(
            """---
name: test-skill
description: A test skill for integration testing
version: "1.0.0"
---

# Test Skill

This is a test skill for integration testing.

## Instructions

When activated, this skill provides specific guidance for testing.
Follow these steps:
1. Read the input
2. Process it
3. Return the result
"""
        )

        # Create a skill with environment modifications
        env_skill_dir = skill_dir / "env-skill"
        env_skill_dir.mkdir()
        (env_skill_dir / "SKILL.md").write_text(
            """---
name: env-skill
description: A skill with environment modifications
version: "1.0.0"
allowed-tools:
  - Read
  - Grep

timeout: 120
---

# Environment Skill

This skill restricts available tools and sets model preferences.

## Instructions

When activated, only use Read and Grep tools.
"""
        )

        # Create a skill with resources
        resource_skill_dir = skill_dir / "resource-skill"
        resource_skill_dir.mkdir()
        (resource_skill_dir / "SKILL.md").write_text(
            """---
name: resource-skill
description: A skill with additional resources
version: "1.0.0"
resources:
  - examples.md
---

# Resource Skill

This skill includes additional resource files.
"""
        )
        (resource_skill_dir / "examples.md").write_text(
            """# Examples

## Example 1
Input: test
Output: processed

## Example 2
Input: demo
Output: verified
"""
        )

        yield skill_dir


@pytest.fixture
def mock_es_client():
    """Create a mock Elasticsearch client."""
    client = MagicMock()
    client.search = MagicMock(return_value={"hits": {"hits": []}})
    client.close = AsyncMock()
    return client


@pytest.fixture
def mock_redis_client():
    """Create a mock Redis client."""
    client = MagicMock()
    client.close = AsyncMock()
    return client


@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns simulated responses."""
    llm = MockLLM(
        name="mock_llm",
        desc="Mock LLM for testing",
    )

    # Use object.__setattr__ to bypass Pydantic validation
    response_storage = {"func": None}

    def set_response(func):
        response_storage["func"] = func

    # Override _execute to use custom response
    original_execute = llm._execute

    async def custom_execute(oxy_request):
        if response_storage["func"]:
            return response_storage["func"](oxy_request)
        return await original_execute(oxy_request)

    # Store methods in a way that bypasses Pydantic
    object.__setattr__(llm, "set_response", set_response)
    object.__setattr__(llm, "_execute", custom_execute)

    return llm


@pytest.fixture
def mock_mas(skill_files, mock_es_client, mock_redis_client, mock_llm):
    """Create a mock MAS with skill registry."""
    mas = MagicMock()
    mas.name = "test_mas"
    mas.oxy_name_to_oxy = {}
    mas.es_client = mock_es_client
    mas.redis_client = mock_redis_client
    mas.skill_dirs = [str(skill_files)]
    mas.auto_discover_skills = True

    # Create skill registry
    mas.skill_registry = SkillRegistry(
        skill_dirs=mas.skill_dirs,
        auto_discover=True,
    )

    # Register MockLLM
    mock_llm.set_mas(mas)
    mas.oxy_name_to_oxy["mock_llm"] = mock_llm

    # Create and register Skill tool
    skill_tool = SkillTool()
    skill_tool.set_registry(mas.skill_registry)
    skill_tool.set_mas(mas)
    mas.oxy_name_to_oxy["Skill"] = skill_tool

    # Mock is_agent method
    def is_agent(name):
        return isinstance(mas.oxy_name_to_oxy.get(name), ReActAgent)

    mas.is_agent = is_agent

    # Mock get_oxy method
    def get_oxy(name):
        return mas.oxy_name_to_oxy.get(name)

    mas.get_oxy = get_oxy

    return mas


@pytest.fixture
def react_agent(mock_mas, mock_llm):
    """Create a ReActAgent for testing."""
    agent = ReActAgent(
        name="test_agent",
        desc="Test ReAct Agent",
        llm_model="mock_llm",
        max_react_rounds=5,
        enable_skills=True,
    )
    agent.set_mas(mock_mas)
    agent.permitted_tool_name_list = ["Skill", "mock_llm"]
    return agent


@pytest.fixture
def oxy_request(mock_mas):
    """Create a sample OxyRequest."""
    request = OxyRequest(
        arguments={"query": "test query"},
        caller="test_agent",
        caller_category="agent",
        current_trace_id="trace_123",
        node_id="node_1",
        session_name="test_session",
        call_stack=["test_agent"],
    )
    request.set_mas(mock_mas)

    # Override get_short_memory to return empty memory (bypass Pydantic)
    original_get_short_memory = request.get_short_memory

    def get_short_memory_override():
        return []

    object.__setattr__(request, "get_short_memory", get_short_memory_override)

    # Override get_query (bypass Pydantic)
    def get_query_override():
        return request.arguments.get("query", "")

    object.__setattr__(request, "get_query", get_query_override)

    # Mock call method (bypass Pydantic)
    async def mock_call(callee, arguments, **kwargs):
        oxy = mock_mas.get_oxy(callee)
        if oxy:
            return await oxy._execute(
                OxyRequest(
                    arguments=arguments,
                    caller=callee,
                    callee=callee,
                    current_trace_id=request.current_trace_id,
                )
            )
        # Default response for LLM calls
        from oxygent.schemas import OxyResponse
        return OxyResponse(
            state=OxyState.COMPLETED,
            output='{"tool_name": "test", "arguments": {}}',
        )

    object.__setattr__(request, "call", mock_call)

    return request


# ──────────────────────────────────────────────────────────────────────────────
# ❷ MAS Integration Tests
# ──────────────────────────────────────────────────────────────────────────────


def test_mas_skill_registry_initialization(skill_files):
    """Test that MAS initializes skill registry correctly."""
    registry = SkillRegistry(skill_dirs=[str(skill_files)], auto_discover=True)

    assert len(registry) == 3
    assert "test-skill" in registry
    assert "env-skill" in registry
    assert "resource-skill" in registry


def test_mas_skill_registry_metadata_only(skill_files):
    """Test that skill registry only loads metadata at startup."""
    registry = SkillRegistry(skill_dirs=[str(skill_files)], auto_discover=True)

    # Metadata should be loaded
    assert "test-skill" in registry.metadata_index
    metadata = registry.metadata_index["test-skill"]
    assert metadata.name == "test-skill"
    assert metadata.description == "A test skill for integration testing"

    # Content cache should be empty initially
    assert len(registry._content_cache) == 0


def test_mas_skill_catalog_generation(skill_files):
    """Test generating skill catalog for system prompt."""
    registry = SkillRegistry(skill_dirs=[str(skill_files)], auto_discover=True)
    catalog = registry.generate_system_prompt_section()

    assert "## Available Skills" in catalog
    assert "**test-skill**" in catalog
    assert "**env-skill**" in catalog
    assert "**resource-skill**" in catalog
    assert "Skill(name=" in catalog


# ──────────────────────────────────────────────────────────────────────────────
# ❸ ReActAgent System Prompt Tests
# ──────────────────────────────────────────────────────────────────────────────


def test_react_agent_build_instruction_with_skills(react_agent):
    """Test that ReActAgent includes skill catalog in system prompt."""
    arguments = {"query": "test query", "tools_description": "Mock tools"}
    instruction = react_agent._build_instruction(arguments)

    # Should contain skill catalog
    assert "## Available Skills" in instruction
    assert "**test-skill**" in instruction
    assert "**env-skill**" in instruction
    assert "**resource-skill**" in instruction


def test_react_agent_build_instruction_without_skills(mock_mas, mock_llm):
    """Test ReActAgent without skills enabled."""
    agent = ReActAgent(
        name="test_agent",
        llm_model="mock_llm",
        enable_skills=False,
    )
    agent.set_mas(mock_mas)

    arguments = {"query": "test", "tools_description": "tools"}
    instruction = agent._build_instruction(arguments)

    # Should NOT contain skill catalog
    assert "## Available Skills" not in instruction


def test_react_agent_build_instruction_no_registry(mock_mas, mock_llm):
    """Test ReActAgent when skill registry is not available."""
    mock_mas.skill_registry = None

    agent = ReActAgent(
        name="test_agent",
        llm_model="mock_llm",
        enable_skills=True,
    )
    agent.set_mas(mock_mas)

    arguments = {"query": "test", "tools_description": "tools"}
    instruction = agent._build_instruction(arguments)

    # Should NOT contain skill catalog
    assert "## Available Skills" not in instruction


# ──────────────────────────────────────────────────────────────────────────────
# ❹ Skill Tool Invocation Tests
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_skill_tool_invocation(mock_mas):
    """Test invoking a skill through the Skill tool."""
    skill_tool = mock_mas.get_oxy("Skill")

    request = OxyRequest(
        arguments={"name": "test-skill"},
        caller="test",
        callee="Skill",
        current_trace_id="trace_123",
    )
    request.set_mas(mock_mas)

    response = await skill_tool._execute(request)

    assert response.state == OxyState.COMPLETED
    assert "[SKILL ACTIVATED: test-skill]" in response.output
    assert "Test Skill" in response.output
    assert response.extra["skill_name"] == "test-skill"
    assert response.extra["context_type"] == "skill_injection"


@pytest.mark.asyncio
async def test_skill_tool_with_environment_mods(mock_mas):
    """Test skill invocation with environment modifications."""
    skill_tool = mock_mas.get_oxy("Skill")

    request = OxyRequest(
        arguments={"name": "env-skill"},
        caller="test",
        callee="Skill",
        current_trace_id="trace_123",
    )
    request.set_mas(mock_mas)

    response = await skill_tool._execute(request)

    assert response.state == OxyState.COMPLETED
    env_mods = response.extra["environment_modifications"]
    assert env_mods["allowed_tools"] == ["Read", "Grep"]
    assert env_mods["model"] == "claude-3-opus"
    assert env_mods["timeout"] == 120


@pytest.mark.asyncio
async def test_skill_tool_with_resources(mock_mas):
    """Test skill invocation with resource files."""
    skill_tool = mock_mas.get_oxy("Skill")

    request = OxyRequest(
        arguments={"name": "resource-skill"},
        caller="test",
        callee="Skill",
        current_trace_id="trace_123",
    )
    request.set_mas(mock_mas)

    response = await skill_tool._execute(request)

    assert response.state == OxyState.COMPLETED
    assert "## Skill Resources" in response.output
    assert "### examples.md" in response.output
    assert "# Examples" in response.output


@pytest.mark.asyncio
async def test_skill_tool_nonexistent_skill(mock_mas):
    """Test invoking a skill that doesn't exist."""
    skill_tool = mock_mas.get_oxy("Skill")

    request = OxyRequest(
        arguments={"name": "nonexistent"},
        caller="test",
        callee="Skill",
        current_trace_id="trace_123",
    )
    request.set_mas(mock_mas)

    response = await skill_tool._execute(request)

    assert response.state == OxyState.FAILED
    assert "not found" in response.output


# ──────────────────────────────────────────────────────────────────────────────
# ❺ ReActAgent Skill Response Handling Tests
# ──────────────────────────────────────────────────────────────────────────────


def test_react_agent_handle_skill_response(react_agent, oxy_request):
    """Test skill response handling in ReActAgent."""
    from oxygent.schemas import OxyResponse

    # Create a mock skill response
    skill_response = OxyResponse(
        state=OxyState.COMPLETED,
        output="[SKILL ACTIVATED: test-skill]\n\nInstructions here",
        extra={
            "skill_name": "test-skill",
            "context_type": "skill_injection",
            "environment_modifications": {"allowed_tools": ["Skill"]},
        },
    )

    react_memory = Memory()
    temp_memory = Memory()
    oxy_request.arguments[react_agent.tools_placeholder] = "original tools"

    # Handle the skill response
    result = react_agent._handle_skill_response(
        "Skill", skill_response, oxy_request, react_memory, temp_memory
    )

    assert result is True
    assert react_agent.active_skill == "test-skill"
    assert react_agent.skill_allowed_tools == ["Skill"]
    assert react_agent.pending_skill_context == skill_response.output
    assert "Tool: Skill" in oxy_request.arguments[react_agent.tools_placeholder]


def test_react_agent_handle_non_skill_response(react_agent, oxy_request):
    """Test handling non-skill tool responses."""
    from oxygent.schemas import OxyResponse

    response = OxyResponse(
        state=OxyState.COMPLETED,
        output="Tool output",
    )

    react_memory = Memory()
    temp_memory = Memory()

    result = react_agent._handle_skill_response(
        "Read", response, oxy_request, react_memory, temp_memory
    )

    assert result is False
    assert react_agent.active_skill is None


def test_react_agent_reset_skill_state(react_agent):
    """Test resetting skill state."""
    react_agent.active_skill = "test-skill"
    react_agent.skill_allowed_tools = ["Read", "Grep"]

    react_agent._reset_skill_state()

    assert react_agent.active_skill is None
    assert react_agent.skill_allowed_tools is None


def test_react_agent_permitted_tools_with_skill_override(react_agent):
    """Test getting permitted tools with skill override."""
    # Normal case - no skill active
    assert react_agent._get_permitted_tools_with_skill_override() == [
        "Skill",
        "mock_llm",
    ]

    # With skill override
    react_agent.skill_allowed_tools = ["Read"]
    assert react_agent._get_permitted_tools_with_skill_override() == ["Read"]


# ──────────────────────────────────────────────────────────────────────────────
# ❻ End-to-End Integration Tests
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_full_skill_invocation_flow(react_agent, mock_llm, oxy_request):
    """Test complete flow from skill invocation to context injection."""
    from oxygent.schemas import OxyResponse

    call_count = [0]
    skill_invoked = [False]
    original_timeout = mock_llm.timeout

    async def mock_llm_execute(oxy_request):
        call_count[0] += 1
        messages = oxy_request.arguments.get("messages", [])

        # First call - LLM should invoke the skill
        if call_count[0] == 1:
            # Check if skill catalog is in the system prompt
            system_msg = messages[0] if messages else None
            assert system_msg and system_msg.get("role") == "system"
            assert "## Available Skills" in system_msg.get("content", "")

            return OxyResponse(
                state=OxyState.COMPLETED,
                output='{"tool_name": "Skill", "arguments": {"name": "env-skill"}}',
            )

        # Second call - LLM should see the skill context
        elif call_count[0] == 2:
            # Check that skill context was injected
            system_msgs = [m for m in messages if m.get("role") == "system"]
            assert any("[SKILL ACTIVATED: env-skill]" in str(m) for m in system_msgs)
            assert oxy_request.arguments.get("model") == "claude-3-opus"
            assert mock_llm.timeout == 120

            skill_invoked[0] = True
            return OxyResponse(
                state=OxyState.COMPLETED,
                output="Task completed successfully with skill guidance.",
            )

        return OxyResponse(
            state=OxyState.COMPLETED,
            output="Done",
        )

    mock_llm._execute = mock_llm_execute

    response = await react_agent._execute(oxy_request)

    assert response.state == OxyState.COMPLETED
    assert call_count[0] >= 2
    assert skill_invoked[0] is True
    assert mock_llm.timeout == original_timeout


# ──────────────────────────────────────────────────────────────────────────────
# ❼ Edge Case Tests
# ──────────────────────────────────────────────────────────────────────────────


def test_skill_registry_empty_skills():
    """Test skill registry with no skills."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SkillRegistry(skill_dirs=[tmpdir], auto_discover=True)
        assert len(registry) == 0
        assert registry.generate_system_prompt_section() == ""


def test_skill_registry_caching(skill_files):
    """Test that content is cached after first load."""
    registry = SkillRegistry(skill_dirs=[str(skill_files)], auto_discover=True)

    # First load - from disk
    content1 = registry.load_full_content("test-skill")
    assert content1 is not None

    # Second load - from cache
    content2 = registry.load_full_content("test-skill")
    assert content1 is content2  # Same object

    # Verify cache has content
    assert "test-skill" in registry._content_cache

    # Clear cache
    registry.clear_cache()
    assert len(registry._content_cache) == 0


def test_react_agent_skill_persistence_across_rounds(react_agent):
    """Test that skill state persists across ReAct rounds."""
    react_agent.active_skill = "test-skill"
    react_agent.skill_allowed_tools = ["Read"]

    # After multiple rounds, skill should still be active
    assert react_agent.active_skill == "test-skill"
    assert react_agent.skill_allowed_tools == ["Read"]

    # Reset should clear state
    react_agent._reset_skill_state()
    assert react_agent.active_skill is None
    assert react_agent.skill_allowed_tools is None

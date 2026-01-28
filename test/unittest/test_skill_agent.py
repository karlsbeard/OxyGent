import textwrap
from unittest.mock import AsyncMock

import pytest

from oxygent.oxy.agents.skill_agent import SkillAgent
from oxygent.oxy.skills import SkillRegistry, SkillTool
from oxygent.oxy.skills.skill_selector import SkillSelection
from oxygent.oxy.base_tool import BaseTool
from oxygent.schemas import OxyRequest, OxyResponse, OxyState


class DummyMAS:
    def __init__(self):
        self.oxy_name_to_oxy = {}
        self.vearch_client = AsyncMock()
        self.es_client = AsyncMock()
        self.background_tasks = set()
        self.skill_registry = None

    @staticmethod
    def is_agent(name: str) -> bool:
        return name.startswith("agent_")


class MockLLMTool(BaseTool):
    name: str = "mock_llm"
    desc: str = "Stub LLM"
    category: str = "llm"
    is_multimodal_supported: bool = False

    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        return OxyResponse(
            state=OxyState.COMPLETED, output="llm-output", oxy_request=oxy_request
        )


def _write_skill(path, *, name: str, description: str, body: str):
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        textwrap.dedent(
            f"""\
            ---
            name: {name}
            description: {description}
            ---

            {body}
            """
        ),
        encoding="utf-8",
    )


@pytest.fixture
def patched_config(monkeypatch):
    monkeypatch.setattr(
        "oxygent.oxy.agents.local_agent.Config.get_vearch_config",
        lambda: None,
        raising=True,
    )
    monkeypatch.setattr(
        "oxygent.oxy.agents.local_agent.Config.get_live_prompt_is_active",
        lambda: False,
        raising=True,
    )


@pytest.mark.asyncio
async def test_manual_skill_activation_injects_context_and_rewrites_query(
    patched_config, tmp_path
):
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir / "demo-skill",
        name="demo-skill",
        description="demo",
        body="Use this skill. Args: $ARGUMENTS",
    )

    mas = DummyMAS()
    mas.skill_registry = SkillRegistry(skill_dirs=[str(skills_dir)], auto_discover=True)

    agent = SkillAgent(name="agent_master", llm_model="mock_llm", enable_selector=False)
    agent.set_mas(mas)

    skill_tool = SkillTool()
    skill_tool.set_mas(mas)
    skill_tool.set_registry(mas.skill_registry)

    mas.oxy_name_to_oxy["mock_llm"] = MockLLMTool()
    mas.oxy_name_to_oxy["Skill"] = skill_tool
    mas.oxy_name_to_oxy[agent.name] = agent

    req = OxyRequest(
        arguments={"query": "/demo-skill do something"},
        caller="user",
        caller_category="user",
        callee=agent.name,
        callee_category="agent",
        current_trace_id="trace123",
        is_send_message=False,
        is_save_history=False,
    )
    req.mas = mas

    req2 = await agent._before_execute(req)
    assert req2.arguments["query"] == "do something"
    assert "[SKILL ACTIVATED: demo-skill]" in req2.arguments.get("additional_prompt", "")
    assert "Args: do something" in req2.arguments.get("additional_prompt", "")
    assert req2.arguments.get("_skill_activation", {}).get("invocation_source") == "user"


@pytest.mark.asyncio
async def test_selector_activation_invokes_skill_tool(monkeypatch, patched_config, tmp_path):
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir / "demo-skill",
        name="demo-skill",
        description="demo",
        body="Selector used.",
    )

    async def _fake_select_skill(**kwargs):
        return SkillSelection(selected_skill="demo-skill", confidence=0.9, reason="ok")

    monkeypatch.setattr(
        "oxygent.oxy.agents.skill_agent.select_skill",
        _fake_select_skill,
        raising=True,
    )

    mas = DummyMAS()
    mas.skill_registry = SkillRegistry(skill_dirs=[str(skills_dir)], auto_discover=True)

    agent = SkillAgent(name="agent_master", llm_model="mock_llm", enable_selector=True)
    agent.set_mas(mas)

    skill_tool = SkillTool()
    skill_tool.set_mas(mas)
    skill_tool.set_registry(mas.skill_registry)

    mas.oxy_name_to_oxy["mock_llm"] = MockLLMTool()
    mas.oxy_name_to_oxy["Skill"] = skill_tool
    mas.oxy_name_to_oxy[agent.name] = agent

    req = OxyRequest(
        arguments={"query": "please help"},
        caller="user",
        caller_category="user",
        callee=agent.name,
        callee_category="agent",
        current_trace_id="trace123",
        is_send_message=False,
        is_save_history=False,
    )
    req.mas = mas

    req2 = await agent._before_execute(req)
    assert "[SKILL ACTIVATED: demo-skill]" in req2.arguments.get("additional_prompt", "")
    assert req2.arguments.get("_skill_activation", {}).get("invocation_source") == "selector"
    assert req2.arguments.get("_skill_selection", {}).get("selected_skill") == "demo-skill"


@pytest.mark.asyncio
async def test_manual_overrides_selector(monkeypatch, patched_config, tmp_path):
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir / "demo-skill",
        name="demo-skill",
        description="demo",
        body="Manual.",
    )

    async def _boom(**kwargs):
        raise AssertionError("selector should not run")

    monkeypatch.setattr("oxygent.oxy.agents.skill_agent.select_skill", _boom, raising=True)

    mas = DummyMAS()
    mas.skill_registry = SkillRegistry(skill_dirs=[str(skills_dir)], auto_discover=True)

    agent = SkillAgent(name="agent_master", llm_model="mock_llm", enable_selector=True)
    agent.set_mas(mas)

    skill_tool = SkillTool()
    skill_tool.set_mas(mas)
    skill_tool.set_registry(mas.skill_registry)

    mas.oxy_name_to_oxy["mock_llm"] = MockLLMTool()
    mas.oxy_name_to_oxy["Skill"] = skill_tool
    mas.oxy_name_to_oxy[agent.name] = agent

    req = OxyRequest(
        arguments={"query": "/demo-skill task"},
        caller="user",
        caller_category="user",
        callee=agent.name,
        callee_category="agent",
        current_trace_id="trace123",
        is_send_message=False,
        is_save_history=False,
    )
    req.mas = mas

    req2 = await agent._before_execute(req)
    assert req2.arguments["query"] == "task"
    assert req2.arguments.get("_skill_activation", {}).get("invocation_source") == "user"

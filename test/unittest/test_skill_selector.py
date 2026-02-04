from pathlib import Path

import pytest

from oxygent.oxy.skills.skill_metadata import SkillMetadata
from oxygent.oxy.skills.skill_selector import select_skill
from oxygent.schemas import OxyRequest


@pytest.mark.asyncio
async def test_select_skill_heuristic_skill_creation_routes_to_skill_creator_without_llm(
    monkeypatch,
):
    async def _boom(*args, **kwargs):
        raise AssertionError("LLM should not be called for heuristic skill-creator selection")

    monkeypatch.setattr("oxygent.schemas.OxyRequest.call", _boom, raising=True)

    req = OxyRequest(
        arguments={"query": "dummy"},
        caller="user",
        caller_category="user",
        current_trace_id="trace123",
        is_send_message=False,
        is_save_history=False,
    )

    skills = [
        SkillMetadata(
            name="skill-creator",
            description="Guide for creating effective skills",
            skill_path=Path("/tmp/skill-creator/SKILL.md"),
        )
    ]

    sel = await select_skill(
        oxy_request=req,
        llm_model="mock_llm",
        skills=skills,
        query="帮我创建一个新的skill，名字叫 hello-skill",
        max_candidates=30,
        min_confidence=0.6,
    )

    assert sel.selected_skill == "skill-creator"
    assert sel.confidence >= 0.9
